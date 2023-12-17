//Maya ASCII 2022 scene
//Name: bahamut_rig_20231218_03074541753_2022.ma
//Last modified: Mon, Dec 18, 2023 03:07:45 AM
//Codeset: 932
file -rdi 1 -ns "chr" -rfn "chrRN" -op "v=0;" -typ "mayaAscii" "F:/myTechData/Maya/sandbox/cygames/wizard2/chr/bahamut/maya/Bahamut.ma";
file -r -ns "chr" -dr 1 -rfn "chrRN" -op "v=0;" -typ "mayaAscii" "F:/myTechData/Maya/sandbox/cygames/wizard2/chr/bahamut/maya/Bahamut.ma";
requires maya "2022";
requires "mtoa" "5.0.0.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202205171752-c25c06f306";
fileInfo "osv" "Windows 10 Home v2009 (Build: 22621)";
fileInfo "UUID" "8F137725-4D5E-9A11-2FF6-1A8F3DF4A3AB";
createNode transform -s -n "persp";
	rename -uid "A8C3E681-4F4D-FBA7-0DA6-ECA355ABC057";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "C67A26E7-412E-1E03-5047-30A9F2149D8E";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "AF0E1CBB-488C-BCCB-EC0A-FCA5FE72B050";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "03518331-4DB6-5927-F3D5-BB94CF420791";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "9391606C-4DDA-F611-6759-0AA09A86504B";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "75C99438-4B79-1086-D983-D599BDA12E17";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "69DB6778-4E34-415A-319A-01AD93555817";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "060E6930-470E-88B8-4BB1-4B893B302654";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "CHAR";
	rename -uid "1DC16F31-4057-E72D-F626-D2A78F814B78";
createNode transform -n "MODEL" -p "CHAR";
	rename -uid "B3E9A13B-4E0E-2350-52DE-849F5D622675";
createNode transform -n "RIG" -p "CHAR";
	rename -uid "900277BE-48FD-DFF0-5A9C-B2BD73321B2D";
createNode transform -n "Cn_root" -p "RIG";
	rename -uid "C4A3B2F7-4760-A955-A320-2FB10A65DA88";
createNode transform -n "Cn_root_MODULE" -p "Cn_root";
	rename -uid "9D4B7A58-4619-D235-7B88-1ABA756CDDCC";
createNode transform -n "Cn_root_MODULE_ROOT" -p "Cn_root_MODULE";
	rename -uid "0318DA6D-4F6A-DB6E-6EBF-6189A10CD8D7";
createNode joint -n "Global" -p "Cn_root_MODULE_ROOT";
	rename -uid "5D83D360-4A15-1B6D-5C84-F1BBBC8F363B";
createNode joint -n "Local" -p "Global";
	rename -uid "7BE05685-41DB-A59D-80ED-059B3B77437D";
createNode joint -n "Root" -p "Local";
	rename -uid "82658162-4F8E-8877-8835-47AD6B109E8B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Root";
	setAttr ".radi" 212.20000000000002;
	setAttr ".liw" yes;
createNode pointConstraint -n "Root_pointConstraint1" -p "Root";
	rename -uid "7151653D-4B4C-C894-2FF9-EBAC8A998B26";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Root_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Root_orientConstraint1" -p "Root";
	rename -uid "0CA90754-4883-CA74-16F4-27ABC89FDAFE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Root_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode pointConstraint -n "Local_pointConstraint1" -p "Local";
	rename -uid "DAC7037E-448B-8DFD-7914-F68533C0CF9A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Local_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Local_orientConstraint1" -p "Local";
	rename -uid "7658B6BA-43A8-87DE-E7EB-BF98456B39B6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Local_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode pointConstraint -n "Global_pointConstraint1" -p "Global";
	rename -uid "0CB22BEF-40BF-E318-441F-3F99A618B634";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Global_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Global_orientConstraint1" -p "Global";
	rename -uid "69CB1B99-4452-44DE-5737-5799B64EF6D8";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Global_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode transform -n "Cn_root_CONTROL" -p "Cn_root";
	rename -uid "985B7125-48B9-BA93-31B1-4AB156288BD9";
createNode transform -n "Cn_root_CONTROL_ROOT" -p "Cn_root_CONTROL";
	rename -uid "6FF9D91E-4807-E8E1-4152-D1880B419FDD";
createNode joint -n "chr:Global" -p "Cn_root_CONTROL_ROOT";
	rename -uid "37E15F8F-4DDD-94FC-97B3-1D95AEFC635B";
createNode joint -n "chr:Local" -p "chr:Global";
	rename -uid "04DB9D0E-4383-35EF-0169-A4BC6ABA3127";
createNode pointConstraint -n "Local_pointConstraint2" -p "chr:Local";
	rename -uid "68E996F3-4C70-C708-E1EB-BD80A05ED371";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "LocalW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Local_orientConstraint2" -p "chr:Local";
	rename -uid "D2F07429-461D-C1B5-93BA-A7A600827C25";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "LocalW0" -dv 1 -min 0 -at "double";
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
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Local_scaleConstraint1" -p "chr:Local";
	rename -uid "9ECEA635-4C09-3BE6-EE9C-A6B084883221";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "LocalW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode pointConstraint -n "Global_pointConstraint2" -p "chr:Global";
	rename -uid "88A7A9E9-4E0D-1C10-60D6-5392101EFD57";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "GlobalW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Global_orientConstraint2" -p "chr:Global";
	rename -uid "90131DCB-474B-CB37-E61D-A2B3730CFE44";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "GlobalW0" -dv 1 -min 0 -at "double";
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
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Global_scaleConstraint1" -p "chr:Global";
	rename -uid "E727E6CF-4D5F-C188-09D8-A7AD7B06CC2F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "GlobalW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode transform -n "Global_CTRL_GRP" -p "Cn_root_CONTROL_ROOT";
	rename -uid "43E6F488-4182-AC2A-1237-BFBA226320C6";
createNode transform -n "Global_CTRL_OFFSET" -p "Global_CTRL_GRP";
	rename -uid "AE0558BD-412C-E036-15B4-AF9FA81BAB10";
createNode transform -n "Global_CTRL_SPACE" -p "Global_CTRL_OFFSET";
	rename -uid "5934F0C0-4149-B668-F606-2F87503A7D64";
createNode transform -n "Global_CTRL_MOCAP" -p "Global_CTRL_SPACE";
	rename -uid "447AB663-4D27-D7E5-E472-E6AB9E3480FF";
createNode transform -n "Global_CTRL_DRV" -p "Global_CTRL_MOCAP";
	rename -uid "60D699EB-4265-BCF6-D419-0BA1EC228DFC";
createNode transform -n "Global_CTRL" -p "Global_CTRL_DRV";
	rename -uid "06EFE448-4835-0911-24B3-869C88D55358";
	setAttr ".wfcc" -type "float3" 0.199 0.108 0.315 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.199 0.108 0.315 ;
createNode nurbsCurve -n "Global_CTRLShape" -p "Global_CTRL";
	rename -uid "CAF45F2F-4AD8-3703-F422-54A47A16108F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.199 0.108 0.315 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 67 0 no 3
		68 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
		 55 56 57 58 59 60 61 62 63 64 65 66 67
		68
		-0.0016987001481580184 3.1161483066773724e-22 1827.2219736957215
		-500.55827130759133 1.2260141770641792e-13 1739.2261038083404
		-985.19208927731302 2.4130247881120555e-13 1474.4450571386642
		-1474.4444225921131 3.6113473660470245e-13 985.19291418782939
		-1739.2261038083404 4.2598755241195525e-13 345.95389131136761
		-1739.2262307176502 4.259875805914829e-13 -345.95357403809192
		-1474.4450571386642 3.6113487750234074e-13 -985.1920258226578
		-985.1927238238643 2.4130261970884373e-13 -1474.4446764107338
		-345.95360576541958 8.4734191142620188e-14 -1739.2261038083404
		345.95344712878176 -8.4734155918210629e-14 -1739.2263576269613
		985.19227964127822 -2.4130250699073314e-13 -1474.444930229354
		1474.4446764107338 -3.6113479296375775e-13 -985.19247000524399
		1739.2262307176502 -4.2598755241195525e-13 -345.95373267472974
		1739.2262307176502 -4.2598755241195525e-13 345.95354231076448
		1474.4446764107338 -3.6113479296375775e-13 985.19247000524399
		985.19240655058877 -2.4130256334978849e-13 1474.4446764107338
		500.55833476224643 -1.2260143179618174e-13 1739.2261038083404
		-0.0016987001481580184 3.1161483066773724e-22 1827.2219736957215
		-0.00096150980305467163 3.632752138975721e-15 2973.7716998216515
		-373.23682309646199 3.1161483066773724e-22 2973.7722074588919
		-525.92458696232279 1.2881438360374002e-13 2657.1113962246186
		-678.61238255551086 1.6621209696758938e-13 2340.4508388089662
		-1175.0967063682047 2.8781569168966765e-13 2134.8003932343486
		-1506.9759744475587 3.6910266712504109e-13 2250.7467696059412
		-1838.8554963455347 4.5038969891946962e-13 2366.6931459775337
		-2366.6918768844312 5.7967227128535875e-13 1838.856765438637
		-2250.745500512839 5.5127367598692586e-13 1506.9774973592814
		-2134.7993779598669 5.2287502432943758e-13 1175.0978485519963
		-2340.4500773531049 5.7324491554167155e-13 678.61352473930287
		-2657.1108885873778 6.5080444395707804e-13 525.92576087344219
		-2973.7714460030311 7.0312790910320923e-13 373.23799700758173
		-2973.7719536402715 7.0312790910320923e-13 -373.23602991327311
		-2657.1113962246186 6.445339354642936e-13 -525.92398414309889
		-2340.4508388089662 5.8593990546632258e-13 -678.61193837292501
		-2134.8003932343486 4.6875193000896372e-13 -1175.0965794588942
		-2250.7465157873207 4.6875193000896372e-13 -1506.9759744475587
		-2366.6928921589129 4.6875193000896372e-13 -1838.8554963455347
		-1838.8565116200159 4.6875193000896372e-13 -2366.6918768844312
		-1506.9768628127308 4.6875193000896372e-13 -2250.7457543314595
		-1175.0973409147555 2.3437596500448186e-13 -2134.7996317784878
		-678.61295364740681 2.3437596500448186e-13 -2340.4503311717249
		-525.92522150887373 2.3437596500448186e-13 -2657.1108885873778
		-373.2374576430131 3.1161483066773724e-22 -2973.7716998216515
		373.23637891387625 -1.1718798250224093e-13 -2973.7722074588919
		525.92426968904704 -1.2881429906515708e-13 -2657.1113962246186
		678.61212873689033 -1.6621204060853406e-13 -2340.4508388089662
		1175.0965794588942 -2.8781566351013995e-13 -2134.8001394157282
		1506.9761013568691 -3.6910266712504109e-13 -2250.7465157873207
		1838.855623254844 -4.5038969891946962e-13 -2366.6926383402924
		2366.692130703052 -5.7967244036252463e-13 -1838.8560039827748
		2250.7460081500794 -5.5127378870503625e-13 -1506.9766089941099
		2134.7998855971077 -5.2287513704754807e-13 -1175.0969601868248
		2340.4505849903453 -5.7324497190072705e-13 -678.61257291947629
		2657.1111424059982 -6.5080450031613333e-13 -525.92484078094299
		2973.7716998216515 -7.2836397237248442e-13 -373.23707691508241
		2973.7722074588919 -7.283641414496502e-13 373.23663273249662
		2657.1113962246186 -6.5080455667518862e-13 525.92449178033996
		2340.4508388089662 -5.7324508461883743e-13 678.61225564620054
		2134.8001394157282 -5.2287519340660336e-13 1175.0967063682047
		2250.7465157873207 -5.5127390142314684e-13 1506.9763551754893
		2366.6926383402924 -5.7967255308063502e-13 1838.8557501641549
		1838.8558770734649 -4.5038983981710806e-13 2366.692384521672
		1506.9766089941099 -3.6910280802267932e-13 2250.7460081500794
		1175.0969601868248 -2.8781574804872299e-13 2134.7998855971077
		678.61244601016597 -1.6621211105735323e-13 2340.4505849903453
		525.92468214430539 -1.2881439769350392e-13 2657.1111424059982
		373.23691827844453 -9.141667023989073e-14 2973.7716998216515
		-0.00096150980305467163 -9.141667023989073e-14 2973.7716998216515
		;
createNode transform -n "Local_CTRL_GRP" -p "Global_CTRL";
	rename -uid "FFC5723C-47FB-E626-CA36-BCAE0B3ABDF1";
createNode transform -n "Local_CTRL_OFFSET" -p "Local_CTRL_GRP";
	rename -uid "3976B902-42F8-55D7-3714-4BA7CFF8CD18";
createNode transform -n "Local_CTRL_SPACE" -p "Local_CTRL_OFFSET";
	rename -uid "37BB2F5E-43C0-E3A1-C05A-92831CB2B2C5";
createNode transform -n "Local_CTRL_MOCAP" -p "Local_CTRL_SPACE";
	rename -uid "1320E938-4FE4-66F0-4A7F-D0BE2CB800DA";
createNode transform -n "Local_CTRL_DRV" -p "Local_CTRL_MOCAP";
	rename -uid "B8E7195E-4414-DE8C-4E95-0D917B242D6A";
createNode transform -n "Local_CTRL" -p "Local_CTRL_DRV";
	rename -uid "58814EE0-45DE-9D02-F764-7CA5B6F2E07B";
	setAttr ".wfcc" -type "float3" 0.068999998 0.377 0.69400001 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.068999998 0.377 0.69400001 ;
createNode nurbsCurve -n "Local_CTRLShape" -p "Local_CTRL";
	rename -uid "D6CCE210-40A8-D0D8-FA91-F39CF451AD87";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.068999998 0.377 0.69400001 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		0.0024299474325695358 2.1784124072666298e-29 -3.7283770936616807e-05
		1409.2922925647333 -3.4517705900296817e-13 -2109.1562492977732
		2109.155312103605 -5.1659406044565691e-13 -1409.2934997320185
		2487.918778434439 -6.0936435353658963e-13 -494.87827148639474
		2487.9189584165215 -6.0936439762615871e-13 494.87774696365369
		2109.1562120140043 -5.1659428083310973e-13 1409.2920752988816
		1409.2931924751329 -3.4517727945081729e-13 2109.1556347839951
		494.87782924294521 -1.212101098912631e-13 2487.9187411506691
		-494.87760426534538 1.2121005480949922e-13 2487.9189211327507
		-1409.2925625378518 3.4517712513732315e-13 2109.1559947481537
		-2109.1556720677645 5.1659414862479648e-13 1409.2927952272019
		-2487.918778434439 6.0936435353658973e-13 494.87797194125289
		-2487.9189584165215 6.0936439762615861e-13 -494.87777653567628
		-2109.1556720677645 5.1659414862479648e-13 -1409.2928697947416
		-1409.2928325109724 3.4517719127167762e-13 -2109.1557093515353
		0.0024299474332400753 2.1784124072666298e-29 -3.7283770936616807e-05
		;
createNode transform -n "Root_CTRL_GRP" -p "Local_CTRL";
	rename -uid "3662C88F-4923-F355-9F84-ACBAC545B042";
createNode transform -n "Root_CTRL_OFFSET" -p "Root_CTRL_GRP";
	rename -uid "42C04CB1-45E3-45B3-35C2-C5BB1C48027B";
createNode transform -n "Root_CTRL_SPACE" -p "Root_CTRL_OFFSET";
	rename -uid "D05E1742-419B-13F8-82D0-7DAA9A9B96DD";
createNode transform -n "Root_CTRL_MOCAP" -p "Root_CTRL_SPACE";
	rename -uid "F3D44619-43C9-E0FF-B87B-0CAA4B3A175B";
createNode transform -n "Root_CTRL_DRV" -p "Root_CTRL_MOCAP";
	rename -uid "D3AC9DCB-47A1-BBC8-8D4E-9883D1183F88";
createNode transform -n "Root_CTRL" -p "Root_CTRL_DRV";
	rename -uid "33ADDE0C-425A-CFCB-EEDD-CC96B216DC58";
	setAttr ".wfcc" -type "float3" 1 1 0.23999999 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 1 0.23999999 ;
