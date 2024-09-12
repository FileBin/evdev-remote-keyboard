#!/usr/bin/env python3

from evdev import UInput, ecodes as e
import asyncio, signal
from shared import Receiver

ui = UInput()

def signal_handler(sig, frame):
    ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
    ui.write(e.EV_KEY, e.KEY_LEFTALT, 0)
    ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
    
    ui.write(e.EV_KEY, e.KEY_RIGHTCTRL, 0)
    ui.write(e.EV_KEY, e.KEY_RIGHTALT, 0)
    ui.write(e.EV_KEY, e.KEY_RIGHTSHIFT, 0)
    
    ui.write(e.EV_KEY, e.KEY_C, 0)
    ui.syn()
    
    print("Client exiting")

async def run():
    receiver = Receiver()
    await receiver.init()
    with UInput() as ui:
        try:
            while True:
                key_event = await receiver.receive_obj()
                match key_event.keystate:
                    case 0:
                        pass
                    case 1:
                        pass
                    case _:
                        continue
                    
                print(f"Recieved: ${key_event}")
                ui.write_event(key_event)
                ui.syn()
        finally:
            signal_handler(0,0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
