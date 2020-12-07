#!/bin/bash

virsh list --uuid >> ./uuid.txt
virsh list  | sed -n '3,$p' |awk '{print $3}' >> ./status.txt
for i in $(cat ./uuid.txt)
do
#  echo ${i}
  ping_result="virsh qemu-agent-command $i '{"execute":"guest-ping"}' 2>/dev/null | grep "return")"
  if [ "${ping_result}" == "" ]
  then
    echo 1 >> ./check.txt
    continue
  fi
  linux_get_cpu_result=$(virsh qemu-agent-command $i '{"execute":"guest-command-execute", "arguments":{"path":"qga_main cpu"}}' 2>/dev/null  | grep "true")
  windows_get_cpu_result=$(virsh qemu-agent-command $i '{"execute":"guest-command-execute", "arguments":{"path":"python qga_main cpu"}}' 2>/dev/null  | grep "true")
  #windows和linux类型的都为空时代表无法采集数据
  if [ ! -n "$linux_get_cpu_result"  ] && [ ! -n "$windows_get_cpu_result" ]
  then
    echo 1 >> ./check.txt
  else
    echo 0 >> ./check.txt
  fi
done
if [ -f ./uuid.txt ] && [ -f ./check.txt ] && [ -f ./status.txt ]
then
  paste -d" " ./uuid.txt ./status.txt ./check.txt >> ${HOSTNAME}_kvm_qga_check.txt
  sed -i '$d' ${HOSTNAME}_kvm_qga_check.txt
fi
rm -f ./status.txt
rm -f ./uuid.txt
rm -f ./check.txt


