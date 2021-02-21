#!/bin/bash
cp midi-linker.service /lib/systemd/system/
cp start-fluid-synth.service /lib/systemd/system/
systemctl daemon-reload

systemctl enable midi-linker.service
systemctl enable start-fluid-synth.service

systemctl show start-fluid-synth.service
systemctl show midi-linker.service 

#/etc/systemd/system/multi-user.target.wants/
