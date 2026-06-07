from base import MetricCollector
import os


class DiskCollector(MetricCollector):
    def __init__(self):
        self.mount_data = {}

    def collect(self):
        mount_data = {}
        mounts_file = open("/proc/mounts")
        mounts = mounts_file.readlines()
        mounts_file.close()
        for mount in mounts:
            fs, mount = mount.split()[:2]
            try:
                mount_stats = os.statvfs(mount)
            except PermissionError:
                continue
            total_size = (mount_stats.f_blocks * mount_stats.f_bsize) / 1024
            if total_size == 0: continue

            free_size = (mount_stats.f_bfree * mount_stats.f_bsize) / 1024
            used_size = total_size - free_size
            perc = int((used_size / total_size) * 100)
            self.mount_data[mount] = {
                "filesystem": fs,
                "total": total_size,
                "avail": free_size,
                "used": used_size,
                "perc": (perc, "%"),
            }

        return self.mount_data

    def convert_size(self, mount, size):
        if self.mount_data[mount][size] < 1024:
            self.mount_data[mount][size] = (round(self.mount_data[mount][size], 1), "K")
        elif self.mount_data[mount][size] / 1024 < 1024:
            self.mount_data[mount][size] /= 1024
            self.mount_data[mount][size] = (round(self.mount_data[mount][size], 1), "M")
        else:
            self.mount_data[mount][size] /= 1024**2
            self.mount_data[mount][size] = (round(self.mount_data[mount][size], 1), "G")

    def format_data(self):
        mounts = self.collect()
        for mount, data in mounts.items():
            self.convert_size(mount, "total")
            self.convert_size(mount, "avail")
            self.convert_size(mount, "used")
        return self.mount_data
