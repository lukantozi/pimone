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
        if not self.values:
            return {"cpu_average": 0, "mem_average": 0}
        cpu_values = []
        mem_values = []
        for value in self.values.values():
            try:
                cpu_values.append(value["cpu"]["cpu"])
                mem_values.append(value["memory"]["MemUsed"])
            except KeyError:
                continue

        if not cpu_values or not mem_values:
            return {"cpu_average": 0, "mem_average": 0}

        cpu_average = round(sum(cpu_values) / len(cpu_values), 2)
        mem_average = round(sum(mem_values) / len(mem_values), 2)
        return {
            "cpu_average": cpu_average,
            "mem_average": mem_average,
        }

    @property
    def peak(self):
        if not self.values:
            return {"cpu_peak": 0, "mem_peak": 0}

        cpu_values = []
        mem_values = []
        for value in self.values.values():
            try:
                cpu_values.append(value["cpu"]["cpu"])
                mem_values.append(value["memory"]["MemUsed"])
            except KeyError:
                continue
        if not cpu_values or not mem_values:
            return {"cpu_peak": 0, "mem_peak": 0}

        cpu_peak = max(cpu_values)
        mem_peak = max(mem_values)

        return {
            "cpu_peak": cpu_peak,
            "mem_peak": mem_peak,
        }


rolling = RollingStore()
