from base import MetricCollector
import time


class CPUCollector(MetricCollector):
    def __init__(self):
        self.cpu_dict = {}

    def collect(self):
        cpu_stat = open("/proc/stat", "r")
        cpu_vals = [
            {y[0]: (float(y[4]), sum(float(z) for z in y[1:]))}
            for y in [x.split() for x in cpu_stat.readlines() if x.startswith("cpu")]
        ]
        cpu_stat.close()
        self.cpu_dict = {"cpu": 0} | {"cpu"+str(i): 0 for i in range(len(cpu_vals) - 1)}
        return cpu_vals

    def format_data(self):
        cpu_data_old = self.collect()
        time.sleep(1)
        cpu_data_new = self.collect()
        for i, cpu in enumerate(self.cpu_dict):
            cpu_idle = cpu_data_new[i][cpu][0] - cpu_data_old[i][cpu][0]
            cpu_delta = cpu_data_new[i][cpu][1] - cpu_data_old[i][cpu][1]
            cpu_used = cpu_delta - cpu_idle
            cpu_usage = 0 if cpu_delta == 0 else (cpu_used / cpu_delta) * 100
            self.cpu_dict[cpu] = round(cpu_usage, 2)
        return self.cpu_dict
