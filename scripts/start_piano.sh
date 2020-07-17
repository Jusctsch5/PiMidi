#!/bin/bash

(STOP=$((SECONDS+5))
until [[ $SECONDS -ge $STOP || $(ps -C fluidsynth -o stat=) =~ S ]]; do:; done && aconnect 20:0 128:0 &)
fluidsynth -a alsa -r 48000 -z 480 -c 1 -v -g 6 /usr/share/sounds/sf2/FluidR3_GM.sf2


