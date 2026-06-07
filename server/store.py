import datetime
import time

class MetricStore:
    def __init__(self):
        self.values = {}
        self.recent = None

    def store(self, data: dict):
        ct = time.time()
        self.values[ct] = data
        self.recent = ct

    @property
    def get(self):
        return self.values[self.recent]

metric_store = MetricStore()
