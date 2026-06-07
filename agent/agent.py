from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from process import ProcessMonitor
import subprocess
import time


class Agent:
    def __init__(self):
        self.collectors = [
            CPUCollector(),
            MemoryCollector(),
            DiskCollector()
        ]
        self.processes = ProcessMonitor()
    
    def post(self):
        return {
            "cpu": self.collectors[0].format_data(),
            "memory": self.collectors[1].format_data(),
            "disk": self.collectors[2].format_data(),
            "processes": dict(list(self.processes.format_data().items())[:10])
        }


def main():
    while True:
        data = Agent().post()
        subprocess.run(["clear"])
        for d, val in data.items():
            print(d, val)
            print()
        time.sleep(1)


if __name__ == "__main__":
    main()
