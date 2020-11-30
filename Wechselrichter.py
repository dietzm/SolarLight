from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder 
import logging
import sys
log = logging.getLogger()
# STP 10k
#
# 30865 Netzbezug in W   s32
# 30867 Einspeisung in W	s32
# 30869 PV Erzeugung in W (Nachts int max) S32
# 30871 EIgenverbrauch in W  u32
# 30535 Tagesertrag in Wh
# 41255 Einspeisebegrenzung ?
class Wechselrichter:
    stp10k={
    "Netzbezug":30865,
    "Einspeisung":30867,
    "Erzeugung": 30869,
    "Eigenverbrauch": 30871,
    "Tagesertrag":30535,
    "PVTotalW": 30775
    }

    def __init__(self, server, port=502, wr=stp10k):
        self.server = server
        self.client = ModbusClient(server, port=502)
        self.connect()
        self.wr = wr
            

    def connect(self):
        c=self.client.connect()
        if c:
            log.info(f"Connect to {self.server} successfull")
        else:
            log.warning(f"Connect to {self.server} failed")
            
    
    def getValue(self,typ):
        nr = self.wr.get(typ, None);
        if nr is None:
            log.error(f"Cannot get register number for typ {typ}")
            return 0
        
        result = self.client.read_input_registers(nr, 2, unit=3)
        log.debug(f"DEBUG: {result.registers}")
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, wordorder=Endian.Big, byteorder=Endian.Big)
        value = decoder.decode_32bit_uint()
        log.debug(f"{typ} ({nr}): {value} W?")
        return value



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: Wechselrichter.py ip register")
        exit(0)

    mw = Wechselrichter(sys.argv[1])
    key = f"Register:{sys.argv[2]}"
    mw.stp10k[key] = int(sys.argv[2])
    val = mw.getValue(key)
    print(f"{key}: {val}")
    
