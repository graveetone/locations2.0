import asyncio
import json
import subprocess
import time

from config import PATH_TO_JMETER_REPORTS, PATH_TO_JMETER, PATH_TO_APP, SERVER_START_STOP_TIMEOUT, \
    PATH_TO_TEST_PLAN
from constants import Action, AppCode
from mappings import ACTIONS_PAYLOADS_MAPPING

RUN_SERVER_COMMAND = ["fastapi", "run", PATH_TO_APP]  # specify workers


def run_server():
    server_process = subprocess.Popen(RUN_SERVER_COMMAND)
    time.sleep(SERVER_START_STOP_TIMEOUT)
    return server_process


def run_test_plans(app_code: AppCode, action: Action):
    output_file = PATH_TO_JMETER_REPORTS / app_code.value / f"{action.value}.csv"
    request_payload = json.dumps({
        **ACTIONS_PAYLOADS_MAPPING[action],
        "action": action.value
    })
    subprocess.run(
        [
            PATH_TO_JMETER,
            "-n",
            f"-t={PATH_TO_TEST_PLAN}",
            f"-l={output_file}",
            f"-Japp_code={app_code.value}",
            f"-Jpayload={request_payload}"
        ]
    )


def parse_reports():
    ...


def send_metrics_to_datadog():
    ...


def shutdown_server(server_process: subprocess.Popen):
    server_process.terminate()
    time.sleep(SERVER_START_STOP_TIMEOUT)  # wait for server to shut down


def get_event_loop():
    try:
        _loop = asyncio.get_running_loop()
    except RuntimeError:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)

    return _loop
