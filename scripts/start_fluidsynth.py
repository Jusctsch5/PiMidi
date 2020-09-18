#!/usr/bin/python

import subprocess, signal
import os
import time

# Remove all connections 
subprocess.call("aconnect -x", shell=True)

# Kill any running fluidsynth proceses
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
for line in out.splitlines():
   if 'fluid' in line:
      print("Killing old fluidsynth process...")
      pid = int(line.split(None, 1)[0])
      os.kill(pid, signal.SIGKILL)

# Determine options. TODO Look for cookie files and override defaults if they exist
# default soundfonts can be found here/usr/share/soundfonts/FluidR3_GM.sf2
default_options="--server -i -a alsa -m alsa_seq -r 48000 -z 960 -c 1 -v -g 8"
default_instrument = "../sf2/general_midi/FluidR3_GM.sf2"

# subprocess.call("cp ../fluidsynth_config/" + conf_file + " /etc/conf.d/fluidsynth", shell=True)

# Run fluidsynth
fluidsynth_cmd = "fluidsynth " + default_options + " " + default_instrument + " &"
print("Running cmd:" + fluidsynth_cmd)
subprocess.call(fluidsynth_cmd, shell=True)
time.sleep(5)

