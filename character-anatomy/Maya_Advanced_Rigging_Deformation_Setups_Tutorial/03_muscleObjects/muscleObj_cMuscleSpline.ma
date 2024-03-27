//Maya ASCII 2017ff04 scene
//Name: muscleObj_cMuscleSpline.ma
//Last modified: Tue, Aug 01, 2017 10:56:57 AM
//Codeset: 1250
requires maya "2017ff04";
requires -nodeType "cMuscleObject" -nodeType "cMuscleSpline" -nodeType "cMuscleSplineDeformer"
		 "MayaMuscle" "2.00 (Build: 004)";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201702071345-1015190";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "718831AA-4B25-EBF7-9D9E-F1973034CAB4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 26.099552049085563 14.581026747769149 26.089394925124569 ;
	setAttr ".r" -type "double3" -23.138352729602655 44.200000000000543 -2.2182365887199775e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "0B49D963-42F2-431C-0B7E-E19E5153E510";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 39.577676177566822;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "D44882C9-47C1-F5B6-A9BA-FDAC0A2A6011";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "2BF2881A-41EF-26BB-BF22-7A9C234EFFA7";
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
	rename -uid "64189B94-4F61-7D90-07A2-319967610BF3";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "024A95F4-457E-361A-E0D4-8AA4268515A6";
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
	rename -uid "F06D866B-4166-AE73-02E9-5A8E10548588";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "5CB61403-4189-B636-CD7E-199A0156E5DE";
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
createNode transform -n "grpMUSCLES";
	rename -uid "1E148F1F-4D58-62FF-52C6-F98D9D87912F";
createNode transform -n "grpMuscleRIG" -p "grpMUSCLES";
	rename -uid "7D8879E5-49B8-E497-630D-70989AAE9299";
createNode transform -n "cMuscleSplineMuscle" -p "grpMuscleRIG";
	rename -uid "83611B57-4383-EEE9-B979-83BDD17B4E4B";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".it" no;
createNode cMuscleSpline -n "cMuscleSplineMuscleShape" -p "cMuscleSplineMuscle";
	rename -uid "117327AC-46E8-C108-08E4-AE993865EDE1";
	addAttr -ci true -k true -sn "curLen" -ln "curLen" -at "double";
	addAttr -ci true -k true -sn "pctSquash" -ln "pctSquash" -at "double";
	addAttr -ci true -k true -sn "pctStretch" -ln "pctStretch" -at "double";
	setAttr -k off ".v";
	setAttr -l on ".DSP";
	setAttr -l on ".TAN";
	setAttr -l on ".LEN";
	setAttr -s 3 ".cdata";
	setAttr -s 23 ".jfrm";
	setAttr ".ldef" 2;
	setAttr ".lsq" 1;
	setAttr ".lst" 4;
	setAttr ".olen" 4.5466002980676654;
	setAttr ".ost" 1;
	setAttr -s 3 ".ocdata";
	setAttr ".ocdata[0].opy" -1;
	setAttr ".ocdata[0].opjy" -1;
	setAttr ".ocdata[0].otgy" 2.2548862366770894;
	setAttr ".ocdata[0].oux" 1;
	setAttr ".ocdata[1].opx" -0.39771309220442991;
	setAttr ".ocdata[1].opy" 1.2172458536385811;
	setAttr ".ocdata[1].opz" -0.10078224629108523;
	setAttr ".ocdata[1].opjx" -0.39771309220442991;
	setAttr ".ocdata[1].opjy" 1.2172458536385811;
	setAttr ".ocdata[1].opjz" -0.10078224629108523;
	setAttr ".ocdata[1].otgx" 0.10826990387796503;
	setAttr ".ocdata[1].otgy" 2.12387861897398;
	setAttr ".ocdata[1].otgz" -0.73539759903033819;
	setAttr ".ocdata[1].oux" 0.99615134036671071;
	setAttr ".ocdata[1].ouy" -0.021346038872279788;
	setAttr ".ocdata[1].ouz" 0.085010903477546237;
	setAttr ".ocdata[2].opx" 0.2022358785368974;
	setAttr ".ocdata[2].opy" 2.9671639396490743;
	setAttr ".ocdata[2].opz" -1.3736391572071338;
	setAttr ".ocdata[2].opjx" 0.2022358785368974;
	setAttr ".ocdata[2].opjy" 2.9671639396490743;
	setAttr ".ocdata[2].opjz" -1.3736391572071338;
	setAttr ".ocdata[2].otgx" 0.87758230128982151;
	setAttr ".ocdata[2].otgy" 1.8335269570099073;
	setAttr ".ocdata[2].otgz" -0.95412000989802193;
	setAttr ".ocdata[2].oux" 0.91735379365199954;
	setAttr ".ocdata[2].ouy" -0.30756881635194461;
	setAttr ".ocdata[2].ouz" 0.25271216923636353;
	setAttr -k on ".curLen";
	setAttr -k on ".pctSquash";
	setAttr -k on ".pctStretch";
createNode transform -n "grpMuscleCONTROLS" -p "grpMuscleRIG";
	rename -uid "72AD5E5B-4165-FC72-A562-528CCBEE14F2";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "grpIControlMuscle1ZERO" -p "grpMuscleCONTROLS";
	rename -uid "8B0BF7D7-4CDE-68FD-EF0F-88B49CE2642A";
	setAttr ".t" -type "double3" 0 -1 0 ;
createNode transform -n "grpIControlMuscle1Cons" -p "grpIControlMuscle1ZERO";
	rename -uid "7A96F7FA-4606-77DB-F7FB-ABAD84AD186E";
createNode transform -n "iControlMuscle1" -p "grpIControlMuscle1Cons";
	rename -uid "1CEF913F-4B8E-EDAA-2358-94B6B4AD023C";
	addAttr -ci true -k true -sn "tanlen" -ln "tangentLength" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "jig" -ln "jiggle" -at "double";
	addAttr -ci true -k true -sn "jigx" -ln "jiggleX" -at "double";
	addAttr -ci true -k true -sn "jigy" -ln "jiggleY" -at "double";
	addAttr -ci true -k true -sn "jigz" -ln "jiggleZ" -at "double";
	addAttr -ci true -k true -sn "jigimp" -ln "jiggleImpact" -at "double";
	addAttr -ci true -k true -sn "jigimpst" -ln "jiggleImpactStart" -dv 1000 -at "double";
	addAttr -ci true -k true -sn "jigimpsp" -ln "jiggleImpactStop" -dv 0.001 -at "double";
	addAttr -ci true -k true -sn "cyc" -ln "cycle" -dv 12 -min 1 -at "double";
	addAttr -ci true -k true -sn "rst" -ln "rest" -dv 24 -min 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -k on ".tanlen";
	setAttr -k on ".jig";
	setAttr -k on ".jigx";
	setAttr -k on ".jigy";
	setAttr -k on ".jigz";
	setAttr -k on ".jigimp";
	setAttr -k on ".jigimpst";
	setAttr -k on ".jigimpsp";
	setAttr -k on ".cyc";
	setAttr -k on ".rst";
