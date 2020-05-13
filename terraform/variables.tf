variable "region" {
  default = "us-west-2"
}
variable "vpc_id" {
  default = ""
}
variable "profile" {
  default = ""
}
variable "instance_type" {
  default = "m5.large"
}
variable "whitelist_ips" {
  type        = list(map(string))
  default     = []
  description = "List of cidr blocks and ports to create ingress rules for."
}
