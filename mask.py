#!/usr/bin/env python
'''
Relevant modes
I (32-bit signed integer pixels)
    includes 16 bit grayscale
LA (L with alpha)
Unfortunately IA isn't a mode
For most of these applications we are stitching to maps which are "best effort" for online viewing
High precision applications will continue to work on raw data
TODO: look into options for combining layers to form tiffs etc

Known issues:
-cpfind
    LA: no
    RGBA: yes
-Hugin
    LA: ?
    RGBA: no
-nona, enblend
    RBGA: yes

Generate as simple .jpgs with gray during .pto creation
Then before actual stitching switch to RBGA or LA
'''
import argparse
import os
from PIL import Image, ImageDraw
#import ImageDraw
import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mask 16 bit grayscale into 8 bit grayscale with alpha')
    parser.add_argument('--overwrite', action='store_true', help='')
    parser.add_argument('--gray', '-g', action='store_true', help='Whiten (noise?) unused instead of alpha')
    parser.add_argument('--jpg', '-j', action='store_true', help='force jpg output')
    parser.add_argument('dir_in', help='')
    parser.add_argument('dir_out', nargs='?', help='')
    args = parser.parse_args()
    
    #mask = Image.open('mask.png').convert('L')
    
    if not args.dir_out:
        if os.path.basename(args.dir_in):
            dir_out = os.path.dirname(args.dir_in) + '/' + os.path.basename(args.dir_in) + '_mask'
        else:
            dir_out = os.path.dirname(args.dir_in) + '_mask'
    else:
        dir_out = args.dir_out
    print dir_out

    if os.path.exists(dir_out):
        if not args.overwrite:
            raise Exception("Refusing to overwrite output")
    else:
        os.mkdir(dir_out)
    
    def im_i2l(im):
        # lame
        return im.point([i/256 for i in xrange(0x10000)],'L')

    for fn in glob.glob(os.path.join(args.dir_in, '*.png')):
        print
        #print
        #print 'orig'
        print fn
        imi = Image.open(fn)
        #print imi.mode
        #print [imi.getpixel((i, i)) for i in xrange(0, 600, 50)]
        
        # IA is not supported
        # truncate to L so we can make LA
        #print
        #print 'L'
        iml = im_i2l(imi)
        #print iml.mode
        #print [iml.getpixel((i, i)) for i in xrange(0, 600, 50)]
        
        #print
        #print 'LA'
        mask = Image.new('L', imi.size, color=0)
        draw = ImageDraw.Draw(mask)
        #draw.rectangle((50,80,100,200), fill=0)
        # opened in image editor to get approx coords
        '''
        Original sensor?
        '''
        polym = {
                        0:(285, 10),            1:(1570, 10),
                 7: (5, 280),                           2: (1845, 240),
                 6: (5, 1060),                          3: (1845, 1100),
                        5: (285, 1335),        4: (1570, 1335),
                    }

        '''
        Newer sensor
        '''
        polym = {
                        0:(300, 13),            1:(1417, 13),
                 7: (10, 300),                           2: (1693, 244),
                 6: (10, 1045),                          3: (1693, 1100),
                        5: (300, 1330),        4: (1408, 1330),
                    }

        draw.polygon(polym.values(), fill=255)
        if args.gray:
            print 'MASK: gray'
            imr = Image.new('RGB', imi.size, color=(128, 128, 128))
            imr.paste(iml, mask=mask)
            imo = imr
        else:
            print 'MASK: alpha'
            iml.putalpha(mask)
            #print iml.mode
            #print [iml.getpixel((i, i)) for i in xrange(0, 600, 50)]
            imo = iml
        
        fn_out = os.path.join(dir_out, os.path.basename(fn))
        if args.jpg:
            imo.save(fn_out.replace('.png', '.jpg'), quality=90)
        else:
            imo.save(fn_out)