createNode nurbsCurve -n "curveShape1" -p "iControlMuscle1";
	rename -uid "3F9F8E3A-422B-E6AF-D5F9-DA8FF4B62D7A";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		-0.25 0.25 0.25
		0.25 0.25 0.25
		0.25 0.25 -0.25
		-0.25 0.25 -0.25
		-0.25 0.25 0.25
		-0.25 -0.25 0.25
		-0.25 -0.25 -0.25
		0.25 -0.25 -0.25
		0.25 -0.25 0.25
		-0.25 -0.25 0.25
		0.25 -0.25 0.25
		0.25 0.25 0.25
		0.25 0.25 -0.25
		0.25 -0.25 -0.25
		-0.25 -0.25 -0.25
		-0.25 0.25 -0.25
		;
createNode transform -n "grpIControlMuscle2ZERO" -p "grpMuscleCONTROLS";
	rename -uid "7B9A31EB-4F0E-ECCF-6950-D2BDB1EC968C";
	setAttr ".t" -type "double3" 0 1 0 ;
createNode transform -n "grpIControlMuscle2Cons" -p "grpIControlMuscle2ZERO";
	rename -uid "E898C03A-4702-5170-CBA4-E39B808A2777";
createNode transform -n "iControlMuscle2" -p "grpIControlMuscle2Cons";
	rename -uid "091D4047-44BB-44A9-93C2-358E041FD84F";
	addAttr -ci true -k true -sn "tanlen" -ln "tangentLength" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "jig" -ln "jiggle" -dv 1 -at "double";
	addAttr -ci true -k true -sn "jigx" -ln "jiggleX" -dv 1 -at "double";
	addAttr -ci true -k true -sn "jigy" -ln "jiggleY" -dv 0.25 -at "double";
	addAttr -ci true -k true -sn "jigz" -ln "jiggleZ" -dv 1 -at "double";
	addAttr -ci true -k true -sn "jigimp" -ln "jiggleImpact" -dv 0.5 -at "double";
	addAttr -ci true -k true -sn "jigimpst" -ln "jiggleImpactStart" -dv 1000 -at "double";
	addAttr -ci true -k true -sn "jigimpsp" -ln "jiggleImpactStop" -dv 0.001 -at "double";
	addAttr -ci true -k true -sn "cyc" -ln "cycle" -dv 12 -min 1 -at "double";
	addAttr -ci true -k true -sn "rst" -ln "rest" -dv 24 -min 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" -0.45207943587370431 0.0050195095720691855 0.665184148643861 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -k on ".tanlen";
	setAttr -k on ".jig";
	setAttr -k on ".jigx";
	setAttr -k on ".jigy";
	setAttr -k on ".jigz";
	setAttr -k on ".jigimp";
	setAttr -k on ".jigimpst";
	setAttr -k on ".jigimpsp";
	setAttr -k on ".cyc";
	setAttr -k on ".rst";
createNode nurbsCurve -n "curveShape2" -p "iControlMuscle2";
	rename -uid "DF4664F8-40B1-8D05-7B62-979A808A7CF4";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		-0.25 0.25 0.25
		0.25 0.25 0.25
		0.25 0.25 -0.25
		-0.25 0.25 -0.25
		-0.25 0.25 0.25
		-0.25 -0.25 0.25
		-0.25 -0.25 -0.25
		0.25 -0.25 -0.25
		0.25 -0.25 0.25
		-0.25 -0.25 0.25
		0.25 -0.25 0.25
		0.25 0.25 0.25
		0.25 0.25 -0.25
		0.25 -0.25 -0.25
		-0.25 -0.25 -0.25
		-0.25 0.25 -0.25
		;
createNode pointConstraint -n "grpIControlMuscle2Cons_pointConstraint1" -p "grpIControlMuscle2Cons";
	rename -uid "5C4DD1F5-48A3-BC4D-6B12-1686E00A744B";
	addAttr -ci true -k true -sn "w0" -ln "iControlMuscle1W0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "iControlMuscle3W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr -k on ".w0" 0.5;
	setAttr -k on ".w1" 0.5;
createNode orientConstraint -n "grpIControlMuscle2Cons_orientConstraint1" -p "grpIControlMuscle2Cons";
	rename -uid "79FB5303-4A7E-5961-1CF2-359E063D678C";
	addAttr -ci true -k true -sn "w0" -ln "grpAimBackMuscle2W0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "grpAimFwdMuscle2W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".lr" -type "double3" -19.147545819144675 -4.8766518622669759 -1.2275753091916575 ;
	setAttr ".int" 2;
	setAttr -k on ".w0" 0.5;
	setAttr -k on ".w1" 0.5;
createNode transform -n "grpAimFwdMuscle2ZERO" -p "grpIControlMuscle2ZERO";
	rename -uid "C0B9CF8D-4107-B540-287E-40BCFF9C1079";
createNode transform -n "grpAimFwdMuscle2" -p "grpAimFwdMuscle2ZERO";
	rename -uid "4C632F8C-49A6-F6CF-6619-E5A72E466249";
createNode aimConstraint -n "grpAimFwdMuscle2_aimConstraint1" -p "grpAimFwdMuscle2";
	rename -uid "1581F437-4B48-0861-89BF-4E9E26636F1A";
	addAttr -ci true -sn "w0" -ln "iControlMuscle3W0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".a" -type "double3" 0 1 0 ;
	setAttr ".wut" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "grpAimFwdMuscle2_pointConstraint1" -p "grpAimFwdMuscle2";
	rename -uid "EDC620C7-4E9E-75DE-A0A4-8EA364713AF8";
	addAttr -ci true -k true -sn "w0" -ln "iControlMuscle1W0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "iControlMuscle3W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".rst" -type "double3" 0 1 0 ;
	setAttr -k on ".w0" 0.5;
	setAttr -k on ".w1" 0.5;
createNode transform -n "grpAimBackMuscle2ZERO" -p "grpIControlMuscle2ZERO";
	rename -uid "E723740E-4BC8-BD2D-4D01-668E2B6195AF";
