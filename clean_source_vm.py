import opc, time, sys

identity_domain = "gse00011327"
# identity_domain = sys.argv[1]
zone = "z11"
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
real_source_volume_name = "new"
real_source_instance_name = "new"
opcc = opc.Compute( identity_domain, zone, False )

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

#delete and wait
image_exists = True
time_ellapsed = 0
while real_source_instance_name != "" and real_source_volume_name != "":
	real_source_volume_name = "new"
	real_source_instance_name = "new"
	print "Deleting EBS Source volume"
	opcc.deleteVolume( cloud_username, source_volume_name )
	print "Deleting EBS Source orchestration"
	opcc.orchestrationAction(cloud_username, source_instance_name, "STOP")	
	opcc.deleteOrchestration( cloud_username, source_instance_name )
	volumes = opcc.getVolumes( cloud_username )
	instances = opcc.getInstances( cloud_username )
	print "Waiting for source instance and volume to be deleted..."
	try:
		for instance in instances["result"]: 
			if instance['name'].find(source_instance_name) > 0:							
				print ("Image exists...", instance['name'])				
				real_source_instance_name = instance['name']
		if real_source_instance_name == "new" : real_source_instance_name = ""
	except Exception as e:
	  print ("Got an error!", e.value)	
	try:
		for volume in volumes["result"]: 			
			if volume['name'].find(source_volume_name) > 0:							
				print ("Volume exists...", volume['name'])				
				real_source_volume_name = volume['name']
		if real_source_volume_name == "new" : real_source_volume_name = ""		
	except Exception as e:
	  print ("Got an error!", e.value)	  

print "Source instance and volume were deleted..."