#/bin/bash

cd ..
python3 entry.py
cd extra
ansible-playbook -i host.ini playbook.yaml