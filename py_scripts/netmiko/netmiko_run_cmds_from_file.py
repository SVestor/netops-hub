from netmiko import ConnectHandler

cisco_router = {
    'host': '192.168.224.11',
    'username': 'admin',
    'password': 'cisco123',
    'device_type': 'cisco_ios',
    'port': 22,                    #optional, default 22
    'secret': 'cisco123',          #optional, default ''
    'verbose': True                #optional, default False
}

connection = ConnectHandler(**cisco_router)
print('Entering enable mode...')
connection.enable()

print('Sending configuration commands from file...')
connection.send_config_from_file('ospf.txt')

print('Saving configuration...')
connection.send_command('wr')

print('Verifying configuration...\n')
output = connection.send_command('show run | section ospf')
print(output)

print('\nClosing connection...')
connection.disconnect()
