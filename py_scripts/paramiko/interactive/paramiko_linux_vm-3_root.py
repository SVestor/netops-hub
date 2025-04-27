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
stdin, stdout, stderr = ssh_client.exec_command('sudo useradd user1\n', get_pty=True)
stdin.write('pass123\n')
time.sleep(0.5)

stdin, stdout, stderr = ssh_client.exec_command('cat /etc/passwd\n')
time.sleep(0.5)

print(stdout.read().decode())
print(stderr.read().decode())

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()
