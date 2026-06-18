# Version
REGISTER_VERSION = "1.3"

#JK-JK_PB1A16S10P Registers  (JK Modbus V1.1)
  # Data Type	Size (Bytes)	Unsigned Format	        Signed Format
    # UINT32	4 bytes	        'I' (unsigned int)	    'i' (signed int)
    # UINT16	2 bytes	        'H' (unsigned short)	'h' (signed short)
    # UINT8	    1 byte	        'B' (unsigned char)	    'b' (signed char)
    #ASCIIstr   1/2             '16s','8s'
    # UINT8[16] 16              '16B'

JKDeviceSettingsBase = 0x1000
JKCellInfoBase = 0x1200 
JKDeviceInfoBase = 0x1400

CMD_TYPE_DEVICE_INFO = 0x97  # 0x03: Device Information
MSG_TYPE_DEVICE_INFO = 0x03

CMD_TYPE_CELL_INFO = 0x96  # 0x02: Cell Information
MSG_TYPE_CELL_INFO = 0x02

CMD_TYPE_SETTINGS = 0x95  # 0x01: Settings
MSG_TYPE_SETTING = 0x01



MSG_TYPE_NAME = {
    MSG_TYPE_SETTING: "MSG_TYPE_SETTING",
    MSG_TYPE_CELL_INFO: "MSG_TYPE_CELL_INFO",
    MSG_TYPE_DEVICE_INFO: "MSG_TYPE_DEVICE_INFO",
}

# BLE things------------------------------------------------------------------------------------------------------------
DEVICE_NAMES = ["191120256043-00","011220256041-01", "191120256053-02"]
# [NEW] Device A4:C1:38:01:6A:08 191120256053-02
# [NEW] Device A4:C1:38:01:22:A4 191120256043-00
# [NEW] Device A4:C1:38:01:39:70 011220256041-01

DEVICE_NAMES_LAST = [] #Keep track of which devices have been processed in the current run
#SERVICE_UUID = "ffe0"
SERVICE_UUID = "0000FFE0-0000-1000-8000-00805f9b34fb"
#CHAR_UUID = "ffe1"
CHAR_UUID = "0000FFE1-0000-1000-8000-00805f9b34fb"
CMD_HEADER = bytes([0xAA, 0x55, 0x90, 0xEB])

#--------------------------------------------------------------------------------------------------------------------------
# split-word registers should be defined with one active register and one  more registers at the same address
#--------------------------------------------------------------------------------------------------------------------------

