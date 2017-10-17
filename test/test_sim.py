from udp_test import UDPcomms
communicator = UDPcomms(remoteport=8001,localport=8000)
controlsignal = "$1.000,1.000"
while True:
    communicator.send(controlsignal)
