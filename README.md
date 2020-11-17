Open source Gendex GXS700 / Dexis Platinum USB x-ray sensor driver


# Installation (python3)

Instructions for Ubuntu 16.04

```
sudo apt-get install -y git python3-pip python3-numpy fxload
sudo pip3 install libusb1 scipy
# Optional for WPS7 x-ray head support
# Not needed by the vast majority of users
sudo pip3 install pycurl
git clone https://github.com/JohnDMcMaster/gxs700.git
cd gxs700
sudo ./udev.sh
sudo python3 setup.py install
```

Now plug in your sensor

TODO: add info about *optional* fxload.
TLDR wanted Windows support so didn't fully move to it


# Installation (python2)

Alternatively if you have python2 you might get away with running an old release:

```
sudo pip install gxs700
```

I'll cut a new pip release after the py3 code stabalizes


# Test

See if basic communications can be established:

```
gxs700-dump-dev
```

Now take a dark frame:

```
gxs700-main --force-trig
```

You should get files in directory "out". Sample output:


```
$ gxs700-main --force-trig
Preparing capture
Init state: 1
Init state: 1
Forcing trigger
New state 2 (scan 0)
scan 0 (state 2)
New state 4 (scan 571)
scan 1000 (state 4)
scan 2000 (state 4)
scan 3000 (state 4)
scan 4000 (state 4)
New state 8 (scan 4628)
Ready (state 8)
Transfer frame in 1.4 sec
Frame captured in 4.1 sec
Decoding image...
Writing out/2020-10-10_08/cap_00.png...
Saving meta...
Reading out/2020-10-10_08 w/ 1 images
Processing out/2020-10-10_08
Avg min: 0, max: 6416
WARNING: default calibration dir cal/130631221 does not exist
Invert min: 59119, max: 65535
Save out/2020-10-10_08.png
Eq mode (GXS700_EQ_MODE) 0
Save out/2020-10-10_08_e.png
Eq min: 1, max: 65535
done
```

If you have a working x-ray source, run the following and then light it up with x-rays:

```
gxs700-main
```

Assuming your x-ray source is intense enough, it should trigger a capture.

# See also

Hardware info here: https://nucwiki.org/wiki/index.php/Gendex_GXS700

There is some more software info here: https://nucwiki.org/wiki/index.php/GXS700_FOSS

Although its a bit out of date

