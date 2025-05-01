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
prompt = connection.find_prompt()
# print(prompt)

if '>' in prompt:
    connection.enable()

# prompt = connection.find_prompt()
# print(prompt)

# output = connection.send_command('show ip int brief')
output = connection.send_command('sh run')
print(output)

if not connection.check_config_mode():  # checking if in global config mode
    connection.config_mode()
    print('In global config mode')

print(connection.check_config_mode())

connection.send_command('username admin3 secret cisco123')

output = connection.send_command('do sh run | i username')
print(output)

connection.exit_config_mode()
print(connection.check_config_mode())

print('\nClosing connection...')
connection.disconnect()
