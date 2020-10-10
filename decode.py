#!/usr/bin/env python3

from gxs700 import usbint

import argparse
import os
import glob


def process_bin(fin, fout):
    print 'Reading %s...' % fin
    buff = open(fin, 'r').read()
    print 'Decoding image...'
    img = usbint.GXS700.decode(buff)
    print 'Saving %s...' % fout
    img.save(fout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decode a .bin to a .png')
    parser.add_argument('fin', help='.bin file name in')
    parser.add_argument(
        'fout', default=None, nargs='?', help='.png file name out')
    args = parser.parse_args()

    if os.path.isdir(args.fin):
        if args.fout is None:
            raise Exception("dir requires fout")
        if not os.path.exists(args.fout):
            os.mkdir(args.fout)
        for fn in glob.glob(os.path.join(args.fin, '*.bin')):
            fout = os.path.join(args.fout,
                                os.path.basename(fn).replace('.bin', '.png'))
            process_bin(fn, fout)
    else:
        fout = args.fout
        if fout is None:
            fout = args.fin.replace('.bin', '.png')
            if args.fin == fout:
                raise Exception("Couldn't auto name output file")
        process_bin(args.fin, fout)
    print 'Done'