createNode nurbsCurve -n "Root_CTRLShape" -p "Root_CTRL";
	rename -uid "BC4421ED-49CB-7F9A-F193-4BA94571E7B8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 1 0.23999999 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 7 0 no 3
		8 0 1 2 3 4 5 6 7
		8
		-444.05115660778921 -4.9299581817739879e-13 -1110.1278915194732
		-444.05115660778921 9.8599163635479836e-14 222.02557830389449
		-888.10231321557842 9.8599163635479836e-14 222.02557830389449
		0 4.9299581817739879e-13 1110.1278915194732
		888.10231321557842 9.8599163635479836e-14 222.02557830389449
		444.05115660778921 9.8599163635479836e-14 222.02557830389449
		444.05115660778921 -4.9299581817739879e-13 -1110.1278915194732
		-444.05115660778921 -4.9299581817739879e-13 -1110.1278915194732
		;
createNode transform -n "Cn_tail" -p "RIG";
	rename -uid "E77691EA-41CB-291F-6AF7-11A0A3BCD095";
createNode transform -n "Cn_tail_MODULE" -p "Cn_tail";
	rename -uid "7BBF4A46-4DBD-3228-A6AC-86B1E5F187E7";
createNode transform -n "Cn_tail_MODULE_FK" -p "Cn_tail_MODULE";
	rename -uid "9260A595-47BA-9172-76FE-CB8A03DAD2B4";
createNode joint -n "FK_Tail_01" -p "Cn_tail_MODULE_FK";
	rename -uid "3389A8A9-468E-5EA0-4FA6-CBBB616552BD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -28.351999999999997 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.88004672214001534 -0.47488710958565156 0
		 0 0.47488710958565156 0.88004672214001534 0 0 4982.0039999999999 -421.351 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_01";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_02" -p "FK_Tail_01";
	rename -uid "C5426DB2-4102-219C-787E-F690E72BA0DF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.4830000000000032 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.90727168381510193 -0.42054499372517762 0
		 0 0.42054499372517762 0.90727168381510193 0 0 4636.9557750461609 -1060.7841478397138 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_02";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_03" -p "FK_Tail_02";
	rename -uid "54FA6ED8-4D58-AA1B-5334-7C985DC67C69";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.762999999999999 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.95576221772681114 -0.29414041403031932 0
		 0 0.29414041403031932 0.95576221772681114 0 0 3547.058752958179 -3412.0966617654467 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_03";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_04" -p "FK_Tail_03";
	rename -uid "2DD3FC5F-4347-FB54-EC36-AC95D16A0B47";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 6.585 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.98318804871343368 -0.18259589498964846 0
		 0 0.18259589498964846 0.98318804871343368 0 0 2918.3615613077045 -5454.9476047458211 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_04";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_05" -p "FK_Tail_04";
	rename -uid "87394C3C-4506-A2F8-D278-80A65D4C3AE0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.382 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99930321969331304 -0.037323921425515355 0
		 0 0.037323921425515355 0.99930321969331304 0 0 2410.405710063591 -8190.0371435636771 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_05";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_06" -p "FK_Tail_05";
	rename -uid "2092CC6F-400A-5751-F87C-2285C20A498B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.6540000000000004 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99965043760887784 0.026438657083501266 0
		 0 -0.026438657083501266 0.99965043760887784 0 0 2293.1700785005614 -11328.880534323403 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_06";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_07" -p "FK_Tail_06";
	rename -uid "16226331-4CAB-6BD3-0CFF-548269C4D2D6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.68700000000000039 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99926157581451325 0.038422689920094552 0
		 0 -0.038422689920094552 0.99926157581451325 0 0 2369.2360513904187 -14204.948817456529 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_07";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode joint -n "FK_Tail_08" -p "FK_Tail_07";
	rename -uid "2E7A3919-42CC-48F2-E423-72BDD7DED4D6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.975693351829396e-16 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99926157581451325 0.038422689920094552 0
		 0 -0.038422689920094552 0.99926157581451325 0 0 2506.1545000441874 -17765.796458378456 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Tail_08";
	setAttr ".radi" 212.70000000000002;
	setAttr ".liw" yes;
createNode pointConstraint -n "FK_Tail_08_pointConstraint1" -p "FK_Tail_08";
	rename -uid "C8A3BC41-4373-FD40-785F-8E949A376916";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_08_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 2.0463630789890885e-12 -3563.4789999999648 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_08_orientConstraint1" -p "FK_Tail_08";
	rename -uid "26CF7553-4482-E327-DDF5-C79E1025F2AF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_08_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_07_pointConstraint1" -p "FK_Tail_07";
	rename -uid "DAD9291B-4706-4C08-DEAB-E5BADA5CEAB3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_07_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 -6.1390892369672656e-12 -2877.0740000000042 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_07_orientConstraint1" -p "FK_Tail_07";
	rename -uid "A0D8C23F-4418-E531-8734-7CAFF309D710";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_07_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -2.981770013872047e-16 0 0 ;
	setAttr ".rsrr" -type "double3" 3.975693351829396e-16 0 0 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_06_pointConstraint1" -p "FK_Tail_06";
	rename -uid "BCF27E9A-498C-DA4B-E66D-3C8E01F94CED";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_06_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 1.3642420526593924e-12 -3141.0319999999938 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_06_orientConstraint1" -p "FK_Tail_06";
	rename -uid "23B8842D-4A5D-B4C8-EDC2-7CAC38342803";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_06_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 1.5902773407317584e-15 0 0 ;
	setAttr ".rsrr" -type "double3" 1.5902773407317584e-15 0 0 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_05_pointConstraint1" -p "FK_Tail_05";
	rename -uid "0D070817-4166-1E07-BA2B-F39F179CED73";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_05_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 2.2737367544323206e-12 -2781.858000000002 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_05_orientConstraint1" -p "FK_Tail_05";
	rename -uid "D71D2E68-4D8B-2A7D-CFF2-4DB70016001A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_05_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -1.5902773407317584e-15 0 0 ;
	setAttr ".rsrr" -type "double3" -1.5902773407317584e-15 0 0 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_04_pointConstraint1" -p "FK_Tail_04";
	rename -uid "53EAF260-4463-CCF6-F0A3-9884184ECC77";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_04_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 -2.7284841053187847e-12 -2137.4049999999988 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_04_orientConstraint1" -p "FK_Tail_04";
	rename -uid "B22C2CDA-4D38-DDA8-EBEB-79AACCEAEE30";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_04_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_03_pointConstraint1" -p "FK_Tail_03";
	rename -uid "FEE8E685-4CE6-B3B3-1B98-90BC44EAC5C9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_03_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 1.8189894035458565e-12 -2591.6300000000056 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_03_orientConstraint1" -p "FK_Tail_03";
	rename -uid "AEDEE9A3-4C39-297A-FFD4-C89A9D6811E2";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_03_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -6.3611093629270335e-15 0 0 ;
	setAttr ".rsrr" -type "double3" -6.3611093629270335e-15 0 0 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_02_pointConstraint1" -p "FK_Tail_02";
	rename -uid "084E24F1-4FE7-9DA4-4E77-CF827FF8FD51";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_02_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 -9.0949470177292824e-13 -726.58999999999787 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_02_orientConstraint1" -p "FK_Tail_02";
	rename -uid "15CF4E0B-46AC-1982-63EC-2E9E2DE3134D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_02_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -6.7586786981099735e-15 0 0 ;
	setAttr ".rsrr" -type "double3" -6.7586786981099735e-15 0 0 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "FK_Tail_01_pointConstraint1" -p "FK_Tail_01";
	rename -uid "99B79656-4005-E291-0B12-CAB46A0176A1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_01_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 0 4982.0039999999999 -421.351 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "FK_Tail_01_orientConstraint1" -p "FK_Tail_01";
	rename -uid "EAB47925-4407-20CC-40A2-75B0CCF5CEB4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_01_CTRLW0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -3.1805546814635168e-15 0 0 ;
	setAttr ".rsrr" -type "double3" -3.1805546814635168e-15 0 0 ;
	setAttr -k on ".w0";
createNode transform -n "Cn_tail_CONTROL" -p "Cn_tail";
	rename -uid "DA49CAC4-42A3-256D-664F-95A411B9AD15";
createNode transform -n "Cn_tail_CONTROL_FK" -p "Cn_tail_CONTROL";
	rename -uid "534F9BD3-4556-6450-22D2-C68FBB9154ED";
createNode transform -n "FK_Tail_01_CTRL_GRP" -p "Cn_tail_CONTROL_FK";
	rename -uid "1D33B000-4A55-02A4-78F6-F8A1D8CEEC1D";
	setAttr ".t" -type "double3" 0 4982.0039999999999 -421.351 ;
	setAttr ".r" -type "double3" -28.352 0 0 ;
createNode transform -n "FK_Tail_01_CTRL_OFFSET" -p "FK_Tail_01_CTRL_GRP";
	rename -uid "DAED4F13-444D-04E0-E53B-A8A24433D39F";
createNode transform -n "FK_Tail_01_CTRL_SPACE" -p "FK_Tail_01_CTRL_OFFSET";
	rename -uid "249B0D55-4732-064D-484F-8BBC75196A5B";
createNode transform -n "FK_Tail_01_CTRL_MOCAP" -p "FK_Tail_01_CTRL_SPACE";
	rename -uid "66472B13-4717-CEBE-3034-CFAAD8831843";
createNode transform -n "FK_Tail_01_CTRL_DRV" -p "FK_Tail_01_CTRL_MOCAP";
	rename -uid "A621EE62-47D8-0479-330C-0DBA3A3B6D9A";
createNode transform -n "FK_Tail_01_CTRL" -p "FK_Tail_01_CTRL_DRV";
	rename -uid "2319BF29-4364-2309-1E5E-629E99EEFCA1";
	addAttr -ci true -k true -sn "rotChildren" -ln "rotChildren" -at "double";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr -k on ".rotChildren";
createNode nurbsCurve -n "FK_Tail_01_CTRLShape" -p "FK_Tail_01_CTRL";
	rename -uid "2F030C68-4777-D1AD-A6A2-2BB8AE84AB11";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-1000 1000 1000
		-1000 1000 -1000
		1000 1000 -1000
		1000 1000 1000
		-1000 1000 1000
		-1000 -1000 1000
		-1000 -1000 -1000
		-1000 1000 -1000
		1000 1000 -1000
		1000 -1000 -1000
		-1000 -1000 -1000
		-1000 -1000 1000
		1000 -1000 1000
		1000 -1000 -1000
		1000 1000 -1000
		1000 1000 1000
		1000 -1000 1000
		;
createNode nurbsCurve -n "FK_Tail_01_CTRLShape_" -p "FK_Tail_01_CTRL";
	rename -uid "83D66282-4867-E84A-C0CB-A2BC553A7071";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 860.57445480537763 8.8667363446472557e-14
		0 860.57445480537763 -430.28722740269029
		0 -2.8662887223875245e-12 1.9405733859701132e-13
		0 860.57445480537763 430.28722740269046
		0 860.57445480537763 8.8667363446472557e-14
		0 3012.0105918188301 -1.7480757442987453e-13
		0 3027.0456881187351 111.24947178328323
		0 3070.0055649026194 214.96203249138111
		0 3138.0363421347356 304.26126194317101
		0 3227.3358943019462 372.29257703432131
		0 3331.0482398664303 415.25170081555797
		0 3442.2978440308061 430.29045455689561
		0 3553.5472910048038 415.25170081555797
		0 3657.2598517129022 372.29257703432131
		0 3746.5590811646912 304.26126194317095
		0 3814.5903962558414 214.96203249138097
		0 3857.5495200370783 111.24947178328316
		0 3872.5882737784164 -2.8019794479282008e-13
		0 3857.5495200370783 -111.24947178328368
		0 3814.5903962558414 -214.96203249138156
		0 3746.5590811646912 -304.26126194317146
		0 3657.2598517129013 -372.29257703432177
		0 3553.5472910048038 -415.25170081555848
		0 3442.2978440308061 -430.29045455689612
		0 3331.0482398664303 -415.25170081555848
		0 3227.3358943019462 -372.29257703432177
		0 3138.0363421347356 -304.26126194317141
		0 3070.0055649026194 -214.96203249138142
		0 3027.0456881187351 -111.2494717832836
		0 3012.0105918188301 -1.7480757442987453e-13
		;
createNode transform -n "FK_Tail_02_CTRL_GRP" -p "FK_Tail_01_CTRL";
	rename -uid "47B65270-4E52-CBBF-298F-1C8E7C9C50A1";
	setAttr ".t" -type "double3" 0 -9.0949470177292824e-13 -726.58999999999833 ;
	setAttr ".r" -type "double3" 3.482999999999997 0 0 ;
createNode transform -n "FK_Tail_02_CTRL_OFFSET" -p "FK_Tail_02_CTRL_GRP";
	rename -uid "8D1E2A95-4137-612A-941E-F989FDA15403";
createNode transform -n "FK_Tail_02_CTRL_SPACE" -p "FK_Tail_02_CTRL_OFFSET";
	rename -uid "6379B068-4A6A-0E7C-0AEE-B9B7603F2347";
createNode transform -n "FK_Tail_02_CTRL_MOCAP" -p "FK_Tail_02_CTRL_SPACE";
	rename -uid "8BA797C6-4723-41BC-FCA7-03A110DB396E";
createNode transform -n "FK_Tail_02_CTRL_DRV" -p "FK_Tail_02_CTRL_MOCAP";
	rename -uid "52394DDC-47BD-2D22-1853-2C997DB62F59";
createNode transform -n "FK_Tail_02_CTRL" -p "FK_Tail_02_CTRL_DRV";
	rename -uid "F362CD8D-4D2B-7A47-6239-D3BB57275E1E";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_02_CTRLShape" -p "FK_Tail_02_CTRL";
	rename -uid "5079F343-49CA-E8DB-E646-EF89450732A7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-910 910 910
		-910 910 -910
		910 910 -910
		910 910 910
		-910 910 910
		-910 -910 910
		-910 -910 -910
		-910 910 -910
		910 910 -910
		910 -910 -910
		-910 -910 -910
		-910 -910 910
		910 -910 910
		910 -910 -910
		910 910 -910
		910 910 910
		910 -910 910
		;
createNode nurbsCurve -n "FK_Tail_02_CTRLShape_" -p "FK_Tail_02_CTRL";
	rename -uid "030C1EDE-46FA-A9C3-4FF2-94875E115A7D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 783.12275387289367 8.0687300736290029e-14
		0 783.12275387289367 -391.5613769364482
		0 -2.6083227373726472e-12 1.7659217812328031e-13
		0 783.12275387289367 391.56137693644837
		0 783.12275387289367 8.0687300736290029e-14
		0 2740.9296385551352 -1.5907489273118581e-13
		0 2754.6115761880487 101.23701932278775
		0 2793.7050640613838 195.61544956715679
		0 2855.6130713426096 276.87774836828561
		0 2936.8756638147711 338.7862451012324
		0 3031.2538982784517 377.87904774215775
		0 3132.4910380680335 391.56431364677502
		0 3233.7280348143713 377.87904774215775
		0 3328.1064650587409 338.7862451012324
		0 3409.368763859869 276.87774836828555
		0 3471.2772605928158 195.61544956715667
		0 3510.3700632337413 101.23701932278766
		0 3524.055329138359 -2.5498012976146629e-13
		0 3510.3700632337413 -101.23701932278814
		0 3471.2772605928158 -195.61544956715724
		0 3409.368763859869 -276.87774836828606
		0 3328.10646505874 -338.78624510123279
		0 3233.7280348143713 -377.87904774215821
		0 3132.4910380680335 -391.56431364677547
		0 3031.2538982784517 -377.87904774215821
		0 2936.8756638147711 -338.78624510123279
		0 2855.6130713426096 -276.87774836828595
		0 2793.7050640613838 -195.6154495671571
		0 2754.6115761880487 -101.23701932278807
		0 2740.9296385551352 -1.5907489273118581e-13
		;
createNode transform -n "FK_Tail_03_CTRL_GRP" -p "FK_Tail_02_CTRL";
	rename -uid "EC67FE23-4ED2-1CF3-AEA7-AEBDAF549E42";
	setAttr ".t" -type "double3" 0 1.8189894035458565e-12 -2591.6300000000047 ;
	setAttr ".r" -type "double3" 7.7629999999999981 0 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999989 0.99999999999999989 ;
createNode transform -n "FK_Tail_03_CTRL_OFFSET" -p "FK_Tail_03_CTRL_GRP";
	rename -uid "C86D1E1C-4670-B3E5-BACF-E4B5269396B8";
createNode transform -n "FK_Tail_03_CTRL_SPACE" -p "FK_Tail_03_CTRL_OFFSET";
	rename -uid "560CD0A8-4682-94A7-819A-AAAEEBA8F1A7";
