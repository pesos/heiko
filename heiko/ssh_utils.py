import sys
import logging
import asyncssh

from heiko.config import Node, Job

class HeikoSSHClientSession(asyncssh.SSHClientSession):
    def data_received(self, data, datatype):
        print(data, end='')

    def connection_lost(self, exc):
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)

async def run_client(node: Node, job: Job):
    async with asyncssh.connect(node.host,
                                port=node.port,
                                username=node.username,
                                password=node.password) as conn:
        chan, session = await conn.create_session(HeikoSSHClientSession,
                                                  '; '.join(job.commands))
        await chan.wait_closed()
