//Maya ASCII 2018ff09 scene
//Name: char_000.ma
//Last modified: Wed, Jan 22, 2020 05:40:45 PM
//Codeset: 932
requires maya "2018ff09";
requires -dataType "HIKCharacter" -dataType "HIKCharacterState" -dataType "HIKEffectorState"
		 -dataType "HIKPropertySetState" "mayaHIK" "1.0_HIK_2016.5";
requires "stereoCamera" "10.0";
requires "mtoa" "3.1.1.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t 59.94fps;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811122215-49253d42f6";
fileInfo "osv" "Microsoft Windows 8 , 64-bit  (Build 9200)\n";
createNode joint -n "root_jnt";
	rename -uid "1CF21616-4FC0-CE2F-103C-A98BFA947BC5";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root_jnt";
	setAttr ".mocapJnt" -type "string" "Character1_Reference";
	setAttr ".init_scale" -type "float3" 1 1 1 ;
createNode joint -n "pelvis_C_body_jnt" -p "root_jnt";
	rename -uid "B362CAC8-4F73-6E2A-35C8-D69AA557FCF0";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 100.69000244140625 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 100.69000244140625 0 1;
	setAttr ".typ" 1;
	setAttr ".otp" -type "string" "pelvis_C";
	setAttr ".mocapJnt" -type "string" "Character1_Hips";
	setAttr ".init_translate" -type "float3" 0 102.00221 -1.5644366 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 0 102.00221 -1.5644366 ;
createNode joint -n "spine_C_01_body_jnt" -p "pelvis_C_body_jnt";
	rename -uid "99404157-4DC0-5EEF-3D75-53BF7C5795E7";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 1.079742431640625 0.001738429069519043 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999936776205633 0.0011244889895439378 0
		 0 -0.0011244889895439378 0.99999936776205633 0 -1.0947644252537633e-47 101.76974567370358 0.001738429069519043 1;
	setAttr ".typ" 6;
	setAttr ".otp" -type "string" "spine_C_01";
	setAttr ".mocapJnt" -type "string" "Character1_Spine";
	setAttr ".init_translate" -type "float3" 0 1.0797433 0.0017384291 ;
	setAttr ".init_rotate" -type "float3" 0.064428486 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 0 103.08195 -1.5626981 ;
	setAttr ".init_worldRotate" -type "float3" 0.064428486 0 0 ;
createNode joint -n "spine_C_02_body_jnt" -p "spine_C_01_body_jnt";
	rename -uid "71926C28-4932-EC68-F395-9A9534E33516";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 2.1735903041905733e-16 12.542381286621094 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99819510651637833 -0.060054386407292139 0
		 0 0.060054386407292139 0.99819510651637833 0 2.1735903242712993e-16 114.31211955976414 0.015842199325561544 1;
	setAttr ".typ" 6;
	setAttr ".otp" -type "string" "spine_C_02";
	setAttr ".mocapJnt" -type "string" "Character1_Spine1";
	setAttr ".init_translate" -type "float3" 2.1735903e-16 12.542382 1.4852564e-12 ;
	setAttr ".init_rotate" -type "float3" -3.5073631 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 2.1735903e-16 115.62433 -1.5485944 ;
	setAttr ".init_worldRotate" -type "float3" -3.4429345 0 0 ;
createNode joint -n "spine_C_03_body_jnt" -p "spine_C_02_body_jnt";
	rename -uid "56891205-42E7-E319-B45E-4BADDBC55E4D";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.3471806083811466e-16 14.07253265380858 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99923594957621453 -0.039083462928978699 0
		 0 0.039083462928978699 0.99923594957621453 0 6.52077091257172e-16 128.35924789153918 -0.82927481962407634 1;
	setAttr ".typ" 6;
	setAttr ".otp" -type "string" "spine_C_03";
	setAttr ".mocapJnt" -type "string" "Character1_Spine2";
	setAttr ".init_translate" -type "float3" 4.3471806e-16 11.321802 -7.9936058e-15 ;
	setAttr ".init_rotate" -type "float3" 1.2030466 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.5207709e-16 126.9257 -2.2285182 ;
	setAttr ".init_worldRotate" -type "float3" -2.239888 0 0 ;
createNode joint -n "neck_C_body_jnt" -p "spine_C_03_body_jnt";
	rename -uid "49E0D180-4565-001A-E43A-6A9EE9ED0E24";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 22.249114990234375 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.96638275797497719 0.25710769161710517 0
		 0 -0.25710769161710517 0.96638275797497719 0 6.5207709728139862e-16 150.59136254249233 -1.6988472455979853 1;
	setAttr ".typ" 7;
	setAttr ".otp" -type "string" "neck_C";
	setAttr ".mocapJnt" -type "string" "Character1_Neck";
	setAttr ".init_translate" -type "float3" 5.0289883e-30 25.002708 1.2434498e-14 ;
	setAttr ".init_rotate" -type "float3" 17.138399 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.5207709e-16 151.9093 -3.2057106 ;
	setAttr ".init_worldRotate" -type "float3" 14.898512 0 0 ;
createNode joint -n "head_C_body_jnt" -p "neck_C_body_jnt";
	rename -uid "4D32915B-4242-840C-E915-0B905D702A31";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 14.324676513671875 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999999999999989 8.3266726846886741e-17 0
		 0 -8.3266726846886741e-17 0.99999999999999989 0 6.5207709728139853e-16 164.4344869321408 1.9841383284090472 1;
	setAttr ".typ" 8;
	setAttr ".otp" -type "string" "head_C";
	setAttr ".mocapJnt" -type "string" "Character1_Head";
	setAttr ".init_translate" -type "float3" -4.7331654e-30 14.32468 0 ;
	setAttr ".init_rotate" -type "float3" -14.898512 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.5207709e-16 165.75243 0.47727492 ;
	setAttr ".init_worldRotate" -type "float3" 9.5416644e-15 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" -14.898511752076436 0 0 ;
createNode joint -n "clavicle_L_body_jnt" -p "spine_C_03_body_jnt";
	rename -uid "3034A3DD-4C47-D8C3-95B9-70A8D2C904A2";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 5.3289742469787589 19.062042236328125 5.0667206048965454 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.85686433669142725 -0.24835706427695223 -0.45177680012379373 0
		 0.21969156543697393 0.96866855457567835 -0.11583111607904835 0 0.46638945590805575 -1.6167622796103842e-15 0.88457949072866693 0
		 5.3289742469787598 147.60475158691415 3.4885640144348113 1;
	setAttr ".sd" 1;
	setAttr ".typ" 9;
	setAttr ".otp" -type "string" "clavicle_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftShoulder";
	setAttr ".init_translate" -type "float3" 6.064528 18.063614 -0.51298386 ;
	setAttr ".init_rotate" -type "float3" 2.2398803 0.016070072 -0.054539811 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.064528 144.95546 -3.4470987 ;
	setAttr ".init_worldRotate" -type "float3" -6.6994298e-06 0.013926188 -0.055126213 ;
createNode joint -n "upperarm_L_body_jnt" -p "clavicle_L_body_jnt";
	rename -uid "99B81548-4D1E-6F65-690A-03B9F9FEC357";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 15.671838283538815 -8.5265128291212022e-14 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.13369198018584244 0.0027637933546295428 0.99101907947338796 0
		 18.757614135742177 143.71253967285151 -3.5916092395782289 1;
	setAttr ".sd" 1;
	setAttr ".typ" 10;
	setAttr ".otp" -type "string" "upperarm_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftArm";
	setAttr ".init_translate" -type "float3" 12.655739 -6.2527761e-13 -1.4566126e-13 ;
	setAttr ".init_rotate" -type "float3" 0.0097352574 5.6539955 -44.051323 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 18.720261 144.94328 -3.4501748 ;
	setAttr ".init_worldRotate" -type "float3" -1.8777435e-14 5.664 -44.10741 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 14.137106198994827 -14.461881788967142
		-31.323999999999995 ;
createNode joint -n "lowerarm_L_body_jnt" -p "upperarm_L_body_jnt";
	rename -uid "BFF967B0-42CC-6906-22E7-5BA8233F609C";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 28.080955505371097 8.5265128291212022e-14 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862928 -0.68834335387957801 0.017762289766140388 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.052335412259155029 0.080819700258297072 0.99535379673451951 0
		 38.825841573540828 124.25057798298377 -6.2446078337019078 1;
	setAttr ".sd" 1;
	setAttr ".typ" 11;
	setAttr ".otp" -type "string" "lowerarm_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftForeArm";
	setAttr ".init_translate" -type "float3" 28.080956 2.8421709e-14 -7.2072972e-08 ;
	setAttr ".init_rotate" -type "float3" 0 -6.4964375 -4.20577e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 38.784966 125.4942 -6.221611 ;
	setAttr ".init_worldRotate" -type "float3" -4.1513027e-07 -0.8324374 -44.107414 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 0 -6.4680651413785855 0 ;
createNode joint -n "hand_L_body_jnt" -p "lowerarm_L_body_jnt";
	rename -uid "AC160734-46F7-2278-6CDE-85A76368B8B8";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 28.45337295532228 0 1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" 6.1775313487003825 0.026074234210768422 -0.12288644018426982 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 59.459301721431203 104.66488940709087 -5.7392108195610598 1;
	setAttr ".sd" 1;
	setAttr ".typ" 12;
	setAttr ".otp" -type "string" "hand_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 6.1775312393756288 0.026074235480836087
		-0.12288644013913305 ;
createNode joint -n "thumb_L_01_body_jnt" -p "hand_L_body_jnt";
	rename -uid "045307CD-4E4D-CA50-032E-D5ABF37AA086";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 1.531403127308792 -1.2215928259968791 3.1211627518060574 ;
	setAttr ".r" -type "double3" 83.509490245240812 -41.676998508266372 -39.802996378764071 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.071007989733464019 -0.74024810751050851 0.66857355969341381 0
		 0.020605510320497171 0.67121103727808096 0.74097986233130153 0 -0.99726289329265849 -0.038839191072850637 0.062914536463066051 0
		 59.657170660413321 102.73225166102877 -2.6079360788153534 1;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
	setAttr ".otp" -type "string" "thumb";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandThumb2";
	setAttr ".init_translate" -type "float3" 1.3482351 0.00016244063 2.1316282e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -8.5725317 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.395477 103.6881 -2.791487 ;
	setAttr ".init_worldRotate" -type "float3" 80.166878 -29.830978 -83.507973 ;
createNode joint -n "thumb_L_02_body_jnt" -p "thumb_L_01_body_jnt";
	rename -uid "BDB8B8E6-4305-C4BA-868A-1C98C60A4308";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.2004884469249113 4.5202837029023613e-06 -4.9615398438618286e-06 ;
	setAttr ".r" -type "double3" 0 0 -25.226646132793515 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.055453813100315073 -0.95572003652030624 0.28900533975388742 0
		 0.048903949474364251 0.29170315224630561 0.9552579100407268 0 -0.99726289329265849 -0.038839191072850637 0.062914536463066051 0
		 59.884431274655867 100.36309235605243 -0.46817070293931762 1;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
	setAttr ".otp" -type "string" "thumb";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandThumb3";
	setAttr ".init_translate" -type "float3" 3.9279501 -7.1054274e-15 -1.4210855e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -10.634403 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.780746 100.30246 -0.83755553 ;
	setAttr ".init_worldRotate" -type "float3" 80.966629 -19.339319 -85.422035 ;
createNode joint -n "thumb_L_03_body_jnt" -p "thumb_L_02_body_jnt";
	rename -uid "935DC474-4BC7-E936-44CB-E0B43C8EC600";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.396447736761786 -3.4057761766348449e-07 6.368051998606461e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.055453813100315073 -0.95572003652030624 0.28900533975388742 0
		 0.048903949474364251 0.29170315224630561 0.9552579100407268 0 -0.99726289329265849 -0.038839191072850637 0.062914536463066051 0
		 60.072777213591287 97.117039874285155 0.51342062559215851 1;
	setAttr ".sd" 1;
	setAttr ".typ" 14;
	setAttr ".otp" -type "string" "thumb";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandThumb4";
	setAttr ".init_translate" -type "float3" 3.7845576 -2.1316282e-14 -1.4210855e-14 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 60.065765 96.742844 0.41574606 ;
	setAttr ".init_worldRotate" -type "float3" 80.966629 -19.339319 -85.422035 ;
createNode joint -n "index_L_01_body_jnt" -p "hand_L_body_jnt";
	rename -uid "D390BF1D-4BCA-96AA-117C-3790539477F4";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 9.0542522728597703 0.69449269112473644 2.4556676922899872 ;
	setAttr ".r" -type "double3" -3.8530005383132808 -12.470018145861461 1.6859898399810771 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72142439406672021 -0.65199486726647538 0.23334424506217641 0
		 0.67891855471834761 0.73231114940087705 -0.052820228344043499 0 -0.13644207453940277 0.19652753883702415 0.97095854019316696 0
		 66.43738980010464 98.927312566030707 -3.1164956729664812 1;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
	setAttr ".otp" -type "string" "index_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandIndex2";
	setAttr ".init_translate" -type "float3" 5.2504559 8.5265128e-14 1.7763568e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -3.295537 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.018509 99.773163 -3.1839013 ;
	setAttr ".init_worldRotate" -type "float3" 15.041655 -11.594504 -46.652084 ;
