#!/bin/bash
gse_admin="gse-admin.oraclecloud.com"
identity_domain=$1
source_ip=$2
executionPath=$3
targetIpHOST="oc-"`echo "$source_ip" | tr . -`
gse_admin_stagedir="/app/EBS_LiftNShift/"${identity_domain}

cd $executionPath
mkdir -p scripts/${identity_domain}

[ ! -f scripts/p22336899_R12_GENERIC.zip ] && cat scripts/p22336899_R12_GENERIC.zip* > scripts/p22336899_R12_GENERIC.zip
echo "Deleting existing ssh keys and authorized cache..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'sudo mkdir -p '${gse_admin_stagedir}' && sudo chown opc:opc '${gse_admin_stagedir}' && sudo chmod 777 '${gse_admin_stagedir}' && rm -rf /home/opc/.ssh/known_hosts '${gse_admin_stagedir}'/'${identity_domain}
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'sudo mkdir -p '${gse_admin_stagedir}' && sudo chown opc:opc '${gse_admin_stagedir}' && sudo chmod 777 '${gse_admin_stagedir}' && rm -rf /home/opc/.ssh/known_hosts '${gse_admin_stagedir}'/'${identity_domain}

echo "Uploading assets to gse admin..."
echo scp -o StrictHostKeyChecking=no -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/change_fqdn.sh scripts/${identity_domain}/cln.props scripts/${identity_domain}/ProvisionEBS.xml scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:${gse_admin_stagedir}
     scp -o StrictHostKeyChecking=no -i ssh_keys/gse_admin ssh_keys/${identity_domain} scripts/root_ebs_workshop.sh scripts/change_fqdn.sh scripts/${identity_domain}/cln.props scripts/${identity_domain}/ProvisionEBS.xml scripts/oracle_ebs_workshop.sh scripts/p22336899_R12_GENERIC.zip opc@${gse_admin}:${gse_admin_stagedir}

echo "Preparing ssh key to connect to target instance (${source_ip})..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'chmod 0400 '${gse_admin_stagedir}'/'${identity_domain}
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'chmod 0400 '${gse_admin_stagedir}'/'${identity_domain}

echo "Creating GSE stage directory on source instance..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${source_ip}' "sudo mkdir -p '${gse_admin_stagedir}' && sudo chmod 777 '${gse_admin_stagedir}'"'
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${source_ip}' "sudo mkdir -p '${gse_admin_stagedir}' && sudo chmod 777 '${gse_admin_stagedir}'"'

echo "Uploading assets to target instance..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' '${gse_admin_stagedir}'/cln.props '${gse_admin_stagedir}'/oracle_ebs_workshop.sh '${gse_admin_stagedir}'/change_fqdn.sh '${gse_admin_stagedir}'/root_ebs_workshop.sh '${gse_admin_stagedir}'/p22336899_R12_GENERIC.zip opc@'${source_ip}':'${gse_admin_stagedir}
     ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'scp -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' '${gse_admin_stagedir}'/cln.props '${gse_admin_stagedir}'/oracle_ebs_workshop.sh '${gse_admin_stagedir}'/change_fqdn.sh '${gse_admin_stagedir}'/root_ebs_workshop.sh '${gse_admin_stagedir}'/p22336899_R12_GENERIC.zip opc@'${source_ip}':'${gse_admin_stagedir}

echo "Preparing source instance..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${source_ip}' "cd '${gse_admin_stagedir}' && sudo dos2unix '${gse_admin_stagedir}'/change_fqdn.sh && sudo chmod 777 '${gse_admin_stagedir}'/oracle_ebs_workshop.sh && sudo sh '${gse_admin_stagedir}'/change_fqdn.sh '${targetIpHOST}' && sudo unzip -o p22336899_R12_GENERIC.zip && sudo chown oracle:dba -R '${gse_admin_stagedir}' && sudo chmod 777 -R '${gse_admin_stagedir}' && cp RemoteClone_v1.7/cln.props RemoteClone_v1.7/cln.props.ORIG && cp cln.props RemoteClone_v1.7/cln.props"'
	 ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${source_ip}' "cd '${gse_admin_stagedir}' && sudo dos2unix '${gse_admin_stagedir}'/change_fqdn.sh && sudo chmod 777 '${gse_admin_stagedir}'/oracle_ebs_workshop.sh && sudo sh '${gse_admin_stagedir}'/change_fqdn.sh '${targetIpHOST}' && sudo unzip -o p22336899_R12_GENERIC.zip && sudo chown oracle:dba -R '${gse_admin_stagedir}' && sudo chmod 777 -R '${gse_admin_stagedir}' && cp RemoteClone_v1.7/cln.props RemoteClone_v1.7/cln.props.ORIG && cp cln.props RemoteClone_v1.7/cln.props"'

echo "Running workshop commands..."
echo ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${source_ip}' "sudo yum install -y expect && sudo su - oracle -c '"'"''${gse_admin_stagedir}'/oracle_ebs_workshop.sh '${gse_admin_stagedir}' '${identity_domain}' '${source_ip}''"'"'"'
	 ssh -o StrictHostKeyChecking=no -i ssh_keys/gse_admin opc@${gse_admin} 'ssh -o StrictHostKeyChecking=no -i '${gse_admin_stagedir}'/'${identity_domain}' opc@'${source_ip}' "sudo yum install -y expect && sudo su - oracle -c '"'"''${gse_admin_stagedir}'/oracle_ebs_workshop.sh '${gse_admin_stagedir}' '${identity_domain}' '${source_ip}''"'"'"'