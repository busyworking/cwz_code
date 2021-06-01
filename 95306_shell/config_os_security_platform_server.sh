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
name=rhel7u6
baseurl=file:///media/rhel7u6
gpgcheck=0
enabled=1''' > /etc/yum.repos.d/localmedia.repo

#disable services
service rhnsd stop
chkconfig rhnsd off

systemctl stop bluetooth.target
systemctl disable bluetooth.target

systemctl stop bluetooth.service
systemctl disable bluetooth.service

systemctl stop cups.path
systemctl disable cups.path

systemctl stop cups.socket
systemctl disable cups.socket

systemctl stop cups.service 
systemctl disable cups.service 

systemctl stop firewalld.service
systemctl disable firewalld.service

systemctl stop dev-mqueue.mount   
systemctl disable dev-mqueue.mount

systemctl stop postfix.service   
systemctl disable postfix.service   

systemctl stop postfix.service   
systemctl disable postfix.service   
  
systemctl stop avahi-daemon.socket   
systemctl disable avahi-daemon.socket 
  
systemctl stop avahi-daemon.service   
systemctl disable avahi-daemon.service  

systemctl stop wpa_supplicant.service     
systemctl disable wpa_supplicant.service  

systemctl stop dnsmasq.service     
systemctl disable dnsmasq.service  

systemctl stop ModemManager.service     
systemctl disable ModemManager.service  

systemctl stop rhsmcertd.service     
systemctl disable rhsmcertd.service  

systemctl stop alsa-state.service     
systemctl disable alsa-state.service 

#disable selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

#config users
echo "Lkj@8970" | passwd --stdin root
#groupadd -g 510 itsm
#useradd -u 510 -g 510 -d /itsm itsm
#echo "Itsm@123" | passwd --stdin itsm
#groupadd -g 610 yunwei
#useradd -u 610 -g 610 yunwei
#echo "Lkj@8970" | passwd --stdin yunwei 

#update sudo
chmod 700 /tmp/sudo-1.8.23-10.el7_9.1.x86_64.rpm
rpm -Uvh /tmp/sudo-1.8.23-10.el7_9.1.x86_64.rpm

#catch mac
hostname >> /tmp/mac.$(cat /etc/hostname).txt
ip a >> /tmp/mac.$(cat /etc/hostname).txt

#config ntp
#sed -i 's/server/#server/' /etc/ntp.conf
#sed -i 's/OPTIONS="-g"/#OPTIONS="-g"/' /etc/sysconfig/ntpd
#echo "OPTIONS=\" -x -u ntp:ntp -p /var/run/ntpd.pid -g\"" >> /etc/sysconfig/ntpd
#echo "server 10.3.103.27 iburst" >>  /etc/ntp.conf
#echo "server 10.3.103.28 iburst" >>  /etc/ntp.conf
#systemctl enable ntpd
#systemctl disable chronyd

reboot

