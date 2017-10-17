from proxy_xbee import NMEAParser
import types

class GenericController(object):
    def __init__(self,period=0.05,pid_gains=[1.0,0.01,0.0]):
        self.period = float(period)
        self.gains = pid_gains

    def control(self,error,old_error,old_output):
        output = error * pid_gains[0] - error * pid_gains[1] + old_output * self.pid_gains[2]
        return output

class SpeedController(GenericController):
    def __init__(self,speed_control_period,speed_control_gains):
        
class ASVController(GenericController):
    def __init__(self,deviceid,asvid,heading_control_period,heading_control_gains,speed_control_period,speed_control_gains):
        self.parser = NMEAParser(deviceid,asvid)
        self.gains = pid_gains
        self.telemetry = types.Telemetry(latitude=0,longitude=0,heading=0)
        self.vehiclestate = types.VehicleState(velocity=0)
        self.controlstate = types.ControlState(heading=0,speed=0)
        self.headingcontroller = types.GenericController(heading_control_period,heading_control_gains)
        self.speedcontroller = types.GenericController(speed_control_period,speed_control_gains)

    def update_state(self):
        old_telemetry = self.telemetry
        self.telemetry = self.parser.get_telemetry()
        self.vehiclestate.estimate(old_telemetry,telemetry)

    def control(self):
        headingcontroller(heading,telemetry)
        speedcontroller(speed,self.vehiclestate.velocity)
        return


class Navigator(object):
    def __init__(self):

    def update(self):

    return control_command
