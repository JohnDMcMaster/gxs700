#!/usr/bin/env python
from __future__ import print_function
from gxs700 import util

import argparse
import binascii
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dump device data')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    util.add_bool_arg(
        parser, '--eeprom', default=False, help='Dump only EEPROM')
    util.add_bool_arg(parser, '--flash', default=False, help='Dump only flash')
    util.add_bool_arg(
        parser,
        '--hexdump',
        default=False,
        help='Instead of writing out, just hexdump')
    parser.add_argument('dout', nargs='?', default=None, help='File out')
    args = parser.parse_args()

    usbcontext, dev, gxs = usbint.ez_open_ex(verbose=args.verbose)

    sn_flash = util.sn_flash_r(gxs)
    try:
        sn_eeprom = util.sn_eeprom_r(gxs)
    except:
        sn_eeprom = None
    print 'S/N (flash): %s' % sn_flash
    print 'S/N (EEPROM): %s' % sn_eeprom
    if sn_flash != sn_eeprom:
        print 'WARNING: S/N mismatch'
    sn = sn_flash

    if 0 < sn < 1000000000:
        print '  S/N guess: black Dexis (size 2)'
    elif 1000000000 <= sn < 2000000000:
        print '  S/N guess: blue Gendex (size 1)'
    elif 2000000000 <= sn < 3000000000:
        print '  S/N guess: blue Gendex (size 2)'
    else:
        print '  S/N guess: unknown'

    if not args.hexdump:
        #today_str = datetime.datetime.now().isoformat()[0:10]
        if args.dout:
            dout = args.dout
        else:
            if not os.path.exists('dump'):
                os.mkdir('dump')
            i = 0
            while True:
                dout = 'dump/' + str(sn_flash)
                if i:
                    dout += '.' + str(i)
                if not os.path.exists(dout):
                    break
                i += 1
        print 'Writing to %s' % dout
        if not os.path.exists(dout):
            os.mkdir(dout)
        _t = util.IOLog(out_fn=os.path.join(dout, 'out.txt'))

    alll = not (args.eeprom or args.flash)
    '''
    FIXME: couldn't get I2C to work
    probably doesn't matter since expect only EEPROM on bus

    List of  controlRead(0xC0, 0xB0,...)
    req     uses
    0x03    fpga_r
    0x04    fpga_sig
    0x0A    i2c_r
    0x0B    eeprom_r
    0x10    flash_r
    0x20    state
    0x23    img_wh
    0x25    trig_param_r
    0x2D    int_time
    0x40    img_ctr_r
    0x51    versions
    0x80    error
    '''

    if alll:
        print
        print 'Versions'
        gxs.versions()
        open(os.path.join(dout, 'ver.bin'), 'w').write(
            gxs.versions(decode=False))

        print
        print 'FPGA signature: 0x%04X' % gxs.fpga_rsig()
        print 'State: %d' % gxs.state()
        print 'Error: %d' % gxs.error()
        print 'Trigger params: %s' % binascii.hexlify(gxs.trig_param_r())
        print 'Int time: %s' % gxs.int_time()
        print 'Img ctr: %s' % binascii.hexlify(gxs.img_ctr_r())

        w, h = gxs.img_wh()
        print 'Sensor dimensions: %dw x %dh' % (w, h)

        print
        print 'Dumping RAM'
        '''
        The FX2 has eight kbytes of internal program/data RAM,
        Only the internal eight kbytes and scratch pad 0.5 kbytes RAM spaces have the following access:

        The available RAM spaces are 8 kbytes from
        0x0000-0x1FFF (code/data) and 512 bytes from 0xE000-0xE1FF (scratch pad RAM).
        '''
        ram = util.ram_r(dev, 0x0000, 0x10000)
        open(os.path.join(dout, 'ram.bin'), 'w').write(ram)

    if alll or args.eeprom:
        print 'Dumping EEPROM'
        eeprom = gxs.eeprom_r()
        if args.hexdump:
            util.hexdump(eeprom)
        else:
            open(os.path.join(dout, 'eeprom.bin'), 'w').write(eeprom)

    if alll or args.flash:
        print 'Dumping flash'
        flash = gxs.flash_r()
        if args.hexdump:
            util.hexdump(flash)
        else:
            open(os.path.join(dout, 'flash.bin'), 'w').write(flash)

    if alll:
        print 'Dumping register space'
        f = open(os.path.join(dout, 'regs.csv'), 'w')
        f.write('reg,val\n')
        # slightly faster
        if 1:
            for kbase in xrange(0x0000, 0x10000, 0x80):
                vs = gxs.fpga_rv(kbase, 0x80)
                for i, v in enumerate(vs):
                    k = kbase + i
                    f.write('0x%04X,0x%04X\n' % (k, v))
        if 0:
            for k in xrange(0x0000, 0x10000, 0x1):
                v = gxs.fpga_r(k)
                f.write('0x%04X,0x%04X\n' % (k, v))
