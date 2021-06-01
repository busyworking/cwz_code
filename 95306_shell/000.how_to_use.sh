#对于图形化系统，打开远程控制页面虚拟键盘
点击Alt+Ctrl+F2

# 寻找Udisk,并挂载
lsblk
mount /dev/sdb2 /mount

# cp文件
cp sudo-1.8.23-10.el7.x86_64.rpm /tmp
cp -a 95306_shell /tmp

#根据操作系统版本拷贝相应packages，执行配置脚本

#关系型数据库-config_os_relation_db
cp -a rhel7u9 /media
sh /tmp/95306_shell/config_os_relation_db.sh

#非关系型数据-config_os_non_relation_db
cp -a rhel7u9 /media
sh /tmp/95306_shell/config_os_non_relation_db.sh

#备份服务器-config_os_backup_server
cp -a rhel7u4 /media
sh /tmp/95306_shell/config_os_backup_server.sh

#铁信云-config_os_srcloud
cp -a rhel7u3 /media
sh /tmp/95306_shell/config_os_srcloud.sh

#安全平台服务器-config_os_security_platform_server
cp -a rhel7u6 /media
sh /tmp/95306_shell/config_os_security_platform_server.sh