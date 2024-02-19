Il documento descrive i passaggi per simulare la distribuzione di servizi di Edge Computing sull'OLT, usufruibili da un IoT Device di un utente.

### Prerequisites
[minikube](https://minikube.sigs.k8s.io/docs/start/)

## Installazione
Il seguente comando consente la creazione di un cluster Kubernetes sulla VM che simula l'OLT.
```
minikube start --driver=docker --static-ip 192.168.50.2 --listen-address=0.0.0.0
```
Occorre specificare un indirizzo IP statico per l'ambiente Minikube e l'indirizzo IP dell'interfaccia verso cui esporre i servizi e le API Kubernetes.
Minikube consente di abilitare un Ingress e un servizio DNS per la risoluzione dei nomi associati ai servizi esposti.
```
minikube addons enable ingress
minikube addons enable ingress-dns
```
Affinché l'indirizzo del cluster sia raggiungibile tramite l'interfaccia Host-only della VM da parte della macchina host o altre VMs, eseguire il comando:
```
sudo ip route add 192.168.50.0/24 via <VM-address>
```
## Distribuzione di un servizio
Le API Kubernetes sono esposte alla porta 8443 dell'indirizzo assegnato al cluster, visualizzabile con il comando `minikube ip`. \
Attraverso lo strumento `kubectl`, è possibile interagire da remoto con le API per la gestione delle risorse del cluster.
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



- La creazione del dispositivo
  ```
  voltctl device create -t openolt -H <olt-address>:50060  
  ```
  Occorre specificare l'indirizzo IP associato all'interfaccia Host-only della VM. L'operazione fornisce in output l'id assegnato al dispositivo.

- L'attivazione del dispositivo
  ```
  voltctl device enable <olt-id>
  ```
  L'operazione abiliterà sia l'OLT sia l'ONU simulati da BBSim. È possibile verificare la corretta registrazione del dispositivo dalla GUI di Onos o eseguendo il comando:
  ```
  voltctl device list
  ```

- La rimozione di un dispositivo
  ```
  voltctl device delete <olt-id>
  ```
Le operazioni possono essere riprodotte utilizzando lo script Python voltha_client.py, in grado di interagire con le APIs di Voltha.


