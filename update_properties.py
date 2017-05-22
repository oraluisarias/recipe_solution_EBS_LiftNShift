import opc, time, sys

identityDomain = sys.argv[1]
demo_central = opc.DemoCentral()
cloudPassword = demo_central.getDCEnvironment("metcs-" + identity_domain)["items"][0]["password"]
from datetime import date
today = date.today()
dateTimeTag = "skwn"+str(today.year)+str(today.month)+str(today.day)

sourceFile="scripts/cln.props.ORIG"
targetFile="scripts/"+identityDomain+"/cln.props"
with open(sourceFile, 'r') as f: 
	source_text=f.read()
	for k, v in replace: source_text = source_text.replace(k, v)
	text_file = open(targetFile, "w")
	text_file.write(source_text)
	text_file.close()