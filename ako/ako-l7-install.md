# Use AVI AKO for Ingress on TKGs

## Create AVI namespace
```
k create ns avi-system`
```

##Create Rolebinding for AKO Pod to use PSP
```
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: rolebinding-default-privileged-sa-ns_avi-system
  namespace: avi-system
roleRef:
  kind: ClusterRole
  name: psp:vmware-system-privileged
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:serviceaccounts
```

## Add VMware Helm Repo for AKO
```
helm repo add ako https://projects.registry.vmware.com/chartrepo/ako
```

## Search Repo for AKO helm versions
```
helm search repo ako -l
```
Note: validate your controller version matches AKO helm chart and version (example 20.1.6 can go up to 1.7)
https://avinetworks.com/docs/ako/1.9/ako-compatibility-guide/

## Generate values.yaml
```
helm show values ako/ako --version 1.7.3 > values.yaml
```

## Update values.yaml - see example

## Install AKO
```
helm install ako-l7 ako/ako --version 1.7.3 -f values.yaml --namespace=avi-system
```

## Validate install
```
k get po -n avi-system
```


https://vra4u.com/2022/02/07/tkgs-use-nsx-alb-avi-as-ingress-controller-for-vsphere-with-tanzu/
