import sys
import asyncssh

from heiko.config import Node, Job


class HeikoSSHClientSession(asyncssh.SSHClientSession):
    """A class to handle SSH connections cleanly"""

    def data_received(self, data, datatype):
        """Prints the received data directly"""
        print(data, end="")

    def connection_lost(self, exc):
        """Prints an error message to stderr"""
        if exc:
            print("SSH session error: " + str(exc), file=sys.stderr)


async def run_client(node: Node, job: Job):
    """Runs given job on given node

    :param node: node to run on
    :type node: :py:class:`heiko.config.Node`
    :param job: job to run
    :type job: :py:class:`heiko.config.Job`
    """
    async with asyncssh.connect(
        node.host, port=node.port, username=node.username, password=node.password
    ) as conn:
        chan, session = await conn.create_session(
            HeikoSSHClientSession, "; ".join(job.commands)
        )
        await chan.wait_closed()
