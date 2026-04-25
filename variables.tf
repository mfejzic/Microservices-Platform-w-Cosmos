variable "vnet_cidr" {
  type = list(string)
  default = ["10.0.0.0/16"]
}

variable "twilio_auth_token" {
  description = "Twilio Auth Token"
  type        = string
  sensitive   = true
}

variable "twilio_sid" {
  type      = string
  default = "get fom tfvars"
  sensitive = true
}