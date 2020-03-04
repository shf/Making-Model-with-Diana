import os
import shutil
from subprocess import call
dirsubmittedfrom = "/c3se/users/fahimi/Glenn/UNIQA/"
files = filter(lambda x: (os.path.isdir(os.path.join('.', x)) and "Model" in x), os.listdir('.'))
dir = os.path.abspath('.')
for i in range(len(files)):
	if os.path.exists(files[i]+"/usrifc.so"):
		os.remove(dstdir+"/usrifc.so")
	shutil.copy("./usrifc.so", files[i])
	os.chdir(files[i])
	os.getcwd()
	call(["echo \""+files[i]+" is begin\" >&1"], shell = True)
	call(["diana",files[i]+"-modified_A.dat","AnalysisL"+files[i]+".dcf"])
	
	call(["rm", "-rf", "*.ff"])
	if not os.path.exists(dirsubmittedfrom+files[i]):
		os.makedirs(dirsubmittedfrom+files[i])
		
	call(["cp", "-p", "-r", "./*", dirsubmittedfrom+files[i]])
	call(["echo \""+files[i]+" is finished\" >&1"], shell = True)
	os.chdir(dir)