createNode transform -n "grpAimBackMuscle2" -p "grpAimBackMuscle2ZERO";
	rename -uid "F4691484-467E-CF3A-F019-AFBBCCF0B2D0";
createNode aimConstraint -n "grpAimBackMuscle2_aimConstraint1" -p "grpAimBackMuscle2";
	rename -uid "5FC63A63-4A12-3312-C92C-B5ACD697AD21";
	addAttr -ci true -sn "w0" -ln "iControlMuscle1W0" -dv 1 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".a" -type "double3" 0 -1 0 ;
	setAttr ".wut" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "grpAimBackMuscle2_pointConstraint1" -p "grpAimBackMuscle2";
	rename -uid "6DD5235E-4075-4870-2571-FFB41452B6C2";
	addAttr -ci true -k true -sn "w0" -ln "iControlMuscle1W0" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "w1" -ln "iControlMuscle3W1" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".rst" -type "double3" 0 1 0 ;
	setAttr -k on ".w0" 0.5;
	setAttr -k on ".w1" 0.5;
createNode transform -n "grpIControlMuscle3ZERO" -p "grpMuscleCONTROLS";
	rename -uid "9063F528-40AF-FFC2-0C27-9F9BC16CF82B";
	setAttr ".t" -type "double3" 0 1 0 ;
createNode transform -n "grpIControlMuscle3Cons" -p "grpIControlMuscle3ZERO";
	rename -uid "09E6601D-48D9-C9EF-9314-548AA94A155F";
createNode transform -n "iControlMuscle3" -p "grpIControlMuscle3Cons";
	rename -uid "04F96D33-4397-6369-D4CE-B39BFEFDB322";
	addAttr -ci true -k true -sn "tanlen" -ln "tangentLength" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "jig" -ln "jiggle" -at "double";
	addAttr -ci true -k true -sn "jigx" -ln "jiggleX" -at "double";
	addAttr -ci true -k true -sn "jigy" -ln "jiggleY" -at "double";
	addAttr -ci true -k true -sn "jigz" -ln "jiggleZ" -at "double";
	addAttr -ci true -k true -sn "jigimp" -ln "jiggleImpact" -at "double";
	addAttr -ci true -k true -sn "jigimpst" -ln "jiggleImpactStart" -dv 1000 -at "double";
	addAttr -ci true -k true -sn "jigimpsp" -ln "jiggleImpactStop" -dv 0.001 -at "double";
	addAttr -ci true -k true -sn "cyc" -ln "cycle" -dv 12 -min 1 -at "double";
	addAttr -ci true -k true -sn "rst" -ln "rest" -dv 24 -min 1 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 0.2022358785368974 1.9671639396490743 -1.3736391572071338 ;
	setAttr ".r" -type "double3" -26.050011829309593 -14.63806262009672 -18.535184547887287 ;
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -k on ".tanlen";
	setAttr -k on ".jig";
	setAttr -k on ".jigx";
	setAttr -k on ".jigy";
	setAttr -k on ".jigz";
	setAttr -k on ".jigimp";
	setAttr -k on ".jigimpst";
	setAttr -k on ".jigimpsp";
	setAttr -k on ".cyc";
	setAttr -k on ".rst";
createNode nurbsCurve -n "curveShape3" -p "iControlMuscle3";
	rename -uid "3ADB8F06-4890-3BFA-9CB7-A887AB0012F7";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		-0.25 0.25 0.25
		0.25 0.25 0.25
		0.25 0.25 -0.25
		-0.25 0.25 -0.25
		-0.25 0.25 0.25
		-0.25 -0.25 0.25
		-0.25 -0.25 -0.25
		0.25 -0.25 -0.25
		0.25 -0.25 0.25
		-0.25 -0.25 0.25
		0.25 -0.25 0.25
		0.25 0.25 0.25
		0.25 0.25 -0.25
		0.25 -0.25 -0.25
		-0.25 -0.25 -0.25
		-0.25 0.25 -0.25
		;
createNode transform -n "grpMuscleDRIVEN" -p "grpMuscleRIG";
	rename -uid "914F38DC-43D9-918F-A4EB-8CB7BFE49471";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".it" no;
createNode transform -n "grpMuscleGEO" -p "grpMuscleRIG";
	rename -uid "A69A5C6D-47D1-19A8-0158-1A89699DBBF7";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".it" no;
createNode transform -n "pSphere1" -p "grpMuscleGEO";
	rename -uid "33729EB9-4B06-564A-E281-06A1B8B1CAAC";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode mesh -n "pSphereShape1" -p "pSphere1";
	rename -uid "48D450C3-4646-3802-F10B-A0968B8A83DB";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ugsdt" no;
	setAttr ".vnm" 0;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode mesh -n "pSphereShape1Orig1" -p "pSphere1";
	rename -uid "801233DF-4C32-7F0B-B7D5-83A8CCBE7A52";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ugsdt" no;
	setAttr ".vnm" 0;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode cMuscleObject -n "cMuscleObject_pSphere1Shape1" -p "pSphere1";
	rename -uid "072CE1B4-45BA-A707-4D8A-B1A8C901C7BF";
	setAttr -k off ".v";
	setAttr -cb off ".lpx";
	setAttr -cb off ".lpy";
	setAttr -cb off ".lpz";
	setAttr -cb off ".lsx";
	setAttr -cb off ".lsy";
	setAttr -cb off ".lsz";
	setAttr -l on -k off ".typ";
	setAttr -k off ".rad";
	setAttr -k off ".len";
	setAttr -k off ".cax";
	setAttr -k off ".usx";
	setAttr -k off ".usy";
	setAttr -k off ".usz";
	setAttr ".drw" 0;
	setAttr ".wcol" -type "float3" 0.80000001 0.80000001 0.80000001 ;
	setAttr ".scol" -type "float3" 0.89999998 0.89999998 0.89999998 ;
	setAttr -k off ".seg";
	setAttr -k off ".sid";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "364F3D24-4DD2-2F19-D1C7-B2ACA3E654FB";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "6D45A2BF-4B5F-C8FA-FC29-41A78A6A5461";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "23E4A7DF-4D00-837D-1D93-2B92BF4D70C7";
createNode displayLayerManager -n "layerManager";
	rename -uid "A111565C-4B27-8B72-C732-588A6698004A";
createNode displayLayer -n "defaultLayer";
	rename -uid "76622BD1-4F25-5F34-1767-92B60E16612B";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "15EC9A7E-4227-83A1-44EA-1E9A281B92E2";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "38328A51-43D6-D8DA-8FBE-D4900440FB4D";
	setAttr ".g" yes;
