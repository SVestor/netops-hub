import ref_paramiko

client = ref_paramiko.connect('192.168.224.110', '22', 'admin', 'linux123')
shell = ref_paramiko.get_shell(client)

ref_paramiko.send_command(shell, 'uname -a')
ref_paramiko.send_command(shell, 'cat /etc/shadow')

cmd = 'sudo groupadd devs'
ref_paramiko.send_command(shell, cmd)
ref_paramiko.send_command(shell, 'sudo123', 2)

ref_paramiko.show(shell) # flashing a buffer to get latest output
ref_paramiko.send_command(shell, 'tail -n 1 /etc/group')

output = ref_paramiko.show(shell)
print(output)

ref_paramiko.close(client)
