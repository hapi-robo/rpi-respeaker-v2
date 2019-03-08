#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Direction of arrival

Uses the ReSpeaker Mic Array v2.0 and returns the direction of arrival

Usage:
    $ python template.py

References:
    http://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/
    https://github.com/respeaker/usb_4_mic_array.git

"""

import sys
sys.path.insert(0, 'usb_4_mic_array')

from tuning import Tuning
import usb.core
import usb.util
import time


if __name__ == '__main__':
    # find microphone array device
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    print("Device: {}".format(dev))

    # if the device exists
    if dev:
        mic = Tuning(dev)
        while True:
            try:
                print("DOA: {}".format(mic.direction)) # direction of arrival
                print("VAD: {}".format(mic.is_voice())) # voice activity detection
                time.sleep(1)
            except KeyboardInterrupt:
                break

    # if device does not exist
    else:
        print("ReSpeaker Mic Array v2.0 device not found")

