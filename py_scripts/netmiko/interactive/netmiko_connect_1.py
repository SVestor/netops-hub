from netmiko import Netmiko

connection = Netmiko(
    host='192.168.224.11',
    username='admin',
    password='cisco123',
    device_type='cisco_ios',
)

output = connection.send_command('show ip int brief')
print(output)

print('\nClosing connection...')
connection.disconnect()

