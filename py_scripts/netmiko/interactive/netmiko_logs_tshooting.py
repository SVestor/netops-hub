from netmiko import ConnectHandler
import logging
import time

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger('netmiko')
logger.disabled = True

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
# output = connection.send_command('sh version')
# print(output)

# instead of using send_command we can use a low level methods to move step by step
connection.write_channel('sh version\n')
time.sleep(2)
output = connection.read_channel()
print(output)

connection.write_channel('en\n')
connection.write_channel('cisco123\n')
time.sleep(2)
output = connection.read_channel()
print(output)

connection.write_channel('sh run\n')
time.sleep(2)
output = connection.read_channel()
print(output)

print('\nClosing connection...')
connection.disconnect()
