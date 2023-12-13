//Maya ASCII 2018ff09 scene
//Name: joints.ma
//Last modified: Mon, Aug 23, 2021 08:22:37 AM
//Codeset: 932
requires maya "2018ff09";
requires -dataType "HIKCharacter" -dataType "HIKCharacterState" -dataType "HIKEffectorState"
		 -dataType "HIKPropertySetState" "mayaHIK" "1.0_HIK_2016.5";
requires -nodeType "displayPoints" "Type" "2.0a";
requires "mtoa" "3.1.1.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntscf;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811122215-49253d42f6";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "A27FC86D-41E9-DA25-6DA6-24AC778DEA68";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
	setAttr ".rp" -type "double3" 3.5527136788005009e-15 0 0 ;
	setAttr ".rpt" -type "double3" -7.6078914483658395e-16 0 -2.1970279652718475e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "135E6874-49A7-28D3-21E5-919C7358DE2E";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "87D106DF-4643-8BC3-F104-4699020C5A5C";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "17071416-43B8-8891-40A4-BFB5737E2AB6";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "0BB21E87-4B3F-1241-01E9-89B74E1B84E0";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "C001A676-4CFA-E597-0577-D2A3E549F8A5";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "F2266572-4F1C-9157-D5CA-76AAF3EACECB";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "C0FD06FA-434D-9067-9F0A-0FA08D20B1C8";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "transform1";
	rename -uid "070CF88C-4FF2-ABC8-9478-CABB54EE5873";
	setAttr ".hio" yes;
createNode displayPoints -n "displayPoints1" -p "transform1";
	rename -uid "38AA2368-4DC3-874F-9E73-BF8E35013485";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".boundingBoxes" -type "vectorArray" 0 ;
	setAttr ".hio" yes;
createNode transform -n "transform2";
	rename -uid "53A60E99-4F0E-B9CF-EE8F-50A96ADBC325";
	setAttr ".hio" yes;
createNode displayPoints -n "displayPoints2" -p "transform2";
	rename -uid "A880B2CA-4094-F6D8-24FD-B596369D26BC";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".boundingBoxes" -type "vectorArray" 0 ;
	setAttr ".hio" yes;
createNode joint -n "root_jnt";
	rename -uid "99774033-495A-8104-0F67-20A72308FF6F";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn -3.1554436208840472e-30 
		-smx -3.1554436208840472e-30 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 1.7516230804060213e-46 
		-smx 1.7516230804060213e-46 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -l on -k on ".txInitVal" -3.1554436208840472e-30;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" 1.7516230804060213e-46;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
createNode joint -n "cog_jnt" -p "root_jnt";
	rename -uid "B8CC79C6-480C-D2D9-4C08-3CB86FDFB5BB";
	addAttr -is true -ci true -k true -sn "TypeID" -ln "TypeID" -dt "string";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn -3.5527136788005009e-13 
		-smx -3.5527136788005009e-13 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn -7.0064923216240854e-46 
		-smx -7.0064923216240854e-46 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0 103.40000152587891 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 103.40000152587891 0 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineA";
	setAttr -l on -k on ".txInitVal" -3.5527136788005009e-13;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" -7.0064923216240854e-46;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
createNode joint -n "hip_jnt" -p "cog_jnt";
	rename -uid "2DF83DEE-40DA-69AA-04F9-01BA321458C1";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 103.99999999999999 
		-smx 103.99999999999999 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 180 -smx 
		180 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 7.0622500768802529e-31 
		-smx 7.0622500768802529e-31 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 89.999999999999986 
		-smx 89.999999999999986 -at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -3.0814879110195774e-33 -0.10000000149013033 3.0814879110195774e-33 ;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 -1.5407439555097887e-33 103.30000152438879 3.0814879110195774e-33 1;
	setAttr -l on -k on ".txInitVal";
	setAttr -l on -k on ".tyInitVal" 103.99999999999999;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" 180;
	setAttr -l on -k on ".jyInitVal" 7.0622500768802529e-31;
	setAttr -l on -k on ".jzInitVal" 89.999999999999986;
	setAttr -k on ".liw";
createNode joint -n "uplegR_jnt" -p "hip_jnt";
	rename -uid "946FAA2B-4E15-DC06-C322-7E826FCD640C";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn -10.500000000000014 
		-smx -10.500000000000014 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 10 -smx 10 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn -4 -smx -4 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 179.99999999999983 
		-smx 179.99999999999983 -at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 7.7999978065490723 -10.499999999999998 -1.7000000476837156 ;
	setAttr ".r" -type "double3" -7.016709298534876e-15 1.1938873188843833e-14 -1.5902773407317584e-13 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 -10.499999999999998 95.500003717839718 -1.7000000476837158 1;
	setAttr -l on -k on ".txInitVal" -10.500000000000014;
	setAttr -l on -k on ".tyInitVal" 10;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" -4;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal" 179.99999999999983;
	setAttr -k on ".liw";
