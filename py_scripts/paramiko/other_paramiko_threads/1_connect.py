# Create a Python script that connects to a Cisco Router using SSH and Paramiko. 
# The script should execute the show users command in order to display the logged-in users.

import paramiko
import time
import getpass

password = getpass.getpass('Enter password: ')

# creating an ssh client object
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

router = {
    'hostname': '192.168.224.11',
    'port': 22,
    'username': 'admin',
    'password': password
}
print(f"Connecting to {router['hostname']}")
ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

shell = ssh_client.invoke_shell()
# shell.send('term len 0\n')
# time.sleep(0.5)
shell.recv(65535).decode('utf-8')

shell.send('show users\n')
time.sleep(0.5)

output = shell.recv(65535).decode('utf-8')

with open('show_users.txt', 'w') as file:
    file.write(output)

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()
    
