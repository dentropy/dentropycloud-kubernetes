#!/usr/bin/python3

import os
import subprocess
import getpass
from shutil import which

logs = [] # TODO log all subprocesses to this list

def yes_or_no(question):
    reply = str(input(question+' (Y/n): ')).lower().strip()
    if len(reply) == 0:
        return True
    elif reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    else:
        return True #yes_or_no("Uhhhh... please enter ")

def run_bash_string(bash_string):
    bash_string = bash_string.replace("sudo", ("echo %s | sudo -S" % sudo_pass))
    for line in bash_string.split("\n"):
        print(line)
        p = subprocess.Popen(line, stdout=subprocess.PIPE, shell=True)
        p.wait()

def check_root():
    print("We need sudo access for later")
    sudo_pass = getpass.getpass()
    sudo_test = subprocess.run( ("echo %s | sudo -S echo test" % sudo_pass).split(), capture_output=True)
    if sudo_test.returncode :
        print("Was unable to obtain root, exiting script")
        exit()
    return sudo_pass

def install_dependencies():
    print("Checking dependencies")
    if os.path.exists('/home/%s/.local/bin' % getpass.getuser()):
        os.environ['PATH'] += ':' + '/home/%s/.local/bin' % getpass.getuser()
    print("Checking for git")
    # TODO support installing git on other operating systems
    if which("git") == None:
        print("Updating")
        run_bash_string("sudo apt-get update")
        print("Installing Git")
        run_bash_string('sudo apt install -y git')
        p.wait()
    else:
        print("git is already installed")
    if which("pip3") == None:
        print("Installing pip3")
        p = subprocess.Popen('wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --user', stdout=subprocess.PIPE, shell=True) # Install pip
        p.wait()
        subprocess.Popen('rm get-pip.py', shell=True)
        os.environ['PATH'] += ':' + '/home/%s/.local/bin' % getpass.getuser()
    else:
        print("pip3 is already installed")
    if which("ansible") == None:
        print("Installing ansible")
        p = subprocess.Popen('python3 -m pip install --user ansible', stdout=subprocess.PIPE, shell=True)
        p.wait()
    else:
        print("ansible already installed")
    print("Installing ansible role xanmanning.k3s")
    p = subprocess.Popen('ansible-galaxy install xanmanning.k3s', stdout=subprocess.PIPE, shell=True) # Install ansible role xanmanning.k3s
    p.wait()
    if os.path.exists("/home/%s/Dentropycloud-Kubernetes"):
        print("Pulling Dentropycloud-Kubernetes git repo")
        pull_command = "cd /home/%s/Dentropycloud-Kubernetes/ && git pull" % getpass.getuser()
        p = subprocess.Popen(pull_command, stdout=subprocess.PIPE, shell=True) # Install pip
        p.wait()
        print("Done pulling")
    else:
        print("Cloning Dentropycloud-Kubernetes repo")
        clone_repo_command = "git clone https://gitlab.com/dentropy/Dentropycloud-Kubernetes.git /home/%s/Dentropycloud-Kubernetes" % getpass.getuser()
        p = subprocess.Popen(clone_repo_command, stdout=subprocess.PIPE, shell=True) # Install pip
        p.wait()
        print("Done cloning")

def import_env_file(env_file_path):
    env_vars = {}
    with open(env_file_path) as f:
        env_file_contents = f.readlines()
    for env_var in env_file_contents:
        env_var = env_var.replace("\n", "")
        if "true" in env_var:
            env_vars[env_var.split("=")[0]] = True
        elif "false" in env_var:
            env_vars[env_var.split("=")[0]] = False
        else:
            env_vars[env_var.split("=")[0]] = env_var.split("=")[1]
    return env_vars

