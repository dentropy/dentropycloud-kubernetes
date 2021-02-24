# DentropyCloud for Kubernetes

DentropyCloud for Kubernetes is an attempt at making it as easy to install secure full stack server applications as it is to install apps on a phone.

## Table of Contents

* [General info](##General-info)
* [Technologies](##Technologies)
* [Setup](##Setup)

## General info



## Technologies

* Ubuntu VPS
* [kubernetes](https://kubernetes.io/docs/home/) cluster
    * Reccomended distribution [k3s.io](https://k3s.io/)
    * Currently configured to use [Traefik loadbalancer](https://doc.traefik.io/traefik/v1.7/user-guide/kubernetes/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [helm](https://helm.sh/docs/intro/install/)

## Instructions

For those that like to live [dangerously](http://tserong.github.io/sudo-wget/) there exists a one line command, listed below, whcih configure everything for you.

``` bash
wget https://gitlab.com/dentropy/Dentropycloud-Kubernetes/-/raw/master/server-install.sh && sudo bash ./server-install.sh
```

For Manual install click [here](./docs/manual-install.md)

To configure backups click [here](./docs/backups.md)

To configure tor-controller click [here](./docs/tor-controller.md)

## Remote Management

``` bash
cd ~/.kube
scp USER@VPS_IP_ADDRESS:~/k3s.yaml .
sed -i -e "s/127.0.0.1/VPS_IP_ADDRESS/g" ./k3s.yaml
cp k3s.yaml config
```