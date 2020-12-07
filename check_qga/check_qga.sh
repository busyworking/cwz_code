#!/bin/bash
PWD=$(cd `dirname $0`;pwd)
export ANSIBLE_HOST_KEY_CHECKING=False
tar -zxf $PWD/single.tar.gz
source $PWD/single/bin/activate
if [ -f ./qga_matinode ]; then
  rm -rf ./qga_matinode
fi

if [ -f ./all_qga_check_value ]; then
  rm -rf ./all_qga_check_value
fi
$PWD/single/bin/python $PWD/create_com_and_con_matinode.py

ansible-playbook -i $PWD/qga_matinode  $PWD/kvm_qga_check.yml   $*

sleep 1

$PWD/single/bin/python $PWD/combine_qga_check_files.py
rm -rf $PWD/qga_check_value/*

ansible-playbook -i $PWD/qga_matinode  $PWD/kvm_controller_check.yml   $*

$PWD/single/bin/python $PWD/create_check_excel.py
rm -rf $PWD/image_check_value/*