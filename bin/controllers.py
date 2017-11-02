from math import atan2, sqrt, pi

class GenericController(object):
    """ Generic PID controller for SISO system
    """
    def __init__(self,pid_gains=[1,0.018],force_gain=0):
        self.pid_gains = pid_gains
        self.force_gain = force_gain

    def control(self,error,old_error,old_output):
        """Usage: pwms = controller.control(error,old_error,old_output)
        """
        error = error/180*3.14159
        output = error * self.pid_gains[0] + old_error * self.pid_gains[1] + old_output * self.force_gain
        return output

class GenericStateController(object):
    """ Generic SS controller for MIMO system
    """
    def __init__(self,K1=.2,K2=0.001):
        self.K1 = K1
        self.K2 = K2

    def control(self,error,speed):
        """Usage: pwms = controller.control(error,old_error,old_output)
        """
        error = error/180*3.14159
        output = error * self.K1 - speed * self.K2
        return output

class SpeedController(object):
    """
    State Spaceish speed control yielding a needed forward force
    """
    def __init__(self,K=0.6,du=0.07,m=1.19):
        self.K = K
        self.du = du
        self.m = m

    def control(self,speed_error,speed):
        output = self.du*speed + self.K*speed_error / self.m
        return output

class WaypointController(object):
    def __init__(self,wps):
        self.wp_index = 0
        self.wp_list = wps

    def add_waypoints(self,waypoints):
        self.wp_list = waypoints

    def navigate(self,asv_location):
        dist_to_next_wp = self.get_distance_to_wp(asv_location)
        if dist_to_next_wp < 0.3:
            if self.wp_index == (len(self.wp_list) - 1):
                self.wp_index = 0 #Consider WP completed, move to next WP
            else:
                self.wp_index += 1
        desired_heading = self.get_heading_to_wp(asv_location)
        des_speed = self.get_distance_to_wp(asv_location) * 0.8
        if des_speed > 0.5:
            des_speed = 0.5
        return [desired_heading,des_speed]

    def get_heading_to_wp(self,location):
        current_wp = self.wp_list[self.wp_index]
        vector_to_wp = [current_wp[0]-location[0],current_wp[1]-location[1]]
        heading_to_wp = atan2(vector_to_wp[1],vector_to_wp[0])
        return heading_to_wp*180/pi

    def get_distance_to_wp(self,location):
        current_wp = self.wp_list[self.wp_index]
        distance = sqrt((current_wp[0]-location[0])**2+(current_wp[1]-location[1])**2)
        return distance
