from proxy_xbee import NMEAParser
import types

class Controller(object):
    def __init__(self,deviceid,asvid,controlperiod=0.05,pid_gains=[1.0,0.01,0.0]):
        self.parser = NMEAParser(deviceid,asvid)
        self.gains = pid_gains
        self.telemetry = types.Telemetry(latitude=0,longitude=0,heading=0)
        self.vehiclestate = type.VehicleState(velocity=0)

    def update_state(self):
        old_telemetry = self.telemetry
        self.telemetry = self.parser.get_telemetry()
        self.vehiclestate.estimate(old_telemetry,telemetry)

    def control(self):
        heading

class Navigator(object):
    def
