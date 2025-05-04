# 🚀 Deploying GNS3 Server in AWS with Terraform

This configuration involves deploying a **GNS3 Server** in **AWS Cloud** along with the necessary infrastructure using **Terraform**. Below are the steps and commands required to set up networking between your local/home network and the GNS3 environment.

## Prerequisites

- An AWS account
- Terraform installed
- Basic networking knowledge

---

## ⚙️ Installation Steps

### 🌌 Deploy GNS3 Server with Terraform

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

---

### 🌍 Connecting Your Local Network to GNS3 

To establish connectivity between your **local/home network** and the networks in **GNS3**, execute the following commands on the **host OS (Windows)**:

```bash
# Add a persistent route to reach the GNS3 networks
route -p add 192.168.224.0 mask 255.255.255.0 172.16.253.5 metric 256 if 13

# Verify the configured routes
route print

# Remove the previously added route if necessary
route delete -p add 192.168.224.0 mask 255.255.255.0 172.16.253.5 metric 256 if 13
```

Additionally, configure **Windows Defender Firewall** to allow **ICMP traffic** from remote **GNS3 server networks** (`172.16.253.0/24` and `192.168.224.0/24`). This will enable communication between the host, virtual machines (VMs), or other devices using the host as a hypervisor. 

```powershell
netsh advfirewall firewall add rule name="Allow ICMP from GNS3 Server" dir=in action=allow protocol=icmpv4 remoteip=172.16.253.0/24, 192.168.224.0/24
```
---

### 🚃 Cisco Router Configuration

Execute the following commands on a **Cisco router** to integrate it with the GNS3 network:

```bash
en
conf t
line 0 
logging synchronous
exit
enable secret cisco123
username admin secret cisco123
host R1
ip domain-name mydomain.local
crypto key generate rsa modulus 2048
ip ssh version 2
line vty 0 4
transport input ssh
exec-timeout 20 0
login local
exit
int g0/1
ip address 192.168.224.11 255.255.255.0
no shut
do sh ip int br
ip route 172.16.253.0 255.255.255.0 192.168.224.254
do sh ip route
do show crypto key mypubkey rsa
do wr
```
---

## 📡 GNS3 Server Configuration (Manual Setup)

The following configuration is already **hardcoded** in Terraform (`main.tf`) and is **not required** unless performing a **manual setup**:

On the GNS3 Server, create a bridge for network connectivity:

```bash
# Create a virtual bridge (switch)
sudo ip link add v-gns-net-0 type bridge 
sudo ip link set dev v-gns-net-0 up
sudo ip addr add 192.168.224.254/24 dev v-gns-net-0
```

To make these settings **persistent**, use **Netplan**: 

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

Apply the configuration: 

```bash
sudo chmod u=rw,g=,o= /etc/netplan/50-v-gns-bridge.yaml
sudo netplan apply
```

### ✅ Test the GNS3 Server Connectivity  

```bash
ssh -i MyAWSkey.pem ubuntu@192.168.224.254

ip route show
ip link
ip a 
```
---

## 📝 These are merely some useful commands provided for general comprehension

### 🔎 Network Debugging and Testing

- Verify connectivity:
  ```bash
  ping 192.168.224.254              # Basic connectivity test
  traceroute 172.16.253.6           # On Linux
  tracert 172.16.253.6              # On Windows
  sudo tcpdump -i v-gns-net-0 icmp  # Capture/debug ICMP traffic on GNS3 server
  ```
- Check routing tables:
  ```bash
  ip route show
  ```
- Debug ICMP traffic on Cisco devices:
  ```bash
  debug ip icmp 
  ```
### 🖥 Windows Interface Metrics 
  ```powershell
  # Show metrics for all interfaces
  netsh interface ipv4 show interfaces

   # Set metric value (for reference)
  netsh interface ipv4 set interface "TAP-Windows Adapter V9 #2" metric=5 
  ```
  ---

## 🔥 Firewall & IP Forwarding

