from __future__ import print_function
import numpy as np
from PIL import Image
import glob
import os

def parse_roi(s):
    if s is None:
        return None
    return [int(x) for x in s.split(',')]


def npf2im(statef, width, height):
    #return statef, None
    rounded = np.round(statef)
    #print("row1: %s" % rounded[1])
    statei = np.array(rounded, dtype=np.uint16)
    #print(len(statei), len(statei[0]), len(statei[0]))

    # for some reason I isn't working correctly
    # only L
    #im = Image.fromarray(statei, mode="I")
    #im = Image.fromarray(statei, mode="L")
    # workaround by plotting manually
    im = Image.new("I", (height, width), "Black")
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

    statef = np.zeros((height, width), np.float)
    for im in imgs:
        assert (width, height) == im.size
        statef = statef + scalar * np.array(im, dtype=np.float)

    return statef, npf2im(statef, width, height)

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
