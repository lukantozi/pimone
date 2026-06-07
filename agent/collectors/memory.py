from .base import MetricCollector


class MemoryCollector(MetricCollector):
    def __init__(self):
        self.mems = {
            "MemTotal": 0.0,
            "MemFree": 0.0,
            "MemAvailable": 0.0,
            "Buffers": 0.0,
            "Cached": 0.0
        }
        self.mem_dict = {} 

    def collect(self):
        mem_info = open("/proc/meminfo")
        mem_stats = mem_info.readlines()[:5]
        mem_info.close()
        for stat in mem_stats:
            stat_name, stat_val = stat.split(":")
            self.mem_dict[stat_name] = stat_val.strip()
        return self.mem_dict

    def format_data(self):
        mem_data = self.collect()
        for mem in self.mems:
            self.mems[mem] = round(float(mem_data[mem].split()[0]) / (1024**2), 2)
        self.mems["MemUsed"] = round(self.mems["MemTotal"] - self.mems["MemFree"] - self.mems["Cached"], 2)
        return self.mems


#mem = MemoryCollector()
#mem_dict = mem.collect()
#print(mem_dict)
#print(mem.format_data())
