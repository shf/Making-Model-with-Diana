newProject( "Model the structure/My Model/Model1", 10 )
setModelAnalysisAspects( [ "STRUCT" ] )
setModelDimension( "3D" )
setDefaultMeshOrder( "LINEAR" )
setDefaultMesherType( "TETTRIA" )
#defining variables
#end
#create block of concrete and load blocks
createBlock( "Concrete-Block", [ 0, 0, 0 ], [ 0.35, 0.075, 0.15 ] )
createBlock( "Load-Block1", [ 0.08, 0, -0.02 ], [ 0.04, 0.075, 0.02 ] )
createBlock( "Load-Block2", [ 0.27, 0, 0.15 ], [ 0.04, 0.075, 0.02 ] )
setViewPoint( "ISO1" )
#end
# Subtract two cylinders from geometry
createCylinder( "Reinforcement1", [ 0, 0.03, 0.02 ], [ 1, 0, 0 ], 0.008, 0.35 )
createCylinder( "Reinforcement2", [ 0, 0.075, 0.02 ], [ 1, 0, 0 ], 0.008, 0.35 )
subtract( "Concrete-Block", [ "Reinforcement2", "Reinforcement1" ], False, True )
#end
# Create reinforcement cylinders
createCylinder( "Reinforcement1", [ 0, 0.03, 0.02 ], [ 1, 0, 0 ], 0.008, 0.35 )
createSheetCircle( "Reinforcement2", [ 0, 0.075, 0.02 ], [ 1, 0, 0 ], 0.008 )
createSheet( "Sheet 1", [[ 0, 0.075, 0 ],[ 0, 0.075, 0.04 ],[ 0, 0.1, 0.04 ],[ 0, 0.1, 0 ]] )
subtract( "Reinforcement2", [ "Sheet 1" ], False, True )
extrudeProfile( "Reinforcement2", [ 0.35, 0, 0 ] )
#end
#make interface elements
createSheetFromFaces( "Interface1", "Concrete-Block", [[ 0.200751, 0.0228397, 0.0164321 ]] )
setInterfaceContactAspects( "SHAPEFACE", "Interface1", [[ 0.200751, 0.0228397, 0.0164321 ]], "" )
createSheetFromFaces( "Interface2", "Concrete-Block", [[ 0.200751, 0.0672127, 0.0181673 ]] )
setInterfaceContactAspects( "SHAPEFACE", "Interface2", [[ 0.200751, 0.0672127, 0.0181673 ]], "" )
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
rename( "GEOMET", "Element geometry 1", "ConcreteGeometry" )
addElementData( "Concrete-Data" )
clearReinforcementAspects( [ "Concrete-Block" ] )
setElementClassType( [ "Concrete-Block" ], "STRSOL" )
assignMaterial( "Concrete", "SHAPE", [ "Concrete-Block" ] )
assignGeometry( "ConcreteGeometry", "SHAPE", [ "Concrete-Block" ] )
assignElementData( "Concrete-Data", "SHAPE", [ "Concrete-Block" ] )
#end
#add LoadPlate material
addMaterial( "LoadPlate", "REINFO", "VMISES", [] )
setParameter( "MATERIAL", "LoadPlate", "LINEAR/ELASTI/YOUNG", 2.1e+11 )
setParameter( "MATERIAL", "LoadPlate", "PLASTI/HARDI1/YLDSTR", 5.9e+08 )
addGeometry( "Element geometry 2", "SOLID", "STRSOL", [] )
rename( "GEOMET", "Element geometry 2", "Concrete-Geometry" )
addElementData( "LoadPlate-Data" )
clearReinforcementAspects( [ "Load-Block2", "Load-Block1" ] )
setElementClassType( [ "Load-Block2", "Load-Block1" ], "STRSOL" )
assignMaterial( "LoadPlate", "SHAPE", [ "Load-Block2", "Load-Block1" ] )
assignGeometry( "LoadPlate-Geometry", "SHAPE", [ "Load-Block2", "Load-Block1" ] )
assignElementData( "LoadPlate-Data", "SHAPE", [ "Load-Block2", "Load-Block1" ] )
#end