JKDeviceSettingsRegs = [  # 0x1000   ##################################################################33
#  (position, JKname,                format, coeff,    unit, word=none/packed=hi/lo,    HAname)
    (0x0000, 'SmartSleepV',            'I', 0.001,     'V',        None,'bms/settingRW/SmartSleepV'),  
    (0x0004, 'UnderVProt',             'I', 0.001,     'V',        None,'bms/settingRW/CellUVprot'),  
    (0x0008, 'UVProtRecover',       'I', 0.001,     'V',        None,'bms/settingRW/CellUVProtRecovr'),  
    (0x000C, 'OverVProt',             'I', 0.001,     'V',        None,'bms/settingRW/CellOVprot'),  
    (0x0010, 'OVProtRecover',       'I', 0.001,     'V',        None,'bms/settingRW/CellOVProtRecovr'),  
    (0x0014, 'BalanTrigV',             'I', 0.001,     'V',        None,'bms/settingRW/BalanTrigV'),  
    (0x0018, 'SOC100_V',               'I', 0.001,     'V',        None,'bms/settingRW/SOC100_V'),  
    (0x001C, 'SOC0_V',                 'I', 0.001,     'V',        None,'bms/settingRW/SOC0_V'),  
    (0x0020, 'RecomendChgV',            'I', 0.001,     'V',        None,'bms/settingRW/CellRecChgV'),  
    (0x0024, 'RecomendFloatV',          'I', 0.001,     'V',        None,'bms/settingRW/CellRecFloatV'),  
    (0x0028, 'SysPwrOffV',             'I', 0.001,     'V',        None,'bms/settingRW/SysPwrOffV'),  
    (0x002C, 'COntChgCur',             'I', 0.001,     'A',        None,'bms/settingRW/COntChgCur'),  
    (0x0030, 'TIMBatCOCPDly',         'I', 1.0,       's',        None,'bms/settingRW/OvrcurChgProtDlyT'),  
    (0x0034, 'TIMBatCOCPRDly',        'I', 1.0,       's',        None,'bms/settingRW/OvrcurChgProtRelT'),  
    (0x0038, 'ContDchgCur',            'I', 0.001,     'A',        None,'bms/settingRW/ContDchgCur'),  
    (0x003C, 'TIMBatDcOCPDly',        'I', 1.0,       's',        None,'bms/settingRW/OvrcurDChgProtDlyT'),  
    (0x0040, 'TIMBatDcOCPRDly',       'I', 1.0,       's',        None,'bms/settingRW/OvrcurDChgProtRelT'),  
    (0x0044, 'SCPRDlyTime',         'I', 1.0,       's',        None,'bms/settingRW/ShortCircuitProtRelR'),  
    (0x0048, 'BalanceMax_I',             'I', 0.001,     'A',        None,'bms/settingRW/BalanMax_I'),  
    (0x004C, 'COTTemp',             'i', 0.1,       'C',        None,'bms/settingRW/BatCOTTemp'),  
    (0x0050, 'COTPRTemp',           'i', 0.1,       'C',        None,'bms/settingRW/BatCOTPRTemp'),  
    (0x0054, 'DcOTTemp',            'i', 0.1,       'C',        None,'bms/settingRW/BatDcOTTemp'),  
    (0x0058, 'DcOTPRTemp',          'i', 0.1,       'C',        None,'bms/settingRW/BatDcOTPRTemp'),  
    (0x005C, 'CUTTemp',             'i', 0.1,       'C',        None,'bms/settingRW/BatCUTTemp'),  
    (0x0060, 'CUTPRTemp',           'i', 0.1,       'C',        None,'bms/settingRW/BatCUTPRTemp'),  
    (0x0064, 'MosOTTemp',              'i', 0.1,       'C',        None,'bms/settingRW/MosOTTemp'),  
    (0x0068, 'MosOTPRTemp',            'i', 0.1,       'C',        None,'bms/settingRW/MosOTPRTemp'),  
    (0x006C, 'CellCount',              'I', 1,       '-',        None,'bms/settingRW/CellCount'),  
    (0x0070, 'BatChargeEN',            'I', 1,       'bool',     None,'switch/charge'),  
    (0x0074, 'BatDisChargeEN',         'I', 1,       'bool',     None,'switch/discharge'),  
    (0x0078, 'BalanEN',                'I', 1,       'bool',     None,'switch/balance'),  
    (0x007C, 'CapBatCell',             'I', 1.0,       'mAh',      None,'bms/settingRW/CapBatCell'),  
    (0x0080, 'SCPDelay',               'I', 1.0,       'us',       None,'bms/settingRW/SCPDelay'),  
    (0x0084, 'StartBalanV',            'I', 0.001,     'V',        None,'bms/settingRW/StartBalanV'),  
    # (0x0088, 'CellConWireRes0',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR0'),
    # (0x008C, 'CellConWireRes1',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR1'),
    # (0x0090, 'CellConWireRes2',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR2'),
    # (0x0094, 'CellConWireRes3',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR3'),
    # (0x0098, 'CellConWireRes4',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR4'),
    # (0x009C, 'CellConWireRes5',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR5'),
    # (0x00A0, 'CellConWireRes6',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR6'),
    # (0x00A4, 'CellConWireRes7',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR7'),
    # (0x00A8, 'CellConWireRes8',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR8'),
    # (0x00AC, 'CellConWireRes9',      'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR9'),
    # (0x00B0, 'CellConWireRes10',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR10'),
    # (0x00B4, 'CellConWireRes11',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR11'),
    # (0x00B8, 'CellConWireRes12',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR12'),
    # (0x00BC, 'CellConWireRes13',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR13'),
    # (0x00C0, 'CellConWireRes14',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR14'),
    # (0x00C4, 'CellConWireRes15',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR15'),
    # (0x00C8, 'CellConWireRes16',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR16'),
    # (0x00CC, 'CellConWireRes17',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR17'),
    # (0x00D0, 'CellConWireRes18',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR18'),
    # (0x00D4, 'CellConWireRes19',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR19'),
    # (0x00D8, 'CellConWireRes20',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR20'),
    # (0x00DC, 'CellConWireRes21',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR21'),
    # (0x00E0, 'CellConWireRes22',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR22'),
    # (0x00E4, 'CellConWireRes23',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR23'),
    # (0x00E8, 'CellConWireRes24',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR24'),
    # (0x00EC, 'CellConWireRes25',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR25'),
    # (0x00F0, 'CellConWireRes26',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR26'),
    # (0x00F4, 'CellConWireRes27',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR27'),
    # (0x00F8, 'CellConWireRes28',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR28'),
    # (0x00FC, 'CellConWireRes29',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR29'),
    # (0x0100, 'CellConWireRes30',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR30'),
    # (0x0104, 'CellConWireRes31',     'I', 1.0,       'uOhm',     None,'bms/settingRW/wireR31'),
    (0x0108, 'DevAddr',                'I', 1,         '-',        None,'bms/settingRW/DevAddr'),     
    (0x010C, 'ProdischargeTime',       'I', 1.0,       'S',        None,'bms/settingRW/ProdischargeTime'),
    (0x0114, 'SysConfigBits',          'H', 1,         'Bits',     None,'switch/SysConfigBits'),  #BIT0..BIT9: HeatEN, DisableTempSensor, GPSHeartbeat, PortSwitch, ...
    (0x0118, 'SmartSleepTime',         'H', 1.0,       'H',        'lo','bms/settingRW/SmartSleepTime'), #packed register
        (0x0118, 'DataDomainCtl',       'B', 1.0,       'H',        'hi','bms/DataDomainCtl') #packed register

]

