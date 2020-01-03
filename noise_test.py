#!/usr/bin/env python
'''
Capture with increasing delay
See how sensor values drift
Sweep two parameters
-Integration time
-Time before triggering
'''

import gxs700.util
import time
import struct

import argparse


def bufavg(buff):
    '''
    Given 16 bit LE packed data, return average value
    '''
    val = 0.0
    for i in xrange(0, len(buff), 2):
        raw = buff[i:i + 2]
        val += struct.unpack('<H', raw)[0]
    #print 'net', val
    return val / len(buff) / 2


class NoiseTest(object):
    def __init__(self):
        self.tstart = None
        self.tmin = 20.0
        self.gxs = None
        self.triggered = None

        _usbcontext, _dev, self.gxs = gxs700.util.ez_open_ex(
            verbose=args.verbose)
        self.gxs.do_printm = False

        self.int_t = None
        self.wait_t = None

    def run(self):
        self.int_t = 125
        self.wait_t = 0.125

        def scan_cb(itr):
            if not self.triggered and time.time() - self.tstart >= self.wait_t:
                #print 'Forcing trigger'
                self.gxs.sw_trig()
                self.triggered = True

        while True:
            self.tstart = time.time()
            self.triggered = False
            self.gxs.int_t_w(self.int_t)
            buff = self.gxs.cap_bin(scan_cb=scan_cb)
            last = bufavg(buff)
            print 'twait % 10.3f, tint % 10.3f, %10.3f' % (self.wait_t,
                                                           self.int_t, last)
            self.wait_t *= 2
            self.int_t *= 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        'Report average pixel noise for various integration/wait times')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('fout', nargs='?')
    args = parser.parse_args()

    r = NoiseTest()
    r.run()
