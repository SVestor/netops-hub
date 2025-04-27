import paramiko
from scp import SCPClient
import getpass

password = getpass.getpass('Enter password: ')

linux_vm1 = {
    'hostname': '192.168.224.254',
    'port': 22,
    'username': 'ubuntu',
    'password': password
}

ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect(**linux_vm1, look_for_keys=False, allow_agent=False)

scp = SCPClient(ssh_client.get_transport())

# copy a single file to the remote location
scp.put('test.txt', 'remote_text.txt')

# copy a directory to the remote location
scp.put('test_dir', recursive=True, remote_path='/tmp/remote_dir')

# copy a single file from the remote location
scp.get('/etc/passwd', '/home/ubuntu/passwd.txt')

# copy a directory from the remote location
scp.get('remote_dir', '/home/ubuntu/remote_dir', recursive=True)

scp.close()

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()



