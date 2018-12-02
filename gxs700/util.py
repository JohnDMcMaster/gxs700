import fw
import usbint
import sys
import datetime
import shutil
import struct

import PIL
from PIL import Image
#import PIL.ImageOps

# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
import usb1
# Bare ctype wrapper, inspired from library C header file.
import numpy as np
import struct
import os

unpack_pix = lambda x: struct.Struct('<H').unpack(x)[0]
pack_pix = struct.Struct('<H').pack

def check_device(usbcontext=None, verbose=True):
    if usbcontext is None:
        usbcontext = usb1.USBContext()

    for udev in usbcontext.getDeviceList(skip_on_error=True):
        vid = udev.getVendorID()
        pid = udev.getProductID()

        try:
            desc, _size = fw.pidvid2name_post[(vid, pid)]
        except KeyError:
            continue

        if verbose:
            print
            print
            print 'Found device (post-FW): %s' % desc
            print 'Bus %03i Device %03i: ID %04x:%04x' % (
                udev.getBusNumber(),
                udev.getDeviceAddress(),
                vid,
                pid)
        return udev
    return None

def open_dev(usbcontext=None, verbose=None):
    '''
    Return a device with the firmware loaded
    '''

    verbose = verbose if verbose is not None else os.getenv('GXS700_VERBOSE', 'N') == 'Y'

    if usbcontext is None:
        usbcontext = usb1.USBContext()

    print 'Checking if firmware load is needed'
    if fw.load_all(wait=True, verbose=verbose):
        print 'Loaded firmware'
    else:
        print 'Firmware load not needed'

    print 'Scanning for loaded devices...'
    udev = check_device(usbcontext, verbose=verbose)
    if udev is None:
        raise Exception("Failed to find a device")

    dev = udev.open()
    return dev

def ez_open_ex(verbose=False, init=True):
    usbcontext = usb1.USBContext()
    dev = open_dev(usbcontext, verbose=verbose)

    # FW load should indicate size
    vid = dev.getDevice().getVendorID()
    pid = dev.getDevice().getProductID()
    _desc, size = fw.pidvid2name_post[(vid, pid)]

    return usbcontext, dev, usbint.GXS700(usbcontext, dev, verbose=verbose, size=size, init=init)

def ez_open(verbose=False):
    _usbcontext, _dev, gxs700 = ez_open_ex(verbose)
    return gxs700

def raw2npim1(buff):
    '''Given raw string, return 1d array of 16 bit unpacked values'''
    depth = 2
    width, height = usbint.sz_wh(len(buff))

    buff = bytearray(buff)
    imnp =  np.zeros(width * height)
    
    for i, y in enumerate(range(0, depth * width * height, depth)):
        imnp[i] = unpack_pix(buff[y:y+2])
    return imnp

