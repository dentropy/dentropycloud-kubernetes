#!/bin/bash

# https://cert-manager.io/docs/installation/kubernetes/
kubectl create namespace cert-manager
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v1.1.0 \
  --set installCRDs=true

echo "Waiting 30 for cert-manager to configure itself"
sleep 30
kubectl apply -f cert-issuer-traefik-ingress.yaml
