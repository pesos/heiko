import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect('', username='', password='', port=8022)
command_list = ["cd JoJo-Telegram-Bot", "source env/bin/activate", "python reply.py"]
stdin, stdout, stderr = client.exec_command("; ".join(command_list))
for line in stdout:
    print('... ' + line.strip('\n'))
client.close()