createNode transform -n "FK_Tail_03_CTRL_MOCAP" -p "FK_Tail_03_CTRL_SPACE";
	rename -uid "52903038-42DE-3C8C-43CA-6BBBA96C9A83";
createNode transform -n "FK_Tail_03_CTRL_DRV" -p "FK_Tail_03_CTRL_MOCAP";
	rename -uid "F3F2A3B0-4D00-3C86-0D01-74BF88EB2A32";
createNode transform -n "FK_Tail_03_CTRL" -p "FK_Tail_03_CTRL_DRV";
	rename -uid "0C8213C6-48E8-EA4A-6B07-BEAD5EBD0586";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_03_CTRLShape" -p "FK_Tail_03_CTRL";
	rename -uid "23326A03-4765-1EAA-7BC5-80B8BF1468C4";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-820 820 820
		-820 820 -820
		820 820 -820
		820 820 820
		-820 820 820
		-820 -820 820
		-820 -820 -820
		-820 820 -820
		820 820 -820
		820 -820 -820
		-820 -820 -820
		-820 -820 820
		820 -820 820
		820 -820 -820
		820 820 -820
		820 820 820
		820 -820 820
		;
createNode nurbsCurve -n "FK_Tail_03_CTRLShape_" -p "FK_Tail_03_CTRL";
	rename -uid "FFE2363C-4632-A88F-E53E-88B2F4410D9D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 705.67105294040971 7.2707238026107489e-14
		0 705.67105294040971 -352.83552647020605
		0 -2.3503567523577699e-12 1.5912701764954928e-13
		0 705.67105294040971 352.83552647020622
		0 705.67105294040971 7.2707238026107489e-14
		0 2469.8486852914407 -1.4334221103249709e-13
		0 2482.1774642573628 91.224566862292249
		0 2517.4045632201478 176.26886664293249
		0 2573.1898005504831 249.49423479340021
		0 2646.415433327596 305.27991316814348
		0 2731.4595566904727 340.50639466875754
		0 2822.6842321052609 352.83817273665443
		0 2913.9087786239393 340.50639466875754
		0 2998.9530784045796 305.27991316814348
		0 3072.1784465550468 249.49423479340015
		0 3127.9641249297902 176.26886664293238
		0 3163.1906064304044 91.224566862292178
		0 3175.5223844983016 -2.297623147301125e-13
		0 3163.1906064304044 -91.224566862292619
		0 3127.9641249297902 -176.26886664293289
		0 3072.1784465550468 -249.49423479340061
		0 2998.9530784045792 -305.27991316814388
		0 2913.9087786239393 -340.50639466875793
		0 2822.6842321052609 -352.83817273665483
		0 2731.4595566904727 -340.50639466875793
		0 2646.415433327596 -305.27991316814388
		0 2573.1898005504831 -249.49423479340052
		0 2517.4045632201478 -176.26886664293278
		0 2482.1774642573628 -91.224566862292548
		0 2469.8486852914407 -1.4334221103249709e-13
		;
createNode transform -n "FK_Tail_04_CTRL_GRP" -p "FK_Tail_03_CTRL";
	rename -uid "3109706B-4B1F-6D0E-3F7C-E1B9418873A2";
	setAttr ".t" -type "double3" 0 -3.637978807091713e-12 -2137.4049999999988 ;
	setAttr ".r" -type "double3" 6.5850000000000062 0 0 ;
createNode transform -n "FK_Tail_04_CTRL_OFFSET" -p "FK_Tail_04_CTRL_GRP";
	rename -uid "B3BE8161-47E3-F01D-E960-F6B2CE87AB0C";
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode transform -n "FK_Tail_04_CTRL_SPACE" -p "FK_Tail_04_CTRL_OFFSET";
	rename -uid "5B3E9B29-4CA3-CDAF-4AFD-1FB801F8BBB8";
	setAttr ".s" -type "double3" 1 0.99999999999999967 0.99999999999999967 ;
createNode transform -n "FK_Tail_04_CTRL_MOCAP" -p "FK_Tail_04_CTRL_SPACE";
	rename -uid "2CBE868F-48D4-4B43-F28A-75B2B0811965";
	setAttr ".t" -type "double3" 0 0 -9.0949470177292824e-13 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode transform -n "FK_Tail_04_CTRL_DRV" -p "FK_Tail_04_CTRL_MOCAP";
	rename -uid "E438C310-4124-6D75-68BE-20ACBA61E092";
	setAttr ".t" -type "double3" 0 0 1.8189894035458565e-12 ;
	setAttr ".s" -type "double3" 1 0.99999999999999978 0.99999999999999978 ;
createNode transform -n "FK_Tail_04_CTRL" -p "FK_Tail_04_CTRL_DRV";
	rename -uid "17A244EC-4AD1-6C3C-75AD-B69DC12E6F86";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 0 -1.8189894035458565e-12 ;
	setAttr -k on ".ro";
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_04_CTRLShape" -p "FK_Tail_04_CTRL";
	rename -uid "945428ED-4EBE-AB23-8FFA-17A89E28CD89";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-730 730 730
		-730 730 -730
		730 730 -730
		730 730 730
		-730 730 730
		-730 -730 730
		-730 -730 -730
		-730 730 -730
		730 730 -730
		730 -730 -730
		-730 -730 -730
		-730 -730 730
		730 -730 730
		730 -730 -730
		730 730 -730
		730 730 730
		730 -730 730
		;
createNode nurbsCurve -n "FK_Tail_04_CTRLShape_" -p "FK_Tail_04_CTRL";
	rename -uid "404820AF-49D0-790C-C471-CBBB66F679BE";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 628.21935200792564 6.4727175315924962e-14
		0 628.21935200792564 -314.10967600396395
		0 -2.0923907673428926e-12 1.4166185717581828e-13
		0 628.21935200792564 314.10967600396407
		0 628.21935200792564 6.4727175315924962e-14
		0 2198.7677320277458 -1.276095293338084e-13
		0 2209.7433523266768 81.212114401796754
		0 2241.1040623789122 156.9222837187082
		0 2290.7665297583571 222.11072121851481
		0 2355.955202840421 271.77358123505456
		0 2431.6652151024941 303.13374159535732
		0 2512.8774261424883 314.11203182653384
		0 2594.0895224335068 303.13374159535732
		0 2669.7996917504188 271.77358123505456
		0 2734.9881292502246 222.11072121851478
		0 2784.6509892667641 156.92228371870812
		0 2816.0111496270674 81.212114401796697
		0 2826.9894398582437 -2.0454449969875869e-13
		0 2816.0111496270674 -81.212114401797081
		0 2784.6509892667641 -156.92228371870854
		0 2734.9881292502246 -222.11072121851518
		0 2669.7996917504179 -271.77358123505491
		0 2594.0895224335068 -303.13374159535766
		0 2512.8774261424883 -314.11203182653418
		0 2431.6652151024941 -303.13374159535766
		0 2355.955202840421 -271.77358123505491
		0 2290.7665297583571 -222.1107212185151
		0 2241.1040623789122 -156.92228371870846
		0 2209.7433523266768 -81.212114401797024
		0 2198.7677320277458 -1.276095293338084e-13
		;
createNode transform -n "FK_Tail_05_CTRL_GRP" -p "FK_Tail_04_CTRL";
	rename -uid "0F80515C-4B72-2F33-F523-F6A9CCB79DED";
	setAttr ".t" -type "double3" 0 2.7284841053187847e-12 -2781.8580000000029 ;
	setAttr ".r" -type "double3" 8.3819999999999979 0 0 ;
createNode transform -n "FK_Tail_05_CTRL_OFFSET" -p "FK_Tail_05_CTRL_GRP";
	rename -uid "A0370689-46DA-A9CF-6791-AB87C23189CB";
	setAttr ".t" -type "double3" 0 -4.5474735088646412e-13 0 ;
createNode transform -n "FK_Tail_05_CTRL_SPACE" -p "FK_Tail_05_CTRL_OFFSET";
	rename -uid "EDDD85D7-4083-D13A-8EA9-80BE50DEBE29";
createNode transform -n "FK_Tail_05_CTRL_MOCAP" -p "FK_Tail_05_CTRL_SPACE";
	rename -uid "EF8CC5DF-4961-85FB-F6D6-F6826BD5ABC2";
createNode transform -n "FK_Tail_05_CTRL_DRV" -p "FK_Tail_05_CTRL_MOCAP";
	rename -uid "BC1AE6FB-4375-F307-8251-F987D2EE0384";
createNode transform -n "FK_Tail_05_CTRL" -p "FK_Tail_05_CTRL_DRV";
	rename -uid "D167C39E-436D-E00C-83EA-1F996910E554";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_05_CTRLShape" -p "FK_Tail_05_CTRL";
	rename -uid "B43D0AB8-45E5-25BF-E4CF-7B8F89E43C93";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-640 640 640
		-640 640 -640
		640 640 -640
		640 640 640
		-640 640 640
		-640 -640 640
		-640 -640 -640
		-640 640 -640
		640 640 -640
		640 -640 -640
		-640 -640 -640
		-640 -640 640
		640 -640 640
		640 -640 -640
		640 640 -640
		640 640 640
		640 -640 640
		;
createNode nurbsCurve -n "FK_Tail_05_CTRLShape_" -p "FK_Tail_05_CTRL";
	rename -uid "F19CB676-4838-01AC-C86E-3CA98B110071";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 550.76765107544168 5.6747112605742434e-14
		0 550.76765107544168 -275.3838255377218
		0 -1.8344247823280158e-12 1.2419669670208725e-13
		0 550.76765107544168 275.38382553772192
		0 550.76765107544168 5.6747112605742434e-14
		0 1927.6867787640513 -1.1187684763511968e-13
		0 1937.3092403959904 71.199661941301272
		0 1964.8035615376764 137.57570079448391
		0 2008.3432589662309 194.72720764362944
		0 2065.4949723532454 238.26724930196565
		0 2131.8708735145156 265.76108852195711
		0 2203.0706201797157 275.38589091641319
		0 2274.2702662430743 265.76108852195711
		0 2340.6463050962575 238.26724930196565
		0 2397.7978119454024 194.72720764362941
		0 2441.3378536037385 137.57570079448382
		0 2468.83169282373 71.199661941301216
		0 2478.4564952181863 -1.7932668466740487e-13
		0 2468.83169282373 -71.199661941301557
		0 2441.3378536037385 -137.57570079448419
		0 2397.7978119454024 -194.72720764362975
		0 2340.646305096257 -238.26724930196593
		0 2274.2702662430743 -265.76108852195739
		0 2203.0706201797157 -275.38589091641353
		0 2131.8708735145156 -265.76108852195739
		0 2065.4949723532454 -238.26724930196593
		0 2008.3432589662309 -194.7272076436297
		0 1964.8035615376764 -137.57570079448411
		0 1937.3092403959904 -71.1996619413015
		0 1927.6867787640513 -1.1187684763511968e-13
		;
createNode transform -n "FK_Tail_06_CTRL_GRP" -p "FK_Tail_05_CTRL";
	rename -uid "E83AE8FB-4D15-8333-9302-FFA0BD0928A3";
	setAttr ".t" -type "double3" 0 2.2737367544323206e-12 -3141.0319999999947 ;
	setAttr ".r" -type "double3" 3.6540000000000044 0 0 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode transform -n "FK_Tail_06_CTRL_OFFSET" -p "FK_Tail_06_CTRL_GRP";
	rename -uid "27369243-41F9-6C84-EFB6-EC8BEBABE848";
	setAttr ".t" -type "double3" 0 -2.2737367544323206e-13 0 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode transform -n "FK_Tail_06_CTRL_SPACE" -p "FK_Tail_06_CTRL_OFFSET";
	rename -uid "6BCEA24E-4155-EE0D-F094-7C91981C73BD";
	setAttr ".s" -type "double3" 1 0.99999999999999967 0.99999999999999967 ;
createNode transform -n "FK_Tail_06_CTRL_MOCAP" -p "FK_Tail_06_CTRL_SPACE";
	rename -uid "A947D0C4-4D93-C93E-8258-57968FA9E6C3";
	setAttr ".t" -type "double3" 0 2.2737367544323206e-13 -1.8189894035458565e-12 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode transform -n "FK_Tail_06_CTRL_DRV" -p "FK_Tail_06_CTRL_MOCAP";
	rename -uid "FE1737C7-4F4E-C9D0-961F-BABDC1FA7DE9";
	setAttr ".t" -type "double3" 0 -6.8212102632969618e-13 1.8189894035458565e-12 ;
createNode transform -n "FK_Tail_06_CTRL" -p "FK_Tail_06_CTRL_DRV";
	rename -uid "37075CF1-481F-7F61-F7FA-D28A57B9960D";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 2.2737367544323206e-13 0 ;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_06_CTRLShape" -p "FK_Tail_06_CTRL";
	rename -uid "7C9ED9A2-4F33-C9C5-3437-B29564A1FDF3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-550 550 550
		-550 550 -550
		550 550 -550
		550 550 550
		-550 550 550
		-550 -550 550
		-550 -550 -550
		-550 550 -550
		550 550 -550
		550 -550 -550
		-550 -550 -550
		-550 -550 550
		550 -550 550
		550 -550 -550
		550 550 -550
		550 550 550
		550 -550 550
		;
createNode nurbsCurve -n "FK_Tail_06_CTRLShape_" -p "FK_Tail_06_CTRL";
	rename -uid "46BFAD2E-43B8-44AD-3FC6-0CA4C34B3834";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 473.31595014295772 4.8767049895559907e-14
		0 473.31595014295772 -236.65797507147968
		0 -1.5764587973131383e-12 1.0673153622835623e-13
		0 473.31595014295772 236.65797507147977
		0 473.31595014295772 4.8767049895559907e-14
		0 1656.6058255003566 -9.6144165936430978e-14
		0 1664.8751284653042 61.187209480805777
		0 1688.5030606964408 118.2291178702596
		0 1725.9199881741047 167.34369406874404
		0 1775.0347418660706 204.76091736887673
		0 1832.0765319265367 228.38843544855686
		0 1893.2638142169433 236.6597500062926
		0 1954.451010052642 228.38843544855686
		0 2011.4929184420962 204.76091736887673
		0 2060.6074946405802 167.34369406874401
		0 2098.0247179407129 118.22911787025953
		0 2121.652236020393 61.187209480805734
		0 2129.9235505781289 -1.5410886963605106e-13
		0 2121.652236020393 -61.187209480806025
		0 2098.0247179407129 -118.22911787025987
		0 2060.6074946405802 -167.34369406874433
		0 2011.4929184420957 -204.76091736887699
		0 1954.451010052642 -228.38843544855715
		0 1893.2638142169433 -236.65975000629288
		0 1832.0765319265367 -228.38843544855715
		0 1775.0347418660706 -204.76091736887699
		0 1725.9199881741047 -167.34369406874427
		0 1688.5030606964408 -118.22911787025978
		0 1664.8751284653042 -61.187209480805976
		0 1656.6058255003566 -9.6144165936430978e-14
		;
createNode transform -n "FK_Tail_07_CTRL_GRP" -p "FK_Tail_06_CTRL";
	rename -uid "AA488377-4320-A12B-2AB1-D0BD0C905424";
	setAttr ".t" -type "double3" 0 -5.0022208597511053e-12 -2877.0740000000023 ;
	setAttr ".r" -type "double3" 0.68699999999999872 0 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999944 0.99999999999999944 ;
createNode transform -n "FK_Tail_07_CTRL_OFFSET" -p "FK_Tail_07_CTRL_GRP";
	rename -uid "F819877F-43D6-3B84-0B8B-2FAC60C4CF72";
createNode transform -n "FK_Tail_07_CTRL_SPACE" -p "FK_Tail_07_CTRL_OFFSET";
	rename -uid "F24A3891-43DA-5F80-CC1E-A488A1C3F2CE";
createNode transform -n "FK_Tail_07_CTRL_MOCAP" -p "FK_Tail_07_CTRL_SPACE";
	rename -uid "7579CF8D-40CF-8590-2951-A6BBCB9FDD5D";
createNode transform -n "FK_Tail_07_CTRL_DRV" -p "FK_Tail_07_CTRL_MOCAP";
	rename -uid "86472F7F-4206-4313-538E-59BF11F92481";
createNode transform -n "FK_Tail_07_CTRL" -p "FK_Tail_07_CTRL_DRV";
	rename -uid "320135B1-4A1D-3F5D-AA26-09A2961DBC45";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_07_CTRLShape" -p "FK_Tail_07_CTRL";
	rename -uid "0C4A8C8B-4118-1358-138A-DE843543F9EF";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-460 460 460
		-460 460 -460
		460 460 -460
		460 460 460
		-460 460 460
		-460 -460 460
		-460 -460 -460
		-460 460 -460
		460 460 -460
		460 -460 -460
		-460 -460 -460
		-460 -460 460
		460 -460 460
		460 -460 -460
		460 460 -460
		460 460 460
		460 -460 460
		;
