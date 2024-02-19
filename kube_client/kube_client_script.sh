#!/bin/bash

kubectl create namespace application --kubeconfig ~/kube_client/config_remote
kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0 -n application --kubeconfig ~/kube_client/config_remote
kubectl expose deployment hello-server --type=NodePort --port=8080 -n application --kubeconfig ~/kube_client/config_remote
kubectl apply -f ~/kube_client/hello-ingress.yaml -n application --kubeconfig ~/kube_client/config_remote
