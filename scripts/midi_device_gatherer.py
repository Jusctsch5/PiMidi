#!/usr/bin/python

import subprocess, signal
import os
import time
import re


class MidiInDevice:
    def __init__(self, name, port):
        self._name = name
        self._port = port

class MidiOutDevice:
    def __init__(self, name, port):
        self._name = name
        self._port = port
   
well_known_midi_devices = ['System', 'Midi Through']
fs_device = 'FLUID Synth'


# Remove all connections 
def look_for_devices():
    result = subprocess.run(['aconnect', '-l'], stdout=subprocess.PIPE)
    midi_in_devices = []
    midi_out_device = []

    resulting_string = result.stdout.decode('utf-8')
    for line in resulting_string.splitlines():
        if 'client' in line:
            split_string = line.split()
    
            port = split_string[1][:-1]
            name = split_string[2][1:-1]
            matched = re.search("\'.*?\'", line)
            matched_string = matched.group(0)[1:-1] 
            if matched_string in well_known_midi_devices:
                continue
            if fs_device in matched_string:
                midi_out_device.append(port)
            else:
                midi_in_devices.append(port)
               

            print(port + " " + matched_string)

    for midi_in_device in midi_in_devices:
        aconnect_cmd =  "aconnect " + str(midi_in_device) + " " + str(midi_out_device[0]) 
        print("Running Cmd:" + aconnect_cmd)
        subprocess.run(aconnect_cmd, shell=True)

while 1:
    look_for_devices()
    time.sleep(240)
