from runner.runner import code_runner
import asyncio

loop = asyncio.get_event_loop()

if __name__ == '__main__':
    print("Executing code runner")
    loop.create_task(code_runner())
    loop.run_forever()