createNode nurbsCurve -n "FK_Tail_07_CTRLShape_" -p "FK_Tail_07_CTRL";
	rename -uid "1626D317-4DE1-6D72-8552-E6B502F3A384";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 395.8642492104737 4.0786987185377373e-14
		0 395.8642492104737 -197.93212460523756
		0 -1.3184928122982612e-12 8.926637575462521e-14
		0 395.8642492104737 197.93212460523762
		0 395.8642492104737 4.0786987185377373e-14
		0 1385.5248722366618 -8.0411484237742273e-14
		0 1392.441016534618 51.174757020310288
		0 1412.202559855205 98.882534946035307
		0 1443.4967173819784 139.96018049385864
		0 1484.5745113788953 171.25458543578782
		0 1532.2821903385579 191.01578237515665
		0 1583.4570082541709 197.93360909617198
		0 1634.6317538622097 191.01578237515665
		0 1682.3395317879351 171.25458543578782
		0 1723.417177335758 139.96018049385864
		0 1754.7115822776871 98.882534946035236
		0 1774.4727792170561 51.174757020310246
		0 1781.3906059380715 -1.2889105460469724e-13
		0 1774.4727792170561 -51.174757020310494
		0 1754.7115822776871 -98.88253494603552
		0 1723.417177335758 -139.9601804938589
		0 1682.3395317879347 -171.25458543578802
		0 1634.6317538622097 -191.0157823751569
		0 1583.4570082541709 -197.93360909617223
		0 1532.2821903385579 -191.0157823751569
		0 1484.5745113788953 -171.25458543578802
		0 1443.4967173819784 -139.96018049385884
		0 1412.202559855205 -98.882534946035463
		0 1392.441016534618 -51.174757020310452
		0 1385.5248722366618 -8.0411484237742273e-14
		;
createNode transform -n "FK_Tail_08_CTRL_GRP" -p "FK_Tail_07_CTRL";
	rename -uid "E3110B79-4B81-49E0-574A-2E8F96588028";
	setAttr ".t" -type "double3" 0 2.0463630789890885e-12 -3563.4789999999684 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode transform -n "FK_Tail_08_CTRL_OFFSET" -p "FK_Tail_08_CTRL_GRP";
	rename -uid "F3D3FF12-4684-C47E-CC7E-FCBAB679FF66";
createNode transform -n "FK_Tail_08_CTRL_SPACE" -p "FK_Tail_08_CTRL_OFFSET";
	rename -uid "83CA2103-497A-5032-13DB-73B7C826948D";
createNode transform -n "FK_Tail_08_CTRL_MOCAP" -p "FK_Tail_08_CTRL_SPACE";
	rename -uid "16B16723-4C23-EF95-FEC4-26BC35C03118";
createNode transform -n "FK_Tail_08_CTRL_DRV" -p "FK_Tail_08_CTRL_MOCAP";
	rename -uid "7C21EEB4-4CD8-D267-0FDC-85933619537C";
createNode transform -n "FK_Tail_08_CTRL" -p "FK_Tail_08_CTRL_DRV";
	rename -uid "DBA6D3AD-4EBA-6A28-E549-2BA8299D6393";
	setAttr ".wfcc" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".uoc" 2;
	setAttr -k on ".ro";
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 0.69999999 0.69999999 0.1 ;
createNode nurbsCurve -n "FK_Tail_08_CTRLShape" -p "FK_Tail_08_CTRL";
	rename -uid "696B6262-48D3-5AC0-5490-DC8F5C4B2B17";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-370 370 370
		-370 370 -370
		370 370 -370
		370 370 370
		-370 370 370
		-370 -370 370
		-370 -370 -370
		-370 370 -370
		370 370 -370
		370 -370 -370
		-370 -370 -370
		-370 -370 370
		370 -370 370
		370 -370 -370
		370 370 -370
		370 370 370
		370 -370 370
		;
createNode nurbsCurve -n "FK_Tail_08_CTRLShape_" -p "FK_Tail_08_CTRL";
	rename -uid "4E9069DF-46E7-D695-5467-F193640C241C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.69999999 0.69999999 0.1 ;
	setAttr ".ls" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 29 0 no 3
		30 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29
		30
		0 318.41254827798974 3.2806924475194846e-14
		0 318.41254827798974 -159.20627413899541
		0 -1.0605268272833839e-12 7.1801215280894192e-14
		0 318.41254827798974 159.20627413899547
		0 318.41254827798974 3.2806924475194846e-14
		0 1114.4439189729671 -6.4678802539053569e-14
		0 1120.0069046039321 41.162304559814793
		0 1135.9020590139692 79.535952021811013
		0 1161.0734465898522 112.57666691897326
		0 1194.1142808917202 137.7482535026989
		0 1232.4878487505791 153.64312930175643
		0 1273.6502022913983 159.20746818605139
		0 1314.8124976717775 153.64312930175643
		0 1353.1861451337738 137.7482535026989
		0 1386.2268600309358 112.57666691897325
		0 1411.3984466146612 79.535952021810957
		0 1427.2933224137189 41.162304559814764
		0 1432.8576612980141 -1.0367323957334344e-13
		0 1427.2933224137189 -41.162304559814963
		0 1411.3984466146612 -79.535952021811184
		0 1386.2268600309358 -112.57666691897344
		0 1353.1861451337736 -137.74825350269907
		0 1314.8124976717775 -153.64312930175663
		0 1273.6502022913983 -159.20746818605156
		0 1232.4878487505791 -153.64312930175663
		0 1194.1142808917202 -137.74825350269907
		0 1161.0734465898522 -112.57666691897342
		0 1135.9020590139692 -79.535952021811127
		0 1120.0069046039321 -41.162304559814928
		0 1114.4439189729671 -6.4678802539053569e-14
		;
createNode transform -n "SKEL" -p "CHAR";
	rename -uid "8CF37F97-426E-36AD-34F5-168B98EF9748";
createNode fosterParent -n "chrRNfosterParent1";
	rename -uid "F9F65837-448D-E108-9ACD-F79F946AEF8E";
createNode scaleConstraint -n "Root_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "906A0B2A-4C45-B987-E6EE-00B60B313CBE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "RootW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Root_orientConstraint2" -p "chrRNfosterParent1";
	rename -uid "22D42B32-43E3-42F7-95BD-619165A3FDAB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "RootW0" -dv 1 -min 0 -at "double";
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
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Root_pointConstraint2" -p "chrRNfosterParent1";
	rename -uid "2C0CACF1-471F-F49D-091A-D388A31D2EDF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "RootW0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_01_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "75AFC7FB-4E15-FD8D-DB06-0EB1CE396758";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_01W0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_01_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "94E4E25D-4EED-A8D0-78BD-25BA49D17321";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_01W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -28.351999999999997 0 0 ;
	setAttr ".rsrr" -type "double3" -28.351999999999997 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_01_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "D0556E81-4C3E-32F6-256C-D2B9DFF186AF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_01W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 1.1368683772161603e-13 0 ;
	setAttr ".rst" -type "double3" 0 -529.139 -421.351 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_02_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "5773038C-49EF-E409-11D7-00A388B6E7CA";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_02W0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_02_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "86605BE3-431F-E408-C0B3-0F901FB5942C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_02W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 3.4830000000000041 0 0 ;
	setAttr ".rsrr" -type "double3" 3.4830000000000041 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_02_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "BC3D3AC1-4B6F-3C85-9109-1C9AF2C835F0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_02W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 9.0949470177292824e-13 -2.3874235921539366e-12 ;
	setAttr ".rst" -type "double3" 0 0 -726.59 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_03_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "F3138958-400E-7B75-3E65-8A9E7516F3F9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_03W0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_03_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "470AE938-497E-86AC-BD87-22B7E6844E5E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_03W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 7.762999999999999 0 0 ;
	setAttr ".rsrr" -type "double3" 7.762999999999999 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_03_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "3E1848CF-44F8-CED6-0428-97AE63BEEF52";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_03W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 -9.0949470177292824e-13 3.637978807091713e-12 ;
	setAttr ".rst" -type "double3" 0 0 -2591.6300000000001 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_04_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "AEA27016-463E-E5D6-9C66-25BD8F6C2D09";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_04W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 1 0.99999999999999978 0.99999999999999978 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_04_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "1C5A0FAA-4C9D-C0AD-ED00-69AA95A6C3BB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_04W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 6.585 0 0 ;
	setAttr ".rsrr" -type "double3" 6.585 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_04_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "79757774-4A01-FC15-180C-8DB3A0B44323";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_04W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 2.7284841053187847e-12 2.2737367544323206e-12 ;
	setAttr ".rst" -type "double3" 0 0 -2137.4050000000002 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_05_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "40EBBA11-40EA-8052-4B8C-AA9F659F641E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_05W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 1 0.99999999999999956 0.99999999999999956 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_05_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "265C705E-42E6-0934-5E18-BA9EB5E68E8F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_05W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 8.382 0 0 ;
	setAttr ".rsrr" -type "double3" 8.382 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_05_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "0C8E9625-4612-86B6-7953-13A0CB3F3EF7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_05W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 4.5474735088646412e-13 5.4569682106375694e-12 ;
	setAttr ".rst" -type "double3" 0 0 -2781.8580000000002 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_06_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "7B84CCB7-4619-220A-BB61-85A5E9FFDE89";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_06W0" -dv 1 -min 0 -at "double";
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
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_06_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "A4D9AD6B-4950-368E-E578-079EDEA2588B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_06W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 3.6540000000000004 0 0 ;
	setAttr ".rsrr" -type "double3" 3.6540000000000004 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_06_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "BB808F7C-4916-C74D-7CEF-F68577F4A262";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_06W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 -4.5474735088646412e-13 -2.7284841053187847e-12 ;
	setAttr ".rst" -type "double3" 0 0 -3141.0320000000002 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_07_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "325DC383-4286-AA37-DE26-4991F2AF82CB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_07W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 1 0.99999999999999956 0.99999999999999956 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_07_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "B8677D49-4A6F-6921-49A0-4BA48688CEFC";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_07W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" 0.6870000000000005 0 0 ;
	setAttr ".rsrr" -type "double3" 0.6870000000000005 0 0 ;
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_07_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "1C1A69A6-4FAB-4C62-B51C-AC9602DA88C5";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_07W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 5.4569682106375694e-12 2.2737367544323206e-12 ;
	setAttr ".rst" -type "double3" 0 0 -2877.0740000000001 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Tail_08_scaleConstraint1" -p "chrRNfosterParent1";
	rename -uid "BA5A6765-4A98-1B5E-4EB2-C2BB8399044C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_08W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 1 0.99999999999999978 0.99999999999999978 ;
	setAttr -k on ".w0";
createNode orientConstraint -n "Tail_08_orientConstraint1" -p "chrRNfosterParent1";
	rename -uid "389337E3-407E-2C9D-DD78-24AC9674FC10";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_08W0" -dv 1 -min 0 -at "double";
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
	setAttr ".int" 2;
	setAttr -k on ".w0";
createNode pointConstraint -n "Tail_08_pointConstraint1" -p "chrRNfosterParent1";
	rename -uid "47FCA8C5-4FFE-E937-3F33-85A28C1794CF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "FK_Tail_08W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0 3.637978807091713e-12 -3.3196556614711881e-11 ;
	setAttr ".rst" -type "double3" 0 0 -3563.4789999999998 ;
	setAttr -k on ".w0";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "7FF5FC84-4823-E135-3FD0-F1B432911C81";
	setAttr -s 6 ".lnk";
	setAttr -s 6 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "F914D766-49FD-68C1-B159-72909610D0F7";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "4E316EA3-4C28-4033-76FB-AF9D12163751";
createNode displayLayerManager -n "layerManager";
	rename -uid "162428FD-4202-1B84-BB3D-05AEBDA44729";
createNode displayLayer -n "defaultLayer";
	rename -uid "C0783B7D-4D5A-8988-2183-F98EA97296A2";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "69B0B0EA-4A4F-DAF0-7CE0-3C8A65585F0A";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "FCA8648F-45C4-4BD4-F38B-5691996221F1";
	setAttr ".g" yes;
