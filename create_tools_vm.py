import opc, time, sys

identity_domain = sys.argv[1]
# identity_domain = "gse00010217"
zone = sys.argv[2]
# zone = "z33"
datacenter = sys.argv[3]
# datacenter = "em3"
demo_central = opc.DemoCentral()
admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
cloud_password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]

tools_orchestration_instance_name="orchestrations/ebstools_instance.json"
tools_orchestration_volume_name="orchestrations/ebstools_storage.json"
tools_orchestration_master_name="orchestrations/ebstools_master.json"
tools_master_name="ebstools_master"
tools_instance_name="ebstools_instance"
tools_storage_name="ebstools_storage"

opcc = opc.Compute( identity_domain, zone, datacenter )
real_source_volume_name = ""
real_tools_instance_name = ""


opcc.addSSHkey( cloud_username, "ssh_keys/gse_admin.pub", identity_domain )
opcc.createOrchestration(cloud_username, tools_orchestration_volume_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#instanceName", tools_instance_name), ("#masterName", tools_master_name), ("#storageName", tools_storage_name)  ]  )
opcc.createOrchestration(cloud_username, tools_orchestration_instance_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#instanceName", tools_instance_name), ("#masterName", tools_master_name), ("#storageName", tools_storage_name)  ]  )
opcc.createOrchestration(cloud_username, tools_orchestration_master_name, 
	[ ("#cloud_username", cloud_username), ("#identityDomain", identity_domain), ("#instanceName", tools_instance_name), ("#masterName", tools_master_name), ("#storageName", tools_storage_name)  ]  )

opcc.orchestrationAction(cloud_username, tools_master_name, "START")	
# sleep here
error_counter = 0
time_ellapsed = 0
while real_tools_instance_name == "" :
	if error_counter >= 10: 
		print ("Reached maximum number of failures")
		sys.exit(1)
	instances = opcc.getInstances( cloud_username )
	print "Waiting for source instance to be created, sleeping 1 minute per iteration "+str(time_ellapsed)+" minutes passed..."
	try:
		for instance in instances["result"]: 
			if instance['name'].find(tools_instance_name) > 0:							
				print instance["state"]
				if instance["state"] == "running":
					source_public_ip = opcc.getReservedIP(cloud_username, instance["vcable_id"])
					real_tools_instance_name = instance['name']
					print ("Retrieving IP and real name of the newly created service...", source_public_ip, real_source_instance_name)
		if real_tools_instance_name == "" :
			time.sleep(60)
			time_ellapsed=time_ellapsed+1	
<<<<<<< HEAD
			if time_ellapsed % 29 == 0:
				print ("29 minutes passed, login in again to OPC")
=======
			if time_ellapsed % 20 == 0:
				print ("20 minutes passed, login in again to OPC")
>>>>>>> 14a1a96b439ee9bbb9a58f432d6462e8873bb87f
				opcc.renovateCookie()  
	except NameError:
		print ("Didnt get any answer from OPC this time!")
	except Exception as e:
		print ("Lost access to OPC, halting recipe...", e)	
		error_counter=error_counter+1
		sys.exit(1)  

print ("Public IP: ", source_public_ip)
f = open("ips/tools_" + identity_domain, 'w')
f.write( source_public_ip["ip"] )