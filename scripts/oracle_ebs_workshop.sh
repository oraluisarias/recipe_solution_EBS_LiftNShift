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

# expect -c "spawn ssh oracle@oc-141-144-144-58.compute.oraclecloud.com
# expect \"(yes/no)?\"
# send \"yes\r\"
# expect eof"

# expect -c "spawn ssh oracle@ebssource.compute-gse00010217.oraclecloud.internal
# expect \"(yes/no)?\"
# send \"yes\r\"
# expect eof"

# expect -c "spawn ssh oracle@ebssource
# expect \"(yes/no)?\"
# send \"yes\r\"
# expect eof"

# source /u01/install/APPS/12.1.0/EBSDB_ebssource.env
# sqlplus "/ as sysdba" <<'EOF'
# select log_mode from v$database;
# shutdown immediate
# startup mount;
# alter database archivelog;
# alter database open;
# select open_mode from v$database;
# exit;
# EOF

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
expect \"(https/http):?\"
send \"http\r\"
expect \"public):?\"
send \"${host_name}\r\"
expect \"domain.com):?\"
send \"compute.oraclecloud.com\r\"
expect \"443/80):?\"
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