createNode joint -n "legR_jnt" -p "uplegR_jnt";
	rename -uid "313517A6-41CE-85FB-2ED5-0FA13A370EB3";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 41.999999999999865 
		-smx 41.999999999999865 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 5.1514348342607263e-14 
		-smx 5.1514348342607263e-14 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 1.340595996300771e-14 
		-smx 1.340595996300771e-14 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 38.599998474121115 5.3290705182007514e-15 6.6613381477509392e-16 ;
	setAttr ".r" -type "double3" 0 -3.8194222020138361e-15 0 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 -10.499999999999989 56.900005243718624 -1.7000000476837158 1;
	setAttr -l on -k on ".txInitVal" 41.999999999999865;
	setAttr -l on -k on ".tyInitVal" 5.1514348342607263e-14;
	setAttr -l on -k on ".tzInitVal" 1.340595996300771e-14;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "footR_jnt" -p "legR_jnt";
	rename -uid "A163E0FA-41CA-C170-B614-AE8BCD4274D0";
	addAttr -is true -ci true -k true -sn "heel_L_PivCtrl_GuideLoc_TRX" -ln "heel_L_PivCtrl_GuideLoc_TRX" 
		-smn 10.000244600072936 -smx 10.000244600072936 -at "double";
	addAttr -is true -ci true -k true -sn "heel_L_PivCtrl_GuideLoc_TRY" -ln "heel_L_PivCtrl_GuideLoc_TRY" 
		-smn 1.4033219031261979e-13 -smx 1.4033219031261979e-13 -at "double";
	addAttr -is true -ci true -k true -sn "heel_L_PivCtrl_GuideLoc_TRZ" -ln "heel_L_PivCtrl_GuideLoc_TRZ" 
		-smn -5.183256692159353 -smx -5.183256692159353 -at "double";
	addAttr -is true -ci true -k true -sn "toe_L_PivCtrl_GuideLoc_TRX" -ln "toe_L_PivCtrl_GuideLoc_TRX" 
		-smn 10.000244600072936 -smx 10.000244600072936 -at "double";
	addAttr -is true -ci true -k true -sn "toe_L_PivCtrl_GuideLoc_TRY" -ln "toe_L_PivCtrl_GuideLoc_TRY" 
		-smn 1.5987211554602254e-13 -smx 1.5987211554602254e-13 -at "double";
	addAttr -is true -ci true -k true -sn "toe_L_PivCtrl_GuideLoc_TRZ" -ln "toe_L_PivCtrl_GuideLoc_TRZ" 
		-smn 21.488872948701733 -smx 21.488872948701733 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_APivCtrl_GuideLoc_TRX" -ln "foot_L_APivCtrl_GuideLoc_TRX" 
		-smn 15.016302728475429 -smx 15.016302728475429 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_APivCtrl_GuideLoc_TRY" -ln "foot_L_APivCtrl_GuideLoc_TRY" 
		-smn 2.5401902803423582e-13 -smx 2.5401902803423582e-13 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_APivCtrl_GuideLoc_TRZ" -ln "foot_L_APivCtrl_GuideLoc_TRZ" 
		-smn 12.320301751885857 -smx 12.320301751885857 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_BPivCtrl_GuideLoc_TRX" -ln "foot_L_BPivCtrl_GuideLoc_TRX" 
		-smn 5.8441362554520202 -smx 5.8441362554520202 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_BPivCtrl_GuideLoc_TRY" -ln "foot_L_BPivCtrl_GuideLoc_TRY" 
		-smn 8.8817841970012523e-14 -smx 8.8817841970012523e-14 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_BPivCtrl_GuideLoc_TRZ" -ln "foot_L_BPivCtrl_GuideLoc_TRZ" 
		-smn 12.32030175188588 -smx 12.32030175188588 -at "double";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 41.499999999996149 
		-smx 41.499999999996149 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn -5.737632591262809e-13 
		-smx -5.737632591262809e-13 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 4 -smx 4 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 54.118398 
		-smx 54.118398 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -k true -sn "bend_twist_angle" -ln "bend_twist_angle" 
		-at "double3" -nc 3;
	addAttr -is true -ci true -sn "bend_twist_angle0" -ln "bend_twist_angle0" -at "double" 
		-p "bend_twist_angle";
	addAttr -is true -ci true -sn "bend_twist_angle1" -ln "bend_twist_angle1" -at "double" 
		-p "bend_twist_angle";
	addAttr -is true -ci true -sn "bend_twist_angle2" -ln "bend_twist_angle2" -at "double" 
		-p "bend_twist_angle";
	addAttr -is true -ci true -k true -sn "twist_bend_angle" -ln "twist_bend_angle" 
		-at "double3" -nc 3;
	addAttr -is true -ci true -sn "twist_bend_angle0" -ln "twist_bend_angle0" -at "double" 
		-p "twist_bend_angle";
	addAttr -is true -ci true -sn "twist_bend_angle1" -ln "twist_bend_angle1" -at "double" 
		-p "twist_bend_angle";
	addAttr -is true -ci true -sn "twist_bend_angle2" -ln "twist_bend_angle2" -at "double" 
		-p "twist_bend_angle";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 46.299999237060547 -5.3290705182007514e-15 8.7418186013099586e-05 ;
	setAttr ".r" -type "double3" 0 1.272221872585407e-14 0 ;
	setAttr ".jo" -type "double3" 0 -59.999981597503286 0 ;
	setAttr ".bps" -type "matrix" 1.1102236422502511e-16 -0.50000027815361459 0.86602524319231466 0
		 1 2.2204460492503131e-16 0 0 -1.9229623297974167e-16 0.86602524319231466 0.50000027815361459 0
		 -10.499999999999986 10.600006006658077 -1.6999126294977032 1;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRX" 10.000244600072936;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRY" 1.4033219031261979e-13;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRZ" -5.183256692159353;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRX" 10.000244600072936;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRY" 1.5987211554602254e-13;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRZ" 21.488872948701733;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRX" 15.016302728475429;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRY" 2.5401902803423582e-13;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRZ" 12.320301751885857;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRX" 5.8441362554520202;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRY" 8.8817841970012523e-14;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRZ" 12.32030175188588;
	setAttr -l on -k on ".txInitVal" 41.499999999996149;
	setAttr -l on -k on ".tyInitVal" -5.737632591262809e-13;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" 4;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 54.118398;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
	setAttr -k on ".bend_twist_angle";
	setAttr -k on ".bend_twist_angle0";
	setAttr -k on ".bend_twist_angle1";
	setAttr -k on ".bend_twist_angle2";
	setAttr -k on ".twist_bend_angle";
	setAttr -k on ".twist_bend_angle0";
	setAttr -k on ".twist_bend_angle1";
	setAttr -k on ".twist_bend_angle2";
createNode joint -n "toebaseR_jnt" -p "footR_jnt";
	rename -uid "978F4368-4C58-A156-DC13-90ADFBFC3633";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 17.408615 
		-smx 17.408615 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 35.881602 
		-smx 35.881602 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 15.699987411499027 1.5720758028692217e-12 -1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" 0 -6.361109362927032e-15 0 ;
	setAttr ".jo" -type "double3" 0 -29.999999999999996 0 ;
	setAttr ".bps" -type "matrix" 7.1317209568116258e-23 -3.2118415843607195e-07 0.99999999999994826 0
		 1 2.2204460492503131e-16 0 0 -2.2204460492501982e-16 0.99999999999994826 3.2118415843607195e-07 0
		 -10.499999999998417 2.7500079339003145 11.896672786662016 1;
	setAttr -l on -k on ".txInitVal" 17.408615;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 35.881602;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "uplegL_jnt" -p "hip_jnt";
	rename -uid "98DD546B-4A82-CC01-1950-23A0384D5101";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn -10.500000000000014 
		-smx -10.500000000000014 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 10 -smx 10 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn -4 -smx -4 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 179.99999999999983 
		-smx 179.99999999999983 -at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 7.8000001907348491 10.499999999999998 -1.7000000476837156 ;
	setAttr ".r" -type "double3" 5.1805298740776707e-20 -5.7892608326792172e-19 1.2722218725854067e-14 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 10.500000000000002 95.500001333653927 -1.7000000476837158 1;
	setAttr -l on -k on ".txInitVal" -10.500000000000014;
	setAttr -l on -k on ".tyInitVal" 10;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" -4;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal" 179.99999999999983;
	setAttr -k on ".liw";
