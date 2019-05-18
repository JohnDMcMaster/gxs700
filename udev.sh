#!/usr/bin/env bash

# For some reason I had to actually kill udev to get rules to take effect
# /etc/init.d/udev stop
# /etc/init.d/udev start
# did not do it automatically, did not work either:
# sudo udevadm control --reload-rules

file=/etc/udev/rules.d/99-gxs700.rules
echo "Updating $file"

# Note old udev rules were like 
# ACTION=="add", SUBSYSTEM=="usb_device", SYSFS{idVendor}=="5328", SYSFS{idProduct}=="2009", MODE="0666"
# Had both originally, decided to remove legacy support to ease troubleshooting

cat << EOF |sudo tee $file >/dev/null
# Dexis Platinum
# Pre renumeration
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="5328", ATTR{idProduct}=="2009", MODE="0666"
# Post enumeration
# In theory...although I guess I'm loading the same (wrong?) FW for both
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="5328", ATTR{idProduct}=="2010", MODE="0666"

# Gendex GX700 (large)
# Pre renumeration
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="5328", ATTR{idProduct}=="202f", MODE="0666"
# Post renumeration
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="5328", ATTR{idProduct}=="2030", MODE="0666"

# Gendex GX700 (small)
# Pre renumeration
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="5328", ATTR{idProduct}=="201f", MODE="0666"
# Post renumeration
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="5328", ATTR{idProduct}=="2020", MODE="0666"
EOF

