import opc, time, sys

identity_domain = sys.argv[1]
zone = sys.argv[2]
datacenter = sys.argv[3]
demo_central = opc.DemoCentral()
admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
cloud_password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]


source_instance_name = "EBS_Source"
source_volume_name = "EBS_Source_Storage_420GB"
source_volume = "/Compute-"+identity_domain+"/"+cloud_username+"/"+source_volume_name
source_orchestration_instance_name = "orchestrations/source_orchestration.json"
source_orchestration_volume_name = "orchestrations/source_orchestration_volume.json"
real_source_instance_name = ""

opcc = opc.Compute( identity_domain, zone, datacenter )
opcc.deleteSSHKey( cloud_username, identity_domain )
opcc.addSSHkey( cloud_username, "ssh_keys/" + identity_domain + ".pub", identity_domain )
opcc.createOrchestration(cloud_username, source_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_instance_name)  ]  )
opcc.createVolumeOrchestration(cloud_username, source_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_volume_name)  ]  )

# sleep here
time_ellapsed = 0
while real_source_instance_name == "" :
	instances = opcc.getInstances( cloud_username )
	print "Waiting for source instance to be created, sleeping 1 minute per iteration "+str(time_ellapsed)+" minutes passed..."
	try:
		for instance in instances["result"]: 
			if instance['name'].find(source_instance_name) > 0:							
				print instance["state"]
				if instance["state"] == "running":
					source_public_ip = opcc.getReservedIP(admin_username, instance["vcable_id"])
					real_source_instance_name = instance['name']
		if real_source_instance_name == "" :
			time.sleep(60)
			time_ellapsed=time_ellapsed+1	  
	except NameError:
	  print ("Didnt get any answer from OPC this time!")
	except Exception as e:
	  print ("Got an error!", e.value)
	else:
	  print ("sure, it was defined.")

print ("Public IP: ", source_public_ip)
f = open("ips/" + identity_domain, 'w')
f.write( source_public_ip["ip"] )

opcc.attachVolume( 1, source_volume, real_source_instance_name )