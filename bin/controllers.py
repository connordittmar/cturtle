from math import atan2

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
    def __init__(self,K1=.2,K2=0.00):
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
    def __init__(self,K=1,du=0.07,m=1.19):
        self.K = K
        self.du = du
        self.m = m

    def control(self,speed_error,speed):
        output = self.du*speed + self.K*speed_error / self.m
        return output

class Navigator(object):
    def __init__(self):
        self.wp_index = 0
        self.location = [0,0]

    def read_waypoints(self,waypoints):
        self.wp_list = waypoints

    def navigate(self):
        desired_heading = self.get_heading_to_wp()

    def get_heading_to_wp(self):
        current_wp = self.wp_list[self.wp_index]
        vector_to_wp = [current_wp[0]-self.location[0],current_wp[1]-self.location[1]]
        heading_to_wp = atan2(vector_to_wp[1],vector_to_wp[0])
        return heading_to_wp
