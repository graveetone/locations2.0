from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path()
PATH_TO_JMETER = os.getenv("PATH_TO_JMETER_EXECUTABLE_FILE")
PATH_TO_TEST_PLAN = PROJECT_DIR / "test_plan.jmx"
PATH_TO_JMETER_REPORTS = PROJECT_DIR / "jmeter_reports"
PATH_TO_APP = PROJECT_DIR / "main.py"
SERVER_START_STOP_TIMEOUT = 2

REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST"),
    "port": int(os.getenv("REDIS_PORT")),
    "decode_responses": True
}

MONGO_CONFIG = {
    "host": os.getenv("MONGO_HOST"),
    "port": int(os.getenv("MONGO_PORT")),
}

SEED_PARAMETERS = [
    {"number_of_resources": 100, "locations_per_resource": 1000},     # 1 000
    {"number_of_resources": 200, "locations_per_resource": 1000},     # 5 000
    {"number_of_resources": 300, "locations_per_resource": 1000},    # 10 000
    {"number_of_resources": 400, "locations_per_resource": 1000},    # 50 000
    {"number_of_resources": 500, "locations_per_resource": 1000},   # 100 000
    {"number_of_resources": 600, "locations_per_resource": 1000},   # 500 000
    {"number_of_resources": 700, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 800, "locations_per_resource": 1000},  # 800 000
    {"number_of_resources": 900, "locations_per_resource": 1000},  # 900 000
    {"number_of_resources": 1000, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1100, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1200, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1300, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1400, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1500, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1600, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1700, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1800, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 1900, "locations_per_resource": 1000},  # 1 000 000
    {"number_of_resources": 2000, "locations_per_resource": 1000},  # 1 000 000
]

DD_API_KEY = os.getenv("DATADOG_API_KEY")
DD_APP_KEY = os.getenv("DATADOG_APP_KEY")
DD_HOST = os.getenv("DATADOG_HOST")
