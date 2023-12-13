//Maya ASCII 2018ff09 scene
//Name: joints.ma
//Last modified: Wed, Dec 01, 2021 10:13:32 AM
//Codeset: 932
requires maya "2018ff09";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntscf;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811122215-49253d42f6";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode joint -n "root_jnt";
	rename -uid "9735C04F-4B49-2E49-69B0-098D272EEE56";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode joint -n "cog_jnt" -p "root_jnt";
	rename -uid "C0F94642-408C-C8B8-9CAC-FEA215AA16FA";
	addAttr -is true -ci true -k true -sn "TypeID" -ln "TypeID" -dt "string";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineA";
createNode joint -n "spine_01_jnt" -p "cog_jnt";
	rename -uid "0367411B-4671-120F-089A-1E953D2F11AE";
	addAttr -is true -ci true -k true -sn "TypeID" -ln "TypeID" -dt "string";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 2.6953385274149003e-17 0.1 0 ;
	setAttr ".jo" -type "double3" 0 0 90.000000000000028 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 2.6953385274149003e-17 0.10000000000000001 0 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineA";
createNode joint -n "spine_02_jnt" -p "spine_01_jnt";
	rename -uid "1B697596-4D9C-A13F-B103-CDA4434FBA73";
	addAttr -is true -ci true -k true -sn "TypeID" -ln "TypeID" -dt "string";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 2.8 6.4440145769070092e-15 0 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -7.6605109792130356e-15 2.8999999999999999 0 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineB";
createNode joint -n "neck_jnt" -p "spine_02_jnt";
	rename -uid "71AD06B7-4547-3AE9-4DC3-02AB4A751088";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 6.6 2.3852089908349331e-09 0 ;
	setAttr ".pa" -type "double3" 1.4433913741954447e-29 0 6.5048988568370912e-29 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -2.3852195823346974e-09 9.5 0 1;
createNode joint -n "head_jnt" -p "neck_jnt";
	rename -uid "A27CCBF4-4174-C59C-824D-ABB5EF2A2B68";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 1.8000000000000007 8.2210266616426009e-16 0 ;
	setAttr ".pa" -type "double3" 1.4433913741954447e-29 0 6.5048988568370912e-29 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -2.3852212037979412e-09 11.300000000000001 0 1;
createNode joint -n "shoulderR_jnt" -p "spine_01_jnt";
	rename -uid "FA80BA2F-4E73-4165-0F31-5BA5CFAC4777";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.30000000000000004 6.2999999999999989 -0.49999999999999989 ;
	setAttr ".r" -type "double3" 3.0963041485194764e-15 -7.016671689544605e-15 2.88375572455273e-20 ;
	setAttr ".jo" -type "double3" 0.00047095700986203782 -4.8531412986198681e-20 89.999999999999972 ;
	setAttr ".bps" -type "matrix" -1 1.1102230246251565e-16 8.4703294725430034e-22 0
		 -1.1102230247751791e-16 -0.99999999996621791 8.2197504573474053e-06 0 5.8486225050340167e-22 8.2197504573474053e-06 0.9999999999662178 0
		 -6.2999999999999998 0.39999999999999725 -0.5 1;
createNode joint -n "armR_jnt" -p "shoulderR_jnt";
	rename -uid "76E44F93-4776-521D-F96D-B6AAE94B0A19";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 0 -5.5511151231257827e-17 5.5511151231257827e-17 ;
	setAttr ".r" -type "double3" 7.0167687523705791e-15 -7.0168094149092666e-15 -1.2179928716837684e-14 ;
	setAttr ".bps" -type "matrix" -1 1.1102230246251565e-16 8.4703294725430034e-22 0
		 -1.1102230247751791e-16 -0.99999999996621791 8.2197504573474053e-06 0 5.8486225050340167e-22 8.2197504573474053e-06 0.9999999999662178 0
		 -6.2999999999999998 0.39999999999999725 -0.5 1;
createNode joint -n "forearmR_jnt" -p "armR_jnt";
	rename -uid "567A97E4-4C72-128F-6FBE-EB8707080C2A";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 6 -5.5511151231257827e-17 1.1102230246251565e-16 ;
	setAttr ".r" -type "double3" -2.3976265146049651e-14 -3.9149630896122239e-20 -4.8789600103285258e-15 ;
	setAttr ".bps" -type "matrix" -1 1.1102230246251565e-16 8.4703294725430034e-22 0
		 -1.1102230247751791e-16 -0.99999999996621791 8.2197504573474053e-06 0 5.8486225050340167e-22 8.2197504573474053e-06 0.9999999999662178 0
		 -12.300000000000001 0.39999999999999791 -0.5 1;
createNode joint -n "handR_jnt" -p "forearmR_jnt";
	rename -uid "A3C95E6C-493C-8203-A058-719FF30BAF0F";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 3.2000000000000046 -1.1102230246251565e-16 -1.6653345369377348e-16 ;
	setAttr ".r" -type "double3" -1.1460207862560956e-15 2.6988859645173072e-19 2.3766803567601224e-15 ;
	setAttr ".bps" -type "matrix" -1 1.1102230246251565e-16 8.4703294725430034e-22 0
		 -1.1102230247751791e-16 -0.99999999996621791 8.2197504573474053e-06 0 5.8486225050340167e-22 8.2197504573474053e-06 0.9999999999662178 0
		 -15.5 0.3999999999999983 -0.5 1;
