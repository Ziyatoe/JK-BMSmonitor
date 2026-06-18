"""
Read/write Data from/to JK_PBxA16S10P and many other newer JK BMS over rs485 on on a pi4 and publish on a MQTT Server

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>

NO COMMERCIAL USE !!

Copyright 2025 Z.TOe toedci@gmail.com
------------------------------------------------------------------------------------------------------------------------
If you do any modification to this python script please SHARE with me, thank you!!!!
------------------------------------------------------------------------------------------------------------------------
"""


Settings:

PUB_INTERVAL = 40.0   # sec. publish mqtt

SETTINGS_INTERVAL = 360 #sec. interval reading settings

CELL_INTERVAL = 60 #sec. interval reading cells 

mqttClient.connect("localhost", 1883, 60) #mqtt host

run:

python jkmonitor4.py 0    (no output)

python jkmonitor4.py 1    (console output)


