import logging
import time
import asyncio
import heapq
import asyncssh

from heiko.config import Config
from heiko.utils.ssh import run_client
from heiko.utils.load import NodeDetails


class BasicScheduler:
    """A very simple scheduler that uses a priority queue to iterate through the avaiable nodes
    and tries to run the FIRST JOB on one node. If the node fails, the scheduler tries the next
    available node and so on.

    The nodes are sorted based on :py:class:`heiko.utils.load.NodeDetails`.

    :param config: configuration object
    :type config: :py:class:`heiko.config.Config`.
    """

    def __init__(self, config: Config):
        self.config = config
        self.nodelist = []

        for i in range(len(config.nodes)):
            self.nodeDetail(config.nodes[i])

        heapq.heapify(self.nodelist)
        logging.info("Node list: %s", [(*n[:2], n[2].name) for n in self.nodelist])

    def nodeDetail(self, node):
        """Adds a new node to the nodelist with its details

        :param node: node to add
        :type node: :py:class:`heiko.config.Node`.
        """
        details = NodeDetails(node=node)
        self.updateNode(details)

        self.nodelist.append([1, details, node])

    def updateNode(self, detail: NodeDetails):
        """Updates details of a node

        :param detail: details of the node to be updated
        :type detail: :py:class:`heiko.utils.load.NodeDetails`
        """
        try:
            asyncio.get_event_loop().run_until_complete(detail.getDetails())
        except (asyncssh.DisconnectError, ConnectionError, OSError) as e:
            logging.error("%s", e)
            logging.error("Could not get details of node %s", detail.node.name)

    def run(self):
        """Runs the scheduler until interrupted."""
        while True:
            node = heapq.heappop(self.nodelist)
            try:
                logging.info("Running on client %s", node[2].name)
                asyncio.get_event_loop().run_until_complete(
                    run_client(node[2], self.config.first_job)
                )
            except Exception as exc:
                logging.error("Got error %s", exc)
            finally:
                if float(node[0]) <= 10:
                    node[0] = node[0] * 2
                time.sleep(node[0])
                self.updateNode(node[1])

                for other_node in self.nodelist:
                    self.updateNode(other_node[1])

                heapq.heapify(self.nodelist)
                heapq.heappush(self.nodelist, node)
