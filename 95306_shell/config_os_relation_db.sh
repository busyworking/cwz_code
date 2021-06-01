#!/bin/bash

#config hostname
my_serial=$(dmidecode -t system | grep -i "serial number" | awk '{print $3}')
hostname=$(cat /tmp/95306_shell/sn_hostname.txt | grep $my_serial | awk '{print $2}')
hostnamectl set-hostname $hostname

#config repo
mkdir -p /etc/yum.repos.d/bak
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak
touch /etc/yum.repos.d/localmedia.repo
echo '''[local_media]
name=rhel7u8
baseurl=file:///media/rhel7u8
gpgcheck=0
enabled=1''' > /etc/yum.repos.d/localmedia.repo

#disable services
systemctl stop firewalld NetworkManager ksm ksmtured
systemctl disable firewalld NetworkManager ksm ksmtured

#disable selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

#config users
echo "Lkj@8970" | passwd --stdin root
groupadd -g 510 itsm
useradd -u 510 -g 510 -d /itsm itsm
echo "Itsm@123" | passwd --stdin itsm
chown -R itsm:itsm /itsm
groupadd -g 610 yunwei
useradd -u 610 -g 610 yunwei
echo "Lkj@8970" | passwd --stdin yunwei 

groupadd -g 900 oinstall
groupadd -g 901 dba
useradd -u 900 -g 900 -G 901 oracle
useradd -u 901 -g 900 -G 901 grid

echo "q1w2e3r4" | passwd --stdin oracle
echo "q1w2e3r4" | passwd --stdin grid

#config kernel
echo "oracle hard   nofile 65535" >> /etc/security/limits.conf
echo "oracle soft   nofile 65535" >> /etc/security/limits.conf
echo "vm.min_free_kbytes = 4194303" >> /etc/sysctl.conf
echo "vm.nr_hugepages=150000" >> /etc/sysctl.conf
echo "kernel.sysrq = 1" >> /etc/sysctl.conf
echo "kernel.unknown_nmi_panic = 1" >> /etc/sysctl.conf

#update sudo
chmod 700 /tmp/sudo-1.8.23-10.el7_9.1.x86_64.rpm
rpm -Uvh /tmp/sudo-1.8.23-10.el7_9.1.x86_64.rpm

#catch mac & wwn
hostname >> /tmp/mac.$(cat /etc/hostname).txt
ip a >> /tmp/mac.$(cat /etc/hostname).txt
cat /sys/class/fc_host/host14/port_name >> /tmp/mac.$(cat /etc/hostname).txt
cat /sys/class/fc_host/host15/port_name >> /tmp/mac.$(cat /etc/hostname).txt
cat /sys/class/fc_host/host16/port_name >> /tmp/mac.$(cat /etc/hostname).txt
cat /sys/class/fc_host/host17/port_name >> /tmp/mac.$(cat /etc/hostname).txt

#config ntp
yum install -y ntp
sed -i 's/server/#server/' /etc/ntp.conf
sed -i 's/OPTIONS="-g"/#OPTIONS="-g"/' /etc/sysconfig/ntpd
echo "OPTIONS=\" -x -u ntp:ntp -p /var/run/ntpd.pid -g\"" >> /etc/sysconfig/ntpd
echo "server 10.3.103.27 iburst" >>  /etc/ntp.conf
echo "server 10.3.103.28 iburst" >>  /etc/ntp.conf
systemctl enable ntpd
systemctl disable chronyd

reboot
