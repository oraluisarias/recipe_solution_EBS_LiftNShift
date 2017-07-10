#!/bin/bash
identity_domain=$1
ipHOST=$2
gse_admin_stagedir="/app/EBS_LiftNShift/"${identity_domain}

# dos2unix $gse_admin_stagedir/change_fqdn.sh
# sh $gse_admin_stagedir/change_fqdn.sh "$ipHOST.compute.oraclecloud.com"
yum install -y expect 
# yum install -y curl tar gcc gcc-c++ openssl-devel wget xz make tcl expect dos2unix #root
# cp /home/opc/.ssh/authorized_keys /home/oracle/.ssh/authorized_keys #root
# chown oracle:oinstall /home/oracle/.ssh/authorized_keys #root

chmod 777 $gse_admin_stagedir/oracle_ebs_workshop.sh
# chmod 777 $gse_admin_stagedir/oracle_ebs_workshop.sh
# unzip -o $gse_admin_stagedir/p22336899_R12_GENERIC.zip
# chown oracle:dba -R $gse_admin_stagedir
# chmod 777 -R $gse_admin_stagedir
# cp -rf RemoteClone_v1.7/cln.props $gse_admin_stagedir/cln.props.ORIG
# cp -rf $gse_admin_stagedir/cln.props RemoteClone_v1.7/cln.props

# if [ -f /u01/install/APPS/apps-unlimited-ebs/ProvisionEBS.xml ] && [ -f $gse_admin_stagedir/ProvisionEBS.xml ] ; then
# 	mv /u01/install/APPS/apps-unlimited-ebs/ProvisionEBS.xml /u01/install/APPS/apps-unlimited-ebs/ProvisionEBS.xml.ORIG 
# 	cp $gse_admin_stagedir/ProvisionEBS.xml /u01/install/APPS/apps-unlimited-ebs/ProvisionEBS.xml
# fi