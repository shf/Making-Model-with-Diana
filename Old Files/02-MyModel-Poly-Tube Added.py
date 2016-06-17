import math
newProject( "Model the structure/My Model/Model1", 10 )
setModelAnalysisAspects( [ "STRUCT" ] )
setModelDimension( "3D" )
setDefaultMeshOrder( "LINEAR" )
setDefaultMesherType( "TETTRIA" )
#importing variables
xLength = 0.7
yLength = 0.15
zLength = 0.15
xPlateLength = 0.04
zPlateLength = 0.02
xWoodenPlateLength = xPlateLength
zWoodenPlateLength = 0.005
xDisBottomPlate = 0.07
xMidDisPlate = 0.04
embeddmentLength = 0.1
reinfo1 = [0, 0.03, 0.02]
reinfo2 = [0, 0.075, 0.02]
r = 0.008
rBig = 2 * r
#end
point = [[0]*3 for i in range(8)]
pointBig = [[0]*3 for i in range(8)]
midPoint = [[0]*3 for i in range(8)]
xAxis = [[0]*3 for i in range(8)]
for i in range(0, 8):
	point[i] = [x * r for x in [0, -math.sin(math.radians(i*45)), math.cos(math.radians(i*45))]]
	midPoint[i] = [x * r for x in [xLength/4., -math.sin(math.radians(i*45+45/2.)), math.cos(math.radians(i*45+45/2.))]]
	xAxis[i] = [0.0, -math.cos(math.radians(i*45+45/2.)), -math.sin(math.radians(i*45+45/2.))]
	pointBig[i] = [x + y for x, y in zip([embeddmentLength, 0, 0], [x * rBig for x in [0, -math.sin(math.radians(i*45)), math.cos(math.radians(i*45))]])]
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
createSheet( "Poly2", [[x + y for x, y in zip(reinfo2, point[0])],[x + y for x, y in zip(reinfo2, point[1])],[x + y for x, y in zip(reinfo2, point[2])],[x + y for x, y in zip(reinfo2, point[3])],[x + y for x, y in zip(reinfo2, point[4])],[x + y for x, y in zip(reinfo2, point[5])],[x + y for x, y in zip(reinfo2, point[6])],[x + y for x, y in zip(reinfo2, point[7])]] )
extrudeProfile( "Poly1", [ embeddmentLength, 0, 0 ] )
extrudeProfile( "Poly2", [ embeddmentLength, 0, 0 ] )
subtract( "Concrete-Block", [ "Poly1", "Poly2" ], False, True )
createSheet( "Poly1-Big", [[x + y for x, y in zip(reinfo1, pointBig[0])],[x + y for x, y in zip(reinfo1, pointBig[1])],[x + y for x, y in zip(reinfo1, pointBig[2])],[x + y for x, y in zip(reinfo1, pointBig[3])],[x + y for x, y in zip(reinfo1, pointBig[4])],[x + y for x, y in zip(reinfo1, pointBig[5])],[x + y for x, y in zip(reinfo1, pointBig[6])],[x + y for x, y in zip(reinfo1, pointBig[7])]] )
createSheet( "Poly2-Big", [[x + y for x, y in zip(reinfo2, pointBig[0])],[x + y for x, y in zip(reinfo2, pointBig[1])],[x + y for x, y in zip(reinfo2, pointBig[2])],[x + y for x, y in zip(reinfo2, pointBig[3])],[x + y for x, y in zip(reinfo2, pointBig[4])],[x + y for x, y in zip(reinfo2, pointBig[5])],[x + y for x, y in zip(reinfo2, pointBig[6])],[x + y for x, y in zip(reinfo2, pointBig[7])]] )
extrudeProfile( "Poly1-Big", [ xLength/2, 0, 0 ] )
extrudeProfile( "Poly2-Big", [ xLength/2, 0, 0 ] )
subtract( "Concrete-Block", [ "Poly1-Big", "Poly2-Big" ], False, True )
#end

