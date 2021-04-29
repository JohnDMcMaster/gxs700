#!/usr/bin/env python3
'''
TODO: move to uvscada or similar

Cone Beam Computed Tomography (CBCT) toy
Was used to create: https://www.youtube.com/watch?v=pYvjq0rDXzI

Three major dependencies:
-x-ray sensor
-indexer controller
-web power switch

Don't start unless all of them are present and seem healthy
'''

# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
# Bare ctype wrapper, inspired from library C header file.
import argparse
import os
import sys

# XXX: this was removed in favor of LinuxCNC
# Code needs to be ported
#from uvscada.pr0ndexer import Indexer
from gxs700 import usbint
from gxs700 import util
from gxs700 import img
from gxs700.util import add_bool_arg, default_date_dir

from gxs700.xray import WPS7XRay

from uscope.hal.cnc import lcnc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--dir', default=None, help='Output dir')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('--steps', type=int, help='Number of slices per 180 degrees')
    parser.add_argument('--range', type=float, default=180.0, help='Maximum unit value to sweep')
    args = parser.parse_args()

    force_trig = False
    bin_out = False
    png_out = True
    meta_out = True

    outdir = args.dir
    if outdir is None:
        outdir = default_date_dir("out", "", args.postfix)
    util.mkdir_p(outdir)

    if os.getenv('WPS7_PASS', None) is None:
        raise Exception("Requires WPS7 password")

    hal = lcnc.LcncPyHal(host=args.host,
                              dry=args.dry)
    gxs = usbint.GXS700()

    xray = args.xray
    if xray is None:
        xray = os.getenv('WPS7_HOST', None) is not None
    print("Opening x-ray")
    xr = xray.WPS7XRay(verbose=args.verbose)

    xr.write_json(outdir)
    xr.warm()

    try:
        taken = 0
        imagen = 0

        def cb(n, imgb):
            assert n == 1
            binfn = os.path.join(outdir, "cap_%03u.bin" % imagen)
            pngfn = os.path.join(outdir, "cap_%03u.png" % imagen)
    
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

        # XXX: ideally would be in degrees but might not be
        step_units = args.range / args.steps
        print("Rotary step size: %0.3f" % step_units)

        for imagen in range(args.steps):
            x = step_units * imagen
            print('Rotating to %0.3f' % x)
            hal.mv_abs({'X': x})
            print('Capturing...')
            gxs.cap_binv(1, cb, force_trig=force_trig, xr=xr)
    finally:
        # Just in case
        print('X-RAY: BEAM OFF (on exit)')
        try:
            xr.beam_off()
        except:
            print('*' * 80)
            print('WARNING: FAILED TO DISARM X-RAY!!!')
            print('*' * 80)

    print('Done')
