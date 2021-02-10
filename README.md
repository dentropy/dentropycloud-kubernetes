# DentropyCloud for Kubernetes

DentropyCloud for Kubernetes is an attempt at making it as easy to install secure full stack server applications as it is to install apps on a phone.

## Table of Contents

* [General info](##General-info)
* [Technologies](##Technologies)
* [Setup](##Setup)

## General info



## Technologies

* [kubernetes](https://kubernetes.io/docs/home/) cluster
    * Reccomended distribution [k3s.io](https://k3s.io/)
    * Currently configured to use [Traefik loadbalancer](https://doc.traefik.io/traefik/v1.7/user-guide/kubernetes/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [helm](https://helm.sh/docs/intro/install/)

## Setup

1. Install k3s.io on VPS

    ``` bash
    # Run each command one at a time
    ssh USER@VPS_IP_ADDRESS
    curl -sfL https://get.k3s.io | sh -
    sudo su
    cp /etc/rancher/k3s/k3s.yaml /home/$USER/k3s.yaml
    cd /home/$USER
    chown -R $USER:$USER .
    exit
    ```

2. Install kubectl on local machine

    The following command works for linux, for other operating systems and install methods such as package managers check out [documentation here](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

    ``` bash
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    ```

3. Install helm package manager for kubernetes

    The following command works for linux, for other operating systems and install methods such as package managers check out [documentation here](https://helm.sh/docs/intro/install/)
    
    ``` bash
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    rm ./get_helm.sh
    ```

4. Configure connection to kubernetes cluster

    Please replace $REMOTE_USER and $REMOTE_IP_ADDRESS with the corresponding infomation required to connect to your VPS
    ``` bash
    scp $REMOTE_USER@$REMOTE_IP_ADDRESS:~/k3s.yaml ~/.kube/config
    sed -i -e "s/127.0.0.1/$REMOTE_IP_ADDRESS/g" ~/.kube/config
    chmod 600 ~/.kube/config
    ```

5. Test the connection

    ``` bash
    kubectl get nodes -o wide
    ```

    Should return something like this

    ``` bash
    NAME        STATUS   ROLES                  AGE    VERSION        INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
    localhost   Ready    control-plane,master   156m   v1.20.2+k3s1   172.105.22.152   <none>        Ubuntu 20.04.1 LTS   5.4.0-65-generic   containerd://1.4.3-k3s1
    ```


6. Configure DNS

7. Install cert-manager and cert issuer

8. Install example app, nextcloud

9. Configure backups

    click [here](./docs/backups.md)

10. Configure tor-controller

    click [here](./docs/tor-controller.md)