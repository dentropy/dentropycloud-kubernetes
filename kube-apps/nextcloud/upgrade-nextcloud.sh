#!/bin/bash
export $(egrep -v '^#' ../../.env | xargs)
helm repo update
envsubst < nextcloud-values.yaml > prod.nextcloud-values.yaml
helm upgrade -f prod.nextcloud-values.yaml nextcloud nextcloud/nextcloud
