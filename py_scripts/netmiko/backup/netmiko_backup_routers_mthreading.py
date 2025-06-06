from netmiko import ConnectHandler
import time
import threading

start = time.time()

def backup(router):
    connection = ConnectHandler(**router)
    print('Entering enable mode...')
    connection.enable()

    output = connection.send_command('show run')
    prompt = connection.find_prompt()
    hostname = prompt[:-1]

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    filename = f'{hostname}_{year}-{month}-{day}-{hour}-{minute}_backup.txt'

    with open(filename, 'w') as file:
        file.write(output)
        print(f'Backup file of {hostname} created successfully: {filename}')
    
    print('Closing connection...')
    connection.disconnect()

    print('#' * 50 + '\n')

with open('devices_ip.txt') as file:
    devices = file.read().splitlines()

threads = list()
for ip in devices:
    cisco_router = {
        'host': ip,
        'username': 'admin',
        'password': 'cisco123',
        'device_type': 'cisco_ios',
        'port': 22,                    #optional, default 22
        'secret': 'cisco123',          #optional, default ''
        'verbose': True                #optional, default False
    }

    thread = threading.Thread(target=backup, args=(cisco_router,))
    threads.append(thread)
    
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


end = time.time()
print(f"Total execution time: {end - start}")
