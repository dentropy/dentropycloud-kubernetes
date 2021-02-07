#!/bin/bash
sudo su
sudo apt -y update
sudo apt install -y nfs-kernel-server
sudo mkdir -p /mnt/nfsdir
sudo chown nobody:nogroup /mnt/nfsdir
sudo chmod 777 /mnt/nfsdir
echo "/mnt/nfsdir -async,no_subtree_check *(rw,insecure,sync,no_subtree_check,no_root_squash)" >  /etc/exports
sudo exportfs
sudo systemctl restart nfs-kernel-server