createNode reference -n "chrRN";
	rename -uid "338F93F1-4BD5-25C8-B7EC-9EA99BFDCE13";
	setAttr -s 161 ".phl";
	setAttr ".phl[1]" 0;
	setAttr ".phl[2]" 0;
	setAttr ".phl[3]" 0;
	setAttr ".phl[4]" 0;
	setAttr ".phl[5]" 0;
	setAttr ".phl[6]" 0;
	setAttr ".phl[7]" 0;
	setAttr ".phl[8]" 0;
	setAttr ".phl[9]" 0;
	setAttr ".phl[10]" 0;
	setAttr ".phl[11]" 0;
	setAttr ".phl[12]" 0;
	setAttr ".phl[13]" 0;
	setAttr ".phl[14]" 0;
	setAttr ".phl[15]" 0;
	setAttr ".phl[16]" 0;
	setAttr ".phl[17]" 0;
	setAttr ".phl[18]" 0;
	setAttr ".phl[19]" 0;
	setAttr ".phl[20]" 0;
	setAttr ".phl[21]" 0;
	setAttr ".phl[22]" 0;
	setAttr ".phl[23]" 0;
	setAttr ".phl[24]" 0;
	setAttr ".phl[25]" 0;
	setAttr ".phl[26]" 0;
	setAttr ".phl[27]" 0;
	setAttr ".phl[28]" 0;
	setAttr ".phl[29]" 0;
	setAttr ".phl[30]" 0;
	setAttr ".phl[31]" 0;
	setAttr ".phl[32]" 0;
	setAttr ".phl[33]" 0;
	setAttr ".phl[34]" 0;
	setAttr ".phl[35]" 0;
	setAttr ".phl[36]" 0;
	setAttr ".phl[37]" 0;
	setAttr ".phl[38]" 0;
	setAttr ".phl[39]" 0;
	setAttr ".phl[40]" 0;
	setAttr ".phl[41]" 0;
	setAttr ".phl[42]" 0;
	setAttr ".phl[43]" 0;
	setAttr ".phl[44]" 0;
	setAttr ".phl[45]" 0;
	setAttr ".phl[46]" 0;
	setAttr ".phl[47]" 0;
	setAttr ".phl[48]" 0;
	setAttr ".phl[49]" 0;
	setAttr ".phl[50]" 0;
	setAttr ".phl[51]" 0;
	setAttr ".phl[52]" 0;
	setAttr ".phl[53]" 0;
	setAttr ".phl[54]" 0;
	setAttr ".phl[55]" 0;
	setAttr ".phl[56]" 0;
	setAttr ".phl[57]" 0;
	setAttr ".phl[58]" 0;
	setAttr ".phl[59]" 0;
	setAttr ".phl[60]" 0;
	setAttr ".phl[61]" 0;
	setAttr ".phl[62]" 0;
	setAttr ".phl[63]" 0;
	setAttr ".phl[64]" 0;
	setAttr ".phl[65]" 0;
	setAttr ".phl[66]" 0;
	setAttr ".phl[67]" 0;
	setAttr ".phl[68]" 0;
	setAttr ".phl[69]" 0;
	setAttr ".phl[70]" 0;
	setAttr ".phl[71]" 0;
	setAttr ".phl[72]" 0;
	setAttr ".phl[73]" 0;
	setAttr ".phl[74]" 0;
	setAttr ".phl[75]" 0;
	setAttr ".phl[76]" 0;
	setAttr ".phl[77]" 0;
	setAttr ".phl[78]" 0;
	setAttr ".phl[79]" 0;
	setAttr ".phl[80]" 0;
	setAttr ".phl[81]" 0;
	setAttr ".phl[82]" 0;
	setAttr ".phl[83]" 0;
	setAttr ".phl[84]" 0;
	setAttr ".phl[85]" 0;
	setAttr ".phl[86]" 0;
	setAttr ".phl[87]" 0;
	setAttr ".phl[88]" 0;
	setAttr ".phl[89]" 0;
	setAttr ".phl[90]" 0;
	setAttr ".phl[91]" 0;
	setAttr ".phl[92]" 0;
	setAttr ".phl[93]" 0;
	setAttr ".phl[94]" 0;
	setAttr ".phl[95]" 0;
	setAttr ".phl[96]" 0;
	setAttr ".phl[97]" 0;
	setAttr ".phl[98]" 0;
	setAttr ".phl[99]" 0;
	setAttr ".phl[100]" 0;
	setAttr ".phl[101]" 0;
	setAttr ".phl[102]" 0;
	setAttr ".phl[103]" 0;
	setAttr ".phl[104]" 0;
	setAttr ".phl[105]" 0;
	setAttr ".phl[106]" 0;
	setAttr ".phl[107]" 0;
	setAttr ".phl[108]" 0;
	setAttr ".phl[109]" 0;
	setAttr ".phl[110]" 0;
	setAttr ".phl[111]" 0;
	setAttr ".phl[112]" 0;
	setAttr ".phl[113]" 0;
	setAttr ".phl[114]" 0;
	setAttr ".phl[115]" 0;
	setAttr ".phl[116]" 0;
	setAttr ".phl[117]" 0;
	setAttr ".phl[118]" 0;
	setAttr ".phl[119]" 0;
	setAttr ".phl[120]" 0;
	setAttr ".phl[121]" 0;
	setAttr ".phl[122]" 0;
	setAttr ".phl[123]" 0;
	setAttr ".phl[124]" 0;
	setAttr ".phl[125]" 0;
	setAttr ".phl[126]" 0;
	setAttr ".phl[127]" 0;
	setAttr ".phl[128]" 0;
	setAttr ".phl[129]" 0;
	setAttr ".phl[130]" 0;
	setAttr ".phl[131]" 0;
	setAttr ".phl[132]" 0;
	setAttr ".phl[133]" 0;
	setAttr ".phl[134]" 0;
	setAttr ".phl[135]" 0;
	setAttr ".phl[136]" 0;
	setAttr ".phl[137]" 0;
	setAttr ".phl[138]" 0;
	setAttr ".phl[139]" 0;
	setAttr ".phl[140]" 0;
	setAttr ".phl[141]" 0;
	setAttr ".phl[142]" 0;
	setAttr ".phl[143]" 0;
	setAttr ".phl[144]" 0;
	setAttr ".phl[145]" 0;
	setAttr ".phl[146]" 0;
	setAttr ".phl[147]" 0;
	setAttr ".phl[148]" 0;
	setAttr ".phl[149]" 0;
	setAttr ".phl[150]" 0;
	setAttr ".phl[151]" 0;
	setAttr ".phl[152]" 0;
	setAttr ".phl[153]" 0;
	setAttr ".phl[154]" 0;
	setAttr ".phl[155]" 0;
	setAttr ".phl[156]" 0;
	setAttr ".phl[157]" 0;
	setAttr ".phl[158]" 0;
	setAttr ".phl[159]" 0;
	setAttr ".phl[160]" 0;
	setAttr ".phl[161]" 0;
	setAttr ".ed" -type "dataReferenceEdits" 
		"chrRN"
		"chrRN" 0
		"chrRN" 189
		0 "|chr:bahamut" "|CHAR|MODEL" "-s -r "
		0 "|chrRNfosterParent1|Tail_08_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_08_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_08_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_07_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_07_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_07_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_06_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_06_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_06_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_05_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_05_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_05_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_04_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_04_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_04_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_03_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_03_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_03_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_02_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_02_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_02_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_01_pointConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_01_orientConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01" 
		"-s -r "
		0 "|chrRNfosterParent1|Tail_01_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01" 
		"-s -r "
		0 "|chrRNfosterParent1|Root_pointConstraint2" "|CHAR|MODEL|chr:bahamut|chr:Root" 
		"-s -r "
		0 "|chrRNfosterParent1|Root_orientConstraint2" "|CHAR|MODEL|chr:bahamut|chr:Root" 
		"-s -r "
		0 "|chrRNfosterParent1|Root_scaleConstraint1" "|CHAR|MODEL|chr:bahamut|chr:Root" 
		"-s -r "
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.scaleX" "chrRN.placeHolderList[1]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.scaleY" "chrRN.placeHolderList[2]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.scaleZ" "chrRN.placeHolderList[3]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.translateX" "chrRN.placeHolderList[4]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.translateY" "chrRN.placeHolderList[5]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.translateZ" "chrRN.placeHolderList[6]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.parentInverseMatrix" "chrRN.placeHolderList[7]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.parentInverseMatrix" "chrRN.placeHolderList[8]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.parentInverseMatrix" "chrRN.placeHolderList[9]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.rotatePivot" "chrRN.placeHolderList[10]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.rotatePivotTranslate" 
		"chrRN.placeHolderList[11]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.rotateX" "chrRN.placeHolderList[12]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.rotateY" "chrRN.placeHolderList[13]" 
		""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.rotateZ" "chrRN.placeHolderList[14]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.rotateOrder" "chrRN.placeHolderList[15]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.jointOrient" "chrRN.placeHolderList[16]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root.inverseScale" "chrRN.placeHolderList[17]" 
		""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.inverseScale" 
		"chrRN.placeHolderList[18]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.scaleX" 
		"chrRN.placeHolderList[19]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.scaleY" 
		"chrRN.placeHolderList[20]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.scaleZ" 
		"chrRN.placeHolderList[21]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.translateX" 
		"chrRN.placeHolderList[22]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.translateY" 
		"chrRN.placeHolderList[23]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.translateZ" 
		"chrRN.placeHolderList[24]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.parentInverseMatrix" 
		"chrRN.placeHolderList[25]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.parentInverseMatrix" 
		"chrRN.placeHolderList[26]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.parentInverseMatrix" 
		"chrRN.placeHolderList[27]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.rotatePivot" 
		"chrRN.placeHolderList[28]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.rotatePivotTranslate" 
		"chrRN.placeHolderList[29]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.rotateX" 
		"chrRN.placeHolderList[30]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.rotateY" 
		"chrRN.placeHolderList[31]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.rotateZ" 
		"chrRN.placeHolderList[32]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.rotateOrder" 
		"chrRN.placeHolderList[33]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.jointOrient" 
		"chrRN.placeHolderList[34]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01.segmentScaleCompensate" 
		"chrRN.placeHolderList[35]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.inverseScale" 
		"chrRN.placeHolderList[36]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.scaleX" 
		"chrRN.placeHolderList[37]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.scaleY" 
		"chrRN.placeHolderList[38]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.scaleZ" 
		"chrRN.placeHolderList[39]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.translateX" 
		"chrRN.placeHolderList[40]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.translateY" 
		"chrRN.placeHolderList[41]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.translateZ" 
		"chrRN.placeHolderList[42]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.parentInverseMatrix" 
		"chrRN.placeHolderList[43]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.parentInverseMatrix" 
		"chrRN.placeHolderList[44]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.parentInverseMatrix" 
		"chrRN.placeHolderList[45]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.rotatePivot" 
		"chrRN.placeHolderList[46]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.rotatePivotTranslate" 
		"chrRN.placeHolderList[47]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.rotateX" 
		"chrRN.placeHolderList[48]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.rotateY" 
		"chrRN.placeHolderList[49]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.rotateZ" 
		"chrRN.placeHolderList[50]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.rotateOrder" 
		"chrRN.placeHolderList[51]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.jointOrient" 
		"chrRN.placeHolderList[52]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02.segmentScaleCompensate" 
		"chrRN.placeHolderList[53]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.inverseScale" 
		"chrRN.placeHolderList[54]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.scaleX" 
		"chrRN.placeHolderList[55]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.scaleY" 
		"chrRN.placeHolderList[56]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.scaleZ" 
		"chrRN.placeHolderList[57]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.translateX" 
		"chrRN.placeHolderList[58]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.translateY" 
		"chrRN.placeHolderList[59]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.translateZ" 
		"chrRN.placeHolderList[60]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.parentInverseMatrix" 
		"chrRN.placeHolderList[61]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.parentInverseMatrix" 
		"chrRN.placeHolderList[62]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.parentInverseMatrix" 
		"chrRN.placeHolderList[63]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.rotatePivot" 
		"chrRN.placeHolderList[64]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.rotatePivotTranslate" 
		"chrRN.placeHolderList[65]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.rotateX" 
		"chrRN.placeHolderList[66]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.rotateY" 
		"chrRN.placeHolderList[67]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.rotateZ" 
		"chrRN.placeHolderList[68]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.rotateOrder" 
		"chrRN.placeHolderList[69]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.jointOrient" 
		"chrRN.placeHolderList[70]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03.segmentScaleCompensate" 
		"chrRN.placeHolderList[71]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.inverseScale" 
		"chrRN.placeHolderList[72]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.scaleX" 
		"chrRN.placeHolderList[73]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.scaleY" 
		"chrRN.placeHolderList[74]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.scaleZ" 
		"chrRN.placeHolderList[75]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.translateX" 
		"chrRN.placeHolderList[76]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.translateY" 
		"chrRN.placeHolderList[77]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.translateZ" 
		"chrRN.placeHolderList[78]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.parentInverseMatrix" 
		"chrRN.placeHolderList[79]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.parentInverseMatrix" 
		"chrRN.placeHolderList[80]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.parentInverseMatrix" 
		"chrRN.placeHolderList[81]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.rotatePivot" 
		"chrRN.placeHolderList[82]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.rotatePivotTranslate" 
		"chrRN.placeHolderList[83]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.rotateX" 
		"chrRN.placeHolderList[84]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.rotateY" 
		"chrRN.placeHolderList[85]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.rotateZ" 
		"chrRN.placeHolderList[86]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.rotateOrder" 
		"chrRN.placeHolderList[87]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.jointOrient" 
		"chrRN.placeHolderList[88]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04.segmentScaleCompensate" 
		"chrRN.placeHolderList[89]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.inverseScale" 
		"chrRN.placeHolderList[90]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.scaleX" 
		"chrRN.placeHolderList[91]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.scaleY" 
		"chrRN.placeHolderList[92]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.scaleZ" 
		"chrRN.placeHolderList[93]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.translateX" 
		"chrRN.placeHolderList[94]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.translateY" 
		"chrRN.placeHolderList[95]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.translateZ" 
		"chrRN.placeHolderList[96]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.parentInverseMatrix" 
		"chrRN.placeHolderList[97]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.parentInverseMatrix" 
		"chrRN.placeHolderList[98]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.parentInverseMatrix" 
		"chrRN.placeHolderList[99]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.rotatePivot" 
		"chrRN.placeHolderList[100]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.rotatePivotTranslate" 
		"chrRN.placeHolderList[101]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.rotateX" 
		"chrRN.placeHolderList[102]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.rotateY" 
		"chrRN.placeHolderList[103]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.rotateZ" 
		"chrRN.placeHolderList[104]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.rotateOrder" 
		"chrRN.placeHolderList[105]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.jointOrient" 
		"chrRN.placeHolderList[106]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05.segmentScaleCompensate" 
		"chrRN.placeHolderList[107]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.inverseScale" 
		"chrRN.placeHolderList[108]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.scaleX" 
		"chrRN.placeHolderList[109]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.scaleY" 
		"chrRN.placeHolderList[110]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.scaleZ" 
		"chrRN.placeHolderList[111]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.translateX" 
		"chrRN.placeHolderList[112]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.translateY" 
		"chrRN.placeHolderList[113]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.translateZ" 
		"chrRN.placeHolderList[114]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.parentInverseMatrix" 
		"chrRN.placeHolderList[115]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.parentInverseMatrix" 
		"chrRN.placeHolderList[116]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.parentInverseMatrix" 
		"chrRN.placeHolderList[117]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.rotatePivot" 
		"chrRN.placeHolderList[118]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.rotatePivotTranslate" 
		"chrRN.placeHolderList[119]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.rotateX" 
		"chrRN.placeHolderList[120]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.rotateY" 
		"chrRN.placeHolderList[121]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.rotateZ" 
		"chrRN.placeHolderList[122]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.rotateOrder" 
		"chrRN.placeHolderList[123]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.jointOrient" 
		"chrRN.placeHolderList[124]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06.segmentScaleCompensate" 
		"chrRN.placeHolderList[125]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.inverseScale" 
		"chrRN.placeHolderList[126]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.scaleX" 
		"chrRN.placeHolderList[127]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.scaleY" 
		"chrRN.placeHolderList[128]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.scaleZ" 
		"chrRN.placeHolderList[129]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.translateX" 
		"chrRN.placeHolderList[130]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.translateY" 
		"chrRN.placeHolderList[131]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.translateZ" 
		"chrRN.placeHolderList[132]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.parentInverseMatrix" 
		"chrRN.placeHolderList[133]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.parentInverseMatrix" 
		"chrRN.placeHolderList[134]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.parentInverseMatrix" 
		"chrRN.placeHolderList[135]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.rotatePivot" 
		"chrRN.placeHolderList[136]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.rotatePivotTranslate" 
		"chrRN.placeHolderList[137]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.rotateX" 
		"chrRN.placeHolderList[138]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.rotateY" 
		"chrRN.placeHolderList[139]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.rotateZ" 
		"chrRN.placeHolderList[140]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.rotateOrder" 
		"chrRN.placeHolderList[141]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.jointOrient" 
		"chrRN.placeHolderList[142]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07.segmentScaleCompensate" 
		"chrRN.placeHolderList[143]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.inverseScale" 
		"chrRN.placeHolderList[144]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.translateX" 
		"chrRN.placeHolderList[145]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.translateY" 
		"chrRN.placeHolderList[146]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.translateZ" 
		"chrRN.placeHolderList[147]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.parentInverseMatrix" 
		"chrRN.placeHolderList[148]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.parentInverseMatrix" 
		"chrRN.placeHolderList[149]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.parentInverseMatrix" 
		"chrRN.placeHolderList[150]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.rotatePivot" 
		"chrRN.placeHolderList[151]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.rotatePivotTranslate" 
		"chrRN.placeHolderList[152]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.rotateX" 
		"chrRN.placeHolderList[153]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.rotateY" 
		"chrRN.placeHolderList[154]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.rotateZ" 
		"chrRN.placeHolderList[155]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.rotateOrder" 
		"chrRN.placeHolderList[156]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.jointOrient" 
		"chrRN.placeHolderList[157]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.scaleX" 
		"chrRN.placeHolderList[158]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.scaleY" 
		"chrRN.placeHolderList[159]" ""
		5 4 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.scaleZ" 
		"chrRN.placeHolderList[160]" ""
		5 3 "chrRN" "|CHAR|MODEL|chr:bahamut|chr:Root|chr:Hip|chr:Tail_01|chr:Tail_02|chr:Tail_03|chr:Tail_04|chr:Tail_05|chr:Tail_06|chr:Tail_07|chr:Tail_08.segmentScaleCompensate" 
		"chrRN.placeHolderList[161]" "";
lockNode -l 1 ;
createNode pairBlend -n "FK_Tail_02_CTRL_DRV_ROT_PBN";
	rename -uid "3FF45B6E-4135-F4B1-2E86-F9BEC3275BAF";
	setAttr ".ri" 1;
createNode pairBlend -n "FK_Tail_03_CTRL_DRV_ROT_PBN";
	rename -uid "7C4597DE-4034-CF04-801F-E699309C2F05";
	setAttr ".ri" 1;
createNode pairBlend -n "FK_Tail_04_CTRL_DRV_ROT_PBN";
	rename -uid "970116F7-45B5-76AA-F181-E7BCC4447F30";
	setAttr ".ri" 1;
createNode pairBlend -n "FK_Tail_05_CTRL_DRV_ROT_PBN";
	rename -uid "A15ACD19-45F9-156C-37D4-BB9DF1F62387";
	setAttr ".ri" 1;
createNode pairBlend -n "FK_Tail_06_CTRL_DRV_ROT_PBN";
	rename -uid "CD2FD769-404F-BAA8-5FFB-86B6108F6A04";
	setAttr ".ri" 1;
createNode pairBlend -n "FK_Tail_07_CTRL_DRV_ROT_PBN";
	rename -uid "5B17424F-4F21-9A27-A1D9-7F8D5CE85BDD";
	setAttr ".ri" 1;
createNode pairBlend -n "FK_Tail_08_CTRL_DRV_ROT_PBN";
	rename -uid "7B40F51B-4935-0350-1FDA-C8936AB12AD6";
	setAttr ".ri" 1;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "2CAC8CE2-47B3-AC45-1732-D6BEADF953C7";
	setAttr ".b" -type "string" "// Maya Mel UI Configuration File.\n// No UI generated in batch mode.\n";
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "B9C242AE-4EC6-B99A-D5D2-7B8EE9755F1E";
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
	setAttr -s 6 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 9 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 4 ".u";
select -ne :defaultRenderingList1;
	setAttr -s 2 ".r";
select -ne :defaultTextureList1;
	setAttr -s 4 ".tx";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "Root_scaleConstraint1.csx" "chrRN.phl[1]";
