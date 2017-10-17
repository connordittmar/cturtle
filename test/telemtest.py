from udp_test import UDPcomms
port = [8000,9000,10000,11000,12000,13000]
communicator = []
for i in range(0,6):
    communicator.append(UDPcomms(remoteport=port[i],localport=(port[i]+100)))
while True:
    for i in range(0,6):
        print "Message from communicator #", i+1
        print communicator[i].receive()
