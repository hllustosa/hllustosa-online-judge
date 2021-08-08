from .seccomp import SECCOMP_CODE
from aio_pika import IncomingMessage
from .bus import Bus
import os
import json
import subprocess
import tempfile
import threading

CORRECT_OUTPUT = 100.0

class Execution():

    def __init__(self, msg):
        self.run_id = msg['id']
        self.code = msg['code']
        self.input = msg['problem']['input']
        self.timeout = msg['problem']['timeout']
        self.expected_output = msg['problem']['output'].split("\n")
        self.files = []


async def on_message(message: IncomingMessage):
    async with message.process():
        bus = Bus()
        msg = json.loads(message.body)
        processing_thread = threading.Thread(target=execute, args=[msg, bus])
        processing_thread.start()


def execute(*args):
    try:
        [message, bus] = args
        execution = Execution(message)

        if 'PYTHONSANDBOX' in os.environ.keys():
            code_file = create_temp_file(
                SECCOMP_CODE + execution.code, files=execution.files)
        else:
            code_file = create_temp_file(execution.code, files=execution.files)

        input_file = create_temp_file(execution.input, files=execution.files)
        output_file = create_temp_file(None, files=execution.files)
        stderr_file = create_temp_file(None, files=execution.files)

        notify_progress(bus, execution.run_id, 'Running')

        process = subprocess.Popen(
            ['timeout', f'{execution.timeout}s', 'python3', f'{code_file.name}'], stdin=input_file, stdout=output_file, stderr=stderr_file)

        process.wait()

        output = open(output_file.name, 'r').readlines()
        errors = open(stderr_file.name, 'r').readlines()
        result = calc_diff(output, execution.expected_output)

        if len(errors) != 0:
            notify_progress(bus, execution.run_id, 'Runtime or Compilation Error')
        elif result == CORRECT_OUTPUT:
            notify_progress(bus, execution.run_id, 'Success')
        else:
            notify_progress(bus, execution.run_id, f'Wrong Answer({result}%)') 

    except Exception:
        notify_progress(bus, execution.run_id, 'Server Error')
    finally:
        kill_process(process)
        clean_up(execution.files)


def create_temp_file(content, files):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    if content != None:
        temp_file.write(content.encode('utf-8'))
        temp_file.flush()
        temp_file.close()
        temp_file = open(temp_file.name)

    files.append(temp_file)
    return temp_file


def calc_diff(output, expected_output):

    expected_length = len(expected_output)
    compare_length = min(len(output), expected_length)

    correct_line_count = 0
    for line in range(compare_length):
        if output[line].replace("\n", "") == expected_output[line].replace("\n", ""):
            correct_line_count = correct_line_count + 1

    if correct_line_count == expected_length:
        return CORRECT_OUTPUT
    else:
        percentage_correct_lines = float(
            correct_line_count)/(1.0 if expected_length == 0 else expected_length)
        return percentage_correct_lines*100


def notify_progress(bus, run_id, progress):
    bus.send_notification({
        'run_id': run_id,
        'progress': progress
    })

def clean_up(files):
    for file in files:
        try:
            os.remove(file.name)
        except Exception as e:
            pass

def kill_process(process):
    try:
        process.kill()
    except:
        pass
