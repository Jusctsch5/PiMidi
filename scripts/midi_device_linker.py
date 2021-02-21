#!/usr/bin/python3

import subprocess, signal
import os
import time
import re
import logging

well_known_midi_devices = ['System', 'Midi Through']
fs_device = 'FLUID Synth'
log_file = "/home/pi/PiMidi/logs/midi-linker.log"

class MidiInDevice:
    def __init__(self, name, port):
        self._name = name
        self._port = port

class MidiOutDevice:
    def __init__(self, name, port):
        self._name = name
        self._port = port
   
# Stop any other of these scripts running. Need to know this process and not close it :|
def stop_other_listener():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    resulting_string = out.decode('utf-8')
    for line in resulting_string.splitlines():
        if __file__ in line:
            pid = int(line.split(None, 1)[0])
            print("Killing listener with pid:" + str(pid))
            os.kill(pid, signal.SIGKILL)

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
            logging.debug(port + " " + matched_string)

    if len(midi_out_device) is 0:
        print("Unable to find output midi device (i.e. Fluidsynth)")
        logging.debug("Unable to find output midi device (i.e. Fluidsynth)")
        return False

    if len(midi_in_devices) is 0:
        print("Unable to find in midi device (i.e. Q49)")
        logging.debug("Unable to find output midi device (i.e. Q49)")
        return False

    # Need to identify already linked devices and don't relink them...
    # but maybe this isn't a problem for now

    for midi_in_device in midi_in_devices:
        connect_devices(midi_in_device, midi_out_device[0])

    return True

def connect_devices(in_dev, out_dev):
    aconnect_cmd =  "aconnect " + str(in_dev) + " " + str(out_dev)
    print("Running Cmd:" + aconnect_cmd)
    logging.debug("Running Cmd:" + aconnect_cmd)
    subprocess.run(aconnect_cmd, shell=True)
    return True

#-------------------------
# Script Starts Here
#-------------------------
logging.basicConfig(filename=log_file, 
                    format='%(asctime)s %(message)s', 
                    level=logging.DEBUG)

with open(log_file, 'w'):
    pass

print("Starting new listener for midi input devices " + __file__)
logging.debug("Starting new listener for midi input devices " + __file__)
connected_devices = False
while connected_devices is False:
    connected_devices = look_for_devices()
    
    if connected_devices == True:
        logging.debug('Connected Device:' + str(connected_devices))
        print('Connected Device:' + str(connected_devices))
        #break       
    time.sleep(5)
    connected_devices = False

