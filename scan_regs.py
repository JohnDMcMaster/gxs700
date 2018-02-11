# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
import usb1
# Bare ctype wrapper, inspired from library C header file.
import libusb1
import binascii
import sys
import argparse
from util import open_dev
import time

'''
I seem to have somehow cleared the eeprom or something of that sort...
'''

verbose = False

def nulls(s, offset):
    end = s.find('\x00', offset)
    if end < 0:
        return s[offset:]
    else:
        return s[offset:end]

def hexdumps(*args, **kwargs):
    '''Hexdump by returning a string'''
    buff = StringIO.StringIO()
    kwargs['f'] = buff
    hexdump(*args, **kwargs)
    return buff.getvalue()

def hexdump(data, label=None, indent='', address_width=8, f=sys.stdout):
    def isprint(c):
        return c >= ' ' and c <= '~'

    bytes_per_half_row = 8
    bytes_per_row = 16
    data = bytearray(data)
    data_len = len(data)
    
    def hexdump_half_row(start):
        left = max(data_len - start, 0)
        
        real_data = min(bytes_per_half_row, left)

        f.write(''.join('%02X ' % c for c in data[start:start+real_data]))
        f.write(''.join('   '*(bytes_per_half_row-real_data)))
        f.write(' ')

        return start + bytes_per_half_row

    pos = 0
    while pos < data_len:
        row_start = pos
        f.write(indent)
        if address_width:
            f.write(('%%0%dX  ' % address_width) % pos)
        pos = hexdump_half_row(pos)
        pos = hexdump_half_row(pos)
        f.write("|")
        # Char view
        left = data_len - row_start
        real_data = min(bytes_per_row, left)

        f.write(''.join([c if isprint(c) else '.' for c in str(data[row_start:row_start+real_data])]))
        f.write((" " * (bytes_per_row - real_data)) + "|\n")

pidvid2name = {
        (0x5328, 0x2030): 'Gendex GXS700 (post enumeration)'
        }

