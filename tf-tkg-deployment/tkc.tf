provider "kubernetes-alpha" {
  config_path = "~/.kube/config" // path to kubeconfig
}

resource "kubernetes_manifest" "tanzukubernetescluster_tf_tkg_cluster" {
  provider = kubernetes-alpha

  manifest = {
    "apiVersion" = "run.tanzu.vmware.com/v1alpha1"
    "kind" = "TanzuKubernetesCluster"
    "metadata" = {
      "name" = var.tkc_name
      "namespace" = var.tkc_namespace
    }
    "spec" = {
      "distribution" = {
        "version" = var.tkc_version
      }
      "settings" = {
        "network" = {
          "cni" = {
            "name" = var.tkc_cni
          }
          "pods" = {
            "cidrBlocks" = [
              "193.0.2.0/16",
            ]
          }
          "serviceDomain" = "managedcluster.local"
          "services" = {
            "cidrBlocks" = [
              "195.51.100.0/12",
            ]
          }
        }
      }
      "topology" = {
        "controlPlane" = {
          "class" = var.cp_size
          "count" = var.cp_count
          "storageClass" = var.cp_storageclass
        }
        "workers" = {
          "class" = var.wrk_size
          "count" = var.wrk_count
          "storageClass" = var.wrk_storageclass
        }
      }
    }
  }
}
