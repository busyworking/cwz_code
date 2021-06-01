#!/bin/bash

#config hostname
my_serial=$(dmidecode -t system | grep -i "serial number" | awk '{print $3}')
hostname=$(cat /tmp/95306_shell/sn_hostname.txt | grep $my_serial | awk '{print $2}')
hostnamectl set-hostname $hostname