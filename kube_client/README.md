Il documento descrive i passaggi necessari per simulare la distribuzione di servizi sull'OLT, usufruibili da un utente finale.

### Prerequisites
[minikube](https://minikube.sigs.k8s.io/docs/start/) \
[resolvconf](https://manpages.ubuntu.com/manpages/jammy/man8/resolvconf.8.html)

## Installazione
Il seguente comando consente la creazione di un cluster Kubernetes sulla VM che simula l'OLT.
```
minikube start --driver=docker --static-ip 192.168.50.2 --listen-address=0.0.0.0
```
Occorre specificare un indirizzo IP statico per l'ambiente Minikube e l'indirizzo IP dell'interfaccia verso cui esporre i servizi e le API Kubernetes.
Minikube consente di abilitare le funzioni Ingress e DNS per l'instradamento delle richieste verso i servizi esposti.
```
minikube addons enable ingress
minikube addons enable ingress-dns
```
Affinché l'indirizzo del cluster sia raggiungibile tramite l'interfaccia Host-only della VM da parte della macchina host o altre VMs, eseguire il comando:
```
sudo ip route add 192.168.50.0/24 via <olt-address>
```
In alternativa, affinché l'aggiunta della rotta sia persistente, è possibile modificare il file `/etc/netplan/01-network-manager-all.yaml` come segue ed applicare le modifiche grazie al comando `sudo netplan apply`. 
```
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    <host-only-interface>:
      dhcp4: true
      routes:
      - to: 192.168.50.0/24
        via: <olt-address>
```
## Distribuzione di un servizio
Le APIs di Kubernetes sono esposte alla porta 8443 dell'indirizzo assegnato al cluster, visualizzabile con il comando `minikube ip`. \
Attraverso lo strumento `kubectl`, è possibile interagire da remoto con le APIs per la gestione delle risorse del cluster.
Occore indicare il file di configurazione che fa riferimento alle chiavi utilizzate per l'autenticazione con l'API server di minikube. Tali chiavi sono generate in seguito alla creazione del cluster. Possono essere prelevate dalla cartella locale `.minikube` e inserite in una cartella keys, a cui fa riferimento il file di configurazione `config_remote` per la gestione da remoto.
I seguenti comandi consentono la creazione di un namespace, un deployment e un servizio all'interno del cluster Kubernetes. L'applicazione web esposta risponde alle richieste HTTP con un messaggio di greeting.

```
kubectl create namespace application --kubeconfig ~/kube_client/config_remote
```
```
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0 -n application --kubeconfig ~/kube_client/config_remote
```
```
kubectl expose deployment hello-server --type=NodePort --port=8080 -n application --kubeconfig ~/kube_client/config_remote
```

## Configurazione del DNS per l'accesso al servizio
Per rendere accessibile l'applicazione web attraverso un nome di dominio, è necessario creare un Ingress e inserire una voce relativa al servizio esposto. Il seguente comando applica un Ingress definito dal file `hello-ingress.yaml`. L'applicazione viene associata al nome di dominio hello.app .
```
kubectl apply -f ~/kube_client/hello-ingress.yaml -n application --kubeconfig ~/kube_client/config_remote
```
Il comando `nslookup hello.app <minikube-ip>` consente di verificare che il cluster risponda correttamente alle query DNS. \
I passaggi per configurare l'indirizzo IP del cluster come indirizzo del server DNS fanno riferimento alla guida [Ingress DNS | minikube](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns/) . \
È necessario modificare il file `/etc/resolvconf/resolv.conf.d/head` inserendo:
```
search app
nameserver <minikube-ip>
timeout 5
```
In questo modo, l'applicazione è accessibile da remoto all'indirizzo web http://<span></span>hello.app/
```
iot@iot-virtual-machine:~$ curl http://hello.app
Hello, world!
Version: 1.0.0
Hostname: hello-server-5f8d66645-chhw9
```
Le operazioni possono essere riprodotte utilizzando lo script Python kube_client_create.py, in grado di interagire con le APIs di Kubernetes grazie alla libreria [Kubernetes Client](https://github.com/kubernetes-client/python).
