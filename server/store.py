import time


class MetricStore:
    def __init__(self):
        self.values = {}

    def calculate_delta(self, minutes):
        now = time.time()
        seconds = minutes * 60
        delta = now - seconds
        return delta


class RollingStore(MetricStore):
    def store(self, data: dict, minutes: float):
        ct = time.time()
        self.values[ct] = data
        delta = self.calculate_delta(minutes)
        if delta < next(iter(self.values)):
            self.values = {
                x: val
                for x, val in self.values.items()
                if delta < x
            }

    @property
    def get(self):
        return self.values

    @property
    def average(self):
        cpu_sum = sum([self.values[k]["cpu"]["cpu"]
                       for k in self.values])
        mem_sum = sum([self.values[k]["memory"]["MemUsed"]
                       for k in self.values])
        cpu_average = cpu_sum / len(self.values) if len(self.values) != 0 else 0
        mem_average = mem_sum / len(self.values) if len(self.values) != 0 else 0
        return {
            "cpu_average": cpu_average,
            "mem_average": mem_average,
        }

    @property
    def peak(self):
        cpu_peak = max([self.values[k]["cpu"]["cpu"]
                       for k in self.values]) if self.values else 0
        mem_peak = max([self.values[k]["memory"]["MemUsed"]
                       for k in self.values]) if self.values else 0
        return {
            "cpu_peak": cpu_peak,
            "mem_peak": mem_peak,
        }


rolling = RollingStore()
