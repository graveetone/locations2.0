import pandas as pd


class JMeterReportParser:
    def __init__(self, path_to_file: str):
        self.dataframe = pd.read_csv(path_to_file)

    @property
    def success_requests_number(self) -> int:
        main_requests_condition = self.dataframe["label"] == "Main request"
        success_requests_condition = self.dataframe["success"]

        return len(self.dataframe[main_requests_condition & success_requests_condition])

    @property
    def total_time_elapsed_in_seconds(self) -> float:
        """Timedelta between highest and lowest timestamps in seconds"""
        return (self.dataframe["timeStamp"].max() - self.dataframe["timeStamp"].min()) / 1000

    @property
    def throughput(self):
        """Throughput in requests per second"""
        return float(self.success_requests_number / self.total_time_elapsed_in_seconds)
