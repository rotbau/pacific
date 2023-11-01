$server = "https://10.0.104.2"
$user = "administrator@vsphere.local"

kubectl vsphere login --server=$server --insecure-skip-tls-verify -u $user

