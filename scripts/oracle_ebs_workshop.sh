#!/bin/bash
#oracle
targetIp=$1
targetIpHOST="oc-"`echo "$targetIp" | tr . -`

echo "Configuring web Tier for domain ${targetIpHOST}"
echo "ServerAliveInterval 100" > /home/oracle/.ssh/config

[ ! -f /home/oracle/.ssh/id_rsa ] && ssh-keygen -b 2048 -t rsa -f /home/oracle/.ssh/id_rsa -q -N ""
cat /home/oracle/.ssh/id_rsa.pub > /home/oracle/.ssh/authorized_keys

cd /u01
[ ! -d /u01/dbstg ] && mkdir /u01/dbstg
[ ! -d /u01/appstg ] && mkdir /u01/appstg

# node_info_file='/u01/install/APPS/fs1/FMW_Home/Oracle_EBS-app1/applications/oacore/APP-INF/node_info.txt'
. /u01/install/APPS/EBSapps.env run
while [ ! $? -eq 0 ]
do
	echo "Waiting for EBS to initialize ..."	
	sleep 60
	. /u01/install/APPS/EBSapps.env run	
done

echo "Waiting 10 more minutes for EBS to start..."
sleep 600


expect -c "spawn sh ${ADMIN_SCRIPTS_HOME}/adstpall.sh
expect \"APPS username:\"
send \"apps\r\"
expect \"APPS password:\"
send \"apps\r\"
expect \"WebLogic Server password:\"
send \"welcome1\r\"
send \"\r\""

. /u01/install/APPS/EBSapps.env run	
expect -c "set timeout 1000
spawn sh /u01/install/scripts/configwebentry.sh
expect \"Press any key to continue...\"
send \"\r\"
expect \"(Eg: https/http):\"
send \" http\r\"
expect \"(Eg: public):\"
send \"$targetIpHOST\r\"
expect \"(Eg: domain.com):\"
send \"compute.oraclecloud.com\r\"
expect \"(Eg: 443/80):\"
send \"8000\r\"
expect \"/u01/install/APPS):\"
send \"/u01/install/APPS\r\"
expect \"Press any key to continue...\"
send \"\r\"
expect \"Enter the APPS user password:\"
send \"apps\r\"
expect eof"
# sleep 240

expect -c "set timeout 1000
spawn sh /u01/install/APPS/scripts/enableDEMOusers.sh
expect \"Enter new password for DEMO users:\"
send \"welcome1\r\"
expect \"Re-enter password for DEMO users:\"
send \"welcome1\r\"
send \"\r\"
expect eof"
# sleep 120


. /u01/install/APPS/EBSapps.env run	
expect -c "set timeout 1000
spawn sh ${ADMIN_SCRIPTS_HOME}/adstrtal.sh
expect \"APPS username:\"
send \"apps\r\"
expect \"APPS password:\"
send \"apps\r\"
expect \"WebLogic Server password:\"
send \"welcome1\r\"
send \"\r\"
expect eof"