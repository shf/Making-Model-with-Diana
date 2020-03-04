# Extracting Data from a Diana table output
# Shayan Fahimi ----------------- 4-19-2016
import pickle
import matplotlib.pyplot as plt
import re
import os

def loadFileFSup(name):
	"""
	This Function will load the support reaction force.
	"""
	inFile = open(name, "r")
	text = inFile.read(); 
	block = text.split('\n  \n  \n  \n')

	if '' in block: block.remove('')
	result = [(0, 0) for i in range(len(block)-1)]
	for i in range(len(block)-1):
		result[i] = (re.search('Load factor(.*?)\n', block[i]).group(0).split()[2], {})
		lines = block[i].split('\n')
		start = lines.index(' Nodnr        FBZ   ')
		for j in range(start+1,len(lines)):
			lineSplitted = lines[j].split()
			result[i][1][int(lineSplitted[0])] = float(lineSplitted[1])
	for i in range(len(result)):
		result[i] = (result[i][0], -sum(result[i][1].values()))
	return result

def loadFileMidDis(name):
	"""
	This Function will load the support reaction force.
	"""
	inFile = open(name, "r")
	text = inFile.read(); 
	block = text.split('\n  \n  \n  \n')

	if '' in block: block.remove('')
	result = [(0, 0) for i in range(len(block)-1)]
	for i in range(len(block)-1):
		result[i] = (re.search('Load factor(.*?)\n', block[i]).group(0).split()[2], {})
		lines = block[i].split('\n')
		start = lines.index(' Nodnr       TDtZ   ')
		nomNodes = len(lines) - start - 1
		for j in range(start+1,len(lines)):
			lineSplitted = lines[j].split()
			result[i][1][int(lineSplitted[0])] = float(lineSplitted[1])
	for i in range(len(result)):
		result[i] = (result[i][0], -sum(result[i][1].values())/nomNodes)
	return result
	
def loadFileReinfoF(name):
	"""
	This Function will load the support reaction force.
	"""
	
	inFile = open(name, "r")
	text = inFile.read(); 
	block = text.split('\n  \n  \n  \n')

	if '' in block: block.remove('')
	result = [(0, 0) for i in range(len(block)-1)]
	for i in range(len(block)-1):
		result[i] = (re.search('Load factor(.*?)\n', block[i]).group(0).split()[2], {})
		lines = block[i].split('\n')
		start = lines.index(' Nodnr        FBX   ')
  		nomNodes = len(lines) - start - 1
		for j in range(start+1,len(lines)):
			lineSplitted = lines[j].split()
			result[i][1][int(lineSplitted[0])] = float(lineSplitted[1])
	for i in range(len(result)):
		result[i] = (result[i][0], sum(result[i][1].values())/nomNodes)
	return result
	    
def loadFileSlip(name):
	"""
	This Function will load the support reaction force.
	"""
	
	inFile = open(name, "r")
	text = inFile.read(); 
	block = text.split('\n  \n  \n  \n')

	if '' in block: block.remove('')
	result = [(0, 0) for i in range(len(block)-1)]
	for i in range(len(block)-1):
		result[i] = (re.search('Load factor(.*?)\n', block[i]).group(0).split()[2], {})
		lines = block[i].split('\n')
		start = lines.index(' Nodnr       TDtX   ')
		nomNodes = len(lines) - start - 1
		for j in range(start+1,len(lines)):
			lineSplitted = lines[j].split()
			result[i][1][int(lineSplitted[0])] = float(lineSplitted[1])
	for i in range(len(result)):
		result[i] = (result[i][0], sum(result[i][1].values())/nomNodes)
	return result
	
def getRandLB(name):
	try:
		r = float(name.split("-r")[1][:2])
	except ValueError:
		r = float(name.split("-r")[1][:1])
	try:
		em = float(name.split("-em")[1][:3])
	except ValueError:
		em = float(name.split("-em")[1][:2])
	return [em, r]
	
	
dir = os.path.dirname(__file__)
	
