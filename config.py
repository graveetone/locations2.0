from pathlib import Path

PROJECT_DIR = Path()
PATH_TO_JMETER = PROJECT_DIR / "apache-jmeter-5.6.2/bin/jmeter"
PATH_TO_TEST_PLAN = PROJECT_DIR / "test_plan.jmx"
PATH_TO_JMETER_REPORTS = PROJECT_DIR / "jmeter_reports"
PATH_TO_APP = PROJECT_DIR / "main.py"
SERVER_START_STOP_TIMEOUT = 2

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "decode_responses": True
}

MONGO_CONFIG = {
    "host": "localhost",
    "port": 27017
}