createNode joint -n "index_L_02_body_jnt" -p "index_L_01_body_jnt";
	rename -uid "3B811216-41B2-0590-BBC6-4B86FE617404";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.9455232916643013 6.5698462492491672e-06 -1.8867964968194428e-09 ;
	setAttr ".r" -type "double3" 0 0 -16.046379848140564 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.50565285054106246 -0.82901411676560011 0.23885306977941528 0
		 0.8518795425616712 0.52355756195667191 0.013737695691188531 0 -0.13644207453940277 0.19652753883702415 0.97095854019316696 0
		 69.283785751923418 96.354852352518364 -2.1958307772577155 1;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
	setAttr ".otp" -type "string" "index_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandIndex3";
	setAttr ".init_translate" -type "float3" 4.5327368 2.8421709e-14 3.5527137e-15 ;
	setAttr ".init_rotate" -type "float3" 0 0 -14.306174 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 69.066414 96.54422 -2.2728939 ;
	setAttr ".init_worldRotate" -type "float3" 17.374487 -7.5812063 -60.582386 ;
createNode joint -n "index_L_03_body_jnt" -p "index_L_02_body_jnt";
	rename -uid "D201E028-4311-0D27-5604-91ACDD86E940";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.0546364250782361 -1.4137034440864227e-06 1.5849028756065309e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.50565285054106246 -0.82901411676560011 0.23885306977941528 0
		 0.8518795425616712 0.52355756195667191 0.013737695691188531 0 -0.13644207453940277 0.19652753883702415 0.97095854019316696 0
		 70.828372752602789 93.82251336389092 -1.4662208358545343 1;
	setAttr ".sd" 1;
	setAttr ".typ" 19;
	setAttr ".otp" -type "string" "index_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandIndex4";
	setAttr ".init_translate" -type "float3" 2.9975078 5.6843419e-14 -2.1316282e-14 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 70.525833 93.956024 -1.8774289 ;
	setAttr ".init_worldRotate" -type "float3" 17.374487 -7.5812063 -60.582386 ;
createNode joint -n "middle_L_01_body_jnt" -p "hand_L_body_jnt";
	rename -uid "B0095ECC-43FA-EB65-5C8D-C688B7D2B487";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 9.2586007827101042 0.91952349165228497 0.02402531023549237 ;
	setAttr ".r" -type "double3" -6.3783474198181205 -1.1840000133123429 -3.1430182831810338 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.68416541573701162 -0.7283660540404342 0.037424259925475205 0
		 0.72791794070932081 0.67875614022875563 -0.097085393830709105 0 0.04531175899150186 0.093664259049700924 0.99457219500334237 0
		 66.793236250439378 98.942837579489705 -5.5410384250711591 1;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
	setAttr ".otp" -type "string" "middle_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandMiddle2";
	setAttr ".init_translate" -type "float3" 5.282619 -4.2632564e-14 5.3290705e-15 ;
	setAttr ".init_rotate" -type "float3" 0 0 -20.568357 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.486145 99.893684 -5.322289 ;
	setAttr ".init_worldRotate" -type "float3" 2.2241752 -0.36346188 -56.74411 ;
createNode joint -n "middle_L_02_body_jnt" -p "middle_L_01_body_jnt";
	rename -uid "82E60512-4CA4-8D42-9DF0-F5835C039382";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.9899563706009076 -2.3775108104473475e-06 -2.7979576966430386e-07 ;
	setAttr ".r" -type "double3" 0 0 -18.812612100600035 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".bps" -type "matrix" 0.41288142566018632 -0.90833677637193855 0.066732518572637484 0
		 0.90965695338512542 0.40761661799650173 -0.079830569903928492 0 0.04531175899150186 0.093664259049700924 0.99457219500334237 0
		 69.523028879277021 96.036686172708585 -5.3917171256684151 1;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
	setAttr ".otp" -type "string" "middle_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandMiddle3";
	setAttr ".init_translate" -type "float3" 4.6574678 5.6843419e-14 0 ;
	setAttr ".init_rotate" -type "float3" 0 0 1.1104718 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 69.040146 95.999046 -5.2927442 ;
	setAttr ".init_worldRotate" -type "float3" 2.2167192 -0.40648782 -55.634449 ;
createNode joint -n "middle_L_03_body_jnt" -p "middle_L_02_body_jnt";
	rename -uid "D64528BC-400C-A465-30A1-F7A1019210E8";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.2657926639850849 5.2394108251974103e-07 2.612537128854342e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.41288142566018632 -0.90833677637193855 0.066732518572637484 0
		 0.90965695338512542 0.40761661799650173 -0.079830569903928492 0 0.04531175899150186 0.093664259049700924 0.99457219500334237 0
		 70.871414114811017 93.070246362067991 -5.1737825391719054 1;
	setAttr ".sd" 1;
	setAttr ".typ" 20;
	setAttr ".otp" -type "string" "middle_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandMiddle4";
	setAttr ".init_translate" -type "float3" 2.9174213 -5.6843419e-14 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 70.686905 93.590912 -5.2720466 ;
	setAttr ".init_worldRotate" -type "float3" 2.2167192 -0.40648782 -55.634449 ;
createNode joint -n "aux_L_body_jnt" -p "hand_L_body_jnt";
	rename -uid "F13EF2C2-4522-6A64-1AB2-A291E1118C88";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.213300218241077 0.30676956594075477 -0.94151817157815909 ;
	setAttr ".r" -type "double3" -0.39331348559624429 13.95666129474931 4.4396542310618106 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.75725065286573834 -0.61380060827675564 -0.22320452955416908 0
		 0.6305641185977664 0.77612118738903058 0.004979440015051244 0 0.17017738119807557 -0.14451545164765708 0.97475891540608051 0
		 62.740371938620513 101.97762182943013 -6.6027118091125168 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "aux_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing1";
	setAttr ".init_translate" -type "float3" 3.8059859 0.26664668 -0.30540955 ;
	setAttr ".init_rotate" -type "float3" -6.114687 8.0901203 4.3293967 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 62.096798 103.26897 -6.4877815 ;
	setAttr ".init_worldRotate" -type "float3" -5.67523 13.737675 -39.694706 ;
createNode joint -n "ring_L_01_body_jnt" -p "aux_L_body_jnt";
	rename -uid "4F1D9757-45C8-E055-237C-A3ABF238B3A8";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.8311405395216127 0.0021514226983470053 -0.11069137836743259 ;
	setAttr ".r" -type "double3" -1.8618300881381078 -0.48299928185627838 -15.314000289355041 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.56523993552923368 -0.7981766402650099 -0.20836954244363273 0
		 0.80237014710612897 0.59062045503545646 -0.08584652076001402 0 0.19158800149225663 -0.11866561856313503 0.97427537619259963 0
		 66.381278216868196 99.029936876723767 -7.7889315450747469 1;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
	setAttr ".otp" -type "string" "ring_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing2";
	setAttr ".init_translate" -type "float3" 5.3333282 1.4210855e-14 3.8191672e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -19.091467 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.083176 99.960037 -7.754324 ;
	setAttr ".init_worldRotate" -type "float3" -9.885396 11.127673 -59.067322 ;
createNode joint -n "ring_L_02_body_jnt" -p "ring_L_01_body_jnt";
	rename -uid "A13E7267-430B-0E07-9D9D-6D838664306F";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.8411543705444515 5.3502594710153062e-06 -9.9262472730288209e-07 ;
	setAttr ".r" -type "double3" 0 0 -7.8844333491650502 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".bps" -type "matrix" 0.44983109893369033 -0.87164991941599068 -0.19462374062330007 0
		 0.87232219971539871 0.47554693664571707 -0.11361818045789504 0 0.19158800149225663 -0.11866561856313503 0.97427537619259963 0
		 68.552454413579724 95.964013870961409 -8.5893119892655942 1;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
	setAttr ".otp" -type "string" "ring_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing3";
	setAttr ".init_translate" -type "float3" 4.4992104 1.5743205e-06 -6.8833828e-15 ;
	setAttr ".init_rotate" -type "float3" 0 0 -2.5844507 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 68.352432 96.173294 -8.622653 ;
	setAttr ".init_worldRotate" -type "float3" -10.375423 10.673018 -61.658226 ;
createNode joint -n "ring_L_03_body_jnt" -p "ring_L_02_body_jnt";
	rename -uid "DA42DE89-49A2-1B77-F33A-2797D9360AFD";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.2657044284341836 -1.1133782322758634e-06 1.01047566047896e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.44983109893369033 -0.87164991941599068 -0.19462374062330007 0
		 0.87232219971539871 0.47554693664571707 -0.11361818045789504 0 0.19158800149225663 -0.11866561856313503 0.97427537619259963 0
		 70.021468186329727 93.117466045180322 -9.2248948917315783 1;
	setAttr ".sd" 1;
	setAttr ".typ" 21;
	setAttr ".otp" -type "string" "ring_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing4";
	setAttr ".init_translate" -type "float3" 3.053267 -4.2632564e-14 -1.5543122e-15 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 69.776833 93.532509 -9.1881304 ;
	setAttr ".init_worldRotate" -type "float3" -10.375423 10.673018 -61.658226 ;
createNode joint -n "pinky_L_01_body_jnt" -p "aux_L_body_jnt";
	rename -uid "3324A320-4BE9-9283-3DA4-C78F3CAE3D1A";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.5299401878647956 -0.65125545467765278 -2.5452931962821701 ;
	setAttr ".r" -type "double3" -11.036792647012575 8.1319986514033165 -12.232572341469872 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.57628323738817189 -0.73618192951809303 -0.35487152176023584 0
		 0.71365499067193505 0.66490917492617718 -0.2204367106178802 0 0.39823885369768786 -0.12622185131746486 0.90855591993863716 0
		 65.326859438768579 99.059519307048902 -10.09810474789934 1;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
	setAttr ".otp" -type "string" "pinky_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandPinky2";
	setAttr ".init_translate" -type "float3" 5.3488827 8.5265128e-14 2.6867397e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -6.2305484 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 64.977966 99.752274 -9.7970438 ;
	setAttr ".init_worldRotate" -type "float3" -13.130558 21.32748 -54.418766 ;
createNode joint -n "pinky_L_02_body_jnt" -p "pinky_L_01_body_jnt";
	rename -uid "853787A5-4A7A-9A69-179B-D99B598F50EE";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.0808041514216384 -4.0872082252008113e-06 -1.1031814111106542e-06 ;
	setAttr ".r" -type "double3" 0 0 -14.601049302792713 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".bps" -type "matrix" 0.37776869766925525 -0.88002162530512207 -0.28784153636437948 0
		 0.8358807489509652 0.45785367012324324 -0.30277613890108679 0 0.39823885369768786 -0.12622185131746486 0.90855591993863716 0
		 67.102275928808496 96.791486068290354 -11.19139483635332 1;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
	setAttr ".otp" -type "string" "pinky_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandPinky3";
	setAttr ".init_translate" -type "float3" 3.6157529 1.4210855e-14 3.3972825e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -16.650715 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.937744 97.013 -11.112085 ;
	setAttr ".init_worldRotate" -type "float3" -18.69408 16.727068 -71.359001 ;
createNode joint -n "pinky_L_03_body_jnt" -p "pinky_L_02_body_jnt";
	rename -uid "4901CAFE-40F4-4C4B-D09F-FD929C40D0CD";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 2.8942376587337044 4.5174186027452379e-06 1.3686764575027155e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.37776869766925525 -0.88002162530512207 -0.28784153636437948 0
		 0.8358807489509652 0.45785367012324324 -0.30277613890108679 0 0.39823885369768786 -0.12622185131746486 0.90855591993863716 0
		 68.195628017035375 94.244495045348046 -12.024476419883474 1;
	setAttr ".sd" 1;
	setAttr ".typ" 22;
	setAttr ".otp" -type "string" "pinky_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandPinky4";
	setAttr ".init_translate" -type "float3" 2.7254827 -1.4210855e-14 7.327472e-15 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 67.772041 94.539772 -11.896515 ;
	setAttr ".init_worldRotate" -type "float3" -18.69408 16.727068 -71.359001 ;
createNode joint -n "hand01_L_mtp_jnt" -p "hand_L_body_jnt";
	rename -uid "5C0244F9-44C4-6C31-FEC6-7598D4D7EDA4";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.5527136788005009e-14 -9.9475983006414026e-14 7.9936057773011271e-15 ;
	setAttr ".r" -type "double3" -3.9477856048777889e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 59.45930172143121 104.6648894070909 -5.7392108195610607 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand01_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand02_L_mtp_jnt" -p "hand_L_body_jnt";
	rename -uid "C6B21D91-43C3-B0DA-8E8D-2389762ADB55";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.5527136788005009e-14 -9.9475983006414026e-14 7.9936057773011271e-15 ;
	setAttr ".r" -type "double3" -3.9477856048777889e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 59.45930172143121 104.6648894070909 -5.7392108195610607 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand02_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand03_L_mtp_jnt" -p "hand_L_body_jnt";
	rename -uid "58A8F1D9-4CAD-AEF4-F776-3DBD94E5D388";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.5527136788005009e-14 -9.9475983006414026e-14 7.9936057773011271e-15 ;
	setAttr ".r" -type "double3" -3.9477856048777889e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 59.45930172143121 104.6648894070909 -5.7392108195610607 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand03_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand04_L_mtp_jnt" -p "hand_L_body_jnt";
	rename -uid "829C3FD8-49EB-B5FB-B1AB-EE95F81E8483";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.5527136788005009e-14 -9.9475983006414026e-14 7.9936057773011271e-15 ;
	setAttr ".r" -type "double3" -3.9477856048777889e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 59.45930172143121 104.6648894070909 -5.7392108195610607 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand04_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand05_L_mtp_jnt" -p "hand_L_body_jnt";
	rename -uid "2E593728-4EC8-C1BD-ABA4-B9949C06CA95";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.5527136788005009e-14 -9.9475983006414026e-14 7.9936057773011271e-15 ;
	setAttr ".r" -type "double3" -3.9477856048777889e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 59.45930172143121 104.6648894070909 -5.7392108195610607 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand05_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand_DL_bendDrv_helper_jnt" -p "hand_L_body_jnt";
	rename -uid "88CE9CD2-41E8-0891-0156-B4816D176C7D";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 57.33908914686409 104.61396124248014 -5.7850773188176507 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 4.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-3.975693351829396e-16, -9.93923337957349e-17, -1.6003718746328877e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-1.5, -1.5, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "hand_UL_bendDrv_helper_jnt" -p "hand_L_body_jnt";
	rename -uid "4E330123-4FF9-A437-1A8F-79B3823AB500";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901412719 -0.68992457717607614 0.017512245399853053 0
		 0.68980584766563602 0.72387649995029901 0.013065425595760391 0 -0.021690861136096848 0.0026250005938265736 0.99976127946378113 0
		 61.528719559880649 106.83651862649238 -5.7000145355369494 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, -4.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-3.975693351829396e-16, -9.93923337957349e-17, -1.6003718746328877e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 3.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "lowerarm01_L_mtp_jnt" -p "lowerarm_L_body_jnt";
	rename -uid "5E01518A-404F-92EE-E7E3-9C9359208209";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 1.0658141036401503e-13 -4.2632564145606011e-14 -3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" -2.5444437451708134e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862928 -0.68834335387957801 0.017762289766140388 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.052335412259155029 0.080819700258297072 0.99535379673451951 0
		 38.825841573540806 124.25057798298377 -6.2446078337019069 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "lowerarm01_L_mtp_jnt";
	setAttr ".radi" 3;
	setAttr ".mocapJnt" -type "string" "Character1_LeftForeArm";
	setAttr ".init_translate" -type "float3" 28.080956 2.8421709e-14 -7.2072972e-08 ;
	setAttr ".init_rotate" -type "float3" 0 -6.4964375 -4.20577e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 38.784966 125.4942 -6.221611 ;
	setAttr ".init_worldRotate" -type "float3" -4.1513027e-07 -0.8324374 -44.107414 ;
