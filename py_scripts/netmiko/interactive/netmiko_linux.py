from netmiko import ConnectHandler

linux = {
    'host': '192.168.224.254',
    'username': 'admin',
    'password': 'linux123',
    'device_type': 'linux',
    'port': 22,                              # optional, default 22
    'secret': 'somestrongpassword',          # sudo password
    'verbose': True                          # optional, default False
}

connection = ConnectHandler(**linux)

connection.enable() # sudo su
connection.send_command('apt update && apt install -y apache2')

print(connection.send_command('systemctl status apache2'))

print('\nClosing connection...')
connection.disconnect()