def plotForceDisp(dir):
	"""
	Plot ForceDisp and save them in the folder
	"""
	files = filter(lambda x: (os.path.isdir(os.path.join(str(dir)+"\\GeneratedModels-Modified", x)) and "Model" in x), os.listdir(str(dir)+"\\GeneratedModels-Modified"))
	for i in range(len(files)):
		appliedForceOutput = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-FST.tb"
		midDispOutput = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-DISMID.tb"
		if os.path.exists(appliedForceOutput) and os.path.exists(midDispOutput):
			appliedForce = loadFileFSup(appliedForceOutput)
			midDisp = loadFileMidDis(midDispOutput)
			fig = plt.figure(figsize=(10, 10))
			plt.plot([x[1]*1000 for x in midDisp], [(4.*x[1])/1000 for x in appliedForce], 'k-', label = 'Force-Displacement', linewidth=3.0)
			print([(x[0], 4*x[1]/1000) for x in appliedForce])
			plt.ylabel('Force(kN)', fontsize=20)
			plt.xlabel('Displacement(mm)', fontsize=20)
			plt.legend(fontsize=20, loc='best')
			plt.savefig(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-ForceDisp"+ '.png')
		else:
			pass

def plotBondSlip(dir):
	"""
	Plot ForceDisp and save them in the folder
	"""
	files = filter(lambda x: (os.path.isdir(os.path.join(str(dir)+"\\GeneratedModels-Modified", x)) and "Model" in x), os.listdir(str(dir)+"\\GeneratedModels-Modified"))
	for i in range(len(files)):
		appliedForceReinfo1Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-FR1.tb"
		dispReinfo1Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-DR1.tb"
		#appliedForceReinfo2Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-FR2.tb"
		#dispReinfo2Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-DR2.tb"
		concreteReinfo1Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-CR1.tb"
		#concreteReinfo2Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-CR2.tb"
		if os.path.exists(appliedForceReinfo1Output) and \
			os.path.exists(dispReinfo1Output) and os.path.exists(concreteReinfo1Output):
			#os.path.exists(appliedForceReinfo2Output) and \
			#os.path.exists(dispReinfo2Output) and \
			#os.path.exists(concreteReinfo2Output):
			appliedForceReinfo1 = loadFileReinfoF(appliedForceReinfo1Output)
			dispReinfo1 = [x[1] for x in loadFileSlip(dispReinfo1Output)]
			#appliedForceReinfo2 = loadFileReinfoF(appliedForceReinfo2Output)
			#dispReinfo2 = [x[1] for x in loadFileSlip(dispReinfo2Output)]
			concreteReinfo1Disp = [x[1] for x in loadFileSlip(concreteReinfo1Output)]
			#concreteReinfo2Disp = [x[1] for x in loadFileSlip(concreteReinfo2Output)]
			em , r = getRandLB(files[i])
			bond1 = [x[1]*(8.)/(2*3.14*r*em) for x in appliedForceReinfo1]
			#bond2 = [x[1]*(8.)/(2*3.14*r*em) for x in appliedForceReinfo2]
			slip1 = [(x - y)*1000 for x, y in zip(dispReinfo1, concreteReinfo1Disp)]
			#slip2 = [(x - y)*1000 for x, y in zip(dispReinfo2, concreteReinfo2Disp)]
			fig = plt.figure(figsize=(10, 10))
			plt.plot(slip1 ,bond1, 'k-', label = 'Bond-Slip side reinforcement', linewidth=3.0)
			#plt.plot(slip2 ,bond2, 'r.-', label = 'Bond-Slip middle reinforcement', linewidth=3.0)
			plt.ylabel('Bond(MPa)', fontsize=20)
			plt.xlabel('Slip(mm)', fontsize=20)
			plt.legend(fontsize=20, loc='best')
			plt.savefig(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-BondSlip"+ '.png')
		else:
			pass

def plotForceBond(dir):
	files = filter(lambda x: (os.path.isdir(os.path.join(str(dir)+"\\GeneratedModels-Modified", x)) and "Model" in x), os.listdir(str(dir)+"\\GeneratedModels-Modified"))
	for i in range(len(files)):
		dispReinfo1Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-DR1.tb"
		#dispReinfo2Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-DR2.tb"
		appliedForceOutput = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-FST.tb"
		concreteReinfo1Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-CR1.tb"
		#concreteReinfo2Output = str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-CR2.tb"
		if os.path.exists(dispReinfo1Output) and os.path.exists(appliedForceOutput) and os.path.exists(concreteReinfo1Output):
			#os.path.exists(dispReinfo2Output) and \
			#os.path.exists(concreteReinfo2Output):
			dispReinfo1 = [x[1] for x in loadFileSlip(dispReinfo1Output)]
			#dispReinfo2 = [x[1] for x in loadFileSlip(dispReinfo2Output)]
			appliedForce = loadFileFSup(appliedForceOutput)
			concreteReinfo1Disp = [x[1] for x in loadFileSlip(concreteReinfo1Output)]
			#concreteReinfo2Disp = [x[1] for x in loadFileSlip(concreteReinfo2Output)]
			em , r = getRandLB(files[i])
			slip1 = [(x - y)*1000 for x, y in zip(dispReinfo1, concreteReinfo1Disp)]
			#slip2 = [(x - y)*1000 for x, y in zip(dispReinfo2, concreteReinfo2Disp)]
			fig = plt.figure(figsize=(10, 10))
			plt.plot(slip1,[x[1]/1000 for x in appliedForce], 'k-', label = 'Force-Slip side reinforcement', linewidth=3.0)
			#plt.plot(slip2,[x[1]/1000 for x in appliedForce], 'r.-', label = 'Force-Slip middle reinforcement', linewidth=3.0)
			plt.ylabel('Force(kN)', fontsize=20)
			plt.xlabel('slip(mm)', fontsize=20)
			plt.legend(fontsize=20, loc='best')
			plt.savefig(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"\\"+files[i]+"-MODIFIED_MLOAD-ForceSlip"+ '.png')
		else:
			pass
	
plotForceDisp(dir)
plotBondSlip(dir)
plotForceBond(dir)