# ReSpeaker Mic Array v2.0

## Installation
Plug in the microphone array into the USB port.

Use `lsusb` to verify that the device has been detected, for example:
```
Bus 001 Device 006: ID 046d:0a56 Logitech, Inc. 
Bus 001 Device 007: ID 2886:0018  
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```
In this case `Bus 001 Device 007: ID 2886:0018` is the microphone array.

By default, this will be read-only. To check:
```
ls -al /dev/bus/usb/001/007
```
where 001 is the `Bus` and is 007 is the `Device`.


Set the permissions to 664 while changing the ownership to `root:pi`. The root user owns the device, members of the pi group (which includes pi) have read/write access, and all other users have read-only access. To do this, add a new file `98-mic-array.rules` to `/etc/udev/rules.d/` with the following line:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="2886", ATTR{idProduct}=="0018", GROUP="pi"
```

Reload udev rules:
```
sudo udevadm control --reload-rules && udevadm trigger
```

Then re-plug the microphone array for changes to take effect.


## Usage
Prepare the appropriate Python virtual environment:
```
./setup
source venv/bin/activate
```

Run:
```
python doa.py
```


## Update Firmware
```
python dfu.py --download 6_channels_firmware.bin
python dfu.py --download 1_channel_firmware.bin
```
