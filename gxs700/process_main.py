#!/usr/bin/env python3
from gxs700 import util
from gxs700 import im_util
from gxs700.util import add_bool_arg

import binascii
import glob
from PIL import Image, ImageOps
import numpy as np
import os
import sys
import time
import usb1
from scipy.ndimage import median_filter
import statistics
import subprocess

try:
    from skimage import exposure
except ImportError:
    exposure = None


def make_bpm(im):
    width, height = im.size
    ret = set()
    for y in range(height):
        for x in range(width):
            if im.getpixel((x, y)):
                ret.add((x, y))
    return ret


def im_med3(im, x, y, badimg):
    width, height = badimg.size
    pixs = []
    for dx in range(-1, 2, 1):
        xp = x + dx
        if xp < 0 or xp >= width:
            continue
        for dy in range(-1, 2, 1):
            yp = y + dy
            if yp < 0 or yp >= height:
                continue
            if not badimg.getpixel((xp, yp)):
                pixs.append(im.getpixel((xp, yp)))
    if len(pixs) == 0:
        return 0
    return int(statistics.median(pixs))


def do_bpr(im, badimg):
    ret = im.copy()
    bad_pixels = make_bpm(badimg)
    for x, y in bad_pixels:
        ret.putpixel((x, y), im_med3(im, x, y, badimg))
    return ret

def run_hist_eq(im_wip, hist_eq_roi=None):
    # https://stackoverflow.com/questions/43569566/adaptive-histogram-equalization-in-python
    # simple implementation
    # CV2 might also work

    mode = os.getenv("GXS700_EQ_MODE", "0")
    print("Eq mode (GXS700_EQ_MODE) %s" % mode)
    if mode == "0":
        if hist_eq_roi:
            x1, y1, x2, y2 = hist_eq_roi
            ref_im = im_wip.crop((x1, y1, x2, y2))
        else:
            ref_im = im_wip

        ref_np2 = np.array(ref_im)
        wip_np2 = np.array(im_wip)
        wip_np2 = im_util.histeq_np_apply(
            wip_np2, im_util.histeq_np_create(ref_np2))
        im_wip = im_util.npf2im(wip_np2)
    elif mode == "convert":
        with util.AutoTempFN(suffix='.png') as tmpa:
            with util.AutoTempFN(suffix='.png') as tmpb:
                im_wip.save(tmpa)
                subprocess.check_call(
                    "convert %s \( +clone -equalize \) -average %s" %
                    (tmpa, tmpb),
                    shell=True)
                im_wip = Image.open(tmpb)
    elif mode == "1":
        # OSError: not supported for this image mode
        im_wip = ImageOps.equalize(im_wip, mask=None)
    elif mode == "2":
        imnp = np.array(im_wip, dtype=np.uint16)
        im_wip = im_util.npf2im(exposure.equalize_hist(imnp))
    elif mode == "3":
        # raise ValueError("Images of type float must be between -1 and 1.")
        imnp = np.array(im_wip, dtype=np.uint16)
        #imnp = np.ndarray.astype(imnp, dtype=np.float)
        print(np.ndarray.min(imnp), np.ndarray.max(imnp))
        imnp = 1.0 * imnp / 0xFFFF
        im_wip = im_util.npf2im(
            exposure.equalize_adapthist(imnp, clip_limit=0.03))
    else:
        raise Exception(mode)
    return im_wip

