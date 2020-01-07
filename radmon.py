#!/usr/bin/env python
'''
x-ray camera based radiation montior
I'm flying from Taipei to Tokyo and happen to have a sensor on me
lets see if I can make a graph of radiation vs time
try to take some notes on 

Capture takes about 2.4 seconds
Lets do ~30 second accumulations to keep capture overhead reasonably low
and noise relatively low

during x-ray inspection?
at least near the machine
might do something funny
run at max rate
'''

from gxs700 import usbint
import gxs700.util
import time
import struct

import argparse
import os
import json


def bufavg(buff):
    '''
    Given 16 bit LE packed data, return average value
    '''
    val = 0.0
    for i in xrange(0, len(buff), 2):
        raw = buff[i:i + 2]
        val += struct.unpack('<H', raw)[0]
    print 'net', val
    return val / len(buff) / 2


class RadMon(object):
    def __init__(self, fout):
        self.tstart = None
        self.tmin = 20.0
        self.gxs = None
        self.triggered = None
        self.fout = fout

        _usbcontext, _dev, self.gxs = gxs700.usbint.ez_open_ex(
            verbose=args.verbose)
        self.gxs.do_printm = False

    def run(self):
        f = open(self.fout, 'w')

        j = {'type': 'init', 't': time.time(), 'tmin': self.tmin}
        json.dump(j, f)
        f.write('\n')
        f.flush()

        def scan_cb(itr):
            #if not self.triggered and time.time() - self.tstart >= self.tmin:
            if not self.triggered:
                print 'Forcing trigger'
                self.gxs.sw_trig()
                self.triggered = True

        while True:
            self.tstart = time.time()
            self.triggered = False
            self.gxs.int_t_w(20000)
            buff = self.gxs.cap_bin(scan_cb=scan_cb)
            #print len(buff)
            last = bufavg(buff)
            print 'Avg: %10.3f' % last

            j = {'type': 'meas', 't': self.tstart, 'avg': last}
            json.dump(j, f)
            f.write('\n')
            f.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('fout', nargs='?')
    args = parser.parse_args()

    if args.fout:
        fout = args.fout
    else:
        if not os.path.exists('radmon'):
            os.mkdir('radmon')
        i = 0
        while True:
            fout = 'radmon/radmon_%03d.jl' % i
            if not os.path.exists(fout):
                break
            i += 1
    print 'Writing to %s' % fout

    r = RadMon(fout)
    r.run()
