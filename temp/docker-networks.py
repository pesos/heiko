import json
import atexit
import subprocess
import sys
import yaml

command = ["cd ~/Downloads", "touch sample.txt"]

def genYAML(path, nodes, command):
    stream = open(path, 'w')
    config = {'nodes': nodes, 'jobs': [{'name': 'job_1', 'commands': command }]}
    yaml.dump(config, stream)
    print(yaml.dump(config, ))
    stream.close()


num_nodes = sys.argv[1]
config_path = sys.argv[2]
lolcommand = sys.argv[3]
num_nodes = int(num_nodes)
name = "heiko_node"
nodes = list()
print("Starting containers ..........")
for i in range(num_nodes):
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

for i in range(num_nodes):
    node_name = name + str(i)
    cid = subprocess.check_output(['docker', "ps", "-a", "-q", "--no-trunc", "--filter", f'name={node_name}'])
    # print(cid)
    cid = cid.decode().strip()
    nodes[i]["host"] = network[0]['Containers'][cid]['IPv4Address'].split('/')[0]

print()
print("YAML CONFIG")
genYAML("config.yml", nodes, command)
    
def cleanup():
    print("Stopping containers .........")
    for i in range(num_nodes):
        node_name = name + str(i)
        p = subprocess.Popen(['docker', 'stop', node_name])
        p.wait()
    print("Removing containeres ............")
    for i in range(num_nodes):
        node_name = name + str(i)
        p = subprocess.Popen(['docker', 'rm', node_name])
        p.wait()

atexit.register(cleanup)
input("Present enter to stop workers")
