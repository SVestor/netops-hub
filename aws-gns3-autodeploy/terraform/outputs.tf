output "vpc_information" {
  description = "VPC Information about Environment"
  value       = "Your ${aws_vpc.vpc.tags.Environment} VPC has an ID of ${aws_vpc.vpc.id}"
}

output "public_ip_gns3_server" {
  value = { for key, value in aws_instance.gns3_server : key => value.public_ip if value.public_ip != null }
}

output "public_dns_gns3_server" {
  value = { for key, value in aws_instance.gns3_server : key => value.public_dns }
}

output "public_url_gns3_server" {
  description = "Public URL for our Web Server"
  value       = { for key, value in aws_instance.gns3_server : key => "http://${value.public_ip}:80/index.html" }
}

output "vpn_url_content" {
  value       = { for key, value in aws_instance.gns3_server : key => data.local_file.vpn_url[key].content }
  description = "The content of the OpenVPN URL file."
}

/* output "vpn_info_content" {
  value       = { for key, value in aws_instance.gns3_server : key => data.local_file.vpn_info[key].content }
  description = "The content of the VPN information file."
} */

/* output "vpn_information" {
  value = fileexists("${path.module}/vpn_url.txt") ? file("${path.module}/vpn_url.txt") : null
} */

/* output "gns3_configuration_info" {
  value = data.external.gns3_info.result["gns3_info"]
} */
