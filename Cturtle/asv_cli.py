import time
from concurrent.futures import ThreadPoolExecutor
from math import sin, cos
from bin import GenericController, UDPcomms,

class ClientHandler(object):
    def __init__(self):
        self.communicator = UDPcomms(remoteport=8001,localport=8000)
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.heading_controller = GenericController()
        self.desired_heading = 270
        self.old_vars = {'error':0.0,'pwms':[0.0,0.0],'timestamp':time.time()}
        self.control_mode = 'auto'

    def compute_heading_error(self):
        # Computes heading error with updated class variables and returns the error value
        error = self.desired_heading - self.telemetry.heading
        if error > 180:
            error = error - 360
        elif error < -180:
            error = error + 360
        self.error = error

    def get_telemetry(self):
        packet = self.executor.submit(self.communicator.receive())
        try:
            telemetry = self.parse_telemetry(packet.result())
            return telemetry
        except Exception as exc:
            print('Exception: %s' % exc)

    def parse_telemetry(self,packet):
        parsed = packet.split('$')[1].split(',')
        telemetry = Telemetry(position=[float(parsed[0]),float(parsed[1])],heading=long(parsed[2]),timestamp=time.time())
        return telemetry

    def send_control_signal(self):
        control_signal = ("$%f,%f" % (self.pwms[0],self.pwms[1]))
        self.communicator.send(control_signal)
        

    def age_state(self):
        self.old_vars['error'] = self.error
        self.old_vars['pwms'] = self.pwms
        self.old_vars['timestamp'] = self.telemetry.timestamp

    def set_control_mode(self,mode):
        self.control_mode = mode
