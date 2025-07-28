with open('mac.txt', 'r') as file:
    content = file.read().split()
    # print(content)

    # Remove duplicates
    content = list(set(content))
    print(content)

with open('mac_unique.txt', 'w', newline='') as file:
    for mac in content:
        file.write(f'{mac}\n')