# At least 0x400 size EEPROM
# with just over 0x200 used
# higher addresses read FF, so its hard to tell how big it actually is
# (ie didn't wrap around)
# 0x200 seems to work but original code uses 0x100
#EEPROM_RMAX = 0x200
EEPROM_RMAX = 0x100
def eeprom_r(dev, addr, l):
    # gives all 0's if you request more than 0x200 bytes
    if l > 0x200:
        raise Exception("Invalid read size 0x%04X" % l)
    res = dev.controlRead(0xC0, 0xB0, 0x0010, addr, l)
    if len(res) != l:
        raise Exception("requested 0x%04X bytes but got 0x%04X" % (dump_len, len(res),))
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replay captured USB packets')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('--fn', '-f', help='write bin to filename')
    args = parser.parse_args()

    usbcontext = usb1.USBContext()
    dev = open_dev(usbcontext)

    print 'Begin'

    #dev.controlWrite(0x40, 0xB0, 0x000C, 0x0020, "\x32\x30\x31\x35\x2F\x30\x33\x2F\x31\x39\x2D\x32\x31\x3A\x34\x34"
    #          "\x3A\x34\x33\x3A\x30\x38\x37")
    #dev.controlWrite(0x40, 0xB0, 0x000C, 0x0020, "2015/03/19-21:44:43:087")
    #dev.controlWrite(0x40, 0xB0, 0x000C, 0x0010, "A" * 32)


    '''
    # 0x03 read:        00040005
    # 0x03 0.001t read: 00040005fc7c5390
    # appears to be some sort of memory?
    # reads are somewhat irregular and vary at each address
    # could be RAM or general register space
    
    # there are a lot of writes to this
    # it looks like this could be I2C bus / register map
    # dev.controlWrite(0x40, 0xB0, 0x0002, 0x0400, "\x00\x00\x60\x00\x00\x00")
    # dev.controlWrite(0x40, 0xB0, 0x0002, 0x0404, "\x00\xE5\xC0\x00\x00\x00")
    # 6 byte writes are odd, almost like command + data?
    
    also some larger ones
    dev.controlWrite(0x40, 0xB0, 0x0002, 0x1000, "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    dev.controlWrite(0x40, 0xB0, 0x0002, 0x1008, "\x00\x02\x00\x00\x00\x00\x90\x00\x00\x00")
    
    further indicates there are two bytes of overhead and n - 2 payload bytes
    
    buff = dev.controlRead(0xC0, 0xB0, 0x0003, 0x2002, 2)
    validate_read("\x00\x00", buff, "packet 453/454", True)    
    '''
    if 0:
        # can't reproduce the larger read in small
        # 00000000  00 04 00 05 00 00 00 00                           |........        |
        print '0x03'
        if 0:
            buff = dev.controlRead(0xC0, 0xB0, 0x03, 0, 8, timeout=100)
            hexdump(buff)
            #print '0x%04X read: %s' % (i, binascii.hexlify(buff))
        if 1:
            '''
            repeats
            
            0x0000 read: 00040005
            0x0001 read: 00050000
            0x0002 read: 00000000
            0x0003 read: 00000005
            0x0004 read: 00000000
            0x0005 read: 00000000
            0x0006 read: 00000000
            0x0007 read: 00000004
            
            then other semi-regular patterns
            nothing I can make def sense of
            '''
            for i in xrange(0x10000):
                buff = dev.controlRead(0xC0, 0xB0, 0x03, i, 4, timeout=100)
                print '0x%04X read: %s' % (i, binascii.hexlify(buff))

        
        
    '''    
    buff = dev.controlRead(0xC0, 0xB0, 0x0004, 0x0000, 2)
    validate_read("\x12\x34", buff, "packet 455/456")
    '''
    # 0x04 read: 1234
    if 0:
        # all 1234
        print '0x04'
        for i in xrange(0x10000):
            buff = dev.controlRead(0xC0, 0xB0, 0x04, i, 2, timeout=100)
            if buff != '\x12\x34':
                print '0x%04X read: %s' % (i, binascii.hexlify(buff))
            
    # 0x0B read: 41414141
    if 0:
        '''
        has that non-volatile memory that I smacked
        has the serial number...?
        ROM wraps around at adddress 0x2000 => 8 KB
        
        00000000  41 41 41 41 41 41 41 41  49 41 41 00 00 00 00 00  |AAAAAAAAIAA.....|
        00000010  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
        00000020  32 30 31 35 2F 30 33 2F  31 39 2D 32 31 3A 34 34  |2015/03/19-21:44|
        00000030  3A 34 33 3A 30 38 37 41  41 41 41 41 41 41 41 41  |:43:087AAAAAAAAA|
        00000040  32 31 30 33 32 33 31 36  36 33 00 FF FF 00 74 E2  |2103231663....t.|
        00000050  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  |................|        '''
        print '0x0B'
        if 1:
            buff = dev.controlRead(0xC0, 0xB0, 0x0B, 0x2000, 0x80, timeout=100)
            hexdump(buff)
        if 0:
            for i in xrange(0x10000):
                buff = dev.controlRead(0xC0, 0xB0, 0x0B, i, 4, timeout=100)
                print '0x%04X read: %s' % (i, binascii.hexlify(buff))
    
    # 0x0D: 41414141
    if 0:
        # seems to be identical to above
        print '0x0D'
        if 1:
            buff = dev.controlRead(0xC0, 0xB0, 0x0D, 0x2000, 0x80, timeout=100)
            hexdump(buff)
    
    '''
    this is the EEPROM array
    what did I do to get 00's..
    ah
    probably messed up the i2c bus
    '''
    # 0x10: 02148245
    if 0:
        # only getting F's
        # may be some sort of buffer reading an old value
        # note quite
        # 000001F0  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  |................|
        # 00000200  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
        print '0x10'
        if 1:
            buff = dev.controlRead(0xC0, 0xB0, 0x10, 0x4000, 0x400, timeout=1000)
            hexdump(buff)
    
    '''
    # 0x20: 01
    Capture state
    buff = dev.controlRead(0xC0, 0xB0, 0x0020, 0x0000, 1)
    validate_read("\x01", buff, "packet 761/762", True)
    '''
    if 0:
        print '0x20'
    
    '''
    # 0x23 read: 1233c364
    
    register space?
    
    buff = dev.controlRead(0xC0, 0xB0, 0x0003, 0x2002, 2)
    validate_read("\x00\x00", buff, "packet 453/454", True)
    
    buff = dev.controlRead(0xC0, 0xB0, 0x0004, 0x0000, 2)
    validate_read("\x12\x34", buff, "packet 455/456")
    '''
    if 0:
        print '0x23'
        for i in xrange(0x10000):
            buff = dev.controlRead(0xC0, 0xB0, 0x23, i, 2, timeout=100)
            print '0x%04X read: %s' % (i, binascii.hexlify(buff))
    
    
    # 0x25 read: 1233c364
    if 0:
        print '0x25'
    # 0x2D read: 1233
    if 0:
        print '0x2D'
    # 0x31 read: f7dbf3b8
    if 0:
        print '0x31'
    
    '''
    # Generated from packet 837/838
    buff = dev.controlRead(0xC0, 0xB0, 0x0051, 0x0000, 28)
    # NOTE:: req max 28 but got 12
    validate_read("\x00\x05\x00\x0A\x00\x03\x00\x06\x00\x04\x00\x05", buff, "packet 837/838")
    '''
    if 0:
        print '0x51'
        
    '''
    gets polled often but always returns 0
    
    buff = dev.controlRead(0xC0, 0xB0, 0x0080, 0x0000, 1)
    validate_read("\x00", buff, "packet 1181/1182")
    '''
    # 0x80 read: 00
    if 0:
        print '0x80'


    

    if 0:
        '''
        read size 1
            0x31 0.000t read: f6
                0x31 0.000t read: f7
            0x80 0.001t read: 00
        read size 2        
            0x03 0.001t read: 0004
            0x04 0.000t read: 1234
            0x0B 0.068t read: 4141
            0x0C 1.000t error
            0x0D 0.091t read: 4141
            0x10 0.001t read: 4141
            0x20 0.000t read: 01
            0x2D 0.000t read: 0000
            0x31 0.000t read: f7db
            0x80 0.001t read: 00
        read size 4
            0x03 0.001t read: 00040005
            0x04 0.000t read: 1234
            0x0B 0.089t read: 41414141
            0x0D 0.091t read: 41414141
            0x10 0.001t read: 41414141
            0x20 0.001t read: 01
            0x23 0.001t read: 00004141
            0x25 0.001t read: 00004141
            0x2D 0.001t read: 0000
            0x31 0.000t read: f7dbf3b8
            0x80 0.000t read: 00
        read size 8
            0x03 0.001t read: 00040005fc7c5390
            0x04 0.000t read: 1234
            0x0B 0.091t read: 4141414141414141
            0x0D 0.091t read: 4141414141414141
            0x10 0.001t read: 4141414141414141
            0x20 0.001t read: 01
            0x23 0.001t read: 00004141
            0x25 0.001t read: 00004141
            0x2D 0.001t read: 0000
            0x31 0.000t read: f6dbf3b8eff3fe3f
            0x40 0.091t read: 4941410049414100
            0x80 0.000t read: 00

        
        '''
        for i in xrange(0x40, 0x100, 1):
            tstart = time.time()
            try:
                buff = dev.controlRead(0xC0, 0xB0, i, 0x0000, 8, timeout=1000)
            except libusb1.USBError:
                tend = time.time()
                print '0x%02X %0.3ft error' % (i, tend - tstart)
                time.sleep(0.3)
                continue
            tend = time.time()
            print '0x%02X %0.3ft read: %s' % (i, tend - tstart, binascii.hexlify(buff))
        
    
    print 'End'

