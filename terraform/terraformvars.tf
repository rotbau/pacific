variable "kube_config" {
  type        = string
  description = "location of kubeconfig"
}

variable "tkc_name" {
  type        = string
  description = "tkg cluster name"
}

variable "tkc_namespace" {
  type        = string
  description = "tkg cluster namespace"
}

variable "tkc_version" {
  type        = string
  description = "tkg kubernetes version"
}

variable "tkc_cni" {
  type        = string
  description = "cni to deploy"
}

variable "cp_size" {
  type        = string
  description = "vmclass for control plane"
}

variable "cp_count" {
  type        = number
  description = "number of control plane nodes 1 or 3"
}

variable "cp_storageclass" {
  type        = string
  description = "storage policy for control plane vms"
}

variable "wrk_size" {
  type        = string
  description = "vmclass for worker nodes"
}

variable "wrk_count" {
  type        = number
  description = "number or worker nodes"
}

variable "wrk_storageclass" {
  type        = string
  description = "storage policy for worker vms"
}
