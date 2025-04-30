import ref_paramiko_v2
import threading

router1 = {
        'server_ip': '192.168.224.11',
        'server_port': 22,
        'username': 'admin',
        'password': 'cisco123',
        'config': 'ospf.txt'
    }

router2 = {
        'server_ip': '192.168.224.12',
        'server_port': 22,
        'username': 'admin',
        'password': 'cisco123',
        'config': 'eigrp.txt'
    }

router3 = {
        'server_ip': '192.168.224.13',
        'server_port': 22,
        'username': 'admin',
        'password': 'cisco123',
        'config': 'bgp.txt'
    }

routers = [router1, router2, router3]

threads = list()
for router in routers:
    thread = threading.Thread(target=ref_paramiko_v2.target_function, args=(router,))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# for router in routers:
#     ssh_client = ref_paramiko_v2.connect(server_ip=router['server_ip'], server_port=router['server_port'], username=router['username'], password=router['password'])
#     shell = ref_paramiko_v2.get_shell(ssh_client)
#     ref_paramiko_v2.send_from_file(shell, router['config'])

#     output = ref_paramiko_v2.show(shell)
#     print(output)
#     print('#' * 50)

# ref_paramiko_v2.close(ssh_client)
    
    
