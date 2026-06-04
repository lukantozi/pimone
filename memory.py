from base import MetricCollector

class MemoryCollector(MetricCollector):
    def collect(self):
        mem_info = open("/proc/meminfo")
        mem_stats = mem_info.readlines()[:3]
        mem_info.close()
        mem_dict = {}
        for stat in mem_stats:
            stat_name, stat_val = stat.split(":")
            mem_dict[stat_name] = stat_val.strip()
        return mem_dict
