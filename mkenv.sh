#!/bin/bash

# sets up env in python 3.3 (no virtualenvwrapper support for now)

/usr/bin/python3.3 -m venv env
wget http://python-distribute.org/distribute_setup.py
env/bin/python distribute_setup.py
env/local/bin/easy_install pip
env/local/bin/pip install -r requirements.txt
rm -f distribute_setup.py
rm -f distribute*.tar.gz
