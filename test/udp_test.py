# Test udp connection with MATLAB Simulator
import socket
import time

def send():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 8001
    MESSAGE = "Helloworld"

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    i = 1
    while(1):
        print("sender up! %f" % i)
        sock.sendto(("good morning " + str(i)), (UDP_IP, UDP_PORT))
        i = i + 1
        time.sleep(0.1)
    print "sender up!"

def receive():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 8000
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print "socket up..."
    now = time.time()
    while (time.time() - now) < 5.0:
        print "in loop...."
        data, addr = sock.recvfrom(1024)
        print "received message:", data

class UDPcomms(object):
    def __init__(self,ip='127.0.0.1',remoteport=8001,localport=8000):
        self.ip = ip
        self.remoteport = remoteport
        self.localport = localport
        self.sock_local = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.sock_remote = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
        self.sock_remote.bind((self.ip,self.remoteport))
        self.sock_remote.settimeout(5.0)

    def receive(self):
        now = time.time()
        while True:
            try:
                data, addr = self.sock_remote.recvfrom(1024)
                return data
            except:
                print "no message received."
    def send(self,message):
        self.sock_local.sendto(message, (self.ip, self.localport))
        print "message send to ", self.localport
