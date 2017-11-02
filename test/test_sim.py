import threading
import time
import pygame

from udp_test import UDPcomms
from math import sin,cos
from concurrent.futures import ThreadPoolExecutor
from bin import GenericStateController, force2pwm, get_speed_dep, SpeedController
from pygame.locals import *
from bin import InputKeys

communicator = UDPcomms(remoteport=8001,localport=8000)
controlsignal = "$1.000,1.000"
variable = 1
executor = ThreadPoolExecutor(max_workers=8)
heading_controller = GenericStateController()
speed_controller = SpeedController()
desired_heading = 0
desired_speed = 1
error_last = 0
timestamp_last = time.time()
heading_last = 1
asv_heading_last = 0
asv_pos_last = [0,0]

while True:
    start = time.time()
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
    speed = get_speed_dep(asv_pos,asv_pos_last,(timestamp_last+0.0001))
    speed_error = desired_speed - speed
    ang_vel_est = (asv_heading - heading_last) / (timestamp - timestamp_last +  0.0001)
    force = heading_controller.control(error,ang_vel_est)
    force2 = speed_controller.control(speed_error,speed)
    pwms = [force2pwm(force2+force,'left'),force2pwm(force2-force,'right')]
    heading_last = asv_heading
    speed_last = speed
    timestamp_last = timestamp
    asv_pos_last = asv_pos
    controlsignal = ("$%f,%f" % (pwms[0],pwms[1]))
    print  "Control Signal:" , controlsignal , "Error:" , error, "Heading:" , asv_heading
    communicator.send(controlsignal)
    dt = time.time() - start
    if dt < 0.01:
        time.sleep(dt)
