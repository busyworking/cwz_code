#!/bin/bash

#catch mac
hostname >> /tmp/mac.$(cat /etc/hostname).txt
ip a >> /tmp/mac.$(cat /etc/hostname).txt