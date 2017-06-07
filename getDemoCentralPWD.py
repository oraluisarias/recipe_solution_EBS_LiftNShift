import opc

identity_domain = sys.argv[1]
opcc = opc.Compute(identity_domain, "z11", "", "cloud.admin", False, False)

try: 
	password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]	
except: 
	print ""
else:
	print password