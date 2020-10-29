import logging
import time
import asyncio
import heapq

from heiko.config import Config
from heiko.utils.ssh import run_client
from heiko.utils.load import NodeDetails


class BasicScheduler:
    """A very simple scheduler that uses a priority queue to iterate through the avaiable nodes
    and tried to run the FIRST JOB on one node. If the node fails, the scheduler tries the next
    available node and so on."""
    def __init__(self, config: Config):
        self.config = config
        self.nodelist = []

        for i in range(len(config.nodes)):
            try:
                self.nodeDetail(config.nodes[i])
            except Exception as e:
                logging.error("Got error %s", e)
                logging.info("Ignoring node for now")

        heapq.heapify(self.nodelist)
    
    def nodeDetail(self, node):
        # print("Node = ", node)
        utils = NodeDetails(node=node)
        asyncio.get_event_loop().run_until_complete(utils.getDetails())
        cores = utils.details['cpu']['cpus']
        
        if utils.details['cpu']['cpu_max']:
            cpu_freq = utils.details['cpu']['cpu_max']
        else:
            cpu_freq = utils.details['cpu']['cpu_mhz']
        
        total_mem = utils.details['ram']['total_mem']
        free_mem = utils.details['ram']['free_mem']

        load = utils.details['usage']

        self.nodelist.append([1, load, free_mem, cpu_freq, cores, total_mem, node])
    
    def updateNode(self, node):
        utils = NodeDetails(node=node[6])
        asyncio.get_event_loop().run_until_complete(utils.getDetails())
        load = utils.details['usage']
        node[1] = load

    def run(self):
        while True:
            node = heapq.heappop(self.nodelist)
            try:
                asyncio.get_event_loop().run_until_complete(run_client(node[6], self.config.first_job))
            except Exception as exc:
                logging.error('Got error %s', exc)
            finally:
                if  float(node[0]) <= 10:
                    node[0] = node[0] * 2
                time.sleep(node[0])
                try:
                    self.updateNode(node)
                except Exception as e:
                    logging.error("Got error %s", e)
                    logging.info("Ignoring node for now")
                
                heapq.heappush(self.nodelist, node)
