import paramiko
import time

def connect(server_ip, server_port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Connecting to {server_ip}")
    ssh_client.connect(hostname=server_ip, port=server_port, username=username, password=password, 
        look_for_keys=False, allow_agent=False)
    
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell 

def send_command(shell, command, timeout=1):
    print(f"Sending command: {command}")
    shell.send(command + "\n")
    time.sleep(timeout)

def show(shell, n=10000):
    output = shell.recv(n).decode('utf-8')
    return output

def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        print('Closing connection')
        ssh_client.close() 

def send_from_list(shell, commands):
    for command in commands:
        send_command(shell, command)

def send_from_file(shell, filename):
    with open(filename, 'r') as file:
        commands = file.read().splitlines()
        send_from_list(shell, commands)

def target_function(router):
    ssh_client = connect(server_ip=router['server_ip'], server_port=router['server_port'], username=router['username'], password=router['password'])
    shell = get_shell(ssh_client)
    send_from_file(shell, router['config'])
    output = show(shell)
    print(output)


if __name__ == '__main__': 
    # client = connect('192.168.224.11', '22', 'admin', 'cisco123')
    router1 = {
        'server_ip': '192.168.224.11',
        'server_port': 22,
        'username': 'admin',
        'password': 'cisco123'
    }

    client = connect(**router1)
    shell = get_shell(client)

    # the second element (cisco) is the enable command
    # commands = ['enable', 'cisco123', 'conf t', 'username admin2 secret cisco123', 'access-list 1 permit any', 'end',
    #             'terminal length 0', 'sh run | i user']
    
    # send_from_list(shell, commands)

    # send_command(shell, 'sh version')
    # send_command(shell, 'sh ip int brief')

    send_from_file(shell, 'commands.txt')

    output = show(shell)
    print(output)

    close(client)

    
