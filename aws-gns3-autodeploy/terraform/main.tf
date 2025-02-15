# Configure the AWS Provider
provider "aws" {
  profile = "cloud-user"
  region  = "us-east-1"

  default_tags {
    tags = {
      Environment = terraform.workspace
      Owner       = "net-admin"
      Project     = "IaC-automation"
      Terraform   = "true"
    }
  }
}

#Retrieve the list of AZs in the current AWS region
data "aws_availability_zones" "available" {}
data "aws_region" "current" {}

locals {
  var_obj      = { for indx, new_obj in var.env.dev : "${var.env.dev[indx].env}-${indx}" => new_obj }
  region       = data.aws_region.current.name
  env          = terraform.workspace
  team         = "sv-team"
  application  = "gns3-server"
  service_name = "Automation"
  app_team     = "GNS3 Team"
  project      = "IaC-automation"
  createdby    = "terraform"
  terraform    = "true"
}

locals {
  # Common tags to be assigned to all resources
  common_tags = {
    Project     = lower(local.project)
    Environment = lower(local.env)
    Owner       = lower(local.team)
    App         = lower(local.application)
    Service     = lower(local.service_name)
    AppTeam     = lower(local.app_team)
    CreatedBy   = lower(local.createdby)
    Region      = lower(local.region)
    Terraform   = lower(local.terraform)
  }
}

#Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = var.vpc_name
    Environment = local.env
    Terraform   = local.terraform
    Region      = local.region
  }
}

#Deploy the public subnets
resource "aws_subnet" "gns_subnets" {
  vpc_id            = aws_vpc.vpc.id
  for_each          = local.var_obj
  cidr_block        = each.value.ip
  availability_zone = each.value.az

  tags = {
    Name        = "${each.key}"
    Environment = "${each.value.env}"
    Terraform   = local.terraform
  }
}

#Create route tables for public and private subnets
resource "aws_route_table" "gns_public_rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
    #nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name      = "gns_public_rtb"
    Terraform = local.terraform
  }
}

#Create route table associations
resource "aws_route_table_association" "gns_public" {
  route_table_id = aws_route_table.gns_public_rtb.id
  for_each       = aws_subnet.gns_subnets
  subnet_id      = each.value.id
}

#Create Internet Gateway
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name      = "gns_igw"
    Terraform = local.terraform
  }
}

# Terraform Data Block - To Lookup Latest Ubuntu 20.04 AMI Image
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20240927"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

resource "tls_private_key" "generated" {
  algorithm = "RSA"
}

resource "local_file" "private_key_pem" {
  content         = tls_private_key.generated.private_key_pem
  filename        = "MyAWSkey.pem"
  file_permission = "0400"
}

resource "aws_key_pair" "generated" {
  key_name   = "MyAWSkey"
  public_key = tls_private_key.generated.public_key_openssh

  lifecycle {
    ignore_changes = [key_name]
  }
}

# Security Groups