def export_env_file(env_vars):
    dot_env_string = ""
    for env_var in env_vars:
        if type(env_vars[env_var]) == type(True):
            if env_vars[env_var]:
                dot_env_string += "%s=%s\n" % (env_var, str(env_vars[env_var]).lower())
        else:
            dot_env_string += "%s=%s\n" % (env_var, env_vars[env_var])
    text_file = open("/home/%s/Dentropycloud-Kubernetes/.env" % getpass.getuser(), "w")
    n = text_file.write(dot_env_string)
    text_file.close()
    return env_vars

def get_env_from_user():
    env_vars = {}
    input_confirmed = True
    while input_confirmed:
        env_vars["YOUR_DOMAIN_NAME"] = input("Please enter your domain name: ")
        # TODO check valid domain name
        input_confirmed = not yes_or_no("Please confirm that %s is your domain name " % env_vars["YOUR_DOMAIN_NAME"])
    input_confirmed = True
    while input_confirmed:
        env_vars["USE_SELF_SIGNED"] = yes_or_no("Would you like to use self signed certificates ")
        if env_vars["USE_SELF_SIGNED"]:
            input_confirmed = not yes_or_no("Please confirm that you want to use a self signed certificates ")
        else:
            env_vars["LETSENCRYPT_EMAIL"] = input("Please enter email you would like to use with Let's Encrypt: ")
            # TODO check valid email
            input_confirmed = not yes_or_no("Please confirm you want to use signed ceritificates from Lets Encrypt and that %s is your email " % env_vars["LETSENCRYPT_EMAIL"])
    input_confirmed = True
    while input_confirmed:
        env_vars["SINGLE_NODE"] = yes_or_no("Are you instlling kubernetes on just this node")
        if env_vars["SINGLE_NODE"]:
            input_confirmed = not yes_or_no("Please confirm that you want to install kubernetes on this node")
        else:
            print("Multi node install is not supported at this time")
    input_confirmed = True
    while input_confirmed:
        env_vars["INSTALL_NFS_SERVER"] = yes_or_no("Would you like to install a NFS Server on this node")
        if env_vars["INSTALL_NFS_SERVER"]:
            env_vars["NFS_SHARE_IP_ADDRESS"] = "127.0.0.1"
            env_vars["NFS_SHARE_PATH"] = "/mnt/nfsdir/provisioner"
            input_confirmed = not yes_or_no("Please confirm that you do want to install a NFS server to be used by Kubernetes")
        else:
            env_vars["NFS_SHARE_IP_ADDRESS"] = input("Please enter IP Address of NFS Share: ")
            # TODO check valid IP address
            env_vars["NFS_SHARE_PATH"] = input("Please enter path of NFS Share to be used with Kubernetes: ")
            # TODO check valid path
            input_confirmed = not yes_or_no("Please confirm you want to use a custom NFS SHare %s%s" % (env_vars["NFS_SHARE_IP_ADDRESS"], env_vars["NFS_SHARE_PATH"])) 
    input_confirmed = True
    while input_confirmed:
        env_vars["INSTALL_TRILIUM_NOTES"] = yes_or_no("As your first application would you like to install Trilium Notes")
        if env_vars["INSTALL_TRILIUM_NOTES"]:
            input_confirmed = not yes_or_no("Please confirm that you do want to install Trilium Notes")
        else:
            input_confirmed = not yes_or_no("Please confirm that you do NOT want to install Trilium Notes")
    # TODO Meta Confirmation with every setting printed out
    export_env_file(env_vars)

