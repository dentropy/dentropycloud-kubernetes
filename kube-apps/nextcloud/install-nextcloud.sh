#!/bin/bash
helm repo add nextcloud https://nextcloud.github.io/helm/
helm repo update
helm install -f nextcloud-values.yaml nextcloud nextcloud/nextcloud
kubectl apply -f nextcloud-ingress.yaml

# helm show values extcloud/nextcloud > test.yaml


#helm install --name nextcloud \
#  --set nextcloud.username=admin,nextcloud.password=password,mariadb.rootUser.password=secretpassword \
#    stable/nextcloud