sys_config_bits = [
    "*HeatingEnable",         #bit0 
    "*DisableTempSensor",      
    "*GPSHeartbeatEnable",     
    "*PortSwitchEnable",       
    "*LCDAlwaysOn",            
    "*SpecialCharger",         
    "*SmartSleep",             
    "*DisablePCLModule",       
    "*TimedStoredData",        
    "*float_charge",   #bit9
    "notused10",
    "notused11",
    "notused12",    
    "notused13",
    "notused14",
    "notused15",
]

JKCellInfoRegisters = [  # 0x1200
 #(position, JKname,              format,  coeff,    unit,     word=none/packed=hi,lo), HAname
    # ---------- Cells ----------
    (0x0000, 'CellV1',              'H',  0.001,        'V',    None, 'cell_voltages/1'),
    (0x0002, 'CellV2',              'H',  0.001,        'V',    None, 'cell_voltages/2'),
    (0x0004, 'CellV3',              'H',  0.001,        'V',    None, 'cell_voltages/3'),
    (0x0006, 'CellV4',              'H',  0.001,        'V',    None, 'cell_voltages/4'),
    (0x0008, 'CellV5',              'H',  0.001,        'V',    None, 'cell_voltages/5'),
    (0x000A, 'CellV6',              'H',  0.001,        'V',    None, 'cell_voltages/6'),
    (0x000C, 'CellV7',              'H',  0.001,        'V',    None, 'cell_voltages/7'),
    (0x000E, 'CellV8',              'H',  0.001,        'V',    None, 'cell_voltages/8'),
    (0x0010, 'CellV9',              'H',  0.001,        'V',    None, 'cell_voltages/9'),
    (0x0012, 'CellV10',             'H',  0.001,        'V',    None, 'cell_voltages/10'),
    (0x0014, 'CellV11',             'H',  0.001,        'V',    None, 'cell_voltages/11'),
    (0x0016, 'CellV12',             'H',  0.001,        'V',    None, 'cell_voltages/12'),
    (0x0018, 'CellV13',             'H',  0.001,        'V',    None, 'cell_voltages/13'),
    (0x001A, 'CellV14',             'H',  0.001,        'V',    None, 'cell_voltages/14'),
    (0x001C, 'CellV15',             'H',  0.001,        'V',    None, 'cell_voltages/15'),
    (0x001E, 'CellV16',             'H', 0.001,         'V',    None, 'cell_voltages/16'),
#     #(0x0022,'CellV17',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/17),
#     #(0x0024,'CellV18',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/18),
#     #(0x0026,'CellV19',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/19),
#     #(0x0028,'CellV20',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/20),
#     #(0x002A,'CellV21',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/21),
#     #(0x002C,'CellV22',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/22),
#     #(0x002E,'CellV23',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/23),
#     #(0x0030,'CellV24',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/24),
#     #(0x0032,'CellV25',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/25),
#     #(0x0034,'CellV26',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/26),
#     #(0x0036,'CellV27',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/27),
#     #(0x0038,'CellV28',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/28),
#     #(0x003A,'CellV29',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/29),
#     #(0x003C,'CellV30',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/30),
#     #(0x003E,'CellV31',                 'H', 0.001,     'V',       None, 'cell_voltages/cells/31),

    (0x0040, 'CellNrSts',           'I',  1,            '',     None, 'cell_voltages/CellNrSts'),
    (0x0044, 'CellVolAve',          'H',  0.001,        'V',    None, 'cell_voltages/average'),
    (0x0046, 'CellVdifMax',         'H',  0.001,        'V',    None, 'cell_voltages/delta'),
    (0x0048, 'MaxVolCellNr',        'H',  1,            '-',    'lo', 'cell_voltages/max_index'), #packed register
    (0x0048, 'MinVolCellNr',        'B',  1,            '-',    'hi', 'cell_voltages/min_index'), 
    
#     (0x004A, 'CellR0',                  'H', 0.001,     '?',       None,  'cell/R0),
#     (0x004C, 'CellR1',                  'H', 0.001,     '?',       None,  'cell/R1),
#     (0x004E, 'CellR2',                  'H', 0.001,     '?',       None,  'cell/R2),
#     (0x0050, 'CellR3',                  'H', 0.001,     '?',       None,  'cell/R3),
#     (0x0052, 'CellR4',                  'H', 0.001,     '?',       None,  'cell/R4),
#     (0x0054, 'CellR5',                  'H', 0.001,     '?',       None,  'cell/R5),
#     (0x0056, 'CellR6',                  'H', 0.001,     '?',       None,  'cell/R6),
#     (0x0058, 'CellR7',                  'H', 0.001,     '?',       None,  'cell/R7),
#     (0x005A, 'CellR8',                  'H', 0.001,     '?',       None,  'cell/R8),
#     (0x005C, 'CellR9',                  'H', 0.001,     '?',       None,  'cell/R9),
#     (0x005E,'CellR10',                  'H', 0.001,     '?',       None,  'cell/R10),
#     (0x0060,'CellR11',                  'H', 0.001,     '?',       None,  'cell/R11),
#     (0x0062,'CellR12',                  'H', 0.001,     '?',       None,  'cell/R12),
#     (0x0064,'CellR13',                  'H', 0.001,     '?',       None,  'cell/R13),
#     (0x0066,'CellR14',                  'H', 0.001,     '?',       None,  'cell/R14),
#     #(0x0068,'CellR15',                 'H', 0.001,     '?',       None,  'cell/R15),
#     #(0x006A,'CellR16',                 'H', 0.001,     '?',       None,  'cell/R16),
#     #(0x006C,'CellR17',                 'H', 0.001,     '?',       None,  'cell/R17),
#     #(0x006E,'CellR18',                 'H', 0.001,     '?',       None,  'cell/R18),
#     #(0x0070,'CellR19',                 'H', 0.001,     '?',       None,  'cell/R19),
#     #(0x0072,'CellR20',                 'H', 0.001,     '?',       None,  'cell/R20),
#     #(0x0074,'CellR21',                 'H', 0.001,     '?',       None,  'cell/R21),
#     #(0x0076,'CellR22',                 'H', 0.001,     '?',       None,  'cell/R22),
#     #(0x0078,'CellR23',                 'H', 0.001,     '?',       None,  'cell/R23),
#     #(0x007A,'CellR24',                 'H', 0.001,     '?',       None,  'cell/R24),
#     #(0x007C,'CellR25',                 'H', 0.001,     '?',       None,  'cell/R25),
#     #(0x007E,'CellR26',                 'H', 0.001,     '?',       None,  'cell/R26),
#     #(0x0080,'CellR27',                 'H', 0.001,     '?',       None,  'cell/R27),
#     #(0x0082,'CellR28',                 'H', 0.001,     '?',       None,  'cell/R28),
#     #(0x0084,'CellR29',                 'H', 0.001,     '?',       None,  'cell/R29),
#     #(0x0086,'CellR30',                 'H', 0.001,     '?',       None,  'cell/R30),
#     #(0x0088,'CellR31',                 'H', 0.001,     '?',       None,  'cell/R31),
   
    (0x008A, 'TempMOS',             'h',  0.1,          'C',    None, 'bms/temp/mosfet'),
    (0x008C, 'CellWireResSts',      'I',  1,            'Bits', None, 'cell_voltages/WireResSts'),

    (0x0090, 'BatV',                'I',  0.001,        'V',    None, 'soc/total_voltage'),
    (0x0098, 'BatI',                'i',  0.001,        'A',    None, 'soc/current'),
    (0x0094, 'BatP',                'I',  0.001,        'W',    None, 'soc/power'),
    (0x009C, 'TempBat1',            'h',  0.1,          'C',    None, 'bms/temp/1'),
    (0x009E, 'TempBat2',            'h',  0.1,          'C',    None, 'bms/temp/2'),

    (0x00A0, 'Alarm',               'I',  1,            'Bits', None, 'bms/Alarm'),
    (0x00A4, 'BalanceI',            'H',  0.001,        'A',    None, 'soc/balance_current'),
    (0x00A6, 'SOC',                 'B',  1,            '%',    'hi', 'soc/soc_percent'),
    (0x00A6, 'BalanceSts',          'H',  1,            '-',    'lo', 'bms/balanceSts'), #packed register
    (0x00A8, 'CapRemain',           'i',  0.001,        'mAh',  None, 'soc/remain_capacity'),
    (0x00AC, 'FullChgCap',          'I',  0.001,        'mAh',  None, 'soc/full_capacity'),

    (0x00B0, 'CycleCount',          'I',  1,            '-',    None, 'soc/cycles'),
    (0x00B4, 'CycleCap',            'I',  0.001,        'mAh',  None, 'soc/CycleCap'),
    (0x00B8, 'SOH',                 'H',  1,            '%',    'lo', 'bms/soh'),
    (0x00B8, 'Precharge',           'B',  1,            '-',    'hi', 'bms/data/precharge'), #packed register
    (0x00BA, 'UserAlarm1',          'H',  1,            '-',    None, 'bms/useralarm1'),
    (0x00BC, 'RunTime',             'I',  0.00027778,   'H',    None, 'bms/runtime'),

    (0x00C0, 'Charge',              'H',  1,            '-',    'lo', 'switch/chargeSts'),
    (0x00C0, 'Discharge',           'B',  1,            '-',    'hi', 'switch/dischargeSts'),
    (0x00C2, 'UserAlarm2',          'H',  1,            '-',    None, 'bms/data/useralarm2'),
        
    (0x00C4,'TimeDcOCPR',           'H',  1,            '-',    None, 'bms/time/TimeDcOCPR'),
    (0x00C6,'TimeDcSCPR',           'H',  1,            '-',    None, 'bms/time/TimeDcSCPR'),
    (0x00C8,'TimeCOCPR',            'H',  1,            '-',    None, 'bms/time/TimeCOCPR'),
    (0x00CA,'TimeCSCPR',            'H',  1,            '-',    None, 'bms/time/TimeCSCPR'),
    (0x00CC,'TimeUVPR',             'H',  1,            '-',    None, 'bms/time/TimeUVPR'), 
    (0x00CE,'TimeOVPR',             'H',  1,            '-',    None, 'bms/time/TimeOVPR'),
    (0x00D0,'Heating',              'B',  1,            '-',    'hi', 'bms/data/heating'),
    (0x00D0,'TempSensorAbsent',     'H',  1,            '-',    'lo', 'bms/temp/TempSensorAbsent'),  #packed register
    (0x00D8,'VolChargCur',          'H',  0.001,        'V',    None, 'bms/data/VolChargCur'),
    (0x00DA,'VolDischargCur',       'H',  0.001,        'V',    None, 'bms/data/VolDischargCur'),
    (0x00DC,'BatVCorrect',          'f',  1.0,          'V',    None, 'bms/data/BatVCorrect'),
  
    (0x00D2,'Reserve',              'H',  1,            '-',    None, 'bms/data/Reserve'),
    (0x00D4,'TimeEmergency',        'H',  1,            'S',    None, 'bms/time/TimeEmergency'),
    (0x00D6,'BatDisCurCorrect',     'H',  1,            '-',    None, 'bms/data/BatDisCurCorrect'),

    (0x00E4,'BatVoltage',           'H',  0.01,         'V',    None, 'bms/data/bat_U'),
    (0x00E6,'HeatCurrent',          'H',  0.001,        'A',    None, 'bms/data/heatCurrent'),
    (0x00EE,'RVD0EE',               'H',  1,            '-',    'lo', 'bms/data/RVD0EE'), #packed register
    (0x00EE, 'ChargerPlugged',      'B',  1,            '-',    'hi', 'bms/data/chgPlugged'),

    (0x00F0,'SysRunTicks',          'I',  0.1,          'S',    None, 'bms/SysRunTics'),
    (0x00F8, 'TempBat3',            'h',  0.1,          'C',    None, 'bms/temp/3'),
    (0x00FA, 'TempBat4',            'h',  0.1,          'C',    None, 'bms/temp/4'),
    (0x00FC, 'TempBat5',            'h',  0.1,          'C',    None, 'bms/temp/5'),

    (0x0100,'RTCTicks',             'I',  1,            '-',    None, 'bms/time/RTCTicks'),
    (0x0108,'TimeEnterSleep',       'I',  1,            'S',    None, 'bms/time/TimeEnterSleep'),
    (0x010C,'PCLModeleSts',         'H',  1,            '-',    'lo', 'bms/data/PCLModeleSts'),  #packed register
    (0x010C,'RVD10C',               'B',  1,            '0/1',  'hi', 'bms/data/RVD10C'),  #packed register

]

