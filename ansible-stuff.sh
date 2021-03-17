
# Install pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py
# Insatll ansible
python3 -m pip install --user ansible
# Install ansible role xanmanning.k3s
ansible-galaxy install xanmanning.k3s
# Run install script
python3 server-install.py