createNode renderLayerManager -n "__clash___renderLayerManager";
	rename -uid "9B214B80-4D62-9D52-8990-F7831B873356";
createNode renderLayer -n "__clash___defaultRenderLayer";
	rename -uid "3181D8F4-40FA-CD18-E0DB-D380B0B7A954";
	setAttr ".g" yes;
createNode polySphere -n "polySphere1";
	rename -uid "7FA14B1A-493B-B507-F4E2-19B6E79D2556";
createNode objectSet -n "setMUSCLERIGS";
	rename -uid "1CDA7FB5-4C81-36C3-D10F-25AD30597963";
	setAttr ".ihi" 0;
createNode objectSet -n "setMuscleRIG";
	rename -uid "848A808A-439B-08B0-904D-2AA003115556";
	setAttr ".ihi" 0;
	setAttr -s 23 ".dsm";
createNode timeToUnitConversion -n "timeToUnitConversion1";
	rename -uid "7903E5ED-46FB-E268-AAB4-E0B8465B798B";
	setAttr ".cf" 0.004;
createNode blendColors -n "blendColorsMuscleSplineAimMuscle";
	rename -uid "D1EA9AA2-48E3-A0FE-6E77-56AED6966785";
	setAttr ".c1" -type "float3" 0 0 1 ;
	setAttr ".c2" -type "float3" 1 0 0 ;
createNode cMuscleSplineDeformer -n "cMuscleSplineDeformer1";
	rename -uid "D1474D1D-4CAB-3A90-3E0A-4A83965873B6";
	setAttr -s 3 ".cdata";
	setAttr -s 3 ".cdatab";
	setAttr ".cdatab[0].pyb" -1;
	setAttr ".cdatab[0].pjyb" -1;
	setAttr ".cdatab[0].tgyb" 1;
	setAttr ".cdatab[0].uxb" 1;
	setAttr ".cdatab[1].tgyb" 1;
	setAttr ".cdatab[1].uxb" 1;
	setAttr ".cdatab[2].pyb" 1;
	setAttr ".cdatab[2].pjyb" 1;
	setAttr ".cdatab[2].tgyb" 1;
	setAttr ".cdatab[2].uxb" 1;
	setAttr -s 382 ".uwt[0:381]"  0.0061558187007904122 0.0061558187007904122 
		0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 
		0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 
		0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 
		0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 0.0061558187007904122 
		0.0061558187007904122 0.0061558187007904122 0.024471729993820211 0.024471729993820211 
		0.024471729993820211 0.024471729993820211 0.024471729993820211 0.024471729993820211 
		0.024471729993820211 0.024471729993820211 0.024471729993820211 0.024471729993820211 
		0.024471729993820211 0.024471729993820211 0.024471729993820211 0.024471729993820211 
		0.024471729993820211 0.024471729993820211 0.024471729993820211 0.024471729993820211 
		0.024471729993820211 0.024471729993820211 0.054496735334396362 0.054496735334396362 
		0.054496735334396362 0.054496735334396362 0.054496735334396362 0.054496735334396362 
		0.054496735334396362 0.054496735334396362 0.054496735334396362 0.054496735334396362 
		0.054496735334396362 0.054496735334396362 0.054496735334396362 0.054496735334396362 
		0.054496735334396362 0.054496735334396362 0.054496735334396362 0.054496735334396362 
		0.054496735334396362 0.054496735334396362 0.095491498708724948 0.095491498708724948 
		0.095491498708724948 0.095491498708724948 0.095491498708724948 0.095491498708724948 
		0.095491498708724948 0.095491498708724948 0.095491498708724948 0.095491498708724948 
		0.095491498708724948 0.095491498708724948 0.095491498708724948 0.095491498708724948 
		0.095491498708724948 0.095491498708724948 0.095491498708724948 0.095491498708724948 
		0.095491498708724948 0.095491498708724948 0.14644661545753473 0.14644661545753473 
		0.14644661545753473 0.14644661545753473 0.14644661545753473 0.14644661545753473 0.14644661545753473 
		0.14644661545753473 0.14644661545753473 0.14644661545753473 0.14644661545753473 0.14644661545753473 
		0.14644661545753473 0.14644661545753473 0.14644661545753473 0.14644661545753473 0.14644661545753473 
		0.14644661545753473 0.14644661545753473 0.14644661545753473 0.20610737800598139 0.20610737800598139 
		0.20610737800598139 0.20610737800598139 0.20610737800598139 0.20610737800598139 0.20610737800598139 
		0.20610737800598139 0.20610737800598139 0.20610737800598139 0.20610737800598139 0.20610737800598139 
		0.20610737800598139 0.20610737800598139 0.20610737800598139 0.20610737800598139 0.20610737800598139 
		0.20610737800598139 0.20610737800598139 0.20610737800598139 0.27300474047660822 0.27300474047660822 
		0.27300474047660822 0.27300474047660822 0.27300474047660822 0.27300474047660822 0.27300474047660822 
		0.27300474047660822 0.27300474047660822 0.27300474047660822 0.27300474047660822 0.27300474047660822 
		0.27300474047660822 0.27300474047660822 0.27300474047660822 0.27300474047660822 0.27300474047660822 
		0.27300474047660822 0.27300474047660822 0.27300474047660822 0.34549151360988611 0.34549151360988611 
		0.34549151360988611 0.34549151360988611 0.34549151360988611 0.34549151360988611 0.34549151360988611 
		0.34549151360988611 0.34549151360988611 0.34549151360988611 0.34549151360988611 0.34549151360988611 
		0.34549151360988611 0.34549151360988611 0.34549151360988611 0.34549151360988611 0.34549151360988611 
		0.34549151360988611 0.34549151360988611 0.34549151360988611 0.42178281396627437 0.42178281396627437 
		0.42178281396627437 0.42178281396627437 0.42178281396627437 0.42178281396627437 0.42178281396627437 
		0.42178281396627437 0.42178281396627437 0.42178281396627437 0.42178281396627437 0.42178281396627437 
		0.42178281396627437 0.42178281396627437 0.42178281396627437 0.42178281396627437 0.42178281396627437 
		0.42178281396627437 0.42178281396627437 0.42178281396627437 0.5 0.5 0.5 0.5 0.5 0.5 
		0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.57821718603372574 0.57821718603372574 
		0.57821718603372574 0.57821718603372574 0.57821718603372574 0.57821718603372574 0.57821718603372574 
		0.57821718603372574 0.57821718603372574 0.57821718603372574 0.57821718603372574 0.57821718603372574 
		0.57821718603372574 0.57821718603372574 0.57821718603372574 0.57821718603372574 0.57821718603372574 
		0.57821718603372574 0.57821718603372574 0.57821718603372574 0.65450848639011383 0.65450848639011383 
		0.65450848639011383 0.65450848639011383 0.65450848639011383 0.65450848639011383 0.65450848639011383 
		0.65450848639011383 0.65450848639011383 0.65450848639011383 0.65450848639011383 0.65450848639011383 
		0.65450848639011383 0.65450848639011383 0.65450848639011383 0.65450848639011383 0.65450848639011383 
		0.65450848639011383 0.65450848639011383 0.65450848639011383 0.72699525952339172 0.72699525952339172 
		0.72699525952339172 0.72699525952339172 0.72699525952339172 0.72699525952339172 0.72699525952339172 
		0.72699525952339172 0.72699525952339172 0.72699525952339172 0.72699525952339172 0.72699525952339172 
		0.72699525952339172 0.72699525952339172 0.72699525952339172 0.72699525952339172 0.72699525952339172 
		0.72699525952339172 0.72699525952339172 0.72699525952339172 0.79389262199401855 0.79389262199401855 
		0.79389262199401855 0.79389262199401855 0.79389262199401855 0.79389262199401855 0.79389262199401855 
		0.79389262199401855 0.79389262199401855 0.79389262199401855 0.79389262199401855 0.79389262199401855 
		0.79389262199401855 0.79389262199401855 0.79389262199401855 0.79389262199401855 0.79389262199401855 
		0.79389262199401855 0.79389262199401855 0.79389262199401855 0.85355338454246521 0.85355338454246521 
		0.85355338454246521 0.85355338454246521 0.85355338454246521 0.85355338454246521 0.85355338454246521 
		0.85355338454246521 0.85355338454246521 0.85355338454246521 0.85355338454246521 0.85355338454246521 
		0.85355338454246521 0.85355338454246521 0.85355338454246521 0.85355338454246521 0.85355338454246521 
		0.85355338454246521 0.85355338454246521 0.85355338454246521 0.90450850129127502 0.90450850129127502 
		0.90450850129127502 0.90450850129127502 0.90450850129127502 0.90450850129127502 0.90450850129127502 
		0.90450850129127502 0.90450850129127502 0.90450850129127502 0.90450850129127502 0.90450850129127502 
		0.90450850129127502 0.90450850129127502 0.90450850129127502 0.90450850129127502 0.90450850129127502 
		0.90450850129127502 0.90450850129127502 0.90450850129127502 0.94550326466560364 0.94550326466560364 
		0.94550326466560364 0.94550326466560364 0.94550326466560364 0.94550326466560364 0.94550326466560364 
		0.94550326466560364 0.94550326466560364 0.94550326466560364 0.94550326466560364 0.94550326466560364 
		0.94550326466560364 0.94550326466560364 0.94550326466560364 0.94550326466560364 0.94550326466560364 
		0.94550326466560364 0.94550326466560364 0.94550326466560364 0.9755282700061797 0.9755282700061797 
		0.9755282700061797 0.9755282700061797 0.9755282700061797 0.9755282700061797 0.9755282700061797 
		0.9755282700061797 0.9755282700061797 0.9755282700061797 0.9755282700061797 0.9755282700061797 
		0.9755282700061797 0.9755282700061797 0.9755282700061797 0.9755282700061797 0.9755282700061797 
		0.9755282700061797 0.9755282700061797 0.9755282700061797 0.99384418129920982 0.99384418129920982 
		0.99384418129920982 0.99384418129920982 0.99384418129920982 0.99384418129920982 0.99384418129920982 
		0.99384418129920982 0.99384418129920982 0.99384418129920982 0.99384418129920982 0.99384418129920982 
		0.99384418129920982 0.99384418129920982 0.99384418129920982 0.99384418129920982 0.99384418129920982 
		0.99384418129920982 0.99384418129920982 0.99384418129920982 0 1.0000000000000004;
	setAttr -l on ".STA";
	setAttr -l on ".SHA";
	setAttr -l on ".SQA";
	setAttr -l on ".STE";