createNode joint -n "legL_jnt" -p "uplegL_jnt";
	rename -uid "D4C23FC4-44F8-E278-7C6F-1BA9343A20AD";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 41.999999999999865 
		-smx 41.999999999999865 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 5.1514348342607263e-14 
		-smx 5.1514348342607263e-14 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 1.340595996300771e-14 
		-smx 1.340595996300771e-14 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 38.599998474121101 0.00021103328617755324 3.3306690738754696e-14 ;
	setAttr ".r" -type "double3" -1.6442988222135227e-40 -1.9412602221009154e-19 9.7062085441803699e-20 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 10.500211033286188 56.900002859532833 -1.7000000476836825 1;
	setAttr -l on -k on ".txInitVal" 41.999999999999865;
	setAttr -l on -k on ".tyInitVal" 5.1514348342607263e-14;
	setAttr -l on -k on ".tzInitVal" 1.340595996300771e-14;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "footL_jnt" -p "legL_jnt";
	rename -uid "747AAD9D-4F38-AC87-7269-BF84F30523DF";
	addAttr -is true -ci true -k true -sn "heel_L_PivCtrl_GuideLoc_TRX" -ln "heel_L_PivCtrl_GuideLoc_TRX" 
		-smn 10.000244600072936 -smx 10.000244600072936 -at "double";
	addAttr -is true -ci true -k true -sn "heel_L_PivCtrl_GuideLoc_TRY" -ln "heel_L_PivCtrl_GuideLoc_TRY" 
		-smn 1.4033219031261979e-13 -smx 1.4033219031261979e-13 -at "double";
	addAttr -is true -ci true -k true -sn "heel_L_PivCtrl_GuideLoc_TRZ" -ln "heel_L_PivCtrl_GuideLoc_TRZ" 
		-smn -5.183256692159353 -smx -5.183256692159353 -at "double";
	addAttr -is true -ci true -k true -sn "toe_L_PivCtrl_GuideLoc_TRX" -ln "toe_L_PivCtrl_GuideLoc_TRX" 
		-smn 10.000244600072936 -smx 10.000244600072936 -at "double";
	addAttr -is true -ci true -k true -sn "toe_L_PivCtrl_GuideLoc_TRY" -ln "toe_L_PivCtrl_GuideLoc_TRY" 
		-smn 1.5987211554602254e-13 -smx 1.5987211554602254e-13 -at "double";
	addAttr -is true -ci true -k true -sn "toe_L_PivCtrl_GuideLoc_TRZ" -ln "toe_L_PivCtrl_GuideLoc_TRZ" 
		-smn 21.488872948701733 -smx 21.488872948701733 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_APivCtrl_GuideLoc_TRX" -ln "foot_L_APivCtrl_GuideLoc_TRX" 
		-smn 15.016302728475429 -smx 15.016302728475429 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_APivCtrl_GuideLoc_TRY" -ln "foot_L_APivCtrl_GuideLoc_TRY" 
		-smn 2.5401902803423582e-13 -smx 2.5401902803423582e-13 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_APivCtrl_GuideLoc_TRZ" -ln "foot_L_APivCtrl_GuideLoc_TRZ" 
		-smn 12.320301751885857 -smx 12.320301751885857 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_BPivCtrl_GuideLoc_TRX" -ln "foot_L_BPivCtrl_GuideLoc_TRX" 
		-smn 5.8441362554520202 -smx 5.8441362554520202 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_BPivCtrl_GuideLoc_TRY" -ln "foot_L_BPivCtrl_GuideLoc_TRY" 
		-smn 8.8817841970012523e-14 -smx 8.8817841970012523e-14 -at "double";
	addAttr -is true -ci true -k true -sn "foot_L_BPivCtrl_GuideLoc_TRZ" -ln "foot_L_BPivCtrl_GuideLoc_TRZ" 
		-smn 12.32030175188588 -smx 12.32030175188588 -at "double";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 41.499999999996149 
		-smx 41.499999999996149 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn -5.737632591262809e-13 
		-smx -5.737632591262809e-13 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 4 -smx 4 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 54.118398 
		-smx 54.118398 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -k true -sn "bend_twist_angle" -ln "bend_twist_angle" 
		-at "double3" -nc 3;
	addAttr -is true -ci true -sn "bend_twist_angle0" -ln "bend_twist_angle0" -at "double" 
		-p "bend_twist_angle";
	addAttr -is true -ci true -sn "bend_twist_angle1" -ln "bend_twist_angle1" -at "double" 
		-p "bend_twist_angle";
	addAttr -is true -ci true -sn "bend_twist_angle2" -ln "bend_twist_angle2" -at "double" 
		-p "bend_twist_angle";
	addAttr -is true -ci true -k true -sn "twist_bend_angle" -ln "twist_bend_angle" 
		-at "double3" -nc 3;
	addAttr -is true -ci true -sn "twist_bend_angle0" -ln "twist_bend_angle0" -at "double" 
		-p "twist_bend_angle";
	addAttr -is true -ci true -sn "twist_bend_angle1" -ln "twist_bend_angle1" -at "double" 
		-p "twist_bend_angle";
	addAttr -is true -ci true -sn "twist_bend_angle2" -ln "twist_bend_angle2" -at "double" 
		-p "twist_bend_angle";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 46.299999237060547 0.00025296214153236463 8.696973236554939e-05 ;
	setAttr ".r" -type "double3" 4.8531412986198681e-20 1.272221872590035e-14 -1.2132853246549664e-20 ;
	setAttr ".jo" -type "double3" 0 -59.999999999999986 0.00031323510035946231 ;
	setAttr ".bps" -type "matrix" 2.7334919171411521e-06 -0.49999999999252831 0.8660254037844386 0
		 0.99999999998505607 5.4669838342823025e-06 4.2351647362715026e-22 0 -4.7345468825673289e-06 0.86602540377149673 0.50000000000000022 0
		 10.500463995427729 10.600003622472286 -1.6999130779513174 1;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRX" 10.000244600072936;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRY" 1.4033219031261979e-13;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRZ" -5.183256692159353;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRX" 10.000244600072936;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRY" 1.5987211554602254e-13;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRZ" 21.488872948701733;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRX" 15.016302728475429;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRY" 2.5401902803423582e-13;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRZ" 12.320301751885857;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRX" 5.8441362554520202;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRY" 8.8817841970012523e-14;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRZ" 12.32030175188588;
	setAttr -l on -k on ".txInitVal" 41.499999999996149;
	setAttr -l on -k on ".tyInitVal" -5.737632591262809e-13;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" 4;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 54.118398;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
	setAttr -k on ".bend_twist_angle";
	setAttr -k on ".bend_twist_angle0";
	setAttr -k on ".bend_twist_angle1";
	setAttr -k on ".bend_twist_angle2";
	setAttr -k on ".twist_bend_angle";
	setAttr -k on ".twist_bend_angle0";
	setAttr -k on ".twist_bend_angle1";
	setAttr -k on ".twist_bend_angle2";
