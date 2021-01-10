import subprocess
import os
from heiko.config import Node

IGNORE_FILE = ".heiko/rsync-ignore"


def sync_folder(name: str, node: Node):
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