createNode tweak -n "tweak1";
	rename -uid "761DD1F1-4FA5-5C25-4E7F-068945430653";
createNode objectSet -n "cMuscleSplineDeformer1Set";
	rename -uid "9CA2773C-4A27-F58B-8F56-EA8B2188C4E6";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cMuscleSplineDeformer1GroupId";
	rename -uid "CB17FC9E-481B-C330-1FCA-8DA74EB1CE3B";
	setAttr ".ihi" 0;
createNode groupParts -n "cMuscleSplineDeformer1GroupParts";
	rename -uid "27F9F5C4-4B98-3B87-4AC4-D68AFA8E028B";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode objectSet -n "tweakSet1";
	rename -uid "9C314456-4D46-155D-E9D0-FC909791C030";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	rename -uid "C40B7721-44B6-18FA-0727-DF8A5D912378";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "CE1B9D04-4089-B38B-2F51-B481145601B7";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "499E3B6E-4D26-314A-3FED-02AE2A8A3BBD";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n"
		+ "            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n"
		+ "            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n"
		+ "            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n"
		+ "            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1318\n            -height 710\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n"
		+ "            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n"
		+ "            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n"
		+ "            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n"
		+ "            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n"
		+ "                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n"
		+ "                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n"
		+ "                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n"
		+ "                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n"
		+ "                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1318\\n    -height 710\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1318\\n    -height 710\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "A7B7B3BF-44A9-724A-ACE5-7B82D6593F8A";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 24 -ast 1 -aet 48 ";
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
	setAttr -s 2 ".r";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "timeToUnitConversion1.o" "cMuscleSplineMuscleShape.it";
connectAttr "cMuscleSplineMuscleShape.olen" "cMuscleSplineMuscleShape.curLen";
connectAttr "cMuscleSplineMuscleShape.osq" "cMuscleSplineMuscleShape.pctSquash";
connectAttr "cMuscleSplineMuscleShape.ost" "cMuscleSplineMuscleShape.pctStretch"
		;
connectAttr "iControlMuscle1.wm" "cMuscleSplineMuscleShape.cdata[0].imat";
connectAttr "iControlMuscle1.tanlen" "cMuscleSplineMuscleShape.cdata[0].tlen";
connectAttr "iControlMuscle1.jig" "cMuscleSplineMuscleShape.cdata[0].jig";
connectAttr "iControlMuscle1.jigx" "cMuscleSplineMuscleShape.cdata[0].jigx";
connectAttr "iControlMuscle1.jigy" "cMuscleSplineMuscleShape.cdata[0].jigy";
connectAttr "iControlMuscle1.jigz" "cMuscleSplineMuscleShape.cdata[0].jigz";
connectAttr "iControlMuscle1.jigimp" "cMuscleSplineMuscleShape.cdata[0].jigimp";
connectAttr "iControlMuscle1.jigimpst" "cMuscleSplineMuscleShape.cdata[0].jigimps"
		;
