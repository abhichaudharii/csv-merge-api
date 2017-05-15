#!/usr/bin/env bash

if [ -z ${1} ];
then
  echo "Port Number not found!"
  echo " "
  echo " "
  echo "Correct usage is : "
  echo "sudo -H ./setup.sh <port_no>"
  exit
fi

if [ ${1} -lt 0 ] || [ ${1} -gt 65535 ]
then
  echo "Port Number must be in the range 0-65535"
  exit
fi

if [ $(dpkg-query -W -f='${Status}' python2.7 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt-get install python2.7;
fi

if [ $(dpkg-query -W -f='${Status}' python-pip 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt-get install python-pip;
fi

pip install virtualenv

if [ $(ls -ax | grep -c .api_runtime_env) -ne 1 ];
then
  echo "Building virtual environment..."
  mkdir .api_runtime_env
  virtualenv .api_runtime_env
  echo "Virtual Environment Successfully built!"
fi

echo "Starting virtual environment..."
source .api_runtime_env/bin/activate
echo "Installing Dependencies..."
pip install -r requirements.txt

export FLASK_APP=src/app.py
flask run -p ${1}
