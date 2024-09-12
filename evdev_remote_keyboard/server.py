#!/usr/bin/env python3

from shared import send_obj, find_keyboard

from evdev import categorize, ecodes as e, InputDevice
import asyncio
    
async def run():
    keyboard: InputDevice = find_keyboard(verbose=True)
            
    async for event in keyboard.async_read_loop():
        if event.type == e.EV_KEY:
            key_event = categorize(event)
            send_obj(key_event)


if __name__ == "__main__":
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
