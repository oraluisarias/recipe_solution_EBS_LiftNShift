import opc, time, sys
from datetime import date

identityDomain = sys.argv[1]
demo_central = opc.DemoCentral()
cloudPassword = demo_central.getDCEnvironment("metcs-" + identityDomain)["items"][0]["password"]
today = date.today()
dateTimeTag = "skwn"+str(today.year)+str(today.month)+str(today.day)

replace=[ ("#dateTimeTag", dateTimeTag), ('#cloudPassword', cloudPassword), ('#identityDomain', identityDomain) ]

sourceFile="scripts/cln.props.ORIG"
targetFile="scripts/"+identityDomain+"/cln.props"
with open(sourceFile, 'r') as f: 
	source_text=f.read()
	for k, v in replace: source_text = source_text.replace(k, v)
	text_file = open(targetFile, "w")
	text_file.write(source_text)
	text_file.close()