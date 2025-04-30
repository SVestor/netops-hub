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

commands = ['enable', 'cisco', 'conf t', 'username admin1 secret cisco', 'access-list 1 permit any',
            'end', 'terminal length 0', 'sh run | i user']

for command in commands:
    print(f"Executing command: {command}")
    shell.send(command + "\n")
    time.sleep(0.5)

output = shell.recv(65535).decode('utf-8')
print(output)
    
if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()
    