import paramiko
import yaml

stream = open("../.config/config.yaml")
config = yaml.load(stream, Loader=yaml.CLoader)

host = config['nodes'][0]['host']
username = config['nodes'][0]['username']
port = config['nodes'][0]['port']
password = config['nodes'][0]['password']

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(host, username=username, password=password, port=port)

    command_list = ["cd JoJo-Telegram-Bot", "python3 reply.py"]
    stdin, stdout, stderr = client.exec_command("; ".join(command_list))
    for line in stdout:
        print('... ' + line.strip('\n'))

except Exception as e:
    print("closing connection")
    client.close()

finally:
    print("closing connection")
    client.close()
