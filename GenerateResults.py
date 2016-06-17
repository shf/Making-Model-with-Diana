import os
import glob
dir = os.path.dirname(__file__)+"/GeneratedModels-Modified"
files = ["Model-em100-r8-rB14-case3"]

def findLastStep(outputaddress):
	
	file = open(outputaddress, 'r')
	lines = file.readlines()
	k = [s for s in lines if 'STEP' in s]
	m = k[-1].split()
	return int(m[1])

for i in range(len(files)):
	modelfile = dir+"/"+files[i]+"/"+files[i]+"-modified_A.dat"
	importModel(modelfile, "" )
	addAnalysis( "Analysis1" )
	resultfile =dir+"/"+files[i]+"/"+files[i].upper()+"-MODIFIED_MLOAD.dnb"
	if os.path.exists(resultfile):
		loadResults( "Analysis1", resultfile )
		showView( "RESULT" )
		setResultPlot( "contours", "Cauchy Total Stresses/node", "S3" )
#		setResultPlot( "contours", "Total Strains/node", "E1" )
		outputaddress = glob.glob(dir+"/"+files[i]+"/"+"*.out")[0]
		lastMechanicalStep = findLastStep(outputaddress)
		for j in range(1,lastMechanicalStep+1):
			setResultCase( "Analysis1/Output-MLoad/MechanicalLoad, Load-step "+str(j)+ ", Load-factor ")
			setViewSettingValue( "result view setting", "CONTOU/AUTRNG", "LIMITS" )
			setViewSettingValue( "result view setting", "CONTOU/LIMITS/MINVAL", -3.0e+07 )
#   			setViewSettingValue( "result view setting", "CONTOU/LIMITS/MAXVAL", 0.001 )
			setViewPoint( "ISO1" )
			writeToPng( dir+"/"+files[i]+"/"+str(j+100)+".png", 1318, 708 )
	closeProject(  )