#!/bin/bash
export $(egrep -v '^#' ../../.env | xargs)
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
envsubst < trilium-notes-values.yaml > prod.trilium-notes-values.yaml