#!/bin/bash
echo "Enter domain or IP address of s3 compatible storage server"
read s3_server
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.1.0 \
    --bucket kubedemo \
    --secret-file ./minio.credentials \
    --backup-location-config region=minio,s3ForcePathStyle=true,s3Url=http://$s3_server:9000