createNode joint -n "lowerarm02_L_mtp_jnt" -p "lowerarm_L_body_jnt";
	rename -uid "12207D5F-4766-5D9F-C912-6B8C43F46270";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 1.0658141036401503e-13 -4.2632564145606011e-14 -3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" -2.5444437451708134e-14 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862928 -0.68834335387957801 0.017762289766140388 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.052335412259155029 0.080819700258297072 0.99535379673451951 0
		 38.825841573540806 124.25057798298377 -6.2446078337019069 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "lowerarm02_L_mtp_jnt";
	setAttr ".radi" 3;
	setAttr ".mocapJnt" -type "string" "Character1_LeftForeArm";
	setAttr ".init_translate" -type "float3" 28.080956 2.8421709e-14 -7.2072972e-08 ;
	setAttr ".init_rotate" -type "float3" 0 -6.4964375 -4.20577e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 38.784966 125.4942 -6.221611 ;
	setAttr ".init_worldRotate" -type "float3" -4.1513027e-07 -0.8324374 -44.107414 ;
createNode joint -n "lowerarm_BL_bendDrv_helper_jnt" -p "lowerarm_L_body_jnt";
	rename -uid "27F3FC06-4D12-A130-8FE7-319272B5AEC4";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862928 -0.68834335387957801 0.017762289766140388 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.052335412259155029 0.080819700258297072 0.99535379673451951 0
		 38.616499354950747 123.9272997342977 -10.226022945345616 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, -1.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [3.975693351829397e-16, -3.975693351829397e-16, -3.1184344728411836e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, -4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
createNode joint -n "lowerarm_FL_bendDrv_helper_jnt" -p "lowerarm_L_body_jnt";
	rename -uid "E84A8FF3-4638-EC8C-6414-4D9C89C232DD";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862928 -0.68834335387957801 0.017762289766140388 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.052335412259155029 0.080819700258297072 0.99535379673451951 0
		 39.035182653023988 124.57385733636409 -2.2631925714694594 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 10.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [3.975693351829397e-16, -3.975693351829397e-16, -3.1184344728411836e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, -10.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "lowerarm_L_twist_helper_jnt" -p "lowerarm_L_body_jnt";
	rename -uid "A96E18C7-432C-38E3-1BFC-89B0B013CE5D";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862928 -0.68834335387957801 0.017762289766140388 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.052335412259155029 0.080819700258297072 0.99535379673451951 0
		 48.978186247008175 114.61377158101681 -5.9959357016815718 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-6.177573051184965, -0.012699031557499506, 0.12497870513322012], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [14.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm00_L_bend_helper_jnt" -p "upperarm_L_body_jnt";
	rename -uid "A794DD65-40F1-1065-8E2C-3F8BCC718103";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.65266077738930073 0.70929726492614065 -0.26632930673489558 0 0.25159596899630926 0.12867257571828075 0.95924076051991847 0
		 18.757613971123298 143.7125397205653 -3.5916091527838696 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 1.0, 1.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": true, \"usePivotRotate\": true, \"translation\": [-0.0, -0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_BL_bendDrv_helper_jnt" -p "upperarm00_L_bend_helper_jnt";
	rename -uid "FC61AA75-473F-25BE-0EF8-C5A6A79D8359";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.65266077738930073 0.70929726492614065 -0.26632930673489558 0 0.25159596899630926 0.12867257571828075 0.95924076051991847 0
		 18.637218627344392 140.47528793770724 -12.508206365598779 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 10.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [3.0, 0.0, -9.0], \"useBaseRotateSpace\": false, \"translationOrient\": [-90.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_FL_bendDrv_helper_jnt" -p "upperarm00_L_bend_helper_jnt";
	rename -uid "6E64ED6D-4710-6566-C615-B4B6C4036A63";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.65266077738930073 0.70929726492614065 -0.26632930673489558 0 0.25159596899630926 0.12867257571828075 0.95924076051991847 0
		 22.199693974552357 143.35578792538251 3.8933633526183811 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 8.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [2.0, 0.0, 8.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_OL_bendDrv_helper_jnt" -p "upperarm00_L_bend_helper_jnt";
	rename -uid "0B63AFB8-4B01-85EE-2B9B-80A6D50D3680";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.65266077738930073 0.70929726492614065 -0.26632930673489558 0 0.25159596899630926 0.12867257571828075 0.95924076051991847 0
		 23.978900190237706 149.38691783997444 -5.7222436066630369 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, -12.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 8.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm01_L_twist_helper_jnt" -p "upperarm_L_body_jnt";
	rename -uid "518C0894-4A42-B3ED-C583-CA9010450BBA";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.13369198018584244 0.0027637933546295428 0.99101907947338796 0
		 28.762799731333381 134.0096129140621 -4.9142842040835326 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [14.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_L_twistDrv_helper_jnt" -p "upperarm01_L_twist_helper_jnt";
	rename -uid "829EB05A-447F-0385-36AD-D9BA97F6BC88";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 -0.69306620046451539 -0.094476789378547504 0
		 0.68658071367581142 0.72086864491387981 -0.094632554591114998 0 0.13369198018584244 0.0027637933546295428 0.99101907947338796 0
		 29.564951612448436 134.02619567418989 1.0318302727567952 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 5.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [1.1044631234966796e-16, 6.468065141378585, -5.10387986614202e-15], \"transAngleType\": \"AXIS_Y\", \"useTranslation\": true, \"useRotate\": false, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [1.0, -1.0, 1.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": false, \"translation\": [0.0, 0.0, 6.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, -50.0, 0.0], \"translationAngleMax\": [-90.0, -130.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "clavicle_R_body_jnt" -p "spine_C_03_body_jnt";
	rename -uid "81A38BA3-447D-09EA-0582-BAB848F57EFD";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -5.3289699554443368 19.062286376953125 5.0667263269424438 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.85686433669142725 0.24835706427695231 0.45177680012379368 0
		 -0.21969156543697618 0.96866855457567824 -0.11583111607904423 0 -0.46638945590805458 -6.1894933622852477e-15 0.88457949072866748 0
		 -5.32897 147.60500000000005 3.4885599999999983 1;
	setAttr ".sd" 2;
	setAttr ".typ" 9;
	setAttr ".otp" -type "string" "clavicle_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftShoulder";
	setAttr ".init_translate" -type "float3" 6.064528 18.063614 -0.51298386 ;
	setAttr ".init_rotate" -type "float3" 2.2398803 0.016070072 -0.054539811 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.064528 144.95546 -3.4470987 ;
	setAttr ".init_worldRotate" -type "float3" -6.6994298e-06 0.013926188 -0.055126213 ;
createNode joint -n "upperarm_R_body_jnt" -p "clavicle_R_body_jnt";
	rename -uid "A3B366AE-49D6-5CA8-3FE4-CAA9C2A8B5BE";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -15.67177581787109 0.00019836425772723487 -1.4305114763857318e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.13369198018584233 0.0027637933546296903 0.99101907947338796 0
		 -18.7576 143.71299999999999 -3.5916100000000077 1;
	setAttr ".sd" 2;
	setAttr ".typ" 10;
	setAttr ".otp" -type "string" "upperarm_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftArm";
	setAttr ".init_translate" -type "float3" 12.655739 -6.2527761e-13 -1.4566126e-13 ;
	setAttr ".init_rotate" -type "float3" 0.0097352574 5.6539955 -44.051323 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 18.720261 144.94328 -3.4501748 ;
	setAttr ".init_worldRotate" -type "float3" -1.8777435e-14 5.664 -44.10741 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 14.137106198994587 14.46188178896729
		31.323999999999938 ;
createNode joint -n "lowerarm_R_body_jnt" -p "upperarm_R_body_jnt";
	rename -uid "0DF632F2-4C03-4994-8E45-3B89CC2553A8";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -28.080965042114261 -4.5776367073813162e-05 -5.2452087375698397e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862917 0.68834335387957801 -0.017762289766139805 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.052335412259155459 0.080819700258296712 0.99535379673451951 0
		 -38.82579999999998 124.25099999999999 -6.2446099999999953 1;
	setAttr ".sd" 2;
	setAttr ".typ" 11;
	setAttr ".otp" -type "string" "lowerarm_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftForeArm";
	setAttr ".init_translate" -type "float3" 28.080956 2.8421709e-14 -7.2072972e-08 ;
	setAttr ".init_rotate" -type "float3" 0 -6.4964375 -4.20577e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 38.784966 125.4942 -6.221611 ;
	setAttr ".init_worldRotate" -type "float3" -4.1513027e-07 -0.8324374 -44.107414 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 0 6.4680651413785437 0 ;
createNode joint -n "hand_R_body_jnt" -p "lowerarm_R_body_jnt";
	rename -uid "0CDD97D4-49D8-B1D8-58AB-499230F2456F";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -28.45361328125 -0.00019836425784092171 -2.002716064453125e-05 ;
	setAttr ".r" -type "double3" 6.1775313487003825 -0.026074234210768637 0.12288644018429917 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.459299999999963 104.66499999999996 -5.7392099999999937 1;
	setAttr ".sd" 2;
	setAttr ".typ" 12;
	setAttr ".otp" -type "string" "hand_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 6.1775312393754556 -0.026074235479975578
		0.12288644013663659 ;
createNode joint -n "thumb_R_01_body_jnt" -p "hand_R_body_jnt";
	rename -uid "77146E3D-4DE8-6563-9488-BCB69221CF1A";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -1.5316706606966903 -1.2218231823617032 3.1211561525100082 ;
	setAttr ".r" -type "double3" 83.509490245240812 41.676998508266372 39.802996378764021 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.071007989733464422 0.74024810751050862 -0.6685735596934137 0
		 -0.020605510320496685 0.67121103727808074 0.74097986233130164 0 0.9972628932926586 -0.038839191072851151 0.062914536463066051 0
		 -59.657199999999968 102.73199999999997 -2.6079384290695198 1;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
	setAttr ".otp" -type "string" "thumb";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandThumb2";
	setAttr ".init_translate" -type "float3" 1.3482351 0.00016244063 2.1316282e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -8.5725317 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.395477 103.6881 -2.791487 ;
	setAttr ".init_worldRotate" -type "float3" 80.166878 -29.830978 -83.507973 ;
createNode joint -n "thumb_R_02_body_jnt" -p "thumb_R_01_body_jnt";
	rename -uid "ECBF54BE-4588-B4CC-F50C-8A9AE54F8E4A";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.2003751263308864 0.00010667671018183 5.7364752876765124e-05 ;
	setAttr ".r" -type "double3" 0 0 25.226646132793508 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.055453813100315621 0.95572003652030635 -0.28900533975388687 0
		 -0.048903949474364009 0.29170315224630483 0.95525791004072702 0 0.9972628932926586 -0.038839191072851151 0.062914536463066051 0
		 -59.884400000000014 100.36300000000001 -0.46817042906954631 1;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
	setAttr ".otp" -type "string" "thumb";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandThumb3";
	setAttr ".init_translate" -type "float3" 3.9279501 -7.1054274e-15 -1.4210855e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -10.634403 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.780746 100.30246 -0.83755553 ;
	setAttr ".init_worldRotate" -type "float3" 80.966629 -19.339319 -85.422035 ;
createNode joint -n "thumb_R_03_body_jnt" -p "thumb_R_02_body_jnt";
	rename -uid "E2E1D2BB-4966-17CD-4BE5-858D3DE2BD28";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.3964027815046407 1.6757288602065046e-05 -5.3717111029527587e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.055453813100315621 0.95572003652030635 -0.28900533975388687 0
		 -0.048903949474364009 0.29170315224630483 0.95525791004072702 0 0.9972628932926586 -0.038839191072851151 0.062914536463066051 0
		 -60.072799999999994 97.11699999999999 0.51342057093049243 1;
	setAttr ".sd" 2;
	setAttr ".typ" 14;
	setAttr ".otp" -type "string" "thumb";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandThumb4";
	setAttr ".init_translate" -type "float3" 3.7845576 -2.1316282e-14 -1.4210855e-14 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 60.065765 96.742844 0.41574606 ;
	setAttr ".init_worldRotate" -type "float3" 80.966629 -19.339319 -85.422035 ;
createNode joint -n "index_R_01_body_jnt" -p "hand_R_body_jnt";
	rename -uid "CC4D7D29-41C1-D99A-B7D1-E0A820BE67E5";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -9.0543439950831583 0.69441560334391284 2.4556626486789135 ;
	setAttr ".r" -type "double3" -3.8530005383132839 12.470018145861456 -1.68598983998112 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.7214243940667201 0.65199486726647504 -0.23334424506217655 0
		 -0.67891855471834617 0.73231114940087871 -0.052820228344034964 0 0.13644207453940893 0.19652753883701773 0.97095854019316741 0
		 -66.437399999999982 98.927299999999988 -3.1164984290695186 1;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
	setAttr ".otp" -type "string" "index_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandIndex2";
	setAttr ".init_translate" -type "float3" 5.2504559 8.5265128e-14 1.7763568e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -3.295537 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.018509 99.773163 -3.1839013 ;
	setAttr ".init_worldRotate" -type "float3" 15.041655 -11.594504 -46.652084 ;
createNode joint -n "index_R_02_body_jnt" -p "index_R_01_body_jnt";
	rename -uid "552F2788-408D-C78B-67AD-0EB21A209435";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.9454882770790363 5.3187840393320585e-05 1.5565972116604598e-05 ;
	setAttr ".r" -type "double3" 0 0 16.046379848140578 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.50565285054106313 0.82901411676560011 -0.23885306977941309 0
		 -0.85187954256166976 0.52355756195667391 0.013737695691196684 0 0.13644207453940893 0.19652753883701773 0.97095854019316741 0
		 -69.283799999999999 96.354900000000015 -2.1958284290695245 1;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
	setAttr ".otp" -type "string" "index_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandIndex3";
	setAttr ".init_translate" -type "float3" 4.5327368 2.8421709e-14 3.5527137e-15 ;
	setAttr ".init_rotate" -type "float3" 0 0 -14.306174 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 69.066414 96.54422 -2.2728939 ;
	setAttr ".init_worldRotate" -type "float3" 17.374487 -7.5812063 -60.582386 ;
createNode joint -n "index_R_03_body_jnt" -p "index_R_02_body_jnt";
	rename -uid "778C2E7B-46D9-C31D-D6CD-09A2EEC14175";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.0546944788163088 -1.7270877663122519e-05 -1.2879797008480409e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.50565285054106313 0.82901411676560011 -0.23885306977941309 0
		 -0.85187954256166976 0.52355756195667391 0.013737695691196684 0 0.13644207453940893 0.19652753883701773 0.97095854019316741 0
		 -70.82840000000003 93.822499999999991 -1.4662184290695095 1;
	setAttr ".sd" 2;
	setAttr ".typ" 19;
	setAttr ".otp" -type "string" "index_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandIndex4";
	setAttr ".init_translate" -type "float3" 2.9975078 5.6843419e-14 -2.1316282e-14 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 70.525833 93.956024 -1.8774289 ;
	setAttr ".init_worldRotate" -type "float3" 17.374487 -7.5812063 -60.582386 ;
createNode joint -n "middle_R_01_body_jnt" -p "hand_R_body_jnt";
	rename -uid "525031BB-4F8C-3890-3F40-0793F1CE874D";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -9.2586773452289037 0.91940065489350786 0.024023292974124644 ;
	setAttr ".r" -type "double3" -6.3783474198181223 1.1840000133123394 3.1430182831809899 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.68416541573701151 0.72836605404043409 -0.037424259925475323 0
		 -0.72791794070932081 0.67875614022875563 -0.097085393830708452 0 -0.045311758991501194 0.093664259049700535 0.99457219500334237 0
		 -66.793199999999985 98.942800000000005 -5.5410384290695189 1;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
	setAttr ".otp" -type "string" "middle_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandMiddle2";
	setAttr ".init_translate" -type "float3" 5.282619 -4.2632564e-14 5.3290705e-15 ;
	setAttr ".init_rotate" -type "float3" 0 0 -20.568357 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.486145 99.893684 -5.322289 ;
	setAttr ".init_worldRotate" -type "float3" 2.2241752 -0.36346188 -56.74411 ;
createNode joint -n "middle_R_02_body_jnt" -p "middle_R_01_body_jnt";
	rename -uid "B5BEE922-41F0-591B-155D-88B4A8FAE0D3";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.9899232686117472 4.1506855325224024e-05 4.166663952531735e-06 ;
	setAttr ".r" -type "double3" 0 0 18.812612100600049 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".bps" -type "matrix" 0.41288142566018626 0.90833677637193833 -0.066732518572637373 0
		 -0.90965695338512531 0.40761661799650184 -0.079830569903927825 0 -0.045311758991501194 0.093664259049700535 0.99457219500334237 0
		 -69.522999999999982 96.036699999999982 -5.3917184290695159 1;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
	setAttr ".otp" -type "string" "middle_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandMiddle3";
	setAttr ".init_translate" -type "float3" 4.6574678 5.6843419e-14 0 ;
	setAttr ".init_rotate" -type "float3" 0 0 1.1104718 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 69.040146 95.999046 -5.2927442 ;
	setAttr ".init_worldRotate" -type "float3" 2.2167192 -0.40648782 -55.634449 ;
createNode joint -n "middle_R_03_body_jnt" -p "middle_R_02_body_jnt";
	rename -uid "32731F49-4917-CCA0-48F5-E481FE827CF3";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.2658594097114921 -2.1692464372335962e-05 2.6339332404035076e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.41288142566018626 0.90833677637193833 -0.066732518572637373 0
		 -0.90965695338512531 0.40761661799650184 -0.079830569903927825 0 -0.045311758991501194 0.093664259049700535 0.99457219500334237 0
		 -70.871399999999994 93.070200000000028 -5.173778429069519 1;
	setAttr ".sd" 2;
	setAttr ".typ" 20;
	setAttr ".otp" -type "string" "middle_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandMiddle4";
	setAttr ".init_translate" -type "float3" 2.9174213 -5.6843419e-14 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 70.686905 93.590912 -5.2720466 ;
	setAttr ".init_worldRotate" -type "float3" 2.2167192 -0.40648782 -55.634449 ;
createNode joint -n "aux_R_body_jnt" -p "hand_R_body_jnt";
	rename -uid "CD3B20CB-40C0-95A8-FF91-B6B048F37760";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -4.2131372075850884 0.30698383693201947 -0.941515555330807 ;
	setAttr ".r" -type "double3" -0.39331348559514329 -13.956661294749848 -4.4396542310593032 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.75725065286573823 0.61380060827675553 0.22320452955416922 0
		 -0.63056411859776906 0.77612118738902824 0.0049794400150661158 0 -0.170177381198066 -0.14451545164766899 0.9747589154060804 0
		 -62.740399999999973 101.97799999999998 -6.6027084290695193 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "aux_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing1";
	setAttr ".init_translate" -type "float3" 3.8059859 0.26664668 -0.30540955 ;
	setAttr ".init_rotate" -type "float3" -6.114687 8.0901203 4.3293967 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 62.096798 103.26897 -6.4877815 ;
	setAttr ".init_worldRotate" -type "float3" -5.67523 13.737675 -39.694706 ;
createNode joint -n "ring_R_01_body_jnt" -p "aux_R_body_jnt";
	rename -uid "62CD2386-433A-FF92-EB08-4EBE1DCC7A68";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -4.8313880113493894 0.0018396150755393137 -0.11063501734193792 ;
	setAttr ".r" -type "double3" -1.8618300881396137 0.48299928185726432 15.314000289352551 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.56523993552923346 0.7981766402650099 0.20836954244363273 0
		 -0.80237014710612686 0.59062045503545768 -0.085846520760025774 0 -0.19158800149226624 -0.11866561856312795 0.97427537619259852 0
		 -66.38130000000001 99.029900000000026 -7.7889284290695135 1;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
	setAttr ".otp" -type "string" "ring_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing2";
	setAttr ".init_translate" -type "float3" 5.3333282 1.4210855e-14 3.8191672e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -19.091467 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.083176 99.960037 -7.754324 ;
	setAttr ".init_worldRotate" -type "float3" -9.885396 11.127673 -59.067322 ;
createNode joint -n "ring_R_02_body_jnt" -p "ring_R_01_body_jnt";
	rename -uid "CA5CAD81-4208-3E54-EF96-80B9030B7553";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.8411556805452065 3.6744347056583138e-05 2.882315804697555e-06 ;
	setAttr ".r" -type "double3" 0 0 7.8844333739273731 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".bps" -type "matrix" 0.44983109893369033 0.87164991941599079 0.19462374062329843 0
		 -0.87232220466019972 0.4755469335830097 -0.11361815531227992 0 -0.19158797897800692 -0.11866563083678898 0.97427537912503437 0
		 -68.552500000000023 95.96399999999997 -8.5893084290695292 1;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
	setAttr ".otp" -type "string" "ring_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing3";
	setAttr ".init_translate" -type "float3" 4.4992104 1.5743205e-06 -6.8833828e-15 ;
	setAttr ".init_rotate" -type "float3" 0 0 -2.5844507 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 68.352432 96.173294 -8.622653 ;
	setAttr ".init_worldRotate" -type "float3" -10.375423 10.673018 -61.658226 ;
createNode joint -n "ring_R_03_body_jnt" -p "ring_R_02_body_jnt";
	rename -uid "7D19D1F4-4684-0B91-DF5B-8DB2B546E068";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.2656585698622607 -3.4114702884835424e-07 -1.4517930694069037e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.44983109893369033 0.87164991941599079 0.19462374062329843 0
		 -0.8723222110439125 0.47554692962906947 -0.11361812284941508 0 -0.19158794991222278 -0.11866564668201719 0.97427538291079185 0
		 -70.021500000000017 93.117500000000021 -9.2248984290695191 1;
	setAttr ".sd" 2;
	setAttr ".typ" 21;
	setAttr ".otp" -type "string" "ring_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandRing4";
	setAttr ".init_translate" -type "float3" 3.053267 -4.2632564e-14 -1.5543122e-15 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 69.776833 93.532509 -9.1881304 ;
	setAttr ".init_worldRotate" -type "float3" -10.375423 10.673018 -61.658226 ;
createNode joint -n "pinky_R_01_body_jnt" -p "aux_R_body_jnt";
	rename -uid "86E33AC3-4254-02EC-0BF9-24BB704EB71E";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -4.5302045164877711 -0.65155616970756114 -2.5452694319784914 ;
	setAttr ".r" -type "double3" -11.036792647014149 -8.1319986514024141 12.232572341467623 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.57628323738817178 0.73618192951809291 0.35487152176023584 0
		 -0.71365499067193461 0.66490917492617696 -0.22043671061788106 0 -0.39823885369768841 -0.12622185131746427 0.90855591993863694 0
		 -65.326899999999995 99.059500000000028 -10.098138429069511 1;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
	setAttr ".otp" -type "string" "pinky_L_01";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandPinky2";
	setAttr ".init_translate" -type "float3" 5.3488827 8.5265128e-14 2.6867397e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -6.2305484 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 64.977966 99.752274 -9.7970438 ;
	setAttr ".init_worldRotate" -type "float3" -13.130558 21.32748 -54.418766 ;
createNode joint -n "pinky_R_02_body_jnt" -p "pinky_R_01_body_jnt";
	rename -uid "1561A1D4-44B6-823C-026F-DBB2CC447443";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.0807706725855084 9.9284757766326948e-06 -2.1994837361205555e-05 ;
	setAttr ".r" -type "double3" 0 0 14.601049302792706 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 0 -90 ;
	setAttr ".bps" -type "matrix" 0.37776869766925514 0.88002162530512196 0.2878415363643792 0
		 -0.83588074895096487 0.45785367012324291 -0.30277613890108768 0 -0.39823885369768841 -0.12622185131746427 0.90855591993863694 0
		 -67.1023 96.791500000000013 -11.191438429069516 1;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
	setAttr ".otp" -type "string" "pinky_L_02";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandPinky3";
	setAttr ".init_translate" -type "float3" 3.6157529 1.4210855e-14 3.3972825e-14 ;
	setAttr ".init_rotate" -type "float3" 0 0 -16.650715 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 66.937744 97.013 -11.112085 ;
	setAttr ".init_worldRotate" -type "float3" -18.69408 16.727068 -71.359001 ;
createNode joint -n "pinky_R_03_body_jnt" -p "pinky_R_02_body_jnt";
	rename -uid "E13B3D32-406F-5559-B4C8-318E4C539CB7";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -2.8942006283938646 -6.4037642374614734e-05 5.6112142679864974e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.37776869766925514 0.88002162530512196 0.2878415363643792 0
		 -0.83588074895096487 0.45785367012324291 -0.30277613890108768 0 -0.39823885369768841 -0.12622185131746427 0.90855591993863694 0
		 -68.195599999999985 94.244499999999988 -12.024438429069516 1;
	setAttr ".sd" 2;
	setAttr ".typ" 22;
	setAttr ".otp" -type "string" "pinky_L_03";
	setAttr ".mocapJnt" -type "string" "Character1_LeftHandPinky4";
	setAttr ".init_translate" -type "float3" 2.7254827 -1.4210855e-14 7.327472e-15 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 67.772041 94.539772 -11.896515 ;
	setAttr ".init_worldRotate" -type "float3" -18.69408 16.727068 -71.359001 ;
createNode joint -n "hand01_R_mtp_jnt" -p "hand_R_body_jnt";
	rename -uid "0BC64130-4097-5BDB-C2A0-72971DFED608";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -2.1316282072803006e-14 5.6843418860808015e-14 7.9936057773011271e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.459300000000063 104.66499999999999 -5.7392099999999893 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand01_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand02_R_mtp_jnt" -p "hand_R_body_jnt";
	rename -uid "FB421E31-4D69-95CB-4DA3-A8BD4DB38489";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -2.1316282072803006e-14 5.6843418860808015e-14 7.9936057773011271e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.459300000000063 104.66499999999999 -5.7392099999999893 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand02_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand03_R_mtp_jnt" -p "hand_R_body_jnt";
	rename -uid "7881F65A-4C9B-2E4A-9D90-C6897F9B7D6F";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -2.1316282072803006e-14 5.6843418860808015e-14 7.9936057773011271e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.459300000000063 104.66499999999999 -5.7392099999999893 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand03_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand04_R_mtp_jnt" -p "hand_R_body_jnt";
	rename -uid "3E210D8C-41E1-214F-C85D-EC83BBD91ED5";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -2.1316282072803006e-14 5.6843418860808015e-14 7.9936057773011271e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.459300000000063 104.66499999999999 -5.7392099999999893 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand04_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand05_R_mtp_jnt" -p "hand_R_body_jnt";
	rename -uid "C2A134CF-4A83-79CA-6E09-DD8FFB70C345";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -2.1316282072803006e-14 5.6843418860808015e-14 7.9936057773011271e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.459300000000063 104.66499999999999 -5.7392099999999893 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "hand05_L_mtp_jnt";
	setAttr ".radi" 3.2;
	setAttr ".mocapJnt" -type "string" "Character1_LeftHand";
	setAttr ".init_translate" -type "float3" 28.453373 -2.8421709e-14 0 ;
	setAttr ".init_rotate" -type "float3" 4.7892206e-07 6.4964375 4.2329502e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 59.21336 105.69258 -5.8082333 ;
	setAttr ".init_worldRotate" -type "float3" -6.1799128e-08 5.664 -44.107407 ;
createNode joint -n "hand_DR_bendDrv_helper_jnt" -p "hand_R_body_jnt";
	rename -uid "0D3AAB99-4D50-C2AA-F07A-60AF91D9DAEB";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -59.510094834998135 102.54429885135657 -5.732539782345885 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 4.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-3.975693351829396e-16, -9.93923337957349e-17, -1.6003718746328877e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-1.5, -1.5, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "hand_UR_bendDrv_helper_jnt" -p "hand_R_body_jnt";
	rename -uid "D4A887DA-4679-15CF-DA24-7B81FA15FB48";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72366939901415783 0.68992457717604361 -0.017512245399863291 0
		 -0.6898058476656036 0.72387649995032988 0.013065425595756464 0 0.02169086113610174 0.002625000593835497 0.99976127946378102 0
		 -61.528717050972119 106.83662996689712 -5.7000137352647755 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, -4.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-3.975693351829396e-16, -9.93923337957349e-17, -1.6003718746328877e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 3.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "lowerarm01_R_mtp_jnt" -p "lowerarm_R_body_jnt";
	rename -uid "F4F2B36B-4694-1060-EA4D-0584C080EF26";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.9737991503207013e-14 -1.7053025658242404e-13 1.9539925233402755e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862917 0.68834335387957801 -0.017762289766139805 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.052335412259155459 0.080819700258296712 0.99535379673451951 0
		 -38.825799999999823 124.25100000000005 -6.2446099999999785 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "lowerarm01_L_mtp_jnt";
	setAttr ".radi" 3;
	setAttr ".mocapJnt" -type "string" "Character1_LeftForeArm";
	setAttr ".init_translate" -type "float3" 28.080956 2.8421709e-14 -7.2072972e-08 ;
	setAttr ".init_rotate" -type "float3" 0 -6.4964375 -4.20577e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 38.784966 125.4942 -6.221611 ;
	setAttr ".init_worldRotate" -type "float3" -4.1513027e-07 -0.8324374 -44.107414 ;
createNode joint -n "lowerarm02_R_mtp_jnt" -p "lowerarm_R_body_jnt";
	rename -uid "1E10A68A-4EBA-5730-6337-AEBFA856E0AC";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.9737991503207013e-14 -1.7053025658242404e-13 1.9539925233402755e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862917 0.68834335387957801 -0.017762289766139805 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.052335412259155459 0.080819700258296712 0.99535379673451951 0
		 -38.825799999999823 124.25100000000005 -6.2446099999999785 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "lowerarm02_L_mtp_jnt";
	setAttr ".radi" 3;
	setAttr ".mocapJnt" -type "string" "Character1_LeftForeArm";
	setAttr ".init_translate" -type "float3" 28.080956 2.8421709e-14 -7.2072972e-08 ;
	setAttr ".init_rotate" -type "float3" 0 -6.4964375 -4.20577e-06 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 38.784966 125.4942 -6.221611 ;
	setAttr ".init_worldRotate" -type "float3" -4.1513027e-07 -0.8324374 -44.107414 ;
createNode joint -n "lowerarm_BR_bendDrv_helper_jnt" -p "lowerarm_R_body_jnt";
	rename -uid "676D3CA6-488A-95AF-9F44-0A8E331C2738";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862917 0.68834335387957801 -0.017762289766139805 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.052335412259155459 0.080819700258296712 0.99535379673451951 0
		 -38.616458177118531 123.92772136755976 -10.22602516395588 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, -1.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [3.975693351829397e-16, -3.975693351829397e-16, -3.1184344728411836e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, -4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, 90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "lowerarm_FR_bendDrv_helper_jnt" -p "lowerarm_R_body_jnt";
	rename -uid "C717C5F9-447B-1C63-9154-669686E5D33D";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862917 0.68834335387957801 -0.017762289766139805 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.052335412259155459 0.080819700258296712 0.99535379673451951 0
		 -39.035141475191772 124.57427896962612 -2.2631947900797229 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 10.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [3.975693351829397e-16, -3.975693351829397e-16, -3.1184344728411836e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, -10.0, 0.0], \"translationAngleMax\": [-90.0, 90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "lowerarm_R_twist_helper_jnt" -p "lowerarm_R_body_jnt";
	rename -uid "40A18693-46CA-32FA-22EE-76ADB2899A49";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.72516751735862917 0.68834335387957801 -0.017762289766139805 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.052335412259155459 0.080819700258296712 0.99535379673451951 0
		 -48.978145069175966 114.61419321427884 -5.9959379202918441 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-6.177573051184965, -0.012699031557499506, 0.12497870513322012], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-14.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm00_R_bend_helper_jnt" -p "upperarm_R_body_jnt";
	rename -uid "61580715-4214-6D7D-8636-E085A0274317";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.65266077738930195 0.70929726492614109 -0.26632930673489102 0 -0.25159596899630604 0.12867257571827742 0.9592407605199198 0
		 -18.757600336594127 143.71299990243372 -3.5916101774673663 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 1.0, 1.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": true, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_BR_bendDrv_helper_jnt" -p "upperarm00_R_bend_helper_jnt";
	rename -uid "6B449111-4D78-C0BE-C940-8DAFC386679C";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.65266077738930195 0.70929726492614109 -0.26632930673489102 0 -0.25159596899630604 0.12867257571827742 0.9592407605199198 0
		 -18.637204992815242 140.47574811957568 -12.508207390282283 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, -10.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-3.0, 0.0, -9.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_FR_bendDrv_helper_jnt" -p "upperarm00_R_bend_helper_jnt";
	rename -uid "6CC5C91D-4CF7-9B56-F0B9-839086E5D5D8";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.65266077738930195 0.70929726492614109 -0.26632930673489102 0 -0.25159596899630604 0.12867257571827742 0.9592407605199198 0
		 -22.199680340023153 143.35624810725091 3.893362327934903 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 8.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-2.0, 0.0, 8.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [-90.0, 90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_OR_bendDrv_helper_jnt" -p "upperarm00_R_bend_helper_jnt";
	rename -uid "B709CAD1-45B9-F82E-33AB-3C92A4B2C10F";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.65266077738930195 0.70929726492614109 -0.26632930673489102 0 -0.25159596899630604 0.12867257571827742 0.9592407605199198 0
		 -23.978886555708538 149.38737802184286 -5.7222446313464905 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, -12.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 8.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm01_R_twist_helper_jnt" -p "upperarm_R_body_jnt";
	rename -uid "DC57D3E4-403D-7DDA-0823-B5A5C6E4DFC8";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.13369198018584233 0.0027637933546296903 0.99101907947338796 0
		 -28.762786096804213 134.01007309593049 -4.914285228767028 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [7.951386703658791e-16, 7.951386703658794e-16, -1.4312496066585827e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-14.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "upperarm_R_twistDrv_helper_jnt" -p "upperarm01_R_twist_helper_jnt";
	rename -uid "64ECB4CF-4A7F-F27C-3F94-4CB64597EEDD";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.71465612572929216 0.69306620046451539 0.094476789378547366 0
		 -0.68658071367581142 0.72086864491387959 -0.094632554591115109 0 -0.13369198018584233 0.0027637933546296903 0.99101907947338796 0
		 -29.564937977919264 134.02665585605828 1.0318292480732998 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, -5.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [1.1044631234966796e-16, 6.468065141378585, -5.10387986614202e-15], \"transAngleType\": \"AXIS_Y\", \"useTranslation\": true, \"useRotate\": false, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [1.0, -1.0, 1.0], \"version\": 0, \"rotAngleType\": \"RHV_X\", \"cancelParentRotate\": false, \"usePivotRotate\": false, \"translation\": [0.0, 0.0, 6.0], \"useBaseRotateSpace\": false, \"translationOrient\": [90.0, -50.0, 0.0], \"translationAngleMax\": [-90.0, 130.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "spine01_C_mtp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "CB3B38CB-4709-28B1-4B1B-03A7E1686F2D";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 9.8607613152626476e-32 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99923594957621453 -0.039083462928978699 0
		 0 0.039083462928978699 0.99923594957621453 0 6.52077091257172e-16 128.35924789153918 -0.82927481962407634 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "spine01_C_mtp_jnt";
	setAttr ".radi" 3.1000000000000005;
	setAttr ".mocapJnt" -type "string" "Character1_Spine2";
	setAttr ".init_translate" -type "float3" 4.3471806e-16 11.321802 -7.9936058e-15 ;
	setAttr ".init_rotate" -type "float3" 1.2030466 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.5207709e-16 126.9257 -2.2285182 ;
	setAttr ".init_worldRotate" -type "float3" -2.239888 0 0 ;
createNode joint -n "spine02_C_mtp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "43A61B9B-40D3-B0F5-BB73-689F84432663";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 9.8607613152626476e-32 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99923594957621453 -0.039083462928978699 0
		 0 0.039083462928978699 0.99923594957621453 0 6.52077091257172e-16 128.35924789153918 -0.82927481962407634 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "spine02_C_mtp_jnt";
	setAttr ".radi" 3.1000000000000005;
	setAttr ".mocapJnt" -type "string" "Character1_Spine2";
	setAttr ".init_translate" -type "float3" 4.3471806e-16 11.321802 -7.9936058e-15 ;
	setAttr ".init_rotate" -type "float3" 1.2030466 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.5207709e-16 126.9257 -2.2285182 ;
	setAttr ".init_worldRotate" -type "float3" -2.239888 0 0 ;
createNode joint -n "spine03_C_mtp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "93F9BF73-483C-86DC-F6C1-1F9DB403DF02";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 9.8607613152626476e-32 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99923594957621453 -0.039083462928978699 0
		 0 0.039083462928978699 0.99923594957621453 0 6.52077091257172e-16 128.35924789153918 -0.82927481962407634 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "spine03_C_mtp_jnt";
	setAttr ".radi" 3.1000000000000005;
	setAttr ".mocapJnt" -type "string" "Character1_Spine2";
	setAttr ".init_translate" -type "float3" 4.3471806e-16 11.321802 -7.9936058e-15 ;
	setAttr ".init_rotate" -type "float3" 1.2030466 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 6.5207709e-16 126.9257 -2.2285182 ;
	setAttr ".init_worldRotate" -type "float3" -2.239888 0 0 ;
createNode joint -n "bow_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "1F89F062-4415-14F0-E84F-57A9F9B8CD01";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 6.45 4.37 -16.58 ;
	setAttr ".r" -type "double3" 203.9 79.67 37.98 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" 0.1413444551327202 0.071812706412477584 -0.98735235868505911 0
		 0.24851935418781387 -0.96800057477278878 -0.034828405556708304 0 -0.9582587727734645 -0.24045336852967131 -0.15466836122952771 0
		 6.4460000000000006 132.07286991261395 -17.568205415232281 1;
	setAttr ".radi" 2.5;
createNode joint -n "sword_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "9808BF0A-4B5A-7F08-3FB3-8AB1086891F3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -21.91 32.18 -14.05 ;
	setAttr ".r" -type "double3" -82.25 85.23 -236.03999999999996 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 54.183 88.702 -100.824 ;
	setAttr ".bps" -type "matrix" -0.046489802359663601 0.030029853605895183 -0.99846727846683481 0
		 0.43966393780574364 -0.89690826650550204 -0.047446635995003733 0 -0.89695837142517743 -0.44119584015095126 0.028494044356491478 0
		 -21.907 159.96261855382676 -16.124130025936484 1;
	setAttr ".radi" 2.5;
createNode joint -n "shield_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "184F6131-4AF4-E9CE-9DF2-B2A7A2484188";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -1.96 -4.09 -21.11 ;
	setAttr ".r" -type "double3" -0.77 178.79 14.09 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 2.164 178.791 14.089 ;
	setAttr ".bps" -type "matrix" -0.96970284628630066 -0.24401330315931138 -0.011571421067830719 0
		 -0.24368184145917882 0.96954632245107164 -0.024476289846838389 0 0.017191569076459877 -0.020914982736899134 -0.99963343954161732 0
		 -1.9599999999999993 123.44528339997964 -21.764215420822161 1;
	setAttr ".radi" 2.5;
createNode joint -n "spr01_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "088EAC77-4A12-7AC6-B045-949109CF6BF6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -6.44 -2.68 -19.62 ;
	setAttr ".r" -type "double3" 2.7700000000000005 0.57 15.680000000000001 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "spr02_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "1D3E6A0C-4B25-5D0A-B95F-9BBB663C176C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -1.07 -4.49 -20.31 ;
	setAttr ".r" -type "double3" 1.8300000000000003 1.04 13.29 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "aid01_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "B24628D2-47CD-E38E-9E3A-F882202C047F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -14.6 -0.97 9.65 ;
	setAttr ".r" -type "double3" 8.67 -0.71 4.93 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "aid02_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "F6333C65-4145-3491-4F45-1E85FE55E0AA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -17.9 -0.69 5.09 ;
	setAttr ".r" -type "double3" 8.78 -11.54 2.23 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "smoke01_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "A1F7B7E3-47B8-795D-CCAE-C7B2CE55AEEE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -5.76 1.1 15 ;
	setAttr ".r" -type "double3" 0 -37.2 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "smoke02_cnp_jnt" -p "spine_C_03_body_jnt";
	rename -uid "E93F5955-4C67-C7BB-6CDE-BE8C6FAD013D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -11.54 -0.53 14.05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "pot_cnp_jnt" -p "spine_C_02_body_jnt";
	rename -uid "680AF4A8-43D1-53D3-DF42-9FB84235DF6C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 21.55 -2.9 -7.5 ;
	setAttr ".r" -type "double3" -27.950000000000003 68.89 -199.94 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.20304654232088 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "pelvis01_C_mtp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "87FF491F-4C34-0AB7-116D-B8AD1A4CF4D1";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 100.69000244140625 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "pelvis01_C_mtp_jnt";
	setAttr ".radi" 3.5;
	setAttr ".mocapJnt" -type "string" "Character1_Hips";
	setAttr ".init_translate" -type "float3" 0 102.00221 -1.5644366 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 0 102.00221 -1.5644366 ;
createNode joint -n "pelvis02_C_mtp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "357F44C3-430F-059E-BA06-7DB9242937FA";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 100.69000244140625 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "pelvis02_C_mtp_jnt";
	setAttr ".radi" 3.5;
	setAttr ".mocapJnt" -type "string" "Character1_Hips";
	setAttr ".init_translate" -type "float3" 0 102.00221 -1.5644366 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 0 102.00221 -1.5644366 ;
createNode joint -n "pelvis03_C_mtp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "9C391A43-4243-C180-EA5A-CCBB6FA49AA0";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 100.69000244140625 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "pelvis03_C_mtp_jnt";
	setAttr ".radi" 3.5;
	setAttr ".mocapJnt" -type "string" "Character1_Hips";
	setAttr ".init_translate" -type "float3" 0 102.00221 -1.5644366 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 0 102.00221 -1.5644366 ;
createNode joint -n "thigh_L_body_jnt" -p "pelvis_C_body_jnt";
	rename -uid "CD47B852-4D7E-AA56-E879-3EAD6E0FAB3C";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 9.5741186141967773 -5.7505722045898438 -1.5196530818939209 ;
	setAttr ".r" -type "double3" -2.1228767084300495 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089715040869101439 0.99581455349447634 0.017452406437283512 0 0.0015659818634078597 -0.017382007687710088 0.99984769515639127 0
		 9.5741186141967773 94.939430236816406 -1.5196530818939209 1;
	setAttr ".sd" 1;
	setAttr ".typ" 2;
	setAttr ".otp" -type "string" "thigh_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftUpLeg";
	setAttr ".init_translate" -type "float3" 9.5741186 -5.7505722 0.044783473 ;
	setAttr ".init_rotate" -type "float3" 1.2861837 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 96.25164 -1.5196531 ;
	setAttr ".init_worldRotate" -type "float3" 1.2861837 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" -2.1228769785642925 0 5.148 ;
createNode joint -n "calf_L_body_jnt" -p "thigh_L_body_jnt";
	rename -uid "B53851C3-4DC7-CA17-4610-5E88BA22C159";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 -42.797706225311522 2.0177970916357424e-07 ;
	setAttr ".r" -type "double3" 7.3921077171332668 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089655158661907736 0.99514987594608317 0.040480574721752483 0 0.0036322696278243494 -0.040317285959674556 0.99918032560203907 0
		 13.413716577304406 52.320851521469997 -2.2665760455215174 1;
	setAttr ".sd" 1;
	setAttr ".typ" 3;
	setAttr ".otp" -type "string" "calf_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftLeg";
	setAttr ".init_translate" -type "float3" 0 -42.637745 -2.8732572e-13 ;
	setAttr ".init_rotate" -type "float3" 2.4125397 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 53.624638 -2.4767108 ;
	setAttr ".init_worldRotate" -type "float3" 3.6987233 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 7.3921081283073979 0 0 ;
createNode joint -n "foot_L_body_jnt" -p "calf_L_body_jnt";
	rename -uid "E9594DAC-4BFB-9511-776E-6CACE63BE3F4";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -1.7763568394002505e-15 -45.277999432143723 -1.2650806002767467e-07 ;
	setAttr ".r" -type "double3" -5.2692310087032146 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089728706985786125 0.99596624397750499 -6.9388939039072284e-18 0 0 -6.9388939039072284e-18 1 0
		 17.473122799314254 7.262456014282769 -4.0994554843466453 1;
	setAttr ".sd" 1;
	setAttr ".typ" 4;
	setAttr ".otp" -type "string" "foot_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftFoot";
	setAttr ".init_translate" -type "float3" 1.7763568e-15 -41.39687 -2.6645353e-14 ;
	setAttr ".init_rotate" -type "float3" -3.6987233 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 12.313996 -5.1472259 ;
	setAttr ".init_worldRotate" -type "float3" 1.5902774e-14 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" -5.2692311497431037 0 0 ;
createNode joint -n "ball_L_body_jnt" -p "foot_L_body_jnt";
	rename -uid "0FD3CAF6-4D18-5926-C5A7-4A95E2337540";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 1.7763568394002505e-15 -3.7383430004119864 13.177079677581787 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089728706985786125 0.99596624397750499 -6.9388939039072284e-18 0 0 -6.9388939039072284e-18 1 0
		 17.808559491584976 3.5391924822892786 9.0776239788969519 1;
	setAttr ".sd" 1;
	setAttr ".typ" 5;
	setAttr ".otp" -type "string" "ball_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftToeBase";
	setAttr ".init_translate" -type "float3" 0 -8.6468592 13.527758 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 3.6671369 8.3805323 ;
createNode joint -n "foot_FL_bendDrv_helper_jnt" -p "foot_L_body_jnt";
	rename -uid "7CE08984-46D0-A313-20BF-06B1F241685C";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.4746155748715515 0 0 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089609862816042773 0.99464710336650008 -0.051451066565436673 0 -0.0046166376759562439 0.051243525515814535 0.99867551674669541 0
		 17.105090501022346 11.347522634603781 -0.20371641005624364 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [-5.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.4746155748715515, -5.843360913954649e-17, -1.1916944583590731e-15], \"transAngleType\": \"RHV_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 4.0, 4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 120.0, 90.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "foot_BL_bendDrv_helper_jnt" -p "foot_L_body_jnt";
	rename -uid "5A59AFB4-44BA-1CAF-EF1C-86AA4DAA1C69";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.4746155748715515 0 0 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089698991022748573 0.99563640420730326 -0.025734055775418652 0 -0.0023090835502284166 0.025630250872951319 0.99966882434801763 0
		 17.293665385342681 9.254388502237779 -8.3616095866720848 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [8.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.4746155748715515, -5.843360913954649e-17, -1.1916944583590731e-15], \"transAngleType\": \"AXIS_X\", \"useTranslation\": true, \"useRotate\": false, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [1.0, -1.0, 1.0], \"version\": 0, \"rotAngleType\": \"AXIS_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": false, \"translation\": [0.0, 2.0, -4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "calf_BL_bendDrv_helper_jnt" -p "calf_L_body_jnt";
	rename -uid "22D2C8AC-4B6D-DA73-0A75-A694AC193616";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089336938256670065 0.99161770890157463 0.093344688417263261 0 0.00837569819567212 -0.092968158718192209 0.99563385295212026 0
		 13.346711025713429 53.064596414108188 -10.231646875747572 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [12.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.987846675914698e-16, -9.279842534897338e-18, 8.748411370334822e-15], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, -8.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "calf_FL_bendDrv_helper_jnt" -p "calf_L_body_jnt";
	rename -uid "771940DD-4167-ED67-5B57-418541E479A6";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089336938256670065 0.99161770890157463 0.093344688417263261 0 0.00837569819567212 -0.092968158718192209 0.99563385295212026 0
		 13.455595102257165 51.856010350771683 2.7115932126299911 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [-1.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.987846675914698e-16, -9.279842534897338e-18, 8.748411370334822e-15], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 5.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "calf_L_twist_helper_jnt" -p "calf_L_body_jnt";
	rename -uid "F2904231-47EF-3D06-C3AC-35B213A18E80";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089655158661907736 0.99514987594608317 0.040480574721752483 0 0.0036322696278243494 -0.040317285959674556 0.99918032560203907 0
		 15.430957681171728 29.929978935575786 -3.1773889833700406 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [2.32, 4.756022374534179e-17, -7.952239896533774e-16], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 0.5, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, -22.5, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh00_L_bend_helper_jnt" -p "thigh_L_body_jnt";
	rename -uid "7FB81F9E-4F64-9D5B-BE38-4DB1EE4D3BE4";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 0.089715040869101439 0.00078451344792710104 0
		 -0.089715040869101439 0.99581455349447634 0.017452406437283512 0 0.00078451344792712077 -0.017452406437283508 0.99984738737879286 0
		 9.5741186141967773 94.939430236816406 -1.5196530818939209 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [2.981770013872047e-16, -1.5530525216016433e-17, -4.055212639601628e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [1.0, 0.0, 1.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": true, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_BL_bendDrv_helper_jnt" -p "thigh00_L_bend_helper_jnt";
	rename -uid "7FA980CA-40BC-7DF6-6FCC-AD95F9D0D70F";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 0.089715040869101439 0.00078451344792710104 0
		 -0.089703105039949729 0.99592034659354989 -0.0097987849846304237 0 -0.0016604113003305158 0.0096888948202946204 0.99995168300847159 0
		 9.5947349180733692 94.819129200679285 -13.935436902871917 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [12.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-0.9959670581475112, -0.08972418823908691, -5.147220146709999], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, -12.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_FL_bendDrv_helper_jnt" -p "thigh00_L_bend_helper_jnt";
	rename -uid "01EEC08D-4B5D-4F25-9709-2E8611074AD9";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 0.089715040869101439 0.00078451344792710104 0
		 -0.089703105039949729 0.99592034659354989 -0.0097987849846304237 0 -0.0016604113003305158 0.0096888948202946204 0.99995168300847159 0
		 9.5608353237941337 95.016941395378765 6.4799603821738518 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [-15.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-0.9959670581475112, -0.08972418823908691, -5.147220146709999], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 8.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_OL_bendDrv_helper_jnt" -p "thigh00_L_bend_helper_jnt";
	rename -uid "0557892E-4AE4-4B8D-4AD4-AD9DF133B502";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 0.089715040869101439 0.00078451344792710104 0
		 -0.089715040869101439 0.99581455349447634 0.017452406437283512 0 0.00078451344792712077 -0.017452406437283508 0.99984738737879286 0
		 17.541855943122243 95.657150563769221 -1.5133769743105041 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 12.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-0.9959670581475112, -0.08972418823908691, -5.147220146709999], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [8.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh01_L_twist_helper_jnt" -p "thigh_L_body_jnt";
	rename -uid "C188D1FF-4D9B-0471-9D9C-B1B29640225D";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 0.089728706985786125 -1.0842021724855042e-19 0
		 -0.089715040869101439 0.99581455349447634 0.017452406437283512 0 0.0015659818634078597 -0.017382007687710088 0.99984769515639127 0
		 11.45813447244791 74.027324613432398 -1.8861536170768749 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [2.981770013872047e-16, -1.5530525216016433e-17, -4.055212639601628e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, 0.0], \"version\": 0, \"rotAngleType\": \"AXIS_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, -21.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_R_body_jnt" -p "pelvis_C_body_jnt";
	rename -uid "226295B7-4F25-0E88-4659-E382D7780B16";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -9.5741195678710938 -5.7506027221679688 -1.5196499824523926 ;
	setAttr ".r" -type "double3" -2.1228767084300495 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089715040869101439 0.99581455349447634 0.017452406437283512 0 -0.0015659818634078597 -0.017382007687710088 0.99984769515639127 0
		 -9.5741200000000006 94.939400000000006 -1.5196499999999999 1;
	setAttr ".sd" 2;
	setAttr ".typ" 2;
	setAttr ".otp" -type "string" "thigh_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftUpLeg";
	setAttr ".init_translate" -type "float3" 9.5741186 -5.7505722 0.044783473 ;
	setAttr ".init_rotate" -type "float3" 1.2861837 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 96.25164 -1.5196531 ;
	setAttr ".init_worldRotate" -type "float3" 1.2861837 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" -2.1228745075475208 -1.2424041724466862e-17
		-5.148 ;
createNode joint -n "calf_R_body_jnt" -p "thigh_R_body_jnt";
	rename -uid "D745DC62-47D2-E330-E344-E5876452C31B";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 -42.79767186995668 2.1525633542296418e-07 ;
	setAttr ".r" -type "double3" 7.392107717133265 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089655158661907736 0.99514987594608317 0.040480574721752483 0 -0.0036322696278243494 -0.040317285959674556 0.99918032560203907 0
		 -13.413714955281689 52.320854670770494 -2.2665723785105523 1;
	setAttr ".sd" 2;
	setAttr ".typ" 3;
	setAttr ".otp" -type "string" "calf_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftLeg";
	setAttr ".init_translate" -type "float3" 0 -42.637745 -2.8732572e-13 ;
	setAttr ".init_rotate" -type "float3" 2.4125397 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 53.624638 -2.4767108 ;
	setAttr ".init_worldRotate" -type "float3" 3.6987233 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" 7.3921003347869423 0 0 ;
createNode joint -n "foot_R_body_jnt" -p "calf_R_body_jnt";
	rename -uid "39E8446E-40F3-9717-24E9-FCA5570B98E3";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "HB_BaseBindOrient" -ln "HB_BaseBindOrient" -at "double3" -nc
		3;
	addAttr -ci true -sn "HB_BaseBindOrientX" -ln "HB_BaseBindOrientX" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientY" -ln "HB_BaseBindOrientY" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -ci true -sn "HB_BaseBindOrientZ" -ln "HB_BaseBindOrientZ" -at "doubleAngle"
		-p "HB_BaseBindOrient";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 -45.278008060365309 -2.2114701980768814e-07 ;
	setAttr ".r" -type "double3" -5.2692310087032128 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089728706985786125 0.99596624397750499 -6.9388939039072284e-18 0 0 -6.9388939039072284e-18 1 0
		 -17.473121880245401 7.2624513609709211 -4.09945213472934 1;
	setAttr ".sd" 2;
	setAttr ".typ" 4;
	setAttr ".otp" -type "string" "foot_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftFoot";
	setAttr ".init_translate" -type "float3" 1.7763568e-15 -41.39687 -2.6645353e-14 ;
	setAttr ".init_rotate" -type "float3" -3.6987233 0 0 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 12.313996 -5.1472259 ;
	setAttr ".init_worldRotate" -type "float3" 1.5902774e-14 0 0 ;
	setAttr ".HB_BaseBindOrient" -type "double3" -5.269 0 0 ;
createNode joint -n "ball_R_body_jnt" -p "foot_R_body_jnt";
	rename -uid "072A9B46-494E-9C49-DAAA-8CB2F28C448B";
	addAttr -ci true -sn "mocapJnt" -ln "mocapJnt" -dt "string";
	addAttr -ci true -sn "init_translate" -ln "init_translate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_translateX" -ln "init_translateX" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateY" -ln "init_translateY" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_translateZ" -ln "init_translateZ" -at "float" -p "init_translate";
	addAttr -ci true -sn "init_rotate" -ln "init_rotate" -at "float3" -nc 3;
	addAttr -ci true -sn "init_rotateX" -ln "init_rotateX" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateY" -ln "init_rotateY" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_rotateZ" -ln "init_rotateZ" -at "float" -p "init_rotate";
	addAttr -ci true -sn "init_scale" -ln "init_scale" -at "float3" -nc 3;
	addAttr -ci true -sn "init_scaleX" -ln "init_scaleX" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleY" -ln "init_scaleY" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_scaleZ" -ln "init_scaleZ" -at "float" -p "init_scale";
	addAttr -ci true -sn "init_worldTranslate" -ln "init_worldTranslate" -at "float3"
		-nc 3;
	addAttr -ci true -sn "init_worldTranslateX" -ln "init_worldTranslateX" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateY" -ln "init_worldTranslateY" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldTranslateZ" -ln "init_worldTranslateZ" -at "float"
		-p "init_worldTranslate";
	addAttr -ci true -sn "init_worldRotate" -ln "init_worldRotate" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_worldRotateX" -ln "init_worldRotateX" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateY" -ln "init_worldRotateY" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_worldRotateZ" -ln "init_worldRotateZ" -at "float" -p "init_worldRotate";
	addAttr -ci true -sn "init_jointOrient" -ln "init_jointOrient" -at "float3" -nc
		3;
	addAttr -ci true -sn "init_jointOrientX" -ln "init_jointOrientX" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientY" -ln "init_jointOrientY" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "init_jointOrientZ" -ln "init_jointOrientZ" -at "float" -p "init_jointOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0 -3.7382879257202148 13.17709493637085 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089728706985786125 0.99596624397750499 -6.9388939039072284e-18 0 0 -6.9388939039072284e-18 1 0
		 -17.80855363451894 3.5392426395132208 9.0776425995695043 1;
	setAttr ".sd" 2;
	setAttr ".typ" 5;
	setAttr ".otp" -type "string" "ball_L";
	setAttr ".mocapJnt" -type "string" "Character1_LeftToeBase";
	setAttr ".init_translate" -type "float3" 0 -8.6468592 13.527758 ;
	setAttr ".init_scale" -type "float3" 1 1 1 ;
	setAttr ".init_worldTranslate" -type "float3" 9.5741186 3.6671369 8.3805323 ;
createNode joint -n "foot_FR_bendDrv_helper_jnt" -p "foot_R_body_jnt";
	rename -uid "61A8F16B-4EAC-5C88-B2CE-6FBA62A1A851";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.4745000000000001 0 0 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089609881440326083 0.99464731009139473 -0.051447037584330557 0 0.0046162761606911218 0.051239512786635223 0.9986757243088451 0
		 -17.10509028707266 11.347510154645255 -0.20370478683179805 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [-5.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.4746155748715515, -5.843360913954649e-17, -1.1916944583590731e-15], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 4.0, 4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 120.0, 90.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "foot_BR_bendDrv_helper_jnt" -p "foot_R_body_jnt";
	rename -uid "91FD96EF-4461-1405-3A12-27BD98C23F92";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.4745000000000001 0 0 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089609881440326083 0.99464731009139473 -0.051447037584330557 0 0.0046162761606911218 0.051239512786635223 0.9986757243088451 0
		 -17.303564739185088 9.1444932915222381 -8.4116380413048315 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [8.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.4746155748715515, -5.843360913954649e-17, -1.1916944583590731e-15], \"transAngleType\": \"AXIS_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 2.0, -4.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "calf_BR_bendDrv_helper_jnt" -p "calf_R_body_jnt";
	rename -uid "439B3C1A-4932-2153-1B1D-CF80B39C55ED";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089336938826311968 0.99161771522445741 0.093344620702912801 0 -0.0083756921197510083 -0.09296809127698491 0.99563385930061143 0
		 -13.346709380002526 53.064599826341627 -10.23164324546077 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [12.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.987846675914698e-16, -9.279842534897338e-18, 8.748411370334822e-15], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, -8.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "calf_FR_bendDrv_helper_jnt" -p "calf_R_body_jnt";
	rename -uid "9DD779B4-44C9-BB05-D920-60B6A9F9A341";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089336938826311968 0.99161771522445741 0.093344620702912801 0 -0.0083756921197510083 -0.09296809127698491 0.99563385930061143 0
		 -13.455593377559289 51.856014639740827 2.7115969254471781 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [-1.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-1.987846675914698e-16, -9.279842534897338e-18, 8.748411370334822e-15], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 5.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "calf_R_twist_helper_jnt" -p "calf_R_body_jnt";
	rename -uid "2F230F4D-42FC-D001-92E5-88A8F2A629EB";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089655158661907736 0.99514987594608317 0.040480574721752483 0 -0.0036322696278243494 -0.040317285959674556 0.99918032560203907 0
		 -15.430955986853458 29.929982887338873 -3.1773853022953089 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [2.32, 4.756022374534179e-17, -7.952239896533774e-16], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, 0.5, 0.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, -22.5, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh00_R_bend_helper_jnt" -p "thigh_R_body_jnt";
	rename -uid "00B9D4F2-453D-6FD8-28B1-61ABE26AA358";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 -0.089715040869101439 -0.00078451344792712869 0
		 0.089715040869101439 0.99581455349447634 0.017452406437283512 0 -0.00078451344792709312 -0.017452406437283512 0.99984738737879286 0
		 -9.5741195678710938 94.939400196075439 -1.5196499824523926 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [2.981770013872047e-16, -1.5530525216016433e-17, -4.055212639601628e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": false, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [1.0, 0.0, 1.0], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": true, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_BR_bendDrv_helper_jnt" -p "thigh00_R_bend_helper_jnt";
	rename -uid "F6AF18AC-4C1D-5101-4D96-A88825A315F9";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 -0.089715040869101439 -0.00078451344792712869 0
		 0.089703105075754311 0.9959203468024781 -0.0097987634219768929 0 0.0016604093660001079 0.0096888733445715941 0.99995168321976946 0
		 -9.5947358477302895 94.819099426589133 -13.935433806053943 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [12.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-0.9959670581475112, -0.08972418823908691, -5.147220146709999], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, -12.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_FR_bendDrv_helper_jnt" -p "thigh00_R_bend_helper_jnt";
	rename -uid "072C2FCF-4CD2-4C4A-0463-1C951A1B0B45";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 -0.089715040869101439 -0.00078451344792712869 0
		 0.089703105075754311 0.9959203468024781 -0.0097987634219768929 0 0.0016604093660001079 0.0096888733445715941 0.99995168321976946 0
		 -9.560836292943085 95.016911182832004 6.4799634833057622 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [-15.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-0.9959670581475112, -0.08972418823908691, -5.147220146709999], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, 0.0, 8.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [-90.0, -90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh_OR_bendDrv_helper_jnt" -p "thigh00_R_bend_helper_jnt";
	rename -uid "20824B31-4326-DB81-E185-8387E171B718";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596716611568348 -0.089715040869101439 -0.00078451344792712869 0
		 0.089703105075754311 0.9959203468024781 -0.0097987634219768929 0 0.0016604093660001079 0.0096888733445715941 0.99995168321976946 0
		 -17.541856896796553 95.657120523028254 -1.513373874868976 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, -12.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [-0.9959670581475112, -0.08972418823908691, -5.147220146709999], \"transAngleType\": \"RHV_Y\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [-0.5, 0.0, -0.5], \"version\": 0, \"rotAngleType\": \"RHV_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [-8.0, 0.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 90.0, 0.0], \"translationAngleMax\": [90.0, 90.0, -90.0]}";
	setAttr ".liw" yes;
createNode joint -n "thigh01_R_twist_helper_jnt" -p "thigh_R_body_jnt";
	rename -uid "A689E01B-43A7-D86B-4370-42AA2FA91745";
	addAttr -ci true -sn "HB_EditData" -ln "HB_EditData" -dt "string";
	addAttr -ci true -sn "HB_BaseOrient" -ln "HB_BaseOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_BaseOrientX" -ln "HB_BaseOrientX" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientY" -ln "HB_BaseOrientY" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_BaseOrientZ" -ln "HB_BaseOrientZ" -at "doubleAngle" -p "HB_BaseOrient";
	addAttr -ci true -sn "HB_ParentOrient" -ln "HB_ParentOrient" -at "double3" -nc 3;
	addAttr -ci true -sn "HB_ParentOrientX" -ln "HB_ParentOrientX" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientY" -ln "HB_ParentOrientY" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "HB_ParentOrientZ" -ln "HB_ParentOrientZ" -at "doubleAngle"
		-p "HB_ParentOrient";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99596624397750499 -0.089728706985786125 1.0842021724855042e-19 0
		 0.089715040869101439 0.99581455349447634 0.017452406437283512 0 -0.0015659818634078597 -0.017382007687710088 0.99984769515639127 0
		 -11.458135426122224 74.027294572691432 -1.8861505176353459 1;
	setAttr ".HB_EditData" -type "string" "{\"translationValue\": [0.0, 0.0, 0.0], \"translationAngleMin\": [0.0, 0.0, 0.0], \"baseSpaceOrient\": [2.981770013872047e-16, -1.5530525216016433e-17, -4.055212639601628e-14], \"transAngleType\": \"AXIS_X\", \"useTranslation\": true, \"useRotate\": true, \"orient\": [0.0, 0.0, 0.0], \"rotationRatio\": [0.0, -0.5, 0.0], \"version\": 0, \"rotAngleType\": \"AXIS_Y\", \"cancelParentRotate\": false, \"usePivotRotate\": true, \"translation\": [0.0, -21.0, 0.0], \"useBaseRotateSpace\": false, \"translationOrient\": [0.0, 0.0, 0.0], \"translationAngleMax\": [90.0, 90.0, 90.0]}";
	setAttr ".liw" yes;
createNode joint -n "torch_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "76575AF5-4FB4-2834-0C64-0F8DB7DE4DCE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 23.9 -0.52 -22.15 ;
	setAttr ".r" -type "double3" 20.13 -55.05 63.65 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991602 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "quiver_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "B02284B3-48F3-DF45-7E2E-B5BCB046AB2D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.69 0.18 -18.73 ;
	setAttr ".r" -type "double3" -68.37 113.42 -79.8 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991611 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "onesword_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "6AA253A6-402B-8DF4-EDD0-F28667E52158";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 20.66 1.29 5.73 ;
	setAttr ".r" -type "double3" -27.14 -12.72 -171.49 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991624 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "porch01_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "F6E603F3-4E89-244B-2CC3-BA964A8312AF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 11.91 -2.88 8.17 ;
	setAttr ".r" -type "double3" -8.58 37.31 2.04 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991629 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "porch02_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "CB6A9279-419C-B445-2304-06936947416F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -18.28 -3.82 -1.46 ;
	setAttr ".r" -type "double3" 12.38 -79.33 -27.06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991637 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "monocle_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "3D1828E1-4172-91A7-D775-10A6B5522E4B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -15.83 0.53 8.48 ;
	setAttr ".r" -type "double3" 90 0 -9.66 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991646 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "waterbottle_cnp_jnt" -p "pelvis_C_body_jnt";
	rename -uid "5C029650-4425-68AD-08A4-A196E1725960";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 18.58 -2.7 -7.97 ;
	setAttr ".r" -type "double3" 10.02 -28.62 -1.54 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2398879660991629 0 0 ;
	setAttr ".pa" -type "double3" 50 86.74 -90 ;
	setAttr ".bps" -type "matrix" -2.2204460492503131e-16 -0.095843806161689013 -0.99539638577826928 0
		 0.64278760968653958 -0.7625178700261579 0.073420615117534255 0 -0.76604444311897801 -0.63982846350503408 0.061607211065932019 0
		 -7.9999999999999991 119.65006393157819 -18.987756572019702 1;
	setAttr ".radi" 2.5;
createNode joint -n "move_jnt" -p "root_jnt";
	rename -uid "D8218578-4AF9-C4D7-36DE-44AFE94810AD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "move_jnt";
createNode joint -n "root01_mtp_jnt" -p "root_jnt";
	rename -uid "3E346839-410D-D235-A407-1A91F73050B1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root01_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root02_mtp_jnt" -p "root_jnt";
	rename -uid "F8C81333-47D2-B678-D60F-F1A8B5CC1D53";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root02_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root03_mtp_jnt" -p "root_jnt";
	rename -uid "7FA8078D-4A43-2778-21C1-098116F3AD1C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root03_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root04_mtp_jnt" -p "root_jnt";
	rename -uid "D6B2B6E7-4CB0-104A-137A-60ADAB81527D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root04_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root05_mtp_jnt" -p "root_jnt";
	rename -uid "77D4C779-422C-49C1-426B-FE8D8E6AE861";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root05_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root06_mtp_jnt" -p "root_jnt";
	rename -uid "297C5600-4C88-280E-DD5D-FAAC1C227593";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root06_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root07_mtp_jnt" -p "root_jnt";
	rename -uid "C959592B-44A1-AD26-680A-27AD7E5AF8A1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root07_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root08_mtp_jnt" -p "root_jnt";
	rename -uid "CBB5725C-4029-6D9B-BFBF-A5B90F80C658";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root08_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root09_mtp_jnt" -p "root_jnt";
	rename -uid "121FA435-46F7-050B-F537-CD8E7CA05CA7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root09_mtp_jnt";
	setAttr ".radi" 3.5;
createNode joint -n "root10_mtp_jnt" -p "root_jnt";
	rename -uid "65E9934A-48CD-15BD-3608-63BFA57217CF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "root10_mtp_jnt";
	setAttr ".radi" 3.5;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 10 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 12 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 8 ".u";
select -ne :defaultRenderingList1;
	setAttr -s 4 ".r";
select -ne :defaultTextureList1;
	setAttr -s 6 ".tx";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
	setAttr ".fs" 1.9980019980019981;
	setAttr ".ef" 19.980019980019978;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 3 ".sol";
connectAttr "root_jnt.s" "pelvis_C_body_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "spine_C_01_body_jnt.is";
connectAttr "spine_C_01_body_jnt.s" "spine_C_02_body_jnt.is";
connectAttr "spine_C_02_body_jnt.s" "spine_C_03_body_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "neck_C_body_jnt.is";
connectAttr "neck_C_body_jnt.s" "head_C_body_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "clavicle_L_body_jnt.is";
connectAttr "clavicle_L_body_jnt.s" "upperarm_L_body_jnt.is";
connectAttr "upperarm_L_body_jnt.s" "lowerarm_L_body_jnt.is";
connectAttr "lowerarm_L_body_jnt.s" "hand_L_body_jnt.is";
connectAttr "hand_L_body_jnt.s" "thumb_L_01_body_jnt.is";
connectAttr "thumb_L_01_body_jnt.s" "thumb_L_02_body_jnt.is";
connectAttr "thumb_L_02_body_jnt.s" "thumb_L_03_body_jnt.is";
connectAttr "hand_L_body_jnt.s" "index_L_01_body_jnt.is";
connectAttr "index_L_01_body_jnt.s" "index_L_02_body_jnt.is";
connectAttr "index_L_02_body_jnt.s" "index_L_03_body_jnt.is";
connectAttr "hand_L_body_jnt.s" "middle_L_01_body_jnt.is";
connectAttr "middle_L_01_body_jnt.s" "middle_L_02_body_jnt.is";
connectAttr "middle_L_02_body_jnt.s" "middle_L_03_body_jnt.is";
connectAttr "hand_L_body_jnt.s" "aux_L_body_jnt.is";
connectAttr "aux_L_body_jnt.s" "ring_L_01_body_jnt.is";
connectAttr "ring_L_01_body_jnt.s" "ring_L_02_body_jnt.is";
connectAttr "ring_L_02_body_jnt.s" "ring_L_03_body_jnt.is";
connectAttr "aux_L_body_jnt.s" "pinky_L_01_body_jnt.is";
connectAttr "pinky_L_01_body_jnt.s" "pinky_L_02_body_jnt.is";
connectAttr "pinky_L_02_body_jnt.s" "pinky_L_03_body_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand01_L_mtp_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand02_L_mtp_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand03_L_mtp_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand04_L_mtp_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand05_L_mtp_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand_DL_bendDrv_helper_jnt.is";
connectAttr "hand_L_body_jnt.s" "hand_UL_bendDrv_helper_jnt.is";
connectAttr "lowerarm_L_body_jnt.s" "lowerarm01_L_mtp_jnt.is";
connectAttr "lowerarm_L_body_jnt.s" "lowerarm02_L_mtp_jnt.is";
connectAttr "lowerarm_L_body_jnt.s" "lowerarm_BL_bendDrv_helper_jnt.is";
connectAttr "lowerarm_L_body_jnt.s" "lowerarm_FL_bendDrv_helper_jnt.is";
connectAttr "lowerarm_L_body_jnt.s" "lowerarm_L_twist_helper_jnt.is";
connectAttr "upperarm_L_body_jnt.s" "upperarm00_L_bend_helper_jnt.is";
connectAttr "upperarm00_L_bend_helper_jnt.s" "upperarm_BL_bendDrv_helper_jnt.is"
		;
connectAttr "upperarm00_L_bend_helper_jnt.s" "upperarm_FL_bendDrv_helper_jnt.is"
		;
connectAttr "upperarm00_L_bend_helper_jnt.s" "upperarm_OL_bendDrv_helper_jnt.is"
		;
connectAttr "upperarm_L_body_jnt.s" "upperarm01_L_twist_helper_jnt.is";
connectAttr "upperarm01_L_twist_helper_jnt.s" "upperarm_L_twistDrv_helper_jnt.is"
		;
connectAttr "spine_C_03_body_jnt.s" "clavicle_R_body_jnt.is";
connectAttr "clavicle_R_body_jnt.s" "upperarm_R_body_jnt.is";
connectAttr "upperarm_R_body_jnt.s" "lowerarm_R_body_jnt.is";
connectAttr "lowerarm_R_body_jnt.s" "hand_R_body_jnt.is";
connectAttr "hand_R_body_jnt.s" "thumb_R_01_body_jnt.is";
connectAttr "thumb_R_01_body_jnt.s" "thumb_R_02_body_jnt.is";
connectAttr "thumb_R_02_body_jnt.s" "thumb_R_03_body_jnt.is";
connectAttr "hand_R_body_jnt.s" "index_R_01_body_jnt.is";
connectAttr "index_R_01_body_jnt.s" "index_R_02_body_jnt.is";
connectAttr "index_R_02_body_jnt.s" "index_R_03_body_jnt.is";
connectAttr "hand_R_body_jnt.s" "middle_R_01_body_jnt.is";
connectAttr "middle_R_01_body_jnt.s" "middle_R_02_body_jnt.is";
connectAttr "middle_R_02_body_jnt.s" "middle_R_03_body_jnt.is";
connectAttr "hand_R_body_jnt.s" "aux_R_body_jnt.is";
connectAttr "aux_R_body_jnt.s" "ring_R_01_body_jnt.is";
connectAttr "ring_R_01_body_jnt.s" "ring_R_02_body_jnt.is";
connectAttr "ring_R_02_body_jnt.s" "ring_R_03_body_jnt.is";
connectAttr "aux_R_body_jnt.s" "pinky_R_01_body_jnt.is";
connectAttr "pinky_R_01_body_jnt.s" "pinky_R_02_body_jnt.is";
connectAttr "pinky_R_02_body_jnt.s" "pinky_R_03_body_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand01_R_mtp_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand02_R_mtp_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand03_R_mtp_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand04_R_mtp_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand05_R_mtp_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand_DR_bendDrv_helper_jnt.is";
connectAttr "hand_R_body_jnt.s" "hand_UR_bendDrv_helper_jnt.is";
connectAttr "lowerarm_R_body_jnt.s" "lowerarm01_R_mtp_jnt.is";
connectAttr "lowerarm_R_body_jnt.s" "lowerarm02_R_mtp_jnt.is";
connectAttr "lowerarm_R_body_jnt.s" "lowerarm_BR_bendDrv_helper_jnt.is";
connectAttr "lowerarm_R_body_jnt.s" "lowerarm_FR_bendDrv_helper_jnt.is";
connectAttr "lowerarm_R_body_jnt.s" "lowerarm_R_twist_helper_jnt.is";
connectAttr "upperarm_R_body_jnt.s" "upperarm00_R_bend_helper_jnt.is";
connectAttr "upperarm00_R_bend_helper_jnt.s" "upperarm_BR_bendDrv_helper_jnt.is"
		;
connectAttr "upperarm00_R_bend_helper_jnt.s" "upperarm_FR_bendDrv_helper_jnt.is"
		;
connectAttr "upperarm00_R_bend_helper_jnt.s" "upperarm_OR_bendDrv_helper_jnt.is"
		;
connectAttr "upperarm_R_body_jnt.s" "upperarm01_R_twist_helper_jnt.is";
connectAttr "upperarm01_R_twist_helper_jnt.s" "upperarm_R_twistDrv_helper_jnt.is"
		;
connectAttr "spine_C_03_body_jnt.s" "spine01_C_mtp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "spine02_C_mtp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "spine03_C_mtp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "bow_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "sword_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "shield_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "spr01_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "spr02_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "aid01_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "aid02_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "smoke01_cnp_jnt.is";
connectAttr "spine_C_03_body_jnt.s" "smoke02_cnp_jnt.is";
connectAttr "spine_C_02_body_jnt.s" "pot_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "pelvis01_C_mtp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "pelvis02_C_mtp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "pelvis03_C_mtp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "thigh_L_body_jnt.is";
connectAttr "thigh_L_body_jnt.s" "calf_L_body_jnt.is";
connectAttr "calf_L_body_jnt.s" "foot_L_body_jnt.is";
connectAttr "foot_L_body_jnt.s" "ball_L_body_jnt.is";
connectAttr "foot_L_body_jnt.s" "foot_FL_bendDrv_helper_jnt.is";
connectAttr "foot_L_body_jnt.s" "foot_BL_bendDrv_helper_jnt.is";
connectAttr "calf_L_body_jnt.s" "calf_BL_bendDrv_helper_jnt.is";
connectAttr "calf_L_body_jnt.s" "calf_FL_bendDrv_helper_jnt.is";
connectAttr "calf_L_body_jnt.s" "calf_L_twist_helper_jnt.is";
connectAttr "thigh_L_body_jnt.s" "thigh00_L_bend_helper_jnt.is";
connectAttr "thigh00_L_bend_helper_jnt.s" "thigh_BL_bendDrv_helper_jnt.is";
connectAttr "thigh00_L_bend_helper_jnt.s" "thigh_FL_bendDrv_helper_jnt.is";
connectAttr "thigh00_L_bend_helper_jnt.s" "thigh_OL_bendDrv_helper_jnt.is";
connectAttr "thigh_L_body_jnt.s" "thigh01_L_twist_helper_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "thigh_R_body_jnt.is";
connectAttr "thigh_R_body_jnt.s" "calf_R_body_jnt.is";
connectAttr "calf_R_body_jnt.s" "foot_R_body_jnt.is";
connectAttr "foot_R_body_jnt.s" "ball_R_body_jnt.is";
connectAttr "foot_R_body_jnt.s" "foot_FR_bendDrv_helper_jnt.is";
connectAttr "foot_R_body_jnt.s" "foot_BR_bendDrv_helper_jnt.is";
connectAttr "calf_R_body_jnt.s" "calf_BR_bendDrv_helper_jnt.is";
connectAttr "calf_R_body_jnt.s" "calf_FR_bendDrv_helper_jnt.is";
connectAttr "calf_R_body_jnt.s" "calf_R_twist_helper_jnt.is";
connectAttr "thigh_R_body_jnt.s" "thigh00_R_bend_helper_jnt.is";
connectAttr "thigh00_R_bend_helper_jnt.s" "thigh_BR_bendDrv_helper_jnt.is";
connectAttr "thigh00_R_bend_helper_jnt.s" "thigh_FR_bendDrv_helper_jnt.is";
connectAttr "thigh00_R_bend_helper_jnt.s" "thigh_OR_bendDrv_helper_jnt.is";
connectAttr "thigh_R_body_jnt.s" "thigh01_R_twist_helper_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "torch_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "quiver_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "onesword_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "porch01_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "porch02_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "monocle_cnp_jnt.is";
connectAttr "pelvis_C_body_jnt.s" "waterbottle_cnp_jnt.is";
connectAttr "root_jnt.s" "move_jnt.is";
connectAttr "root_jnt.s" "root01_mtp_jnt.is";
connectAttr "root_jnt.s" "root02_mtp_jnt.is";
connectAttr "root_jnt.s" "root03_mtp_jnt.is";
connectAttr "root_jnt.s" "root04_mtp_jnt.is";
connectAttr "root_jnt.s" "root05_mtp_jnt.is";
connectAttr "root_jnt.s" "root06_mtp_jnt.is";
connectAttr "root_jnt.s" "root07_mtp_jnt.is";
connectAttr "root_jnt.s" "root08_mtp_jnt.is";
connectAttr "root_jnt.s" "root09_mtp_jnt.is";
connectAttr "root_jnt.s" "root10_mtp_jnt.is";
// End of char_000.ma
