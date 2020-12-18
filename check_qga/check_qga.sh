#!/bin/bash
PWD=$(cd `dirname $0`;pwd)
export ANSIBLE_HOST_KEY_CHECKING=False
tar -zxf $PWD/single.tar.gz
# 加载虚拟环境用来执行ansible剧本
source $PWD/single/bin/activate
# 删除原有的qga_matinode
if [ -f ./qga_matinode ]; then
  rm -rf ./qga_matinode
fi
# 删除原有qga检查生成的临时文件
if [ -f ./all_qga_check_value ]; then
  rm -rf ./all_qga_check_value
fi
# 创建qga_matinode
$PWD/single/bin/python $PWD/create_com_and_con_matinode.py
# 执行qga检查脚本
ansible-playbook -i $PWD/qga_matinode  $PWD/kvm_qga_check.yml   $*
sleep 1
# 整合qga检查文件
$PWD/single/bin/python $PWD/combine_qga_check_files.py
# 删除整合后的剩余文件
rm -rf $PWD/qga_check_value/*
# 检查虚拟机对应镜像
ansible-playbook -i $PWD/qga_matinode  $PWD/kvm_controller_check.yml   $*
# 生成文本
$PWD/single/bin/python $PWD/create_check_excel.py
rm -rf $PWD/image_check_value/*