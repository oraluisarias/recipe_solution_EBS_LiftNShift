import opc, time, sys

demo_central = opc.DemoCentral()
admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
cloud_password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]
identity_domain = sys.argv[1]
zone = sys.argv[2]
datacenter = sys.argv[3]


source_instance_name = "EBS_Source"
source_volume_name = "EBS_Source_Storage_420GB"
source_volume = "/Compute-"+identity_domain+"/"+cloud_username+"/"+source_volume_name
source_orchestration_instance_name = "orchestrations/source_orchestration.json"
source_orchestration_volume_name = "orchestrations/source_orchestration_volume.json"
real_source_instance_name = ""

opcc = opc.Compute(identity_domain, zone, datacenter, cloud_username, cloud_password)

opcc.authenticate(zone, datacenter, cloud_username, cloud_password)
opcc.addSSHkey( cloud_username, "ssh_keys/"+identity_domain+".pub", "gse_key" )
opcc.createOrchestration(cloud_username, source_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_instance_name)  ]  )
opcc.createVolumeOrchestration(cloud_username, source_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_volume_name)  ]  )

# sleep here
instances = opcc.getInstances( cloud_username )
while real_source_instance_name == "" :
	print "Waiting for source instance to be created, sleeping 1 minute per iteration..."
	for instance in instances["result"]:
		if instance['name'].find(source_instance_name) > 0:				
			print instance
			print instance["state"]
			if instance["state"] == "running":
				source_public_ip = opcc.getReservedIP(admin_username, instance["vcable_id"])
				real_source_instance_name = instance['name']
	if real_source_instance_name == "" :
		time.sleep(60)

print ("Public IP: ", source_public_ip)
f = open("ips/" + identity_domain, 'w')
f.write( source_public_ip["ip"] )

opcc.attachVolume( 1, source_volume, real_source_instance_name )