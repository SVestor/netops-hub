variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_name" {
  type    = string
  default = "gns3_vpc"
}

variable "vpc_cidr" {
  type    = string
  default = "10.110.0.0/16"
}

variable "env" {
  type = map(any)
  default = {
    prod = [
      {
        ip  = "10.110.120.0/24"
        az  = "us-east-1a"
        env = "prod"
      }
    ]
    dev = [
      {
        ip  = "10.110.220.0/24"
        az  = "us-east-1c"
        env = "dev"
      }
    ]
  }
}






