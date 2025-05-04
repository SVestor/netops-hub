from netmiko import ConnectHandler
from netmiko import file_transfer

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

print(file_transfer(connection, source_file='test.txt', dest_file='test.txt',
                    file_system='disk0:', direction='put', overwrite_file=True))

print('\nClosing connection...')
connection.disconnect()
