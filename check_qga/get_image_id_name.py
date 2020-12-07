#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os


host_name = os.popen("hostname").read().strip()


def get_kvm_in_computer_info():
    with open('/opt/cloud/mon/agent/agent/all_qga_check_value', 'r') as f:
        data = f.readlines()
    for item in data:
        uuid = item.strip('\n').split()[0]
        cmd = 'nova show {}'.format(uuid)
        nova_show_data = os.popen(cmd).read().split("|")
        kvm_ip = 'execute_nova_show_error'
        kvm_hostname = 'execute_cinder_show_error'
        kvm_in_computer_host_name = 'execute_cinder_show_error'
        qga_config = 'execute_cinder_show_error'
        kvm_image_name = 'execute_cinder_show_error'
        kvm_image_id = 'execute_cinder_show_error'
        if nova_show_data:
            for i in nova_show_data:
                if "OS-EXT-SRV-ATTR:host" == i.strip():
                    index_val = nova_show_data.index(i)
                    host_name_index = index_val + 1
                    kvm_in_computer_host_name = nova_show_data[host_name_index].strip()
                if "network" in i.strip():
                    index_val = nova_show_data.index(i)
                    kvm_ip_index = index_val + 1
                    kvm_ip = nova_show_data[kvm_ip_index].strip()
                    if ":" in kvm_ip:
                        kvm_ip = '[]'
                if "OS-EXT-SRV-ATTR:hostname" == i.strip():
                    index_val = nova_show_data.index(i)
                    kvm_index = index_val + 1
                    kvm_hostname = nova_show_data[kvm_index].strip()
                if "os-extended-volumes:volumes_attached" == i.strip():
                    index_val = nova_show_data.index(i)
                    volume_index = index_val + 1
                    volume_id = nova_show_data[volume_index].split(',')[1].split(':')[1].split("\"")[1]
                    cinder_cmd = 'cinder show {}'.format(volume_id)
                    cinder_show_data = os.popen(cinder_cmd).read().split('|')
                    for k in cinder_show_data:
                        if "volume_image_metadata" == k.strip():
                            index_val = cinder_show_data.index(k)
                            val_index = index_val + 1
                            qga_config = cinder_show_data[val_index].split()[7].strip(",").strip("\'")
                            kvm_image_name = cinder_show_data[val_index].split()[13].strip(",").strip("\'")
                            kvm_image_id = cinder_show_data[val_index].split()[15].strip(",").strip("\'")

        kvm_controller_check = "{} {} {} {} {} {} {} {} {}\n".format(kvm_ip, kvm_hostname, item.strip('\n').split()[0],
                                                                   item.strip('\n').split()[1],kvm_image_name,
                                                                   kvm_image_id, qga_config, kvm_in_computer_host_name,
                                                                   item.strip('\n').split()[2])
        print kvm_controller_check
        with open('/root/{}_kvm_controller_check.txt'.format(host_name), 'a') as f:
            f.write(kvm_controller_check)


if __name__ == "__main__":
    get_kvm_in_computer_info()