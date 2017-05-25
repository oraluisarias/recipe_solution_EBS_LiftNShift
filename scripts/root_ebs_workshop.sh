#!/bin/bash
yum update -y #root
yum install -y curl tar gcc gcc-c++ openssl-devel wget xz make tcl expect #root
cp /home/opc/.ssh/authorized_keys /home/oracle/.ssh/authorized_keys #root

chown oracle:oinstall /home/oracle/.ssh/authorized_keys #root
cp /home/opc/.ssh/authorized_keys  /home/oracle/.ssh/authorized_keys #root
