import time
from uvscada.wps7 import WPS7
import argparse

SW_HV = 1
SW_FIL = 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Planner module command line')
    parser.add_argument(
        '--fil', type=int, default=5, help='Filament warm time')
    parser.add_argument('--hv', type=int, default=3, help='HV fire time')
    args = parser.parse_args()

    wps = WPS7()
    print 'Warm %d sec, fire %d sec' % (args.fil, args.hv)

    try:
        print 'Warming filament %d sec...' % args.fil
        wps.on(SW_FIL)
        time.sleep(args.fil)

        print 'Nuking %d sec...' % args.hv
        wps.on(SW_HV)
        time.sleep(args.hv)
    finally:
        print 'Forcing HV off at exit'
        wps.off(SW_HV)
    print 'Done'
