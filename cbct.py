from __future__ import print_function
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
import gxs700.usbint
import gxs700.util

from gxs700.xray import WPS7XRay

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    args = parser.parse_args()

    if os.getenv('WPS7_PASS', None) is None:
        raise Exception("Requires WPS7 password")

    usbcontext, dev, gxs = gxs700.util.ez_open_ex(verbose=args.verbose)

    fn = ''
    
    xray = WPS7XRay()

    print('Warming filament...')
    xray.fil_warm()
    '''
    Head likes 10% duty cycle
    3 second pulses
    About 30 seconds per image
    
    AS took 45 images (8 deg steps), follow his example initially
    400 steps per rev (200 actual * 2 microstep)
    72 rev => 360 deg =>  deg / rev
    400 * 8 / 5 = 640 steps each image
    TODO: verify this works as calculated
    
    hmm seems to be 800 per rev
    w/e, just fix it for now but figure out why later
    800 * 8 / 5 = 1280 steps each image
    '''
    to_take = 1
    IMG_STEPS = 1280
    indexer = Indexer(device='/dev/ttyUSB0')

    if 0:
        indexer.step('X', IMG_STEPS)
        sys.exit(1)

    try:
        ctn = 0
        taken = 0
        imagen = 0
        while os.path.exists('ct_%03d' % ctn):
            ctn += 1
        fn_d = 'ct_%03d' % ctn
        os.mkdir(fn_d)
        print('Taking first image to %s' % ('%s/ct_%03d.bin' %
                                            (fn_d, imagen), ))

        def fire():
            xray.fire(3)

        gxs.wait_trig_cb = fire

        def cap_cb(imgb):
            global taken
            global imagen

            fn = '%s/ct_%03d.bin' % (fn_d, imagen)
            print('Writing %s' % fn)
            open(fn, 'w').write(imgb)

            fn = '%s/ct_%03d.png' % (fn_d, imagen)
            print('Decoding %s' % fn)
            img = gxs700.usbint.GXS700.decode(imgb)
            print('Writing %s' % fn)
            img.save(fn)

            taken += 1
            imagen += 1

            return taken != to_take

        def loop_cb():
            print('TABLE: rotating')
            indexer.step('X', IMG_STEPS)

        gxs.cap_binv(1, cap_cb=cap_cb, loop_cb=loop_cb)
    finally:
        # Just in case
        print('X-RAY: BEAM OFF (on exit)')
        try:
            xray.beam_off()
        except:
            print('*' * 80)
            print('WARNING: FAILED TO DISARM X-RAY!!!')
            print('*' * 80)

    print('Done')
