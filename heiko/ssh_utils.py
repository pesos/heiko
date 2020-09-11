import sys
import asyncssh

from heiko.config import Node, Job

async def run_client(node: Node, job: Job):
    async with asyncssh.connect(node.host,
                                port=node.port,
                                username=node.username,
                                password=node.password) as conn:
        await conn.run('; '.join(job.commands), check=True,
                                stdout=sys.stdout, stderr=sys.stdout)
