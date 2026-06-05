from cpu import CPUCollector
from memory import MemoryCollector
from disk import DiskCollector
import subprocess
import time


def run_cpu():
    cpu = CPUCollector()
    return cpu.format_data()


def run_mem():
    mem = MemoryCollector()
    return mem.format_data()

def run_disk():
    dc = DiskCollector()
    return dc.format_data()

def main():
    while True:
        mem_data = run_mem()
        cpu_data = run_cpu()
        mount_data = run_disk()
        subprocess.run(["clear"])
        print(f"Memory: {mem_data}")
        print(f"CPU: {cpu_data}")
        print(f"Mounts: {mount_data}")
        time.sleep(1)


if __name__ == "__main__":
    main()
