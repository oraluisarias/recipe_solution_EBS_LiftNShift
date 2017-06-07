#!/bin/bash
#oracle
gse_admin_stagedir=$1
identityDomain=$2
targetIp=$3
host_name="oc-"`echo "$targetIp" | tr . -`

echo "ServerAliveInterval 100" > /home/oracle/.ssh/config

[ ! -f /home/oracle/.ssh/id_rsa ] && ssh-keygen -b 2048 -t rsa -f /home/oracle/.ssh/id_rsa -q -N ""
cat /home/oracle/.ssh/id_rsa.pub > /home/oracle/.ssh/authorized_keys

cd /u01
[ ! -d /u01/dbstg ] && mkdir /u01/dbstg
[ ! -d /u01/appstg ] && mkdir /u01/appstg

. /u01/install/APPS/EBSapps.env run
cd $gse_admin_stagedir/RemoteClone_v1.7
# perl ebsclone.pl

expect -c "spawn sh ${ADMIN_SCRIPTS_HOME}/adstpall.sh
expect \"APPS username:?\"
send \"apps\r\"
expect \"APPS password:?\"
send \"apps\r\"
expect \"WebLogic Server password:?\"
send \"welcome1\r\"
send \"\r\"
expect eof"

expect -c "spawn sh /u01/install/scripts/configwebentry.sh
expect \"Press any key to continue...\"
send \"\r\"
expect \"(Eg: https/http):?\"
send \" http\r\"
expect \"(Eg: public):?\"
send \"${host_name}\r\"
expect \"(Eg: domain.com):?\"
send \"compute.oraclecloud.com\r\"
expect \"(Eg: 443/80):?\"
send \"8000\r\"
expect \" /u01/install/APPS):?\"
send \"/u01/install/APPS\r\"
send \"\r\"
expect eof"


expect -c "spawn sh ${ADMIN_SCRIPTS_HOME}/adstrtal.sh
expect \"APPS username:?\"
send \"apps\r\"
expect \"APPS password:?\"
send \"apps\r\"
expect \"WebLogic Server password:?\"
send \"welcome1\r\"
send \"\r\"
expect eof"

expect -c "spawn sh /u01/install/APPS/scripts/enableDEMOusers.sh
expect \"Enter new password for DEMO users:?\"
send \"welcome1\r\"
expect \"Re-enter password for DEMO users:?\"
send \"welcome1\r\"
send \"\r\"
expect eof"

