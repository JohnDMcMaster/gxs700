'''
Related tools:
-fxload: tool that we want to feed into (also IDA...)
-cycfx2prog: allows dumping memory but not to bin or hex
'''

# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
import usb1
import binascii
import argparse
from gxs700.util import open_dev

verbose = False


def ram_w(dev, addr, data):
    bs = 16
    offset = 0
    while offset < len(data):
        l = min(bs, len(data) - offset)
        payload = data[offset:offset + l]
        print 'Write 0x%04X: %s' % (addr + offset, binascii.hexlify(payload))
        dev.controlWrite(0x40, 0xA0, addr + offset, 0x0000, payload, timeout=1000)
        offset += bs

def rst(dev, running):
    ram_w(dev, 0xe600, chr(int(bool(running))))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    args = parser.parse_args()

    usbcontext = usb1.USBContext()
    dev = open_dev(usbcontext)

    # Reset is accomplished by writing a 1 to address 0xE600. 
    rst(dev, 1)
    # Start running by writing a 0 to that address. 
    rst(dev, 0)