createNode joint -n "toebaseL_jnt" -p "footL_jnt";
	rename -uid "135454AD-4B05-491C-AFE7-0293D52ED6C2";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 17.408615 
		-smx 17.408615 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 35.881602 
		-smx 35.881602 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 15.699999809265135 5.3290705182007514e-15 5.3290705182007514e-15 ;
	setAttr ".r" -type "double3" 3.0670042365060381e-20 -3.8166656177562201e-14 2.5554435383223469e-10 ;
	setAttr ".jo" -type "double3" 0 -29.999999999999996 0 ;
	setAttr ".bps" -type "matrix" 1.6940658945086007e-21 -3.8857805861880479e-16 1 0
		 0.99999999998505607 5.4669838342823025e-06 4.2351647362715026e-22 0 -5.4669838342823025e-06 0.99999999998505618 2.7755575615628914e-16 0
		 10.50050691125031 2.7500037179570285 11.896685596283136 1;
	setAttr -l on -k on ".txInitVal" 17.408615;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 35.881602;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "spine_01_jnt" -p "cog_jnt";
	rename -uid "5137F120-44A3-A731-D28A-FCA7D584614A";
	addAttr -is true -ci true -k true -sn "TypeID" -ln "TypeID" -dt "string";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn -3.5527136788005009e-13 
		-smx -3.5527136788005009e-13 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn -7.0064923216240854e-46 
		-smx -7.0064923216240854e-46 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 2.0779561154552755e-17 0.10000000149010191 0 ;
	setAttr ".jo" -type "double3" 0 0 90.000000000000028 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 2.0779561154552755e-17 103.50000152736902 0 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineA";
	setAttr -l on -k on ".txInitVal" -3.5527136788005009e-13;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" -7.0064923216240854e-46;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "spine_02_jnt" -p "spine_01_jnt";
	rename -uid "46DF775C-44E6-EF50-80EA-4086EC2094DE";
	addAttr -is true -ci true -k true -sn "TypeID" -ln "TypeID" -dt "string";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 12.314499999999981 
		-smx 12.314499999999981 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 6.3108872417680944e-29 
		-smx 6.3108872417680944e-29 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn -7.0064923216240854e-46 
		-smx -7.0064923216240854e-46 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn -5.5 -smx 
		-5.5 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 15.400139808654771 -7.6744361394785503e-17 0 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -6.7415119966566535e-15 118.90014133602381 0 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineB";
	setAttr -l on -k on ".txInitVal" 12.314499999999981;
	setAttr -l on -k on ".tyInitVal" 6.3108872417680944e-29;
	setAttr -l on -k on ".tzInitVal" -7.0064923216240854e-46;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" -5.5;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "spine_03_jnt" -p "spine_02_jnt";
	rename -uid "D87356B0-4E59-C567-81F3-E099BE9A86FA";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 12.102500000000191 
		-smx 12.102500000000191 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn -5.9953428796796897e-29 
		-smx -5.9953428796796897e-29 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 1.7763568394002503e-15 
		-smx 1.7763568394002503e-15 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 1.4124500153760508e-30 
		-smx 1.4124500153760508e-30 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn -7.2786214345459537e-32 
		-smx -7.2786214345459537e-32 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 6.3611093629270304e-15 
		-smx 6.3611093629270304e-15 -at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 15.00000476837161 1.0117624515970647e-09 -0.00012308963050600141 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -1.0117758544493267e-09 133.90014610439539 -0.00012308963050600141 1;
	setAttr -l on -k on ".txInitVal" 12.102500000000191;
	setAttr -l on -k on ".tyInitVal" -5.9953428796796897e-29;
	setAttr -l on -k on ".tzInitVal" 1.7763568394002503e-15;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" 1.4124500153760508e-30;
	setAttr -l on -k on ".jyInitVal" -7.2786214345459537e-32;
	setAttr -l on -k on ".jzInitVal" 6.3611093629270304e-15;
	setAttr -k on ".liw";
createNode joint -n "neck_jnt" -p "spine_03_jnt";
	rename -uid "0E415622-4746-80EF-1F0B-AAAC1377E625";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 21.483000000000089 
		-smx 21.483000000000089 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn -2.2088105346188331e-29 
		-smx -2.2088105346188331e-29 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn -2.0744933548755293e-15 
		-smx -2.0744933548755293e-15 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 1.4433913741954447e-29 
		-smx 1.4433913741954447e-29 -at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 24.000000000000004 
		-smx 24.000000000000004 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 6.5048988568370912e-29 
		-smx 6.5048988568370912e-29 -at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 15.800000190734863 1.0825219609600367e-09 -0.00013169858721084893 ;
	setAttr ".pa" -type "double3" 1.4433913741954447e-29 0 6.5048988568370912e-29 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -2.0943048320189637e-09 149.70014629513025 -0.00025478821771685034 1;
	setAttr -l on -k on ".txInitVal" 21.483000000000089;
	setAttr -l on -k on ".tyInitVal" -2.2088105346188331e-29;
	setAttr -l on -k on ".tzInitVal" -2.0744933548755293e-15;
	setAttr -l on -k on ".rxInitVal" 1.4433913741954447e-29;
	setAttr -l on -k on ".ryInitVal" 24.000000000000004;
	setAttr -l on -k on ".rzInitVal" 6.5048988568370912e-29;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "head_jnt" -p "neck_jnt";
	rename -uid "C23B7B83-4CC5-5B52-938B-1B9674B62AE6";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 11.5 -smx 
		11.5 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 3.1554436208840472e-30 
		-smx 3.1554436208840472e-30 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn -18.5 -smx 
		-18.5 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 16.799999237060547 1.1354432949417514e-09 -0.00013813351688440889 ;
	setAttr ".bps" -type "matrix" -4.4408920985006262e-16 1 0 0 -1 -4.4408920985006262e-16 0 0
		 0 0 1 0 -3.2297555876591018e-09 166.5001455321908 -0.00039292173460125923 1;
	setAttr -l on -k on ".txInitVal" 11.5;
	setAttr -l on -k on ".tyInitVal" 3.1554436208840472e-30;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" -18.5;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "shoulderL_jnt" -p "spine_03_jnt";
	rename -uid "70F2A709-4C88-A1E8-1875-53880BE574D3";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 18.151584018760246 
		-smx 18.151584018760246 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 3.5165270660160961 
		-smx 3.5165270660160961 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 2.4842249701844956 
		-smx 2.4842249701844956 -at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0.23229819789589176 
		-smx 0.23229819789589176 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn -17.669713662365165 
		-smx -17.669713662365165 -at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -179.99999999999997 
		-smx -179.99999999999997 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn -8.13 -smx 
		-8.13 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 90.000000000001606 
		-smx 90.000000000001606 -at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 11.699999809265137 -2.7000000476837158 -0.00012347938900347799 ;
	setAttr ".r" -type "double3" 0 9.7062825972397362e-20 0 ;
	setAttr ".jo" -type "double3" 0 0.0004709569395787377 -90.000000000000028 ;
	setAttr ".bps" -type "matrix" 0.99999999996621791 -1.5002260872653745e-26 -8.2197492306724107e-06 0
		 0 1 0 0 8.2197492306724107e-06 -5.8486279525653077e-22 0.99999999996621791 0 2.7000000466719345 145.60014591366053 -0.0002465690195094794 1;
	setAttr -l on -k on ".txInitVal" 18.151584018760246;
	setAttr -l on -k on ".tyInitVal" 3.5165270660160961;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal" 2.4842249701844956;
	setAttr -l on -k on ".ryInitVal" 0.23229819789589176;
	setAttr -l on -k on ".rzInitVal" -17.669713662365165;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -179.99999999999997;
	setAttr -l on -k on ".jyInitVal" -8.13;
	setAttr -l on -k on ".jzInitVal" 90.000000000001606;
	setAttr -k on ".liw";
