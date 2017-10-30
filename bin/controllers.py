from math import atan2

class GenericController(object):
    def __init__(self,pid_gains=[0.40396,0.008491],force_gain=1.0869):
        self.pid_gains = pid_gains
        self.force_gain = force_gain

    def control(self,error,old_error,old_output):
        output = error * self.pid_gains[0] + old_error * self.pid_gains[1] + old_output * self.force_gain
        print output
        return [self.force2pwm(output,'left'),self.force2pwm(-output,'right')]

    def force2pwm(self,force,motor):
        if motor == 'left':
            if force >= 0:
                pwm = -0.0207*force**2 + 0.579*force + 0.2512
            else:
                pwm = 0.5154*force**2 + 1.3465*force -0.1741
        if motor == 'right':
            if force >= 0:
                pwm = -0.2458*force**2 + 1.3465*force - 0.1741
            else:
                pwm = 0.8796*force**2 + 1.8056*force - 0.0972
        if pwm > 1:
            pwm = 1
        elif pwm < -1:
            pwm = -1
        return pwm

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
