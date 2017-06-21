import json, requests, os, datetime, sys, time

# identity_domain = "gse00000012"
identity_domain = sys.argv[1]

print ( "Cleaning domain using psm Clean" )
data = {
	"identity_domain": identity_domain,
	"solution_profile" : "psm_CleanDomain",
	"override_concurrency" : True
}
CloudBots_endpoint = "http://hq-techadmin.us.oracle.com:3000/CloudBots"	
CloudBots_response = requests.post( CloudBots_endpoint + "/runRecipe", data=data )
CloudBots_job = json.loads( CloudBots_response.text )
jobId = CloudBots_job["result"]["jobid"]

time_ellapsed = 0
CloudBots_status_response = json.loads( requests.get( CloudBots_endpoint + "/getJobs/" + str(jobId) ).text )
print ( "status", CloudBots_status_response[str(jobId)]["status"] )
while CloudBots_status_response[str(jobId)]["status"] == "RUNNING":
	CloudBots_status_response = requests.get( CloudBots_endpoint + "/getJobs/" + str(jobId) )
	CloudBots_status_response = json.loads( requests.get( CloudBots_endpoint + "/getJobs/" + str(jobId) ).text )
	print("Sleeping 1 minute...", time_ellapsed, "minutes passed")
	time_ellapsed=time_ellapsed+1
	time.sleep(60)
# CloudBots_status = json.loads( CloudBots_status_response.text )
# print (CloudBots_status)