createNode joint -n "armL_jnt" -p "shoulderL_jnt";
	rename -uid "6CDC8CC8-45BF-6390-0B61-098BEA8BE3EE";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 18.016798560432804 
		-smx 18.016798560432804 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn -1.7763568394002505e-15 
		-smx -1.7763568394002505e-15 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 3.9295766422768144 
		-smx 3.9295766422768144 -at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 4.1369394875594834 
		-smx 4.1369394875594834 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn -27.157050437318002 
		-smx -27.157050437318002 -at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn -8.13 -smx 
		-8.13 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 14.300000190734862 -1.1368683772161603e-13 -5.4210108624275222e-20 ;
	setAttr ".r" -type "double3" 0 9.7062825972397362e-20 0 ;
	setAttr ".bps" -type "matrix" 0.7071067811626599 -0.70710678118654757 -5.8122404206613681e-06 0
		 0.70710678116266001 0.70710678118654746 -5.8122404206613689e-06 0 8.2197492306724107e-06 -5.8486279525653077e-22 0.99999999996621791 0
		 17.000000236923714 145.60014591366053 -0.00036411143507588761 1;
	setAttr -l on -k on ".txInitVal" 18.016798560432804;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" -1.7763568394002505e-15;
	setAttr -l on -k on ".rxInitVal" 3.9295766422768144;
	setAttr -l on -k on ".ryInitVal" 4.1369394875594834;
	setAttr -l on -k on ".rzInitVal" -27.157050437318002;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" -8.13;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "forearmL_jnt" -p "armL_jnt";
	rename -uid "9E3EBF00-4807-EEA2-FC4A-84AFD26527F1";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 27.349999999997255 
		-smx 27.349999999997255 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 27.299999237060547 2.8421709430404007e-14 -5.4210108624275222e-20 ;
	setAttr ".r" -type "double3" 0 9.7062825972397362e-20 0 ;
	setAttr ".bps" -type "matrix" 0.7071067811626599 -0.70710678118654757 -5.8122404206613681e-06 0
		 0.70710678116266001 0.70710678118654746 -5.8122404206613689e-06 0 8.2197492306724107e-06 -5.8486279525653077e-22 0.99999999996621791 0
		 36.304014823184673 126.29613132674744 -0.00052278559412555561 1;
	setAttr -l on -k on ".txInitVal" 27.349999999997255;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "handL_jnt" -p "forearmL_jnt";
	rename -uid "9AF1DDFE-4830-F6A1-A0A4-C9A77BB497A3";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 28.200000002904758 
		-smx 28.200000002904758 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -89.999999984260256 
		-smx -89.999999984260256 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 25.79999923706054 -2.8421709430404007e-14 -1.6263032587282567e-19 ;
	setAttr ".r" -type "double3" 0 9.7062825972397362e-20 0 ;
	setAttr ".bps" -type "matrix" 0.7071067811626599 -0.70710678118654757 -5.8122404206613681e-06 0
		 0.70710678116266001 0.70710678118654746 -5.8122404206613689e-06 0 8.2197492306724107e-06 -5.8486279525653077e-22 0.99999999996621791 0
		 54.547369237701645 108.05277691161419 -0.00067274139254423152 1;
	setAttr -l on -k on ".txInitVal" 28.200000002904758;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -89.999999984260256;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "handWeaponL_offset_jnt" -p "handL_jnt";
	rename -uid "12A0903A-473B-7C68-1581-978239A72AC9";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 28.200000002904758 
		-smx 28.200000002904758 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -89.999999984260256 
		-smx -89.999999984260256 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 7.3000001907348633 -2.4000000953674316 9.5287818434319771e-14 ;
	setAttr ".r" -type "double3" 0 9.7062825972397362e-20 0 ;
	setAttr ".bps" -type "matrix" 0.7071067811626599 -0.70710678118654757 -5.8122404206613681e-06 0
		 0.70710678116266001 0.70710678118654746 -5.8122404206613689e-06 0 8.2197492306724107e-06 -5.8486279525653077e-22 0.99999999996621791 0
		 58.012192532833637 101.1938409317998 -0.00070122137106448266 1;
	setAttr -l on -k on ".txInitVal" 28.200000002904758;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -89.999999984260256;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
createNode joint -n "handWeaponL_bind_jnt" -p "handWeaponL_offset_jnt";
	rename -uid "8DA9E666-48B8-1B6D-4578-1BA19BD07146";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 28.200000002904758 
		-smx 28.200000002904758 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -89.999999984260256 
		-smx -89.999999984260256 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 4.2632564145606011e-14 0 8.5337552996334054e-16 ;
	setAttr ".r" -type "double3" 0 9.7062825972397362e-20 0 ;
	setAttr ".bps" -type "matrix" 0.7071067811626599 -0.70710678118654757 -5.8122404206613681e-06 0
		 0.70710678116266001 0.70710678118654746 -5.8122404206613689e-06 0 8.2197492306724107e-06 -5.8486279525653077e-22 0.99999999996621791 0
		 58.012192532833666 101.19384093179978 -0.00070122137106362972 1;
	setAttr -l on -k on ".txInitVal" 28.200000002904758;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -89.999999984260256;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
createNode joint -n "shoulderR_jnt" -p "spine_03_jnt";
	rename -uid "9743D9EC-4617-200C-AD9C-72ADBDA1C153";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 18.151584018760246 
		-smx 18.151584018760246 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 3.5165270660160961 
		-smx 3.5165270660160961 -at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 2.4842249701844956 
		-smx 2.4842249701844956 -at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0.23229819789589176 
		-smx 0.23229819789589176 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn -17.669713662365165 
		-smx -17.669713662365165 -at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -179.99999999999997 
		-smx -179.99999999999997 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn -8.13 -smx 
		-8.13 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 90.000000000001606 
		-smx 90.000000000001606 -at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 11.699856758117647 2.7000000476837158 -7.9091507359407842e-05 ;
	setAttr ".r" -type "double3" 3.0968865254753111e-15 -7.0168172837835639e-15 -1.9083299250668456e-14 ;
	setAttr ".jo" -type "double3" 0.00047095700986203728 0 89.999999999999986 ;
	setAttr ".bps" -type "matrix" -1 -2.2204460492503131e-16 0 0 2.2204460491002905e-16 -0.99999999996621791 8.2197504573473951e-06 0
		 -2.8032695385137959e-21 8.2197504573473968e-06 0.9999999999662178 0 -2.7000000486954971 145.60000286251307 -0.00020218113786540926 1;
	setAttr -l on -k on ".txInitVal" 18.151584018760246;
	setAttr -l on -k on ".tyInitVal" 3.5165270660160961;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal" 2.4842249701844956;
	setAttr -l on -k on ".ryInitVal" 0.23229819789589176;
	setAttr -l on -k on ".rzInitVal" -17.669713662365165;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -179.99999999999997;
	setAttr -l on -k on ".jyInitVal" -8.13;
	setAttr -l on -k on ".jzInitVal" 90.000000000001606;
	setAttr -k on ".liw";
