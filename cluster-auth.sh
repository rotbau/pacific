#!/bin/bash

#server='https://10.0.104.2'
#user='administrator@vsphere.local'

kubectl vsphere login --server=$server -u $user --tanzu-kubernetes-cluster-namespace $1 --tanzu-kubernetes-cluster-name $2 --insecure-skip-tls-verify
