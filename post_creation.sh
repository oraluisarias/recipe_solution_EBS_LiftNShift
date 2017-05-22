#!/bin/bash
gse_admin="gse-admin.oraclecloud.com"
identity_domain=$1
target_ip=$2
gse_admin_stagedir="/app/EBS_LiftNShift/"${identity_domain}

mkdir scripts/${identity_domain}
python update_properties.py ${identity_domain}

[ ! -f scripts/p22336899_R12_GENERIC.zip ] && cat scripts/p22336899_R12_GENERIC.zip* > scripts/p22336899_R12_GENERIC.zip
echo "Deleting existing ssh keys and authorized cache..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'sudo mkdir -p '${gse_admin_stagedir}' && sudo chown opc:opc '${gse_admin_stagedir}' && sudo chmod 777 '${gse_admin_stagedir}' && rm -rf /home/opc/.ssh/known_hosts '${gse_admin_stagedir}'/'${identity_domain}
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'sudo mkdir -p '${gse_admin_stagedir}' && sudo chown opc:opc '${gse_admin_stagedir}' && sudo chmod 777 '${gse_admin_stagedir}' && rm -rf /home/opc/.ssh/known_hosts '${gse_admin_stagedir}'/'${identity_domain}

echo "Uploading assets to gse admin..."
echo scp -o StrictHostKeyChecking=no -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/${identity_domain}/cln.props scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:${gse_admin_stagedir}
     scp -o StrictHostKeyChecking=no -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/${identity_domain}/cln.props scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:${gse_admin_stagedir}

echo "Preparing ssh key to connect to target instance (${target_ip})..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'chmod 0400 '${gse_admin_stagedir}'/'${identity_domain}
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'chmod 0400 '${gse_admin_stagedir}'/'${identity_domain}

echo "Uploading assets to target instance..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "sudo mkdir -p '${gse_admin_stagedir}'"'
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "sudo mkdir -p '${gse_admin_stagedir}'"'

echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' '${gse_admin_stagedir}'/cln.props '${gse_admin_stagedir}'/oracle_ebs_workshop.sh '${gse_admin_stagedir}'/root_ebs_workshop.sh '${gse_admin_stagedir}'/p22336899_R12_GENERIC.zip opc@'${target_ip}':'${gse_admin_stagedir}
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' '${gse_admin_stagedir}'/cln.props '${gse_admin_stagedir}'/oracle_ebs_workshop.sh '${gse_admin_stagedir}'/root_ebs_workshop.sh '${gse_admin_stagedir}'/p22336899_R12_GENERIC.zip opc@'${target_ip}':'${gse_admin_stagedir}

echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "cd '${gse_admin_stagedir}' && sudo unzip -o p22336899_R12_GENERIC.zip && sudo chown oracle:dba -R '${gse_admin_stagedir}' && sudo chmod 777 -R '${gse_admin_stagedir}' && cp RemoteClone_v1.7/cln.props RemoteClone_v1.7/cln.props.ORIG && cp cln.props RemoteClone_v1.7/cln.props"'
	 ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "cd '${gse_admin_stagedir}' && sudo unzip -o p22336899_R12_GENERIC.zip && sudo chown oracle:dba -R '${gse_admin_stagedir}' && sudo chmod 777 -R '${gse_admin_stagedir}' && cp RemoteClone_v1.7/cln.props RemoteClone_v1.7/cln.props.ORIG && cp cln.props RemoteClone_v1.7/cln.props"'
	 
echo "Running oracle workshop commands..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"''${gse_admin_stagedir}'/oracle_ebs_workshop.sh'"'"'"'
	 ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"''${gse_admin_stagedir}'/oracle_ebs_workshop.sh'"'"'"'

echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"'perl '${gse_admin_stagedir}'/RemoteClone_v1.7/ebsclone.pl'"'"'"'
	 ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${target_ip}' "sudo su - oracle -c '"'"'perl '${gse_admin_stagedir}'/RemoteClone_v1.7/ebsclone.pl'"'"'"'

