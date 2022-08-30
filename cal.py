#!/usr/bin/env python3
"""
Looking over:
https://stackoverflow.com/questions/18951500/automatically-remove-hot-dead-pixels-from-an-image-in-python
Suggests take the median of the surrounding pixels

Lets just create an image map with the known bad pixels
Arbitrarily going to set to black to good pixel, white for bad pixel
"""

from gxs700.util import hexdump, add_bool_arg, default_date_dir, mkdir_p
from gxs700 import xray
from gxs700 import util
from gxs700 import im_util

import binascii
import glob
from PIL import Image
import numpy as np
import os
import sys
import time
import usb1
"""
def bad_pixs_ff1(fff, ffi):
    ffmed = np.median(fff)
    print("min: %0.1f, med: %0.1f, max: %0.1f" % (np.amin(fff), ffmed, np.amax(fff)))
    #cold_pixs = fff[fff <= ffmed/2.0]
    cold_pixs = np.nonzero(fff <= ffmed/2.0)
    print(cold_pixs)
    print("Cold pixels: %u / %u" % (len(cold_pixs), width * height))
    #x = i % width
    #y = i // width
"""


def bad_pixs_ff(fff, ffi, thresh_scalar=0.25):
    ffmed = np.median(fff)
    print("min: %0.1f, med: %0.1f, max: %0.1f" % (np.amin(fff), ffmed,
                                                  np.amax(fff)))

    ret = []
    width, height = ffi.size
    thresh = ffmed * thresh_scalar
    for y in range(height):
        for x in range(width):
            val = ffi.getpixel((x, y))
            if 0 and y == 0 and x < 16:
                print(x, y, val)
            if val <= thresh:
                ret.append((x, y))

    print("Cold pixels: %u / %u" % (len(ret), width * height))
    return ret


def bad_pixs_df(fff, ffi, thresh_scalar=0.25):
    ffmed = np.median(fff)
    print("min: %0.1f, med: %0.1f, max: %0.1f" % (np.amin(fff), ffmed,
                                                  np.amax(fff)))

    ret = []
    width, height = ffi.size
    # FIXME
    PIX_MAX = 0xFFFF
    thresh = PIX_MAX * thresh_scalar
    for y in range(height):
        for x in range(width):
            val = ffi.getpixel((x, y))
            if 0 and y == 0 and x < 16:
                print(x, y, val)
            if val >= thresh:
                ret.append((x, y))

    print("Hot pixels: %u / %u" % (len(ret), width * height))
    return ret


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate calibreation files from specially captured frames')
    parser.add_argument(
        '--images',
        type=int,
        default=0,
        help='Only take first n images, for debugging')
    parser.add_argument('--ff-thresh', default=0.25, type=float, help='')
    parser.add_argument('--df-thresh', default=0.25, type=float, help='')
    parser.add_argument('ff_dir', help='Flat field images')
    parser.add_argument('df_dir', help='Dark field images')
    parser.add_argument('cal_dir', nargs='?', default=None, help='Output calibration files dir')
    args = parser.parse_args()

    cal_dir = args.cal_dir
    if not cal_dir:
        cal_dir_ff = im_util.default_cal_dir(im_dir=args.ff_dir)
        cal_dir_df = im_util.default_cal_dir(im_dir=args.df_dir)
        assert cal_dir_ff == cal_dir_df, "Files are from different sensors"
        cal_dir = cal_dir_ff
    mkdir_p(cal_dir)

    fff, ffi = im_util.average_dir(args.ff_dir, images=args.images)
    width, height = ffi.size
    badimg = Image.new("1", (width, height), "Black")
    ffi.save(cal_dir + '/ff.png')
    im_util.histeq_im(ffi).save(cal_dir + '/ffe.png')
    for x, y in bad_pixs_ff(fff, ffi, thresh_scalar=args.ff_thresh):
        badimg.putpixel((x, y), 1)

    dff, dfi = im_util.average_dir(args.df_dir, images=args.images)
    dfi.save(cal_dir + '/df.png')
    im_util.histeq_im(dfi).save(cal_dir + '/dfe.png')
    for x, y in bad_pixs_df(dff, dfi, thresh_scalar=args.df_thresh):
        badimg.putpixel((x, y), 1)

    badimg.save(cal_dir + '/bad.png')

    print("done")


if __name__ == "__main__":
    #im = Image.fromarray(np.asarray([[1, 2, 3], [4, 5, 6]]), mode="I")
    #im.show()
    main()
