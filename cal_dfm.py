#!/usr/bin/env python
from __future__ import print_function
'''
File:               287304 bytes

1346 * 1700 / 8 =   286025
1850 * 1344 / 8 =   310800
Buff:               287300

287300 => 2298400 pixels
Possible configurations
1300 * 1768
1352 * 1700
    seems plausible
1690 * 1360
 '''

from PIL import Image
import binascii

MAGIC = '\xa9\x00\xa4\x06'

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument(
        '--hist-eq', '-e', action='store_true', help='Equalize histogram')
    parser.add_argument('fin', help='File name in')
    parser.add_argument('fout', default=None, nargs='?', help='File name out')
    args = parser.parse_args()

    buff = open(args.fin).read()
    magic = buff[0:4]
    # 2/2 sensors, both flat and dark have this value
    if magic != MAGIC:
        raise ValueError('Bad magic: expect %s but got %s' %
                         (binascii.hexlify(MAGIC), binascii.hexlify(magic)))

    raw = buff[4:]
    # http://effbot.org/imagingbook/decoder.htm
    im = Image.frombytes("1", (1352, 1700), raw)

    if args.fout:
        im2 = im.convert('1').save(args.fout)
    else:
        im.show()
