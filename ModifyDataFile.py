import numpy as np
import os

def modDataFile(dir):
	files = os.listdir(str(dir)+"\\GeneratedModels")
	for i in range(len(files)):
		#Define Material Data
		#material data here
		case = [0 for k in range(5)]
		#Case1
		case[0] = {}
		case[0]['concreteYoungMod'] = "2.479000E+10"
		case[0]['concretePoison'] = "1.50000E-01"
		case[0]['concreteDensity'] = "2.40000E+03"
		case[0]['concreteTensileStrength'] = "1.37000E+06"
		case[0]['concreteGF1'] = "4.49000E+01"
		case[0]['concreteCompressiveStrength'] = "1.77700E+07"
		#end
		#Case2
		case[1] = {}
		case[1]['concreteYoungMod'] = "2.77800E+10"
		case[1]['concretePoison'] = "1.50000E-01"
		case[1]['concreteDensity'] = "2.40000E+03"
		case[1]['concreteTensileStrength'] = "1.98000E+06"
		case[1]['concreteGF1'] = "5.70000E+01"
		case[1]['concreteCompressiveStrength'] = "2.50000E+07"
		#end
		#Case3
		case[2] = {}
		case[2]['concreteYoungMod'] = "2.95200E+10"
		case[2]['concretePoison'] = "1.50000E-01"
		case[2]['concreteDensity'] = "2.40000E+03"
		case[2]['concreteTensileStrength'] = "2.36000E+06"
		case[2]['concreteGF1'] = "6.47000E+01"
		case[2]['concreteCompressiveStrength'] = "3.00000E+07"
		#end
		#Case4
		case[3] = {}
		case[3]['concreteYoungMod'] = "3.249000E+10"
		case[3]['concretePoison'] = "1.50000E-01"
		case[3]['concreteDensity'] = "2.40000E+03"
		case[3]['concreteTensileStrength'] = "3.02000E+06"
		case[3]['concreteGF1'] = "7.92000E+01"
		case[3]['concreteCompressiveStrength'] = "4.00000E+07"
		#end
		#Case5
		case[4] = {}
		case[4]['concreteYoungMod'] = "3.892000E+10"
		case[4]['concretePoison'] = "1.50000E-01"
		case[4]['concreteDensity'] = "2.40000E+03"
		case[4]['concreteTensileStrength'] = "4.64000E+06"
		case[4]['concreteGF1'] = "11.57000E+01"
		case[4]['concreteCompressiveStrength'] = "6.880000E+07"
		#end
		reinfoYoungMod = "2.10000E+11"
		reinfoPoison = "3.00000E-01"
		reinfoDensity = "7.850000E+03"
		#end
		#end
		for j in [1]:
			try:
				r = float(files[i].split("-r")[1][:2])/1000
			except ValueError:
				r = float(files[i].split("-r")[1][:1])/1000
			originalfile = files[i]+".dat"
			outputfile_A = files[i]+"-case"+str(j+1)+"-modified_A.dat"
			outputfile_B = files[i]+"-case"+str(j+1)+"-modified_B.dat"
			outputfile_ModAna = files[i]+"-case"+str(j+1)+"-ModAna.txt"

			os.chdir(str(dir))

			#storing lines in memory for later use
			os.chdir(str(dir)+"\\GeneratedModels\\"+files[i])
			myFile = open(originalfile, 'r')
			lines = myFile.readlines()
			myFile.close()
			#end

			os.chdir(str(dir)+"\\GeneratedModels-Modified")
			if not os.path.exists(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"-case"+str(j+1)):
					os.makedirs(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"-case"+str(j+1))
			#Open the file and copy everything upto material data    
			os.chdir(str(dir)+"\\GeneratedModels-Modified\\"+files[i]+"-case"+str(j+1))
			outfile_A = open(outputfile_A, "w")
			outfile_B = open(outputfile_B, "w")
			outfile_ModAna = open(outputfile_ModAna, "w")
			end = lines.index("'MATERI'\n")
			for k in range(0, end+1):
				outfile_A.write(lines[k])
			#end

				
			#add concrete material data
			outfile_A.write("   1 NAME   \"Concrete\"\n")
			outfile_A.write("     MCNAME CONCR\n")
			outfile_A.write("     MATMDL TSCR\n")
			outfile_A.write("     YOUNG    " + case[j]['concreteYoungMod'] + "\n")
			outfile_A.write("     POISON   " + case[j]['concretePoison'] + "\n")
			outfile_A.write("     DENSIT   " + case[j]['concreteDensity'] + "\n")
			outfile_A.write("     TOTCRK ROTATE\n")
			outfile_A.write("     TENCRV HORDYK\n")
			outfile_A.write("     REDCRV NONE\n")    
			outfile_A.write("     POIRED NONE\n")
			outfile_A.write("     TENSTR  " + case[j]['concreteTensileStrength'] + "\n")
			outfile_A.write("     GF1      " + case[j]['concreteGF1'] + "\n")
			outfile_A.write("     COMCRV THOREN\n")
			outfile_A.write("     CNFCRV VECCHI\n")
			outfile_A.write("     COMSTR   " + case[j]['concreteCompressiveStrength'] + "\n")
			if case[j]['concreteCompressiveStrength'] == "3.00000E+07":
				outfile_A.write("     NTHORE   2.01200E+00\n")
				outfile_A.write("     KTHORE   1.15400E+00\n")
				outfile_A.write("     LTHORE   3.00000E-01\n")
				outfile_A.write("     RESCST   0.00000E+00\n")
				outfile_A.write("     RESTST   0.00000E+00\n")
			elif case[j]['concreteCompressiveStrength'] == "4.00000E+07":
				outfile_A.write("     NTHORE   2.48500E+00\n")
				outfile_A.write("     KTHORE   1.31500E+00\n")
				outfile_A.write("     LTHORE   3.00000E-01\n")
				outfile_A.write("     RESCST   0.00000E+00\n")
				outfile_A.write("     RESTST   0.00000E+00\n")
			elif case[j]['concreteCompressiveStrength'] == "2.50000E+07":
				outfile_A.write("     NTHORE   1.81800E+00\n")
				outfile_A.write("     KTHORE   1.07300E+00\n")
				outfile_A.write("     LTHORE   3.00000E-01\n")
				outfile_A.write("     RESCST   0.00000E+00\n")
				outfile_A.write("     RESTST   0.00000E+00\n")
				outfile_A.write("     ASPECT\n")
			#end

			#add Loadplate material data
			outfile_A.write("   2 NAME   \"LoadPlate\"\n")
			outfile_A.write("     MCNAME MCSTEL\n")
			outfile_A.write("     MATMDL TRESCA\n")
			outfile_A.write("     YOUNG    2.10000E+11\n")
			outfile_A.write("     POISON   3.00000E-01\n")
			outfile_A.write("     DENSIT   7.80000E+03\n")
			outfile_A.write("     YIELD  VMISES\n")
			outfile_A.write("     YLDSTR  4.90000E+008\n")    
			outfile_A.write("     ASPECT\n")
			#end
			
			#add Woodenplate material data
			outfile_A.write("   3 NAME   \"WoodenPlate\"\n")
			outfile_A.write("     MCNAME MCSTEL\n")
			outfile_A.write("     MATMDL ISOTRO\n")
			outfile_A.write("     YOUNG    1.60000E+009\n")
			outfile_A.write("     POISON   3.50000E-001\n")
			outfile_A.write("     DENSIT   6.00000E+002\n")
			outfile_A.write("     ASPECT\n")
			#end

			#add reinforcement data
			outfile_A.write("   4 NAME   \"Reinforcement\"\n")
			outfile_A.write("     MCNAME MCSTEL\n")
			outfile_A.write("     MATMDL TRESCA\n")
			outfile_A.write("     YOUNG    " + reinfoYoungMod + "\n")
			outfile_A.write("     POISON   " + reinfoPoison + "\n")
			outfile_A.write("     DENSIT   " + reinfoDensity + "\n")
			outfile_A.write("     YIELD  VMISES\n")
			outfile_A.write("     HARDEN STRAIN\n")
			outfile_A.write("     KAPSIG   0.00000E+00   5.35000E+08   1.25000E-01   9.57000E+08\n")    
			outfile_A.write("     ASPECT\n")
			#end

			#add bond material data
			outfile_A.write("   5 NAME   \"Bond\"\n")
			outfile_A.write("     MCNAME INTERF\n")
			outfile_A.write("     DSNZ      " + str(float(case[j]['concreteYoungMod'])*35 * 9.5) + "\n")
			outfile_A.write("     DSNY      " + str(float(case[j]['concreteYoungMod'])*35 * 9.5) + "\n")
			outfile_A.write("     DSSX      " + str(float(case[j]['concreteYoungMod'])*35) + "\n")
			outfile_A.write("     USRIFC     BOTH\n")
			outfile_A.write("     USRVAL     0     0.4     0.05     4.00E-03\n")
			outfile_A.write("                0.00E+00     "+case[j]['concreteCompressiveStrength']+"     1     "+case[j]['concreteTensileStrength']+"\n")
			outfile_A.write("                1.35E-04     "+case[j]['concreteCompressiveStrength']+"     0.86     "+str(float(case[j]['concreteTensileStrength'])*0.0001)+"\n")    
			outfile_A.write("                2.80E-04     "+str(float(case[j]['concreteCompressiveStrength'])*0.997)+"     0.78     0\n")
			outfile_A.write("                4.11E-04     "+str(float(case[j]['concreteCompressiveStrength'])*0.992)+"     0.72     0\n")
			outfile_A.write("                6.21E-04     "+str(float(case[j]['concreteCompressiveStrength'])*0.964)+"     0.65     0\n")
			outfile_A.write("                8.30E-04     "+str(float(case[j]['concreteCompressiveStrength'])*0.939)+"     0.59     0\n")
			outfile_A.write("                1.07E-03     "+str(float(case[j]['concreteCompressiveStrength'])*0.87)+"     0.56     0\n")
			outfile_A.write("                1.51E-03     "+str(float(case[j]['concreteCompressiveStrength'])*0.757)+"     0.52     0\n")
			outfile_A.write("                1.90E-03     "+str(float(case[j]['concreteCompressiveStrength'])*0.704)+"     0.52     0\n")
			outfile_A.write("                2.60E-03     "+str(float(case[j]['concreteCompressiveStrength'])*0.642)+"     0.52     0\n")
			outfile_A.write("                4.71E-03     "+str(float(case[j]['concreteCompressiveStrength'])*0.541)+"     0.52     0\n")
			outfile_A.write("                1.21E-02     "+str(float(case[j]['concreteCompressiveStrength'])*0.676)+"     0.52     0\n")
			outfile_A.write("                1.50E+20     "+str(float(case[j]['concreteCompressiveStrength'])*0.0)+"     0.52     0\n")
			outfile_A.write("                0      0\n")
			outfile_A.write("                1E6    0\n")
			outfile_A.write("                14E9 2.0      "+str(r)+"     0E-6 7.0\n")
			outfile_A.write("     USRSTA  0.0  0.0  0.0  0.0  0.0  0.0  0.0     "+str(float(case[j]['concreteYoungMod'])*35 * 9.5)+"     0.0 0.0 0.0 0.0 0.0\n")
			outfile_A.write("     USRIND  0 13 2\n")
			#end
			
			#add wood concrete interface data
			outfile_A.write("   6 NAME   \"Friction\"\n")
			outfile_A.write("     MCNAME INTERF\n")
			outfile_A.write("     MATMDL FRICTI\n")
			outfile_A.write("     IFTYP  SUR3D\n")
			outfile_A.write("     DSNZ     1.08000E+13\n")
			outfile_A.write("     DSSX     1.14000E+10\n")
			outfile_A.write("     DSSY     1.14000E+10\n")
			outfile_A.write("     FRICTI\n")
			outfile_A.write("     GAP\n")
			outfile_A.write("     COHESI   1.00000E+00\n")
			outfile_A.write("     PHI      1.70000E-01\n")
			outfile_A.write("     PSI      1.70000E-01\n")
			outfile_A.write("     MODE2  0\n")
			outfile_A.write("     GAPVAL   1.00000E+00\n")
			outfile_A.write("     ASPECT\n")
			#end
			
			#adding everything up to support and loads
			# add weight load to A file
			start = lines.index("'GEOMET'\n")
			end = lines.index("CASE 2\n")
			for k in range(start, end):
				outfile_A.write(lines[k])
			#add third phase loads in B file
			start = end
			end = lines.index("'SUPPOR'\n")
			outfile_B.write("PHASE 3\n")
			outfile_B.write("'LOADS'\n")
			for k in range(start, end):
				outfile_B.write(lines[k])
			#add supports to A files
			start =  end
			end = lines.index("NAME \"Geometry support set 4\"\n")
			for k in range(start, end):
				outfile_A.write(lines[k])
			outfile_A.write("'END'\n")
			outfile_A.close()
			#add supports to b file
			start = end
			end = lines.index("NAME \"Geometry support set 5\"\n")
			outfile_B.write("'SUPPOR'\n")
			for k in range(start, end):
				outfile_B.write(lines[k])
			outfile_B.close()
			start = lines.index("NAME \"Geometry support set 4\"\n")
			end = lines.index("'END'\n")
			for k in range(start, end):
				outfile_ModAna.write(lines[k])
			outfile_ModAna.close()