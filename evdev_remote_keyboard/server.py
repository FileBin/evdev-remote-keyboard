#!/usr/bin/env python3

from shared import send_obj, find_keyboard
import signal

from evdev import categorize, ecodes as e, InputDevice
import asyncio
    
async def run():
    keyboard: InputDevice = find_keyboard(verbose=True)

    async for event in keyboard.async_read_loop():
        try:
            if event.type == e.EV_KEY:
                key_event = categorize(event)
                match key_event.keystate:
                    case 0:
                        pass
                    case 1:
                        pass
                    case _:
                        continue 
                        
                send_obj(key_event)
        except BrokenPipeError:
            print("\nERR:BROKEN_PIPE")
            exit(0)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
