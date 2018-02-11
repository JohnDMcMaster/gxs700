'''
FIXME: extract firmware from this and properly pass it to fxload
'''

# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
import usb1
# Bare ctype wrapper, inspired from library C header file.
import libusb1
import binascii
import sys
import argparse
import time
import gxs700_util
import gxs700_fw_sm
import gxs700_fw_lg

'''
small sensor from adam
both large and small enumerate the same
how to tell them apart?
stage1 verified identical
stage2 curosry glance looks identical (not to mention same VID/PID)

Bus 003 Device 029: ID 5328:202f  
Bus 003 Device 030: ID 5328:2030  

dexis
pre-enumer
post-enumeration
Bus 003 Device 036: ID 5328:2010  
'''
pidvid2name_pre = {
        # (vid, pid): (desc, firmware load)
        (0x5328, 0x2009): ('Dexis Platinum (pre-enumeration)', gxs700_fw_lg),
        (0x5328, 0x201F): ('Gendex GXS700SM (pre-enumeration)', gxs700_fw_sm),
        (0x5328, 0x202F): ('Gendex GXS700LG (pre-enumeration)', gxs700_fw_lg),
        # ooops
        # Bus 002 Device 043: ID 04b4:8613 Cypress Semiconductor Corp. CY7C68013 EZ-USB FX2 USB 2.0 Development Kit
        (0x04b4, 0x8613): ('CY7C68013 EZ-USB FX2 USB 2.0 Development Kit', gxs700_fw_lg),
        }

pidvid2name_post = {
        # note: load_firmware.py deals with pre-enumeration
        # (vid, pid): (desc, size)
        (0x5328, 0x2010): ('Dexis Platinum (post-enumeration)', 2),
        (0x5328, 0x2020): ('Gendex GXS700SM (post enumeration)', 1),
        (0x5328, 0x2030): ('Gendex GXS700LG (post enumeration)', 2),
        }

def load_all(wait=False, verbose=True):
    ret = False
    usbcontext = usb1.USBContext()
    if verbose:
        print 'Scanning for devices...'
    for udev in usbcontext.getDeviceList(skip_on_error=True):
        vid = udev.getVendorID()
        pid = udev.getProductID()

        try:
            desc, fwmod = pidvid2name_pre[(vid, pid)]
        except KeyError:
            continue

        if verbose:
            print
            print
            print 'Found device (pre-FW): %s' % desc
            print 'Bus %03i Device %03i: ID %04x:%04x' % (
                udev.getBusNumber(),
                udev.getDeviceAddress(),
                vid,
                pid)
            print 'Loading firmware'
        load(udev.open(), fwmod)
        if verbose:
            print 'Firmware load OK'
        ret = True

    if ret and wait:
        print 'Waiting for device to come up'
        tstart = time.time()
        while time.time() - tstart < 3.0:
            udev = gxs700_util.check_device()
            if udev:
                break
        else:
            raise Exception("Renumeration timed out")
        print 'Up after %0.1f sec' % (time.time() - tstart,)

    return ret

def load(dev, fwmod=gxs700_fw_lg):
    # Source data: cap1.cap
    # Source range: 107 - 286
    
    # 2017-08-07: below comment indicates that I tested small at some point
    # but I don't have a small so I guess never added supported
    # TODO: re-verify this and shrink the code
    # Verified stage1 is the same for gendex small and large
    fwmod.stage1(dev)
    # xxx: should sleep here?
    fwmod.stage2(dev)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    args = parser.parse_args()

    load_all()
