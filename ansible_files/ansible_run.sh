#!/bin/bash
ansible-playbook -i /home/$USER/kubernetes-playbook/inventory.yml /home/$USER/kubernetes-playbook/cluster.yml --extra-vars "ansible_sudo_pass=PasswordsSuck"
