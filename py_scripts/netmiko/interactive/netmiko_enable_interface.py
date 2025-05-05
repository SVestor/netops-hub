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

interface = input('Enter the interface you want to be enabled: ')
output = connection.send_command(f'sh ip interface {interface}')
# print(output)

if 'Invalid input detected' in output or 'Incomplete command' in output:
    print('Invalid interface name')
else:
    first_line = output.splitlines()[0]
    print(first_line)
    if 'administratively down' in first_line:
        print(f'Interface {interface} is down. Enabling it...')
        commands = ['interface ' + interface, 'no shutdown', 'do wr', 'exit']
        output = connection.send_config_set(commands)
        # print(output)
        print(f'Interface {interface} enabled successfully')
    else:
        print(f'Interface {interface} is up')

print('\nClosing connection...')
connection.disconnect()
