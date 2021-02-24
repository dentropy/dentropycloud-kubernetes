#!/bin/bash
helm repo add nextcloud https://nextcloud.github.io/helm/
helm repo update
# helm show values nextcloud/nextcloud > nextcloud-values.yaml
kubectl apply -f nextcloud-pv.yaml
kubectl apply -f nextcloud-pvc.yaml
helm install -f nextcloud-values.yaml nextcloud nextcloud/nextcloud
kubectl apply -f nextcloud-ingress.yaml


helm install --name my-release \
  --set nextcloud.username=admin,nextcloud.password=password,mariadb.rootUser.password=secretpassword \
    stable/nextcloud