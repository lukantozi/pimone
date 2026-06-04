from cpu import CPUCollector
from memory import MemoryCollector
import subprocess
import time


def run_cpu():
    cpu = CPUCollector()
    return cpu.format_data()

def run_mem():
    mem = MemoryCollector()
    return mem.collect()

def main():
    while True:
        mem_data = run_mem()
        cpu_data = run_cpu()
        subprocess.run(["clear"])
        print(mem_data)
        print(f"CPU: {cpu_data}")
        time.sleep(1)


if __name__ == "__main__":
    main()
