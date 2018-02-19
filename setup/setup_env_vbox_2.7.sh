#!/usr/bin/env bash

# Must run this script from Vagrant /vagrant
# Tested on a Mac with Vagrant

echo "This will set up a python virtual environment inside Vagrant with python 2.7 and include all the required packages for SimPrily."
echo "This script must be run from inside Vagrant."
echo "This script requires sudo privileges and apt-get.
If you do not have sudo privileges or cannot install apt-get see the SimPrily documentation for other options.
http://simprily.readthedocs.io/en/latest/install.html#environment-set-up"

sleep 5

set -e # quits at first error

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-virtualenv git python-dev
sudo easy_install -U distribute
cd ~
virtualenv simprily_env
source ~/simprily_env/bin/activate
pip install --upgrade pip
pip install pip-tools
cd /vagrant
pip-sync

echo ""
echo "###################################"
echo ""
echo "Finished installing"
echo "SimPrily should be run like this:"
echo "~/simprily_env/bin/python simprily.py"
echo ""
~/simprily_env/bin/python simprily.py --help