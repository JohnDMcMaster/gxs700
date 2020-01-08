#!/usr/bin/env python
from __future__ import print_function
from gxs700.xray import WPS7XRay
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Planner module command line')
    parser.add_argument(
        '--fil', type=int, default=5, help='Filament warm time')
    parser.add_argument('--hv', type=int, default=3, help='HV fire time')
    args = parser.parse_args()

    xray = WPS7XRay()
    print('Warm %d sec, fire %d sec' % (args.fil, args.hv))
    xray.warm_time = args.fil
    xray.warm()
    xray.fire(args.hv)
    print('Done')