#add Steel material
addMaterial( "Steel", "REINFO", "VMISES", [] )
setParameter( "MATERIAL", "Steel", "LINEAR/ELASTI/YOUNG", 2.4e+11 )
setParameter( "MATERIAL", "Steel", "PLASTI/HARDI1/YLDSTR", 5.9e+08 )
addGeometry( "Element geometry 3", "SOLID", "STRSOL", [] )
rename( "GEOMET", "Element geometry 3", "Steel-Geometry" )
addElementData( "Steel-Data" )
clearReinforcementAspects( [ "Reinforcement1", "Reinforcement2" ] )
setElementClassType( [ "Reinforcement1", "Reinforcement2" ], "STRSOL" )
assignMaterial( "Steel", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
assignGeometry( "Steel-Geometry", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
assignElementData( "Steel-Data", "SHAPE", [ "Reinforcement1", "Reinforcement2" ] )
#end

#add total interface material
addMaterial( "Interface", "INTERF", "ELASTI", [] )
setParameter( "MATERIAL", "Interface", "LINEAR/ELAS6/DSNZ", 3.8e+11 )
setParameter( "MATERIAL", "Interface", "LINEAR/ELAS6/DSSX", 3.8e+11 )
setParameter( "MATERIAL", "Interface", "LINEAR/ELAS6/DSSY", 3.8e+11 )
addGeometry( "Element geometry 4", "SHEET", "MEM3D", [] )
rename( "GEOMET", "Element geometry 4", "Interface-Geometry" )
addElementData( "Interface-Geometry" )
clearReinforcementAspects( [ "Interface1" ] )
setElementClassType( [ "Interface1" ], "MEM3D" )
assignMaterial( "Interface", "SHAPE", [ "Interface1" ] )
assignGeometry( "Interface-Geometry", "SHAPE", [ "Interface1" ] )
assignElementData( "Interface-Geometry", "SHAPE", [ "Interface1" ] )
clearReinforcementAspects( [ "Interface2" ] )
setElementClassType( [ "Interface2" ], "MEM3D" )
assignMaterial( "Interface", "SHAPE", [ "Interface2" ] )
assignGeometry( "Interface-Geometry", "SHAPE", [ "Interface2" ] )
assignElementData( "Interface-Geometry", "SHAPE", [ "Interface2" ] )
#end
#add support mirror about x axis
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 1" )
createSurfaceSupport( "ReflectX", "Geometry support set 1" )
setParameter( "GEOMETRYSUPPORT", "ReflectX", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectX", "TRANSL", [ 1, 0, 0 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectX", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "ReflectX", "Concrete-Block", [[ 0.35, 0.0131002, 0.0284209 ]] )
attach( "GEOMETRYSUPPORT", "ReflectX", "Reinforcement1", [[ 0.35, 0.0310536, 0.019475 ]] )
attach( "GEOMETRYSUPPORT", "ReflectX", "Reinforcement2", [[ 0.35, 0.0705334, 0.0189488 ]] )
#end
#add support mirror about y axis
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 2" )
createSurfaceSupport( "ReflectY", "Geometry support set 2" )
setParameter( "GEOMETRYSUPPORT", "ReflectY", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectY", "TRANSL", [ 0, 1, 0 ] )
setParameter( "GEOMETRYSUPPORT", "ReflectY", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Concrete-Block", [[ 0.200751, 0.075, 0.0979759 ],[ 0.200751, 0.075, 0.00688288 ]] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Load-Block1", [[ 0.102943, 0.075, -0.00852854 ]] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Load-Block2", [[ 0.292943, 0.075, 0.161471 ]] )
attach( "GEOMETRYSUPPORT", "ReflectY", "Reinforcement2", [[ 0.200751, 0.075, 0.0188228 ]] )
#end
#add bottom support
addSet( "GEOMETRYSUPPORTSET", "Geometry support set 3" )
createSurfaceSupport( "Support-Bottom", "Geometry support set 3" )
setParameter( "GEOMETRYSUPPORT", "Support-Bottom", "AXES", [ 1, 2 ] )
setParameter( "GEOMETRYSUPPORT", "Support-Bottom", "TRANSL", [ 0, 0, 1 ] )
setParameter( "GEOMETRYSUPPORT", "Support-Bottom", "ROTATI", [ 0, 0, 0 ] )
attach( "GEOMETRYSUPPORT", "Support-Bottom", "Load-Block1", [[ 0.0970571, 0.043018, -0.02 ]] )
#end
#hide supports
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 1" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 2" ] )
hide( "GEOMETRYSUPPORTSET", [ "Geometry support set 3" ] )
#end
#add dead load - Weight
addSet( "GEOMETRYLOADSET", "Geometry load set 1" )
createModelLoad( "Weight-Load", "Geometry load set 1" )
#end
#add pressure load

#end
#Generate Mesh
'''
addSet( "ELEMENTSET", "Element set 1" )
setElementSize( [ "Concrete-Block", "Load-Block1", "Load-Block2", "Reinforcement1", "Reinforcement2", "Interface1", "Interface2" ], 0.006 )
setMesherType( [ "Concrete-Block", "Load-Block1", "Load-Block2", "Reinforcement1", "Reinforcement2", "Interface1", "Interface2" ], "TETTRIA" )
generateMesh( [] )
#end'''