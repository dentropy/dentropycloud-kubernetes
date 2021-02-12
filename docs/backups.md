# Backups

1. Configure a S3 compatible backup server

    On a seperate server accessable to the kubernetes cluter set up minio object storage using docker-compose 

    a. [Install docker-compose](https://docs.docker.com/compose/install/)

        ``` bash
        # On Ubuntu
        sudo apt-get update
        sudo apt install docker-compose
        ```

    b. Save the following yaml script to a "docker-compose.yaml" file on the server.

        **NOTE you probably want to change the Username and Password mapped to stored as MINIO_ROOT_USER and MINIO_ROOT_PASSWORD in the YAML below**

        ``` yaml
        version: '3.7'
        services:
        minio:
            image: minio/minio:RELEASE.2021-02-07T01-31-02Z
            hostname: minio
            volumes:
            - /srv/minio:/export
            ports:
            - "9000:9000"
            environment:
            MINIO_ROOT_USER: AKIAIOSFODNN7EXAMPLE
            MINIO_ROOT_PASSWORD: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
            deploy:
            restart_policy:
                delay: 10s
                max_attempts: 10
                window: 60s
            placement:
                constraints:
                - node.labels.minio==true
            command: server http://minio/export
            healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
            interval: 30s
            timeout: 20s
            retries: 3
        ```

    c. In the same folder you saved the docker-compose.yaml file run the following command

        ``` bash
        sudo docker-compose up -d
        ```

    d. Log into the web gui and create a bucket



2. Install Velero on your client machine

    ``` bash
    curl -L -o /tmp/velero.tar.gz https://github.com/vmware-tanzu/velero/releases/download/v1.5.1/velero-v1.5.1-linux-amd64.tar.gz 
    tar -C /tmp -xvf /tmp/velero.tar.gz
    mv /tmp/velero-v1.5.1-linux-amd64/velero /usr/local/bin/velero
    chmod +x /usr/local/bin/velero
    rm -r /tmp
    ```

3. In kube-apps/velero save minio.credentials file adding username and password similar to the file below.

    ``` txt
    [default]
    aws_access_key_id=$USERNAME_FOR_MINIO
    aws_secret_access_key=$PASSWORD_FOR_MINIO
    ```

4. Run the following command to install velero with the minio.credentials file in the same directory

    ``` bash
    #!/bin/bash
    echo "Enter domain or IP address of minio server"
    read s3_server
    velero install \
        --provider aws \
        --plugins velero/velero-plugin-for-aws:v1.1.0 \
        --bucket kubedemo \
        --secret-file ./minio.credentials \
        --backup-location-config region=minio,s3ForcePathStyle=true,s3Url=http://$s3_server:9000
    ```

5. Run the following script to create your own backup

    ``` bash
    echo "Please enter name of backup"
    read backup_name
    echo "Creating backup named $backup_name"
    velero backup create $backup_name
    echo "Done creating backup $backup_name"
    ```
## Important velero commands

    ``` bash
    velero get backups
    velero describe backup $BACKUP_NAME
    velero backup logs $BACKUP_NAME
    ```
