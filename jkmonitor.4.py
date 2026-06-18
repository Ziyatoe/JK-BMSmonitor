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
import serial
import struct
from registers_1_3 import *
from colors import *
import paho.mqtt.client as mqtt
import json
import time
import sys
import errno

VERSION = "4"

OUTPUT = True

last_pub = {}
PUB_INTERVAL = 40.0   # Sekunden
last_settings_pub = {}
last_cell_pub = {}
SETTINGS_INTERVAL = 360
CELL_INTERVAL = 60
myserial = serial.Serial()
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

buf = bytearray()
mbadr = None 
current_bms = None

def crc8(d):
    #---------------------------------------------------------------------------------
    return sum(d) & 0xff

def modbus_crc(data):
    #---------------------------------------------------------------------------------
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H',crc)
    #---------------------------------------------------------------------------------

def select_bms(bms):
    #---------------------------------------------------------------------------------
    frame = bytearray([
        0x01,       # master address
        0x10,       # write registers
        0x16,0x20,  # register 0x1620
        0x00,0x01,  # count
        0x02,       # byte count
        0x00,bms
    ])
    frame += modbus_crc(frame)
    myserial.write(frame)
    #---------------------------------------------------------------------------------

def request_device_info():
    #---------------------------------------------------------------------------------
    cmd = bytearray(20)
    cmd[0:4] = b'\xAA\x55\x90\xEB'
    cmd[4] = 0x97     # device info
    cmd[5] = 0x00     # length

    # value = 0
    cmd[6:10] = b'\x00\x00\x00\x00'
    # padding bleibt 0 (10..18)
    cmd[19] = sum(cmd[:19]) & 0xFF
    myserial.write(cmd)
    #---------------------------------------------------------------------------------

def request_device_info_bms(bms):
    #---------------------------------------------------------------------------------
    select_bms(bms)
    time.sleep(0.05)
    request_device_info()
    #---------------------------------------------------------------------------------

def parse_settings(frame):
    #---------------------------------------------------------------------------------
    global mbadr
    frame_type = frame[4]
    if frame_type != 0x01:
        if OUTPUT: print(f"wrong frame for settings {hex(frame_type)}")
        return None
    payload = frame[6:]
    res = {}
    for off,name,fmt,coef,unit,word,hatopic in JKDeviceSettingsRegs:
        if word == 'hi':
            v = payload[off+1]
        elif word == 'lo':
            v = payload[off]
        else:
            if fmt == 'I':
                v = struct.unpack_from('<I',payload,off)[0]
            elif fmt == 'i':
                v = struct.unpack_from('<i',payload,off)[0]
            elif fmt == 'H':
                v = struct.unpack_from('<H',payload,off)[0]
            elif fmt == 'B':
                v = payload[off]
            else:
                continue
        v = v * coef
        # if off == 0x0114:
        #     bits = int(v)
        #     for i,bitname in enumerate(sys_config_bits):
        #         if bitname.startswith("*"):
        #             bitname = bitname[1:]
                  
        #             res[f"switch/{bitname}"] = (bits >> i) & 1
        #     continue
        res[name] = v
    mbadr = res.get("DevAddr","?")
   
    return res
    #---------------------------------------------------------------------------------

def parse_cell_info(frame):
    #---------------------------------------------------------------------------------
    if frame[0:4] != b'\x55\xaa\xeb\x90':
        return None

    frame_type = frame[4]

    if frame_type != 0x02:
        if OUTPUT: print(f"wrong frame for cells {hex(frame_type)}")
        return None
#    else:
#        if OUTPUT: print(f"frame for cells {hex(frame_type)}")

    payload = frame[6:]
    res = {}

    for off,name,fmt,coef,unit,word,hatopic in JKCellInfoRegisters:
        if word == 'hi':
            v = payload[off+1]
        elif word == 'lo':
            v = payload[off]
        else:
            if fmt == 'I':
                v = struct.unpack_from('<I',payload,off)[0]
            elif fmt == 'i':
                v = struct.unpack_from('<i',payload,off)[0]
            elif fmt == 'H':
                v = struct.unpack_from('<H',payload,off)[0]
            elif fmt == 'h':
                v = struct.unpack_from('<h',payload,off)[0]
            elif fmt == 'B':
                v = payload[off]
            elif fmt == 'f':
                v = struct.unpack_from('<f',payload,off)[0]
            else:
                continue
        res[name] = v * coef

    return res
    #---------------------------------------------------------------------------------

def parse_device_info(frame):
    #-------------------------------------------------------------------------------
    if frame[0:4] != b'\x55\xaa\xeb\x90':
        return None

    frame_type = frame[4]

    if frame_type != 0x03:
        if OUTPUT: print(f"wrong frame for device info {hex(frame_type)}")
        return None
