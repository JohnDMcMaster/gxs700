#!/usr/bin/env python3
from PIL import Image
import numpy as np
import glob
import os


def histeq_np_create(npim, nbr_bins=256):
    '''
    Given a numpy nD array (ie image), return a histogram equalized numpy nD array of pixels
    That is, return 2D if given 2D, or 1D if 1D
    '''

    # get image histogram
    imhist, bins = np.histogram(npim.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()  #cumulative distribution function
    cdf = 0xFFFF * cdf / cdf[-1]  #normalize
    return cdf, bins


def histeq_np_apply(npim, create):
    cdf, bins = create

    # use linear interpolation of cdf to find new pixel values
    ret1d = np.interp(npim.flatten(), bins[:-1], cdf)
    return ret1d.reshape(npim.shape)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Histogram equalize an entire directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument(
        'ref_png', help='Reference image to use for distribution')
    parser.add_argument('din', help='Input directory or file')
    parser.add_argument('dout', help='Output directory or file')

    args = parser.parse_args()

    # Create
    ref_im = Image.open(args.ref_png)
    ref_np2 = np.array(ref_im)
    create = histeq_np_create(ref_np2)

    if not os.path.exists(args.dout):
        os.mkdir(args.dout)

    # Apply distribution to images
    for fn_in in glob.glob(args.din + '/*.png'):
        print 'Processing %s' % fn_in
        im_in = Image.open(fn_in)
        np_in2 = np.array(im_in)
        np_scaled = histeq_np_apply(np_in2, create)
        imc = Image.fromarray(np_scaled).convert("I")
        imc.save(os.path.join(args.dout, os.path.basename(fn_in)))
