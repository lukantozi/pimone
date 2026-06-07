from base import MetricCollector
import os


CLK_TCK = os.sysconf('SC_CLK_TCK')

class ProcessMonitor(MetricCollector):
    def __init__(self):
        self.procs = {}

    def collect(self):
        uptime_file = open("/proc/uptime", "r")
        sys_uptime = uptime_file.readlines()[0].split()[0]
        uptime_file.close()

        procs = os.listdir("/proc")
        for proc in procs:
            if not proc.isdigit():
                continue
            path = os.path.join("/proc", proc, "stat")
            try:
                proc_stat = open(path, "r")
            except FileNotFoundError:
                continue

            proc_stat_vals = proc_stat.readlines()
            proc_stat.close()
            proc_stat_list = proc_stat_vals[0].split()

            pid = proc_stat_list[0]
            name = proc_stat_list[1]
            utime = float(proc_stat_list[13]) / CLK_TCK
            stime = float(proc_stat_list[14]) / CLK_TCK
            starttime = float(proc_stat_list[21]) / CLK_TCK

            proc_elapsed = float(sys_uptime) - starttime
            proc_usage_sec = utime + stime
            proc_usage_perc = proc_usage_sec * 100 / proc_elapsed if proc_elapsed != 0 else 0
            self.procs[pid] = [name, utime, stime, round(proc_usage_sec, 2), round(proc_usage_perc, 2)]
        return self.procs

    def format_data(self):
        procs = self.collect()
        procs = dict(sorted(procs.items(), key=lambda item: item[1][-1], reverse=True))
        return procs
