import time
from concurrent.futures import ThreadPoolExecutor
from math import sin, cos
from bin import GenericStateController, UDPcomms, SpeedController, WaypointController, force2pwm
from bin import VehicleState, Telemetry
import json
import requests

class ClientHandler(object):
    def __init__(self,url):
        self.url = url
        self.timeout = 10
        self.session = requests.Session()
        self.session.mount(
            'http://', requests.adapters.HTTPAdapter(max_retries=10))
        self.communicator = UDPcomms(remoteport=8001,localport=8000,timeout=1)
        self.console_connect = UDPcomms(remoteport=9001,localport=9000,timeout=1)
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.hdg_control = GenericStateController()
        self.spd_control = SpeedController()
        wps = [[15,10],[15,15],[10,15],[10,10]]
        self.telemetry = Telemetry()
        self.wp_nav = WaypointController(wps)
        self.vehicle_state = VehicleState()
        self.desired_state = VehicleState()
        self.telemetry_last = Telemetry()
        self.pwms_last = [0,0]
        self.wp_last = 0
        self.control_mode = 'auto'
        self.telem_count = 0

    def get(self, uri, **kwargs):
        """GET request to server.
        Args:
            uri: Server URI to access (without base URL).
            **kwargs: Arguments to requests.Session.get method.
        Raises:
            InteropError: Error from server.
            requests.Timeout: Request timeout.
        """
        r = self.session.get(self.url + uri, timeout=self.timeout, **kwargs)
        if not r.ok:
            print "Problem with GET."
        return r

    def post(self, uri, **kwargs):
        """POST request to server.
        Args:
            uri: Server URI to access (without base URL).
            **kwargs: Arguments to requests.Session.post method.
        Raises:
            InteropError: Error from server.
            requests.Timeout: Request timeout.
        """
        r = self.session.post(self.url+uri, timeout=self.timeout, **kwargs)
        if not r.ok:
            print "Problem with POST."
        return r

    def get_telemetry(self):
        #packet = self.executor.submit(self.communicator.receive())
        try:
            packet = self.communicator.receive()
            parsed = packet.split('$')[1].split(',')
            result = Telemetry(pos_x=float(parsed[0]),pos_y=float(parsed[1]),heading=float(parsed[2]),timestamp=float(parsed[3]))
            return result
        except Exception as exc:
            print('Timeout: %s' % exc)
            return Telemetry()

    def post_telemetry(self, telem):
        self.post('/console/telemetry', data=telem.serialize())

    def post_telem_to_server(self,telem):
        return self.executor.submit(self.post_telemetry, telem)

    def send_control_signal(self):
        control_signal = ("$%f,%f" % (self.pwms[0],self.pwms[1]))
        self.communicator.send(control_signal)

    def set_control_mode(self,mode):
        self.control_mode = mode

    def set_waypoint(self,index):
        self.wp_controller.wp_index = index

    def add_waypoint(self,wp,index=False):
        if index:
            self.wp_controller.wp_list.insert(index,wp)
        else:
            self.wp_controller.wp_list.append(wp)

    def get_err_hdg(self):
        error = self.desired_state.heading - self.vehicle_state.heading
        if error > 180:
            error = error - 360
        elif error < -180:
            error = error + 360
        return error

    def nav_loop(self):
        start = time.time()
        self.telemetry = self.get_telemetry()
        self.vehicle_state.update(self.telemetry,self.telemetry_last)
        [self.desired_state.heading,self.desired_state.speed] = self.wp_nav.navigate([self.vehicle_state.pos_x,self.vehicle_state.pos_y])
        #[self.desired_state.heading,self.desired_state.speed] = [0,1]
        err_spd = self.desired_state.speed -self.vehicle_state.speed
        err_hdg = self.get_err_hdg()
        f1 = self.hdg_control.control(err_hdg,self.vehicle_state.ang_vel) #forces for heading correction
        f2 = self.spd_control.control(err_spd,self.vehicle_state.speed) #forces for speed correction
        self.pwms = [force2pwm(f2+f1,'left'),force2pwm(f2-f1,'right')]
        self.telemetry_last = self.telemetry
        if self.wp_last != self.wp_nav.wp_index:
            print "Headed to WP %d" % self.wp_nav.wp_index
            print '\n\n\n\n\n'
        self.wp_last = self.wp_nav.wp_index
        self.send_control_signal()
        dt = time.time() - start
        print  "Current wp:" , self.wp_nav.wp_index , "Position:" , [self.vehicle_state.pos_x,self.vehicle_state.pos_y], "Heading Ordered:" , round(self.desired_state.heading,1)
        if self.telem_count == 200:
            response = self.post_telem_to_server(self.telemetry)
            print response.result()
            self.telem_count = 0
        else:
            self.telem_count += 1
        if dt < 0.01:
            time.sleep(dt)
