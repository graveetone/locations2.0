import random
from datetime import datetime
from functools import cached_property

from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries

from config import DD_API_KEY, DD_HOST, DD_APP_KEY


class DatadogClient:
    METRIC_TYPE = MetricIntakeType

    def __init__(self, metric_data):
        self.metric_name = metric_data.get("name")
        self.metric_type = metric_data.get("type", MetricIntakeType.UNSPECIFIED)
        self.metric_value = metric_data.get("value")
        self.metric_tags = metric_data.get("tags", [])

        self.metric = self._compose_metric()

    def _compose_metric(self):
        return MetricSeries(
            metric=self.metric_name,
            type=self.metric_type,
            points=[
                MetricPoint(
                    timestamp=int(datetime.now().timestamp()),
                    value=self.metric_value,
                )
            ],
            tags=self.metric_tags,
        )

    def send_metric(self):
        if self.metric is None:
            return

        body = MetricPayload(series=[self.metric])

        with ApiClient(self.configuration) as api_client:
            api_instance = MetricsApi(api_client)

            return api_instance.submit_metrics(body=body)

    @cached_property
    def configuration(self):
        return Configuration(
            host=DD_HOST,
            api_key={
                "apiKeyAuth": DD_API_KEY,
                "appKeyAuth": DD_APP_KEY,
            }
        )


apps = ["mongo_normalized", "mongo_embedded", "redis_sorted_set", "redis_list"]
actions = ["get_locations", "get_last_location", "add_location", "find_resources_nearby"]
seeds = [10, 100, 1000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]

if __name__ == "__main__":
    # while True:
    #         pair_id = str(uuid.uuid4())[:8]
    #         metric1 = {
    #             "name": "test.one",
    #             "value": random.uniform(0, 100),
    #             "tags": [f"pair_id:{pair_id}"],
    #             "type": MetricIntakeType.GAUGE
    #         }
    #         response = DatadogClient(metric_data=metric1).send_metric()
    #         print(response)
    #
    #         metric2 = {
    #             "name": "test.two",
    #             "value": random.uniform(0, 100),
    #             "tags": [f"pair_id:{pair_id}"],
    #             "type": MetricIntakeType.GAUGE
    #         }
    #         response = DatadogClient(metric_data=metric2).send_metric()
    #         print(response)
    #         time.sleep(10)

    for seed in seeds:
        for app in apps:
            for action in actions:
                pair_id = f"{app}-{seed}-{action}"
                metric = {
                    "name": "jmeter.successful_requests",
                    "value": random.uniform(0, 100),
                    "tags": [f"app:{app}", f"action:{action}", f"seed:{seed}", f"pair_id:{pair_id}"],
                    "type": MetricIntakeType.GAUGE
                }
                response = DatadogClient(metric_data=metric).send_metric()
                print(f"{app}-{action}-{seed}: {response}")

                metric = {
                    "name": "app.seed",
                    "value": seed,
                    "tags": [f"pair_id:{pair_id}"],
                    "type": MetricIntakeType.GAUGE
                }
                response = DatadogClient(metric_data=metric).send_metric()
                print(f"{app}-{action}-{seed}: {response}")