def process_raw(im_wip, dir_in=None, rescale=True, bpr=True, invert=True, cal_dir=None):
    if not cal_dir:
        cal_dir = im_util.default_cal_dir(im_dir=dir_in)
        if not os.path.exists(cal_dir):
            print("WARNING: default calibration dir %s does not exist" %
                  cal_dir)
            cal_dir = None

    if cal_dir:
        assert os.path.exists(cal_dir), cal_dir
        print("Found calibration files at %s" % cal_dir)

    if rescale and cal_dir:
        ffimg = Image.open(os.path.join(cal_dir, 'ff.png'))
        np_ff2 = np.array(ffimg)
        dfimg = Image.open(os.path.join(cal_dir, 'df.png'))
        np_df2 = np.array(dfimg)

        # ff *should* be brighter than df
        # (due to .png pixel value inversion convention)
        mins = np.minimum(np_df2, np_ff2)
        maxs = np.maximum(np_df2, np_ff2)

        u16_mins = np.full(mins.shape, 0x0000, dtype=np.dtype('float'))
        u16_ones = np.full(mins.shape, 0x0001, dtype=np.dtype('float'))
        u16_maxs = np.full(mins.shape, 0xFFFF, dtype=np.dtype('float'))

        cal_det = maxs - mins
        # Prevent div 0 on bad pixels
        cal_det = np.maximum(cal_det, u16_ones)
        cal_scalar = 0xFFFF / cal_det

        np_in2 = np.array(im_wip)
        np_scaled = (np_in2 - mins) * cal_scalar
        # If it clipped, squish to good values
        np_scaled = np.minimum(np_scaled, u16_maxs)
        np_scaled = np.maximum(np_scaled, u16_mins)
        im_wip = Image.fromarray(np_scaled).convert("I")
        print("Rescale min: %u, max: %u" % (np.ndarray.min(
            np.array(im_wip)), np.ndarray.max(np.array(im_wip))))

    # Seems this needs to be done after scaling or artifacts get amplified
    if bpr and cal_dir:
        badimg = Image.open(os.path.join(cal_dir, 'bad.png'))
        im_wip = do_bpr(im_wip, badimg)
        print("BPR min: %u, max: %u" % (np.ndarray.min(np.array(im_wip)),
                                        np.ndarray.max(np.array(im_wip))))

    if invert:
        # IOError("not supported for this image mode")
        # im_wip = ImageOps.invert(im_wip)
        im_wip = im_util.im_inv16_slow(im_wip)
        print("Invert min: %u, max: %u" % (np.ndarray.min(
            np.array(im_wip)), np.ndarray.max(np.array(im_wip))))

    return im_wip

def run(dir_in,
        fn_out,
        cal_dir=None,
        hist_eq=True,
        invert=True,
        hist_eq_roi=None,
        scalar=None,
        rescale=True,
        bpr=True,
        raw=False):
    if not fn_out:
        dir_in = dir_in
        if dir_in[-1] == '/':
            dir_in = dir_in[:-1]
        fn_out = dir_in + '.png'
        fn_oute = dir_in + '_e.png'
    else:
        fn_out = fn_out
        fn_oute = fn_out

    _imgn, img_in = im_util.average_dir(dir_in, scalar=scalar)

    desc = dir_in
    print('Processing %s' % desc)

    im_wip = img_in
    print("Avg min: %u, max: %u" % (np.ndarray.min(np.array(im_wip)),
                                    np.ndarray.max(np.array(im_wip))))
    if not raw:
        im_wip = process_raw(im_wip, dir_in, rescale=rescale, bpr=bpr, invert=invert, cal_dir=cal_dir)
    print("Save %s" % fn_out)
    im_wip.save(fn_out)

    if hist_eq:
        im_wip = run_hist_eq(im_wip=im_wip, hist_eq_roi=hist_eq_roi)
        print("Save %s" % fn_oute)
        im_wip.save(fn_oute)
        print("Eq min: %u, max: %u" % (np.ndarray.min(np.array(im_wip)),
                                       np.ndarray.max(np.array(im_wip))))


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Apply image correction')
    #parser.add_argument('--images', type=int, default=0, help='Only take first n images, for debugging')
    parser.add_argument('--cal-dir', default='', help='')
    parser.add_argument(
        '--hist-eq-roi', default=None, help='hist eq x1,y1,x2,y2')
    add_bool_arg(parser, "--hist-eq", default=True)
    add_bool_arg(parser, "--invert", default=True)
    add_bool_arg(parser, "--rescale", default=True)
    add_bool_arg(parser, "--bpr", default=True)
    add_bool_arg(parser, "--raw", default=False)
    parser.add_argument('--scalar', default=None, type=float, help='')
    parser.add_argument('dir_in', help='')
    parser.add_argument('fn_out', default=None, nargs='?', help='')
    args = parser.parse_args()

    run(args.dir_in,
        args.fn_out,
        cal_dir=args.cal_dir,
        hist_eq=args.hist_eq,
        invert=args.invert,
        hist_eq_roi=im_util.parse_roi(args.hist_eq_roi),
        scalar=args.scalar,
        rescale=args.rescale,
        bpr=args.bpr,
        raw=args.raw)

    print("done")
