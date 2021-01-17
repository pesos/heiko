import json
import atexit
import subprocess
import yaml
import argparse
import textwrap
from dataclasses import dataclass

@dataclass
class Config:
    num_nodes: int
    config_path: str
    def __init__(self, n: int, c: str):
        self.num_nodes = n
        self.config_path = c
        self.place_holder_commands = ["cd ~/Downloads", "touch sample.txt"]

def make_parser():
    parser_ = argparse.ArgumentParser(
        prog="heiko-docker-test",
        description=textwrap.dedent(
            """
            heiko-docker-test allows you test your heiko config
            locally with just docker.\n

            It takes 2 arguments, number of nodes (containers) and
            config_path (the path where the config is written to).\n

            Using the provided args, it generates a config file which
            connects to the containers. The config can then be further 
            modified to provide the required jobs to be run.\n

            After modifying the config, deploy heiko to test.
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_.add_argument(
        "-n",
        "--number",
        help="Number of nodes",
        required=True,
        action="store",
        dest="number_of_nodes",
    )
    parser_.add_argument(
        "-c",
        "--config_path",
        help="Path where the config should be generated",
        required=True,
        action="store",
        dest="config",
    )
    return parser_

def genYAML(path, nodes, command):
    stream = open(path, 'w')
    config = {'nodes': nodes, 'jobs': [{'name': 'job_1', 'commands': command }]}
    yaml.dump(config, stream)
    print(yaml.dump(config, ))
    stream.close()

parser = make_parser()
args = parser.parse_args()
n = int(args.number_of_nodes)
c = args.config
config = Config(n, c)
# num_nodes = sys.argv[1]
# config_path = sys.argv[2]
# num_nodes = int(num_nodes)
name = "heiko_node"
nodes = list()
print("Starting containers ..........")
for i in range(config.num_nodes):
    nodes.append(dict())
    node_name = name + str(i)
    # spawn containers
    p = subprocess.Popen(['docker', 'run', '-it', '-d', '--name', node_name, "heiko-node", "/bin/bash"])
    p.wait()
    nodes[i]["name"] = node_name
    nodes[i]["username"] = "root"
    nodes[i]["password"] = "yabe"

# gets networks
print("Network extraction")
out = subprocess.check_output(["docker", "network", "inspect", "bridge"])
network = json.loads(out)
# print(network)
# print(network[0]['Containers'])

for i in range(config.num_nodes):
    node_name = name + str(i)
    cid = subprocess.check_output(['docker', "ps", "-a", "-q", "--no-trunc", "--filter", f'name={node_name}'])
    # print(cid)
    cid = cid.decode().strip()
    nodes[i]["host"] = network[0]['Containers'][cid]['IPv4Address'].split('/')[0]

print()
print("YAML CONFIG")
genYAML(config.config_path, nodes, config.place_holder_commands)


def cleanup():
    print("Stopping containers .........")
    for i in range(config.num_nodes):
        node_name = name + str(i)
        p = subprocess.Popen(['docker', 'stop', node_name])
        p.wait()
    print("Removing containeres ............")
    for i in range(config.num_nodes):
        node_name = name + str(i)
        p = subprocess.Popen(['docker', 'rm', node_name])
        p.wait()


atexit.register(cleanup)
input("Present enter to stop workers")
