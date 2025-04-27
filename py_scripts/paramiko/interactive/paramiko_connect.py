import paramiko
import time
import getpass

ssh_client = paramiko.SSHClient()
#print(type(ssh_client))

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname="192.168.224.11", username="admin", password="cisco123", 
#     look_for_keys=False, allow_agent=False)

password = getpass.getpass('Enter password: ')

router = {
    'hostname': '192.168.224.11',
    'port': 22,
    'username': 'admin',
    'password': password
}
print(f"Connecting to {router['hostname']}")
ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

# print(f"Connection status: {ssh_client.get_transport().is_active()}")

# sending commands
shell = ssh_client.invoke_shell()
shell.send('term len 0\n')
shell.send('show version\n')
shell.send('sh ip int br\n')
shell.send('sh ip route\n')

time.sleep(2)

output = shell.recv(65535).decode('utf-8')
print(output)

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()


