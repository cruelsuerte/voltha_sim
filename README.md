# voltha sim
## Prerequisites
minikube https://minikube.sigs.k8s.io/docs/start/ \
helm https://helm.sh/docs/intro/install/
## Deploy Voltha

VOLTHA relies to a set of infrastructure components (ONOS, Kafka, ETCD, …) that can be installed via the `voltha-infra` helm chart:

```
helm upgrade --install --create-namespace -n infra voltha-infra voltha-helm-charts/voltha-infra
```

```
helm upgrade --install --create-namespace \
-n voltha voltha /home/cruel/voltha-helm-charts/voltha-stack \
--set global.stack_name=voltha \
--set global.voltha_infra_name=voltha-infra \
--set global.voltha_infra_namespace=infra
```

```
helm upgrade --install -n voltha bbsim0 voltha-helm-charts/bbsim --set olt_id=10
```