connectAttr "iControlMuscle1.jigimpsp" "cMuscleSplineMuscleShape.cdata[0].jigimpp"
		;
connectAttr "iControlMuscle1.cyc" "cMuscleSplineMuscleShape.cdata[0].cyc";
connectAttr "iControlMuscle1.rst" "cMuscleSplineMuscleShape.cdata[0].rst";
connectAttr "iControlMuscle2.wm" "cMuscleSplineMuscleShape.cdata[1].imat";
connectAttr "iControlMuscle2.tanlen" "cMuscleSplineMuscleShape.cdata[1].tlen";
connectAttr "iControlMuscle2.jig" "cMuscleSplineMuscleShape.cdata[1].jig";
connectAttr "iControlMuscle2.jigx" "cMuscleSplineMuscleShape.cdata[1].jigx";
connectAttr "iControlMuscle2.jigy" "cMuscleSplineMuscleShape.cdata[1].jigy";
connectAttr "iControlMuscle2.jigz" "cMuscleSplineMuscleShape.cdata[1].jigz";
connectAttr "iControlMuscle2.jigimp" "cMuscleSplineMuscleShape.cdata[1].jigimp";
connectAttr "iControlMuscle2.jigimpst" "cMuscleSplineMuscleShape.cdata[1].jigimps"
		;
connectAttr "iControlMuscle2.jigimpsp" "cMuscleSplineMuscleShape.cdata[1].jigimpp"
		;
connectAttr "iControlMuscle2.cyc" "cMuscleSplineMuscleShape.cdata[1].cyc";
connectAttr "iControlMuscle2.rst" "cMuscleSplineMuscleShape.cdata[1].rst";
connectAttr "iControlMuscle3.wm" "cMuscleSplineMuscleShape.cdata[2].imat";
connectAttr "iControlMuscle3.tanlen" "cMuscleSplineMuscleShape.cdata[2].tlen";
connectAttr "iControlMuscle3.jig" "cMuscleSplineMuscleShape.cdata[2].jig";
connectAttr "iControlMuscle3.jigx" "cMuscleSplineMuscleShape.cdata[2].jigx";
connectAttr "iControlMuscle3.jigy" "cMuscleSplineMuscleShape.cdata[2].jigy";
connectAttr "iControlMuscle3.jigz" "cMuscleSplineMuscleShape.cdata[2].jigz";
connectAttr "iControlMuscle3.jigimp" "cMuscleSplineMuscleShape.cdata[2].jigimp";
connectAttr "iControlMuscle3.jigimpst" "cMuscleSplineMuscleShape.cdata[2].jigimps"
		;
connectAttr "iControlMuscle3.jigimpsp" "cMuscleSplineMuscleShape.cdata[2].jigimpp"
		;
connectAttr "iControlMuscle3.cyc" "cMuscleSplineMuscleShape.cdata[2].cyc";
connectAttr "iControlMuscle3.rst" "cMuscleSplineMuscleShape.cdata[2].rst";
connectAttr "grpIControlMuscle2Cons_pointConstraint1.ctx" "grpIControlMuscle2Cons.tx"
		;
connectAttr "grpIControlMuscle2Cons_pointConstraint1.cty" "grpIControlMuscle2Cons.ty"
		;
connectAttr "grpIControlMuscle2Cons_pointConstraint1.ctz" "grpIControlMuscle2Cons.tz"
		;
connectAttr "grpIControlMuscle2Cons_orientConstraint1.crx" "grpIControlMuscle2Cons.rx"
		;
connectAttr "grpIControlMuscle2Cons_orientConstraint1.cry" "grpIControlMuscle2Cons.ry"
		;
connectAttr "grpIControlMuscle2Cons_orientConstraint1.crz" "grpIControlMuscle2Cons.rz"
		;
connectAttr "grpIControlMuscle2Cons.pim" "grpIControlMuscle2Cons_pointConstraint1.cpim"
		;
connectAttr "grpIControlMuscle2Cons.rp" "grpIControlMuscle2Cons_pointConstraint1.crp"
		;
connectAttr "grpIControlMuscle2Cons.rpt" "grpIControlMuscle2Cons_pointConstraint1.crt"
		;
connectAttr "iControlMuscle1.t" "grpIControlMuscle2Cons_pointConstraint1.tg[0].tt"
		;
connectAttr "iControlMuscle1.rp" "grpIControlMuscle2Cons_pointConstraint1.tg[0].trp"
		;
connectAttr "iControlMuscle1.rpt" "grpIControlMuscle2Cons_pointConstraint1.tg[0].trt"
		;
connectAttr "iControlMuscle1.pm" "grpIControlMuscle2Cons_pointConstraint1.tg[0].tpm"
		;
connectAttr "grpIControlMuscle2Cons_pointConstraint1.w0" "grpIControlMuscle2Cons_pointConstraint1.tg[0].tw"
		;
connectAttr "iControlMuscle3.t" "grpIControlMuscle2Cons_pointConstraint1.tg[1].tt"
		;
connectAttr "iControlMuscle3.rp" "grpIControlMuscle2Cons_pointConstraint1.tg[1].trp"
		;
connectAttr "iControlMuscle3.rpt" "grpIControlMuscle2Cons_pointConstraint1.tg[1].trt"
		;
connectAttr "iControlMuscle3.pm" "grpIControlMuscle2Cons_pointConstraint1.tg[1].tpm"
		;
connectAttr "grpIControlMuscle2Cons_pointConstraint1.w1" "grpIControlMuscle2Cons_pointConstraint1.tg[1].tw"
		;
connectAttr "grpIControlMuscle2Cons.ro" "grpIControlMuscle2Cons_orientConstraint1.cro"
		;
connectAttr "grpIControlMuscle2Cons.pim" "grpIControlMuscle2Cons_orientConstraint1.cpim"
		;
connectAttr "grpAimBackMuscle2.r" "grpIControlMuscle2Cons_orientConstraint1.tg[0].tr"
		;
connectAttr "grpAimBackMuscle2.ro" "grpIControlMuscle2Cons_orientConstraint1.tg[0].tro"
		;
connectAttr "grpAimBackMuscle2.pm" "grpIControlMuscle2Cons_orientConstraint1.tg[0].tpm"
		;
