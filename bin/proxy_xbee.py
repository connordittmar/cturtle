#Module to receive NMEAish packets and forward
#over to other systems

import logging
import sys
import time
import types
import serial

class NMEAParser(object):
    def __init__(self,deviceid,asvid):
        self.logger = logging.getLogger(__name__)
        self.PRINT_PERIOD = 5.0
        self.asv = serial.Serial(deviceid,115200,timeout=10,parity=serial.PARITY_NONE)
        self.sent_since_print = 0
        self.last_print = time.time()
        self.asvid = asvid

        def asv_heading(self,heading):
            """Converts from radians to decimal degrees"""
            return (heading / 0.0174532925)

        def get_telemetry(self):
            """Receives NMEA strings over serial connection to xbee

            Args:

            Returns:
            Telemetry object of either ownship or another vehicle.

            Exception:
            timeoutexception
            """
            msg = self.asv.readline()
            msg = msg.split('!')[0].split(',')
            if msg[0] == '$'+ self.asvid:
                telemetry = types.Telemetry(timestamp=msg[1],latitude=msg[2],longitude=msg[4],heading=self.asv_heading(msg[5])
            if msg is None:
                logger.critical(
                    "Did not receive telemetry packet for over 10 seconds.")
                sys.exit(-1)

            #Track telemetry rates
            self.sent_since_print += 1
            self.now = time.time()
            self.since_print = self.now - self.last_print
            if self.since_print > self.PRINT_PERIOD:
                self.logger.info('Telemetry rate: %f Hz', self.sent_since_print / self.since_print)
                self.sent_since_print = 0
                self.last_print = self.now
            return telemetry
