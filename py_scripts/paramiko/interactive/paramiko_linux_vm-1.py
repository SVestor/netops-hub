import paramiko
import time
import getpass

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

password = getpass.getpass('Enter password: ')

linux_vm1 = {
    'hostname': '192.168.224.254',
    'port': 22,
    'username': 'ubuntu',
    'password': password
}

print(f"Connecting to {linux_vm1['hostname']}")
ssh_client.connect(**linux_vm1, look_for_keys=False, allow_agent=False)

# print(f"Connection status: {ssh_client.get_transport().is_active()}")

# sending commands
shell = ssh_client.invoke_shell()
shell.send('cat /etc/passwd\n')
time.sleep(1)

shell.send('sudo cat /etc/shadow\n')
shell.send('pass123\n')
time.sleep(1)

output = shell.recv(65535).decode('utf-8')
print(output)

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()
