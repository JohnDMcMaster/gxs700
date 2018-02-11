import gxs700_fw
import gxs700

from PIL import Image
import PIL.ImageOps

# https://github.com/vpelletier/python-libusb1
# Python-ish (classes, exceptions, ...) wrapper around libusb1.py . See docstrings (pydoc recommended) for usage.
import usb1
# Bare ctype wrapper, inspired from library C header file.
import numpy as np
import struct
import os

def check_device(usbcontext=None, verbose=True):
    if usbcontext is None:
        usbcontext = usb1.USBContext()

    for udev in usbcontext.getDeviceList(skip_on_error=True):
        vid = udev.getVendorID()
        pid = udev.getProductID()

        try:
            desc, _size = gxs700_fw.pidvid2name_post[(vid, pid)]
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
    if gxs700_fw.load_all(wait=True, verbose=verbose):
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
    _desc, size = gxs700_fw.pidvid2name_post[(vid, pid)]

    return usbcontext, dev, gxs700.GXS700(usbcontext, dev, verbose=verbose, size=size, init=init)

def ez_open(verbose=False):
    _usbcontext, _dev, gxs700 = ez_open_ex(verbose)
    return gxs700

def raw2npim1(buff):
    '''Given raw string, return 1d array of 16 bit unpacked values'''
    depth = 2
    width, height = gxs700.sz_wh(len(buff))

    buff = bytearray(buff)
    imnp =  np.zeros(width * height)
    i = 0
    for y in range(height):
        line0 = buff[y * width * depth:(y + 1) * width * depth]
        for x in range(width):
            b0 = line0[2*x + 0]
            b1 = line0[2*x + 1]

            imnp[i] = (b1 << 8) + b0
            i += 1
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
        ret += struct.pack('>H', int(rs[i]))
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
    width, height = wh or gxs700.sz_wh(len(buff))
    buff = str(buff[0:2 * width * height])

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
