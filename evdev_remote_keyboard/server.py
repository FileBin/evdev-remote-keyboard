#!/usr/bin/env python3

from shared import send_obj, find_keyboard
import signal

from evdev import categorize, ecodes as e, InputDevice
import asyncio
    
async def run():
    keyboard: InputDevice = find_keyboard(verbose=True)
    
    keyboard.grab()
    
    rightctrl_state = 0
    
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
                    
                match key_event.keycode:
                    case 'KEY_RIGHTCTRL':
                        rightctrl_state = key_event.keystate
                    case 'KEY_ESC':
                        if rightctrl_state > 0:
                            keyboard.ungrab()
                            print("Exiting...")
                            exit(0)
                        
                send_obj(key_event)
        except BrokenPipeError:
            print("\nERR:BROKEN_PIPE")
            keyboard.ungrab()
            exit(0)
            
    keyboard.ungrab()

def signal_handler(sig, frame):
    print("\nERR:CLIENT_EXIT")
    print('You pressed Ctrl+C!')
    exit()
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
