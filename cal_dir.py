#!/usr/bin/env python3

from gxs700 import usbint
from gxs700 import im_util

def main():
    import argparse 
    
    parser = argparse.ArgumentParser(description='Get default calibration file directory for attached sensor')
    _args = parser.parse_args()

    gxs = usbint.GXS700(do_print=False)
    print(im_util.default_cal_dir(j=gxs.get_json()))

if __name__ == "__main__":
    main()
