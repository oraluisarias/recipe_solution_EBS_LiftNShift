import opc, time

admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
identity_domain = "gse00010217"

source_instance_name = "EBS_Source"
source_volume_name = "EBS_Source_Storage_420GB"
source_volume = "/Compute-"+identity_domain+"/"+cloud_username+"/"+source_volume_name
source_orchestration_instance_name = "source_orchestration.json"
source_orchestration_volume_name = "source_orchestration_volume.json"
real_source_instance_name = ""

target_instance_name = "EBS_Target"
target_volume_name = "EBS Target Volume"
target_volume = "/Compute-"+identity_domain+"/"+cloud_username+"/"+source_volume_name
target_orchestration_instance_name = "target_orchestration.json"
target_orchestration_volume_name = "target_orchestration_volume.json"
real_target_instance_name = ""


opcc = opc.Compute(identity_domain, "z33", "em3")

opcc.addSSHkey( cloud_username, "gse_key.pub", "gse_key" )
opcc.createOrchestration(cloud_username, source_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_instance_name)  ]  )
opcc.createVolumeOrchestration(cloud_username, source_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_volume_name)  ]  )

opcc.createOrchestration(cloud_username, target_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", target_instance_name)  ]  )
opcc.createVolumeOrchestration(cloud_username, target_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", target_volume_name)  ]  )

# sleep here
instances = opcc.getInstances( cloud_username )
while real_source_instance_name == "" :
	print "Waiting for source instance to be created, sleeping 1 minute per iteration..."
	for instance in instances["result"]:
		if instance['name'].find(source_instance_name) > 0:				
			print instance["state"]
			if instance["state"] == "running":
				real_source_instance_name = instance['name']
		if instance['name'].find(target_instance_name) > 0:				
			print instance["state"]
			if instance["state"] == "running":
				real_target_instance_name = instance['name']
	# if real_source_instance_name == "" :
	if real_source_instance_name == "" and real_target_instance_name == "" :
		time.sleep(60)

opcc.attachVolume( 1, source_volume, real_source_instance_name )
opcc.attachVolume( 1, source_volume, real_target_instance_name )