connectAttr "Root_scaleConstraint1.csy" "chrRN.phl[2]";
connectAttr "Root_scaleConstraint1.csz" "chrRN.phl[3]";
connectAttr "Root_pointConstraint2.ctx" "chrRN.phl[4]";
connectAttr "Root_pointConstraint2.cty" "chrRN.phl[5]";
connectAttr "Root_pointConstraint2.ctz" "chrRN.phl[6]";
connectAttr "chrRN.phl[7]" "Root_orientConstraint2.cpim";
connectAttr "chrRN.phl[8]" "Root_pointConstraint2.cpim";
connectAttr "chrRN.phl[9]" "Root_scaleConstraint1.cpim";
connectAttr "chrRN.phl[10]" "Root_pointConstraint2.crp";
connectAttr "chrRN.phl[11]" "Root_pointConstraint2.crt";
connectAttr "Root_orientConstraint2.crx" "chrRN.phl[12]";
connectAttr "Root_orientConstraint2.cry" "chrRN.phl[13]";
connectAttr "Root_orientConstraint2.crz" "chrRN.phl[14]";
connectAttr "chrRN.phl[15]" "Root_orientConstraint2.cro";
connectAttr "chrRN.phl[16]" "Root_orientConstraint2.cjo";
connectAttr "chrRN.phl[17]" "Root_orientConstraint2.is";
connectAttr "chrRN.phl[18]" "Tail_01_orientConstraint1.is";
connectAttr "Tail_01_scaleConstraint1.csx" "chrRN.phl[19]";
connectAttr "Tail_01_scaleConstraint1.csy" "chrRN.phl[20]";
connectAttr "Tail_01_scaleConstraint1.csz" "chrRN.phl[21]";
connectAttr "Tail_01_pointConstraint1.ctx" "chrRN.phl[22]";
connectAttr "Tail_01_pointConstraint1.cty" "chrRN.phl[23]";
connectAttr "Tail_01_pointConstraint1.ctz" "chrRN.phl[24]";
connectAttr "chrRN.phl[25]" "Tail_01_orientConstraint1.cpim";
connectAttr "chrRN.phl[26]" "Tail_01_pointConstraint1.cpim";
connectAttr "chrRN.phl[27]" "Tail_01_scaleConstraint1.cpim";
connectAttr "chrRN.phl[28]" "Tail_01_pointConstraint1.crp";
connectAttr "chrRN.phl[29]" "Tail_01_pointConstraint1.crt";
connectAttr "Tail_01_orientConstraint1.crx" "chrRN.phl[30]";
connectAttr "Tail_01_orientConstraint1.cry" "chrRN.phl[31]";
connectAttr "Tail_01_orientConstraint1.crz" "chrRN.phl[32]";
connectAttr "chrRN.phl[33]" "Tail_01_orientConstraint1.cro";
connectAttr "chrRN.phl[34]" "Tail_01_orientConstraint1.cjo";
connectAttr "chrRN.phl[35]" "Tail_01_scaleConstraint1.tsc";
connectAttr "chrRN.phl[36]" "Tail_02_orientConstraint1.is";
connectAttr "Tail_02_scaleConstraint1.csx" "chrRN.phl[37]";
connectAttr "Tail_02_scaleConstraint1.csy" "chrRN.phl[38]";
connectAttr "Tail_02_scaleConstraint1.csz" "chrRN.phl[39]";
connectAttr "Tail_02_pointConstraint1.ctx" "chrRN.phl[40]";
connectAttr "Tail_02_pointConstraint1.cty" "chrRN.phl[41]";
connectAttr "Tail_02_pointConstraint1.ctz" "chrRN.phl[42]";
connectAttr "chrRN.phl[43]" "Tail_02_orientConstraint1.cpim";
connectAttr "chrRN.phl[44]" "Tail_02_pointConstraint1.cpim";
connectAttr "chrRN.phl[45]" "Tail_02_scaleConstraint1.cpim";
connectAttr "chrRN.phl[46]" "Tail_02_pointConstraint1.crp";
connectAttr "chrRN.phl[47]" "Tail_02_pointConstraint1.crt";
connectAttr "Tail_02_orientConstraint1.crx" "chrRN.phl[48]";
connectAttr "Tail_02_orientConstraint1.cry" "chrRN.phl[49]";
connectAttr "Tail_02_orientConstraint1.crz" "chrRN.phl[50]";
connectAttr "chrRN.phl[51]" "Tail_02_orientConstraint1.cro";
connectAttr "chrRN.phl[52]" "Tail_02_orientConstraint1.cjo";
connectAttr "chrRN.phl[53]" "Tail_02_scaleConstraint1.tsc";
connectAttr "chrRN.phl[54]" "Tail_03_orientConstraint1.is";
connectAttr "Tail_03_scaleConstraint1.csx" "chrRN.phl[55]";
connectAttr "Tail_03_scaleConstraint1.csy" "chrRN.phl[56]";
connectAttr "Tail_03_scaleConstraint1.csz" "chrRN.phl[57]";
connectAttr "Tail_03_pointConstraint1.ctx" "chrRN.phl[58]";
connectAttr "Tail_03_pointConstraint1.cty" "chrRN.phl[59]";
connectAttr "Tail_03_pointConstraint1.ctz" "chrRN.phl[60]";
connectAttr "chrRN.phl[61]" "Tail_03_orientConstraint1.cpim";
connectAttr "chrRN.phl[62]" "Tail_03_pointConstraint1.cpim";
connectAttr "chrRN.phl[63]" "Tail_03_scaleConstraint1.cpim";
connectAttr "chrRN.phl[64]" "Tail_03_pointConstraint1.crp";
connectAttr "chrRN.phl[65]" "Tail_03_pointConstraint1.crt";
connectAttr "Tail_03_orientConstraint1.crx" "chrRN.phl[66]";
connectAttr "Tail_03_orientConstraint1.cry" "chrRN.phl[67]";
connectAttr "Tail_03_orientConstraint1.crz" "chrRN.phl[68]";
connectAttr "chrRN.phl[69]" "Tail_03_orientConstraint1.cro";
connectAttr "chrRN.phl[70]" "Tail_03_orientConstraint1.cjo";
connectAttr "chrRN.phl[71]" "Tail_03_scaleConstraint1.tsc";
connectAttr "chrRN.phl[72]" "Tail_04_orientConstraint1.is";
connectAttr "Tail_04_scaleConstraint1.csx" "chrRN.phl[73]";
connectAttr "Tail_04_scaleConstraint1.csy" "chrRN.phl[74]";
connectAttr "Tail_04_scaleConstraint1.csz" "chrRN.phl[75]";
connectAttr "Tail_04_pointConstraint1.ctx" "chrRN.phl[76]";
connectAttr "Tail_04_pointConstraint1.cty" "chrRN.phl[77]";
connectAttr "Tail_04_pointConstraint1.ctz" "chrRN.phl[78]";
connectAttr "chrRN.phl[79]" "Tail_04_orientConstraint1.cpim";
connectAttr "chrRN.phl[80]" "Tail_04_pointConstraint1.cpim";
connectAttr "chrRN.phl[81]" "Tail_04_scaleConstraint1.cpim";
connectAttr "chrRN.phl[82]" "Tail_04_pointConstraint1.crp";
connectAttr "chrRN.phl[83]" "Tail_04_pointConstraint1.crt";
connectAttr "Tail_04_orientConstraint1.crx" "chrRN.phl[84]";
connectAttr "Tail_04_orientConstraint1.cry" "chrRN.phl[85]";
connectAttr "Tail_04_orientConstraint1.crz" "chrRN.phl[86]";
connectAttr "chrRN.phl[87]" "Tail_04_orientConstraint1.cro";
connectAttr "chrRN.phl[88]" "Tail_04_orientConstraint1.cjo";
connectAttr "chrRN.phl[89]" "Tail_04_scaleConstraint1.tsc";
connectAttr "chrRN.phl[90]" "Tail_05_orientConstraint1.is";
connectAttr "Tail_05_scaleConstraint1.csx" "chrRN.phl[91]";
connectAttr "Tail_05_scaleConstraint1.csy" "chrRN.phl[92]";
connectAttr "Tail_05_scaleConstraint1.csz" "chrRN.phl[93]";
connectAttr "Tail_05_pointConstraint1.ctx" "chrRN.phl[94]";
connectAttr "Tail_05_pointConstraint1.cty" "chrRN.phl[95]";
connectAttr "Tail_05_pointConstraint1.ctz" "chrRN.phl[96]";
connectAttr "chrRN.phl[97]" "Tail_05_orientConstraint1.cpim";
connectAttr "chrRN.phl[98]" "Tail_05_pointConstraint1.cpim";
connectAttr "chrRN.phl[99]" "Tail_05_scaleConstraint1.cpim";
connectAttr "chrRN.phl[100]" "Tail_05_pointConstraint1.crp";
connectAttr "chrRN.phl[101]" "Tail_05_pointConstraint1.crt";
connectAttr "Tail_05_orientConstraint1.crx" "chrRN.phl[102]";
connectAttr "Tail_05_orientConstraint1.cry" "chrRN.phl[103]";
connectAttr "Tail_05_orientConstraint1.crz" "chrRN.phl[104]";
connectAttr "chrRN.phl[105]" "Tail_05_orientConstraint1.cro";
connectAttr "chrRN.phl[106]" "Tail_05_orientConstraint1.cjo";
connectAttr "chrRN.phl[107]" "Tail_05_scaleConstraint1.tsc";
connectAttr "chrRN.phl[108]" "Tail_06_orientConstraint1.is";
connectAttr "Tail_06_scaleConstraint1.csx" "chrRN.phl[109]";
connectAttr "Tail_06_scaleConstraint1.csy" "chrRN.phl[110]";
connectAttr "Tail_06_scaleConstraint1.csz" "chrRN.phl[111]";
connectAttr "Tail_06_pointConstraint1.ctx" "chrRN.phl[112]";
connectAttr "Tail_06_pointConstraint1.cty" "chrRN.phl[113]";
connectAttr "Tail_06_pointConstraint1.ctz" "chrRN.phl[114]";
connectAttr "chrRN.phl[115]" "Tail_06_orientConstraint1.cpim";
connectAttr "chrRN.phl[116]" "Tail_06_pointConstraint1.cpim";
connectAttr "chrRN.phl[117]" "Tail_06_scaleConstraint1.cpim";
connectAttr "chrRN.phl[118]" "Tail_06_pointConstraint1.crp";
connectAttr "chrRN.phl[119]" "Tail_06_pointConstraint1.crt";
connectAttr "Tail_06_orientConstraint1.crx" "chrRN.phl[120]";
connectAttr "Tail_06_orientConstraint1.cry" "chrRN.phl[121]";
connectAttr "Tail_06_orientConstraint1.crz" "chrRN.phl[122]";
connectAttr "chrRN.phl[123]" "Tail_06_orientConstraint1.cro";
connectAttr "chrRN.phl[124]" "Tail_06_orientConstraint1.cjo";
connectAttr "chrRN.phl[125]" "Tail_06_scaleConstraint1.tsc";
connectAttr "chrRN.phl[126]" "Tail_07_orientConstraint1.is";
connectAttr "Tail_07_scaleConstraint1.csx" "chrRN.phl[127]";
connectAttr "Tail_07_scaleConstraint1.csy" "chrRN.phl[128]";
connectAttr "Tail_07_scaleConstraint1.csz" "chrRN.phl[129]";
connectAttr "Tail_07_pointConstraint1.ctx" "chrRN.phl[130]";
connectAttr "Tail_07_pointConstraint1.cty" "chrRN.phl[131]";
connectAttr "Tail_07_pointConstraint1.ctz" "chrRN.phl[132]";
connectAttr "chrRN.phl[133]" "Tail_07_orientConstraint1.cpim";
connectAttr "chrRN.phl[134]" "Tail_07_pointConstraint1.cpim";
connectAttr "chrRN.phl[135]" "Tail_07_scaleConstraint1.cpim";
connectAttr "chrRN.phl[136]" "Tail_07_pointConstraint1.crp";
connectAttr "chrRN.phl[137]" "Tail_07_pointConstraint1.crt";
connectAttr "Tail_07_orientConstraint1.crx" "chrRN.phl[138]";
connectAttr "Tail_07_orientConstraint1.cry" "chrRN.phl[139]";
connectAttr "Tail_07_orientConstraint1.crz" "chrRN.phl[140]";
connectAttr "chrRN.phl[141]" "Tail_07_orientConstraint1.cro";
connectAttr "chrRN.phl[142]" "Tail_07_orientConstraint1.cjo";
connectAttr "chrRN.phl[143]" "Tail_07_scaleConstraint1.tsc";
connectAttr "chrRN.phl[144]" "Tail_08_orientConstraint1.is";
connectAttr "Tail_08_pointConstraint1.ctx" "chrRN.phl[145]";
connectAttr "Tail_08_pointConstraint1.cty" "chrRN.phl[146]";
connectAttr "Tail_08_pointConstraint1.ctz" "chrRN.phl[147]";
connectAttr "chrRN.phl[148]" "Tail_08_orientConstraint1.cpim";
connectAttr "chrRN.phl[149]" "Tail_08_pointConstraint1.cpim";
connectAttr "chrRN.phl[150]" "Tail_08_scaleConstraint1.cpim";
connectAttr "chrRN.phl[151]" "Tail_08_pointConstraint1.crp";
connectAttr "chrRN.phl[152]" "Tail_08_pointConstraint1.crt";
connectAttr "Tail_08_orientConstraint1.crx" "chrRN.phl[153]";
connectAttr "Tail_08_orientConstraint1.cry" "chrRN.phl[154]";
connectAttr "Tail_08_orientConstraint1.crz" "chrRN.phl[155]";
connectAttr "chrRN.phl[156]" "Tail_08_orientConstraint1.cro";
connectAttr "chrRN.phl[157]" "Tail_08_orientConstraint1.cjo";
connectAttr "Tail_08_scaleConstraint1.csx" "chrRN.phl[158]";
connectAttr "Tail_08_scaleConstraint1.csy" "chrRN.phl[159]";
connectAttr "Tail_08_scaleConstraint1.csz" "chrRN.phl[160]";
connectAttr "chrRN.phl[161]" "Tail_08_scaleConstraint1.tsc";
connectAttr "Global_CTRL.s" "Global.s";
connectAttr "Global_pointConstraint1.ctx" "Global.tx";
connectAttr "Global_pointConstraint1.cty" "Global.ty";
connectAttr "Global_pointConstraint1.ctz" "Global.tz";
connectAttr "Global_orientConstraint1.crx" "Global.rx";
connectAttr "Global_orientConstraint1.cry" "Global.ry";
connectAttr "Global_orientConstraint1.crz" "Global.rz";
connectAttr "Global_CTRL.sh" "Global.sh";
connectAttr "Global.s" "Local.is";
connectAttr "Local_CTRL.s" "Local.s";
connectAttr "Local_pointConstraint1.ctx" "Local.tx";
connectAttr "Local_pointConstraint1.cty" "Local.ty";
connectAttr "Local_pointConstraint1.ctz" "Local.tz";
connectAttr "Local_orientConstraint1.crx" "Local.rx";
connectAttr "Local_orientConstraint1.cry" "Local.ry";
connectAttr "Local_orientConstraint1.crz" "Local.rz";
connectAttr "Local_CTRL.sh" "Local.sh";
connectAttr "Root_CTRL.s" "Root.s";
connectAttr "Local.s" "Root.is";
connectAttr "Root_pointConstraint1.ctx" "Root.tx";
connectAttr "Root_pointConstraint1.cty" "Root.ty";
connectAttr "Root_pointConstraint1.ctz" "Root.tz";
connectAttr "Root_orientConstraint1.crx" "Root.rx";
connectAttr "Root_orientConstraint1.cry" "Root.ry";
connectAttr "Root_orientConstraint1.crz" "Root.rz";
connectAttr "Root_CTRL.sh" "Root.sh";
connectAttr "Root.pim" "Root_pointConstraint1.cpim";
connectAttr "Root.rp" "Root_pointConstraint1.crp";
connectAttr "Root.rpt" "Root_pointConstraint1.crt";
connectAttr "Root_CTRL.t" "Root_pointConstraint1.tg[0].tt";
connectAttr "Root_CTRL.rp" "Root_pointConstraint1.tg[0].trp";
connectAttr "Root_CTRL.rpt" "Root_pointConstraint1.tg[0].trt";
connectAttr "Root_CTRL.pm" "Root_pointConstraint1.tg[0].tpm";
connectAttr "Root_pointConstraint1.w0" "Root_pointConstraint1.tg[0].tw";
connectAttr "Root.ro" "Root_orientConstraint1.cro";
connectAttr "Root.pim" "Root_orientConstraint1.cpim";
connectAttr "Root.jo" "Root_orientConstraint1.cjo";
connectAttr "Root.is" "Root_orientConstraint1.is";
connectAttr "Root_CTRL.r" "Root_orientConstraint1.tg[0].tr";
connectAttr "Root_CTRL.ro" "Root_orientConstraint1.tg[0].tro";
connectAttr "Root_CTRL.pm" "Root_orientConstraint1.tg[0].tpm";
connectAttr "Root_orientConstraint1.w0" "Root_orientConstraint1.tg[0].tw";
connectAttr "Local.pim" "Local_pointConstraint1.cpim";
connectAttr "Local.rp" "Local_pointConstraint1.crp";
connectAttr "Local.rpt" "Local_pointConstraint1.crt";
connectAttr "Local_CTRL.t" "Local_pointConstraint1.tg[0].tt";
connectAttr "Local_CTRL.rp" "Local_pointConstraint1.tg[0].trp";
connectAttr "Local_CTRL.rpt" "Local_pointConstraint1.tg[0].trt";
connectAttr "Local_CTRL.pm" "Local_pointConstraint1.tg[0].tpm";
connectAttr "Local_pointConstraint1.w0" "Local_pointConstraint1.tg[0].tw";
connectAttr "Local.ro" "Local_orientConstraint1.cro";
connectAttr "Local.pim" "Local_orientConstraint1.cpim";
connectAttr "Local.jo" "Local_orientConstraint1.cjo";
connectAttr "Local.is" "Local_orientConstraint1.is";
connectAttr "Local_CTRL.r" "Local_orientConstraint1.tg[0].tr";
connectAttr "Local_CTRL.ro" "Local_orientConstraint1.tg[0].tro";
connectAttr "Local_CTRL.pm" "Local_orientConstraint1.tg[0].tpm";
connectAttr "Local_orientConstraint1.w0" "Local_orientConstraint1.tg[0].tw";
connectAttr "Global.pim" "Global_pointConstraint1.cpim";
connectAttr "Global.rp" "Global_pointConstraint1.crp";
connectAttr "Global.rpt" "Global_pointConstraint1.crt";
connectAttr "Global_CTRL.t" "Global_pointConstraint1.tg[0].tt";
connectAttr "Global_CTRL.rp" "Global_pointConstraint1.tg[0].trp";
connectAttr "Global_CTRL.rpt" "Global_pointConstraint1.tg[0].trt";
connectAttr "Global_CTRL.pm" "Global_pointConstraint1.tg[0].tpm";
connectAttr "Global_pointConstraint1.w0" "Global_pointConstraint1.tg[0].tw";
connectAttr "Global.ro" "Global_orientConstraint1.cro";
connectAttr "Global.pim" "Global_orientConstraint1.cpim";
connectAttr "Global.jo" "Global_orientConstraint1.cjo";
connectAttr "Global.is" "Global_orientConstraint1.is";
connectAttr "Global_CTRL.r" "Global_orientConstraint1.tg[0].tr";
connectAttr "Global_CTRL.ro" "Global_orientConstraint1.tg[0].tro";
connectAttr "Global_CTRL.pm" "Global_orientConstraint1.tg[0].tpm";
connectAttr "Global_orientConstraint1.w0" "Global_orientConstraint1.tg[0].tw";
connectAttr "Global_scaleConstraint1.csx" "chr:Global.sx";
connectAttr "Global_scaleConstraint1.csy" "chr:Global.sy";
connectAttr "Global_scaleConstraint1.csz" "chr:Global.sz";
connectAttr "Global_pointConstraint2.ctx" "chr:Global.tx";
connectAttr "Global_pointConstraint2.cty" "chr:Global.ty";
connectAttr "Global_pointConstraint2.ctz" "chr:Global.tz";
connectAttr "Global_orientConstraint2.crx" "chr:Global.rx";
connectAttr "Global_orientConstraint2.cry" "chr:Global.ry";
connectAttr "Global_orientConstraint2.crz" "chr:Global.rz";
connectAttr "chr:Global.s" "chr:Local.is";
connectAttr "Local_pointConstraint2.ctx" "chr:Local.tx";
connectAttr "Local_pointConstraint2.cty" "chr:Local.ty";
connectAttr "Local_pointConstraint2.ctz" "chr:Local.tz";
connectAttr "Local_orientConstraint2.crx" "chr:Local.rx";
connectAttr "Local_orientConstraint2.cry" "chr:Local.ry";
connectAttr "Local_orientConstraint2.crz" "chr:Local.rz";
connectAttr "Local_scaleConstraint1.csx" "chr:Local.sx";
connectAttr "Local_scaleConstraint1.csy" "chr:Local.sy";
connectAttr "Local_scaleConstraint1.csz" "chr:Local.sz";
connectAttr "chr:Local.pim" "Local_pointConstraint2.cpim";
connectAttr "chr:Local.rp" "Local_pointConstraint2.crp";
connectAttr "chr:Local.rpt" "Local_pointConstraint2.crt";
connectAttr "Local.t" "Local_pointConstraint2.tg[0].tt";
connectAttr "Local.rp" "Local_pointConstraint2.tg[0].trp";
connectAttr "Local.rpt" "Local_pointConstraint2.tg[0].trt";
connectAttr "Local.pm" "Local_pointConstraint2.tg[0].tpm";
connectAttr "Local_pointConstraint2.w0" "Local_pointConstraint2.tg[0].tw";
connectAttr "chr:Local.ro" "Local_orientConstraint2.cro";
connectAttr "chr:Local.pim" "Local_orientConstraint2.cpim";
connectAttr "chr:Local.jo" "Local_orientConstraint2.cjo";
connectAttr "chr:Local.is" "Local_orientConstraint2.is";
connectAttr "Local.r" "Local_orientConstraint2.tg[0].tr";
connectAttr "Local.ro" "Local_orientConstraint2.tg[0].tro";
connectAttr "Local.pm" "Local_orientConstraint2.tg[0].tpm";
connectAttr "Local.jo" "Local_orientConstraint2.tg[0].tjo";
connectAttr "Local_orientConstraint2.w0" "Local_orientConstraint2.tg[0].tw";
connectAttr "chr:Local.ssc" "Local_scaleConstraint1.tsc";
connectAttr "chr:Local.pim" "Local_scaleConstraint1.cpim";
connectAttr "Local.s" "Local_scaleConstraint1.tg[0].ts";
connectAttr "Local.pm" "Local_scaleConstraint1.tg[0].tpm";
connectAttr "Local_scaleConstraint1.w0" "Local_scaleConstraint1.tg[0].tw";
connectAttr "chr:Global.pim" "Global_pointConstraint2.cpim";
connectAttr "chr:Global.rp" "Global_pointConstraint2.crp";
connectAttr "chr:Global.rpt" "Global_pointConstraint2.crt";
connectAttr "Global.t" "Global_pointConstraint2.tg[0].tt";
connectAttr "Global.rp" "Global_pointConstraint2.tg[0].trp";
connectAttr "Global.rpt" "Global_pointConstraint2.tg[0].trt";
connectAttr "Global.pm" "Global_pointConstraint2.tg[0].tpm";
connectAttr "Global_pointConstraint2.w0" "Global_pointConstraint2.tg[0].tw";
connectAttr "chr:Global.ro" "Global_orientConstraint2.cro";
connectAttr "chr:Global.pim" "Global_orientConstraint2.cpim";
connectAttr "chr:Global.jo" "Global_orientConstraint2.cjo";
connectAttr "chr:Global.is" "Global_orientConstraint2.is";
connectAttr "Global.r" "Global_orientConstraint2.tg[0].tr";
connectAttr "Global.ro" "Global_orientConstraint2.tg[0].tro";
connectAttr "Global.pm" "Global_orientConstraint2.tg[0].tpm";
connectAttr "Global.jo" "Global_orientConstraint2.tg[0].tjo";
connectAttr "Global_orientConstraint2.w0" "Global_orientConstraint2.tg[0].tw";
connectAttr "chr:Global.pim" "Global_scaleConstraint1.cpim";
connectAttr "Global.s" "Global_scaleConstraint1.tg[0].ts";
connectAttr "Global.pm" "Global_scaleConstraint1.tg[0].tpm";
connectAttr "Global_scaleConstraint1.w0" "Global_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_01_CTRL.s" "FK_Tail_01.s";
connectAttr "FK_Tail_01_pointConstraint1.ctx" "FK_Tail_01.tx";
connectAttr "FK_Tail_01_pointConstraint1.cty" "FK_Tail_01.ty";
connectAttr "FK_Tail_01_pointConstraint1.ctz" "FK_Tail_01.tz";
connectAttr "FK_Tail_01_orientConstraint1.crx" "FK_Tail_01.rx";
connectAttr "FK_Tail_01_orientConstraint1.cry" "FK_Tail_01.ry";
connectAttr "FK_Tail_01_orientConstraint1.crz" "FK_Tail_01.rz";
connectAttr "FK_Tail_01_CTRL.sh" "FK_Tail_01.sh";
connectAttr "FK_Tail_01.s" "FK_Tail_02.is";
connectAttr "FK_Tail_02_CTRL.s" "FK_Tail_02.s";
connectAttr "FK_Tail_02_pointConstraint1.ctx" "FK_Tail_02.tx";
connectAttr "FK_Tail_02_pointConstraint1.cty" "FK_Tail_02.ty";
connectAttr "FK_Tail_02_pointConstraint1.ctz" "FK_Tail_02.tz";
connectAttr "FK_Tail_02_orientConstraint1.crx" "FK_Tail_02.rx";
connectAttr "FK_Tail_02_orientConstraint1.cry" "FK_Tail_02.ry";
connectAttr "FK_Tail_02_orientConstraint1.crz" "FK_Tail_02.rz";
connectAttr "FK_Tail_02_CTRL.sh" "FK_Tail_02.sh";
connectAttr "FK_Tail_02.s" "FK_Tail_03.is";
connectAttr "FK_Tail_03_CTRL.s" "FK_Tail_03.s";
connectAttr "FK_Tail_03_pointConstraint1.ctx" "FK_Tail_03.tx";
connectAttr "FK_Tail_03_pointConstraint1.cty" "FK_Tail_03.ty";
connectAttr "FK_Tail_03_pointConstraint1.ctz" "FK_Tail_03.tz";
connectAttr "FK_Tail_03_orientConstraint1.crx" "FK_Tail_03.rx";
connectAttr "FK_Tail_03_orientConstraint1.cry" "FK_Tail_03.ry";
connectAttr "FK_Tail_03_orientConstraint1.crz" "FK_Tail_03.rz";
connectAttr "FK_Tail_03_CTRL.sh" "FK_Tail_03.sh";
connectAttr "FK_Tail_03.s" "FK_Tail_04.is";
connectAttr "FK_Tail_04_CTRL.s" "FK_Tail_04.s";
connectAttr "FK_Tail_04_pointConstraint1.ctx" "FK_Tail_04.tx";
connectAttr "FK_Tail_04_pointConstraint1.cty" "FK_Tail_04.ty";
connectAttr "FK_Tail_04_pointConstraint1.ctz" "FK_Tail_04.tz";
connectAttr "FK_Tail_04_orientConstraint1.crx" "FK_Tail_04.rx";
connectAttr "FK_Tail_04_orientConstraint1.cry" "FK_Tail_04.ry";
connectAttr "FK_Tail_04_orientConstraint1.crz" "FK_Tail_04.rz";
connectAttr "FK_Tail_04_CTRL.sh" "FK_Tail_04.sh";
connectAttr "FK_Tail_04.s" "FK_Tail_05.is";
connectAttr "FK_Tail_05_CTRL.s" "FK_Tail_05.s";
connectAttr "FK_Tail_05_pointConstraint1.ctx" "FK_Tail_05.tx";
connectAttr "FK_Tail_05_pointConstraint1.cty" "FK_Tail_05.ty";
connectAttr "FK_Tail_05_pointConstraint1.ctz" "FK_Tail_05.tz";
connectAttr "FK_Tail_05_orientConstraint1.crx" "FK_Tail_05.rx";
connectAttr "FK_Tail_05_orientConstraint1.cry" "FK_Tail_05.ry";
connectAttr "FK_Tail_05_orientConstraint1.crz" "FK_Tail_05.rz";
connectAttr "FK_Tail_05_CTRL.sh" "FK_Tail_05.sh";
connectAttr "FK_Tail_05.s" "FK_Tail_06.is";
connectAttr "FK_Tail_06_CTRL.s" "FK_Tail_06.s";
connectAttr "FK_Tail_06_pointConstraint1.ctx" "FK_Tail_06.tx";
connectAttr "FK_Tail_06_pointConstraint1.cty" "FK_Tail_06.ty";
connectAttr "FK_Tail_06_pointConstraint1.ctz" "FK_Tail_06.tz";
connectAttr "FK_Tail_06_orientConstraint1.crx" "FK_Tail_06.rx";
connectAttr "FK_Tail_06_orientConstraint1.cry" "FK_Tail_06.ry";
connectAttr "FK_Tail_06_orientConstraint1.crz" "FK_Tail_06.rz";
connectAttr "FK_Tail_06_CTRL.sh" "FK_Tail_06.sh";
connectAttr "FK_Tail_06.s" "FK_Tail_07.is";
connectAttr "FK_Tail_07_CTRL.s" "FK_Tail_07.s";
connectAttr "FK_Tail_07_pointConstraint1.ctx" "FK_Tail_07.tx";
connectAttr "FK_Tail_07_pointConstraint1.cty" "FK_Tail_07.ty";
connectAttr "FK_Tail_07_pointConstraint1.ctz" "FK_Tail_07.tz";
connectAttr "FK_Tail_07_orientConstraint1.crx" "FK_Tail_07.rx";
connectAttr "FK_Tail_07_orientConstraint1.cry" "FK_Tail_07.ry";
connectAttr "FK_Tail_07_orientConstraint1.crz" "FK_Tail_07.rz";
connectAttr "FK_Tail_07_CTRL.sh" "FK_Tail_07.sh";
connectAttr "FK_Tail_07.s" "FK_Tail_08.is";
connectAttr "FK_Tail_08_pointConstraint1.ctx" "FK_Tail_08.tx";
connectAttr "FK_Tail_08_pointConstraint1.cty" "FK_Tail_08.ty";
connectAttr "FK_Tail_08_pointConstraint1.ctz" "FK_Tail_08.tz";
connectAttr "FK_Tail_08_orientConstraint1.crx" "FK_Tail_08.rx";
connectAttr "FK_Tail_08_orientConstraint1.cry" "FK_Tail_08.ry";
connectAttr "FK_Tail_08_orientConstraint1.crz" "FK_Tail_08.rz";
connectAttr "FK_Tail_08_CTRL.s" "FK_Tail_08.s";
connectAttr "FK_Tail_08_CTRL.sh" "FK_Tail_08.sh";
connectAttr "FK_Tail_08.pim" "FK_Tail_08_pointConstraint1.cpim";
connectAttr "FK_Tail_08.rp" "FK_Tail_08_pointConstraint1.crp";
connectAttr "FK_Tail_08.rpt" "FK_Tail_08_pointConstraint1.crt";
connectAttr "FK_Tail_08_CTRL.t" "FK_Tail_08_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_08_CTRL.rp" "FK_Tail_08_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_08_CTRL.rpt" "FK_Tail_08_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_08_CTRL.pm" "FK_Tail_08_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_08_pointConstraint1.w0" "FK_Tail_08_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_08.ro" "FK_Tail_08_orientConstraint1.cro";
connectAttr "FK_Tail_08.pim" "FK_Tail_08_orientConstraint1.cpim";
connectAttr "FK_Tail_08.jo" "FK_Tail_08_orientConstraint1.cjo";
connectAttr "FK_Tail_08.is" "FK_Tail_08_orientConstraint1.is";
connectAttr "FK_Tail_08_CTRL.r" "FK_Tail_08_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_08_CTRL.ro" "FK_Tail_08_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_08_CTRL.pm" "FK_Tail_08_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_08_orientConstraint1.w0" "FK_Tail_08_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_07.pim" "FK_Tail_07_pointConstraint1.cpim";
connectAttr "FK_Tail_07.rp" "FK_Tail_07_pointConstraint1.crp";
connectAttr "FK_Tail_07.rpt" "FK_Tail_07_pointConstraint1.crt";
connectAttr "FK_Tail_07_CTRL.t" "FK_Tail_07_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_07_CTRL.rp" "FK_Tail_07_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_07_CTRL.rpt" "FK_Tail_07_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_07_CTRL.pm" "FK_Tail_07_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_07_pointConstraint1.w0" "FK_Tail_07_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_07.ro" "FK_Tail_07_orientConstraint1.cro";
connectAttr "FK_Tail_07.pim" "FK_Tail_07_orientConstraint1.cpim";
connectAttr "FK_Tail_07.jo" "FK_Tail_07_orientConstraint1.cjo";
connectAttr "FK_Tail_07.is" "FK_Tail_07_orientConstraint1.is";
connectAttr "FK_Tail_07_CTRL.r" "FK_Tail_07_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_07_CTRL.ro" "FK_Tail_07_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_07_CTRL.pm" "FK_Tail_07_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_07_orientConstraint1.w0" "FK_Tail_07_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_06.pim" "FK_Tail_06_pointConstraint1.cpim";
connectAttr "FK_Tail_06.rp" "FK_Tail_06_pointConstraint1.crp";
connectAttr "FK_Tail_06.rpt" "FK_Tail_06_pointConstraint1.crt";
connectAttr "FK_Tail_06_CTRL.t" "FK_Tail_06_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_06_CTRL.rp" "FK_Tail_06_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_06_CTRL.rpt" "FK_Tail_06_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_06_CTRL.pm" "FK_Tail_06_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_06_pointConstraint1.w0" "FK_Tail_06_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_06.ro" "FK_Tail_06_orientConstraint1.cro";
connectAttr "FK_Tail_06.pim" "FK_Tail_06_orientConstraint1.cpim";
connectAttr "FK_Tail_06.jo" "FK_Tail_06_orientConstraint1.cjo";
connectAttr "FK_Tail_06.is" "FK_Tail_06_orientConstraint1.is";
connectAttr "FK_Tail_06_CTRL.r" "FK_Tail_06_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_06_CTRL.ro" "FK_Tail_06_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_06_CTRL.pm" "FK_Tail_06_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_06_orientConstraint1.w0" "FK_Tail_06_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_05.pim" "FK_Tail_05_pointConstraint1.cpim";
connectAttr "FK_Tail_05.rp" "FK_Tail_05_pointConstraint1.crp";
connectAttr "FK_Tail_05.rpt" "FK_Tail_05_pointConstraint1.crt";
connectAttr "FK_Tail_05_CTRL.t" "FK_Tail_05_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_05_CTRL.rp" "FK_Tail_05_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_05_CTRL.rpt" "FK_Tail_05_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_05_CTRL.pm" "FK_Tail_05_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_05_pointConstraint1.w0" "FK_Tail_05_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_05.ro" "FK_Tail_05_orientConstraint1.cro";
connectAttr "FK_Tail_05.pim" "FK_Tail_05_orientConstraint1.cpim";
connectAttr "FK_Tail_05.jo" "FK_Tail_05_orientConstraint1.cjo";
connectAttr "FK_Tail_05.is" "FK_Tail_05_orientConstraint1.is";
connectAttr "FK_Tail_05_CTRL.r" "FK_Tail_05_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_05_CTRL.ro" "FK_Tail_05_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_05_CTRL.pm" "FK_Tail_05_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_05_orientConstraint1.w0" "FK_Tail_05_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_04.pim" "FK_Tail_04_pointConstraint1.cpim";
connectAttr "FK_Tail_04.rp" "FK_Tail_04_pointConstraint1.crp";
connectAttr "FK_Tail_04.rpt" "FK_Tail_04_pointConstraint1.crt";
connectAttr "FK_Tail_04_CTRL.t" "FK_Tail_04_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_04_CTRL.rp" "FK_Tail_04_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_04_CTRL.rpt" "FK_Tail_04_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_04_CTRL.pm" "FK_Tail_04_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_04_pointConstraint1.w0" "FK_Tail_04_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_04.ro" "FK_Tail_04_orientConstraint1.cro";
connectAttr "FK_Tail_04.pim" "FK_Tail_04_orientConstraint1.cpim";
connectAttr "FK_Tail_04.jo" "FK_Tail_04_orientConstraint1.cjo";
connectAttr "FK_Tail_04.is" "FK_Tail_04_orientConstraint1.is";
connectAttr "FK_Tail_04_CTRL.r" "FK_Tail_04_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_04_CTRL.ro" "FK_Tail_04_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_04_CTRL.pm" "FK_Tail_04_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_04_orientConstraint1.w0" "FK_Tail_04_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_03.pim" "FK_Tail_03_pointConstraint1.cpim";
connectAttr "FK_Tail_03.rp" "FK_Tail_03_pointConstraint1.crp";
connectAttr "FK_Tail_03.rpt" "FK_Tail_03_pointConstraint1.crt";
connectAttr "FK_Tail_03_CTRL.t" "FK_Tail_03_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_03_CTRL.rp" "FK_Tail_03_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_03_CTRL.rpt" "FK_Tail_03_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_03_CTRL.pm" "FK_Tail_03_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_03_pointConstraint1.w0" "FK_Tail_03_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_03.ro" "FK_Tail_03_orientConstraint1.cro";
connectAttr "FK_Tail_03.pim" "FK_Tail_03_orientConstraint1.cpim";
connectAttr "FK_Tail_03.jo" "FK_Tail_03_orientConstraint1.cjo";
connectAttr "FK_Tail_03.is" "FK_Tail_03_orientConstraint1.is";
connectAttr "FK_Tail_03_CTRL.r" "FK_Tail_03_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_03_CTRL.ro" "FK_Tail_03_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_03_CTRL.pm" "FK_Tail_03_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_03_orientConstraint1.w0" "FK_Tail_03_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_02.pim" "FK_Tail_02_pointConstraint1.cpim";
connectAttr "FK_Tail_02.rp" "FK_Tail_02_pointConstraint1.crp";
connectAttr "FK_Tail_02.rpt" "FK_Tail_02_pointConstraint1.crt";
connectAttr "FK_Tail_02_CTRL.t" "FK_Tail_02_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_02_CTRL.rp" "FK_Tail_02_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_02_CTRL.rpt" "FK_Tail_02_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_02_CTRL.pm" "FK_Tail_02_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_02_pointConstraint1.w0" "FK_Tail_02_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_02.ro" "FK_Tail_02_orientConstraint1.cro";
connectAttr "FK_Tail_02.pim" "FK_Tail_02_orientConstraint1.cpim";
connectAttr "FK_Tail_02.jo" "FK_Tail_02_orientConstraint1.cjo";
connectAttr "FK_Tail_02.is" "FK_Tail_02_orientConstraint1.is";
connectAttr "FK_Tail_02_CTRL.r" "FK_Tail_02_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_02_CTRL.ro" "FK_Tail_02_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_02_CTRL.pm" "FK_Tail_02_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_02_orientConstraint1.w0" "FK_Tail_02_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_01.pim" "FK_Tail_01_pointConstraint1.cpim";
connectAttr "FK_Tail_01.rp" "FK_Tail_01_pointConstraint1.crp";
connectAttr "FK_Tail_01.rpt" "FK_Tail_01_pointConstraint1.crt";
connectAttr "FK_Tail_01_CTRL.t" "FK_Tail_01_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_01_CTRL.rp" "FK_Tail_01_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_01_CTRL.rpt" "FK_Tail_01_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_01_CTRL.pm" "FK_Tail_01_pointConstraint1.tg[0].tpm";
connectAttr "FK_Tail_01_pointConstraint1.w0" "FK_Tail_01_pointConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_01.ro" "FK_Tail_01_orientConstraint1.cro";
connectAttr "FK_Tail_01.pim" "FK_Tail_01_orientConstraint1.cpim";
connectAttr "FK_Tail_01.jo" "FK_Tail_01_orientConstraint1.cjo";
connectAttr "FK_Tail_01.is" "FK_Tail_01_orientConstraint1.is";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_01_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_01_CTRL.ro" "FK_Tail_01_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_01_CTRL.pm" "FK_Tail_01_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_01_orientConstraint1.w0" "FK_Tail_01_orientConstraint1.tg[0].tw"
		;
