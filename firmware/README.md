# Introduction

This directory contains the firmware for the Gendex GXS-700 dental x-ray
sensor, and the associated udev scripts.

In order to use these, you will need to have the `fxload` tool installed. To
install this on Ubuntu Linux, you would use something like:

```
apt-get install fxload
```

which will install the fxload binary as `/sbin/fxload`.

# Installation

1. Copy the `*.ihx` files in to `/lib/firmware`.
2. Copy `99-gendex.rules` in to `/etc/udev/rules.d`
3. Run `udevadm control -R` (or similar), to reload the udev rules
4. Plug in your Gendex GXS-700

And you're done!