#    else:
#        if OUTPUT: print(f"frame for device info {hex(frame_type)}")

    payload = frame[6:]
    res = {}

    for off,name,fmt,coef,unit,word,hatopic in JKDeviceInfoRegisters:
        if word == 'hi':
            v = payload[off+1]
        elif word == 'lo':
            v = payload[off]
        else:
            if fmt == 'I':
                v = struct.unpack_from('<I',payload,off)[0]
            elif fmt == 'i':
                v = struct.unpack_from('<i',payload,off)[0]
            elif fmt == 'H':
                v = struct.unpack_from('<H',payload,off)[0]
            elif fmt == 'h':
                v = struct.unpack_from('<h',payload,off)[0]
            elif fmt == 'B':
                v = payload[off]
            elif fmt == '16s':
                v = struct.unpack_from('<16s',payload,off)[0].split(b'\x00')[0].decode(errors="ignore")
            elif fmt == '8s':
                v = struct.unpack_from('<8s',payload,off)[0].split(b'\x00')[0].decode(errors="ignore")
            else:
                continue

        if isinstance(v,(int,float)):
            v = v * coef
        res[name] = v

    return res
    #--------------------------------------------------------------

def publish_register(bms_name,regs,regmap):
    #--------------------------------------------------------------

    base = bms_name.replace("-","_")
    data = {}
    for off,name,fmt,coef,unit,word,hatopic in regmap:
        if hatopic is None:
            continue

        v = regs.get(name)
        if v is None:
            continue
        if regmap is JKDeviceSettingsRegs:
            if off == 0x0114:
                bits = int(v)
                for i,bitname in enumerate(sys_config_bits):
                    if bitname.startswith("*"):
                        bitname = bitname[1:]
                    
                        data[f"switch/{bitname}"] = (bits >> i) & 1
                continue

        data[hatopic] = v
    try:
        mqttClient.publish(f"{base}/block", json.dumps(data), retain=False)
        #print(json.dumps(data))
    except Exception:
        if OUTPUT: print (RED,"MQTT: error publish register",RESET)
        return False
    #--------------------------------------------------------------

def connectMqtt():
    #--------------------------------------------------------------
    global mqttClient
    try:    
        mqttClient.connect("localhost", 1883, 60)
        mqttClient.loop_start()
        return mqttClient
    except Exception:
        if OUTPUT: print (RED,"MQTT: error connecting",RESET)
        return False
    #--------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: jkrs485.py OUTPUT=0/1")
        sys.exit(1)

    if sys.argv[1] not in ("0", "1"):
        print("usage: jkrs485.py OUTPUT=0/1")
        sys.exit(1)

    OUTPUT = sys.argv[1] == "1"
    
    
    try:
        myserial = serial.Serial("/dev/ttyUSB0",115200,timeout=1)
    except Exception:
        if OUTPUT: print (RED,"SERIAL: error connecting",RESET)
        sys.exit(1)

    
    
    while not connectMqtt(): 
        if OUTPUT: print("Can't connect mqtt")
        time.sleep(5)

    time.sleep(2)  # Bus kurz stabilisieren

    for bms in range(len(DEVICE_NAMES)):
        #request_device_info_bms(bms)
        request_device_info()  #doesnt work really
        time.sleep(0.3)

    while True:
        try:
            d = myserial.read(512)
            if not d:
                continue
        except Exception:
            if OUTPUT: print("Can't read serial!")
            continue

        buf += d

        while True:
            p = buf.find(b'\x55\xaa\xeb\x90')
            if p < 0:
                if len(buf) > 1000:
                    buf = buf[-100:]
                break

            if len(buf) < p + 300:
                break
            frame = buf[p:p+300]
            buf = buf[p+300:]
            crc = frame[299]

            if crc != crc8(frame[:-1]):
                if OUTPUT: print("CRC_FAIL", frame[:8].hex())
                continue

            t = frame[4]
                                                                                                                                                                                               
            if t == 0x01:
                s = parse_settings(frame)

                if s and mbadr is not None:
                    current_bms = mbadr

                if current_bms is None or current_bms >= len(DEVICE_NAMES):
                    if OUTPUT: print(f"unknown bms addr {current_bms}, skipping")
                    continue

                if OUTPUT: print("--BEGIN BLOCK---------------------------------------------------------")

                bmsname = DEVICE_NAMES[current_bms]

                if OUTPUT: print(mbadr,bmsname, " -- SETTINGS")
                if OUTPUT: print(str(s)[:70])

                now = time.time()

                if now - last_settings_pub.get(current_bms,0) > SETTINGS_INTERVAL:
                    publish_register(bmsname, s, JKDeviceSettingsRegs)
                    if OUTPUT: print(now,YELLOW, bmsname,"PUBLISH SETTINGS",RESET)
                    last_settings_pub[current_bms] = now

            elif t == 0x02 and current_bms is not None and current_bms < len(DEVICE_NAMES):
                c = parse_cell_info(frame)
                bmsname = DEVICE_NAMES[current_bms]

                if OUTPUT: print(bmsname," -- CELL INFO")
                if OUTPUT: print(str(c)[:70])

                now = time.time()

                if now - last_cell_pub.get(current_bms,0) > CELL_INTERVAL:
                    publish_register(bmsname,c,JKCellInfoRegisters)
                    if OUTPUT: print(now, GREEN,bmsname,"PUBLISH CELL INFO",RESET)
                    last_cell_pub[current_bms] = now
                if OUTPUT: print("--END BLOCK-----------------------------------------------------------")
            
            elif t == 0x03 and current_bms is not None and current_bms < len(DEVICE_NAMES):
                dev = parse_device_info(frame)
                bmsname = DEVICE_NAMES[current_bms]
                if OUTPUT: print(bmsname," -- DEVICE INFO")
                if OUTPUT: print(str(dev)[:70])
                publish_register(bmsname,dev,JKDeviceInfoRegisters)
