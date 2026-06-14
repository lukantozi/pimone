from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from process import ProcessMonitor
import requests
import os


LOGICAL_CORES = os.cpu_count() or 1
url = "http://localhost:5000/metrics"


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
            "processes": dict(list(self.processes.format_data().items())[:10]),
            "cores": LOGICAL_CORES,
        }


def main():
    while True:
        data = Agent().post()
        #time.sleep(5)
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("sent ok")
        else:
            print("failed to send")


if __name__ == "__main__":
    main()