def configure_nfs_server():
    # TODO test NFS server Install
    # TODO support other linux distros
    if which("showmount") != None:
        nfs_check_command = "showmount -e %s" % env_vars["NFS_SHARE_IP_ADDRESS"]
        try:
            nfs_test = subprocess.check_output(nfs_check_command.split(), shell=True)
            print(nfs_test)
            print("NFS server working and ready")
            return True
        except subprocess.CalledProcessError:
            if env_vars["INSTALL_NFS_SERVER"]:
                print("Need to install NFS server")
            else:
                # TODO add troubleshooting steps here, 
                # TODO have ansible script install NFS on another server
                print("Problem with NFS server exiting")
                exit()
    print("Installing NFS server on localhost")
    print("Configuring firewall for NFS server")
    configure_firewall_script = '''
    sudo ufw default allow outgoing
    sudo ufw default allow incoming
    sudo ufw deny 2049
    sudo ufw --force enable
    '''
    run_bash_string(configure_firewall_script)
    bash_script = '''
    echo "Installing NFS server on localhost"
    sudo apt -y update
    sudo apt install -y nfs-kernel-server
    sudo mkdir -p /mnt/nfsdir
    sudo chown nobody:nogroup /mnt/nfsdir
    sudo chmod 777 /mnt/nfsdir
    sudo su
    sudo sh -c 'echo "/mnt/nfsdir *(rw,async,no_subtree_check,no_root_squash)" > /etc/exports'
    sudo exportfs
    sudo systemctl restart nfs-kernel-server
    '''
    run_bash_string(bash_script)


def install_k3s():
    test_kubectl = subprocess.check_output("echo %s | sudo -S kubectl get nodes" % sudo_pass, shell=True)
    if "Ready".lower() in str(test_kubectl.lower()):
        print("Kubernetes cluster already configured")
    else:
        print("Installing k3s on localhost")
        # p = subprocess.Popen("sudo usermod -a -G root %s" % getpass.getuser(), stdout=subprocess.PIPE, shell=True) 
        # p.wait()
        print("Configuring SSH for localhost")
        if not os.path.exists("/home/dentropy/.ssh/ddaemon"):
            print("Generating Dentropy Daemon ssh key")
            p = subprocess.Popen('ssh-keygen -f /home/dentropy/.ssh/ddaemon -P ""', stdout=subprocess.PIPE, shell=True) 
            p.wait()
        print("Adding Dentropy Daemon ssh key to ssh-agent")
        p = subprocess.Popen('ssh-add /home/dentropy/.ssh/ddaemon', stdout=subprocess.PIPE, shell=True) 
        p.wait()
        print("Copying Dentropy Daemon ssh key to host")
        p = subprocess.Popen('ssh-copy-id -f %s@127.0.0.1' % getpass.getuser(), stdout=subprocess.PIPE, shell=True) 
        p.wait()
        print("Fixing some permissions")
        # p = subprocess.Popen('sudo chmod -R 775 /usr/local/bin', stdout=subprocess.PIPE, shell=True) 
        # p.wait()
        print("Configuring ansible playbook")
        if not os.path.exists("/home/%s/kubernetes-playbook" % getpass.getuser()):
            os.mkdir("/home/%s/kubernetes-playbook" % getpass.getuser())
        ansible_inventory_yml = '''
        k3s_cluster:
            hosts:
                kube-0:
                    ansible_user: %s
                    ansible_host: 127.0.0.1
                    ansible_sudo_pass: 
                    ansible_python_interpreter: /usr/bin/python3
        ''' % getpass.getuser()
        print(ansible_inventory_yml, file=open("/home/%s/kubernetes-playbook/inventory.yml" % getpass.getuser(), 'w'))
        ansible_cluster_yaml = '''
        - name: Build a single node k3s cluster with etcd datastore
        hosts: k3s_cluster
        vars:
            k3s_release_version: v1.19
            k3s_become_for_all: true
            k3s_etcd_datastore: true
        roles:
            - role: xanmanning.k3s
        '''
        print(ansible_cluster_yaml, file=open("/home/%s/kubernetes-playbook/cluster.yml" % getpass.getuser(), 'w'))
        print("Testing if ansible can connect to host")
        anisble_test = "ansible -i /home/%s/kubernetes-playbook/inventory.yml -m ping all" % getpass.getuser()
        p = subprocess.Popen(anisble_test, stdout=subprocess.PIPE, shell=True) 
        p.wait()
        if "SUCCESS" in str(p.stdout.read()):
            print("Ansible sucessfully connected to host")
        else:
            print("We have a problem ansible did not connect")
            # TODO troubleshoot here
        print("Installing k3s")
        ansible_install = 'ansible-playbook -i /home/%s/kubernetes-playbook/inventory.yml /home/%s/kubernetes-playbook/cluster.yml --extra-vars "ansible_sudo_pass=%s"' % (getpass.getuser(), getpass.getuser(), sudo_pass)
        # TODO actually test installing k3s on localhost
        p = subprocess.Popen(ansible_install, stdout=subprocess.PIPE, shell=True) 
        p.wait()
        print("Putting permissions back to normal")
        print("Fixing some permissions")
        #p = subprocess.Popen('sudo chmod -R 755 /usr/local/bin', stdout=subprocess.PIPE, shell=True) 
        #p.wait()
        print("k3s installed")
        '''
        echo "Install kubernetes, k3s.io distribution"
        sudo curl -sfL https://get.k3s.io |  INSTALL_K3S_VERSION=v1.19.7+k3s1 sh -
        sudo cp /etc/rancher/k3s/k3s.yaml $HOME/k3s.yaml
        cd $HOME
        sudo chown -R $USER:$USER .
        mkdir .kube
        cp $HOME/k3s.yaml $HOME/.kube/config
        '''


