import opc, time, sys

# identity_domain = "gse00010217"
identity_domain = sys.argv[1]
# zone = "z33"
zone = sys.argv[2]
# datacenter = "em3"
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
source_orchestration_name = "/Compute-"+identity_domain+"/"+cloud_username+"/EBS_Source"

opcc = opc.Compute( identity_domain, zone, datacenter )
real_source_volume_name = ""
real_source_instance_name = ""


#find image in datacenters
print ( "Getting datacenter...", opcc.domain_data )
for domain in opcc.domain_data:
	domain_data = opcc.domain_data[domain]	
	opcc.setDataCenter(domain_data["datacenter"].lower().replace('0', ''))
	opcc.setZone(domain_data["zone"].lower())
	opcc.authenticate(False, False, "cloud.admin")
	images = opcc.getImageLists("cloud.admin") 
	for image in images["result"]:
		if "OPC_OL6_8_EBS_1226_VISION_SINGLE_TIER_11302016" in image or "OPC_OL6_8_EBS_ORCH_VM_03282017" in image or "OPC_OL6_8_X86_64_EBS_OS_VM_12202016" in image: 
			return

# opcc.deleteSSHKey( cloud_username, identity_domain )
opcc.addSSHkey( cloud_username, "ssh_keys/gse_admin.pub", identity_domain )
opcc.createOrchestration(cloud_username, source_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_instance_name)  ]  )
opcc.createVolumeOrchestration(cloud_username, source_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#name", source_volume_name)  ]  )

# sleep here
time_ellapsed = 0
while real_source_instance_name == "" :
	if time_ellapsed == 29:
		opcc = opc.Compute( identity_domain, zone, datacenter )
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
  		print ( "Lost access to OPC, halting recipe..." , e)	  
		sys.exit(0)

print ("Public IP: ", source_public_ip)
f = open("ips/" + identity_domain, 'w')
f.write( source_public_ip["ip"] )

opcc.attachVolume( 1, source_volume, real_source_instance_name )