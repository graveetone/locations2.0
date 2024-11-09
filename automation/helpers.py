import asyncio
import datetime
import json
import os
import random
import shutil
import subprocess
import time

from config import PATH_TO_JMETER_REPORTS, PATH_TO_JMETER, PATH_TO_APP, SERVER_START_STOP_TIMEOUT, \
    PATH_TO_TEST_PLAN
from constants import Action, AppCode
from mappings import ACTIONS_PAYLOADS_MAPPING
from utils.datadog_client import DatadogClient
from utils.jmeter_report_parser import JMeterReportParser

RUN_SERVER_COMMAND = ["fastapi", "run", PATH_TO_APP]  # specify workers


def run_server():
    server_process = subprocess.Popen(RUN_SERVER_COMMAND)
    time.sleep(SERVER_START_STOP_TIMEOUT)
    return server_process


def get_path_to_jmeter_report(app_code: AppCode, action: Action, seed_param: dict):
    resources, locations = seed_param["number_of_resources"], seed_param["locations_per_resource"],
    return PATH_TO_JMETER_REPORTS / f"{resources}_{locations}" / app_code.value / f"{action.value}.csv"


def run_test_plans(app_code: AppCode, action: Action, seed_param: dict):
    output_file = get_path_to_jmeter_report(app_code=app_code, action=action, seed_param=seed_param)
    request_payload = {
        **ACTIONS_PAYLOADS_MAPPING[action],
        "action": action.value
    }
    if request_payload.get("resource_id") is not None:
        request_payload.update(
            {
                "resource_id": random.randint(1, seed_param["number_of_resources"])
            }
        )
    request_payload = json.dumps(request_payload)
    subprocess.run(
        [
            PATH_TO_JMETER,
            "-n",
            f"-t={PATH_TO_TEST_PLAN}",
            f"-l={output_file}",
            f"-Japp_code={app_code.value}",
            f"-Jpayload={request_payload}",
        ]
    )


def parse_report(app_code: AppCode, action: Action, seed_param: dict) -> dict:
    path_to_report = get_path_to_jmeter_report(app_code=app_code, action=action, seed_param=seed_param)
    parser = JMeterReportParser(path_to_report)

    return {
        "app_code": app_code.value,
        "action": action.value,
        "locations": seed_param["number_of_resources"] * seed_param["locations_per_resource"],
        "throughput": parser.throughput
    }


def send_metrics_to_datadog(report_data):
    identifier = "{app}-{action}-{locations}".format(
        app=report_data["app_code"],
        action=report_data["action"],
        locations=report_data["locations"]
    )
    throughput_metric = {
        "name": "app.throughput",
        "type": DatadogClient.METRIC_TYPE.GAUGE,
        "value": report_data["throughput"],
        "tags": [
            f"app:{report_data['app_code']}",
            f"action:{report_data['action']}",
            f"locations:{report_data['locations']}",
            f"identifier:{identifier}",
        ]
    }
    locations_metric = {
        "name": "app.locations",
        "type": DatadogClient.METRIC_TYPE.GAUGE,
        "value": report_data["locations"],
        "tags": [
            f"identifier:{identifier}"
        ]
    }

    DatadogClient(metric_data=throughput_metric).send_metric()
    DatadogClient(metric_data=locations_metric).send_metric()


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


def rotate_reports():
    if not os.path.exists(PATH_TO_JMETER_REPORTS):
        return

    timestamp = datetime.datetime.now().timestamp()
    shutil.copytree(PATH_TO_JMETER_REPORTS, f"{PATH_TO_JMETER_REPORTS}_{timestamp}")
    shutil.rmtree(PATH_TO_JMETER_REPORTS)
