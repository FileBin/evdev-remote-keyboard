#!/usr/bin/env python3

from evdev import UInput
import asyncio
from shared import Receiver

async def run():
    receiver = Receiver()
    await receiver.init()
    with UInput() as ui:
        while True:
            key_event = await receiver.receive_obj()
            print(f"Recieved: ${key_event}")
            ui.write_event(key_event)
            ui.syn()


if __name__ == "__main__":
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