connectAttr "grpIControlMuscle2Cons_orientConstraint1.w0" "grpIControlMuscle2Cons_orientConstraint1.tg[0].tw"
		;
connectAttr "grpAimFwdMuscle2.r" "grpIControlMuscle2Cons_orientConstraint1.tg[1].tr"
		;
connectAttr "grpAimFwdMuscle2.ro" "grpIControlMuscle2Cons_orientConstraint1.tg[1].tro"
		;
connectAttr "grpAimFwdMuscle2.pm" "grpIControlMuscle2Cons_orientConstraint1.tg[1].tpm"
		;
connectAttr "grpIControlMuscle2Cons_orientConstraint1.w1" "grpIControlMuscle2Cons_orientConstraint1.tg[1].tw"
		;
connectAttr "grpAimFwdMuscle2_aimConstraint1.crx" "grpAimFwdMuscle2.rx";
connectAttr "grpAimFwdMuscle2_aimConstraint1.cry" "grpAimFwdMuscle2.ry";
connectAttr "grpAimFwdMuscle2_aimConstraint1.crz" "grpAimFwdMuscle2.rz";
connectAttr "grpAimFwdMuscle2_pointConstraint1.ctx" "grpAimFwdMuscle2.tx";
connectAttr "grpAimFwdMuscle2_pointConstraint1.cty" "grpAimFwdMuscle2.ty";
connectAttr "grpAimFwdMuscle2_pointConstraint1.ctz" "grpAimFwdMuscle2.tz";
connectAttr "grpAimFwdMuscle2.pim" "grpAimFwdMuscle2_aimConstraint1.cpim";
connectAttr "grpAimFwdMuscle2.t" "grpAimFwdMuscle2_aimConstraint1.ct";
connectAttr "grpAimFwdMuscle2.rp" "grpAimFwdMuscle2_aimConstraint1.crp";
connectAttr "grpAimFwdMuscle2.rpt" "grpAimFwdMuscle2_aimConstraint1.crt";
connectAttr "grpAimFwdMuscle2.ro" "grpAimFwdMuscle2_aimConstraint1.cro";
connectAttr "iControlMuscle3.t" "grpAimFwdMuscle2_aimConstraint1.tg[0].tt";
connectAttr "iControlMuscle3.rp" "grpAimFwdMuscle2_aimConstraint1.tg[0].trp";
connectAttr "iControlMuscle3.rpt" "grpAimFwdMuscle2_aimConstraint1.tg[0].trt";
connectAttr "iControlMuscle3.pm" "grpAimFwdMuscle2_aimConstraint1.tg[0].tpm";
connectAttr "grpAimFwdMuscle2_aimConstraint1.w0" "grpAimFwdMuscle2_aimConstraint1.tg[0].tw"
		;
connectAttr "iControlMuscle3.wm" "grpAimFwdMuscle2_aimConstraint1.wum";
connectAttr "blendColorsMuscleSplineAimMuscle.op" "grpAimFwdMuscle2_aimConstraint1.u"
		;
connectAttr "blendColorsMuscleSplineAimMuscle.op" "grpAimFwdMuscle2_aimConstraint1.wu"
		;
connectAttr "grpAimFwdMuscle2.pim" "grpAimFwdMuscle2_pointConstraint1.cpim";
connectAttr "grpAimFwdMuscle2.rp" "grpAimFwdMuscle2_pointConstraint1.crp";
connectAttr "grpAimFwdMuscle2.rpt" "grpAimFwdMuscle2_pointConstraint1.crt";
connectAttr "iControlMuscle1.t" "grpAimFwdMuscle2_pointConstraint1.tg[0].tt";
connectAttr "iControlMuscle1.rp" "grpAimFwdMuscle2_pointConstraint1.tg[0].trp";
connectAttr "iControlMuscle1.rpt" "grpAimFwdMuscle2_pointConstraint1.tg[0].trt";
connectAttr "iControlMuscle1.pm" "grpAimFwdMuscle2_pointConstraint1.tg[0].tpm";
connectAttr "grpAimFwdMuscle2_pointConstraint1.w0" "grpAimFwdMuscle2_pointConstraint1.tg[0].tw"
		;
connectAttr "iControlMuscle3.t" "grpAimFwdMuscle2_pointConstraint1.tg[1].tt";
connectAttr "iControlMuscle3.rp" "grpAimFwdMuscle2_pointConstraint1.tg[1].trp";
connectAttr "iControlMuscle3.rpt" "grpAimFwdMuscle2_pointConstraint1.tg[1].trt";
connectAttr "iControlMuscle3.pm" "grpAimFwdMuscle2_pointConstraint1.tg[1].tpm";
connectAttr "grpAimFwdMuscle2_pointConstraint1.w1" "grpAimFwdMuscle2_pointConstraint1.tg[1].tw"
		;
connectAttr "grpAimBackMuscle2_aimConstraint1.crx" "grpAimBackMuscle2.rx";
connectAttr "grpAimBackMuscle2_aimConstraint1.cry" "grpAimBackMuscle2.ry";
connectAttr "grpAimBackMuscle2_aimConstraint1.crz" "grpAimBackMuscle2.rz";
connectAttr "grpAimBackMuscle2_pointConstraint1.ctx" "grpAimBackMuscle2.tx";
connectAttr "grpAimBackMuscle2_pointConstraint1.cty" "grpAimBackMuscle2.ty";
connectAttr "grpAimBackMuscle2_pointConstraint1.ctz" "grpAimBackMuscle2.tz";
connectAttr "grpAimBackMuscle2.pim" "grpAimBackMuscle2_aimConstraint1.cpim";
connectAttr "grpAimBackMuscle2.t" "grpAimBackMuscle2_aimConstraint1.ct";
connectAttr "grpAimBackMuscle2.rp" "grpAimBackMuscle2_aimConstraint1.crp";
connectAttr "grpAimBackMuscle2.rpt" "grpAimBackMuscle2_aimConstraint1.crt";
connectAttr "grpAimBackMuscle2.ro" "grpAimBackMuscle2_aimConstraint1.cro";
connectAttr "iControlMuscle1.t" "grpAimBackMuscle2_aimConstraint1.tg[0].tt";
connectAttr "iControlMuscle1.rp" "grpAimBackMuscle2_aimConstraint1.tg[0].trp";
connectAttr "iControlMuscle1.rpt" "grpAimBackMuscle2_aimConstraint1.tg[0].trt";
connectAttr "iControlMuscle1.pm" "grpAimBackMuscle2_aimConstraint1.tg[0].tpm";
connectAttr "grpAimBackMuscle2_aimConstraint1.w0" "grpAimBackMuscle2_aimConstraint1.tg[0].tw"
		;