connectAttr "FK_Tail_02_CTRL_DRV_ROT_PBN.or" "FK_Tail_02_CTRL_DRV.r";
connectAttr "FK_Tail_03_CTRL_DRV_ROT_PBN.or" "FK_Tail_03_CTRL_DRV.r";
connectAttr "FK_Tail_04_CTRL_DRV_ROT_PBN.or" "FK_Tail_04_CTRL_DRV.r";
connectAttr "FK_Tail_05_CTRL_DRV_ROT_PBN.or" "FK_Tail_05_CTRL_DRV.r";
connectAttr "FK_Tail_06_CTRL_DRV_ROT_PBN.or" "FK_Tail_06_CTRL_DRV.r";
connectAttr "FK_Tail_07_CTRL_DRV_ROT_PBN.or" "FK_Tail_07_CTRL_DRV.r";
connectAttr "FK_Tail_08_CTRL_DRV_ROT_PBN.or" "FK_Tail_08_CTRL_DRV.r";
connectAttr "Root.s" "Root_scaleConstraint1.tg[0].ts";
connectAttr "Root.pm" "Root_scaleConstraint1.tg[0].tpm";
connectAttr "Root_scaleConstraint1.w0" "Root_scaleConstraint1.tg[0].tw";
connectAttr "Root.r" "Root_orientConstraint2.tg[0].tr";
connectAttr "Root.ro" "Root_orientConstraint2.tg[0].tro";
connectAttr "Root.pm" "Root_orientConstraint2.tg[0].tpm";
connectAttr "Root.jo" "Root_orientConstraint2.tg[0].tjo";
connectAttr "Root_orientConstraint2.w0" "Root_orientConstraint2.tg[0].tw";
connectAttr "Root.t" "Root_pointConstraint2.tg[0].tt";
connectAttr "Root.rp" "Root_pointConstraint2.tg[0].trp";
connectAttr "Root.rpt" "Root_pointConstraint2.tg[0].trt";
connectAttr "Root.pm" "Root_pointConstraint2.tg[0].tpm";
connectAttr "Root_pointConstraint2.w0" "Root_pointConstraint2.tg[0].tw";
connectAttr "FK_Tail_01.s" "Tail_01_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_01.pm" "Tail_01_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_01_scaleConstraint1.w0" "Tail_01_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_01.r" "Tail_01_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_01.ro" "Tail_01_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_01.pm" "Tail_01_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_01.jo" "Tail_01_orientConstraint1.tg[0].tjo";
connectAttr "Tail_01_orientConstraint1.w0" "Tail_01_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_01.t" "Tail_01_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_01.rp" "Tail_01_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_01.rpt" "Tail_01_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_01.pm" "Tail_01_pointConstraint1.tg[0].tpm";
connectAttr "Tail_01_pointConstraint1.w0" "Tail_01_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_02.s" "Tail_02_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_02.pm" "Tail_02_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_02_scaleConstraint1.w0" "Tail_02_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_02.r" "Tail_02_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_02.ro" "Tail_02_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_02.pm" "Tail_02_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_02.jo" "Tail_02_orientConstraint1.tg[0].tjo";
connectAttr "Tail_02_orientConstraint1.w0" "Tail_02_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_02.t" "Tail_02_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_02.rp" "Tail_02_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_02.rpt" "Tail_02_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_02.pm" "Tail_02_pointConstraint1.tg[0].tpm";
connectAttr "Tail_02_pointConstraint1.w0" "Tail_02_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_03.s" "Tail_03_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_03.pm" "Tail_03_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_03_scaleConstraint1.w0" "Tail_03_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_03.r" "Tail_03_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_03.ro" "Tail_03_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_03.pm" "Tail_03_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_03.jo" "Tail_03_orientConstraint1.tg[0].tjo";
connectAttr "Tail_03_orientConstraint1.w0" "Tail_03_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_03.t" "Tail_03_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_03.rp" "Tail_03_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_03.rpt" "Tail_03_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_03.pm" "Tail_03_pointConstraint1.tg[0].tpm";
connectAttr "Tail_03_pointConstraint1.w0" "Tail_03_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_04.s" "Tail_04_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_04.pm" "Tail_04_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_04_scaleConstraint1.w0" "Tail_04_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_04.r" "Tail_04_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_04.ro" "Tail_04_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_04.pm" "Tail_04_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_04.jo" "Tail_04_orientConstraint1.tg[0].tjo";
connectAttr "Tail_04_orientConstraint1.w0" "Tail_04_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_04.t" "Tail_04_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_04.rp" "Tail_04_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_04.rpt" "Tail_04_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_04.pm" "Tail_04_pointConstraint1.tg[0].tpm";
connectAttr "Tail_04_pointConstraint1.w0" "Tail_04_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_05.s" "Tail_05_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_05.pm" "Tail_05_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_05_scaleConstraint1.w0" "Tail_05_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_05.r" "Tail_05_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_05.ro" "Tail_05_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_05.pm" "Tail_05_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_05.jo" "Tail_05_orientConstraint1.tg[0].tjo";
connectAttr "Tail_05_orientConstraint1.w0" "Tail_05_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_05.t" "Tail_05_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_05.rp" "Tail_05_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_05.rpt" "Tail_05_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_05.pm" "Tail_05_pointConstraint1.tg[0].tpm";
connectAttr "Tail_05_pointConstraint1.w0" "Tail_05_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_06.s" "Tail_06_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_06.pm" "Tail_06_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_06_scaleConstraint1.w0" "Tail_06_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_06.r" "Tail_06_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_06.ro" "Tail_06_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_06.pm" "Tail_06_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_06.jo" "Tail_06_orientConstraint1.tg[0].tjo";
connectAttr "Tail_06_orientConstraint1.w0" "Tail_06_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_06.t" "Tail_06_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_06.rp" "Tail_06_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_06.rpt" "Tail_06_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_06.pm" "Tail_06_pointConstraint1.tg[0].tpm";
connectAttr "Tail_06_pointConstraint1.w0" "Tail_06_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_07.s" "Tail_07_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_07.pm" "Tail_07_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_07_scaleConstraint1.w0" "Tail_07_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_07.r" "Tail_07_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_07.ro" "Tail_07_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_07.pm" "Tail_07_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_07.jo" "Tail_07_orientConstraint1.tg[0].tjo";
connectAttr "Tail_07_orientConstraint1.w0" "Tail_07_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_07.t" "Tail_07_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_07.rp" "Tail_07_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_07.rpt" "Tail_07_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_07.pm" "Tail_07_pointConstraint1.tg[0].tpm";
connectAttr "Tail_07_pointConstraint1.w0" "Tail_07_pointConstraint1.tg[0].tw";
connectAttr "FK_Tail_08.s" "Tail_08_scaleConstraint1.tg[0].ts";
connectAttr "FK_Tail_08.pm" "Tail_08_scaleConstraint1.tg[0].tpm";
connectAttr "Tail_08_scaleConstraint1.w0" "Tail_08_scaleConstraint1.tg[0].tw";
connectAttr "FK_Tail_08.r" "Tail_08_orientConstraint1.tg[0].tr";
connectAttr "FK_Tail_08.ro" "Tail_08_orientConstraint1.tg[0].tro";
connectAttr "FK_Tail_08.pm" "Tail_08_orientConstraint1.tg[0].tpm";
connectAttr "FK_Tail_08.jo" "Tail_08_orientConstraint1.tg[0].tjo";
connectAttr "Tail_08_orientConstraint1.w0" "Tail_08_orientConstraint1.tg[0].tw";
connectAttr "FK_Tail_08.t" "Tail_08_pointConstraint1.tg[0].tt";
connectAttr "FK_Tail_08.rp" "Tail_08_pointConstraint1.tg[0].trp";
connectAttr "FK_Tail_08.rpt" "Tail_08_pointConstraint1.tg[0].trt";
connectAttr "FK_Tail_08.pm" "Tail_08_pointConstraint1.tg[0].tpm";
connectAttr "Tail_08_pointConstraint1.w0" "Tail_08_pointConstraint1.tg[0].tw";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "chrRNfosterParent1.msg" "chrRN.fp";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_02_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_02_CTRL_DRV_ROT_PBN.w";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_03_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_03_CTRL_DRV_ROT_PBN.w";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_04_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_04_CTRL_DRV_ROT_PBN.w";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_05_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_05_CTRL_DRV_ROT_PBN.w";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_06_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_06_CTRL_DRV_ROT_PBN.w";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_07_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_07_CTRL_DRV_ROT_PBN.w";
connectAttr "FK_Tail_01_CTRL.r" "FK_Tail_08_CTRL_DRV_ROT_PBN.ir2";
connectAttr "FK_Tail_01_CTRL.rotChildren" "FK_Tail_08_CTRL_DRV_ROT_PBN.w";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of bahamut_rig_20231218_03074541753_2022.ma
