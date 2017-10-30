import threading
import time
import pygame

from udp_test import UDPcomms
from math import sin,cos
from concurrent.futures import ThreadPoolExecutor
from bin import GenericController
from pygame.locals import *
from bin import InputKeys

communicator = UDPcomms(remoteport=8001,localport=8000)
controlsignal = "$1.000,1.000"
variable = 1
executor = ThreadPoolExecutor(max_workers=8)
heading_controller = GenericController()
desired_heading = 270
old_error = 0
old_pwms = [0.0,0.0]
old_timestamp = time.time()
old_heading = 1

pygame.init()
user_done = False
keys = InputKeys()
manual_control = False
while True:

    # Get User Input
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            user_done = True
        elif (event.type == pygame.KEYDOWN):
            if (event.key == K_ESCAPE):
                user_done = True
            elif (event.key==K_w):
                keys.w = 'D'
            elif (event.key==K_a):
                keys.a = 'D'
            elif (event.key==K_s):
                keys.s = 'D'
            elif (event.key==K_d):
                keys.d = 'D'

        elif (event.type == pygame.KEYUP):
            if (event.key==K_w):
                keys.w = 'U'
            elif (event.key==K_a):
                keys.a = 'U'
            elif (event.key==K_s):
                keys.s = 'U'
            elif (event.key==K_d):
                keys.d = 'U'
    # If keys are down, input control commands
    if keys.w == 'D':
        pwms = [1.0,1.0]
        manual_control = True
    elif keys.s == 'D':
        pwms = [-1.0,-1.0]
        manual_control = True
    elif keys.a == 'D':
        pwms = [-1.0,1.0]
        manual_control = True
    elif keys.d == 'D':
        pwms = [1.0,-1.0]
        manual_control = True
    else:
        manual_control == False

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
    #if error > 180:
    #    error = error - 360
    #elif error < -180:
    #    error = error + 360
    #if manual_control == False:
    pwms = heading_controller.control(error,old_error,old_pwms[0])
    old_error = error
    old_pwms = pwms
    old_timestamp = timestamp
    controlsignal = ("$%f,%f" % (pwms[0],pwms[1]))
    print  "Control Signal:" , controlsignal , "Error:" , error, "Heading:" , asv_heading
    communicator.send(controlsignal)
