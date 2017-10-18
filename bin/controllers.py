from math import atan2

class GenericController(object):
    def __init__(self,period=0.05,pid_gains=[0.002,0,0.00],digital_gains=[0.01]):
        self.period = float(period)
        self.pid_gains = pid_gains
        self.digital_gains = digital_gains

    def control(self,error,old_error,old_output,speed):
        output = error * self.pid_gains[0] + old_error * self.pid_gains[1] - old_output * self.pid_gains[2] - speed * self.digital_gains[0]
        if output > 1.0:
            output = 1.0
        elif output < -1.0:
            output = -1.0
        if abs(error) > 3:
            scaled_output = abs(output) * 0.6 + 0.4 # deadzone correction
        elif abs(speed) < 2:
            scaled_output = 0
        else:
            scaled_output = output
        if output < 0:
            scaled_output = -scaled_output
        return [scaled_output,-scaled_output]

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
