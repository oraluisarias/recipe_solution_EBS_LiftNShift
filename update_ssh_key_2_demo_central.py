import requests, sys, json

demo_central_keys_endpoint = "https://adsweb.oracleads.com/apex/rest/api/opc-ssh-keys"
admin_username = "gse-admin_ww@oracle.com"
cloud_username = "cloud.admin"
identity_domain = sys.argv[1]
zone = sys.argv[2]
datacenter = sys.argv[3]

headers = {'X-Oracle-Authorization': 'Z3NlLWRldm9wc193d0BvcmFjbGUuY29tOjVjWmJzWkxuMQ=='}
private_key = open('ssh_keys/'+identity_domain, 'r').read()
public_key = open('ssh_keys/'+identity_domain+'.pub', 'r').read()
demo_central_payload = {
	"key_name":"default",
	"public_key":public_key,
	"private_key":private_key,
	"identity_domain_name":identity_domain
}

print ("Submitting request to save key in demo central", 
	requests.post( demo_central_keys_endpoint, data=json.dumps( demo_central_payload ), headers=headers ) )