resource "aws_security_group" "ingress-ssh" {
  name   = "allow-all-ssh-${local.env}"
  vpc_id = aws_vpc.vpc.id
  ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
  }
  // Terraform removes the default rule
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create Security Group - Web Traffic
resource "aws_security_group" "vpc-web" {
  name        = "vpc-web-${local.env}"
  vpc_id      = aws_vpc.vpc.id
  description = "Web Traffic"

  ingress {
    description = "Allow Port 80"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow Port 443"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow Port 8003 for OpenVPN .opvn"
    from_port   = 8003
    to_port     = 8003
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow UDP traffic for OpenVpn"
    from_port   = 1194
    to_port     = 1194
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow TCP traffic for OpenVpn"
    from_port   = 1194
    to_port     = 1194
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all ip and ports outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "vpc-ping" {
  name        = "vpc-ping-${local.env}"
  vpc_id      = aws_vpc.vpc.id
  description = "ICMP for Ping Access"
  ingress {
    description = "Allow ICMP Traffic"
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all ip and ports outboun"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Terraform Resource Block - To Build EC2 instance in Public Subnet
resource "aws_instance" "gns3_server" {
  for_each      = local.var_obj
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  subnet_id     = aws_subnet.gns_subnets[each.key].id

  root_block_device {
    volume_size = 40
    volume_type = "gp3"
  }

  security_groups = [
    aws_security_group.ingress-ssh.id,
    aws_security_group.vpc-web.id,
    aws_security_group.vpc-ping.id
  ]
  associate_public_ip_address = true
  key_name                    = aws_key_pair.generated.key_name

  tags = merge({ Name = join("-", [local.application, each.key, each.value.az, local.createdby]) }, local.common_tags) # Merge local.common_tags


  lifecycle {
    ignore_changes = [security_groups]
  }
}

# Will wait 75 seconds for the instance to be created
resource "time_sleep" "wait_75_seconds" {
  for_each        = aws_instance.gns3_server
  create_duration = "75s"
  depends_on      = [aws_instance.gns3_server]
}

# Install GNS3 Server
resource "null_resource" "install_gns3" {
  for_each = aws_instance.gns3_server
  connection {
    timeout     = "1m"
    user        = "ubuntu"
    private_key = tls_private_key.generated.private_key_pem
    host        = aws_instance.gns3_server[each.key].public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo -s cd /tmp",
      "sudo -s curl https://raw.githubusercontent.com/GNS3/gns3-server/master/scripts/remote-install.sh > gns3-remote-install.sh",
      "sudo -s bash gns3-remote-install.sh --with-openvpn --with-iou --with-i386-repository",
    ]
  }

  depends_on = [time_sleep.wait_75_seconds]

}

# Update files with actual content and server restart
resource "null_resource" "restart_server" {
  for_each = aws_instance.gns3_server

  provisioner "local-exec" {
    command = <<-EOT
      scp -o StrictHostKeyChecking=no -i ${local_file.private_key_pem.filename} ubuntu@${aws_instance.gns3_server[each.key].public_ip}:/etc/update-motd.d/70-openvpn ./vpn_info_content-${each.key}.txt &&
      echo "" > ./vpn_url_content-${each.key}.txt &&
      echo "Alert! GNS3 Server will be restarted in 3 minutes and all critical services will be disabled." >> ./vpn_url_content-${each.key}.txt &&
      echo -e "Download the VPN configuration here:" >> ./vpn_url_content-${each.key}.txt &&
      grep -o 'http.*' vpn_info_content-${each.key}.txt | sed 's/\"$//' >> ./vpn_url_content-${each.key}.txt &&
      echo "If the VPN works, this page should work: http://172.16.253.1:3080/" >> ./vpn_url_content-${each.key}.txt
    EOT
  }

  provisioner "remote-exec" {
    inline = [
      <<-EOT
      cat <<EOF | sudo tee /etc/netplan/50-v-gns-bridge.yaml
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
      EOF
      EOT
      ,
      "sudo bash -c 'chmod u=rw,g=,o= /etc/netplan/50-v-gns-bridge.yaml'",
      "sudo netplan apply",
      "sudo -i bash -c 'echo \"enable_kvm = false\" >> /etc/gns3/gns3_server.conf'",
      "nohup sudo -s bash -c 'sleep 170s && apt remove nginx-light -y' > /dev/null 2>&1 &", # Redirect output to /dev/null and use && for proper sequencing, removes nginx-light after 5 minutes in the background, even if the session is closed
      "sudo -s shutdown -r +3 'Restarting in 3 minutes'",
    ]
  }

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.generated.private_key_pem
    host        = aws_instance.gns3_server[each.key].public_ip
  }

  triggers = {
    instance_id = aws_instance.gns3_server[each.key].id
    first_boot  = "true" # Will be true on first run
    # content_hash = fileexists("${path.module}/vpn_info_content.txt") ? filemd5("${path.module}/vpn_info_content.txt") : "none"
    #time         = timestamp()
  }

  depends_on = [null_resource.install_gns3]
}

# Read file contents after they are created
data "local_file" "vpn_url" {
  for_each   = aws_instance.gns3_server
  filename   = "${path.module}/vpn_url_content-${each.key}.txt"
  depends_on = [null_resource.restart_server]
}

data "local_file" "vpn_info" {
  for_each   = aws_instance.gns3_server
  filename   = "${path.module}/vpn_info_content-${each.key}.txt"
  depends_on = [null_resource.restart_server]
}


/* data "external" "gns3_info" {
  program = ["bash", "-c", <<EOT
    key_file=$(mktemp)
    echo "${tls_private_key.generated.private_key_pem}" > $key_file
    chmod 400 $key_file
    ssh -o StrictHostKeyChecking=no -i $key_file ubuntu@${aws_instance.gns3_server.public_ip} "cat /etc/update-motd.d/70-openvpn | jq -Rs '{gns3_info: .}'"
    rm -f $key_file
  EOT
  ]

  depends_on = [ aws_instance.gns3_server ]
} */

/* # Create EBS Volume
resource "aws_ebs_volume" "ebs_volume" {
  availability_zone = aws_instance.gns3_server.availability_zone
  size              = 40
  tags = {
    Name = "demo_ebs"
  }
}

# Attach EBS Volume
resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.ebs_volume.id
  instance_id = aws_instance.gns3_server.id
}
 */

/* triggers = {
    vpn_url_content  = fileexists("${path.module}/vpn_url_content.txt") ? file("${path.module}/vpn_url_content.txt") : "File not created yet"
    vpn_info_content = fileexists("${path.module}/vpn_info_content.txt") ? file("${path.module}/vpn_info_content.txt") : "File not created yet"
    time = timestamp()
    content_hash = fileexists("${path.module}/vpn_info_content.txt") ? filemd5("${path.module}/vpn_info_content.txt") : "none"
  } */
