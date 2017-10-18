from udp_test import UDPcomms
from math import sin,cos
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from bin import GenericController

communicator = UDPcomms(remoteport=8001,localport=8000)
controlsignal = "$1.000,1.000"
variable = 1
executor = ThreadPoolExecutor(max_workers=8)
heading_controller = GenericController()
desired_heading = 000
old_error = 0
old_pwms = [0.0,0.0]
old_timestamp = time.time()
old_heading = 1
while True:
    packet = executor.submit(communicator.receive)
    try:
        telemetry = packet.result()
        parsed = telemetry.split('$')[1].split(',')
        asv_pos = [float(parsed[0]),float(parsed[1])]
        asv_heading = float(parsed[2])
        timestamp = float(parsed[3])
    except Exception as exc:
        print('Exception: %s' % exc)
    error = desired_heading - asv_heading
    if error > 180:
        error = error - 360
    elif error < -180:
        error = error + 360
    est_speed = (asv_heading - old_heading) / (1/120.0)
    print est_speed
    pwms = heading_controller.control(error,old_error,old_pwms[0],est_speed)
    old_error = error
    old_pwms = pwms
    old_timestamp = timestamp
    old_heading = asv_heading
    controlsignal = ("$%f,%f" % (pwms[0],pwms[1]))
    print  "Control Signal:" , controlsignal , "Error:" , error, "Heading:" , asv_heading
    communicator.send(controlsignal)
