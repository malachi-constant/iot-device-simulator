#!/bin/bash
set -x
yum install -y jq
yum install -y python3
yum install -y git
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip3 install boto3
aws s3 cp s3://simulator-keys/mojio-sim.pem /root/.ssh/id_rsa
chmod 400 /root/.ssh/id_rsa

aws s3 cp s3://lucas-simulator/simulator simulator/ --recursive
# git clone git@gitlab.com:missioncloud/proserv/mojio-simulator.git
