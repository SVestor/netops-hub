from netmiko import ConnectHandler

with open('devices_ip.txt') as file:
    devices = file.read().splitlines()

router_list = list()
for ip in devices:
    cisco_router = {
        'host': ip,
        'username': 'admin',
        'password': 'cisco123',
        'device_type': 'cisco_ios',
        'port': 22,
        'secret': 'cisco123',
        'verbose': True
    }
    router_list.append(cisco_router)

for router in router_list:
    connection = ConnectHandler(**router)

    print('Entering enable mode ...')
    connection.enable()

    file = input(f'Enter a configuration file for {router["host"]}: ')

    print(f'\nSending configuration from {file} to {router["host"]}...')
    print(connection.send_config_from_file(file))

    print(f'\nSaving configuration on {router["host"]}...')
    connection.send_command('wr')

    print(f'\nClosing connection to {router["host"]}...')
    connection.disconnect()

    print('#' * 50)
    
    
    


    
