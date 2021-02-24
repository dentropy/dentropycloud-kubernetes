#!/bin/bash

echo "We need sudo access for later"
sudo echo "Thanks"

function get_env_from_user {
    echo "Please enter your domain name"
    read YOUR_DOMAIN_NAME

    # https://tecadmin.net/bash-script-prompt-to-confirm-yes-no/
    read -r -p "Would you like to use self signed certificates [Y/n] " input
    case $input in 
    [yY][eE][sS]|[yY] )
        echo "You selected use self signed certificates"
        USE_SELF_SIGNED=true
        CERT_ISSUER=selfsigned-issuer
    ;;
    [nN][oO]|[nN])
        echo "You selected to use signed certificates"
        echo "Please enter email you would like to use with Let's Encrypt"
        read LETSENCRYPT_EMAIL
        echo LETSENCRYPT_EMAIL=$LETSENCRYPT_EMAIL >> .env
        CERT_ISSUER=letsencrypt-staging
    ;;
    *)
    echo "Invalid input..."
    exit 1
    ;;
    esac
    echo CERT_ISSUER=$CERT_ISSUER >> .env
    echo YOUR_DOMAIN_NAME=$YOUR_DOMAIN_NAME >> .env
    read -r -p "Would you like to install example app trilium-notes [Y/n] " input
    case $input in
    [yY][eE][sS]|[yY])
        INSTALL_EXAMPLE_APP=true
    ;;
    [nN][oO]|[nN])
        INSTALL_EXAMPLE_APP=false
    ;;
    *)
    echo "Invalid input..."
    exit 1
    ;;
    esac

    echo INSTALL_EXAMPLE_APP=$INSTALL_EXAMPLE_APP >> .env
}

FILE=.env
if test -f "$FILE"; then
    echo "loaded .env file "
    export $(cat .env | xargs)
else
    get_env_from_user
fi


echo "Configuring Firewall"
sudo ufw default allow outgoing
sudo ufw default allow incoming
sudo ufw deny 2049 # For NFS
sudo ufw enable


echo "Updating Packages"
sudo apt-get -y update

echo "Insatlling git"
sudo apt install -y git

echo "git cloning git repo"
git clone https://gitlab.com/dentropy/Dentropycloud-Kubernetes.git

echo "Install kubernetes, k3s.io distribution"
sudo curl -sfL https://get.k3s.io |  INSTALL_K3S_VERSION=v1.19.7+k3s1 sh -
sudo cp /etc/rancher/k3s/k3s.yaml $HOME/k3s.yaml
cd $HOME
sudo chown -R $USER:$USER .
mkdir .kube
cp $HOME/k3s.yaml $HOME/.kube/config


echo "Installing NFS server on localhost"
sudo apt -y update
sudo apt install -y nfs-kernel-server
sudo mkdir -p /mnt/nfsdir
sudo chown nobody:nogroup /mnt/nfsdir
sudo chmod 777 /mnt/nfsdir
echo "/mnt/nfsdir    *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee /etc/exports
sudo exportfs
sudo systemctl restart nfs-kernel-server

echo "Installing kubectl on localhost"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

echo "Installing helm on localhost"
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
rm ./get_helm.sh

echo "Installing nfs-provisioner"
sudo mkdir /mnt/nfsdir/provisioner
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner
helm repo update
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=127.0.0.1 \
    --set nfs.path=/mnt/nfsdir/provisioner

echo "Installing cert-manager"
sudo kubectl create namespace cert-manager
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install \
    cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --version v1.2.0 \
    --set installCRDs=true
echo "Waiting for cert-manager to configure itself"
sleep 30
# Wait 30 seconds
# kubectl get pods --namespace cert-manager
# Should return a bunch of pods

echo "Configuring certificate issuer"
if USE_SELF_SIGNED; then
    sed -i -e "s/personinternet@protonmail.com/$LETSENCRYPT_EMAIL/g" ./kube-apps/cert-manager/cert-issuer-traefik-ingress.yaml
    sudo kubectl apply -f ./kube-apps/cert-manager/cert-issuer-self-signed.yaml
else
    sudo kubectl apply -f ./kube-apps/cert-manager/cert-issuer-traefik-ingress.yaml
fi

if $INSTALL_EXAMPLE_APP; then
    cd Dentropycloud-Kubernetes/kube-apps/trilium-notes && bash install-trilium-notes.sh
fi
