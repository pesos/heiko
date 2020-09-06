import time
import logging
import paramiko
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logging.basicConfig(level=logging.DEBUG)

stream = open("../.config/config.yaml")
config = yaml.load(stream, Loader=Loader)

host = config['nodes'][0]['host']
username = config['nodes'][0]['username']
port = config['nodes'][0]['port']
password = config['nodes'][0]['password']

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(host, username=username, password=password, port=port)

    command_list = ["cd JoJo-Telegram-Bot", "source env/bin/activate", "python3 reply.py"]
    stdin, stdout, stderr = client.exec_command("; ".join(command_list))
    while True:
        try:
            transport = client.get_transport()
            transport.send_ignore()
            if stdout.channel.exit_status_ready():
                exit_status = stdout.channel.recv_exit_status()
            else:
                exit_status = 0
            if transport.is_active() and not (exit_status > 0):
                logging.debug("sleeping for 0.1s")
                time.sleep(0.1)
            else:
                logging.info("connection closed")
                break
        except EOFError as e:
            logging.info("connection closed")
            break
    client.close()
    del client, stdin, stdout, stderr

except Exception as e:
    logging.error("Got error %s", e)

finally:
    logging.info("Inside finally")

logging.info("Hello there")