createNode joint -n "armR_jnt" -p "shoulderR_jnt";
	rename -uid "6A91AFFE-49CD-6616-524C-FCA89BE86C00";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 18.016798560432804 
		-smx 18.016798560432804 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn -1.7763568394002505e-15 
		-smx -1.7763568394002505e-15 -at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 3.9295766422768144 
		-smx 3.9295766422768144 -at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 4.1369394875594834 
		-smx 4.1369394875594834 -at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn -27.157050437318002 
		-smx -27.157050437318002 -at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn -8.13 -smx 
		-8.13 -at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 14.30000019073486 2.5579538487363607e-13 -1.7347234759768071e-18 ;
	setAttr ".r" -type "double3" 6.7434398344323055e-15 1.1059377021502992e-20 1.2326083877484378e-15 ;
	setAttr ".bps" -type "matrix" -0.70710678118654735 -0.70710678116266013 5.8122412880515689e-06 0
		 0.70710678118654768 -0.70710678116265979 5.8122412880515681e-06 0 -2.8032695385137959e-21 8.2197504573473968e-06 0.9999999999662178 0
		 -17.00000023943036 145.60000286251292 -0.00020218113786540939 1;
	setAttr -l on -k on ".txInitVal" 18.016798560432804;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" -1.7763568394002505e-15;
	setAttr -l on -k on ".rxInitVal" 3.9295766422768144;
	setAttr -l on -k on ".ryInitVal" 4.1369394875594834;
	setAttr -l on -k on ".rzInitVal" -27.157050437318002;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" -8.13;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "forearmR_jnt" -p "armR_jnt";
	rename -uid "08CA5D84-4257-EBB9-3B3D-3795107535BF";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 27.349999999997255 
		-smx 27.349999999997255 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 27.299978256225582 0 -2.4839071771642907e-15 ;
	setAttr ".r" -type "double3" 8.6949850134333284e-15 1.6188461608924121e-20 1.8035122365398687e-15 ;
	setAttr ".bps" -type "matrix" -0.70710678118654735 -0.70710678116266013 5.8122412880515689e-06 0
		 0.70710678118654768 -0.70710678116265979 5.8122412880515681e-06 0 -2.8032695385137959e-21 8.2197504573473968e-06 0.9999999999662178 0
		 -36.30399999065277 126.29600311194264 -4.3507077084148799e-05 1;
	setAttr -l on -k on ".txInitVal" 27.349999999997255;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "handR_jnt" -p "forearmR_jnt";
	rename -uid "4655A4A8-44A5-6A19-C4B8-12B460479378";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 28.200000002904758 
		-smx 28.200000002904758 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -89.999999984260256 
		-smx -89.999999984260256 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 25.799999237060526 -7.0710681029595435e-05 3.9872619095326911e-15 ;
	setAttr ".r" -type "double3" -3.3422613495335301e-15 -7.0169485828579673e-15 -1.3802959962022948e-14 ;
	setAttr ".jo" -type "double3" 0.00047465856352600183 0 0 ;
	setAttr ".bps" -type "matrix" -0.70710678118654735 -0.70710678116266013 5.8122412880515689e-06 0
		 0.7071067811622832 -0.70710678107030001 1.4096596043792895e-05 0 -5.8579234258786451e-06 1.4077673882746081e-05 0.99999999988375188 0
		 -54.547404405788086 108.05269869742773 0.00010644833272964089 1;
	setAttr -l on -k on ".txInitVal" 28.200000002904758;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -89.999999984260256;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".liw";
createNode joint -n "handWeaponR_offset_jnt" -p "handR_jnt";
	rename -uid "69C8BA84-413A-9AB0-BE38-C7B4E66CA3FD";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 28.200000002904758 
		-smx 28.200000002904758 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -89.999999984260256 
		-smx -89.999999984260256 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 7.2997465133667134 2.4000000953673748 3.6628686195250282e-15 ;
	setAttr ".r" -type "double3" -1.4181962066126464e-35 -1.4033418596114129e-14 1.1580450850781008e-19 ;
	setAttr ".bps" -type "matrix" -0.70710678118654735 -0.70710678116266013 5.8122412880515689e-06 0
		 0.7071067811622832 -0.70710678107030001 1.4096596043792895e-05 0 -5.8579234258786451e-06 1.4077673882746081e-05 0.99999999988375188 0
		 -58.0120483241081 101.19394209505397 0.00018270805266006328 1;
	setAttr -l on -k on ".txInitVal" 28.200000002904758;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -89.999999984260256;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
createNode joint -n "handWeaponR_bind_jnt" -p "handWeaponR_offset_jnt";
	rename -uid "DD304EFA-450B-13C9-4163-999BA8CA5119";
	addAttr -is true -ci true -k true -sn "txInitVal" -ln "txInitVal" -smn 28.200000002904758 
		-smx 28.200000002904758 -at "double";
	addAttr -is true -ci true -k true -sn "tyInitVal" -ln "tyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "tzInitVal" -ln "tzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rxInitVal" -ln "rxInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "ryInitVal" -ln "ryInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "rzInitVal" -ln "rzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "sxInitVal" -ln "sxInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "syInitVal" -ln "syInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "szInitVal" -ln "szInitVal" -smn 1 -smx 1 
		-at "double";
	addAttr -is true -ci true -k true -sn "jxInitVal" -ln "jxInitVal" -smn -89.999999984260256 
		-smx -89.999999984260256 -at "double";
	addAttr -is true -ci true -k true -sn "jyInitVal" -ln "jyInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "jzInitVal" -ln "jzInitVal" -smn 0 -smx 0 
		-at "double";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.4210854715202004e-14 -2.8421709430404007e-14 -8.6736173798840355e-19 ;
	setAttr ".r" -type "double3" 7.0437757383509378e-15 -6.402029319687168e-14 -2.5808916329094227e-09 ;
	setAttr ".jo" -type "double3" 0.0004756355705899373 0.00015637876761293482 0 ;
	setAttr ".bps" -type "matrix" -0.70710678116792547 -0.70710678119844894 3.082916913293801e-06 0
		 0.70710678107326863 -0.70710678094509205 2.2398002788743891e-05 0 -1.3657828202742216e-05 1.8017731111414428e-05 0.99999999974441256 0
		 -58.0120483241081 101.19394209505398 0.00018270805266006193 1;
	setAttr -l on -k on ".txInitVal" 28.200000002904758;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -89.999999984260256;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "E5975FD6-4306-F5A8-325C-7AAE43A1B05B";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "609267F7-47BF-D584-E8AC-85A5876D7333";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "D9CDAEC6-4AFF-5231-BE07-2BB8467A930C";
createNode displayLayerManager -n "layerManager";
	rename -uid "7090F9A0-445B-597F-04C4-EFBA9F0E0256";
	setAttr ".cdl" 1;
	setAttr -s 3 ".dli[1:2]"  1 2;
createNode displayLayer -n "defaultLayer";
	rename -uid "C0B07420-455F-8E7F-4F7F-09A0C39D331F";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "FA9E59E3-4E46-AEF7-6377-9DB093A17376";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "FEAF4369-4446-39FE-EC9C-9BA7F3C5291B";
	setAttr ".g" yes;
