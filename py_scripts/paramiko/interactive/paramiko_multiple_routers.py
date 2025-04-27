import paramiko
import time
import getpass

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

password = getpass.getpass('Enter password: ')

router1 = {
    'hostname': '192.168.224.11',
    'port': 22,
    'username': 'admin',
    'password': password
}

router2 = {
    'hostname': '192.168.224.12',
    'port': 22,
    'username': 'admin',
    'password': password
}

router3 = {
    'hostname': '192.168.224.13',
    'port': 22,
    'username': 'admin',
    'password': password
}

routers = [router1, router2, router3]

for router in routers:
    print(f"Connecting to {router['hostname']}")
    ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

    # print(f"Connection status: {ssh_client.get_transport().is_active()}")

    # sending commands
    shell = ssh_client.invoke_shell()
    shell.send('enable\n')
    shell.send('cisco123\n')
    shell.send('conf t\n')
    shell.send('router ospf 1\n')
    shell.send('network 0.0.0.0 0.0.0.0 area 0\n')
    shell.send('end\n')
    shell.send('term len 0\n')
    shell.send('sh ip protocols\n')
    shell.send('sh ip route\n')
    time.sleep(2)

    output = shell.recv(65535).decode('utf-8')
    print(output)

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()
