import logging
import time
import asyncio
import heapq

from heiko.config import Config
from heiko.ssh_utils import run_client

class BasicScheduler:
    """A very simple scheduler that uses a priority queue to iterate through the avaiable nodes
    and tried to run the FIRST JOB on one node. If the node fails, the scheduler tries the next
    available node and so on."""
    def __init__(self, config: Config):
        self.config = config
        self.nodelist = []

        for i in range(len(config.nodes)):
            self.nodelist.append([1, i, config.nodes[i]])

        heapq.heapify(self.nodelist)

    def run(self):
        while True:
            node = heapq.heappop(self.nodelist)
            try:
                asyncio.get_event_loop().run_until_complete(run_client(node[2], self.config.first_job))
            except Exception as exc:
                logging.error('Got error %s', exc)
            finally:
                if node[0] <= 10:
                    node[0] = node[0] * 2
                time.sleep(node[0])
                heapq.heappush(self.nodelist, node)
