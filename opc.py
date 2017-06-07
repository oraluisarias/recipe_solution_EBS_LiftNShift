#!/usr/bin/env python
#################################################################################
#************************************************************************************************#
# Script: opc.py                                                                                 #
# Usage : GSE - Python wrapper to execute REST calls on Oracle Compute Cloud Services            #
# Date                                  Who                           What                       #
#------------------------------------------------------------------------------------------------#
# Aug-2016                           LUISARIA.MX                  Initial Version                #
#------------------------------------------------------------------------------------------------#
import requests, json, yaml, os, time, sys, subprocess

class DemoCentral:
	def saveDCEnvironmentPassword(self, environment_id, new_pass):		
		endpoint = "https://adsweb.oracleads.com/apex/adsweb/rest/environments/" + str(environment_id) + "/password"
		headers = {
			'Authorization': 'Bearer YTg3ZWJmNDctNzFhYS00ZDM4LWE5YWQtN2FlNTNlZjNlNTNm'
		}
		pass_data = {
			"password" : new_pass
		}
		return requests.put(endpoint, data=json.dumps(pass_data), headers=headers )
		
	def getDCEnvironment(self, environment):
		# print ("Getting environment username/password from Demo Central...")
		endpoint = "https://adsweb.oracleads.com/apex/adsweb/rest/environments"
		headers = {
			'Authorization': 'Bearer YTg3ZWJmNDctNzFhYS00ZDM4LWE5YWQtN2FlNTNlZjNlNTNm',
			'X-Oracle-Environment-Name': environment
		}
		return json.loads( requests.get(endpoint, headers=headers).text )	

