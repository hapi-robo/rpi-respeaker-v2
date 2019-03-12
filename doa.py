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

import usb.core
import usb.util
import time
import json
import paho.mqtt.client as mqtt

from tuning import Tuning


CLIENT_ID = 'mic-array-publisher'

# MQTT broker parameters
MQTT_BROKER_IP = "raytrek.local"
MQTT_BROKER_PORT = 1883

# microphone array parameters
DOA_DELTA_THRESHOLD = 20


def mqtt_init():
    """Setup and start MQTT client.

    """
    # create a new client instance
    client = mqtt.Client(client_id = CLIENT_ID)

    # connect to a broker
    client.connect(
        host = MQTT_BROKER_IP,
        port = MQTT_BROKER_PORT,
        keepalive = 60,
        bind_address = "")

    return client


if __name__ == '__main__':
    # connect to MQTT broker
    client = mqtt_init()

    # find microphone array device
    dev = usb.core.find(idVendor = 0x2886, idProduct = 0x0018)
    print("Device: {}".format(dev))

    # if the device exists
    if dev:
        last_doa = 0
        mic = Tuning(dev)

        while True:
            try:
                time.sleep(0.5)

                # transform coordinate frame
                doa = mic.direction            
                if abs(doa - last_doa) > DOA_DELTA_THRESHOLD:
                    print("DOA: {} | Last DOA: {}".format(doa, last_doa))
                    last_doa = doa

                    # adjust coordinate frame
                    if doa > 180: doa = doa - 360

                    # publish data
                    data = {'angle':doa}
                    client.publish('robot/servo/pan', json.dumps(data))
                    
                    # print to console
                    print("DOA: {}°".format(doa)) # direction of arrival
                    # print("VAD: {}".format(mic.is_voice())) # voice activity detection

            except KeyboardInterrupt:
                break

    # if the device does not exist
    else:
        print("ReSpeaker Mic Array v2.0 device not found")

