#!/bin/bash

gse_admin="gse-admin.oraclecloud.com"
source_ip=$1

echo "Executing a wget to the newly created EBS tier"
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'wget -T 8 -t 3 http://'${source_ip}':8000'
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'wget -T 8 -t 3 http://'${source_ip}':8000'
