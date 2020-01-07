import gxs700.util
from uvscada import util

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dump device data')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    util.add_bool_arg(parser, '--quick', default=True, help='')
    util.add_bool_arg(parser, '--eeprom', default=False, help='')
    util.add_bool_arg(parser, '--flash', default=False, help='')
    parser.add_argument('din', nargs='?', default='dump', help='File in')
    args = parser.parse_args()

    usbcontext, dev, gxs = gxs700.usbint.ez_open_ex()

    print 'Ready'

    if args.eeprom:
        print
        print 'Writing EEPROM'
        eeprom_w = open(os.path.join(args.din, 'eeprom.bin'), 'r').read()
        if args.quick:
            eeprom_w = eeprom_w[0:0x400]
        gxs.eeprom_w(0x0000, eeprom_w)

        print 'Reading back to verify'
        eeprom_r = gxs.eeprom_r()
        if eeprom_w != eeprom_r:
            raise Exception("Failed to update EEPROM")
        print 'Update OK!'

    if args.flash:
        print
        print 'Erasing flash'
        gxs.flash_erase_all()
        print 'Writing flash'
        flash_w = open(os.path.join(args.din, 'flash.bin'), 'r').read()
        gxs.flash_w(0x0000, flash_w)

        print 'Reading back to verify'
        flash_r = gxs.flash_r()
        if flash_w != flash_r:
            raise Exception("Failed to update flash")
        print 'Update OK!'
