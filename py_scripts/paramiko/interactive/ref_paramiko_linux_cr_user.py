import ref_paramiko
import getpass

username = input('Enter username: ')
password = getpass.getpass('Enter password: ')

linux_vm = {
    'server_ip': '192.168.224.254',
    'server_port': 22,
    'username': username,
    'password': password
}

ssh_client = ref_paramiko.connect(**linux_vm)
shell = ref_paramiko.get_shell(ssh_client)

new_user = input('Enter the username you want to create: ')
command = f"sudo useradd -m -d /home/{new_user} -s /bin/bash {new_user}"
ref_paramiko.send_command(shell, command)
ref_paramiko.send_command(shell, password)
print(f"User {new_user} created successfully")

ref_paramiko.show(shell)

answer = input('Do you want to display the user list? (y/n): ')
if answer.lower() == 'y':
    ref_paramiko.send_command(shell, 'cat /etc/passwd')
    ref_paramiko.show(shell)

ref_paramiko.close(ssh_client)