class Compute:	
	def __init__(self, identity_domain, api="z26", zone="us2", username="cloud.admin", password=False, findDomainData=True):
		self.api = api
		self.identity_domain = identity_domain
		self.zone = self.DATACENTER_SHORT = self.findDataCenter()
		# print ( "Datacenter...", self.findDataCenter() )
		if self.DATACENTER_SHORT == "us2" :
			self.DATACENTER_LONG="us"
		elif self.DATACENTER_SHORT == "em2" :
			self.DATACENTER_LONG="emea"
		self.user = username
		self.password = password
		if self.password == False:
			try: 
				self.password =  self.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]				
			except: 
				try: 
					self.password =  self.getCredentialsDemoCentral()["password"]				
					print("no data in Demo Central, environment retired?"); 	
				except: 
					self.password =  ""		
		auth = self.authenticate( self.api, self.zone, self.user, self.password)		
		if findDomainData:
			self.findDomainData()

	def findDomainData(self):
		RTpayload = { "identity_domain":self.identity_domain, "password":self.password }
		# print("Querying domain data using RT using data...", RTpayload)
		r = requests.post("http://gse-admin.oraclecloud.com:7002/getOPCZone", data=RTpayload )
		self.domain_data = yaml.safe_load( r.text )["identity_domain"]

	def findDataCenter(self):
		datacenters = ["us2", "em2", "em3", "us6"]
		DC_header_token = {
			'X-Auth-Token': 'AUTH_tk3cbd98e962069a0e22abc9e119962831'
		}
		for dc in datacenters:
			endpoint = "https://" + dc + ".storage.oraclecloud.com/v1/Storage-"+self.identity_domain+"/test"
			response =  requests.put(endpoint, headers = DC_header_token).text
			if response != "<html><body>Sorry, but the content requested does not seem to be available. Try again later. If you still see this message, then contact Oracle Support.</body></html>":
				return dc
		return False

	def getZone(self):
		return self.api

	def getDataCenter(self):
		return self.zone

	def setZone(self, zone):
		self.api = zone

	def setDataCenter(self, dc):
		self.zone = dc

	def getDataCenterLong(self):
		return self.DATACENTER_LONG
		
	def getDataCenterShort(self):
		return self.DATACENTER_SHORT

	def runScriptRemote(self, pkey, ip, script_directory, file):		
		return self.scp(pkey, ip, script_directory + "/" + file, "~/" + file) and self.sshLinux(pkey, ip, "sudo chmod 777 ~/" + file) and self.sshLinux(pkey, ip, "sudo ~/" + file)					

	def sshLinux(self, pkey, ip, command):
		ssh_command = "ssh -tt -i " + pkey + " opc@" + ip + " '" + command + "'"
		# print (ssh_command)
		try:
			print ( subprocess.check_output( ssh_command , shell=True ) )
		except: 
			print ( "command returned error, disregarded..." )
			return False
		return True

	def scp(self, pkey, ip, origin_file, destiny_file):
		scp_command = "scp -i " + pkey + " " + origin_file + " opc@" + ip + ":" + destiny_file
		# print (scp_command)
		try:
			print (subprocess.check_output(scp_command, shell=True ))
		except: 
			print ("command returned error, disregarded...")
			return False
		return True

	def uploadOrchestration(self, admin_username, cloud_username, private_key, orchestrations_folder, identity_domain, orch_instance_name, orch_storage_name, cloud_shape):				
		limit_wait=40
		print ("Adding an existing ssh key")
		self.addSSHkey(cloud_username, private_key + ".pub", private_key)

		print ("Creating an allow all, inbound and outbound security list")
		self.addSeclist(cloud_username, {
		 	  "policy": "PERMIT",
		 	  "outbound_cidr_policy": "PERMIT",
		 	  "name": "/Compute-" + identity_domain + "/" + cloud_username + "/allow_all"
		 	}
		)
		print ("Uploading storage orchestration")
		self.createOrchestration(cloud_username, orchestrations_folder + "/storage.json", [ ('#cloud_shape', cloud_shape),
			('#ssh_key', private_key), ('#identity_domain', identity_domain), ('#username', cloud_username), 
			('#orchestration_name_instance', orch_instance_name), ('#orchestration_name_storage', orch_storage_name) ] )

		print ("Waiting for orchestration to be on stopped state")
		limit_count=0
		status = self.getOrchestrationState(cloud_username, orch_storage_name)
		while "stopped" != status and "ready" != status:
			if limit_count == limit_wait:
				print ("Something failed...")
				sys.exit(1)
			print ("Status was %s, sleeping for 30s before retry..." % (status))
			time.sleep(30)
			status = self.getOrchestrationState(cloud_username, orch_storage_name)
			limit_count = limit_count + 1

		print ("Starting orchestration")
		self.orchestrationAction(cloud_username, orch_storage_name, "START")	

		print ("Waiting for orchestration to be on ready state")
		limit_count=0
		status = self.getOrchestrationState(cloud_username, orch_storage_name)
		while "ready" != status:
			if limit_count == limit_wait:
				print ("Something failed...")
				sys.exit(1)
			print ("Status was %s, sleeping for 30s before retry..." % (status))
			time.sleep(30)
			status = self.getOrchestrationState(cloud_username, orch_storage_name)
			limit_count = limit_count + 1

		print ("Uploading instance orchestration")
		self.createOrchestration(cloud_username, 
			orchestrations_folder + "/instance.json", 
			[ ('#ssh_key', private_key), ('#identity_domain', identity_domain), 
			('#username', cloud_username), ('#cloud_shape', cloud_shape),
			('#orchestration_name_instance', orch_instance_name), 
			('#orchestration_name_storage', orch_storage_name) ] )

		print ("Waiting for orchestration to be on stopped state")
		limit_count=0
		status = self.getOrchestrationState(cloud_username, orch_instance_name)
		while "stopped" != status and "error" != status and "ready" != status:
			if limit_count == limit_wait:
				print ("Something failed...")
				sys.exit(1)
			print ("Status was %s, sleeping for 30s before retry..." % (status))
			time.sleep(30)
			status = self.getOrchestrationState(cloud_username, orch_instance_name)
			limit_count = limit_count + 1

		print ("Starting orchestration")
		self.orchestrationAction(cloud_username, orch_instance_name, "START")	

		print ("Getting IP of new instance")
		ip = self.getIpByOrchestration(cloud_username, admin_username, orch_instance_name)["ip"]
		return ip

	def authenticate(self, api=False, zone=False, username=False, password=False):
		if api == False:
			api = self.api
		if zone == False:
			zone = self.zone
		if username == False:
			username = self.username
		if password == False:
			password = self.password
		if (username == password == False):
			credentials = self.getCredentialsDemoCentral()
		else: 
			# return {"user" : "/Compute-" + self.identity_domain + "/" + opc_email["items"][0]["value"], "password" : opc_password["items"][0]["value"]}
			credentials = {"user" : "/Compute-" + self.identity_domain + "/" + username, "password" : password}
			# print ("Testing login with custom credentials...")
			# print (credentials)
		if api != False and zone != False:
			headers = {'Content-Type': 'application/oracle-compute-v3+json'}		
			url = "https://api-"+api+".compute."+zone+".oraclecloud.com/authenticate/"
			# print("url", url)
			r = requests.post(url, data=json.dumps(credentials), headers=headers)	
			cookies = "nimbula=" + r.cookies["nimbula"] + "; Path=/; Max-Age=1800"	
			# print (r.text)
			self.cookie = cookies
			return {"cookie" : cookies, "user" : credentials["user"], "password" : credentials["password"]}	
		else:
			return {"cookie" : "", "user" : self.username, "password" : self.password}	

	def setAPI(self, api, zone):
		self.api = api
		self.zone = zone

	def addSSHkey(self, user, key, name):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/sshkey/"
		data = {"enabled" : "true", "name" : "/Compute-" + self.identity_domain + "/" + user + "/" + name}
		# "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAseR3ONbBVVRGcEKyXA7kVFSFdQJdDvhRjxKJrhAhpq5AWpDL6vhk1u3YXJ5mJ5tOdml0oZrEl0jVebECFqx0IlhfHxDmtrDapeYbYal7XpLL2xAH3OpAGmzSMF5mTZNOt1UEbgWEIWej1aL9prhJcFTgV5ZHISGRUwFalhFuAdxddH/yiW5x/ACqsWXdoksC9hPvYNIAd7Z+8Jpzz7z18MUB8rTV5khUuoHiW7VZ0yKdV+Md4XbzoFROmKRek1z8wtZJRkELZZtcHEaisTR4fJxiMefFph2Q0iaBmDSK6lTij+vWQLyVP0TaXoLDJg5KBZOFZnDzEpvAV1HboU68+Q== luis.a.arias@oracle.com"
		if type(key) == str and os.path.isfile(key):
			with open(key, 'r') as f: 
				data["key"]=f.read()
		else: data["key"] = key
		r = requests.post(endpoint, data=json.dumps(data), headers=headers)	
		print ("key: " + data["key"])
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def addSeclist(self,  user, seclist):		
		headers = {"Cookie" : self.cookie, "Content-Type" : "application/oracle-compute-v3+json", "Accept" : "application/oracle-compute-v3+json"}			
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/seclist/"
		if type(seclist) == str and os.path.isfile(seclist): 
			with open(key, 'r') as f: 
				seclist=f.read()		
		r = requests.post(endpoint, data=json.dumps(seclist), headers=headers)
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	# def deleteOrchestration(self, user, orchestration_name):	
	# 	headers = {"Cookie" : self.cookie, "Content-Type" : "application/oracle-compute-v3+json", "Accept" : "application/oracle-compute-v3+json"}	
	# 	endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/orchestration/" + orchestration_name
	# 	r = requests.delete(endpoint, headers=headers)
	# 	print ("Deleting orchestration...", r.text)
	# 	return yaml.safe_load(r.text) 

	def createOrchestration(self,  user, orchestration, replace=[]):	
		headers = {"Cookie" : self.cookie, "Content-Type" : "application/oracle-compute-v3+json", "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/orchestration/"
		if os.path.isfile(orchestration):
			with open(orchestration, 'r') as f: 
				jsonfile=f.read()
				for k, v in replace: jsonfile = jsonfile.replace(k, v)
				orchestration=yaml.safe_load(jsonfile)		
		else: print ("Uploading plain orchestration")

		r = requests.post(endpoint, data=json.dumps(orchestration), headers=headers)
		print ("orchestration: ")
		print (orchestration)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def attachVolume(self, index, storage_volume_name, source_instance):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/attachment/"
		data={"index": index,"storage_volume_name": storage_volume_name,"instance_name": source_instance}
		r = requests.post(endpoint, data=json.dumps(data), headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def createVolumeOrchestration(self, user, orchestration, replace=[]):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/volume/"
		if os.path.isfile(orchestration):
			with open(orchestration, 'r') as f: 
				jsonfile=f.read()
				for k, v in replace: jsonfile = jsonfile.replace(k, v)
				orchestration=yaml.safe_load(jsonfile)	
		print ("uploading orchestration: " + json.dumps(orchestration))	
		r = requests.post(endpoint, data=json.dumps(orchestration), headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def orchestrationAction(self,  user, orchestration_name, action):		
		headers = {"Cookie" : self.cookie, "Content-Type" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/orchestration/Compute-" + self.identity_domain + "/" + user + "/" + orchestration_name + "?action=" + action
		r = requests.put(endpoint, headers=headers)
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def deleteOrchestration(self,  user, orchestration_name):	
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/orchestration/Compute-" + self.identity_domain + "/" + user + "/" + orchestration_name + "/"
		r = requests.delete(endpoint, headers=headers)
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def getOrchestrations(self,  user):		
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/orchestration/Compute-" + self.identity_domain + "/" + user + "/"	
		r = requests.get(endpoint, headers=headers)
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def getOrchestrationState(self, user, orchestration_name):
		orchestrations = self.getOrchestrations(user)	
		for orchestration in orchestrations["result"]:		
			print ("orchestration name: %s" % (orchestration["name"]))
			if "/Compute-" + self.identity_domain + "/" + user + "/" + orchestration_name == orchestration["name"]:				
				return orchestration["status"]
		return False

	def rebootInstance(self,  instance):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/rebootinstancerequest/"
		data = { "hard": "true", "instance": instance }
		r = requests.post(endpoint, data=json.dumps(data), headers=headers)
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def deleteInstance(self,  instance):
		headers = {"Cookie" : self.cookie}
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/instance" + instance
		r = requests.delete(endpoint, headers=headers)
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def getShapes(self):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/shape/"	
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)			
		return yaml.safe_load(r.text)

	def getIpByOrchestration(self, user, admin_user, nimbula_orchestration):		
		instance = self.getInstanceByOrchestration(user, nimbula_orchestration)
		print (instance)
		if instance != False: return self.getReservedIP(admin_user, instance["vcable_id"])
		return False

	def getInstanceByOrchestration(self, user, nimbula_orchestration):
		instances = self.getInstances(user)
		instance = False
		for inst in instances["result"]:
			print ("Searching: " + nimbula_orchestration)
			print (inst["attributes"]["nimbula_orchestration"])
			if inst["attributes"]["nimbula_orchestration"] == "/Compute-" + self.identity_domain + "/" + user + "/" + nimbula_orchestration:
				instance = inst		
		return instance

	def getAllReservedIP(self,  user):  
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/ip/reservation/Compute-" + self.identity_domain + "/" + user + "/"	
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)			
		return yaml.safe_load(r.text)

	def getAllAssociatedIP(self,  user):  
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/ip/association/Compute-" + self.identity_domain + "/" + user + "/"			
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)			
		return yaml.safe_load(r.text)

	def getReservedIP(self,  user, vcable_id):  
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/ip/association/Compute-" + self.identity_domain + "/" + user + "/"					
		r = requests.get(endpoint, headers=headers)			
		result=yaml.safe_load(r.text)
		for ips in result["result"]:
			if ips["vcable"] == vcable_id:
				return ips

	def getAssociatedIP(self,  user, instance_name):  
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/ip/association" + instance_name + "/"		
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)			
		return yaml.safe_load(r.text)

	def getInstances(self,  user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json"}	
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/instance/Compute-" + self.identity_domain + "/" + user + "/"	
		r = requests.get(endpoint, headers=headers)	
		# print ("endpoint: " + endpoint)			
		return yaml.safe_load(r.text)

	def getAttachmentDetails(self, user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/attachment/Compute-" + self.identity_domain + "/" + user + "/"
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)	
		return yaml.safe_load(r.text)

	def getVolumes(self, user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/volume/Compute-" + self.identity_domain + "/" + user + "/"
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)	
		return yaml.safe_load(r.text)

	def deleteVolume(self, user, volume):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/volume/Compute-" + self.identity_domain + "/" + user + "/" + volume
		r = requests.delete(endpoint, headers=headers)	
		return yaml.safe_load(r.text)

	def createSimpleVolume(self,  size, name):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/volume/"
		volume_data = {"size" : size, "name" : name, "properties" : ["/oracle/public/storage/default"]}
		r = requests.post(endpoint, data=json.dumps(volume_data), headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def createBootableVolume(self,  size, name):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+json", "Content-Type" : "application/oracle-compute-v3+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/storage/volume/"
		volume_data = {"size" : size, "name" : name, "properties" : ["/oracle/public/storage/default"]}
		r = requests.post(endpoint, data=json.dumps(volume_data), headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def getImageLists(self,  user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/imagelist/Compute-" + self.identity_domain + "/" + user + "/"
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def getSSHKey(self, user):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/sshkey/Compute-" + self.identity_domain + "/" + user + "/"
		r = requests.get(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)

	def deleteSSHKey(self,  user, key):
		headers = {"Cookie" : self.cookie, "Accept" : "application/oracle-compute-v3+directory+json"}		
		endpoint = "https://api-"+self.api+".compute."+self.zone+".oraclecloud.com/sshkey/Compute-" + self.identity_domain + "/" + user + "/" + key
		r = requests.delete(endpoint, headers=headers)	
		print ("endpoint: " + endpoint)	
		print (r.text)
		return yaml.safe_load(r.text)	
 	
 	def getDCEnvironment(self, environment):
		# print ("Getting environment username/password from Demo Central...")
		endpoint = "https://adsweb.oracleads.com/apex/adsweb/rest/environments"
		headers = {
			'Authorization': 'Bearer YTg3ZWJmNDctNzFhYS00ZDM4LWE5YWQtN2FlNTNlZjNlNTNm',
			'X-Oracle-Environment-Name': environment
		}
		return json.loads( requests.get(endpoint, headers=headers).text )	

	def getCredentialsDemoCentral(self):
		# curlUser = curl -X GET -H X-Oracle-Authorization:Z3NlLWRldm9wc193d0BvcmFjbGUuY29tOjVjWmJzWkxuMQ== 
		#https://adsweb.oracleads.com/apex/adsweb/parameters/democloud_admin_opc_email
		# curlPass = curl -X GET -H X-Oracle-Authorization:Z3NlLWRldm9wc193d0BvcmFjbGUuY29tOjVjWmJzWkxuMQ== 
		#https://adsweb.oracleads.com/apex/adsweb/parameters/democloud_admin_opc_password
		# print ("Getting cloud username/password from Demo Central...")
		headers = {'X-Oracle-Authorization': 'Z3NlLWRldm9wc193d0BvcmFjbGUuY29tOjVjWmJzWkxuMQ=='}
		opc_email = yaml.safe_load(requests.get("https://adsweb.oracleads.com/apex/adsweb/parameters/democloud_admin_opc_email", headers=headers).text)
		opc_password = yaml.safe_load(requests.get("https://adsweb.oracleads.com/apex/adsweb/parameters/democloud_admin_opc_password", headers=headers).text)	
		sso_email = yaml.safe_load(requests.get("https://adsweb.oracleads.com/apex/adsweb/parameters/democloud_admin_sso_email", headers=headers).text)
		sso_password = yaml.safe_load(requests.get("https://adsweb.oracleads.com/apex/adsweb/parameters/democloud_admin_sso_password", headers=headers).text)	
		# print ("%s, %s, %s, %s" % (opc_email["items"][0]["value"], opc_password["items"][0]["value"], 
		# 			sso_email["items"][0]["value"], sso_password["items"][0]["value"]))
		return {"user" : "/Compute-" + self.identity_domain + "/" + opc_email["items"][0]["value"], "password" : opc_password["items"][0]["value"]}

	