#!/bin/bash
helm install -f owncloud-values.yaml owncloud bitnami/owncloud

helm repo update
helm install -f gitea-values.yaml gitea gitea-charts/gitea
kubectl apply -f gitea-ingress.yaml