createNode shapeEditorManager -n "shapeEditorManager1";
	rename -uid "2BFA72E7-45F9-B310-2892-BA90FD990E95";
createNode poseInterpolatorManager -n "poseInterpolatorManager1";
	rename -uid "4C20FC49-4FB1-6694-05D7-FC88F7457766";
createNode renderLayerManager -n "renderLayerManager1";
	rename -uid "8DDCEEDF-4749-96E8-F863-D7A1F2B12EC7";
createNode renderLayer -n "defaultRenderLayer1";
	rename -uid "238ABD8E-4CF2-941E-5B20-5B8897ECB21C";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "3893CDD9-445B-EA5F-C833-03A28AC55189";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode dagPose -n "bindPose11";
	rename -uid "DC5C4046-438E-8CE3-62A8-9D81DA647201";
	setAttr -s 27 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 29 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 103.40000152587891 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.5407439555097887e-33
		 -0.10000000149010191 3.0814879110195774e-33 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 -0.70710678118654746 0.70710678118654757 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 7.7999978065490723 -10.5
		 -1.7000000476837158 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 38.599998474121108 0 2.2204460492503131e-16 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 46.299999237060547 -7.1054273576010019e-15
		 8.7418186012655497e-05 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 -0.49999986092317339 0 0.86602548408046709 1
		 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 15.699987411499023 1.5631940186722204e-12
		 -1.7763568394002505e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 -0.25881904510252074 0 0.96592582628906831 1
		 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 7.8000001907348633 10.5
		 -1.7000000476837158 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 38.599998474121087 0.00021103328617932959
		 3.3084646133829665e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 46.299999237060554 0.00025296214153058827
		 8.6969732365105301e-05 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1.3667459585201702e-06 -0.49999999999813183 2.3672734411963607e-06 0.86602540378120318 1
		 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 0 0 0 0 15.69999980926514 5.3290705182007514e-15
		 7.1054273576010019e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 -0.25881904510252074 0 0.96592582628906831 1
		 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.0779561154552755e-17
		 0.10000000149011612 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0.70710678118654768 0.70710678118654735 1
		 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 0 0 0 0 15.400139808654785 -7.6744361394791814e-17
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 0 0 0 0 15.000004768371582 1.0117624515970647e-09
		 -0.00012308963050600141 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 0 0 0 0 15.800000190734863 1.0825219609600367e-09
		 -0.00013169858721084893 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 0 0 0 0 16.799999237060547 1.1354432949417514e-09
		 -0.00013813351688440889 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[17]" -type "matrix" "xform" 1 1 1 0 0 0 0 11.699999809265137 -2.7000000476837158
		 -0.00012347938900347799 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2.9061202103552285e-06 2.9061202103552272e-06 -0.70710678118057579 0.70710678118057546 1
		 1 1 yes;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 0 0 -0.78539816339744828 0 14.300000190734862
		 1.1368683772161603e-13 2.7105054312137611e-20 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 0 0 0 0 27.299999237060533 2.8421709430404007e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 0 0 0 0 25.799999237060582 -2.8421709430404007e-14
		 -8.1315162936412833e-20 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 0 0 0 0 7.3000001907348633 -2.4000000953674174
		 9.5288008169699956e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.1316282072803006e-14
		 1.4210854715202004e-14 8.5332131985471626e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 0 0 0 0 11.699856758117676 2.7000000476837158
		 -7.9091507359407842e-05 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2.9061206440503285e-06 2.9061206440503281e-06 0.70710678118057557 0.70710678118057568 1
		 1 1 yes;
	setAttr ".xm[24]" -type "matrix" "xform" 1 1 1 0 0 0.78539816339744828 0 14.300000190734863
		 1.4210854715202004e-13 -1.7347234759768071e-18 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 0 0 0 0 27.299978256225565 -1.4210854715202004e-14
		 -2.4834734962952965e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 0 0 0 0 25.799999237060575 -7.071068101538458e-05
		 3.987045069098194e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 4.1421773781458538e-06 0 0 0.9999999999914212 1
		 1 1 yes;
	setAttr ".xm[27]" -type "matrix" "xform" 1 1 1 0 0 0 0 7.2997465133666992 2.4000000953674174
		 3.6630854599595253e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[28]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.5527136788005009e-15
		 0 -1.0842021724855044e-18 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 4.1507033731823732e-06 1.3646621875162138e-06 -5.6643079450320544e-12 0.99999999999045464 1
		 1 1 yes;
	setAttr -s 27 ".m";
	setAttr -s 27 ".p";
	setAttr -s 29 ".g[0:28]" yes yes yes no no no no no no no no no no 
		no no no no no no no no yes no no no no no yes no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av -k on ".unw" 1;
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -av ".ta";
	setAttr -av ".tq";
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".hfd";
	setAttr -av ".hfs";
	setAttr -av ".hfe";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
	setAttr -s 2 ".r";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
	setAttr ".fs" 1;
	setAttr ".ef" 10;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -av -k off -cb on ".fbfm";
	setAttr -av -k off -cb on ".ehql";
	setAttr -av -k off -cb on ".eams";
	setAttr -av -k off -cb on ".eeaa";
	setAttr -av -k off -cb on ".engm";
	setAttr -av -k off -cb on ".mes";
	setAttr -av -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -av -k off -cb on ".mbs";
	setAttr -av -k off -cb on ".trm";
	setAttr -av -k off -cb on ".tshc";
	setAttr -av -k off -cb on ".enpt";
	setAttr -av -k off -cb on ".clmt";
	setAttr -av -k off -cb on ".tcov";
	setAttr -av -k off -cb on ".lith";
	setAttr -av -k off -cb on ".sobc";
	setAttr -av -k off -cb on ".cuth";
	setAttr -av -k off -cb on ".hgcd";
	setAttr -av -k off -cb on ".hgci";
	setAttr -av -k off -cb on ".mgcs";
	setAttr -av -k off -cb on ".twa";
	setAttr -av -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :ikSystem;
	setAttr -s 2 ".sol";
