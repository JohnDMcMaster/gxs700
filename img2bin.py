#!/usr/bin/env python
import argparse
from PIL import Image

from gxs700 import usbint

def run(fin, fout):
    im = Image.open(fin)
    b = usbint.im2bin(im)
    open(fout, 'w').write(b)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Equalize 16 bit GXS700 image histogram')
    parser.add_argument('fin', help='File name in')
    parser.add_argument('fout', default=None, nargs='?', help='File name out')
    args = parser.parse_args()

    run(args.fin, args.fout)