# Create reinforcement cylinders
createSheet( "Reinforcement1", [[x + y for x, y in zip(reinfo1, point[0])],[x + y for x, y in zip(reinfo1, point[1])],[x + y for x, y in zip(reinfo1, point[2])],[x + y for x, y in zip(reinfo1, point[3])],[x + y for x, y in zip(reinfo1, point[4])],[x + y for x, y in zip(reinfo1, point[5])],[x + y for x, y in zip(reinfo1, point[6])],[x + y for x, y in zip(reinfo1, point[7])]] )
createSheet( "Reinforcement2", [[x + y for x, y in zip(reinfo2, point[0])],[x + y for x, y in zip(reinfo2, point[1])],[x + y for x, y in zip(reinfo2, point[2])],[x + y for x, y in zip(reinfo2, point[3])],[x + y for x, y in zip(reinfo2, point[4])]] )
extrudeProfile( "Reinforcement1", [ xLength/2, 0, 0 ] )
extrudeProfile( "Reinforcement2", [ xLength/2, 0, 0 ] )
#end

#add concrete material
addMaterial( "Concrete", "CONCR", "TSCR", [] )
setParameter( "MATERIAL", "Concrete", "LINEAR/ELASTI/YOUNG", 20000 )
setParameter( "MATERIAL", "Concrete", "LINEAR/ELASTI/YOUNG", 20000 )
setParameter( "MATERIAL", "Concrete", "LINEAR/ELASTI/POISON", 0.2 )
setParameter( "MATERIAL", "Concrete", "LINEAR/MASS/DENSIT", 3400 )
setParameter( "MATERIAL", "Concrete", "MODTYP/TOTCRK", "ROTATE" )
setParameter( "MATERIAL", "Concrete", "TENSIL/TENSTR", 3.7e+08 )
setParameter( "MATERIAL", "Concrete", "LINEAR/ELASTI/YOUNG", 2e+10 )
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
setParameter( "MATERIAL", "LoadPlate", "LINEAR/ELASTI/YOUNG", 2.1e+11 )
setParameter( "MATERIAL", "LoadPlate", "LINEAR/ELASTI/POISON", 0.3 )
setParameter( "MATERIAL", "LoadPlate", "LINEAR/ELASTI/POISON", 0.3 )
setParameter( "MATERIAL", "LoadPlate", "TREPLA/YLDSTR", 5.9e+08 )
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
#add reinforcement material
addMaterial( "Reinforcement", "MCSTEL", "TRESCA", [] )
setParameter( "MATERIAL", "Reinforcement", "LINEAR/ELASTI/YOUNG", 2.4e+11 )
setParameter( "MATERIAL", "Reinforcement", "LINEAR/ELASTI/YOUNG", 2.4e+11 )
setParameter( "MATERIAL", "Reinforcement", "LINEAR/ELASTI/POISON", 0.3 )
setParameter( "MATERIAL", "Reinforcement", "LINEAR/ELASTI/POISON", 0.3 )
setParameter( "MATERIAL", "Reinforcement", "TREPLA/YLDSTR", 6.9e+08 )
addGeometry( "Element geometry 3", "SOLID", "STRSOL", [] )
rename( "GEOMET", "Element geometry 3", "Reinforcement-Geometry" )
addElementData( "Reinforcement-Data" )
clearReinforcementAspects( [ "Reinforcement1", "Reinforcement2" ] )
setElementClassType( [ "Reinforcement1", "Reinforcement2" ], "STRSOL" )
assignMaterial( "Reinforcement", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
assignGeometry( "Reinforcement-Geometry", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
assignElementData( "Reinforcement-Data", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
#end


#define interface material and make interface elements
addMaterial( "Bond", "INTERF", "ELASTI", [] )
setParameter( "MATERIAL", "Bond", "LINEAR/ELAS6/DSNZ", 1.0e13 )
setParameter( "MATERIAL", "Bond", "LINEAR/ELAS6/DSSX", 1.0e13 )
setParameter( "MATERIAL", "Bond", "LINEAR/ELAS6/DSSY", 1.0e13 )
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
for i in range(8, 12):
	addGeometry( "Int"+str(i), "SHEET", "STRINT", [] )
	setParameter( "GEOMET", "Int"+str(i), "LOCAXS", True )
	setParameter( "GEOMET", "Int"+str(i), "LOCAXS/XAXIS", xAxis[i - 8] )
	setInterfaceContactAspects( "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]], "Bond" )
	setElementClassType( "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]], "STRINT" )
	assignGeometry( "Int"+str(i), "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]] )
	resetElementData( "SHAPEFACE", "Reinforcement2", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]] )
	addElementData( "Int"+str(i) )
	assignElementData( "Int"+str(i), "SHAPEFACE", "Reinforcement1", [[x + y for x, y in zip(reinfo2, midPoint[i - 8])]] )
#end
#add support mirror about x axis
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 1" )
createSurfaceSupport( "ReflectX", "Geometry support set 1" )
setParameter( "GEOMETRYSUPPORT", "ReflectX", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectX", "TRANSL", [ 1, 0, 0 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectX", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "ReflectX", "Concrete-Block", [[ xLength/2., 0, 0 ]] )
attach( "GEOMETRYSUPPORT", "ReflectX", "Reinforcement1", [[ xLength/2., reinfo1[1], reinfo1[2] ]] )
attach( "GEOMETRYSUPPORT", "ReflectX", "Reinforcement2", [[ xLength/2., reinfo2[1]-r/2., reinfo2[2] ]] )
#end
#add support mirror about y axis
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 2" )
createSurfaceSupport( "ReflectY", "Geometry support set 2" )
setParameter( "GEOMETRYSUPPORT", "ReflectY", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectY", "TRANSL", [ 0, 1, 0 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectY", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Concrete-Block", [[ xLength/4., yLength/2., zLength/2. ], [ xLength/4., yLength/2., 0.0 ]] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Load-Block1", [[ xDisBottomPlate + xPlateLength/2., yLength/2., -zPlateLength/2. ]] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Load-Block2", [[ xLength/2. - xMidDisPlate - xPlateLength/2., yLength/2., zLength+zPlateLength/2. ]] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Reinforcement2", [[ 0, yLength/2., reinfo2[2] ]] )
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
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 7" )
createSurfaceSupport( "reinforcement2_debond", "Geometry support set 7" )
setParameter( "GEOMETRYSUPPORT", "reinforcement2_debond", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "reinforcement2_debond", "TRANSL", [ 1, 0, 0 ] )
setParameter( "GEOMETRYSUPPORT", "reinforcement2_debond", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "reinforcement2_debond", "Reinforcement2", [[ xLength/2., reinfo2[1]-r/2., reinfo2[2] ]] )
#end
#surface reinforcement 1 displacement for bond slip curve
#createVertex( "Vertex-reinfo1", [ reinfo1[0], reinfo1[1], reinfo1[2] ] )
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 8" )
createSurfaceSupport( "reinforcement1_center", "Geometry support set 8" )
setParameter( "GEOMETRYSUPPORT", "reinforcement1_center", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "reinforcement1_center", "TRANSL", [ 1, 0, 0 ] )
setParameter( "GEOMETRYSUPPORT", "reinforcement1_center", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "reinforcement1_center", "Reinforcement1", [[ reinfo1[0], reinfo1[1], reinfo1[2] ]] )
#end
#surface  reinforcement 2 displacement for bond slip curve
#createVertex( "Vertex-reinfo2", [ reinfo2[0], reinfo2[1], reinfo2[2] ] )
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 9" )
createSurfaceSupport( "reinforcement2_center", "Geometry support set 9" )
setParameter( "GEOMETRYSUPPORT", "reinforcement2_center", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "reinforcement2_center", "TRANSL", [ 1, 0, 0 ] )
setParameter( "GEOMETRYSUPPORT", "reinforcement2_center", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "reinforcement2_center", "Reinforcement2", [[ reinfo2[0], reinfo2[1], reinfo2[2] ]] )
#end
#three different points on concrete for bond slip curve
#createVertex( "Vertex-concreteMiddle", [ 0, yLength/2, zLength/2 ] )
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 10" )
createPointSupport( "concretePoints", "Geometry support set 10" )
setParameter( "GEOMETRYSUPPORT", "concretePoints", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "concretePoints", "TRANSL", [ 1, 0, 0 ] )
setParameter( "GEOMETRYSUPPORT", "concretePoints", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "concretePoints", "Concrete-Block", [[ 0, yLength/2, 0 ],  [ 0, yLength/2, zLength ]])
#end
#end

#hide supports
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 1" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 2" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 3" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 4" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 5" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 6" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 7" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 8" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 9" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 10" ] )

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
setElementSize( [ "Concrete-Block", "Load-Block1", "Load-Block2", "Reinforcement1", "Reinforcement2" ], 0.01 )
setMesherType( [ "Concrete-Block", "Load-Block1", "Load-Block2", "Reinforcement1", "Reinforcement2" ], "TETTRIA" )
#generateMesh( [] )
#end
#exportModel( "C:/Users/ShayanFa/Documents/Model the structure/My Model/GeneratedModel/Model-xDisBottomPlate"+str(xDisBottomPlate*1000)+"-xMidDisPlate"+str(xMidDisPlate*1000)+".dat", 5 )
#closeProject(  )
'''