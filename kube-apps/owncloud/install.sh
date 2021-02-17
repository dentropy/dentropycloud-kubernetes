#!/bin/bash
helm repo add gitea-charts https://dl.gitea.io/charts/
helm repo update
helm install -f gitea-values.yaml gitea gitea-charts/gitea
kubectl apply -f gitea-ingress.yaml
