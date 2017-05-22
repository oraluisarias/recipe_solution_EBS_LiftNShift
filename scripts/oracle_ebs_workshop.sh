#!/bin/bash
#oracle
gse_admin_stagedir=$1
identityDomain=$2
targetIp=$3

echo "ServerAliveInterval 100" > /home/oracle/.ssh/config

[ ! -f /home/oracle/.ssh/id_rsa ] && ssh-keygen -b 2048 -t rsa -f /home/oracle/.ssh/id_rsa -q -N ""
cat /home/oracle/.ssh/id_rsa.pub > /home/oracle/.ssh/authorized_keys

cd /u01
[ ! -d /u01/dbstg ] && mkdir /u01/dbstg
[ ! -d /u01/appstg ] && mkdir /u01/appstg

expect -c "spawn ssh oracle@oc-141-144-144-58.compute.oraclecloud.com
expect \"(yes/no)?\"
send \"yes\r\"
expect eof"

expect -c "spawn ssh oracle@ebssource.compute-gse00010217.oraclecloud.internal
expect \"(yes/no)?\"
send \"yes\r\"
expect eof"

expect -c "spawn ssh oracle@ebssource
expect \"(yes/no)?\"
send \"yes\r\"
expect eof"

source /u01/install/APPS/12.1.0/EBSDB_ebssource.env
sqlplus "/ as sysdba" <<'EOF'
select log_mode from v$database;
shutdown immediate
startup mount;
alter database archivelog;
alter database open;
select open_mode from v$database;
exit;
EOF

. /u01/install/APPS/EBSapps.env run
cd $gse_admin_stagedir/RemoteClone_v1.7
perl ebsclone.pl