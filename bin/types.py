import re
import sys
from math import sqrt

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
            if isinstance(data, ClientBaseType):
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

class LocalPosition(BaseType):
    """Local position in 'latitude' and 'longitude'

    Attributes:
        latitude: Latitude in meters
        Longitude: Longitude in meters

    Raises:
        ValueError: Argument not convertable to float.
    """

    attrs = ['latitude','longitude']

    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

class Waypoint(BaseType):
    """Waypoint consisting of order, lat, long

    Attributes:
        order: an ID giving place of wp in stack
        latitude: coordinates in basin in meters
        longitude: coordinates in basin in meters

    Raises:
        ValueError: Argument not convertable to int
        or float
    """

    def __init__(self, order, latitude, longitude):
        self.order = int(order)
        self.latitude = float(latitude)
        self.longitude = float(longitude)

class Telemetry(BaseType):
    """Platform Telemetry at a point in time.

    Attributes:
        latitude: Latitude in meters from origin of optitrack system.
        longitude: Longitude in meters from origin of optitrack system.
        heading: Heading in degrees from i axis of optitrack system (0-360).

    Raises:
        ValueError: Argument not convertable to float.
    """

    attrs = ['latitude', 'longitude', 'heading']

    def __init__(self,position,heading,timestamp):
        self.position = position
        self.heading = float(heading)
        self.timestamp = float(timestamp)

class ControlState(BaseType):
    """Placeholder class for control variables"""
    def __init__(self,heading,speed):
        self.heading = float(heading)
        self.speed = float(speed)

class VehicleState(BaseType):
    """Platform state estimation

    Attributes:
        velocity: Velocity of vehicle in meters/sec
    """
    def __init__(self,velocity):
        self.velocity = float(velocity)

    def estimate(self,telemetry_old,telemetry):
        self.velocity = sqrt((telemetry.latitude-telemety_old.latitude)**2+(telemetry.longitude-telemetry_old.longitude)**2)/(telemetry.timestamp-telemetry_old.timestamp)

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

    attrs = ['latitude','longitude','radius']

    def __init__(self,latitude,longitude,radius):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.radius = float(radius)

class Mission(BaseType):
    """Mission Details for payload.

    Attributes:
        home_pos: LocalPosition of the start point
        mission_waypoints: list of waypoints to travel
    """

    def __init__(self,home_pos,mission_waypoints):
        self.home_pos = LocalPosition.deserialize(home_pos)
        self.mission_waypoints = [Waypoint.deserialize(mw)
                                    for mw in mission_waypoints]

class ControlCommand(BaseType):
    def __init__(self,speed,heading):
        self.speed = fload(speed)
        self.heading = float(hading)
