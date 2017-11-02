from math import sqrt

def force2pwm(force,motor):
    if force > 2:
        force = 2
    if force < -2:
        force = -2
    pwm = 0.8*abs(force)+0.35
    if force < 0:
        pwm = -pwm

    if pwm > 1:
        pwm = 1
    elif pwm < -1:
        pwm = -1
    return pwm

def get_speed(telemetry,telemetry_last):
    pos,pos_last = [telemetry.pos_x,telemetry.pos_y],[telemetry_last.pos_x,telemetry_last.pos_y]
    dt = (telemetry.timestamp - telemetry_last.timestamp) + 0.00001
    speed = sqrt(((pos[0]-pos_last[0])**2+(pos[1]-pos_last[1])**2))/dt
    return speed

def get_speed_dep(telemetry,telemetry_last):
    pos,pos_last = [telemetry.pos_x,telemetry.pos_y],[telemetry_last.pos_x,telemetry_last.pos_y]
    dt = telemetry.timestamp - telemetry_last.timestamp + 0.00001
    speed = sqrt(((pos[0]-pos_last[0])**2+(pos[1]-pos_last[1])**2))/dt
    return speed

def get_ang_vel(telemetry,telemetry_last):
    ang_vel = (telemetry.heading - telemetry_last.heading) / (telemetry.timestamp-telemetry_last.timestamp + 0.00001)
    return ang_vel