createNode joint -n "shoulderL_jnt" -p "spine_01_jnt";
	rename -uid "DEAD3AB7-441D-DEA4-5DAF-34B4DA58FBF7";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.30000000000000004 -6.2999999999999989 -0.5 ;
	setAttr ".r" -type "double3" 0 0 -3.1805546814635168e-14 ;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".bps" -type "matrix" 1 6.6613381477509392e-16 0 0 -6.6613381477509392e-16 1 0 0
		 0 0 1 0 6.2999999999999998 0.4000000000000028 -0.5 1;
createNode joint -n "armL_jnt" -p "shoulderL_jnt";
	rename -uid "2F7D0130-4BEB-C4F7-3820-BEB2905DA070";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -8.8817841970012523e-16 1.7763568394002505e-15 5.5511151231257827e-17 ;
	setAttr ".jo" -type "double3" 1.7075472925031869e-06 0 0 ;
	setAttr ".bps" -type "matrix" 1 6.6613381477509392e-16 0 0 -6.6613381477509363e-16 0.99999999999999956 2.9802322387695296e-08 0
		 1.9852334701272652e-23 -2.9802322387695296e-08 0.99999999999999956 0 6.2999999999999998 0.40000000000000457 -0.49999999999999994 1;
createNode joint -n "forearmL_jnt" -p "armL_jnt";
	rename -uid "B5BF5358-4965-039E-EC28-F4807D6BC1E2";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 6.0000000000000009 -5.5511151231257827e-17 1.1102230246251565e-16 ;
	setAttr ".r" -type "double3" -3.2324078448137451e-52 -7.5830332790935298e-22 4.8846766289002763e-29 ;
	setAttr ".jo" -type "double3" 2.2588727439225557e-06 0 0 ;
	setAttr ".bps" -type "matrix" 1 6.6613381477509392e-16 0 0 -6.6613381477509235e-16 0.99999999999999756 6.9227089152702524e-08 0
		 4.6114504983065266e-23 -6.9227089152702524e-08 0.99999999999999756 0 12.300000000000001 0.40000000000000857 -0.49999999999999994 1;
createNode joint -n "handL_jnt" -p "forearmL_jnt";
	rename -uid "B996D686-49F7-4008-90DB-B1AD0AA16D25";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 3.1999999999999993 -7.7715611723760958e-16 0 ;
	setAttr ".r" -type "double3" 6.1039369283490625e-22 -1.803209861856655e-21 2.9842778343338019e-13 ;
	setAttr ".bps" -type "matrix" 1 6.6613381477509392e-16 0 0 -6.6613381477509235e-16 0.99999999999999756 6.9227089152702524e-08 0
		 4.6114504983065266e-23 -6.9227089152702524e-08 0.99999999999999756 0 15.5 0.40000000000001001 -0.49999999999999994 1;
createNode transform -s -n "persp";
	rename -uid "1E7E515E-40B8-E0D0-1EE8-948F8FA0462B";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 107.28612057144394 53.922828120062476 168.61964536524064 ;
	setAttr ".r" -type "double3" -13.538352729600554 33.000000000000668 9.4809416325866393e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "6442D97D-4D3C-A5AC-A808-9484BE54D707";
	setAttr ".ihi" 0;
	setAttr -k off ".v" no;
	setAttr ".fl" 100;
	setAttr ".coi" 206.39189483923872;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "06FFA5AC-4A80-854C-3DC9-1B937E5E871C";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "C55A50C4-4436-8778-8A8D-FCAD3DEFB607";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "BE36C6AA-4803-BDD0-E3C6-BA93A77D9741";
createNode displayLayerManager -n "layerManager";
	rename -uid "0C4E2ED3-4BC6-4829-492B-13A8C74883D2";
createNode displayLayer -n "defaultLayer";
	rename -uid "8A643760-456C-78EF-8B6D-E8A45C154706";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "1EE4179C-42FF-F6E4-8658-53B84A319544";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "12FB2694-403A-E3C9-9FB1-16AA499A89D3";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "CFE1EBBB-4B84-4F9B-A615-3AB6542C972E";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".fs" 1;
	setAttr ".ef" 10;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "root_jnt.s" "cog_jnt.is";
connectAttr "cog_jnt.s" "spine_01_jnt.is";
connectAttr "spine_01_jnt.s" "spine_02_jnt.is";
connectAttr "spine_02_jnt.s" "neck_jnt.is";
connectAttr "neck_jnt.s" "head_jnt.is";
connectAttr "spine_01_jnt.s" "shoulderR_jnt.is";
connectAttr "shoulderR_jnt.s" "armR_jnt.is";
connectAttr "armR_jnt.s" "forearmR_jnt.is";
connectAttr "forearmR_jnt.s" "handR_jnt.is";
connectAttr "spine_01_jnt.s" "shoulderL_jnt.is";
connectAttr "shoulderL_jnt.s" "armL_jnt.is";
connectAttr "armL_jnt.s" "forearmL_jnt.is";
connectAttr "forearmL_jnt.s" "handL_jnt.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of joints.ma
