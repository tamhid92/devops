ui = true
disable_mlock = "true"

storage "file" {
  path    = "/opt/vault/data"
}

listener "tcp" {
  address = "[::]:8200"
  tls_disable = "true"
}

api_addr = "127.0.0.1:8200"
cluster_addr = "127.0.0.1:8201"