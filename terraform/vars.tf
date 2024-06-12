variable "vsphere_user" {
  description = "vSphere username"
  type        = string
  default     = ""
}

variable "vsphere_password" {
  description = "vSphere password"
  type        = string
  default     = ""
}

variable "vsphere_server" {
  description = "vSphere server URL"
  type        = string
  default     = ""
}

variable "datacenter_name" {
  description = "Name of the datacenter"
  type        = string
  default     = ""
}

variable "datastore_name" {
  description = "Name of the datastore"
  type        = string
  default     = ""
}

variable "cluster_name" {
  description = "Name of the compute cluster"
  type        = string
  default     = ""
}

variable "network_name" {
  description = "Name of the network"
  type        = string
  default     = ""
}

variable "template_name" {
  description = "Name of the virtual machine template"
  type        = string
  default     = ""
}

variable "vm_name" {
  description = "Name of the new virtual machine"
  type        = string
  default     = ""
}

variable "vm_annotation" {
  description = "Annotation for the new virtual machine"
  type        = string
  default     = ""
}

variable "vm_folder" {
  description = "Folder for the new virtual machine"
  type        = string
  default     = ""
}

variable "vm_hostname" {
  description = "Hostname for the new virtual machine"
  type        = string
  default     = ""
}

variable "vm_domain" {
  description = "Domain for the new virtual machine"
  type        = string
  default     = ""
}

variable "disk_size" {
  description = "Size of additonal disk to be attached"
  type        = number
  default     = 50
}

variable "disk_label" {
  description = "Disk label"
  type        = string
  default     = "disk0"
}

variable "cpu" {
  description = "Number of CPUs for the VM"
  type        = number
  default     = 2

}

variable "memory" {
  description = "Memory size in MB"
  type        = number
  default     = 1024
}

variable "ipv4_address" {
  description = "IPv4 address for the new virtual machine"
  type        = string
  default     = ""
}

variable "ipv4_netmask" {
  description = "IPv4 netmask for the new virtual machine"
  type        = string
  default     = ""
}

variable "ipv4_gateway" {
  description = "IPv4 gateway for the new virtual machine"
  type        = string
  default     = ""
}

variable "dns_server_list" {
  description = "List of DNS servers for the new virtual machine"
  type        = list(string)
  default     = []
}

variable "dns_suffix_list" {
  description = "List of DNS suffixes for the new virtual machine"
  type        = list(string)
  default     = []
}
