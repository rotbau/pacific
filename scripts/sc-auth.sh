#!/bin/bash

$server='https://10.0.104.2'
$user='administrator@vsphere.local'

kubectl vsphere login --server=$server -u $user --insecure-skip-tls-verify