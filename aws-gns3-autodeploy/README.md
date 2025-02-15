# GNS3 Server Deployment in AWS Cloud

This repository provides the necessary configurations and steps to deploy a GNS3 Server in the AWS Cloud, including connectivity with a local/home network and essential network configurations.

## Prerequisites

- An AWS account
- Terraform installed
- Basic networking knowledge

## Installation Steps

### 1. Deploy GNS3 Server with Terraform

Terraform is used to automate the deployment of the GNS3 Server instance, SSH key and all the network and infrastructural components.

1. Clone this repository:
   ```bash
   git clone https://github.com/SVestor/netops-hub.git
   cd ./netops-hub/aws-gns3-autodeploy/terraform
   ```
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Plan and apply the deployment:
   ```bash
   terraform plan
   terraform apply -auto-approve
   ```
4. After deployment, note the public and private IPs assigned to your GNS3 Server.

### 2. Configure Network Connectivity

To allow your local/home network to communicate with GNS3 networks, run the following command on your local machine (Windows example):

```bash
route -p add 192.168.224.0 mask 255.255.255.0 172.16.253.5 metric 256 if 13
route print
route delete -p add 192.168.224.0 mask 255.255.255.0 172.16.253.5 metric 256 if 13 # use this command to remove the route
```

Ensure Windows Defender allows ICMP inbound traffic from GNS3 Server networks.

For Example:
On the host/windows defender stateful firewall add the inbound rule that allows ICMP traffic to the windows host from remote GNS Server networks: 172.16.253.0/24 and 192.168.224.0/24 , you're going to communicate with form the host or VMs also if your host is used like a hypervisor etc

```powershell
netsh advfirewall firewall add rule name="Allow ICMP from GNS3 Server" dir=in action=allow protocol=icmpv4 remoteip=172.16.253.0/24, 192.168.224.0/24
```

### 3. Configure Cisco Router

Inside GNS3, configure a Cisco router with the following settings:

```bash
en
conf t
line 0 
logging synchronous
host R1
int g0/0
ip address 192.168.224.11 255.255.255.0
no shut
do sh ip int br
ip route 172.16.253.0 255.255.255.0 192.168.224.254
do sh ip route
do wr
```
## The following configurations is not required for the specific operational pattern, it's already hardcoded into the terraform main.tf file

### 1. Set Up GNS3 Server Networking

On the GNS3 Server, create a bridge for network connectivity:

```bash
sudo ip link add v-gns-net-0 type bridge    # create a virtual bridge / switch
sudo ip link set dev v-gns-net-0 up
sudo ip addr add 192.168.224.254/24 dev v-gns-net-0
```

To make these changes persistent, add them to Netplan:

```yaml
/etc/netplan/50-v-gns-bridge.yaml:
network:
  version: 2
  renderer: networkd
  # If you have physical interfaces that should be part of the bridge, specify them in interfaces:
  # ethernets:
  #   ens5:
  #     dhcp4: true
  bridges:
    v-gns-net-0:
      interfaces: []    # If the bridge does not include any physical interfaces, leave it empty
      addresses:
        - 192.168.224.254/24
      dhcp4: no
      parameters:
        stp: false
        forward-delay: 0
```

Apply the changes:

```bash
sudo chmod u=rw,g=,o= /etc/netplan/50-v-gns-bridge.yaml
sudo netplan apply
```

Test it on a server:

```bash
ssh -i MyAWSkey.pem ubuntu@192.168.224.254

ip route show
ip link
ip a 
```

### 2. These are merely some useful commands provided for general comprehension

### Debugging and Testing

- Verify connectivity:
  ```bash
  ping 192.168.224.254
  traceroute 172.16.253.6
  sudo tcpdump -i v-gns-net-0 icmp # catching/debugging icmp traffic on GNS Server on v-gns-net-0 device
  ```
- Check routing tables:
  ```bash
  ip route show
  ```
- Debug Cisco ICMP traffic:
  ```bash
  debug ip icmp
  ```
- Show metric on Windows for all interfaces:
  ```powershell
  tracert 192.168.224.11
  netsh interface ipv4 show interfaces
  netsh interface ipv4 set interface "TAP-Windows Adapter V9 #2" metric=5 # set metric value // don't do that , just FYI
  ```  

### IPTables firewall useful commands

```bash
sudo sysctl net.ipv4.ip_forward  # check if packet forwading btw interfaces is enabled on the GNS Server, must be = 1 // source/destionation check 
cat /proc/sys/net/ipv4/ip_forward # repeats the previous command 
sudo sysctl -w net.ipv4.ip_forward=1  # enable forwarding if the value=0

echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf  # enable IP forwarding to save it permanently
sudo sysctl -p

sudo iptables-save > /etc/iptables/rules.v4 # repeats the previous command

# to save rules after reboot, it is recommended to use iptables-save and iptables-restore, or install the iptables-persistent or netfilter-persistent package
sudo apt install netfilter-persistent  OR sudo apt install iptables-persistent
sudo netfilter-persistent save # netfilter-persistent automatically saves and restores rules on reboot

# check iptables rules
sudo iptables -L
sudo iptables -L -v -n
sudo iptables -t nat -L -v -n
sudo iptables -t nat -L POSTROUTING

# it allows server to change the source ip to the dev's interface ip 
sudo iptables -t nat -A POSTROUTING -s <ip adress/net adress>/cidr -o dev -j MASQUERADE 

# just an example don't do that:
sudo iptables -t nat -A POSTROUTING -s 172.16.253.0/24 -o some-vr-br0 -j MASQUERADE  # add the rule 
sudo iptables -t nat -D POSTROUTING -s 172.16.253.0/24 -o some-vr-br0 -j MASQUERADE  # delete the rule
sudo iptables -t nat -D POSTROUTING 1 # delete the rule by its number

# to allow traffic
sudo iptables -A INPUT -i tun1194 -j ACCEPT
sudo iptables -A FORWARD -i tun1194 -j ACCEPT
sudo iptables -A OUTPUT -o tun1194 -j ACCEPT

# allows traffic forwarding btw devices/interfaces
sudo iptables -A FORWARD -i tun1194 -o some-vr-br0 -j ACCEPT
sudo iptables -A FORWARD -i some-vr-br0 -o tun1194 -j ACCEPT

# temporary disables iptables firewall
sudo iptables -F
sudo iptables -t nat -F

sudo ufw status
sudo ufw status verbose # if ufw is used
sudo ufw allow from 172.16.253.0/24 to 192.168.224.0/24 # just an example 
sudo ufw disable
```
### Virtual link/Virtual cable and Bridges
```bash
# create a virtual link/cable with the veth-gnet interface
sudo ip link add veth-gnet type veth peer name veth-gnet-br

# connect one side to the virtual bridge 
sudo ip link set veth-gnet-br master v-gns-net-0

# assign the ip address to the interface
sudo ip addr add 192.168.224.10/24 dev veth-gnet
sudo ip link set veth-gnet up

# delete the link and its peer / both sides of the link
sudo ip link del veth-gnet 
```

## Cleanup

To destroy the AWS deployment, run:
```bash
terraform destroy -auto-approve
```

## License

MIT License

