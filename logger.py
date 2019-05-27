#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ReSpeaker Mic Array v2.0

Collects data from ReSpeaker Mic Array v2.0

Usage:
    $ python mic.py

References:
    http://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/
    https://github.com/respeaker/usb_4_mic_array.git

"""

import sys
sys.path.insert(0, 'usb_4_mic_array')

import usb.core
import usb.util
import time
import csv

from datetime import datetime
from tuning import Tuning


def main():
    # find microphone array device
    dev = usb.core.find(idVendor = 0x2886, idProduct = 0x0018)
    # print("Device: {}".format(dev))

    # if the device exists
    if dev:
        last_doa = 0
        mic = Tuning(dev)

        file_ts = datetime.today().strftime("%Y%m%d%H%M%S")

        with open("log_" + file_ts + ".csv", "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Timestamp", "VAD", "DOA"])

            while True:
                ts = time.time()
                vad = mic.is_voice()
                doa = mic.direction

                # print to console
                print("[{:.2f}] VAD: {} DOA: {}°".format(ts, vad, doa)) 

                # write to csv
                csvwriter.writerow([[ts, vad, doa]])
    
                # wait
                time.sleep(0.5)
                

    # if the device does not exist
    else:
        print("ReSpeaker Mic Array v2.0 device not found")
        return


if __name__ == '__main__':
    try:
        main()        

    except KeyboardInterrupt:
        pass
