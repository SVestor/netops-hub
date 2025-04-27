import ref_paramiko
import threading

# implementing multithreading for multiple devices

def backup(router):
    client = ref_paramiko.connect(**router)
    shell = ref_paramiko.get_shell(client)

    ref_paramiko.send_command(shell, 'term len 0')
    ref_paramiko.send_command(shell, 'enable')
    ref_paramiko.send_command(shell, 'cisco123')
    ref_paramiko.send_command(shell, 'sh running-config')

    output = ref_paramiko.show(shell)
    # print(output)

    output_list = output.splitlines()
    output_list = output_list[21:-1]
    # print(output_list)

    output_str = '\n'.join(output_list)
    # print(output_str)

    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    file_name = f"{router['server_ip']}_{year}-{month}-{day}-{hour}-{minute}.txt"
    print(f"Backup file name: {file_name}")

    with open(file_name, 'w') as file:
        file.write(output_str)

    ref_paramiko.close(client)

router1 = {
    'server_ip': '192.168.224.11',
    'server_port': 22,
    'username': 'admin',
    'password': 'cisco123'
}
router2 = {
    'server_ip': '192.168.224.12',
    'server_port': 22,
    'username': 'admin',
    'password': 'cisco123'
}

router3 = {
    'server_ip': '192.168.224.13',
    'server_port': 22,
    'username': 'admin',
    'password': 'cisco123'
}

routers = [router1, router2, router3]

threads = list()
for router in routers:
    thread = threading.Thread(target=backup, args=(router,))
    threads.append(thread)
    
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


