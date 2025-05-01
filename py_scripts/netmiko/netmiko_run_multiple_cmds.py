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

# commands = ['int loopback 0', 'ip address 1.1.1.1 255.255.255.255', 'exit', 'username user1 secret cisco']
# instead of declaring commands as a list, we can also use ';' as a separator for example
# commands = 'int loopback 1; ip address 1.1.1.2 255.255.255.255; exit; username user2 secret cisco'
# or we can use the following presentation with an '\n' as a separator
commands = '''
int loopback 2
ip address 2.2.2.2 255.255.255.255
exit
access-list 100 permit any
username user3 secret cisco
'''
connection.send_config_set(commands.split('\n')) # enter automatically into the global config mode before starting send commands

print(connection.find_prompt())

connection.send_command('wr')
output = connection.send_command('show run | i username')
print(output)

print('\nClosing connection...')
connection.disconnect()
