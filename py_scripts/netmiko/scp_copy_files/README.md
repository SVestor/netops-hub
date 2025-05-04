### 🚃 Cisco Router Configuration

As an example, let's configure a Cisco router to use SCP to copy files from a remote device. (Cisco C7200-152-4S5: 192.168.224.11)

Before executing the commands below, add PCMCIA disk0 (32MiB for example) to the router.

Execute the following commands on a **Cisco router** to enable SCP and SSH:

```bash
en
dir all-filesystems
format disk0:
conf t
host R1
user admin privilege 15 secret cisco123
ip domain-name mydomain.internal
crypto key generate rsa modulus 2048
ip ssh version 2
line vty 0 1869
transport input telnet ssh 
exec-timeout 20 0
login local
exit
int g1/0
ip address 192.168.224.11 255.255.255.0
no shut
do sh ip int br
ip route 172.16.253.0 255.255.255.0 192.168.224.254
do sh ip route
do show crypto key mypubkey rsa
# enabling SCP server on the router
ip scp server enable
aaa new-model
aaa authentication login default local
aaa authorization exec default local none
do wr
dir disk0:
```
---

🚀 **Happy networking!**
