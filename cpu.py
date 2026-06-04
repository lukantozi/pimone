from base import MetricCollector
import subprocess
import time

class CPUCollector(MetricCollector):
    def collect(self):
        cpu_stat = open("/proc/stat", "r")
        cpu_vals = cpu_stat.readlines()[0].split()[1:]
        cpu_stat.close()
        return float(cpu_vals[3]), sum([int(x) for x in cpu_vals])

    def format_data(self):
        idle_last, cpu_sum_last = self.collect()
        time.sleep(1)
        idle_now, cpu_sum_now = self.collect()
        cpu_idle = idle_now - idle_last
        cpu_delta = cpu_sum_now - cpu_sum_last
        cpu_used = cpu_delta - cpu_idle
        cpu_usage = 0 if cpu_delta == 0 else (cpu_used / cpu_delta) * 100
        return f"{round(cpu_usage, 2)}%"
