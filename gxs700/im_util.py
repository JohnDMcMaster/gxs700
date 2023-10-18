#!/usr/bin/env python3
from __future__ import print_function
import numpy as np
from PIL import Image
import glob
import os
import json


def parse_roi(s):
    if s is None:
        return None
    return [int(x) for x in s.split(',')]


def npf2im(statef):
    #return statef, None
    rounded = np.round(statef)
    #print("row1: %s" % rounded[1])
    statei = np.array(rounded, dtype=np.uint16)
    #print(len(statei), len(statei[0]), len(statei[0]))
    height = len(statef)
    width = len(statef[0])

    # for some reason I isn't working correctly
    # only L
    #im = Image.fromarray(statei, mode="I")
    #im = Image.fromarray(statei, mode="L")
    # workaround by plotting manually
    im = Image.new("I", (width, height), "Black")
    for y, row in enumerate(statei):
        for x, val in enumerate(row):
            # this causes really weird issues if not done
            val = int(val)
            im.putpixel((x, y), val)

    return im


def average_imgs(imgs, scalar=None):
    width, height = imgs[0].size
    if not scalar:
        scalar = 1.0
    scalar = scalar / len(imgs)

    statef = np.zeros((height, width), float)
    for im in imgs:
        assert (width, height) == im.size
        statef = statef + scalar * np.array(im, dtype=float)

    return statef, npf2im(statef)


def average_dir(din, images=0, verbose=1, scalar=None):
    imgs = []

    files = list(glob.glob(os.path.join(din, "cap_*.png")))
    verbose and print('Reading %s w/ %u images' % (din, len(files)))

    for fni, fn in enumerate(files):
        imgs.append(Image.open(fn))
        if images and fni + 1 >= images:
            verbose and print("WARNING: only using first %u images" % images)
            break
    return average_imgs(imgs, scalar=scalar)


# Tried misc other things but this was only thing I could make work
def im_inv16_slow(im):
    '''Invert 16 bit image pixels'''
    im32_2d = np.array(im)
    im32_1d = im32_2d.flatten()
    for i, p in enumerate(im32_1d):
        im32_1d[i] = 0xFFFF - p
    ret = Image.fromarray(im32_1d.reshape(im32_2d.shape))
    return ret


def default_cal_dir(j=None, im_dir=None):
    if im_dir:
        j = json.load(open(os.path.join(im_dir, "sensor.json"), "r"))
    assert j
    """
    {
        "force_trig": true,
        "int_time": 700,
        "mode": "norm",
        "size": 2,
        "sn_eeprom": 2093130284,
        "sn_flash": 2093130284,
        "trig_params": "000301f4"
    }
    """
    # serial numbers are unique across sizes
    # EEPROM is sometimes erased, but flash never is
    return os.path.join("cal", j["sn_flash"])


def histeq_im(im, nbr_bins=256):
    imnp2 = np.array(im)
    imnp2_eq = histeq_np(imnp2, nbr_bins=nbr_bins)
    imf = Image.fromarray(imnp2_eq)
    return imf.convert("I")


def histeq_np(npim, nbr_bins=256):
    '''
    Given a numpy nD array (ie image), return a histogram equalized numpy nD array of pixels
    That is, return 2D if given 2D, or 1D if 1D
    '''
    return histeq_np_apply(npim, histeq_np_create(npim, nbr_bins=nbr_bins))


def histeq_np_create(npim, nbr_bins=256, verbose=0):
    '''
    Given a numpy nD array (ie image), return a histogram equalized numpy nD array of pixels
    That is, return 2D if given 2D, or 1D if 1D
    '''

    # get image histogram
    flat = npim.flatten()
    verbose and print('flat', flat)
    imhist, bins = np.histogram(flat, nbr_bins)
    verbose and print('imhist', imhist)
    verbose and print('imhist', bins)
    cdf = imhist.cumsum()  #cumulative distribution function
    verbose and print('cdfraw', cdf)
    cdf = 0xFFFF * cdf / cdf[-1]  #normalize
    verbose and print('cdfnorm', cdf)
    return cdf, bins


def histeq_np_apply(npim, create):
    cdf, bins = create

    # use linear interpolation of cdf to find new pixel values
    ret1d = np.interp(npim.flatten(), bins[:-1], cdf)
    return ret1d.reshape(npim.shape)
