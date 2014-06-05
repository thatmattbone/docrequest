#!/bin/bash

echo "don't use this...doesn't do anything anymore..."

##
# Setup envs for python 3 and python 2.
#
# Not doing this with virtualenvwrapper since it doesn't seem to have support
# for the env module in python 3.3 right now.
#


#wget http://python-distribute.org/distribute_setup.py
#
#echo setting up python3 env...
#if [ ! -e env3 ]
#then
#    python3.3 -m venv env3
#    env3/bin/python distribute_setup.py
#    env3/local/bin/easy_install pip
#fi
#env3/local/bin/pip install -r requirements3.txt
#cd pyramid_test_proj
#../env3/bin/python setup.py develop
#cd ..
#
#echo setting up python2 env...
#if [ ! -e env2 ]
#then
#    virtualenv -p `which python2.7` env2
#fi
#env2/bin/pip install -r requirements2.txt
#cd pyramid_test_proj
#../env2/bin/python setup.py develop
#cd ..
#
#
#rm -f distribute_setup.py
#rm -f distribute*.tar.gz
#
