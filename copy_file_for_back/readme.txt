#脚本使用说明
# 本脚本将2.5.13版本mon的大文件比如rrd，postgres的数据目录进程远程备份，考虑到武清环境磁盘空间有限，故采用分批打包、发送的方式来备份
# 使用方式：
#     1.拷贝本脚本至需要备份的服务器上
#     2.修改脚本中des_ip参数，本参数为备份机器的ip
#     3.手动操作使本机器与目标机器免密，具体命令如下
#         ssh-keygen -t rsa #一路回车至结束
#         ssh-copy-id -i ~/.ssh/id_rsa.pub [romte_ip]
#     4.在远程服务器上创建备份目录，建议同需要备份的目录一致如：/home/psql_data/base和/home/cloud-data/6070
#     5.执行 python copy_file_for_back.py  脚本执行完毕不报错即可
#     6.验证远程服务器上是否存在备份文件