connectAttr "root_jnt.s" "cog_jnt.is";
connectAttr "cog_jnt.s" "hip_jnt.is";
connectAttr "hip_jnt.s" "uplegR_jnt.is";
connectAttr "uplegR_jnt.s" "legR_jnt.is";
connectAttr "legR_jnt.s" "footR_jnt.is";
connectAttr "footR_jnt.s" "toebaseR_jnt.is";
connectAttr "hip_jnt.s" "uplegL_jnt.is";
connectAttr "uplegL_jnt.s" "legL_jnt.is";
connectAttr "legL_jnt.s" "footL_jnt.is";
connectAttr "footL_jnt.s" "toebaseL_jnt.is";
connectAttr "cog_jnt.s" "spine_01_jnt.is";
connectAttr "spine_01_jnt.s" "spine_02_jnt.is";
connectAttr "spine_02_jnt.s" "spine_03_jnt.is";
connectAttr "spine_03_jnt.s" "neck_jnt.is";
connectAttr "neck_jnt.s" "head_jnt.is";
connectAttr "spine_03_jnt.s" "shoulderL_jnt.is";
connectAttr "shoulderL_jnt.s" "armL_jnt.is";
connectAttr "armL_jnt.s" "forearmL_jnt.is";
connectAttr "forearmL_jnt.s" "handL_jnt.is";
connectAttr "handL_jnt.s" "handWeaponL_offset_jnt.is";
connectAttr "handWeaponL_offset_jnt.s" "handWeaponL_bind_jnt.is";
connectAttr "spine_03_jnt.s" "shoulderR_jnt.is";
connectAttr "shoulderR_jnt.s" "armR_jnt.is";
connectAttr "armR_jnt.s" "forearmR_jnt.is";
connectAttr "forearmR_jnt.s" "handR_jnt.is";
connectAttr "handR_jnt.s" "handWeaponR_offset_jnt.is";
connectAttr "handWeaponR_offset_jnt.s" "handWeaponR_bind_jnt.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "renderLayerManager1.rlmi[0]" "defaultRenderLayer1.rlid";
connectAttr "root_jnt.msg" "bindPose11.m[1]";
connectAttr "cog_jnt.msg" "bindPose11.m[2]";
connectAttr "hip_jnt.msg" "bindPose11.m[3]";
connectAttr "uplegR_jnt.msg" "bindPose11.m[4]";
connectAttr "legR_jnt.msg" "bindPose11.m[5]";
connectAttr "footR_jnt.msg" "bindPose11.m[6]";
connectAttr "toebaseR_jnt.msg" "bindPose11.m[7]";
connectAttr "uplegL_jnt.msg" "bindPose11.m[8]";
connectAttr "legL_jnt.msg" "bindPose11.m[9]";
connectAttr "footL_jnt.msg" "bindPose11.m[10]";
connectAttr "toebaseL_jnt.msg" "bindPose11.m[11]";
connectAttr "spine_01_jnt.msg" "bindPose11.m[12]";
connectAttr "spine_02_jnt.msg" "bindPose11.m[13]";
connectAttr "spine_03_jnt.msg" "bindPose11.m[14]";
connectAttr "neck_jnt.msg" "bindPose11.m[15]";
connectAttr "head_jnt.msg" "bindPose11.m[16]";
connectAttr "shoulderL_jnt.msg" "bindPose11.m[17]";
connectAttr "armL_jnt.msg" "bindPose11.m[18]";
connectAttr "forearmL_jnt.msg" "bindPose11.m[19]";
connectAttr "handL_jnt.msg" "bindPose11.m[20]";
connectAttr "handWeaponL_offset_jnt.msg" "bindPose11.m[21]";
connectAttr "shoulderR_jnt.msg" "bindPose11.m[23]";
connectAttr "armR_jnt.msg" "bindPose11.m[24]";
connectAttr "forearmR_jnt.msg" "bindPose11.m[25]";
connectAttr "handR_jnt.msg" "bindPose11.m[26]";
connectAttr "handWeaponR_offset_jnt.msg" "bindPose11.m[27]";
connectAttr "bindPose11.w" "bindPose11.p[0]";
connectAttr "bindPose11.m[0]" "bindPose11.p[1]";
connectAttr "bindPose11.m[1]" "bindPose11.p[2]";
connectAttr "bindPose11.m[2]" "bindPose11.p[3]";
connectAttr "bindPose11.m[3]" "bindPose11.p[4]";
connectAttr "bindPose11.m[4]" "bindPose11.p[5]";
connectAttr "bindPose11.m[5]" "bindPose11.p[6]";
connectAttr "bindPose11.m[6]" "bindPose11.p[7]";
connectAttr "bindPose11.m[3]" "bindPose11.p[8]";
connectAttr "bindPose11.m[8]" "bindPose11.p[9]";
connectAttr "bindPose11.m[9]" "bindPose11.p[10]";
connectAttr "bindPose11.m[10]" "bindPose11.p[11]";
connectAttr "bindPose11.m[2]" "bindPose11.p[12]";
connectAttr "bindPose11.m[12]" "bindPose11.p[13]";
connectAttr "bindPose11.m[13]" "bindPose11.p[14]";
connectAttr "bindPose11.m[14]" "bindPose11.p[15]";
connectAttr "bindPose11.m[15]" "bindPose11.p[16]";
connectAttr "bindPose11.m[14]" "bindPose11.p[17]";
connectAttr "bindPose11.m[17]" "bindPose11.p[18]";
connectAttr "bindPose11.m[18]" "bindPose11.p[19]";
connectAttr "bindPose11.m[19]" "bindPose11.p[20]";
connectAttr "bindPose11.m[20]" "bindPose11.p[21]";
connectAttr "bindPose11.m[14]" "bindPose11.p[23]";
connectAttr "bindPose11.m[23]" "bindPose11.p[24]";
connectAttr "bindPose11.m[24]" "bindPose11.p[25]";
connectAttr "bindPose11.m[25]" "bindPose11.p[26]";
connectAttr "bindPose11.m[26]" "bindPose11.p[27]";
connectAttr "root_jnt.bps" "bindPose11.wm[1]";
connectAttr "cog_jnt.bps" "bindPose11.wm[2]";
connectAttr "hip_jnt.bps" "bindPose11.wm[3]";
connectAttr "uplegR_jnt.bps" "bindPose11.wm[4]";
connectAttr "legR_jnt.bps" "bindPose11.wm[5]";
connectAttr "footR_jnt.bps" "bindPose11.wm[6]";
connectAttr "toebaseR_jnt.bps" "bindPose11.wm[7]";
connectAttr "uplegL_jnt.bps" "bindPose11.wm[8]";
connectAttr "legL_jnt.bps" "bindPose11.wm[9]";
connectAttr "footL_jnt.bps" "bindPose11.wm[10]";
connectAttr "toebaseL_jnt.bps" "bindPose11.wm[11]";
connectAttr "spine_01_jnt.bps" "bindPose11.wm[12]";
connectAttr "spine_02_jnt.bps" "bindPose11.wm[13]";
connectAttr "spine_03_jnt.bps" "bindPose11.wm[14]";
connectAttr "neck_jnt.bps" "bindPose11.wm[15]";
connectAttr "head_jnt.bps" "bindPose11.wm[16]";
connectAttr "shoulderL_jnt.bps" "bindPose11.wm[17]";
connectAttr "armL_jnt.bps" "bindPose11.wm[18]";
connectAttr "forearmL_jnt.bps" "bindPose11.wm[19]";
connectAttr "handL_jnt.bps" "bindPose11.wm[20]";
connectAttr "handWeaponL_offset_jnt.bps" "bindPose11.wm[21]";
connectAttr "shoulderR_jnt.bps" "bindPose11.wm[23]";
connectAttr "armR_jnt.bps" "bindPose11.wm[24]";
connectAttr "forearmR_jnt.bps" "bindPose11.wm[25]";
connectAttr "handR_jnt.bps" "bindPose11.wm[26]";
connectAttr "handWeaponR_offset_jnt.bps" "bindPose11.wm[27]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "defaultRenderLayer1.msg" ":defaultRenderingList1.r" -na;
// End of joints.ma
