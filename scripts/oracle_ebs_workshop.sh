#oracle
. /u01/install/APPS/EBSapps.env run

expect -c "spawn /u01/install/APPS/fs1/inst/apps/EBSDB_ebssource/admin/scripts/adstpall.sh -skipNM -skipAdmin" #oracle
expect \"username:\"
send \"apps\r\"
expect \"APPS password:\"
send \"apps\r\"
expect \"Server password:\"
send \"welcome1\r\"

expect -c "spawn perl /u01/install/APPS/fs1/EBSapps/appl/fnd/12.0.0/patch/115/bin/txkUpdateEBSDomain.pl -action=updateAdminPassword" #oracle
send \"Yes\r\"
send \"\r\"
send \"welcome1\r\"
send \"welcome1\r\"
send \"apps\r\"

expect -c "spawn /u01/install/APPS/fs1/inst/apps/EBSDB_ebssource/admin/scripts/adstrtal.sh"
expect \"username:\"
send \"apps\r\"
expect \"APPS password:\"
send \"apps\r\"
expect \"Server password:\"
send \"welcome1\r\"

. /u01/install/APPS/EBSapps.env run
mkdir -p ~/logs
cd ~/logs

expect -c "spawn /u01/install/APPS/scripts/enableSYSADMIN.sh"
expect \"new password for SYSADMIN:\"
send \"welcome1\r\"
expect \"enter password for SYSADMIN:\"
send \"welcome1\r\"

expect -c "spawn /u01/install/APPS/scripts/enableDEMOusers.sh"
expect \"new password for SYSADMIN:\"
send \"welcome1\r\"
expect \"enter password for SYSADMIN:\"
send \"welcome1\r\"

echo "ServerAliveInterval 100" >/home/oracle/.ssh/config
ServerAliveInterval 100

cd /u01
mkdir /u01/dbstg
mkdir /u01/appstg