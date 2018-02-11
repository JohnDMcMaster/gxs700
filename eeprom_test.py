'''
with the bad eeprom connected it didn't register sensor ID
however it did still do state probes
does this mean that it would continue to work even with a wiped eeprom?
how did I wipe it?

What is EEPROM1?
Could it be an FPGA and the bitstream is no longer loading?
Think its a SmartFusion
could be talking to an ARM/FPGA over SPI or something like that
what could cause it to stop booting?
Is there a mode pin I set?
Wrote a bad register to it?
 

eeprom1
    read:  controlRead( 0xC0, 0xB0, 0x0010
    write: 
eeprom2
    read:  controlRead( 0xC0, 0xB0, 0x000B
    write: controlWrite(0x40, 0xB0, 0x000C
'''

# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
import usb1
# Bare ctype wrapper, inspired from library C header file.
import libusb1
import binascii
import sys
import argparse
from util import hexdump
from util import open_dev
import dump_eeprom
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    args = parser.parse_args()

    usbcontext = usb1.USBContext()
    dev = open_dev(usbcontext)

    '''
    def controlWrite(self, request_type,
                    request, value, index, data,
                     timeout=0):
    '''
    print 'writing'
    dev.controlWrite(0x40, 0xB0, 0x000F, 0x0000, 'B' * 0x100)
    sys.exit(0)

    if 0:
        '''
        There's some funny math around the beginning
        its not a linear mapping
        seems to level out after the first 0x20 bytes
        writing to 0x10 writes to 0x0000...if large enough?
        
        think its supposed to be written 0x20 aligned
        '''
        if 0:
            '''
            the first 6 bytes are special
            but I did manage to erase them before
            00000000  FF FF FF FF FF FF 06 07  08 09 0A 0B 0C 0D 0E 0F  |................|
            00000010  10 11 12 13 14 15 16 17  18 19 1A 1B 1C 1D 1E 1F  |................|
            '''
            #for i in xrange(0x100):
            for i in xrange(0xFF):
                print 'Write %d' % i
                dev.controlWrite(0x40, 0xB0, 0x000C, i, chr(i) * 4)
        if 0:
            # does nothing
            #dev.controlWrite(    0x40, 0xB0, 0x000C, 0x0000, "\xCC" * 0x80)
        
            # writes first 0x20 bytes
            #dev.controlWrite(    0x40, 0xB0, 0x000C, 0x0010, "\xFF" * 0x80)
            dev.controlWrite(    0x40, 0xB0, 0x000C, 0x0010, "C" * 32)
        if 0:
            # writes 0x20:0x3F
            dev.controlWrite(    0x40, 0xB0, 0x000C, 0x0020, "\xDD" * 0x80)
        if 0:
            for i in xrange(0x2000 - 0x20, 0x2000, 0x20):
                print 'Write 0x%04X' % i
                dev.controlWrite(0x40, 0xB0, 0x000C, i, chr(i/0x80) * 0x20)
        dev.controlWrite(0x40, 0xB0, 0x000C, 0x0010, "A" * 32)
        sys.exit(1)


    if 0:
        '''
        0x00 0.000t error
        0x01 0.000t error
        0x02 0.000t okay
        0x03 0.000t okay
        0x04 0.000t okay
        0x05 0.000t error
        0x06 0.000t error
        0x07 0.000t error
        0x08 0.000t error
        0x09 0.000t error
        0x0A 0.000t okay
        0x0B 0.000t okay
        0x0C 0.000t okay
        0x0D 0.000t okay
        0x0E 0.000t okay
        0x0F 0.000t okay
        0x10 0.000t okay
        0x11 0.000t okay
        0x12 0.000t error
        0x13 0.000t error
        0x14 0.000t error
        0x15 0.000t error
        0x16 0.000t error
        0x17 0.000t error
        0x18 0.000t error
        0x19 0.000t error
        0x1A 0.000t error
        0x1B 0.000t error
        0x1C 0.000t error
        0x1D 0.000t error
        0x1E 0.000t error
        0x1F 0.000t error
        0x20 0.000t okay
        0x21 0.000t okay
        0x22 0.000t okay
        0x23 0.000t okay
        0x24 0.000t okay
        0x25 0.000t okay
        0x26 0.000t error
        0x27 0.000t error
        0x28 0.000t error
        0x29 0.000t error
        0x2A 0.000t error
        0x2B 0.000t okay
        0x2C 0.000t okay
        0x2D 0.000t okay
        0x2E 0.000t okay
        0x2F 0.000t okay
        0x30 0.000t error
        0x31 0.000t okay
        0x32 0.000t okay
        0x33 0.000t okay
        0x34: frooze
        0x35 0.000t okay
        0x36: frooze
        '''
        for i in xrange(0x00, 0x12):
            try:
                dev.controlWrite(0x40, 0xB0, i, 0x0020, 'A' * 0x20)
                print '0x%02X %0.3ft okay' % (i, 0)
            except libusb1.USBError:
                print '0x%02X %0.3ft error' % (i, 0)
        sys.exit(1)


    
    if 0:
        i = 0
        while True:
            # /usr/local/lib/python2.7/dist-packages/usb1.py
            print 'Iter %d' % i
            # def controlWrite(self, request_type, request, value, index, data,
            #request_type = random.randint(0x00, 0xFF)
            request_type = 0x40
            request = random.randint(0x00, 0xFF)
            value = random.randint(0x00, 0xFF)
            #index = 0x0000
            index = random.randint(0x00, 0xFF)
            
            try:
                try:
                    dev.controlWrite(request_type, request, value, index, 'A' * 0x20, timeout=1000)
                    print '%d %0.3ft okay' % (i, 0)
                except libusb1.USBError:
                    print '%d %0.3ft error' % (i, 0)

                r = dump_eeprom.read1(dev, 0x0000, 0x20)
                if r != ('\xFF' * 0x20):
                    print 'Found result'
                    print 'request_type: 0x%02X' % request_type
                    print 'request: 0x%02X' % request
                    print 'value: 0x%04X' % value
                    print 'index: 0x%04X' % index
                    break
            except libusb1.USBError as e:
                if e.value == -7:
                    print 'LIBUSB_ERROR_TIMEOUT'
                else:
                    raise
            i += 1

