terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.6"
    }

    random = {
      source  = "hashicorp/random"
      version = ">=3.6.1"
    }

    http = {
      source  = "hashicorp/http"
      version = "3.4.5"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.5.2"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "4.0.6"
    }

    external = {
      source  = "hashicorp/external"
      version = "2.3.4"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.2.3"
    }

    time = {
      source  = "hashicorp/time"
      version = "0.12.1"
    }
  }
}