### Enabling IP Forwarding

```bash
# Check if packet forwarding is enabled (should be = 1) // source/destionation check
sudo sysctl net.ipv4.ip_forward
cat /proc/sys/net/ipv4/ip_forward # Alternative check

# Enable forwarding if disabled
sudo sysctl -w net.ipv4.ip_forward=1

# Persist the setting
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

sudo iptables-save > /etc/iptables/rules.v4 # Alternative way to save rules

# To save rules after reboot, it is recommended to use iptables-save and iptables-restore, or install the iptables-persistent or netfilter-persistent package
sudo apt install netfilter-persistent  OR sudo apt install iptables-persistent

# netfilter-persistent automatically saves and restores rules on reboot
sudo netfilter-persistent save
```
### Managing `iptables` Rules

```bash
sudo iptables -L                         # View iptables rules
sudo iptables -L -v -n                   # View detailed iptables rules
sudo iptables -t nat -L -v -n            # View NAT rules
sudo iptables -t nat -L POSTROUTING      # View NAT rules for POSTROUTING chain
```
Example rule for **MASQUERADE** (NAT):

```bash
# It allows server to change the source ip to the dev's interface ip 
sudo iptables -t nat -A POSTROUTING -s <ip adress/net adress>/cidr -o dev -j MASQUERADE 

# Just an example:
sudo iptables -t nat -A POSTROUTING -s 172.16.253.0/24 -o some-vr-br0 -j MASQUERADE  # add the rule 
```
To delete the rule:

```bash
sudo iptables -t nat -D POSTROUTING -s 172.16.253.0/24 -o some-vr-br0 -j MASQUERADE  # delete the rule
sudo iptables -t nat -D POSTROUTING 1                                                # delete by rule number
```
### Allowing Traffic and Forwarding

```bash
# To allow traffic
sudo iptables -A INPUT -i tun1194 -j ACCEPT
sudo iptables -A FORWARD -i tun1194 -j ACCEPT
sudo iptables -A OUTPUT -o tun1194 -j ACCEPT

# Allows traffic forwarding btw devices/interfaces
sudo iptables -A FORWARD -i tun1194 -o some-vr-br0 -j ACCEPT
sudo iptables -A FORWARD -i some-vr-br0 -o tun1194 -j ACCEPT
```
To **disable** `iptables` temporarily:

```bash
# Temporary disables iptables firewall
sudo iptables -F
sudo iptables -t nat -F
```

---

## 🛠️ `UFW` (Uncomplicated Firewall)

```bash
sudo ufw status
sudo ufw status verbose 
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 172.16.253.0/24 to 192.168.224.0/24 # Allow traffic between networks 
sudo ufw disable
```

---

## 🏗️ Creating Virtual Network Links

```bash
# Create a virtual link (veth pair) with the veth-gnet interface
sudo ip link add veth-gnet type veth peer name veth-gnet-br

# Attach one end to the bridge 
sudo ip link set veth-gnet-br master v-gns-net-0

# Assign an IP address
sudo ip addr add 192.168.224.10/24 dev veth-gnet
sudo ip link set veth-gnet up

# Delete the virtual link // both sides of the link
sudo ip link del veth-gnet 
```

---

## 🌞 Cleanup

To destroy the AWS deployment, run:
```bash
terraform destroy -auto-approve
```

---

## 🎯 Summary  

This guide provides a comprehensive setup for deploying and configuring **GNS3 in AWS Cloud** using **Terraform** while ensuring **seamless network integration** with local/home environments. The provided configurations cover:  

- **Networking setup** (routes, firewall rules, and interfaces)  
- **Cisco router integration**  
- **GNS3 Server manual configuration**  
- **Debugging tools and commands**  

💡 **Tip:** The Terraform script already **automates** most of these configurations, so manual Windows setup is only needed for debugging or custom adjustments.  

---

## 📜 License  

This project is licensed under the **MIT License**. Feel free to use and modify as needed.  

---

🚀 **Happy networking!**