def histeq_np(npim, nbr_bins=256):
    '''
    Given a numpy nD array (ie image), return a histogram equalized numpy nD array of pixels
    That is, return 2D if given 2D, or 1D if 1D
    '''

    # get image histogram
    imhist,bins = np.histogram(npim.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum() #cumulative distribution function
    cdf = 0xFFFF * cdf / cdf[-1] #normalize

    # use linear interpolation of cdf to find new pixel values
    ret1d = np.interp(npim.flatten(), bins[:-1], cdf)
    return ret1d.reshape(npim.shape)

def npim12raw(rs):
    '''
    Given a numpy 1D array of pixels, return a string as if a raw capture
    '''
    ret = bytearray()
    
    for i in xrange(len(rs)):
        ret += pack_pix(int(rs[i]))
    return str(ret)

# Tried misc other things but this was only thing I could make work
def im_inv16_slow(im):
    '''Invert 16 bit image pixels'''
    im32_2d = np.array(im)
    im32_1d = im32_2d.flatten()
    for i, p in enumerate(im32_1d):
        im32_1d[i] = 0xFFFF - p
    ret = Image.fromarray(im32_1d.reshape(im32_2d.shape))
    return ret

def decode_i16(buff, wh=None):
    '''
    Given raw bin return PIL image object
    '''
    width, height = wh or usbint.sz_wh(len(buff))
    # Some older files had extra data
    # Consider removing in favor of just truncating the files on disk
    buff = str(buff[0:2 * width * height])

    # TODO: currently flipping image to preserve original behavior, but probably shouldn't be
    im = Image.frombytes('I', (width, height), buff, "raw", "I;16", 0, -1)
    # IOError: not supported for this image mode
    # im =  PIL.ImageOps.invert(im)
    im = im_inv16_slow(im)
    im = im.transpose(PIL.Image.ROTATE_270)
    return im

# Tried to do
# import PIL.ImageOps
# img = PIL.ImageOps.equalize(img)
# but
# IOError: not supported for this image mode
# http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html
def histeq(buff, nbr_bins=256):
    '''Histogram equalize raw buffer, returning a raw buffer'''
    npim1 = raw2npim1(buff)
    npim1_eq = histeq_np(npim1, nbr_bins)
    return npim12raw(npim1_eq)

def histeq_im(im, nbr_bins=256):
    imnp2 = np.array(im)
    imnp2_eq = histeq_np(imnp2, nbr_bins=nbr_bins)
    imf = Image.fromarray(imnp2_eq)
    return imf.convert("I")

def ram_r(dev, addr, datal):
    bs = 16
    offset = 0
    ret = bytearray()
    while offset < datal:
        l = min(bs, datal - offset)
        #print 'Read 0x%04X: %d' % (addr + offset, l)
        ret += dev.controlRead(0xC0, 0xA0, addr + offset, 0x0000, l, timeout=1000)
        offset += bs
    return str(ret)

def sn_flash_r(gxs):
    s = gxs.flash_r(addr=0x0C, n=11).replace('\x00', '')
    return int(s)

def sn_eeprom_r(gxs):
    s = gxs.eeprom_r(addr=0x40, n=11).replace('\x00', '')
    return int(s)

def add_bool_arg(parser, yes_arg, default=False, **kwargs):
    dashed = yes_arg.replace('--', '')
    dest = dashed.replace('-', '_')
    parser.add_argument(yes_arg, dest=dest, action='store_true', default=default, **kwargs)
    parser.add_argument('--no-' + dashed, dest=dest, action='store_false', **kwargs)

def hexdump(data, label=None, indent='', address_width=8, f=sys.stdout):
    def isprint(c):
        return c >= ' ' and c <= '~'

    if label:
        print label
    
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

# Print timestamps in front of all output messages
class IOTimestamp(object):
    def __init__(self, obj=sys, name='stdout'):
        self.obj = obj
        self.name = name
        
        self.fd = obj.__dict__[name]
        obj.__dict__[name] = self
        self.nl = True

    def __del__(self):
        if self.obj:
            self.obj.__dict__[self.name] = self.fd

    def flush(self):
        self.fd.flush()
       
    def write(self, data):
        parts = data.split('\n')
        for i, part in enumerate(parts):
            if i != 0:
                self.fd.write('\n')
            # If last bit of text is just an empty line don't append date until text is actually written
            if i == len(parts) - 1 and len(part) == 0:
                break
            if self.nl:
                self.fd.write('%s: ' % datetime.datetime.utcnow().isoformat())
            self.fd.write(part)
            # Newline results in n + 1 list elements
            # The last element has no newline
            self.nl = i != (len(parts) - 1)

# Log file descriptor to file
class IOLog(object):
    def __init__(self, obj=sys, name='stdout', out_fn=None, out_fd=None, mode='a', shift=False, multi=False):
        if not multi:
            if out_fd:
                self.out_fd = out_fd
            else:
                self.out_fd = open(out_fn, 'w')
        else:
            # instead of jamming logs together, shift last to log.txt.1, etc
            if shift and os.path.exists(out_fn):
                i = 0
                while True:
                    dst = out_fn + '.' + str(i)
                    if os.path.exists(dst):
                        i += 1
                        continue
                    shutil.move(out_fn, dst)
                    break
            
            hdr = mode == 'a' and os.path.exists(out_fn)
            self.out_fd = open(out_fn, mode)
            if hdr:
                self.out_fd.write('*' * 80 + '\n')
                self.out_fd.write('*' * 80 + '\n')
                self.out_fd.write('*' * 80 + '\n')
                self.out_fd.write('Log rolled over\n')
        
        self.obj = obj
        self.name = name
        
        self.fd = obj.__dict__[name]
        obj.__dict__[name] = self
        self.nl = True

    def __del__(self):
        if self.obj:
            self.obj.__dict__[self.name] = self.fd

    def flush(self):
        self.fd.flush()
       
    def write(self, data):
        self.fd.write(data)
        self.out_fd.write(data)
