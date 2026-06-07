from cpu import CPUCollector
from memory import MemoryCollector
from disk import DiskCollector
from process import ProcessMonitor
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


def run_proc():
    proc = ProcessMonitor()
    return list(proc.format_data().items())[:10]


def main():
    while True:
        mem_data = run_mem()
        cpu_data = run_cpu()
        mount_data = run_disk()
        proc_data = run_proc()
        subprocess.run(["clear"])
        print()
        print(f"Memory: {mem_data}")
        print()
        print(f"CPU: {cpu_data}")
        print()
        print(f"Mounts: {mount_data}")
        print()
        print(f"Processes: {proc_data}")
        time.sleep(1)


if __name__ == "__main__":
    main()
