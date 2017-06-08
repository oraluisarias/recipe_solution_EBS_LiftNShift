import opc, time

admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
identity_domain = "gse00002320"

opcc = opc.Compute(identity_domain, "z17", "em2")

volumes = opcc.getVolumes(cloud_username)
# print (volumes)
for volume in volumes["result"]:
	print (volume["status"])
# print opcc.attachVolume( 1, "/Compute-gse00002317/cloud.admin/OL_68_rsync_storage_storage", "/Compute-gse00002317/cloud.admin/OL_68_rsync_storage/7b44394a-1f50-4223-b9f7-059f231bc6e0" )
# print opcc.attachVolume( 1, "/Compute-gse00002317/cloud.admin/gse-admin_storage", "/Compute-gse00002317/cloud.admin/OL_68_rsync_storage/7b44394a-1f50-4223-b9f7-059f231bc6e0" )

# print volumes