alarm_flags = [
   "A_WireRes",               # bit 0
   "A_MosOTP",                # bit 1
   "A_CellQuantity",          # bit 2
   "A_CurSensorErr",          # bit 3
   "A_CellOVP",               # bit 4
   "A_BatOVP",                # bit 5
   "A_ChOCP",                 # bit 6
   "A_ChSCP",                 # bit 7
   "A_ChOTP",                 # bit 8
   "A_ChUTP",                 # bit 9
   "A_CPUAuxCommErr",         # bit 10
   "A_CellUVP",               # bit 11
   "A_BatUVP",                # bit 12
   "A_DchOCP",                # bit 13
   "A_DchSCP",                # bit 14
   "A_DchOTP",                # bit 15
   "A_ChargeMOS",             # bit 16
   "A_DischargeMOS",          # bit 17
   "A_GPSDisconnected",       # bit 18
   "A_ModifyPWDtime",         # bit 19
   "A_DischargeOnFailed",     # bit 20
   "A_BatOverTemp",           # bit 21
   "A_TempSensorAnomaly",     # bit 22
   "A_PLCModuleAnomaly"       # bit 23
   ]

JKDeviceInfoRegisters = [  # base 0x1400 ###########################################################
#  (position, JKname,                 format,     coeff,  unit,       word=none/packed=hi,lo, HAname)
    (0x0000, 'DeviceID',                '16s', 1,       'string',       None,'bms/name'),  
    (0x0010, 'HWVersion',               '8s',  1,       'string',       None,'bms/hw_version'),  
    (0x0018, 'SWVersion',               '8s',  1,       'string',       None,'bms/sw_version'),  
    (0x0020, 'ODDRunTime',              'I',   1,       's',            None,'bms/ODDRunTime'),            
    (0x0024, 'PWROnTimes',              'I',   1,       'count',        None,'bms/PWROnTimes'),    
    (0x00B2, 'rwUART1MPRTOLNr',          'H',   1,       '-',           'lo','bms/settingRW/UART1MPRTOLNr'),  #packed register      
        (0x00B2, 'rwCANMPRTOLNr',        'B',   1,       '-',           'hi','bms/settingRW/CANMPRTOLNr'),          #packed register 
    (0x00B4, 'UART1MPRTOLEnable',       'H',   1,       '-',            None,'bms/setting/UART1MPRTOLEnable'),  
    (0x00D4, 'rwUART2MPRTOLNr',          'H',   1,       '-',            'lo','bms/settingRW/UART2MPRTOLEnable'),  #packed register     
        (0x00D4, 'rwUART2MPRTOLEnable',  'B',   1,       '-',            'hi','bms/settingRW/PWROnTimes'),          #packed register
    (0x00E4, 'rwLCDBuzzerTrigger',       'H',   1,       '-',            'lo','bms/settingRW/LCDBuzzerTrigger'),  #packed register 
        (0x00E4, 'rwDRY1Trigger',        'B',   1,       '-',            'hi','bms/settingRW/DRY1Trigger'),          #packed register
    (0x00E6, 'rwDRY2Trigger',            'H',   1,       '-',            'lo','bms/settingRW/DRY2Trigger'),  #packed register
        (0x00E6, 'rwUARTMPTLVer',        'B',   1,       '-',            'hi','bms/settingRW/UARTMPTLVer'),          #packed register
    (0x00E8, 'rwLCDBuzzerTriggerVal',    'i',   1,       'raw',          None,'bms/settingRW/LCDBuzzerTriggerVal'),     
    (0x00EC, 'rwLCDBuzzerReleaseVal',    'i',   1,       'raw',          None,'bms/settingRW/LCDBuzzerReleaseVal'),     
    (0x00F0, 'rwDRY1TriggerVal',         'i',   1,       'raw',          None,'bms/settingRW/DRY1TriggerVal'),     
    (0x00F4, 'rwDRY1ReleaseVal',         'i',   1,       'raw',          None,'bms/settingRW/DRY1ReleaseVal'),     
    (0x00F8, 'rwDRY2TriggerVal',         'i',   1,       'raw',          None,'bms/settingRW/DRY2TriggerVal'),     
    (0x00FC, 'rwDRY2ReleaseVal',         'i',   1,       'raw',          None,'bms/settingRW/DRY2ReleaseVal'),     
    (0x0100, 'rwDataStoredPeriod',       'i',   1,       'raw',          None,'bms/settingRW/DataStoredPeriod'),     
    (0x0104, 'rwRCVTime',                'H',   0.1,     'h',            'lo','bms/settingRW/RCVTime'),  #packed register
        (0x0104, 'rwRFVTime',            'H',   0.1,     'h',            'hi','bms/settingRW/RFVTime'),          #packed register
    (0x0106, 'rwCANProtklVer',           'B',   1,       '-',            'lo','bms/settingRW/CANProtklVer'),  #packed register 
        (0x0106, 'rwRVD106',             'B',   1,       '-',            'hi','bms/settingRW/RVD106'),          #packed register
]



