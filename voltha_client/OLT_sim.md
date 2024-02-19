# Simulazione OLT
Il documento descrive i passaggi per la simulazione di un OLT remoto registrato con Voltha.

### Prerequisites
[docker](https://docs.docker.com/engine/install/ubuntu/)

## Installazione
L'OLT remoto viene simulato attraverso un container docker in esecuzione su una Virtual Machine Ubuntu 22.04. \
La VM è configurata in modalità Host-only, in modo da condividere una rete privata virtualizzata con la macchina host o altre VMs. \
Il container fa riferimento all'immagine ufficiale DockerHub di [BBSim](https://hub.docker.com/r/voltha/bbsim), un simulatore Control Plane per Voltha. \
Il seguente comando consente di eseguire il container in modo che possa ricevere messaggi di registrazione da Voltha.

```
docker run -p 50060:50060 voltha/bbsim:master
```
## Registrazione
A questo punto è possibile utilizzare lo strumento `voltctl` per richiedere al server Voltha:
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
Le operazioni possono essere riprodotte utilizzando lo script Python `voltha_client.py`, in grado di interagire con le APIs di Voltha.
