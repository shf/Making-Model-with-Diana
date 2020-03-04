#dimensional values here
xLength = 0.7
supportDistance = 0.15
xPlateLength = 0.04
zPlateLength = 0.015
xWoodenPlateLength = xPlateLength
zWoodenPlateLength = 0.005
zLength = 0.15
embeddedLengthList = [0.1]
concreteCoverRatioList = [1.0]
rList = [0.008]
#end

for embeddedLength in embeddedLengthList:
	for r in rList:
		for concreteCoverRatio in concreteCoverRatioList:
			import math
			import os
			dir = "Model the structure/My Model/Allfiles/GeneratedModels"
			newProject( dir, 10 )
			setModelAnalysisAspects( [ "STRUCT" ] )
			setModelDimension( "3D" )
			setDefaultMeshOrder( "LINEAR" )
			setDefaultMesherType( "TETTRIA" )
			#Geometrical Calculation
			rBig = 1.5 * r
			concreteCover = concreteCoverRatio * 2.0 * rBig
			s = 2 * concreteCover
			yLength = 2*((concreteCover + 3.0*rBig) + (max(concreteCover, 0.02)))
			reinfo1 = [0, concreteCover+rBig, concreteCover+rBig]
			reinfo2 = [0, yLength/2, concreteCover+rBig]
			xMidDisPlate = (supportDistance/2.0 - xPlateLength/2.0)
			xDisBottomPlate = embeddedLength+s
			#end
			point = [[0]*3 for i in range(8)]
			pointBig = [[0]*3 for i in range(8)]
			midPoint = [[0]*3 for i in range(8)]
			xAxis = [[0]*3 for i in range(8)]
			for i in range(0, 8):
				point[i] = [x * r for x in [0, -math.sin(math.radians(i*45)), math.cos(math.radians(i*45))]]
				midPoint[i] = [x * r for x in [xLength/4., -math.sin(math.radians(i*45+45/2.)), math.cos(math.radians(i*45+45/2.))]]
				xAxis[i] = [0.0, -math.cos(math.radians(i*45+45/2.)), -math.sin(math.radians(i*45+45/2.))]
				pointBig[i] = [x + y for x, y in zip([embeddedLength, 0, 0], [x * rBig for x in [0, -math.sin(math.radians(i*45)), math.cos(math.radians(i*45))]])]
			#end
			#create block of concrete and load blocks
			createBlock( "Concrete-Block", [ 0, 0, 0 ], [ xLength/2.0, yLength/2.0, zLength ] )
			createBlock( "Wooden-Block1", [ xDisBottomPlate, 0, -zWoodenPlateLength ], [ xPlateLength, yLength/2.0, zWoodenPlateLength ] )
			createBlock( "Wooden-Block2", [ xLength/2. - xMidDisPlate - xPlateLength, 0, zLength ], [ xPlateLength, yLength/2.0, zWoodenPlateLength ] )
			createBlock( "Load-Block1", [ xDisBottomPlate, 0, -(zPlateLength+zWoodenPlateLength) ], [ xPlateLength, yLength/2.0, zPlateLength ] )
			createBlock( "Load-Block2", [ xLength/2. - xMidDisPlate - xPlateLength, 0, (zLength+zWoodenPlateLength) ], [ xPlateLength, yLength/2.0, zPlateLength ] )
			setViewPoint( "ISO1" )
			#end
			# Subtract two Polynominal from geometry
			createSheet( "Poly1", [[x + y for x, y in zip(reinfo1, point[0])],[x + y for x, y in zip(reinfo1, point[1])],[x + y for x, y in zip(reinfo1, point[2])],[x + y for x, y in zip(reinfo1, point[3])],[x + y for x, y in zip(reinfo1, point[4])],[x + y for x, y in zip(reinfo1, point[5])],[x + y for x, y in zip(reinfo1, point[6])],[x + y for x, y in zip(reinfo1, point[7])]] )
			#createSheet( "Poly2", [[x + y for x, y in zip(reinfo2, point[0])],[x + y for x, y in zip(reinfo2, point[1])],[x + y for x, y in zip(reinfo2, point[2])],[x + y for x, y in zip(reinfo2, point[3])],[x + y for x, y in zip(reinfo2, point[4])],[x + y for x, y in zip(reinfo2, point[5])],[x + y for x, y in zip(reinfo2, point[6])],[x + y for x, y in zip(reinfo2, point[7])]] )
			extrudeProfile( "Poly1", [ embeddedLength, 0, 0 ] )
			#extrudeProfile( "Poly2", [ embeddedLength, 0, 0 ] )
			#subtract( "Concrete-Block", [ "Poly1", "Poly2" ], False, True )
			subtract( "Concrete-Block", [ "Poly1"], False, True )
			createSheet( "Poly1-Big", [[x + y for x, y in zip(reinfo1, pointBig[0])],[x + y for x, y in zip(reinfo1, pointBig[1])],[x + y for x, y in zip(reinfo1, pointBig[2])],[x + y for x, y in zip(reinfo1, pointBig[3])],[x + y for x, y in zip(reinfo1, pointBig[4])],[x + y for x, y in zip(reinfo1, pointBig[5])],[x + y for x, y in zip(reinfo1, pointBig[6])],[x + y for x, y in zip(reinfo1, pointBig[7])]] )
			#createSheet( "Poly2-Big", [[x + y for x, y in zip(reinfo2, pointBig[0])],[x + y for x, y in zip(reinfo2, pointBig[1])],[x + y for x, y in zip(reinfo2, pointBig[2])],[x + y for x, y in zip(reinfo2, pointBig[3])],[x + y for x, y in zip(reinfo2, pointBig[4])],[x + y for x, y in zip(reinfo2, pointBig[5])],[x + y for x, y in zip(reinfo2, pointBig[6])],[x + y for x, y in zip(reinfo2, pointBig[7])]] )
			extrudeProfile( "Poly1-Big", [ xLength/2, 0, 0 ] )
			#extrudeProfile( "Poly2-Big", [ xLength/2, 0, 0 ] )
			#subtract( "Concrete-Block", [ "Poly1-Big", "Poly2-Big" ], False, True )
			subtract( "Concrete-Block", [ "Poly1-Big"], False, True )
			#end

			# Create reinforcement cylinders
			createSheet( "Reinforcement1", [[x + y for x, y in zip(reinfo1, point[0])],[x + y for x, y in zip(reinfo1, point[1])],[x + y for x, y in zip(reinfo1, point[2])],[x + y for x, y in zip(reinfo1, point[3])],[x + y for x, y in zip(reinfo1, point[4])],[x + y for x, y in zip(reinfo1, point[5])],[x + y for x, y in zip(reinfo1, point[6])],[x + y for x, y in zip(reinfo1, point[7])]] )
			#createSheet( "Reinforcement2", [[x + y for x, y in zip(reinfo2, point[0])],[x + y for x, y in zip(reinfo2, point[1])],[x + y for x, y in zip(reinfo2, point[2])],[x + y for x, y in zip(reinfo2, point[3])],[x + y for x, y in zip(reinfo2, point[4])]] )
			extrudeProfile( "Reinforcement1", [ xLength/2, 0, 0 ] )
			#extrudeProfile( "Reinforcement2", [ xLength/2, 0, 0 ] )
			#end

			#add concrete material
			addMaterial( "Concrete", "CONCR", "TSCR", [] )
			setParameter( "MATERIAL", "Concrete", "LINEAR/ELASTI/YOUNG", 0.1 )
			setParameter( "MATERIAL", "Concrete", "LINEAR/ELASTI/POISON", 0.1 )
			setParameter( "MATERIAL", "Concrete", "LINEAR/MASS/DENSIT", 0.1 )
			setParameter( "MATERIAL", "Concrete", "MODTYP/TOTCRK", "ROTATE" )
			setParameter( "MATERIAL", "Concrete", "TENSIL/TENSTR", 0.1 )
			addGeometry( "Element geometry 1", "SOLID", "STRSOL", [] )
			rename( "GEOMET", "Element geometry 1", "Concrete-Geometry" )
			addElementData( "Concrete-Data" )
			clearReinforcementAspects( [ "Concrete-Block" ] )
			setElementClassType( [ "Concrete-Block" ], "STRSOL" )
			assignMaterial( "Concrete", "SHAPE", [ "Concrete-Block" ] )
			assignGeometry( "Concrete-Geometry", "SHAPE", [ "Concrete-Block" ] )
			assignElementData( "Concrete-Data", "SHAPE", [ "Concrete-Block" ] )
			#end
			#add LoadPlate material
			addMaterial( "LoadPlate", "MCSTEL", "TRESCA", [] )
			setParameter( "MATERIAL", "LoadPlate", "LINEAR/ELASTI/YOUNG", 0.1 )
			setParameter( "MATERIAL", "LoadPlate", "LINEAR/ELASTI/POISON", 0.1 )
			setParameter( "MATERIAL", "LoadPlate", "LINEAR/MASS/DENSIT", 0.1 )
			setParameter( "MATERIAL", "LoadPlate", "TREPLA/YLDSTR", 0.1 )
			addGeometry( "Element geometry 2", "SOLID", "STRSOL", [] )
			rename( "GEOMET", "Element geometry 2", "LoadPlate-Geometry" )
			addElementData( "LoadPlate-Data" )
			clearReinforcementAspects( [ "Load-Block1" ] )
			setElementClassType( [ "Load-Block1" ], "STRSOL" )
			assignMaterial( "LoadPlate", "SHAPE", [ "Load-Block1" ] )
			assignGeometry( "LoadPlate-Geometry", "SHAPE", [ "Load-Block1" ] )
			assignElementData( "LoadPlate-Data", "SHAPE", [ "Load-Block1" ] )
			clearReinforcementAspects( [ "Load-Block2" ] )
			setElementClassType( [ "Load-Block2" ], "STRSOL" )
			assignMaterial( "LoadPlate", "SHAPE", [ "Load-Block2" ] )
			assignGeometry( "LoadPlate-Geometry", "SHAPE", [ "Load-Block2" ] )
			assignElementData( "LoadPlate-Data", "SHAPE", [ "Load-Block2" ] )
			#end
			#add WoodenPlate material
			addMaterial( "WoodenPlate", "MCSTEL", "TRESCA", [] )
			setParameter( "MATERIAL", "WoodenPlate", "LINEAR/ELASTI/YOUNG", 0.2 )
			setParameter( "MATERIAL", "WoodenPlate", "LINEAR/ELASTI/POISON", 0.2 )
			setParameter( "MATERIAL", "WoodenPlate", "LINEAR/MASS/DENSIT", 0.2 )
			setParameter( "MATERIAL", "WoodenPlate", "TREPLA/YLDSTR", 0.2 )
			addGeometry( "Element geometry 3", "SOLID", "STRSOL", [] )
			rename( "GEOMET", "Element geometry 3", "WoodenPlate-Geometry" )
			addElementData( "WoodenPlate-Data" )
			clearReinforcementAspects( [ "Wooden-Block1" ] )
			setElementClassType( [ "Wooden-Block1" ], "STRSOL" )
			assignMaterial( "WoodenPlate", "SHAPE", [ "Wooden-Block1" ] )
			assignGeometry( "WoodenPlate-Geometry", "SHAPE", [ "Wooden-Block1" ] )
			assignElementData( "WoodenPlate-Data", "SHAPE", [ "Wooden-Block1" ] )
			clearReinforcementAspects( [ "Wooden-Block2" ] )
			setElementClassType( [ "Wooden-Block2" ], "STRSOL" )
			assignMaterial( "WoodenPlate", "SHAPE", [ "Wooden-Block2" ] )
			assignGeometry( "WoodenPlate-Geometry", "SHAPE", [ "Wooden-Block2" ] )
			assignElementData( "WoodenPlate-Data", "SHAPE", [ "Wooden-Block2" ] )
			#end
			#add reinforcement material
			addMaterial( "Reinforcement", "MCSTEL", "TRESCA", [] )
			setParameter( "MATERIAL", "Reinforcement", "LINEAR/ELASTI/YOUNG", 0.1 )
			setParameter( "MATERIAL", "Reinforcement", "LINEAR/ELASTI/POISON", 0.1 )
			setParameter( "MATERIAL", "Reinforcement", "LINEAR/MASS/DENSIT", 0.1 )
			setParameter( "MATERIAL", "Reinforcement", "TREPLA/YLDSTR", 0.1 )
			addGeometry( "Element geometry 4", "SOLID", "STRSOL", [] )
			rename( "GEOMET", "Element geometry 4", "Reinforcement-Geometry" )
			addElementData( "Reinforcement-Data" )
			#clearReinforcementAspects( [ "Reinforcement1", "Reinforcement2" ] )
			#setElementClassType( [ "Reinforcement1", "Reinforcement2" ], "STRSOL" )
			#assignMaterial( "Reinforcement", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
			#assignGeometry( "Reinforcement-Geometry", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
			#assignElementData( "Reinforcement-Data", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
			clearReinforcementAspects( [ "Reinforcement1"] )
			setElementClassType( [ "Reinforcement1"], "STRSOL" )
			assignMaterial( "Reinforcement", "SHAPE", [ "Reinforcement1"] )
			assignGeometry( "Reinforcement-Geometry", "SHAPE", [ "Reinforcement1"] )
			assignElementData( "Reinforcement-Data", "SHAPE", [ "Reinforcement1"] )
			#end


			#define interface material and make interface elements
			addMaterial( "Bond", "INTERF", "ELASTI", [] )
			setParameter( "MATERIAL", "Bond", "LINEAR/ELAS6/DSNZ", 0.1 )
			setParameter( "MATERIAL", "Bond", "LINEAR/ELAS6/DSSX", 0.1 )
			setParameter( "MATERIAL", "Bond", "LINEAR/ELAS6/DSSY", 0.1 )
			for i in range(0, 8):
				addGeometry( "Int"+str(i), "SHEET", "STRINT", [] )
				setParameter( "GEOMET", "Int"+str(i), "LOCAXS", True )
				setParameter( "GEOMET", "Int"+str(i), "LOCAXS/XAXIS", xAxis[i] )
				setInterfaceContactAspects( "SHAPEFACE", "Reinforcement1", [[x + y for x, y in zip(reinfo1, midPoint[i])]], "Bond" )
				setElementClassType( "SHAPEFACE", "Reinforcement1", [[x + y for x, y in zip(reinfo1, midPoint[i])]], "STRINT" )
				assignGeometry( "Int"+str(i), "SHAPEFACE", "Reinforcement1", [[x + y for x, y in zip(reinfo1, midPoint[i])]] )
				resetElementData( "SHAPEFACE", "Reinforcement1", [[x + y for x, y in zip(reinfo1, midPoint[i])]] )
				addElementData( "Int"+str(i) )
				assignElementData( "Int"+str(i), "SHAPEFACE", "Reinforcement1", [[x + y for x, y in zip(reinfo1, midPoint[i])]] )
			# for i in range(8, 12):
				# addGeometry( "Int"+str(i), "SHEET", "STRINT", [] )
				# setParameter( "GEOMET", "Int"+str(i), "LOCAXS", True )
				# setParameter( "GEOMET", "Int"+str(i), "LOCAXS/XAXIS", xAxis[i - 8] )
				# setInterfaceContactAspects( "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]], "Bond" )
				# setElementClassType( "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]], "STRINT" )
				# assignGeometry( "Int"+str(i), "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]] )
				# resetElementData( "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]] )
				# addElementData( "Int"+str(i) )
				# assignElementData( "Int"+str(i), "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]] )
			#end
			
			#define interface for wood concrete
			addMaterial( "Friction", "INTERF", "ELASTI", [] )
			addGeometry( "WoodCon-Interface", "SHEET", "STRINT", [] )
			setParameter( "GEOMET", "WoodCon-Interface", "LOCAXS", True )
			setInterfaceContactAspects( "SHAPEFACE", "Wooden-Block1", [[xDisBottomPlate+xPlateLength/2., yLength/2., 0]], "Friction" )
			setInterfaceContactAspects( "SHAPEFACE", "Wooden-Block2", [[xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength/2]], "Friction" )
			setElementClassType( "SHAPEFACE", "Wooden-Block1", [[xDisBottomPlate+xPlateLength/2., yLength/2., 0]], "STRINT" )
			setElementClassType( "SHAPEFACE", "Wooden-Block2",  [[xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength/2]], "STRINT" )
			assignGeometry( "WoodCon-Interface", "SHAPEFACE", "Wooden-Block1", [[xDisBottomPlate+xPlateLength/2., yLength/2., 0]] )
			assignGeometry( "WoodCon-Interface", "SHAPEFACE", "Wooden-Block2", [[xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength/2]] )
			resetElementData( "SHAPEFACE", "Wooden-Block1", [[xDisBottomPlate+xPlateLength/2., yLength/2., 0]] )
			addElementData( "WoodCon-Interface" )
			assignElementData( "WoodCon-Interface", "SHAPEFACE", "Wooden-Block1", [[xDisBottomPlate+xPlateLength/2., yLength/2., 0]] )
			resetElementData( "SHAPEFACE", "Wooden-Block2", [[xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength/2]] )
			assignElementData( "WoodCon-Interface", "SHAPEFACE", "Wooden-Block2", [[xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength/2]] )
			#end
			
			#add support mirror about x axis
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 1" )
			createSurfaceSupport( "ReflectX", "Geometry support set 1" )
			setParameter( "GEOMETRYSUPPORT", "ReflectX", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "ReflectX", "TRANSL", [ 1, 0, 0 ] )
			setParameter( "GEOMETRYSUPPORT", "ReflectX", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "ReflectX", "Concrete-Block", [[ xLength/2., 0, 0 ]] )
			attach( "GEOMETRYSUPPORT", "ReflectX", "Reinforcement1", [[ xLength/2., reinfo1[1], reinfo1[2] ]] )
			#attach( "GEOMETRYSUPPORT", "ReflectX", "Reinforcement2", [[ xLength/2., reinfo2[1]-r/2., reinfo2[2] ]] )
			#end
			#add support mirror about y axis
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 2" )
			createSurfaceSupport( "ReflectY", "Geometry support set 2" )
			setParameter( "GEOMETRYSUPPORT", "ReflectY", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "ReflectY", "TRANSL", [ 0, 1, 0 ] )
			setParameter( "GEOMETRYSUPPORT", "ReflectY", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "ReflectY", "Concrete-Block", [[ xLength/4., yLength/2., zLength/2. ], [ xLength/4., yLength/2., 0.0 ]] )
			attach( "GEOMETRYSUPPORT", "ReflectY", "Load-Block1", [[ xDisBottomPlate + xPlateLength/2., yLength/2., -zWoodenPlateLength-zPlateLength/2. ]] )
			attach( "GEOMETRYSUPPORT", "ReflectY", "Load-Block2", [[ xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength+zWoodenPlateLength+zPlateLength/2. ]] )
			attach( "GEOMETRYSUPPORT", "ReflectY", "Wooden-Block1", [[ xDisBottomPlate + xPlateLength/2., yLength/2., -zWoodenPlateLength/2. ]] )
			attach( "GEOMETRYSUPPORT", "ReflectY", "Wooden-Block2", [[ xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength+zWoodenPlateLength/2. ]] )
			#attach( "GEOMETRYSUPPORT", "ReflectY", "Reinforcement2", [[ 0, yLength/2., reinfo2[2] ]] )
			#end
			#add bottom support
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 3" )
			createSurfaceSupport( "Support-Bottom", "Geometry support set 3" )
			setParameter( "GEOMETRYSUPPORT", "Support-Bottom", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "Support-Bottom", "TRANSL", [ 0, 0, 1 ] )
			setParameter( "GEOMETRYSUPPORT", "Support-Bottom", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "Support-Bottom", "Load-Block1", [[ xDisBottomPlate+xPlateLength/2., yLength/4., -zPlateLength ]] )
			#end
			#add top support
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 4" )
			createSurfaceSupport( "Support-Top", "Geometry support set 4" )
			setParameter( "GEOMETRYSUPPORT", "Support-Top", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "Support-Top", "TRANSL", [ 1, 1, 1 ] )
			setParameter( "GEOMETRYSUPPORT", "Support-Top", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "Support-Top", "Load-Block2", [[ xLength/2. - xMidDisPlate - xPlateLength/2., yLength/4., zPlateLength+zLength ]] )
			#end
			#add supports to get nodes
			#y middle node for force-displacement curve
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 5" )
			createPointSupport( "yMiddleNode", "Geometry support set 5" )
			setParameter( "GEOMETRYSUPPORT", "yMiddleNode", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "yMiddleNode", "TRANSL", [ 0, 0, 1 ] )
			setParameter( "GEOMETRYSUPPORT", "yMiddleNode", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "yMiddleNode", "Concrete-Block", [[ xLength/2, yLength/2, 0 ]] )
			#end
			#reinforcement one surface for bond slip curve
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 6" )
			createSurfaceSupport( "reinforcement1_debond", "Geometry support set 6" )
			setParameter( "GEOMETRYSUPPORT", "reinforcement1_debond", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "reinforcement1_debond", "TRANSL", [ 1, 0, 0 ] )
			setParameter( "GEOMETRYSUPPORT", "reinforcement1_debond", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "reinforcement1_debond", "Reinforcement1", [[ xLength/2., reinfo1[1], reinfo1[2] ]] )
			#end
			#reinforcement two surface for bond slip curve
			#addSet( "GEOMETRYSUPPORTSET", "Geometry support set 7" )
			#createSurfaceSupport( "reinforcement2_debond", "Geometry support set 7" )
			#setParameter( "GEOMETRYSUPPORT", "reinforcement2_debond", "AXES", [ 1, 2 ] )
			#setParameter( "GEOMETRYSUPPORT", "reinforcement2_debond", "TRANSL", [ 1, 0, 0 ] )
			#setParameter( "GEOMETRYSUPPORT", "reinforcement2_debond", "ROTATI", [ 0, 0, 0 ] )
			#attach( "GEOMETRYSUPPORT", "reinforcement2_debond", "Reinforcement2", [[ xLength/2., reinfo2[1]-r/2., reinfo2[2] ]] )
			#end
			#surface reinforcement 1 displacement for bond slip curve
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 8" )
			createSurfaceSupport( "reinforcement1_center", "Geometry support set 8" )
			setParameter( "GEOMETRYSUPPORT", "reinforcement1_center", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "reinforcement1_center", "TRANSL", [ 1, 0, 0 ] )
			setParameter( "GEOMETRYSUPPORT", "reinforcement1_center", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "reinforcement1_center", "Reinforcement1", [[ reinfo1[0], reinfo1[1], reinfo1[2] ]] )
			#end
			#surface  reinforcement 2 displacement for bond slip curve
			#addSet( "GEOMETRYSUPPORTSET", "Geometry support set 9" )
			#createSurfaceSupport( "reinforcement2_center", "Geometry support set 9" )
			#setParameter( "GEOMETRYSUPPORT", "reinforcement2_center", "AXES", [ 1, 2 ] )
			#setParameter( "GEOMETRYSUPPORT", "reinforcement2_center", "TRANSL", [ 1, 0, 0 ] )
			#setParameter( "GEOMETRYSUPPORT", "reinforcement2_center", "ROTATI", [ 0, 0, 0 ] )
			#attach( "GEOMETRYSUPPORT", "reinforcement2_center", "Reinforcement2", [[ reinfo2[0], reinfo2[1]-r/2., reinfo2[2] ]] )
			#end
			#points around reinforcement one
			addSet( "GEOMETRYSUPPORTSET", "Geometry support set 10" )
			createPointSupport( "aroundReinfoOne", "Geometry support set 10" )
			setParameter( "GEOMETRYSUPPORT", "aroundReinfoOne", "AXES", [ 1, 2 ] )
			setParameter( "GEOMETRYSUPPORT", "aroundReinfoOne", "TRANSL", [ 1, 0, 0 ] )
			setParameter( "GEOMETRYSUPPORT", "aroundReinfoOne", "ROTATI", [ 0, 0, 0 ] )
			attach( "GEOMETRYSUPPORT", "aroundReinfoOne", "Concrete-Block", [[x + y for x, y in zip(reinfo1, point[0])],[x + y for x, y in zip(reinfo1, point[1])],[x + y for x, y in zip(reinfo1, point[2])],[x + y for x, y in zip(reinfo1, point[3])],[x + y for x, y in zip(reinfo1, point[4])],[x + y for x, y in zip(reinfo1, point[5])],[x + y for x, y in zip(reinfo1, point[6])],[x + y for x, y in zip(reinfo1, point[7])]])
			#end
			#points around reinforcement two
			#addSet( "GEOMETRYSUPPORTSET", "Geometry support set 11" )
			#createPointSupport( "aroundReinfoTwo", "Geometry support set 11" )
			#setParameter( "GEOMETRYSUPPORT", "aroundReinfoTwo", "AXES", [ 1, 2 ] )
			#setParameter( "GEOMETRYSUPPORT", "aroundReinfoTwo", "TRANSL", [ 1, 0, 0 ] )
			#setParameter( "GEOMETRYSUPPORT", "aroundReinfoTwo", "ROTATI", [ 0, 0, 0 ] )
			#attach( "GEOMETRYSUPPORT", "aroundReinfoTwo", "Concrete-Block", [[x + y for x, y in zip(reinfo2, point[0])],[x + y for x, y in zip(reinfo2, point[1])],[x + y for x, y in zip(reinfo2, point[2])],[x + y for x, y in zip(reinfo2, point[3])],[x + y for x, y in zip(reinfo2, point[4])],[x + y for x, y in zip(reinfo2, point[5])],[x + y for x, y in zip(reinfo2, point[6])],[x + y for x, y in zip(reinfo2, point[7])]])
			#end
			#end
			#hide supports
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 1" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 2" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 3" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 4" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 5" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 6" ] )
			#hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 7" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 8" ] )
			#hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 9" ] )
			hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 10" ] )
			#hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 11" ] )
			#end
			#add dead load - Weight
			addSet( "GEOMETRYLOADSET", "Geometry load set 1" )
			createModelLoad( "Weight-Load", "Geometry load set 1" )
			#end
			#add deformation load
			addSet( "GEOMETRYLOADSET", "Geometry load set 2" )
			createSurfaceLoad( "DisplacementLoad", "Geometry load set 2" )
			setParameter( "GEOMETRYLOAD", "DisplacementLoad", "LODTYP", "DEFORM" )
			setParameter( "GEOMETRYLOAD", "DisplacementLoad", "DEFORM/VALUE", -0.001 )
			setParameter( "GEOMETRYLOAD", "DisplacementLoad", "DEFORM/DIRECT", 3 )
			attach( "GEOMETRYLOAD", "DisplacementLoad", "Load-Block2", [[ xLength/2. - xMidDisPlate - xPlateLength/2., yLength/4., zPlateLength+zLength ]] )
			#end
			#Generate Mesh
			#setElementSize( ["Reinforcement1", "Reinforcement2" ], r )
			setElementSize( ["Reinforcement1"], r )
			setElementSize( ["Wooden-Block1", "Wooden-Block2" ], zWoodenPlateLength )
			setElementSize( [ "Concrete-Block", "Load-Block1", "Load-Block2"], 1.6 * r )
			#setMesherType( [ "Concrete-Block", "Load-Block1", "Load-Block2", "Reinforcement1", "Reinforcement2", "Wooden-Block1", "Wooden-Block2"], "TETTRIA" )
			setMesherType( [ "Concrete-Block", "Load-Block1", "Load-Block2", "Reinforcement1", "Wooden-Block1", "Wooden-Block2"], "TETTRIA" )
			generateMesh( [] )
			#end
			#r = reinforcement radius
			#ccr = concreteCoverRatio
			#em = Embedded length
			path = "Model-em"+str(embeddedLength*1000)[:-2]+"-r"+str(r*1000)[:-2]+"NoMiddle"
			if not os.path.exists(".\\GeneratedModels\\"+path):
				os.makedirs(".\\GeneratedModels\\"+path)
			exportModel(".\\GeneratedModels\\"+path+"\\"+path+".dat", 5 )
			setViewPoint( "ISO2" )
			#setMeshColor( "ELEMENT", "#ff00ff", [ "Reinforcement2", "Reinforcement1" ] )
			setMeshColor( "ELEMENT", "#ff00ff", [ "Reinforcement1" ] )
			writeToPng(".\\GeneratedModels\\"+path+"\\"+path+".png", 1318, 708 )
			#save properties alongside
			dataFile = open(".\\GeneratedModels\\"+path+"\\data.txt", 'w+')
			dataFile.write("All data are written in mili meters\n")
			dataFile.write("x direction length\t=\t" + str(xLength*1000) + "\n")
			dataFile.write("y direction length\t=\t" + str(yLength*1000) + "\n")
			dataFile.write("z direction lenght\t=\t" + str(zLength*1000) + "\n")
			dataFile.write("x direction plate length\t=\t" + str(xPlateLength*1000) + "\n")
			dataFile.write("z direction plate length\t=\t" + str(zPlateLength*1000) + "\n")
			dataFile.write("support distance in the middle\t=\t" + str(supportDistance*1000) + "\n")
			dataFile.write("reinforcement radius\t=\t" + str(r*1000) + "\n")
			dataFile.write("lb\t=\t" + str(embeddedLength*1000) + "\n")
			dataFile.write("s\t=\t" + str(s*1000) + "\n")
			dataFile.write("concreteCoverRatio\t=\t" + str(concreteCoverRatio) + "\n")
			dataFile.write("concreteCover\t=\t" + str(concreteCover*1000) + "\n")
			dataFile.write("radius of debonding\t=\t" + str(rBig*1000) + "\n")
			dataFile.write("x direction distance to bottom support\t=\t" + str(xDisBottomPlate*1000) + "\n")
			dataFile.write("top support to middle distance x direction\t=\t" + str(xMidDisPlate*1000) + "\n")
			dataFile.write("first reinforcement center coordination\t=\t"+(str(reinfo1[0]*1000)+"\t"+str(reinfo1[1]*1000)+"\t"+str(reinfo1[2]*1000))+"\n")
			dataFile.write("second reinforcement center coordination\t=\t"+(str(reinfo2[0]*1000)+"\t"+str(reinfo2[1]*1000)+"\t"+str(reinfo2[2]*1000))+"\n")
			dataFile.close()
			#end
			closeProject(  )