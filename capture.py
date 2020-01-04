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

kvp_user = None
ma_user = None


def meta(gxs):
    sn_flash = usbint.sn_flash_r(gxs)
    try:
        sn_eeprom = usbint.sn_eeprom_r(gxs)
    except:
        sn_eeprom = None

    return {
        'size': gxs.size,
        'sn_flash': sn_flash,
        'sn_eeprom': sn_eeprom,
        'int_time': gxs.int_time(),
        'trig_params': binascii.hexlify(gxs.trig_param_r()),
        'mode': usbint.cap_mode2s(gxs.cap_mode)
    }


def run(
        force,
        cap_mode=None,
        int_t=None,
        ctr_thresh=None,
        bin_thresh=None,
):

    itrs = [None]

    def scan_cb(itr):
        itrs[0] = itr
        if force and itr == 0:
            print('Forcing trigger')
            gxs.sw_trig()

    def cb(imgb):
        base = os.path.join(args.dir, 'capture_%03d' % imagen[0])
        if args.bin:
            fn = base + '.bin'
            print('Writing %s' % fn)
            open(fn, 'w').write(imgb)

        if args.png:
            pngfn = base + '.png'
            print('Decoding image...')
            img = usbint.GXS700.decode(imgb)
            print('Writing %s...' % pngfn)
            img.save(pngfn)

        if args.hist_eq:
            pngfn = base + '_e.png'
            print('Equalizing histogram...')
            imgb = img.histeq(imgb)
            print('Decoding image...')
            img = usbint.GXS700.decode(imgb)
            print('Writing %s...' % pngfn)
            img.save(pngfn)

        if args.meta:
            print('Saving meta...')
            fn = base + '.json'
            j = {
                'sensor': meta(gxs),
                'x-ray': {
                    'kvp_user': kvp_user,
                    'ma_user': ma_user,
                },
                'force': force,
                'itr': itrs[0],
            }
            json.dump(j, open(fn, 'w'), indent=4, sort_keys=True)

        imagen[0] += 1

    _usbcontext, _dev, gxs = usbint.ez_open_ex(verbose=args.verbose, init=False)

    if cap_mode:
        gxs.cap_mode = cap_mode
    if int_t:
        gxs.int_t = int_t
    if ctr_thresh or bin_thresh:
        gxs.trig_param_w(
            pix_clust_ctr_thresh=ctr_thresh, bin_thresh=bin_thresh)
    gxs._init()
    #gxs.fpga_off()

    if not os.path.exists(args.dir):
        os.mkdir(args.dir)

    imagen = [0]
    while glob.glob('%s/capture_%03d*' % (args.dir, imagen[0])):
        imagen[0] += 1
    print('Taking first image to %s' % ('%s/capture_%03d.bin' %
                                        (args.dir, imagen[0]), ))

    gxs.cap_binv(args.number, cb, scan_cb=scan_cb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('--dir', default='out', help='Output dir')
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
    parser.add_argument(
        '--hist-eq',
        '-e',
        action='store_true',
        help='Write histogram equalized .png image file')
    util.add_bool_arg(
        parser, '--meta', default=True, help='Write metadata .json file')
    parser.add_argument('--kvp', default=None, help='Metadata kVp comment')
    parser.add_argument('--ma', default=None, help='Metadata mA comment')

    args = parser.parse_args()

    kvp_user = args.kvp
    ma_user = args.ma

    run(force=args.force,
        cap_mode=args.cap_mode,
        int_t=args.int_t,
        ctr_thresh=args.ctr_thresh,
        bin_thresh=args.bin_thresh)
