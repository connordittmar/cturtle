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

def get_speed(pos,pos_last,dt):
    speed = sqrt(((pos[0]-pos_last[0])**2+(pos[1]-pos_last[1])**2))/dt
    return speed
