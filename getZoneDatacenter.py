import opc, time, sys
 
identity_domain = sys.argv[1]
# identity_domain = "gse00002320"
opcc = opc.Compute( identity_domain, "z11", False )
 
image_found = False
#find image in datacenters
print ( "Getting datacenter...", opcc.domain_data )
for domain in opcc.domain_data:
    if image_found: break
    domain_data = opcc.domain_data[domain]    
    opcc.setDataCenter(domain_data["datacenter"].lower().replace('0', ''))
    opcc.setZone(domain_data["zone"].lower())
    opcc.authenticate(False, False, "cloud.admin")
    images = opcc.getImageLists("cloud.admin") 
    for image in images["result"]:
        if "OPC_OL6_8_EBS_1226_VISION_SINGLE_TIER_11302016" in image or "OPC_OL6_8_EBS_ORCH_VM_03282017" in image or "OPC_OL6_8_X86_64_EBS_OS_VM_12202016" in image: 
            image_found = True
if image_found == False:
    print ("EBS images were not installed")
    sys.exit(1)
 
zone = opcc.getZone() 
datacenter = opcc.getDataCenter() 
print ("EBS images found: ", "zone", zone, "datacenter", datacenter)
f = open("cache/" + identity_domain + "/zone", 'w')
f.write( zone )
f1 = open("cache/" + identity_domain + "/datacenter", 'w')
f1.write( datacenter )
sys.exit(0)