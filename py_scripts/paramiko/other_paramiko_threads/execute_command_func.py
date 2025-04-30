import paramiko 
import time
import threading
import getpass

def execute_command(device, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Connecting to {device['hostname']}")
    ssh_client.connect(**device, look_for_keys=False, allow_agent=False)
    
    shell = ssh_client.invoke_shell()

    print(f"Executing command: {command} on {device['hostname']}")
    shell.send('term len 0\n')
    shell.send(f"{command}\n")
    time.sleep(0.5)

    output = shell.recv(65535).decode('utf-8')
    print(output)
    
    if ssh_client.get_transport().is_active() == True:
        print('Closing connection')
        ssh_client.close()

if __name__ == '__main__':
    password = getpass.getpass('Enter password: ')

    router1 = {
        'hostname': '192.168.224.11',
        'port': 22,
        'username': 'admin',
        'password': password,
    }

    router2 = {
        'hostname': '192.168.224.12',
        'port': 22,
        'username': 'admin',
        'password': password,
    }

    router3 = {
        'hostname': '192.168.224.13',
        'port': 22,
        'username': 'admin',
        'password': password,
    }

    devices = [router1, router2, router3]

    threads = list()
    for device in devices:
        thread = threading.Thread(target=execute_command, args=(device, 'show ip int brief'))
        threads.append(thread)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    
    

    
    
