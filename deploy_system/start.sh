#!/bin/bash
PWD=$(cd `dirname $0`;pwd)
export ANSIBLE_HOST_KEY_CHECKING=False
tar -zxf $PWD/single.tar.gz
source $PWD/single/bin/activate

ansible-playbook -i $PWD/deploy_matinode  $PWD/deploy_system.yml   $*