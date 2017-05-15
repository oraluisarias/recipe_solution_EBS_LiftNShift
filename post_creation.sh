#!/bin/bash
gse_admin="gse-admin.oraclecloud.com"
identity_domain=$1
target_ip=$2

[ ! -f scripts/p22336899_R12_GENERIC.zip ] && cat scripts/p22336899_R12_GENERIC.zip* > scripts/p22336899_R12_GENERIC.zip
echo "Deleting existing ssh keys and authorized cache..."
ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'rm -rf /home/opc/.ssh/known_hosts ~/${identity_domain}'
echo "Uploading assets to gse admin..."
scp -o StrictHostKeyChecking=no -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:~/
echo "Preparing ssh key to connect to target instance (${target_ip})..."
ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'chmod 0400 ~/'${identity_domain}
echo "Uploading assets to target instance..."
ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i ~/'${identity_domain}' ~/oracle_ebs_workshop.sh ~/root_ebs_workshop.sh ~/p22336899_R12_GENERIC.zip opc@'${target_ip}':~/'
echo "Running root commands..."
ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i ~/'${identity_domain}' opc@'${target_ip}' "sudo nohup sh ~/root_ebs_workshop.sh &"'
echo "Running oracle commands..."
ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i ~/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"'nohup sh ~/oracle_ebs_workshop.sh &'"'"'"'