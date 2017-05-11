import opc, time

admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
identity_domain = "gse00010217"

opcc = opc.Compute(identity_domain, "z33", "em3")

volumes = opcc.getVolumes(cloud_username)
for volume in volumes:
	print volume