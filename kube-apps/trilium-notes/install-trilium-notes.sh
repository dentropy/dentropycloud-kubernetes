#!/bin/bash
# https://docs.gitea.io/en-us/install-on-kubernetes/
export YOUR_DOMAIN_NAME=test.local
export CERT_ISSUER=selfsigned-issuer
helm repo add ohdearaugustin https://ohdearaugustin.github.io/charts/
helm repo update
envsubst < trilium-notes-values.yaml > prod.trilium-notes-values.yaml
helm install -f prod.trilium-notes-values.yaml trilium-notes ohdearaugustin/trilium-notes