def install_kubectl():
    if which("kubectl") == None:
        print("Installing kubectl on localhost")
        bash_script = '''
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x ./kubectl
        sudo mv ./kubectl /usr/local/bin/kubectl
        '''
        run_bash_string(bash_script)
        print("kubectl installed")
    else:
        print("kubectl is already installed")

def install_helm():
    if which("helm") == None:
        print("Installing Helm, a kubernetes package manager")
        bash_script = '''
        curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
        chmod 700 get_helm.sh
        ./get_helm.sh
        rm ./get_helm.sh
        '''
        run_bash_string(bash_script)
    else:
        print("helm is already installed")

def install_nfs_provisioner():
    print("Installing nfs-provisioner")
    bash_script = '''
    echo "Installing nfs-provisioner"
    sudo mkdir /mnt/nfsdir/provisioner
    helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner
    helm repo update
    helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
        --set nfs.server=127.0.0.1 \
        --set nfs.path=/mnt/nfsdir/provisioner
    '''
    run_bash_string(bash_script)


def install_cert_manager():
    print("Installing cert-manager")
    bash_script = '''
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
    '''
    run_bash_string(bash_script)

def configure_certificate_issuer():
    # TODO can't use bash for this
    '''
    echo "Configuring certificate issuer"
    cd Dentropycloud-Kubernetes/kube-apps/cert-manager
    if $USE_SELF_SIGNED; then
        echo "Creating self signed issuer"
        sudo kubectl apply -f ./cert-issuer-self-signed.yaml 
    else
        echo "Creating let's encrypt issuer"
        sed -i -e "s/personinternet@protonmail.com/$LETSENCRYPT_EMAIL/g" ./cert-issuer-traefik-ingress.yaml
        sudo kubectl apply -f ./cert-issuer-traefik-ingress.yaml
    fi
    '''

def install_trilium_notes():
    install_trilium_command = 'cd /home/%s/Dentropycloud-Kubernetes/kube-apps/trilium-notes && bash install-trilium-notes.sh' % getpass.getuser()
    subprocess.run(install_trilium_command.split(), capture_output=True)

sudo_pass = check_root()
install_dependencies()
env_vars = None
if os.path.exists("/home/%s/Dentropycloud-Kubernetes/.env" % getpass.getuser()):
    env_vars = import_env_file("/home/%s/Dentropycloud-Kubernetes/.env" % getpass.getuser())
else:
    env_vars = get_env_from_user()
configure_nfs_server()
install_k3s()
# install_kubectl()
# install_helm()
# install_nfs_provisioner()
# install_cert_manager()
# configure_certificate_issuer()
