import opc, sys, time, requests, json
demo_central = opc.DemoCentral()
f = open(sys.argv[1], 'r')
content = f.read()
domains = json.loads(content)
print ("Reading domains...", domains)
for domain in domains:	
	print ( domain )
	try: cloud_password = demo_central.getDCEnvironment("metcs-" + domain)["items"][0]["password"]
	except: continue	
	print ( requests.post("http://gse-admin.oraclecloud.com:7002/getOPCZone", data={ "identity_domain":domain, "password":cloud_password } ).text )