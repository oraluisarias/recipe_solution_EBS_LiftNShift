import opc, time, sys

# identity_domain = "gse00010217"
identity_domain = sys.argv[1]
# zone = "z33"
zone = sys.argv[2]
# datacenter = "em3"
datacenter = sys.argv[3]
hostname = sys.argv[4]
demo_central = opc.DemoCentral()
admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
cloud_password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]

source_instance_name = hostname
source_volume_name = hostname+"_Storage_420GB"
source_volume = "/Compute-"+identity_domain+"/"+cloud_username+"/"+source_volume_name
vision_orchestration_instance_name = "orchestrations/vision_orchestration.json"
vision_orchestration_volume_name = "orchestrations/vision_orchestration_volume.json"
vision_orchestration_name = "/Compute-"+identity_domain+"/"+cloud_username+"/EBS_Source"

opcc = opc.Compute( identity_domain, zone, datacenter )
real_source_volume_name = ""
real_source_instance_name = ""

# opcc.deleteSSHKey( cloud_username, identity_domain )
opcc.addSSHkey( cloud_username, "ssh_keys/gse_admin.pub", identity_domain )
opcc.createOrchestration(cloud_username, vision_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), 
	("#name", source_instance_name), ("#hostname", hostname)  ]  )
opcc.createVolumeOrchestration(cloud_username, vision_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), 
	("#name", source_volume_name), ("#hostname", hostname)  ]  )

# sleep here
time_ellapsed = 0
while real_source_instance_name != "" and real_source_volume_name != "" :
	if time_ellapsed == 29:
		opcc = opc.Compute( identity_domain, zone, datacenter )	
	instances = opcc.getInstances( cloud_username )
	volumes = opcc.getVolumes( cloud_username )
	print ("Waiting for instance and volume to be created, sleeping 1 minute per iteration ",str(time_ellapsed)," minutes passed...")
	try:
		for volume in volumes["result"]: 
			if volume['name'].find(source_volume_name) > 0:		
				print ("Volume state: ", volume["status"])
				if volume["status"] == "Online":
					real_source_volume_name = volume['name']					
		for instance in instances["result"]: 
			if instance['name'].find(source_instance_name) > 0:							
				print ("Instance state: ", instance["state"])
				if instance["state"] == "running":
					source_public_ip = opcc.getReservedIP(cloud_username, instance["vcable_id"])
					real_source_instance_name = instance['name']
					print ("Retrieving IP and real name of the newly created service...", source_public_ip, real_source_instance_name)
		if real_source_instance_name == "" :
			time.sleep(60)
			time_ellapsed=time_ellapsed+1	  
	except NameError:
		print ("Didn't get any answer from OPC this time!")
	except Exception as e:
  		print ( "Lost access to OPC, halting recipe..." , e)	  
		sys.exit(0)

print ("Public IP: ", source_public_ip)
f = open("ips/" + identity_domain, 'w')
f.write( source_public_ip["ip"] )

opcc.attachVolume( 1, source_volume, real_source_instance_name )