# ample_desc = {
#     "soc/total_voltage": {
#         "field": "voltage",
#         "device_class": "voltage",
#         "state_class": "measurement",
#         "unit_of_measurement": "V",
#         "precision": 2,
#         "significant_digits": 4,  # round_to_n
#         "icon": "meter-electric"},
#     "soc/current": {
#         "field": "current",
#         "device_class": "current",
#         "state_class": "measurement",
#         "unit_of_measurement": "A",
#         "precision": 2,
#         "significant_digits": 4,
#     },
#     "soc/balance_current": {
#         "field": "balance_current",
#         "device_class": "current",
#         "state_class": "measurement",
#         "unit_of_measurement": "A",
#         "precision": 2,
#         "significant_digits": 4,
#         "icon": "scale-unbalanced"},
#     "soc/soc_percent": {
#         "field": "soc",
#         "device_class": "battery",
#         "state_class": None,
#         "unit_of_measurement": "%",
#         "precision": 2,
#         "significant_digits": 4,
#         "icon": "battery"},
#     "soc/power": {
#         "field": "power",
#         "device_class": "power",
#         "state_class": "measurement",
#         "unit_of_measurement": "W",
#         "precision": 1,
#         "significant_digits": 4,
#         "icon": "flash"},
#     "soc/capacity": {
#         "field": "capacity",
#         "device_class": None,
#         "state_class": None,
#         "unit_of_measurement": "Ah"
#     },
#     "soc/cycle_capacity": {
#         "field": "cycle_capacity",
#         "device_class": None,
#         "state_class": None,
#         "unit_of_measurement": "Ah"},
#     "soc/num_cycles": {
#         "field": "num_cycles",
#         "device_class": None,
#         "state_class": "measurement",
#         "unit_of_measurement": "N",
#         "icon": "battery-sync"},
#     "mosfet_status/capacity_ah": {
#         "field": "charge",
#         "device_class": None,
#         "state_class": None,
#         "unit_of_measurement": "Ah"},
#     "mosfet_status/temperature": {
#         "field": "mos_temperature",
#         "device_class": "temperature",
#         "state_class": "measurement",
#         "unit_of_measurement": "°C",
#         "icon": "thermometer"},
#     "bms/uptime": {
#         "field": "uptime",
#         "device_class": "duration",
#         "state_class": "measurement",
#         "unit_of_measurement": "s",
#         "precision": 0,
#         "icon": "clock"},
#     "meter/sample_count": {
#         "field": "num_samples",
#         "device_class": None,
#         "state_class": "measurement",
#         "unit_of_measurement": "N",
#         "icon": "counter"},
# }
