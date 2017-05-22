#!/bin/bash
#oracle
. /u01/install/APPS/EBSapps.env run

echo "ServerAliveInterval 100" > /home/oracle/.ssh/config

[ ! -f /home/oracle/.ssh/id_rsa ] && ssh-keygen -b 2048 -t rsa -f /home/oracle/.ssh/id_rsa -q -N ""
cat /home/oracle/.ssh/id_rsa.pub > /home/oracle/.ssh/authorized_keys

cd /u01
[ ! -d /u01/dbstg ] && mkdir /u01/dbstg
[ ! -d /u01/appstg ] && mkdir /u01/appstg

source /u01/install/APPS/12.1.0/EBSDB_ebssource.env
sqlplus / as sysdba
select log_mode from v$database;
shutdown immediate
startup mount;
alter database archivelog;
alter database open;
select open_mode from v$database;
