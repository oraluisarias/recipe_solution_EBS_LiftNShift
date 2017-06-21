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

echo "***************************************************************************************"
echo "Step 0 - Getting Demo Central cloud.admin password"
echo "***************************************************************************************"
password=`python getDemoCentralPWD.py ${identity_domain}`
echo "Found password: ${password}"
#Run RT script (selenium)
echo "***************************************************************************************"
echo "Step 1 - Installing required VMs from Market Place via selenium"
echo "***************************************************************************************"
export PATH=$PATH:${executionPath}
# python install_marketplace_images_WD.py $identity_domain $zone $datacenter
# curl -X POST -d 'identity_domain='identity_domain'&datacenter='datacenter'&password='password http://gse-admin.oraclecloud.com:7002/install_EBS_marketplace_images
curl -X POST -d "identity_domain=${identity_domain}&password=${password}" http://gse-admin.oraclecloud.com:7002/install_marketplace_images
sleep 120

#Add the allow_all security list
echo "***************************************************************************************"
echo "Step 2 - Finding source and Datacenter"
echo "***************************************************************************************"
mkdir -p $executionPath/cache/$identity_domain
touch $executionPath/cache/$identity_domain/zone && chmod 777 $executionPath/cache/$identity_domain/zone
touch $executionPath/cache/$identity_domain/datacenter && chmod 777 $executionPath/cache/$identity_domain/datacenter
python getZoneDatacenter.py $identity_domain

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
echo "Step 3 - Creating an open security list for the domain (allow_all)"
echo "***************************************************************************************"
python create_open_seclist.py $identity_domain $zone $datacenter


#Create ssh key and upload to demo central
echo "***************************************************************************************"
echo "Step 4 - Creating a new ssh key and uploading to Demo Central"
echo "***************************************************************************************"
chmod 0400 ssh_keys/*
# [ ! -f ssh_keys/${identity_domain} ] && ssh-keygen -b 2048 -t rsa -f ssh_keys/${identity_domain} -q -N ""
# python update_ssh_key_2_demo_central.py $identity_domain $zone $datacenter
rm -rf ssh_keys/${identity_domain}*
cp ssh_keys/gse_admin ssh_keys/${identity_domain}
cp ssh_keys/gse_admin.pub ssh_keys/${identity_domain}.pub

#Create source instance
echo "***************************************************************************************"
echo "Step 5 - Creating EBS source instance and waiting until it starts"
echo "***************************************************************************************"
rm -rf ips/${identity_domain}
# python clean_source_vm.py $identity_domain $zone $datacenter
python create_vision_vm.py $identity_domain $zone $datacenter ebscloud
source_ip=`cat ips/${identity_domain}`
tools_ip=1
if [ "$source_ip" != "" ] ; then
	echo "***************************************************************************************"
	echo "Instance finally started, vision public IP: ${source_ip} " 
	echo "***************************************************************************************"

	#Upload and execute configuration script to source instance 
	echo "***************************************************************************************"
	echo "Step 6 - Running workshop commands on the new VM, using gse-admin as bridge"
	echo "***************************************************************************************"
	echo python update_properties.py ${identity_domain}
	python update_properties.py ${identity_domain}
	echo sh post_creation.sh ${identity_domain} ${source_ip} ${tools_ip} ${executionPath}	
	sh post_creation.sh ${identity_domain} ${source_ip} ${tools_ip} ${executionPath}	
fi