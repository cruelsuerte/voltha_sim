# Voltha Environment Simulation
This repository defines Kubernetes Helm charts that can be used to deploy a VOLTHA instance and interact with VOLTHA APIs.

### Prerequisites
minikube https://minikube.sigs.k8s.io/docs/start/ \
helm https://helm.sh/docs/intro/install/

## Deploy Voltha
Open a terminal in the project folder. \
VOLTHA relies to a set of infrastructure components (ONOS, Kafka, ETCD, …) that can be installed via the `voltha-infra` helm chart:

```
helm upgrade --install --create-namespace -n infra voltha-infra voltha-helm-charts/voltha-infra
```

VOLTHA encompass multiple components that work together to manage OLT devices. Such group of component is known as a stack and is composed by:
- VOLTHA core
- OfAgent (OpenFlow Agent)
- OLT Adapter
- ONU Adapter

To deploy a VOLTHA stack with the opensource adapters (OpenOLT and OpenONU) you can use the `voltha-stack` chart:
```
helm upgrade --install --create-namespace \
-n voltha voltha voltha-helm-charts/voltha-stack \
--set global.stack_name=voltha \
--set global.voltha_infra_name=voltha-infra \
--set global.voltha_infra_namespace=infra
```
## Deploy BBSim
BBSim is a broadband simulator tool that is used as an OpenOLT compatible device in emulated environments.
In order to install a single BBSim instance to test VOLTHA, you can use the BBSim helm chart:
```
helm upgrade --install -n voltha bbsim0 voltha-helm-charts/bbsim --set olt_id=10
```

## Installing voltctl
```
HOSTOS="$(uname -s | tr "[:upper:]" "[:lower:"])"
HOSTARCH="$(uname -m | tr "[:upper:]" "[:lower:"])"
if [ "$HOSTARCH" == "x86_64" ]; then
    HOSTARCH="amd64"
fi
sudo wget https://github.com/opencord/voltctl/releases/download/v1.8.45/voltctl-1.8.45-$HOSTOS-$HOSTARCH -O /usr/local/bin/voltctl
sudo chmod +x /usr/local/bin/voltctl
source <(voltctl completion bash)
```
(In MacOS use '=' instead of '==')

## Accessing the ONOS and Voltha API
Expose ONOS SSH (username: karaf, password: karaf):
```
kubectl -n infra port-forward --address 0.0.0.0 svc/voltha-infra-onos-classic-hs 8101:8101
```
Connect to ONOS by ```ssh karaf@127.0.0.1 -p 8101```.

Expose ONOS Rest API and GUI (username: onos, password: rocks):
```
kubectl -n infra port-forward --address 0.0.0.0 svc/voltha-infra-onos-classic-hs 8181:8181
```
Expose Voltha API:
```
kubectl -n voltha port-forward svc/voltha-voltha-api 55555
```
If you are exposing the voltha-api service on 127.0.0.1:55555 there is no need to configure `voltctl`, if you are exposing the service on a different port/IP you configure `voltctl` with:
```
mkdir ~/.volt/
voltctl -s 127.0.0.1:55555 config > $HOME/.volt/config
```
Then, you have to modify $HOME/.volt/config file.
## Provisioning an OLT
To create and enable the OLT device in VOLTHA you can use these `voltctl` commands:
```
voltctl device create -t openolt -H bbsim0.voltha.svc:50060
voltctl device list --filter Type~openolt -q | xargs voltctl device enable
```
## Voltha client
To use Voltha Python protobufs and gRPC stubs and interact with Voltha APIs, first install the dependencies:
```
pip install voltha-protos
```
Python script `test.py` is a demo client that can be used as a reference/starting point.

## References
https://docs.voltha.org/voltha-2.9/voltha-helm-charts/README.html \
https://docs.voltha.org/voltha-2.9/voltha-protos/README.html \
https://gerrit.opencord.org/plugins/gitiles/voltha/+/e0d53f8301eab8f38ccc042bf9d2eb49f4d6e430/voltha/protos/voltha.proto
