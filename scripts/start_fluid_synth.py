#!/usr/bin/python3

import subprocess, signal
import os
import time
import logging

# Determine options. TODO Look for cookie files and override defaults if they exist
# default soundfonts can be found here /usr/share/soundfonts/FluidR3_GM.sf2
default_options="--server -i -a alsa -m alsa_seq -r 48000 -z 960 -c 1 -v -g 8"
default_instrument = "/home/pi/PiMidi/sf2/general_midi/FluidR3_GM.sf2"
log_file = "/home/pi/PiMidi/logs/start_fluid_synth.log"

def kill_running_fluidsynth():
    # Kill any running fluidsynth proceses
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    resulting_string = out.decode('utf-8')
    for line in resulting_string.splitlines():
        if 'fluidsynth' in line:
            pid = int(line.split(None, 1)[0])
            print("Killing old fluidsynth process with pid:" + str(pid))
            logging.debug("Killing old fluidsynth process with pid:" + str(pid))
            os.kill(pid, signal.SIGKILL)

def run_fluidsynth():
    # Run fluidsynth
    # fluidsynth_cmd = "fluidsynth " + default_options + " " + default_instrument + " &"
    fluidsynth_cmd = "fluidsynth " + default_options + " " + default_instrument
    print("Running cmd:" + fluidsynth_cmd)
    logging.debug("Running cmd:" + fluidsynth_cmd)
    subprocess.run(fluidsynth_cmd, shell=True)

#--------------------
# Main Script
#--------------------

logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)
with open(log_file, 'w'):
   pass

# Remove all connections 
subprocess.call("aconnect -x", shell=True)

# Kill fluidsynth if running
kill_running_fluidsynth()

# Run Fluidsynth
run_fluidsynth()

