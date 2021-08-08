from runner.bus import Bus
from runner.runner import on_message
import asyncio

loop = asyncio.get_event_loop()


async def start_code_runner():
    bus = Bus()
    await bus.register_message(on_message, loop)


if __name__ == '__main__':
    print("Executing code runner")
    loop.create_task(start_code_runner())
    loop.run_forever()
