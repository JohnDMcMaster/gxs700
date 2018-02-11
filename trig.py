from uvscada import gxs700_util
from uvscada import util

import argparse
import binascii
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dump device data')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('dout', nargs='?', default='dump', help='File out')
    args = parser.parse_args()

    usbcontext, dev, gxs = gxs700_util.ez_open_ex()
    
    print
    print 'Versions'
    gxs.versions()
    
    print
    print 'FPGA signature: 0x%04X' % gxs.fpga_rsig()
    print 'State: %d' % gxs.state()
    print 'Error: %d' % gxs.error()
    print 'Int time: %s' % gxs.int_time()
    print 'Img ctr: %s' % binascii.hexlify(gxs.img_ctr_r())
        
    w, h = gxs.img_wh()
    print 'Sensor dimensions: %dw x %dh' % (w, h)

    print
    print
    print
    print 'Trigger params: %s' % binascii.hexlify(gxs.trig_param_r())
    print 'exp_cal_last: %s' % gxs.exp_cal_last()
    print 'exp_since_manu: %s' % gxs.exp_since_manu()
    print 'exp_ts: %s' % gxs.exp_ts()
    print 'img_ctr_r: %s' % gxs.img_ctr_r()
