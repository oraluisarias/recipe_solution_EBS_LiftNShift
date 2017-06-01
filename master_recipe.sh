#!/bin/bash

admin_username="gse-admin_ww@oracle.com"
cloud_username="cloud.admin"
gse_admin="gse-admin.oraclecloud.com"
identity_domain=$1
zone=$2
datacenter=$3
executionPath=$4
password=$5
cd $executionPath
if [ -f cache/$identity_domain/zone ] ; then
	zone=`cat cache/$identity_domain/zone`
else
	mkdir -p cache/$identity_domain
	echo zone > cache/$identity_domain/zone
	echo "Found zone ${zone} value on cache"
fi
if [ -f cache/$identity_domain/datacenter ] ; then
	datacenter=`cat cache/$identity_domain/datacenter`
else
	mkdir -p cache/$identity_domain
	echo datacenter > cache/$identity_domain/datacenter
	echo "Found datacenter ${datacenter} value on cache"
fi
#Add the allow_all security list
echo "***************************************************************************************"
echo "Step 1 - Creating an open security list for the domain (allow_all)"
echo "***************************************************************************************"
python create_open_seclist.py $identity_domain $zone $datacenter

#Run RT script (selenium)
echo "***************************************************************************************"
echo "Step 2 - Installing required VMs from Market Place via selenium"
echo "***************************************************************************************"
export PATH=$PATH:${executionPath}
# python install_marketplace_images_WD.py $identity_domain $zone $datacenter
# curl -X POST -d 'identity_domain='identity_domain'&datacenter='datacenter'&password='password http://gse-admin.oraclecloud.com:7002/install_EBS_marketplace_images
curl -X POST -d 'identity_domain='identity_domain'&datacenter='datacenter'&password='password http://gse-admin.oraclecloud.com:7002/install_marketplace_images
sleep 60
#Create ssh key and upload to demo central
echo "***************************************************************************************"
echo "Step 3 - Creating a new ssh key and uploading to Demo Central"
echo "***************************************************************************************"
chmod 0400 ssh_keys/*
# [ ! -f ssh_keys/${identity_domain} ] && ssh-keygen -b 2048 -t rsa -f ssh_keys/${identity_domain} -q -N ""
# python update_ssh_key_2_demo_central.py $identity_domain $zone $datacenter
rm -rf ips/${identity_domain}*
cp ssh_keys/gse_admin ssh_keys/${identity_domain}
cp ssh_keys/gse_admin.pub ssh_keys/${identity_domain}.pub

#Create source instance
echo "***************************************************************************************"
echo "Step 4 - Creating EBS source instance and waiting until it starts"
echo "***************************************************************************************"
rm -rf ips/${identity_domain}
python create_source_vm.py $identity_domain $zone $datacenter
python create_tools_vm.py $identity_domain $zone $datacenter
source_ip=`cat ips/${identity_domain}`
tools_ip=`cat ips/tools_${identity_domain}`
if [ "$source_ip" != "" ] && [ "$tools_ip" != "" ] ; then
	echo "***************************************************************************************"
	echo "Instance finally started, source public IP: ${source_ip}, tools public IP: ${tools_ip}" 
	echo "***************************************************************************************"

	#Upload and execute configuration script to source instance 
	echo "***************************************************************************************"
	echo "Step 5 - Running workshop commands on the new VM, using gse-admin as bridge"
	echo "***************************************************************************************"
	sh post_creation.sh ${identity_domain} ${source_ip} ${tools_ip} ${executionPath}	
fi