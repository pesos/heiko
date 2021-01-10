import subprocess
import os

import asyncio

from heiko.config import Node
from heiko.utils.ssh import run_client

IGNORE_FILE = ".heiko/rsync-ignore"


def sync_folder(name: str, node: Node):
    # make ~/.heiko folder if it doesn't exist
    asyncio.get_event_loop().run_until_complete(run_client(node, ["mkdir -p ~/.heiko"]))

    pwd = os.getcwd()

    command = [
        "rsync",
        "-a",
        "--info=progress2",
        "-e",
        f"ssh -p {node.port}",
        pwd + "/",
        f"{node.username}@{node.host}:~/.heiko/{name}",
    ]

    if os.path.isfile(os.path.join(pwd, IGNORE_FILE)):
        exclude = f"--exclude-from={IGNORE_FILE}"
        command.insert(-2, exclude)  # add exclude before source dir name

    if node.password:
        subprocess.run(["sshpass", "-p", node.password, *command])
    else:
        subprocess.run(command)
