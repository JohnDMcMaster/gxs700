#!/usr/bin/env python
from __future__ import print_function

from gxs700 import usbint
from gxs700 import util
from gxs700 import img

import argparse
import glob
import os
import binascii
import json


def run(
        outdir=None,
        postfix=None,
        imgn=1,
        force_trig=False,
        cap_mode=None,
        int_t=None,
        ctr_thresh=None,
        bin_thresh=None,
        bin_out=False, png_out=True,
        meta_out=True,
        xr=None,
        ):

    print("Preparing capture")

    if not outdir:
        outdir = util.default_date_dir("out", "", postfix)
    if not os.path.exists(outdir):
        util.mkdir_p(outdir)

    def cb(n, imgb):
        binfn = os.path.join(outdir, "cap_%02u.bin" % n)
        pngfn = os.path.join(outdir, "cap_%02u.png" % n)

        if bin_out:
            print('Writing %s' % binfn)
            open(binfn, 'w').write(imgb)

        if png_out:
            print('Decoding image...')
            img = gxs.decode(imgb)
            print('Writing %s...' % pngfn)
            img.save(pngfn)

        if meta_out:
            print('Saving meta...')
            gxs.write_json(outdir, force_trig=force_trig)

    gxs = usbint.GXS700()

    if cap_mode:
        gxs.set_cap_mode(cap_mode)
    if int_t:
        gxs.set_int_t(int_t)
    if ctr_thresh or bin_thresh:
        gxs.trig_param_w(
            pix_clust_ctr_thresh=ctr_thresh, bin_thresh=bin_thresh)
    gxs._init()

    gxs.cap_binv(imgn, cb, force_trig=force_trig, xr=xr)


def main():
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('--dir', default='', help='Output dir')
    parser.add_argument('--postfix', default='', help='Default output dir postfix')
    parser.add_argument(
        '--force', '-f', action='store_true', help='Force trigger')
    parser.add_argument(
        '--number', '-n', type=int, default=1, help='number to take')
    # Most users should not touch these
    parser.add_argument(
        '--int-t',
        type=int,
        default=None,
        help='Integration time in ms (default: 700)')
    parser.add_argument(
        '--ctr-thresh', type=int, default=None, help='Advanced')
    parser.add_argument(
        '--bin-thresh', type=int, default=None, help='Advanced')
    parser.add_argument(
        '--cap-mode',
        default=None,
        help='Advanced: norm (default), hblock, vblock, vbar')
    parser.add_argument(
        '--bin', '-b', action='store_true', help='Write .bin raw data capture')
    util.add_bool_arg(
        parser, '--png', default=True, help='Write normal .png image file')

    args = parser.parse_args()

    run(
        outdir=args.dir,
        postfix=args.postfix,
        imgn=args.number,
        force_trig=args.force,
        cap_mode=args.cap_mode,
        int_t=args.int_t,
        ctr_thresh=args.ctr_thresh,
        bin_thresh=args.bin_thresh)

if __name__ == "__main__":
    main()
