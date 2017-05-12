#!/bin/bash

admin_username="gse-admin_ww@oracle.com"
cloud_username="cloud.admin"
gse_admin="gse-admin.oraclecloud.com"
identity_domain=$1
zone=$2
datacenter=$3

#Add the allow_all security list
echo "***************************************************************************************"
echo "Step 1 - Creating an open security list for the domain (allow_all)"
echo "***************************************************************************************"
python create_open_seclist.py $identity_domain $zone $datacenter

#Run RT script (selenium)
echo "***************************************************************************************"
echo "Step 2 - Installing required VMs from Market Place via selenium"
echo "***************************************************************************************"
python install_marketplace_images_WD.py $identity_domain $zone $datacenter

#Create ssh key and upload to demo central
echo "***************************************************************************************"
echo "Step 3 - Creating a new ssh key and uploading to Demo Central"
echo "***************************************************************************************"
chmod 0400 ssh_keys/*
rm -rf ssh_keys/${identity_domain}*
[ ! -f ssh_keys/${identity_domain} ] && ssh-keygen -b 2048 -t rsa -f ssh_keys/${identity_domain} -q -N ""
python update_ssh_key_2_demo_central.py $identity_domain $zone $datacenter

#Create source instance
echo "***************************************************************************************"
echo "Step 4 - Creating EBS source instance and waiting until it starts"
echo "***************************************************************************************"
rm -rf ips/${identity_domain}
python create_source_vm.py $identity_domain $zone $datacenter
target_ip=`cat ips/${identity_domain}`
echo "***************************************************************************************"
echo "Instance finally started, public IP: ${target_ip}" 
echo "***************************************************************************************"

#Upload and execute configuration script to source instance 
echo "***************************************************************************************"
echo "Step 5 - Running workshop commands on the new VM, using gse-admin as bridge"
echo "***************************************************************************************"
[ ! -f scripts/p22336899_R12_GENERIC.zip ] && cat scripts/p22336899_R12_GENERIC.zip* > scripts/p22336899_R12_GENERIC.zip
echo scp -o StrictHostKeyChecking=no -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:~/
scp -o StrictHostKeyChecking=no -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:~/
ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'rm -rf /home/opc/.ssh/known_hosts && chmod 0400 ~/'${identity_domain}
echo ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i ~/'${identity_domain}' ~/oracle_ebs_workshop.sh ~/root_ebs_workshop.sh ~/p22336899_R12_GENERIC.zip opc@'${target_ip}':~/'
ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i ~/'${identity_domain}' ~/oracle_ebs_workshop.sh ~/root_ebs_workshop.sh ~/p22336899_R12_GENERIC.zip opc@'${target_ip}':~/'
echo ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i ~/'${identity_domain}' opc@'${target_ip}' "sudo nohup sh ~/root_ebs_workshop.sh &"'
ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i ~/'${identity_domain}' opc@'${target_ip}' "sudo nohup sh ~/root_ebs_workshop.sh &"'
echo ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i ~/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"'nohup sh ~/oracle_ebs_workshop.sh &'"'"'"'
ssh -o StrictHostKeyChecking=no  -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i ~/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"'nohup sh ~/oracle_ebs_workshop.sh &'"'"'"'