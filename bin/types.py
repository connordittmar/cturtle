import re
import sys
from math import sqrt
from helpers import get_speed,get_ang_vel, force2pwm

class InputKeys(object):
    def __init__(self):
        self.w = "U"
        self.a = "U"
        self.s = "U"
        self.d = "U"


class BaseType(object):
    """ BaseType is a simple base class which provides basic functions.

    The attributes are obtained from the 'attrs' property, which should be
    defined by subclasses.
    """

    # Subclasses should override.
    attrs = []

    def __eq__(self, other):
        """Compares two objects."""
        for attr in self.attrs:
            if self.__dict__[attr] != other.__dict__[attr]:
                return False
        return True

    def __repr__(self):
        """Gets string encoding of object."""
        return "%s(%s)" % (self.__class__.__name__,
                           ', '.join('%s=%s' % (attr, self.__dict__[attr])
                                     for attr in self.attrs))

    def __unicode__(self):
        """Gets unicode encoding of object."""
        return unicode(self.__str__())

    def serialize(self):
        """Serialize the current state of the object."""
        serial = {}
        for attr in self.attrs:
            data = self.__dict__[attr]
            if isinstance(data, BaseType):
                serial[attr] = data.serialize()
            elif isinstance(data, list):
                serial[attr] = [d.serialize() for d in data]
            elif data is not None:
                serial[attr] = data
        return serial

    @classmethod
    def deserialize(cls, d):
        """Deserialize the state of the object."""
        if isinstance(d, cls):
            return d
        else:
            return cls(**d)

class Position(BaseType):

    attrs = ['pos_x','pos_y']

    def __init__(self,pos_x,pos_y):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)

class Waypoint(BaseType):
    """Waypoint consisting of order, lat, long

    Attributes:
        order: an ID giving place of wp in stack
        position: list [x,y] coordinates of location in basin

    Raises:
        ValueError: Argument not convertable to int
        or float
    """

    attrs = ['order','pos_x','pos_y']

    def __init__(self, order, pos_x, pos_y):
        self.order = int(order)
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)

class Telemetry(BaseType):
    """Platform Telemetry at a point in time.

    Attributes:
        latitude: Latitude in meters from origin of optitrack system.
        longitude: Longitude in meters from origin of optitrack system.
        heading: Heading in degrees from i axis of optitrack system (0-360).

    Raises:
        ValueError: Argument not convertable to float.
    """

    attrs = ['pos_x','pos_y','heading','timestamp']

    def __init__(self,pos_x=0,pos_y=0,heading=0,timestamp=1):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.heading = float(heading)
        self.timestamp = float(timestamp)

class VehicleState(BaseType):
    """Platform state estimation

    Attributes:
        velocity: Velocity of vehicle in meters/sec
    """

    attrs = ['pos_x','pos_y','heading','speed','ang_vel']

    def __init__(self,pos_x=0,pos_y=0,heading=0,speed=0,ang_vel=0):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.heading = float(heading)
        self.speed = float(speed)
        self.ang_vel = float(ang_vel)

    def update(self,telemetry,telemetry_last):
        self.pos_x = telemetry.pos_x
        self.pos_y = telemetry.pos_y
        self.heading = telemetry.heading
        self.speed = get_speed(telemetry,telemetry_last)
        self.ang_vel = get_ang_vel(telemetry,telemetry_last)

class StationaryObstacle(BaseType):
    """A fixed obstacle.

    Obstacle is treated as a cylinder with location and radius.

    Attributes:
        latitude:
        longitude:
        radius:
    Raises:
        ValueError: Argument not convertable to float.
    """

    attrs = ['pos_x','pos_y','radius']

    def __init__(self,pos_x,pos_y,radius):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.radius = float(radius)

class Mission(BaseType):
    """Mission Details for payload.

    Attributes:
        home_pos: LocalPosition of the start point
        mission_waypoints: list of waypoints to travel
    """

    attrs = ['id','active','home_pos','mission_waypoints']

    def __init__(self,id,active,home_pos,mission_waypoints):
        self.id = int(id)
        self.active = bool(active)
        self.home_pos = Position.deserialize(home_pos)
        self.mission_waypoints = [
            Waypoint.deserialize(mw) for mw in mission_waypoints
        ]