connectAttr "iControlMuscle1.wm" "grpAimBackMuscle2_aimConstraint1.wum";
connectAttr "blendColorsMuscleSplineAimMuscle.op" "grpAimBackMuscle2_aimConstraint1.u"
		;
connectAttr "blendColorsMuscleSplineAimMuscle.op" "grpAimBackMuscle2_aimConstraint1.wu"
		;
connectAttr "grpAimBackMuscle2.pim" "grpAimBackMuscle2_pointConstraint1.cpim";
connectAttr "grpAimBackMuscle2.rp" "grpAimBackMuscle2_pointConstraint1.crp";
connectAttr "grpAimBackMuscle2.rpt" "grpAimBackMuscle2_pointConstraint1.crt";
connectAttr "iControlMuscle1.t" "grpAimBackMuscle2_pointConstraint1.tg[0].tt";
connectAttr "iControlMuscle1.rp" "grpAimBackMuscle2_pointConstraint1.tg[0].trp";
connectAttr "iControlMuscle1.rpt" "grpAimBackMuscle2_pointConstraint1.tg[0].trt"
		;
connectAttr "iControlMuscle1.pm" "grpAimBackMuscle2_pointConstraint1.tg[0].tpm";
connectAttr "grpAimBackMuscle2_pointConstraint1.w0" "grpAimBackMuscle2_pointConstraint1.tg[0].tw"
		;
connectAttr "iControlMuscle3.t" "grpAimBackMuscle2_pointConstraint1.tg[1].tt";
connectAttr "iControlMuscle3.rp" "grpAimBackMuscle2_pointConstraint1.tg[1].trp";
connectAttr "iControlMuscle3.rpt" "grpAimBackMuscle2_pointConstraint1.tg[1].trt"
		;
connectAttr "iControlMuscle3.pm" "grpAimBackMuscle2_pointConstraint1.tg[1].tpm";
connectAttr "grpAimBackMuscle2_pointConstraint1.w1" "grpAimBackMuscle2_pointConstraint1.tg[1].tw"
		;
connectAttr "cMuscleSplineDeformer1GroupId.id" "pSphereShape1.iog.og[0].gid";
connectAttr "cMuscleSplineDeformer1Set.mwc" "pSphereShape1.iog.og[0].gco";
connectAttr "groupId2.id" "pSphereShape1.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "pSphereShape1.iog.og[1].gco";
connectAttr "cMuscleSplineDeformer1.og[0]" "pSphereShape1.i";
connectAttr "tweak1.vl[0].vt[0]" "pSphereShape1.twl";
connectAttr "polySphere1.out" "pSphereShape1Orig1.i";
connectAttr "pSphereShape1.w" "cMuscleObject_pSphere1Shape1.mesh";
connectAttr "pSphere1.wm" "cMuscleObject_pSphere1Shape1.wms";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "__clash___renderLayerManager.rlmi[0]" "__clash___defaultRenderLayer.rlid"
		;
connectAttr "setMuscleRIG.msg" "setMUSCLERIGS.dnsm" -na;
connectAttr "grpMuscleRIG.iog" "setMuscleRIG.dsm" -na;
connectAttr "cMuscleSplineMuscleShape.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpMuscleCONTROLS.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpMuscleDRIVEN.iog" "setMuscleRIG.dsm" -na;
connectAttr "iControlMuscle1.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle1Cons.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle1ZERO.iog" "setMuscleRIG.dsm" -na;
connectAttr "iControlMuscle2.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle2Cons.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle2ZERO.iog" "setMuscleRIG.dsm" -na;
connectAttr "iControlMuscle3.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle3Cons.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle3ZERO.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimBackMuscle2.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimFwdMuscle2.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimBackMuscle2_aimConstraint1.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimFwdMuscle2_aimConstraint1.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimBackMuscle2_pointConstraint1.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimFwdMuscle2_pointConstraint1.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpIControlMuscle2Cons_orientConstraint1.iog" "setMuscleRIG.dsm" -na
		;
connectAttr "grpAimBackMuscle2ZERO.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpAimFwdMuscle2ZERO.iog" "setMuscleRIG.dsm" -na;
connectAttr "grpMuscleGEO.iog" "setMuscleRIG.dsm" -na;
connectAttr "blendColorsMuscleSplineAimMuscle.msg" "setMuscleRIG.dnsm" -na;
connectAttr ":time1.o" "timeToUnitConversion1.i";
connectAttr "cMuscleSplineMuscleShape.uax" "blendColorsMuscleSplineAimMuscle.b";
connectAttr "cMuscleSplineMuscleShape.olen" "cMuscleSplineDeformer1.clen";
connectAttr "cMuscleSplineMuscleShape.osq" "cMuscleSplineDeformer1.psq";
connectAttr "cMuscleSplineMuscleShape.ost" "cMuscleSplineDeformer1.pst";
connectAttr "cMuscleSplineMuscleShape.usc" "cMuscleSplineDeformer1.usc";
connectAttr "cMuscleSplineDeformer1GroupParts.og" "cMuscleSplineDeformer1.ip[0].ig"
		;
connectAttr "cMuscleSplineDeformer1GroupId.id" "cMuscleSplineDeformer1.ip[0].gi"
		;
connectAttr "cMuscleSplineMuscleShape.ocdata[0]" "cMuscleSplineDeformer1.cdata[0]"
		;
connectAttr "cMuscleSplineMuscleShape.ocdata[1]" "cMuscleSplineDeformer1.cdata[1]"
		;
connectAttr "cMuscleSplineMuscleShape.ocdata[2]" "cMuscleSplineDeformer1.cdata[2]"
		;
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "cMuscleSplineDeformer1GroupId.msg" "cMuscleSplineDeformer1Set.gn" -na
		;
connectAttr "pSphereShape1.iog.og[0]" "cMuscleSplineDeformer1Set.dsm" -na;
connectAttr "cMuscleSplineDeformer1.msg" "cMuscleSplineDeformer1Set.ub[0]";
connectAttr "tweak1.og[0]" "cMuscleSplineDeformer1GroupParts.ig";
connectAttr "cMuscleSplineDeformer1GroupId.id" "cMuscleSplineDeformer1GroupParts.gi"
		;
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "pSphereShape1.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "pSphereShape1Orig1.w" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "__clash___defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "pSphereShape1.iog" ":initialShadingGroup.dsm" -na;
// End of muscleObj_cMuscleSpline.ma
