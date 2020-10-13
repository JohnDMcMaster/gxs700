#!/usr/bin/env python3

from gxs700.util import add_bool_arg, default_date_dir
from gxs700 import im_util
from gxs700 import xray
from gxs700 import util
from gxs700 import process_main
from gxs700 import raw_main
import os

def main():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--verbose', action="store_true")
    add_bool_arg(parser, "--xray", default=None)
    add_bool_arg(parser, "--force-trig", default=None)
    parser.add_argument('--dir', default=None, help='Output dir')
    parser.add_argument(
        '--int-t',
        type=int,
        default=None,
        help='Integration time in ms (default: 700)')
    parser.add_argument('-n', default=1, type=int, help='Number images')
    parser.add_argument('--postfix', default=None, help='')
    parser.add_argument('--cal-dir', default=None, help='')
    parser.add_argument(
        '--hist-eq-roi', default="258,258,516,516", help='hist eq x1,y1,x2,y2')
    add_bool_arg(parser, "--hist-eq", default=True)
    add_bool_arg(parser, "--raw", default=False)
    parser.add_argument('fn_out', default=None, nargs='?', help='')
    args = parser.parse_args()

    outdir = args.dir
    if outdir is None:
        outdir = default_date_dir("out", "", args.postfix)

    xray = args.xray
    if xray is None:
        xray = os.getenv('WPS7_HOST', None) is not None
    if xray:
        print("Opening x-ray")
        xr = xray.WPS7XRay(verbose=args.verbose)
        util.mkdir_p(outdir)
        xr.write_json(outdir)
        xr.warm()
    else:
        xr = None

    try:
        force_trig = args.force_trig
        # Force a capture by default if not given
        if force_trig is None:
            force_trig = xr is None
        raw_main.run(
            outdir=outdir,
            postfix=args.postfix,
            imgn=args.n,
            int_t=args.int_t,
            force_trig=force_trig,
            xr=xr)
    # notably ^C can cause this
    finally:
        xr and xr.beam_off()

    process_main.run(
        outdir,
        args.fn_out,
        cal_dir=args.cal_dir,
        hist_eq=args.hist_eq,
        raw=args.raw,
        hist_eq_roi=im_util.parse_roi(args.hist_eq_roi))

    print("done")


if __name__ == "__main__":
    main()
