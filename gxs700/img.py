import struct
import numpy as np

# enum
SIZE_SM = 1
SIZE_LG = 2

WH_SM = (1040, 1552)
WH_LG = (1344, 1850)

# 16 bit image
SZ_SM = 2 * WH_SM[0] * WH_SM[1]
SZ_LG = 2 * WH_LG[0] * WH_LG[1]

unpack_pix = lambda x: struct.Struct('<H').unpack(x)[0]
pack_pix = struct.Struct('<H').pack


def sz_wh(sz):
    # Was bug capturing too much data, just below two frames
    if sz == SZ_LG or sz == 9937152:
        return WH_LG
    elif sz == SZ_SM:
        return WH_SM
    else:
        print((SZ_SM, SZ_LG))
        raise ValueError("Bad buffer size %s" % sz)



def raw2npim1(buff):
    '''Given raw string, return 1d array of 16 bit unpacked values'''
    depth = 2
    width, height = sz_wh(len(buff))

    buff = bytearray(buff)
    imnp = np.zeros(width * height)

    for i, y in enumerate(range(0, depth * width * height, depth)):
        imnp[i] = unpack_pix(buff[y:y + 2])
    return imnp

def get_bufF_sz(sz):
    return {1: SZ_SM, 2: SZ_LG}[sz]

def histeq_np(npim, nbr_bins=256):
    '''
    Given a numpy nD array (ie image), return a histogram equalized numpy nD array of pixels
    That is, return 2D if given 2D, or 1D if 1D
    '''

    # get image histogram
    imhist, bins = np.histogram(npim.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()  #cumulative distribution function
    cdf = 0xFFFF * cdf / cdf[-1]  #normalize

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


# This sort of works, but gives an 8 bit image
# Can I get it to work with mode I somehow instead?
def decode_l8(buff, wh=None):
    '''Given bin return PIL image object'''
    width, height = wh or img.sz_wh(len(buff))
    buff = str(buff[0:2 * width * height])

    # http://pillow.readthedocs.io/en/3.1.x/handbook/writing-your-own-file-decoder.html
    # http://svn.effbot.org/public/tags/pil-1.1.4/libImaging/Unpack.c
    img = Image.frombytes('L', (width, height), buff, "raw", "L;16", 0, -1)
    img = PIL.ImageOps.invert(img)
    img = img.transpose(PIL.Image.ROTATE_270)
    return img


def decode(buff, wh=None):
    '''Given bin return PIL image object'''
    depth = 2
    width, height = wh or img.sz_wh(len(buff))
    buff = bytearray(buff)

    # no need to reallocate each loop
    img = Image.new("I", (height, width), "White")

    for y in range(height):
        line0 = buff[y * width * depth:(y + 1) * width * depth]
        for x in range(width):
            b0 = line0[2 * x + 0]
            b1 = line0[2 * x + 1]

            G = (b1 << 8) + b0
            # optional 16-bit pixel truncation to turn into 8-bit PNG
            # G = b1

            # In most x-rays white is the part that blocks the x-rays
            # however, the camera reports brightness (unimpeded x-rays)
            # compliment to give in conventional form per above
            G = 0xFFFF - G

            img.putpixel((y, x), G)
    return img


def im2bin(im):
    '''Given PIL image object return bin'''
    depth = 2
    height, width = im.size
    ret = bytearray()

    for y in range(height):
        #line0 = buff[y * width * depth:(y + 1) * width * depth]
        line0 = bytearray(width * depth)
        for x in range(width):
            g = im.getpixel((y, x))
            g = 0xFFFF - g

            b0 = g & 0xFF
            b1 = (g >> 8) & 0xFF

            line0[2 * x + 0] = b0
            line0[2 * x + 1] = b1
        ret += line0
    return ret

