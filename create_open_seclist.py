import opc, sys

admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
identity_domain = sys.argv[1]
zone = sys.argv[2]
datacenter = sys.argv[3]

demo_central = opc.DemoCentral()
cloud_password = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]
opcc = opc.Compute(identity_domain, zone, datacenter, cloud_username, cloud_password)
opcc.addSeclist(cloud_username, {
 	  "policy": "PERMIT",
 	  "outbound_cidr_policy": "PERMIT",
 	  "name": "/Compute-" + identity_domain + "/" + cloud_username + "/allow_all"
 	}
)