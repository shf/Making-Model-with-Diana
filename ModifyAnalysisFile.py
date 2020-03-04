import os
import shutil
import re
def modAnalysisFile(dir):
	with open('GeneralAnalysisfile.dcf', 'r') as file :
		filedata = file.read()
		file.close()
	#os.chdir(str(dir)+"\\GeneratedModels-Modified")
	files = filter(lambda x: (os.path.isdir(os.path.join(str(dir)+"\\GeneratedModels-Modified", x)) and "Model" in x), os.listdir(str(dir)+"\\GeneratedModels-Modified"))
	for i in range(len(files)):
		outputanalysisWindows = "AnalysisW"+files[i]+".dcf"
		outputanalysisLinux = "AnalysisL"+files[i]+".dcf"
		
		
		filedataTempWindows = filedata[:]
		filedataTempLinux = filedata[:]
		
		nodeNumbers = addNodes(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-ModAna.txt")
		
		#Open the file and copy everything upto material data   
		filedataTempWindows = filedataTempWindows.replace('%%USRIFC%%', 'usrifc.dll')
		filedataTempLinux = filedataTempLinux.replace('%%USRIFC%%', '\"usrifc.so\"')
		
		filedataTempWindows = filedataTempWindows.replace('%%ModelName%%', files[i]+"-modified")
		filedataTempLinux = filedataTempLinux.replace('%%ModelName%%', files[i]+"-modified")
		
		filedataTempWindows = filedataTempWindows.replace('%%FORCETOP%%', nodeNumbers[0])
		filedataTempLinux = filedataTempLinux.replace('%%FORCETOP%%', nodeNumbers[0])
		
		filedataTempWindows = filedataTempWindows.replace('%%DISPLACEMENTMIDDLE%%', nodeNumbers[1])
		filedataTempLinux = filedataTempLinux.replace('%%DISPLACEMENTMIDDLE%%', nodeNumbers[1])
		
		filedataTempWindows = filedataTempWindows.replace('%%BondForceReinfo1%%', nodeNumbers[2])
		filedataTempLinux = filedataTempLinux.replace('%%BondForceReinfo1%%', nodeNumbers[2])
		
		filedataTempWindows = filedataTempWindows.replace('%%DisplacementReinfo1%%', nodeNumbers[4])
		filedataTempLinux = filedataTempLinux.replace('%%DisplacementReinfo1%%', nodeNumbers[4])
		
		filedataTempWindows = filedataTempWindows.replace('%%BondForceReinfo2%%', nodeNumbers[3])
		filedataTempLinux = filedataTempLinux.replace('%%BondForceReinfo2%%', nodeNumbers[3])
		
		filedataTempWindows = filedataTempWindows.replace('%%DisplacementReinfo2%%', nodeNumbers[5])
		filedataTempLinux = filedataTempLinux.replace('%%DisplacementReinfo2%%', nodeNumbers[5])
		
		filedataTempWindows = filedataTempWindows.replace('%%DisplacementConReinfo1%%', nodeNumbers[6])
		filedataTempLinux = filedataTempLinux.replace('%%DisplacementConReinfo1%%', nodeNumbers[6])
		
		filedataTempWindows = filedataTempWindows.replace('%%DisplacementConReinfo2%%', nodeNumbers[7])
		filedataTempLinux = filedataTempLinux.replace('%%DisplacementConReinfo2%%', nodeNumbers[7])
		
		os.chdir(str(dir)+"\\GeneratedModels-Modified\\"+files[i])
		with open(outputanalysisWindows, 'w') as outfile:
			outfile.write(filedataTempWindows)
		outfile.close()
		with open(outputanalysisLinux, 'w') as outfile:
			outfile.write(filedataTempLinux)
		outfile.close()
		srcfileWindows = str(dir)+"\\usrifc.dll"
		srcfileLinux = str(dir)+"\\usrifc.f"
		dstdir = str(dir)+"\\GeneratedModels-Modified\\"+files[i]
		if os.path.exists(dstdir+"\\usrifc.dll"):
			os.remove(dstdir+"\\usrifc.dll")
		if os.path.exists(dstdir+"\\usrifc.f"):
			os.remove(dstdir+"\\usrifc.f")
		shutil.copy(srcfileWindows, dstdir)
		shutil.copy(srcfileLinux, dstdir)
		#end
		
def addNodes(filename):
	myFile = open(filename, 'r')
	text = myFile.read().replace('\n', '')
	myFile.close()
	
	text = text.split('NAME')
	text.remove('')
	instance = [0 for i in range(len(text))]
	for i in range(len(text)):
		instance[i] = re.search('\d"(.*?)TR', text[i]).group(0)
	supportTop = instance[0][3:-2]
	yMiddleNode = instance[1][2:-2]
	reinfo1Debond = instance[2][3:-2]
	reinfo2Debond = instance[3][3:-2]
	reinfo1Center = instance[4][3:-2]
	reinfo2Center = instance[5][3:-2]
	concretereinfo1Points = instance[6][3:-2]
	concretereinfo2Points = instance[7][3:-2]
	return([supportTop, yMiddleNode, reinfo1Debond, reinfo2Debond, reinfo1Center, reinfo2Center, concretereinfo1Points, concretereinfo2Points])