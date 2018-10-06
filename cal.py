#!/usr/bin/env python
from PIL import Image
import PIL.ImageOps
import numpy as np
import glob
import os

def dir2np(d):
    np_df2s = []
    for fn in glob.glob(d + '/*.png'):
        np_df2s.append(np.array(Image.open(fn)))
    return np.average(np_df2s)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Correct images against darkfield and flat field capture')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')
    parser.add_argument('df_png', help='Dark field .png ("force capture")')
    parser.add_argument('ff_png', help='Flat field .png ("no sample")')
    parser.add_argument('din', help='Input directory or file')
    parser.add_argument('dout', help='Output directory or file')

    args = parser.parse_args()

    if os.path.isdir(args.df_png):
        np_df2 = dir2np(args.df_png)
    else:
        np_df2 = np.array(Image.open(args.df_png))

    if os.path.isdir(args.ff_png):
        np_ff2 = dir2np(args.ff_png)
    else:
        np_ff2 = np.array(Image.open(args.ff_png))

    # ff *should* be brighter than df
    # (due to .png pixel value inversion convention)
    mins = np.minimum(np_df2, np_ff2)
    maxs = np.maximum(np_df2, np_ff2)

    u16_mins = np.full(mins.shape, 0x0000, dtype=np.dtype('float'))
    u16_ones = np.full(mins.shape, 0x0001, dtype=np.dtype('float'))
    u16_maxs = np.full(mins.shape, 0xFFFF, dtype=np.dtype('float'))

    cal_det = maxs - mins
    # Prevent div 0 on bad pixels
    cal_det = np.maximum(cal_det, u16_ones)
    cal_scalar = 0xFFFF / cal_det

    if not os.path.exists(args.dout):
        os.mkdir(args.dout)

    for fn_in in glob.glob(args.din + '/*.png'):
        print 'Processing %s' % fn_in
        im_in = Image.open(fn_in)
        np_in2 = np.array(im_in)
        np_scaled = (np_in2 - mins) * cal_scalar
        # If it clipped, squish to good values
        np_scaled = np.minimum(np_scaled, u16_maxs)
        np_scaled = np.maximum(np_scaled, u16_mins)
        imc = Image.fromarray(np_scaled).convert("I")
        imc.save(os.path.join(args.dout, os.path.basename(fn_in)))
