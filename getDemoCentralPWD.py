import sys, opc

identity_domain = sys.argv[1]
demo_central = opc.DemoCentral()
try: 
	password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]	
except: 
	print ""
else:
	print password