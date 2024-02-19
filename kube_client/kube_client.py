from kubernetes import client, config
from kubernetes.client.rest import ApiException

cert_file = "/home/cruel/kube_client/configs/apiserver.crt"
key_file = "/home/cruel/kube_client/configs/apiserver.key"
ca_file = "/home/cruel/kube_client/configs/ca.crt"

# Configurazione del client
configuration = client.Configuration()
configuration.host = "https://192.168.150.129:8443"
configuration.ssl_ca_cert = ca_file
configuration.cert_file = cert_file
configuration.key_file = key_file

# Impostazione della configurazione predefinita per il client
client.Configuration.set_default(configuration)

# Creazione di un oggetto del client per l'API CoreV1
CoreV1 = client.CoreV1Api()
AppsV1 = client.AppsV1Api()

# Ora puoi utilizzare la libreria Kubernetes per interagire con il cluster
print("Listing pods with their IPs:")
ret = CoreV1.list_pod_for_all_namespaces()
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))