from pickle import dumps, loads
from base64 import b64encode, b64decode
from evdev import InputDevice, list_devices

import sys, asyncio

PREFIX = "OBJ:"
ERR_PREFIX = "ERR:"
UTF8 = "utf-8"

def find_keyboard(verbose = False) -> InputDevice:
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        print(f"Device: ${device.path} ${device.name}")
        if "keyboard" in str(device.name).lower():
            if verbose:
                print(f"Keyboard found ${device.path} ${device.name}")
            return device
    raise RuntimeError("Keyboard were not found!")

def send_obj(o):
    encoded_obj = b64encode(dumps(o)).decode(UTF8)
    sys.stdout.write(PREFIX+encoded_obj+'\n')
    sys.stdout.flush()
    
def receive_obj():
    while True:
        line = sys.stdin.readline()
        if line.startswith(PREFIX):
            b64str = line.removeprefix(PREFIX)
            return loads(b64decode(b64str))
        if line.startswith(ERR_PREFIX):
            raise BrokenPipeError()
    
class Receiver:
    reader = asyncio.StreamReader()
    
    async def init(self):
        loop = asyncio.get_event_loop()
        protocol = asyncio.StreamReaderProtocol(self.reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    async def receive_obj(self):
        BYTEPREFIX = PREFIX.encode(UTF8)
        BYTE_ERR_PREFIX = ERR_PREFIX.encode(UTF8)
        while True:
            line = await self.reader.readline()
            if self.reader.at_eof():
                raise BrokenPipeError()
        
            if line.startswith(BYTEPREFIX):
                b64str = line.removeprefix(BYTEPREFIX)
                return loads(b64decode(b64str))
            if line.startswith(BYTE_ERR_PREFIX):
                raise BrokenPipeError()
