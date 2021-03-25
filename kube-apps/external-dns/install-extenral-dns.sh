#!/bin/bash
export $(egrep -v '^#' ../../.env | xargs)
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
envsubst < cloud-flare.yaml > prod.cloud-flare.yaml
# helm install -f prod.cloud-flare.yaml external-dns bitnami/external-dns