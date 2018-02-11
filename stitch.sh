#!/usr/bin/env bash

# FIXME
# Switch rows

# Organize scan products
mkdir bin png
mv *.bin bin/
mv *.png png/

# For feature detection
gxs700-mask -g png png_maskg

# Normal map
gxs700-mask png png_maska
# Histogram equalize map
gxs700-decode -e bin pnge
gxs700-mask pnge pnge_maska

# Link up projects 
# (we can do this before they exist)
ln -s $PWD/png_maskg/out.pto png_maska/out.pto
ln -s $PWD/png_maskg/out.pto pnge_maska/out.pto

pushd png_maskg
stitch "$@"
popd



