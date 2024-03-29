//Maya ASCII 2022 scene
//Name: enm_m_ghost01.ma
//Last modified: Wed, Mar 27, 2024 02:18:43 PM
//Codeset: 932
requires maya "2022";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.0.0.1";
requires "stereoCamera" "10.0";
requires -nodeType "quatToEuler" -nodeType "eulerToQuat" -nodeType "quatNormalize"
		 "quatNodes" "1.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "exportedFrom" "C:/cygames/wiz2/team/3dcg/chr/enm/minion/ghost01/scenes/enm_m_ghost01_C.ma";
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202110272215-ad32f8f1e6";
fileInfo "osv" "Windows 10 Pro v2009 (Build: 19045)";
fileInfo "UUID" "B920BBD0-46CD-888B-BF89-72BBE7B4F312";
createNode transform -s -n "persp";
	rename -uid "68804002-4D7F-9C1F-10CA-63AD387A98BA";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 626.23833359144533 419.88036847748782 736.63150083082417 ;
	setAttr ".r" -type "double3" 700.46164606354523 399.79999999992663 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "F878EB6E-47E0-0BF6-CB2E-65A871734078";
	setAttr -k off ".v" no;
	setAttr ".fl" 150;
	setAttr ".ncp" 10;
	setAttr ".fcp" 100000;
	setAttr ".coi" 1048.0029638830231;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -9.909 37.781499999999994 3.9074999999999993 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "1846ABA8-4C06-8EC0-DDEB-6F806FBEAE70";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "8B8B2C4B-4F4E-7031-60B5-6D88755C9AA6";
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
	rename -uid "520C9247-4230-21BF-AA73-3EAD96EC1E9D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -1.9111629905695102 75.964099932822108 1029.853920196023 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "D22A80EF-453A-43EE-4FF8-3285156667ED";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1021.0825723634495;
	setAttr ".ow" 9.2498864971783181;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".tp" -type "double3" -1.1892262967146507 84.891500767801915 8.7713478325735323 ;
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "88CB5AD5-417F-B210-682E-B08358FBF2BF";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1043.4059608378016 100.25684356689453 -5.6050877571105957 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "46B0F3E7-4C68-C766-45FF-AE87EED92FF4";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1054.7151554026209;
	setAttr ".ow" 1.0526315789473684;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".tp" -type "double3" -11.309194564819336 100.25684356689453 -5.6050877571105957 ;
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode joint -n "Root";
	rename -uid "D39E320D-42D7-C85B-AC22-C697A9BB3FCA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.41600001 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Root";
createNode joint -n "Hip" -p "Root";
	rename -uid "8DC54A88-4BD1-8AC6-DBE6-79A057E4D6F3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0 78.026643974576743 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 78.026643974576743 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Hip";
createNode joint -n "Spine1" -p "Hip";
	rename -uid "CA8EB528-455A-09D8-17DE-CE981AACA0D2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 3.173 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -5.182 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99591282253538971 -0.090319709419336397 0
		 0 0.090319709419336397 0.99591282253538971 0 0 81.199643974576745 0 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Spine1";
createNode joint -n "Spine2" -p "Spine1";
	rename -uid "0F0CD439-49E3-2994-FBFB-E5896E4E4617";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 12.618 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -9.24 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.96848759966788733 -0.24906177805824403 0
		 0 0.24906177805824403 0.96848759966788733 0 0 93.766071969328294 -1.1396540934531867 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Spine2";
createNode joint -n "Spine3" -p "Spine2";
	rename -uid "BD243FA5-4E30-3544-6339-9B88385E7916";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 11.828 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 3.0000000000000004 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.9801952073901623 -0.19803372290939886 0
		 0 0.19803372290939886 0.9801952073901623 0 0 105.22134329820007 -4.0855568043260968 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Spine3";
createNode joint -n "Neck" -p "Spine3";
	rename -uid "520B56D1-40B0-752C-CB06-BCB366E76131";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.40400001 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 12.99 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 26 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.96780588682795876 0.25169776602335642 0
		 0 -0.25169776602335642 0.96780588682795876 0 0 117.95407904219827 -6.6580148649191884 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Neck";
createNode joint -n "Head" -p "Neck";
	rename -uid "A552B81F-4320-AA08-0991-C3A3B7C11D18";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.435 0.18799999 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 7.2 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -14.579000000000002 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999999984769128 -1.7453292519065133e-05 0
		 0 1.7453292519065133e-05 0.99999999984769128 0 0 124.92228142735958 -4.8457909495510219 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Head";
createNode joint -n "Shoulder_L" -p "Spine3";
	rename -uid "5C5FF94D-4104-26AA-BED5-FA8496DD668B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.40400001 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 1.95 7.738 -0.06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 11.178 2.36 -11.769 ;
	setAttr ".bps" -type "matrix" 0.97814754033663942 -0.2079119749122498 -4.6335984732470692e-06 0
		 0.20791197483647364 0.97814754027452866 -1.3209338021930028e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 1.95 112.79421178961059 -5.6767534646424345 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Shoulder";
createNode joint -n "Arm_L" -p "Shoulder_L";
	rename -uid "CB13532F-4D32-E213-510D-779DB05C266B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.435 0.18799999 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 9.532 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 0 -33 ;
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 11.273702354488846 110.81239484474702 -5.6767976321030815 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm";
createNode joint -n "Elbow_L" -p "Arm_L";
	rename -uid "05B88670-4E53-E9FA-E819-18A47260270B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.18799999 0.41600001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 22 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 26.830047023090799 95.256041141312451 -5.6767248504171759 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Elbow";
createNode joint -n "Wrist_L" -p "Elbow_L";
	rename -uid "47618229-448C-87D8-ABC5-BBBE41E0FF34";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.41600001 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 19.399999999999991 2.8421709430404007e-14 1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 40.547914594494358 81.538165602829267 -5.6766606702032387 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Wrist";
createNode joint -n "Thumb_01_L" -p "Wrist_L";
	rename -uid "114DE4A5-4A0B-DCEE-7130-A1B6D386E224";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 2.4326999999999828 -2.3211000000000439 2.4768000000000043 ;
	setAttr ".r" -type "double3" 90 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 120.32899999999998 -27.134 -31.212 ;
	setAttr ".bps" -type "matrix" 0.21210307431026609 -0.86429254535022848 0.45608188071897421 0
		 -0.5842277563808268 0.26197260616916423 0.76814600323842119 0 -0.78338382325802358 -0.42938182270440683 -0.44937849947308589 0
		 40.626844763151659 78.176750979587084 -3.1998210510252982 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_01";
createNode joint -n "Thumb_02_L" -p "Thumb_01_L";
	rename -uid "AA9C22A6-42D2-7960-9089-299A360F9A9B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 3.2588999999999757 -4.4408920985006262e-15 -1.4210854715202004e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".pa" -type "double3" 0 0 -5.94 ;
	setAttr ".bps" -type "matrix" 0.27142419886545888 -0.88676274093157836 0.37414000797262753 0
		 -0.55914102847840164 0.17112303067254012 0.81122020354867852 0 -0.78338382325802358 -0.42938182270440683 -0.44937849947308589 0
		 41.318067472021397 75.36010800354525 -1.7134958099502411 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_02";
createNode joint -n "Thumb_03_L" -p "Thumb_02_L";
	rename -uid "39F9F669-47BB-836D-57A6-0999495CDB8E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 2.5749000000000493 1.4210854715202004e-14 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".pa" -type "double3" 6.361109362927032e-15 9.5416640443905487e-15 6.361109362927032e-15 ;
	setAttr ".bps" -type "matrix" 0.27142419886545888 -0.88676274093157836 0.37414000797262753 0
		 -0.55914102847840164 0.17112303067254012 0.81122020354867852 0 -0.78338382325802358 -0.42938182270440683 -0.44937849947308589 0
		 42.016957641680072 73.076782621920486 -0.75012270342149245 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_03";
createNode joint -n "Index_01_L" -p "Wrist_L";
	rename -uid "B793BDEE-43FD-7121-B47A-73B38A3242EC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 7.1900999999999868 -0.50130000000002894 2.5424999999999986 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 6.0000000000000009 -8 -6.475 ;
	setAttr ".bps" -type "matrix" 0.6167952503179599 -0.77472132943187089 0.13917787506827176 0
		 0.76899064488356239 0.63082607731522355 0.1034980592119977 0 -0.16797918700472353 0.043189372563187015 0.9848439829896054 0
		 45.277627359305889 76.099553534066516 -3.1341300650999582 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_01";
createNode joint -n "Index_02_L" -p "Index_01_L";
	rename -uid "D41AB323-4A49-026E-4FC4-42B6EEE5B60B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 3.8682000000000052 0 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.6167952503179599 -0.77472132943187089 0.13917787506827176 0
		 0.76899064488356239 0.63082607731522355 0.1034980592119977 0 -0.16797918700472353 0.043189372563187015 0.9848439829896054 0
		 47.663514746585825 73.102776487558145 -2.5957622087608705 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_02";
createNode joint -n "Index_03_L" -p "Index_02_L";
	rename -uid "0FEDE966-4300-2915-685D-82B0CCFC20CE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 2.2770000000000117 0 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.6167952503179599 -0.77472132943187089 0.13917787506827176 0
		 0.76899064488356239 0.63082607731522355 0.1034980592119977 0 -0.16797918700472353 0.043189372563187015 0.9848439829896054 0
		 49.067957531559827 71.338736020441772 -2.2788541872304133 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_03";
createNode joint -n "Middle_01_L" -p "Wrist_L";
	rename -uid "93DE0C2B-44B6-1560-E2F1-58A6F477D8EE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 7.3385999999999925 0.10619999999997276 -0.00090000000000234337 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -1 0 -12.475 ;
	setAttr ".bps" -type "matrix" 0.53766731128701029 -0.84315708046327176 6.1683517475687645e-06 0
		 0.8430285365159178 0.53758521317001351 -0.017464970677921486 0 0.014722397672483798 0.0093955439226509653 0.99984747574876165 0
		 45.812181667408829 76.424084979138712 -5.6775378367417657 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_01";
createNode joint -n "Middle_02_L" -p "Middle_01_L";
	rename -uid "0A74DB6B-46CF-6DE6-0BBA-0F9766B6A786";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 4.2291000000000167 0 -8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.53766731128701029 -0.84315708046327176 6.1683517475687645e-06 0
		 0.8430285365159178 0.53758521317001351 -0.017464970677921486 0 0.014722397672483798 0.0093955439226509653 0.99984747574876165 0
		 48.086030493572736 72.858289370151482 -5.6775117501653911 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_02";
createNode joint -n "Middle_03_L" -p "Middle_02_L";
	rename -uid "B08473B3-41C2-38AC-B159-7097F542B61C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 2.6388000000000105 0 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.53766731128701029 -0.84315708046327176 6.1683517475687645e-06 0
		 0.8430285365159178 0.53758521317001351 -0.017464970677921486 0 0.014722397672483798 0.0093955439226509653 0.99984747574876165 0
		 49.504826994596904 70.633366466224999 -5.6774954731187988 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_03";
createNode joint -n "Ring_01_L" -p "Wrist_L";
	rename -uid "F814D8A6-401C-548C-DE36-1B8E56283731";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 6.8237999999999914 -0.46980000000003486 -2.2302000000000026 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -10 10 -20.475 ;
	setAttr ".bps" -type "matrix" 0.40878257098694837 -0.89596082911836239 -0.17364043982562608 0
		 0.88344101347341897 0.43621502461570294 -0.17102171795587762 0 0.22897332894981187 -0.08349038857891293 0.9698456421743531 0
		 45.040853351489204 76.38078361175495 -7.9068317049079386 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_01";
createNode joint -n "Ring_02_L" -p "Ring_01_L";
	rename -uid "9126A779-4530-F796-E043-AB94CB289017";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 4.0679999999999978 -1.4210854715202004e-14 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.40878257098694837 -0.89596082911836239 -0.17364043982562608 0
		 0.88344101347341897 0.43621502461570294 -0.17102171795587762 0 0.22897332894981187 -0.08349038857891293 0.9698456421743531 0
		 46.703780850264096 72.73601495890145 -8.613201014118582 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_02";
createNode joint -n "Ring_03_L" -p "Ring_02_L";
	rename -uid "45822CDD-4C87-FD15-C7A9-A082C19F2D7B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 2.4444000000000017 2.8421709430404007e-14 -8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.40878257098694837 -0.89596082911836239 -0.17364043982562608 0
		 0.88344101347341897 0.43621502461570294 -0.17102171795587762 0 0.22897332894981187 -0.08349038857891293 0.9698456421743531 0
		 47.703008966784616 70.545928308204537 -9.0376477052283484 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_03";
createNode joint -n "Pinky_01_L" -p "Wrist_L";
	rename -uid "A1B3A679-4394-BE78-FF27-1CA207BD61E7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 5.8895999999999873 -1.2150000000000318 -4.1805000000000021 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -20 19 -24.475 ;
	setAttr ".bps" -type "matrix" 0.33151135967537926 -0.88550037735814824 -0.32555997927380154 0
		 0.84099664031243893 0.43374943726802223 -0.3233977066289494 0 0.42758024906369485 -0.16658483534899199 0.8884957080607524 0
		 43.853324066309419 76.514403817987258 -9.8571246591399024 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_01";
createNode joint -n "Pinky_02_L" -p "Pinky_01_L";
	rename -uid "85EA02CF-41BD-AF27-AAC8-83B94DE1972D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 3.3318000000000225 1.4210854715202004e-14 8.4376949871511897e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.33151135967537926 -0.88550037735814824 -0.32555997927380154 0
		 0.84099664031243893 0.43374943726802223 -0.3233977066289494 0 0.42758024906369485 -0.16658483534899199 0.8884957080607524 0
		 44.957853614475873 73.564093660705367 -10.941825398084358 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_02";
createNode joint -n "Pinky_03_L" -p "Pinky_02_L";
	rename -uid "F57463B0-4B32-DC61-4113-6D9C27A7D786";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 1.9988999999999777 1.4210854715202004e-14 -2.2204460492503131e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.33151135967537926 -0.88550037735814824 -0.32555997927380154 0
		 0.84099664031243893 0.43374943726802223 -0.3233977066289494 0 0.42758024906369485 -0.16658483534899199 0.8884957080607524 0
		 45.620511671330995 71.794066956404194 -11.592587240654758 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_03";
createNode joint -n "HandattachOffset_L" -p "Wrist_L";
	rename -uid "E6768217-407A-10C4-BBBD-798B4E25349F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 6.8948999999999856 -2.6379000000000303 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 43.558066204629711 74.797457205297533 -5.6766019795830047 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "HandattachOffset";
createNode joint -n "Handattach_L" -p "HandattachOffset_L";
	rename -uid "A400F4D4-460F-2947-7D54-71A8D3CC3EDB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 1.7763568394002505e-14 0 1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 9.7062825972397362e-20 4.8531412986198681e-20 0 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 43.558066204629725 74.797457205297519 -5.6766019795830029 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Handattach";
createNode joint -n "WristRoll_L" -p "Elbow_L";
	rename -uid "DE385F8A-44AB-6A6B-58A8-1385C2ADE109";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.41600001 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 15.5 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 37.79019894869672 84.295882850256277 -5.6766735724111967 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "WristRoll";
	setAttr ".radi" 2;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 1 0 ;
createNode joint -n "ArmRoll_L" -p "Arm_L";
	rename -uid "93BC951F-4111-75D1-3034-78B6FFC070E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.18799999 0.41600001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0.001 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 -0.7071069865197529 3.3082584502621084e-06 0
		 0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 11.274409461064691 110.81168773776049 -5.676797628794823 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ArmRoll";
	setAttr ".radi" 2;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 1 0 ;
createNode joint -n "Shoulder_R" -p "Spine3";
	rename -uid "9420A516-40C5-A92E-9971-468DA61A0F80";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.40400001 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -1.95 7.738 -0.06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 11.178 -2.36 11.769 ;
	setAttr ".bps" -type "matrix" 0.97814754033663942 0.2079119749122498 4.6335984732470692e-06 0
		 -0.20791197483647364 0.97814754027452866 -1.3209338021930028e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -1.95 112.79421178961059 -5.6767534646424345 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Shoulder";
createNode joint -n "Arm_R" -p "Shoulder_R";
	rename -uid "CB62C474-4BF5-EF7C-24BE-0F8C1532B296";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.435 0.18799999 0.63099998 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -9.532 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 0 33 ;
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -11.273702354488846 110.81239484474702 -5.6767976321030815 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm";
createNode joint -n "Elbow_R" -p "Arm_R";
	rename -uid "4B8D8949-4784-ECF1-30ED-2491CD39FA42";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.18799999 0.41600001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -22 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -26.830047023090799 95.256041141312451 -5.6767248504171759 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Elbow";
createNode joint -n "Wrist_R" -p "Elbow_R";
	rename -uid "3854CDE5-48E3-479E-8A1D-E792A681A923";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.41600001 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -19.399999999999991 2.8421709430404007e-14 1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -40.547914594494358 81.538165602829267 -5.6766606702032387 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Wrist";
createNode joint -n "Thumb_01_R" -p "Wrist_R";
	rename -uid "51BEAC53-4C51-15DE-7656-AAAC054AC5A8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -2.4326999999999863 -2.3211000000000297 2.4767999999999986 ;
	setAttr ".r" -type "double3" 90 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 120.32899999999998 27.134 31.212 ;
	setAttr ".bps" -type "matrix" 0.21210307431026609 0.86429254535022848 -0.45608188071897421 0
		 0.5842277563808268 0.26197260616916423 0.76814600323842119 0 0.78338382325802358 -0.42938182270440683 -0.44937849947308589 0
		 -40.626844763151674 78.176750979587098 -3.199821051025304 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_01";
createNode joint -n "Thumb_02_R" -p "Thumb_01_R";
	rename -uid "F19CC1BB-4625-330F-349C-4A88354E3568";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -3.2588999999999899 -5.3290705182007514e-15 1.4210854715202004e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".pa" -type "double3" 0 0 5.94 ;
	setAttr ".bps" -type "matrix" 0.27142419886545888 0.88676274093157836 -0.37414000797262753 0
		 0.55914102847840164 0.17112303067254012 0.81122020354867852 0 0.78338382325802358 -0.42938182270440683 -0.44937849947308589 0
		 -41.31806747202139 75.360108003545236 -1.713495809950254 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_02";
createNode joint -n "Thumb_03_R" -p "Thumb_02_R";
	rename -uid "AFF6A9E1-4948-4A84-0CE8-3AA62FA47235";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -2.5748999999999995 0 -1.4210854715202004e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.27142419886545888 0.88676274093157836 -0.37414000797262753 0
		 0.55914102847840164 0.17112303067254012 0.81122020354867852 0 0.78338382325802358 -0.42938182270440683 -0.44937849947308589 0
		 -42.016957641680072 73.076782621920515 -0.75012270342152909 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_03";
createNode joint -n "Index_01_R" -p "Wrist_R";
	rename -uid "4ADD5B45-48F3-8B83-80E1-25923B778FDD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -7.1900999999999868 -0.50130000000002894 2.5424999999999986 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 6.0000000000000009 8 6.475 ;
	setAttr ".bps" -type "matrix" 0.6167952503179599 0.77472132943187089 -0.13917787506827176 0
		 -0.76899064488356239 0.63082607731522355 0.1034980592119977 0 0.16797918700472353 0.043189372563187015 0.9848439829896054 0
		 -45.277627359305889 76.099553534066516 -3.1341300650999582 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_01";
createNode joint -n "Index_02_R" -p "Index_01_R";
	rename -uid "7580F485-4119-666A-3CE1-1CB19A9DBE96";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -3.8682000000000052 0 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.6167952503179599 0.77472132943187089 -0.13917787506827176 0
		 -0.76899064488356239 0.63082607731522355 0.1034980592119977 0 0.16797918700472353 0.043189372563187015 0.9848439829896054 0
		 -47.663514746585825 73.102776487558145 -2.5957622087608705 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_02";
createNode joint -n "Index_03_R" -p "Index_02_R";
	rename -uid "FC865F72-456A-AEA0-EFED-8CA1272B4124";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -2.2770000000000117 0 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.6167952503179599 0.77472132943187089 -0.13917787506827176 0
		 -0.76899064488356239 0.63082607731522355 0.1034980592119977 0 0.16797918700472353 0.043189372563187015 0.9848439829896054 0
		 -49.067957531559827 71.338736020441772 -2.2788541872304133 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_03";
createNode joint -n "Middle_01_R" -p "Wrist_R";
	rename -uid "C5AC7B18-4AA0-2DA5-6B86-BCA52A28C008";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -7.3385999999999925 0.10619999999997276 -0.00090000000000234337 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -1 0 12.475 ;
	setAttr ".bps" -type "matrix" 0.53766731128701029 0.84315708046327176 -6.1683517475687645e-06 0
		 -0.8430285365159178 0.53758521317001351 -0.017464970677921486 0 -0.014722397672483798 0.0093955439226509653 0.99984747574876165 0
		 -45.812181667408829 76.424084979138712 -5.6775378367417657 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_01";
createNode joint -n "Middle_02_R" -p "Middle_01_R";
	rename -uid "323BCAC4-4752-B84A-6F2B-BBBCC86296B8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -4.2291000000000167 0 -8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.53766731128701029 0.84315708046327176 -6.1683517475687645e-06 0
		 -0.8430285365159178 0.53758521317001351 -0.017464970677921486 0 -0.014722397672483798 0.0093955439226509653 0.99984747574876165 0
		 -48.086030493572736 72.858289370151482 -5.6775117501653911 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_02";
createNode joint -n "Middle_03_R" -p "Middle_02_R";
	rename -uid "605432BB-47E1-990D-0FCB-04B1E78C0CA9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -2.6388000000000105 0 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.53766731128701029 0.84315708046327176 -6.1683517475687645e-06 0
		 -0.8430285365159178 0.53758521317001351 -0.017464970677921486 0 -0.014722397672483798 0.0093955439226509653 0.99984747574876165 0
		 -49.504826994596904 70.633366466224999 -5.6774954731187988 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_03";
createNode joint -n "Ring_01_R" -p "Wrist_R";
	rename -uid "C516ABB6-4F46-9DE1-813E-5EABFA087144";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -6.8237999999999914 -0.46980000000003486 -2.2302000000000026 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -10 -10 20.475 ;
	setAttr ".bps" -type "matrix" 0.40878257098694837 0.89596082911836239 0.17364043982562608 0
		 -0.88344101347341897 0.43621502461570294 -0.17102171795587762 0 -0.22897332894981187 -0.08349038857891293 0.9698456421743531 0
		 -45.040853351489204 76.38078361175495 -7.9068317049079386 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_01";
createNode joint -n "Ring_02_R" -p "Ring_01_R";
	rename -uid "1E49550E-484F-7C32-4109-AD960CF91CC2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -4.0679999999999978 -1.4210854715202004e-14 8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.40878257098694837 0.89596082911836239 0.17364043982562608 0
		 -0.88344101347341897 0.43621502461570294 -0.17102171795587762 0 -0.22897332894981187 -0.08349038857891293 0.9698456421743531 0
		 -46.703780850264096 72.73601495890145 -8.613201014118582 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_02";
createNode joint -n "Ring_03_R" -p "Ring_02_R";
	rename -uid "49A977EA-4258-9D26-7117-CF932923DA1C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -2.4444000000000017 2.8421709430404007e-14 -8.8817841970012523e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.40878257098694837 0.89596082911836239 0.17364043982562608 0
		 -0.88344101347341897 0.43621502461570294 -0.17102171795587762 0 -0.22897332894981187 -0.08349038857891293 0.9698456421743531 0
		 -47.703008966784616 70.545928308204537 -9.0376477052283484 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_03";
createNode joint -n "Pinky_01_R" -p "Wrist_R";
	rename -uid "B2A8BDBF-4798-085A-EF27-918A02963D94";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -5.8895999999999873 -1.2150000000000318 -4.1805000000000021 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -20 -19 24.475 ;
	setAttr ".bps" -type "matrix" 0.33151135967537926 0.88550037735814824 0.32555997927380154 0
		 -0.84099664031243893 0.43374943726802223 -0.3233977066289494 0 -0.42758024906369485 -0.16658483534899199 0.8884957080607524 0
		 -43.853324066309419 76.514403817987258 -9.8571246591399024 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_01";
createNode joint -n "Pinky_02_R" -p "Pinky_01_R";
	rename -uid "827B1F4E-4C22-4718-DB04-C7A788C7CB95";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -3.3318000000000225 1.4210854715202004e-14 8.4376949871511897e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.33151135967537926 0.88550037735814824 0.32555997927380154 0
		 -0.84099664031243893 0.43374943726802223 -0.3233977066289494 0 -0.42758024906369485 -0.16658483534899199 0.8884957080607524 0
		 -44.957853614475873 73.564093660705367 -10.941825398084358 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_02";
createNode joint -n "Pinky_03_R" -p "Pinky_02_R";
	rename -uid "D5C075A0-4721-FE84-C536-D393124AF3BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.18799999 0.63099998 0.36500001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -1.9988999999999777 1.4210854715202004e-14 -2.2204460492503131e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.33151135967537926 0.88550037735814824 0.32555997927380154 0
		 -0.84099664031243893 0.43374943726802223 -0.3233977066289494 0 -0.42758024906369485 -0.16658483534899199 0.8884957080607524 0
		 -45.620511671330995 71.794066956404194 -11.592587240654758 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_03";
createNode joint -n "HandattachOffset_R" -p "Wrist_R";
	rename -uid "533C837D-4B08-4D3D-B002-86B171C24C84";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.62 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -6.8948999999999856 -2.6379000000000303 -1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -43.558066204629711 74.797457205297533 -5.6766019795830047 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "HandattachOffset";
createNode joint -n "Handattach_R" -p "HandattachOffset_R";
	rename -uid "E8921B77-4E10-8BE2-6634-10A6EDA08140";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.40799999 0.63099998 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -1.7763568394002505e-14 0 1.7763568394002505e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 9.7062825972397362e-20 0 3.9564259898737216e-17 ;
	setAttr ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -43.558066204629725 74.797457205297519 -5.6766019795830029 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Handattach";
createNode joint -n "WristRoll_R" -p "Elbow_R";
	rename -uid "AFBE8C92-45E7-B9A8-AB3F-9E8EAFD3C8E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.41600001 0.18799999 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -15.5 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -37.79019894869672 84.295882850256277 -5.6766735724111967 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "WristRoll";
	setAttr ".radi" 2;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 1 0 ;
createNode joint -n "ArmRoll_R" -p "Arm_R";
	rename -uid "DF70685C-4764-63DD-946F-6CAE0541211F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 0.63099998 0.18799999 0.41600001 ;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -0.001 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70710657584554337 0.7071069865197529 -3.3082584502621084e-06 0
		 -0.70710698649002957 0.70710657575218216 -1.3601921622151527e-05 0 -7.2787225046388998e-06 1.1957300886433764e-05 0.99999999990202149 0
		 -11.274409461064691 110.81168773776049 -5.676797628794823 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ArmRoll";
	setAttr ".radi" 2;
	setAttr ".uocol" yes;
	setAttr ".oclr" -type "float3" 1 1 0 ;
createNode joint -n "Thigh_L" -p "Hip";
	rename -uid "A5A84196-49F9-B62C-CA7E-6E8CBD24E381";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 9.909 -4.8556439745767506 -0.8 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 1.4999999999343618 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99965732497558724 0.026176948306727944 0
		 0 -0.026176948306727944 0.99965732497558724 0 9.9090000000000007 73.170999999999992 -0.80000000000000004 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thigh";
createNode joint -n "Knee_L" -p "Thigh_L";
	rename -uid "3584999D-47DF-8148-C138-788B91147810";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 -32.39 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 3.999 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99539787103963651 0.095828379563463073 0
		 0 -0.095828379563463073 0.99539787103963651 0 9.9090000000000007 40.79209924404072 -1.6478713556549183 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Knee";
createNode joint -n "Ankle_L" -p "Knee_L";
	rename -uid "531F94C6-4D6C-4675-09AA-0584F764F420";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 -30.6 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -5.4989999999343633 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -1.3877787807814457e-17 0 0 1.3877787807814457e-17 1 0
		 9.9090000000000007 10.332924390227841 -4.580219770296889 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ankle";
createNode joint -n "Toe_L" -p "Ankle_L";
	rename -uid "65B036A4-4E21-6410-DDE3-8D8AF397F9EE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 -6.923 8.549 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 -1.3877787807814457e-17 0 0 1.3877787807814457e-17 1 0
		 9.9090000000000007 3.4099243902278413 3.9687802297031105 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toe";
createNode joint -n "Thigh_R" -p "Hip";
	rename -uid "01FE0A18-43DF-2AF1-AE8B-8BBC500939BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" -9.909 -4.8556439745767506 -0.8 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 1.5000000000000002 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99965732497555726 0.026176948307873163 0
		 0 -0.026176948307873163 0.99965732497555726 0 -9.9090000000000007 73.170999999999992 -0.80000000000000004 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thigh";
createNode joint -n "Knee_R" -p "Thigh_R";
	rename -uid "CDC74462-4BA8-B538-B780-84B261970DE6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 -32.39 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 3.999 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.9953978710395267 0.095828379564603411 0
		 0 -0.095828379564603411 0.9953978710395267 0 -9.9090000000000007 40.792099244041694 -1.6478713556920117 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Knee";
createNode joint -n "Ankle_R" -p "Knee_R";
	rename -uid "3F4ABC49-4F82-B172-BDEC-859E7C687363";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 -30.6 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -5.499 0 0 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999999999999989 0 0 0 0 0.99999999999999989 0
		 -9.9090000000000007 10.332924390232176 -4.5802197703688758 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ankle";
createNode joint -n "Toe_R" -p "Ankle_R";
	rename -uid "74E983A1-45D1-1676-967D-EE92529F4C19";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 2;
	setAttr ".t" -type "double3" 0 -6.923 8.549 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.99999999999999989 0 0 0 0 0.99999999999999989 0
		 -9.9090000000000007 3.4099243902321765 3.9687802296311219 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toe";
createNode displayLayerManager -n "layerManager";
	rename -uid "4BA994B8-4693-1AC9-218E-D9960F58C238";
	setAttr ".cdl" 1;
	setAttr -s 7 ".dli[1:6]"  2 1 3 4 5 6;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "7164B04A-440E-D0A6-B4BE-E78DB59D7FF4";
	setAttr -s 7 ".lnk";
	setAttr -s 7 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "4A9358F5-4B2F-10E9-BFD5-76BEEFBA8570";
	setAttr ".bsdt[0].bscd" -type "Int32Array" 0 ;
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "9405A899-4227-3B5A-14EB-9A916965A224";
	setAttr ".tpdt[0].tpcd" -type "Int32Array" 0 ;
createNode displayLayer -n "defaultLayer";
	rename -uid "249BE50F-4257-B974-8C2F-379EA05AD7F4";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "0D7F73C3-4245-017F-1044-7AB4752649E4";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "6EBB58A2-4D5B-5E16-9061-2D8E7431D9C3";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "C2F806C4-4AA9-3068-6EF5-299D4A3417CD";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"updateModelPanelBar\" \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n"
		+ "            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n"
		+ "            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            -activeShadingGraph \"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\" \n"
		+ "            -activeCustomGeometry \"meshShaderball\" \n            -activeCustomLighSet \"defaultAreaLightSet\" \n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"updateModelPanelBar\" \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"flat\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n"
		+ "            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 1\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n"
		+ "            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n"
		+ "            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            -activeShadingGraph \"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\" \n            -activeCustomGeometry \"meshShaderball\" \n            -activeCustomLighSet \"defaultAreaLightSet\" \n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n"
		+ "        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"updateModelPanelBar\" \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n"
		+ "            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n"
		+ "            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            -activeShadingGraph \"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\" \n            -activeCustomGeometry \"meshShaderball\" \n"
		+ "            -activeCustomLighSet \"defaultAreaLightSet\" \n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"updateModelPanelBar\" \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"flat\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 1\n"
		+ "            -xray 0\n            -jointXray 1\n            -activeComponentsXray 1\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n"
		+ "            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n"
		+ "            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1079\n            -height 1061\n            -sceneRenderFilter 0\n            -activeShadingGraph \"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\" \n            -activeCustomGeometry \"meshShaderball\" \n            -activeCustomLighSet \"defaultAreaLightSet\" \n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n"
		+ "            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n"
		+ "            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"look\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n"
		+ "            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n"
		+ "            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n"
		+ "                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n"
		+ "                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n"
		+ "                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n"
		+ "                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n"
		+ "                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n"
		+ "                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n"
		+ "            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -image \"D:/users/araki/projects/TK6_CSED/Jack6/maya_projects/data/Cut/c06/Jack6_C06_v01_070925.mb_Jane1_pony_hairSystemShape2.mchp\" \n"
		+ "                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n"
		+ "                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n"
		+ "                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n"
		+ "                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n"
		+ "                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n"
		+ "            stereoCameraView -e -viewSelected 0 $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -docTag \"RADRENDER\" \n            -editorChanged \"updateModelPanelBar\" \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 1\n            -xray 1\n            -jointXray 1\n            -activeComponentsXray 1\n"
		+ "            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 0\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 0\n            -imagePlane 0\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n"
		+ "            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 898\n            -height 1061\n            -sceneRenderFilter 0\n            -activeShadingGraph \"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\" \n            -activeCustomGeometry \"meshShaderball\" \n            -activeCustomLighSet \"defaultAreaLightSet\" \n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n"
		+ "            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n"
		+ "            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n"
		+ "        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -editorChanged \\\"updateModelPanelBar\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"flat\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 1\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 1\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1079\\n    -height 1061\\n    -sceneRenderFilter 0\\n    -activeShadingGraph \\\"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\\\" \\n    -activeCustomGeometry \\\"meshShaderball\\\" \\n    -activeCustomLighSet \\\"defaultAreaLightSet\\\" \\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -docTag \\\"RADRENDER\\\" \\n    -editorChanged \\\"updateModelPanelBar\\\" \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"flat\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 1\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 1\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1079\\n    -height 1061\\n    -sceneRenderFilter 0\\n    -activeShadingGraph \\\"ballora_animatronic_shadow_rig:rsMaterial1SG,ballora_animatronic_shadow_rig:MAT_ballora,ballora_animatronic_shadow_rig:MAT_ballora\\\" \\n    -activeCustomGeometry \\\"meshShaderball\\\" \\n    -activeCustomLighSet \\\"defaultAreaLightSet\\\" \\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"1 0.000000 -1.000000 -0.000000 0.000000 0.000000 -1.000000\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "23DDBC2E-416C-A276-DA99-B29DA4B7A56B";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 60 -ast 0 -aet 60 ";
	setAttr ".st" 6;
createNode eulerToQuat -n "ArmRoll_L_twist_etq";
	rename -uid "507F78DF-47FD-D5BE-9210-3B818765333A";
createNode quatNormalize -n "ArmRoll_L_twist_qnz";
	rename -uid "90402492-4BFA-61F0-FD73-DAAB6D4015B9";
createNode quatToEuler -n "ArmRoll_L_twist_qte";
	rename -uid "53E2BFEB-40D7-C156-7977-F098E38D1C36";
createNode pairBlend -n "ArmRoll_L_twist_pb";
	rename -uid "2E4FED68-4F11-A0AF-4635-75BD48B9CA58";
	setAttr ".w" -0.5;
createNode eulerToQuat -n "ArmRoll_R_twist_etq";
	rename -uid "A506FABF-405A-DE48-AA3C-D2A3BED57606";
createNode quatNormalize -n "ArmRoll_R_twist_qnz";
	rename -uid "2F6A44DA-4931-46F9-AE99-03B5C8EEB8D0";
createNode quatToEuler -n "ArmRoll_R_twist_qte";
	rename -uid "EE0D83BD-47F2-194E-F2CB-B5AC5C63ADE3";
createNode pairBlend -n "ArmRoll_R_twist_pb";
	rename -uid "0B454295-4AF0-C86D-D29A-6C86F706C725";
	setAttr ".w" -0.5;
createNode eulerToQuat -n "WristRoll_L_twist_etq";
	rename -uid "9298BF50-4126-F4A6-0552-DDB3DEC3910E";
createNode quatNormalize -n "WristRoll_L_twist_qnz";
	rename -uid "3489B145-4A03-345D-6C62-5BB5D63EAC17";
createNode quatToEuler -n "WristRoll_L_twist_qte";
	rename -uid "3A6A635C-43AD-1E1E-3FDB-E793EBC5B39C";
createNode pairBlend -n "WristRoll_L_twist_pb";
	rename -uid "F9B6D1FC-460F-D010-F4C7-60A4E6358D4D";
	setAttr ".w" 0.5;
createNode eulerToQuat -n "WristRoll_R_twist_etq";
	rename -uid "303CFC2C-468F-81D8-1195-AC84292D8607";
createNode quatNormalize -n "WristRoll_R_twist_qnz";
	rename -uid "DE7C550E-4A61-538C-BB93-30AFB91B7CA8";
createNode quatToEuler -n "WristRoll_R_twist_qte";
	rename -uid "BC54F877-4D6A-1A90-B06F-4F8B395BF87C";
createNode pairBlend -n "WristRoll_R_twist_pb";
	rename -uid "F0F9D2A2-4A1E-A408-7884-28BBADDD679D";
	setAttr ".w" 0.5;
createNode materialInfo -n "p2_t_tshirt01_kurosaka_materialInfo18";
	rename -uid "DAC944AE-471E-55D9-9265-9AA5C46A216B";
createNode lambert -n "mt_enm_m_ghost01";
	rename -uid "239F8366-4340-89C1-49C4-388B85863EEB";
createNode shadingEngine -n "lambert19SG";
	rename -uid "D4F6A93F-4B07-918B-175B-CAB0EF40B61C";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo29";
	rename -uid "21CFF836-4495-82BA-266D-7C83F29B2E66";
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "2645E929-409C-41CD-A15F-42B6B4D07B3A";
	setAttr ".version" -type "string" "5.0.0.1";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "B7F62B11-48A3-FAE1-EF3D-09B918EAA248";
	setAttr ".ai_translator" -type "string" "gaussian";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "F6968200-46CC-675E-21D9-EF901F720BA8";
	setAttr ".ai_translator" -type "string" "exr";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "84A662D8-4617-7EBF-440D-3AA2E1F8721C";
	setAttr ".output_mode" 0;
	setAttr ".ai_translator" -type "string" "maya";
createNode lambert -n "mt_enm_m_ghost01_hair";
	rename -uid "A2F9A08E-439A-A6AC-91E1-EF9B293B5A6A";
createNode shadingEngine -n "lambert20SG";
	rename -uid "CD01EF25-4624-2CC3-3E4A-28894971D4CD";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo30";
	rename -uid "066EAC30-4B76-19C0-8852-E4ADE5A45AAC";
createNode file -n "tx_enm_m_ghost01";
	rename -uid "9CCA7DD6-4615-5967-19E0-69BC01B434DE";
	setAttr ".ftn" -type "string" "C:/cygames/wiz2/team/3dcg/chr/enm/minion/ghost01/sourceimages/001/enm_m_ghost01_001_decal.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode place2dTexture -n "place2dTexture15";
	rename -uid "9167354B-4FCF-9200-F162-3F98A7A11669";
createNode shadingEngine -n "lambert10SG1";
	rename -uid "728526C4-4550-54F7-05AB-72B596D5801A";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo31";
	rename -uid "23FEBAD6-468F-722E-0D02-5AAF760C0F7F";
createNode lambert -n "mt_enm_m_ghost01_face";
	rename -uid "491CB5B9-432D-3760-A34A-A48537D46583";
createNode file -n "tx_enm_m_ghost01_face";
	rename -uid "E4FA6A67-46B5-7DAF-A813-36B76429BA11";
	setAttr ".ftn" -type "string" "C:/cygames/wiz2/team/3dcg/chr/enm/minion/ghost01/sourceimages/001/enm_m_ghost01_001_face_decal.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode place2dTexture -n "place2dTexture16";
	rename -uid "71D89AF7-4DB6-50BD-1CD7-02B6A1970C2F";
createNode shadingEngine -n "lambert12SG1";
	rename -uid "734E9EEA-42F4-3A99-6D88-BAAB1DFE79B0";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo33";
	rename -uid "DF073D53-41DB-6242-FA21-5C888D9DD605";
createNode lambert -n "mt_enm_m_ghost01_eye";
	rename -uid "FF3DFBAB-40E9-ABFD-5A0A-6D81CFA0384F";
createNode file -n "tx_enm_m_ghost01_eye";
	rename -uid "1C62F763-4A94-3A6D-DEFC-3AA4136EB381";
	setAttr ".ftn" -type "string" "C:/cygames/wiz2/team/3dcg/chr/enm/minion/ghost01/sourceimages/001/enm_m_ghost01_001_eye_decal.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode place2dTexture -n "place2dTexture17";
	rename -uid "F9DA62E0-4B2C-7006-6288-AFB6BC34D260";
createNode shadingEngine -n "mt_mouth0001_00SG1";
	rename -uid "93558414-4188-0D04-9E7F-67BB5304D957";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo32";
	rename -uid "BA9F56B6-4B40-D4B7-0494-0384074FF424";
createNode lambert -n "mt_enm_m_ghost01_mouth";
	rename -uid "E0CDCFE8-4443-D4F1-BD03-9BA675102E55";
createNode file -n "tx_enm_m_ghost01_mouth";
	rename -uid "DD27C6F7-4B72-B310-57FC-ED81A8DE2EF9";
	setAttr ".ftn" -type "string" "C:/cygames/wiz2/team/3dcg/chr/enm/minion/ghost01/sourceimages/001/enm_m_ghost01_001_mouth_decal.tga";
	setAttr ".cs" -type "string" "sRGB";
createNode place2dTexture -n "pasted__place2dTexture3";
	rename -uid "2AA30C6E-4189-76E9-27B3-928BA90E67A5";
createNode renderLayerManager -n "renderLayerManager1";
	rename -uid "03067230-4D99-42F7-EF7A-5498EA32F806";
createNode renderLayer -n "defaultRenderLayer1";
	rename -uid "EA40DFC6-42C6-D214-86FD-60BB99D97072";
	setAttr ".g" yes;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo1";
	rename -uid "FDDE762B-4109-AEEB-7224-589D8989C8B9";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -526.19045528154618 -322.0237967277335 ;
	setAttr ".tgi[0].vh" -type "double2" -269.04760835662768 335.11903430261367 ;
createNode materialInfo -n "p2_t_tshirt01_kurosaka_materialInfo19";
	rename -uid "777F12CF-4E8B-151F-80D7-58B00DEDE3A1";
createNode reference -n "_UNKNOWN_REF_NODE_";
	rename -uid "7C734ADB-4196-2386-9BB0-0EAC5ABE6FED";
	setAttr ".ed" -type "dataReferenceEdits" 
		"_UNKNOWN_REF_NODE_"
		"_UNKNOWN_REF_NODE_" 1
		2 ":modelPanel2ViewSelectedSet" "ihi" " 0";
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "A65EFBE8-4810-A549-56A8-6B96409CB55A";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -34527.378593574715 -802.27081865736807 ;
	setAttr ".tgi[0].vh" -type "double2" -33104.245473734103 912.70296400769735 ;
	setAttr -s 18 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -34080;
	setAttr ".tgi[0].ni[0].y" 514.28570556640625;
	setAttr ".tgi[0].ni[0].nvs" 1923;
	setAttr ".tgi[0].ni[1].x" -34044.28515625;
	setAttr ".tgi[0].ni[1].y" -321.42855834960938;
	setAttr ".tgi[0].ni[1].nvs" 1923;
	setAttr ".tgi[0].ni[2].x" -33427.14453125;
	setAttr ".tgi[0].ni[2].y" -165.71427917480469;
	setAttr ".tgi[0].ni[2].nvs" 1923;
	setAttr ".tgi[0].ni[3].x" -33734.28515625;
	setAttr ".tgi[0].ni[3].y" -165.71427917480469;
	setAttr ".tgi[0].ni[3].nvs" 1923;
	setAttr ".tgi[0].ni[4].x" -33427.14453125;
	setAttr ".tgi[0].ni[4].y" -477.14285278320312;
	setAttr ".tgi[0].ni[4].nvs" 1923;
	setAttr ".tgi[0].ni[5].x" -34387.14453125;
	setAttr ".tgi[0].ni[5].y" 491.42855834960938;
	setAttr ".tgi[0].ni[5].nvs" 1923;
	setAttr ".tgi[0].ni[6].x" -33427.14453125;
	setAttr ".tgi[0].ni[6].y" 151.42857360839844;
	setAttr ".tgi[0].ni[6].nvs" 1923;
	setAttr ".tgi[0].ni[7].x" -33427.14453125;
	setAttr ".tgi[0].ni[7].y" 831.4285888671875;
	setAttr ".tgi[0].ni[7].nvs" 1923;
	setAttr ".tgi[0].ni[8].x" -34382.85546875;
	setAttr ".tgi[0].ni[8].y" 151.42857360839844;
	setAttr ".tgi[0].ni[8].nvs" 1923;
	setAttr ".tgi[0].ni[9].x" -34351.4296875;
	setAttr ".tgi[0].ni[9].y" -344.28570556640625;
	setAttr ".tgi[0].ni[9].nvs" 1923;
	setAttr ".tgi[0].ni[10].x" -34097.14453125;
	setAttr ".tgi[0].ni[10].y" 854.28570556640625;
	setAttr ".tgi[0].ni[10].nvs" 1923;
	setAttr ".tgi[0].ni[11].x" -33734.28515625;
	setAttr ".tgi[0].ni[11].y" 174.28572082519531;
	setAttr ".tgi[0].ni[11].nvs" 1923;
	setAttr ".tgi[0].ni[12].x" -33427.14453125;
	setAttr ".tgi[0].ni[12].y" 491.42855834960938;
	setAttr ".tgi[0].ni[12].nvs" 1923;
	setAttr ".tgi[0].ni[13].x" -34404.28515625;
	setAttr ".tgi[0].ni[13].y" 831.4285888671875;
	setAttr ".tgi[0].ni[13].nvs" 1923;
	setAttr ".tgi[0].ni[14].x" -33734.28515625;
	setAttr ".tgi[0].ni[14].y" -477.14285278320312;
	setAttr ".tgi[0].ni[14].nvs" 1923;
	setAttr ".tgi[0].ni[15].x" -34075.71484375;
	setAttr ".tgi[0].ni[15].y" 174.28572082519531;
	setAttr ".tgi[0].ni[15].nvs" 1923;
	setAttr ".tgi[0].ni[16].x" -33734.28515625;
	setAttr ".tgi[0].ni[16].y" 514.28570556640625;
	setAttr ".tgi[0].ni[16].nvs" 1923;
	setAttr ".tgi[0].ni[17].x" -33734.28515625;
	setAttr ".tgi[0].ni[17].y" 854.28570556640625;
	setAttr ".tgi[0].ni[17].nvs" 1923;
createNode dagPose -n "bindPose1";
	rename -uid "F98025C1-4809-4704-36F7-8B8947888F93";
	setAttr -s 54 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 54 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 78.026643974576743 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 -0.090442961838346159 0 0 0 0
		 3.1729999999999876 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 -0.16126842288427606 0 0 0 0 12.617999999999995
		 -8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0.052359877559829897 0 0 0 0 11.828000000000003
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0.4537856055185257 0 0 0 0 12.989999999999981
		 -3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 -0.25445155164825334 0 0 0 0 7.2000000000000028
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0.19509290378792618 0.041189770347066175
		 -0.20540779966721265 0 1.95 7.7380000000000004 -0.059999999999999998 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 -0.57595865315812877 0 9.5320000000000089
		 -5.6843418860808015e-14 3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 no;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 22.000000000000021 -2.8421709430404007e-14
		 8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 0 0 0 0 19.400000000000013 2.8421709430404007e-14
		 3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 2.1001372356322565 -0.47357763923614138
		 -0.54475216613247013 0 2.4326999999999757 -2.3211000000000439 2.4768000000000052 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 0 0 -0.10367255756846318 0 3.2588999999999757
		 -4.4408920985006262e-15 -1.4210854715202004e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 no;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 1.1102230246251563e-16 1.6653345369377346e-16
		 1.1102230246251563e-16 0 2.5749000000000635 1.5987211554602254e-14 7.1054273576010019e-15 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 0.10471975511965979 -0.13962634015954636
		 -0.11301006906663283 0 7.1900999999999868 -0.50130000000002894 2.5424999999999986 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.8682000000000052 0
		 -2.6645352591003757e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[17]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.2770000000000152 1.4210854715202004e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 -0.017453292519943295 0 -0.21772982418629261 0 7.3385999999999925
		 0.10619999999997276 -0.00090000000000234337 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 no;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.2291000000000096 0
		 -8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.6388000000000176 1.4210854715202004e-14
		 8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 -0.17453292519943295 0.17453292519943295
		 -0.357356164345839 0 6.8237999999999914 -0.46980000000003486 -2.2302000000000026 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.0679999999999907 -2.8421709430404007e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.4443999999999875 2.8421709430404007e-14
		 -8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[24]" -type "matrix" "xform" 1 1 1 -0.3490658503988659 0.33161255787892263
		 -0.42716933442561217 0 5.8895999999999873 -1.2150000000000318 -4.1805000000000021 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.3318000000000225 1.4210854715202004e-14
		 1.021405182655144e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.9988999999999777 1.4210854715202004e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[27]" -type "matrix" "xform" 1 1 1 0 0 0 0 6.8948999999999856 -2.6379000000000303
		 -1.7763568394002505e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[28]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.0658141036401503e-14
		 0 8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[29]" -type "matrix" "xform" 1 1 1 0 0 0 0 15.5 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[30]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.001 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[31]" -type "matrix" "xform" 1 1 1 0.19509290378792618 -0.041189770347066175
		 0.20540779966721265 0 -1.95 7.7380000000000004 -0.059999999999999998 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[32]" -type "matrix" "xform" 1 1 1 0 0 0.57595865315812877 0 -9.5320000000000089
		 -5.6843418860808015e-14 3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 no;
	setAttr ".xm[33]" -type "matrix" "xform" 1 1 1 0 0 0 0 -22.000000000000021 -2.8421709430404007e-14
		 8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[34]" -type "matrix" "xform" 1 1 1 0 0 0 0 -19.400000000000013 2.8421709430404007e-14
		 3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[35]" -type "matrix" "xform" 1 1 1 2.1001372356322565 0.47357763923614138
		 0.54475216613247013 0 -2.4326999999999792 -2.3211000000000297 2.4767999999999994 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[36]" -type "matrix" "xform" 1 1 1 0 0 0.10367255756846318 0 -3.2588999999999899
		 -6.2172489379008766e-15 2.1316282072803006e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 no;
	setAttr ".xm[37]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.5748999999999995 0
		 -1.4210854715202004e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[38]" -type "matrix" "xform" 1 1 1 0.10471975511965979 0.13962634015954636
		 0.11301006906663283 0 -7.1900999999999868 -0.50130000000002894 2.5424999999999986 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[39]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.8682000000000052 0
		 -2.6645352591003757e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[40]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.2770000000000152 1.4210854715202004e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[41]" -type "matrix" "xform" 1 1 1 -0.017453292519943295 0 0.21772982418629261 0 -7.3385999999999925
		 0.10619999999997276 -0.00090000000000234337 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 no;
	setAttr ".xm[42]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.2291000000000096 0
		 -8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[43]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.6388000000000176 1.4210854715202004e-14
		 8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[44]" -type "matrix" "xform" 1 1 1 -0.17453292519943295 -0.17453292519943295
		 0.357356164345839 0 -6.8237999999999914 -0.46980000000003486 -2.2302000000000026 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[45]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.0679999999999907 -2.8421709430404007e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[46]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.4443999999999875 2.8421709430404007e-14
		 -8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[47]" -type "matrix" "xform" 1 1 1 -0.3490658503988659 -0.33161255787892263
		 0.42716933442561217 0 -5.8895999999999873 -1.2150000000000318 -4.1805000000000021 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[48]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.3318000000000225 1.4210854715202004e-14
		 1.021405182655144e-14 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[49]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.9988999999999777 1.4210854715202004e-14
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[50]" -type "matrix" "xform" 1 1 1 0 0 0 0 -6.8948999999999856 -2.6379000000000303
		 -1.7763568394002505e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[51]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.0658141036401503e-14
		 0 8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[52]" -type "matrix" "xform" 1 1 1 0 0 0 0 -15.5 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr ".xm[53]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.001 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 no;
	setAttr -s 54 ".m";
	setAttr -s 54 ".p";
	setAttr -s 54 ".g[0:53]" yes no no no no no no no no no no no no no 
		no no no no no no no no no no no no no no no no no no no no no no no no no no no 
		no no no no no no no no no no no no no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".fzn";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av -k on ".unw";
	setAttr -av -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rm";
	setAttr -k on ".lm";
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr -k on ".hom";
	setAttr -k on ".hodm";
	setAttr -k on ".xry";
	setAttr -k on ".jxr";
	setAttr -k on ".sslt";
	setAttr -k on ".cbr";
	setAttr -k on ".bbr";
	setAttr -av -k on ".mhl";
	setAttr -k on ".cons";
	setAttr -k on ".vac";
	setAttr -av -k on ".hwi";
	setAttr -k on ".csvd";
	setAttr -av -k on ".ta";
	setAttr -av -k on ".tq";
	setAttr -k on ".ts";
	setAttr -av -k on ".etmr";
	setAttr ".tmrm" 1;
	setAttr -av -k on ".tmr";
	setAttr -av -k on ".aoon";
	setAttr -av -k on ".aoam";
	setAttr -av -k on ".aora";
	setAttr -k on ".aofr";
	setAttr -av -k on ".aosm";
	setAttr -av -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av -k on ".mbe";
	setAttr -k on ".mbt";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".mbsc";
	setAttr -k on ".mbc";
	setAttr -k on ".mbfa";
	setAttr -k on ".mbftb";
	setAttr -k on ".mbftg";
	setAttr -k on ".mbftr";
	setAttr -k on ".mbfta";
	setAttr -k on ".mbfe";
	setAttr -k on ".mbme";
	setAttr -k on ".mbcsx";
	setAttr -k on ".mbcsy";
	setAttr -k on ".mbasx";
	setAttr -k on ".mbasy";
	setAttr -av -k on ".blen";
	setAttr -k on ".blth";
	setAttr -k on ".blfr";
	setAttr -k on ".blfa";
	setAttr -av -k on ".blat";
	setAttr -av -k on ".msaa";
	setAttr -av -k on ".aasc";
	setAttr -k on ".aasq";
	setAttr -k on ".laa";
	setAttr -k on ".fprt" yes;
	setAttr -k on ".rtfm";
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 7 ".st";
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
	setAttr -s 10 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".u";
select -ne :defaultRenderingList1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".r";
select -ne :defaultTextureList1;
	setAttr -av -cb on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".tx";
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
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
	setAttr -cb on ".ai_override";
	setAttr -cb on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -cb on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".fzn";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -cb on ".mwc";
	setAttr -av -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -k on ".hio";
	setAttr -cb on ".ai_override";
	setAttr -cb on ".ai_surface_shader";
	setAttr -cb on ".ai_surface_shaderr";
	setAttr -cb on ".ai_surface_shaderg";
	setAttr -cb on ".ai_surface_shaderb";
	setAttr -cb on ".ai_volume_shader";
	setAttr -cb on ".ai_volume_shaderr";
	setAttr -cb on ".ai_volume_shaderg";
	setAttr -cb on ".ai_volume_shaderb";
lockNode -l 0 -lu 1;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -cb on ".ren" -type "string" "arnold";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -cb on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".exrc";
	setAttr -av -k on ".expt";
	setAttr -av -k on ".an";
	setAttr -cb on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -av -cb on ".me";
	setAttr -cb on ".se";
	setAttr -av -k on ".be";
	setAttr -av -cb on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -cb on ".ofe";
	setAttr -cb on ".efe";
	setAttr -cb on ".oft";
	setAttr -cb on ".umfn";
	setAttr -cb on ".ufe";
	setAttr -av -cb on ".pff";
	setAttr -av -cb on ".peie";
	setAttr -av -cb on ".ifp";
	setAttr -k on ".rv";
	setAttr -av -k on ".comp";
	setAttr -av -k on ".cth";
	setAttr -av -k on ".soll";
	setAttr -av -cb on ".sosl";
	setAttr -av -k on ".rd";
	setAttr -av -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -av -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -av -k on ".uf";
	setAttr -av -k on ".oi";
	setAttr -av -k on ".rut";
	setAttr -av -k on ".mot";
	setAttr -av -k on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -av -k on ".pram";
	setAttr -av -k on ".poam";
	setAttr -av -k on ".prlm";
	setAttr -av -k on ".polm";
	setAttr -av -cb on ".prm";
	setAttr -av -cb on ".pom";
	setAttr -cb on ".pfrm";
	setAttr -cb on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -av -k on ".ope";
	setAttr -av -k on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -cb on ".hbl";
	setAttr ".dss" -type "string" "lambert1";
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
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya-legacy/config.ocio";
	setAttr ".vtn" -type "string" "sRGB gamma (legacy)";
	setAttr ".vn" -type "string" "sRGB gamma";
	setAttr ".dn" -type "string" "legacy";
	setAttr ".wsn" -type "string" "scene-linear Rec 709/sRGB";
	setAttr ".ovt" no;
	setAttr ".povt" no;
	setAttr ".otn" -type "string" "sRGB gamma (legacy)";
	setAttr ".potn" -type "string" "sRGB gamma (legacy)";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
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
	setAttr -av -k on ".hwcc";
	setAttr -av -k on ".hwdp";
	setAttr -av -k on ".hwql";
	setAttr -av -k on ".hwfr";
	setAttr -av -k on ".soll";
	setAttr -av -k on ".sosl";
	setAttr -av -k on ".bswa";
	setAttr -av -k on ".shml";
	setAttr -av -k on ".hwel";
connectAttr "Root.s" "Hip.is";
connectAttr "Hip.s" "Spine1.is";
connectAttr "Spine1.s" "Spine2.is";
connectAttr "Spine2.s" "Spine3.is";
connectAttr "Spine3.s" "Neck.is";
connectAttr "Neck.s" "Head.is";
connectAttr "Spine3.s" "Shoulder_L.is";
connectAttr "Shoulder_L.s" "Arm_L.is";
connectAttr "Arm_L.s" "Elbow_L.is";
connectAttr "Elbow_L.s" "Wrist_L.is";
connectAttr "Wrist_L.s" "Thumb_01_L.is";
connectAttr "Thumb_01_L.s" "Thumb_02_L.is";
connectAttr "Thumb_02_L.s" "Thumb_03_L.is";
connectAttr "Wrist_L.s" "Index_01_L.is";
connectAttr "Index_01_L.s" "Index_02_L.is";
connectAttr "Index_02_L.s" "Index_03_L.is";
connectAttr "Wrist_L.s" "Middle_01_L.is";
connectAttr "Middle_01_L.s" "Middle_02_L.is";
connectAttr "Middle_02_L.s" "Middle_03_L.is";
connectAttr "Wrist_L.s" "Ring_01_L.is";
connectAttr "Ring_01_L.s" "Ring_02_L.is";
connectAttr "Ring_02_L.s" "Ring_03_L.is";
connectAttr "Wrist_L.s" "Pinky_01_L.is";
connectAttr "Pinky_01_L.s" "Pinky_02_L.is";
connectAttr "Pinky_02_L.s" "Pinky_03_L.is";
connectAttr "Wrist_L.s" "HandattachOffset_L.is";
connectAttr "HandattachOffset_L.s" "Handattach_L.is";
connectAttr "Elbow_L.s" "WristRoll_L.is";
connectAttr "WristRoll_L_twist_pb.or" "WristRoll_L.r";
connectAttr "ArmRoll_L_twist_pb.or" "ArmRoll_L.r";
connectAttr "Arm_L.s" "ArmRoll_L.is";
connectAttr "Spine3.s" "Shoulder_R.is";
connectAttr "Shoulder_R.s" "Arm_R.is";
connectAttr "Arm_R.s" "Elbow_R.is";
connectAttr "Elbow_R.s" "Wrist_R.is";
connectAttr "Wrist_R.s" "Thumb_01_R.is";
connectAttr "Thumb_01_R.s" "Thumb_02_R.is";
connectAttr "Thumb_02_R.s" "Thumb_03_R.is";
connectAttr "Wrist_R.s" "Index_01_R.is";
connectAttr "Index_01_R.s" "Index_02_R.is";
connectAttr "Index_02_R.s" "Index_03_R.is";
connectAttr "Wrist_R.s" "Middle_01_R.is";
connectAttr "Middle_01_R.s" "Middle_02_R.is";
connectAttr "Middle_02_R.s" "Middle_03_R.is";
connectAttr "Wrist_R.s" "Ring_01_R.is";
connectAttr "Ring_01_R.s" "Ring_02_R.is";
connectAttr "Ring_02_R.s" "Ring_03_R.is";
connectAttr "Wrist_R.s" "Pinky_01_R.is";
connectAttr "Pinky_01_R.s" "Pinky_02_R.is";
connectAttr "Pinky_02_R.s" "Pinky_03_R.is";
connectAttr "Wrist_R.s" "HandattachOffset_R.is";
connectAttr "HandattachOffset_R.s" "Handattach_R.is";
connectAttr "Elbow_R.s" "WristRoll_R.is";
connectAttr "WristRoll_R_twist_pb.or" "WristRoll_R.r";
connectAttr "ArmRoll_R_twist_pb.or" "ArmRoll_R.r";
connectAttr "Arm_R.s" "ArmRoll_R.is";
connectAttr "Hip.s" "Thigh_L.is";
connectAttr "Thigh_L.s" "Knee_L.is";
connectAttr "Knee_L.s" "Ankle_L.is";
connectAttr "Ankle_L.s" "Toe_L.is";
connectAttr "Hip.s" "Thigh_R.is";
connectAttr "Thigh_R.s" "Knee_R.is";
connectAttr "Knee_R.s" "Ankle_R.is";
connectAttr "Ankle_R.s" "Toe_R.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert19SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert20SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert10SG1.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert12SG1.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "mt_mouth0001_00SG1.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert19SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert20SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert10SG1.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert12SG1.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "mt_mouth0001_00SG1.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "Arm_L.r" "ArmRoll_L_twist_etq.irt";
connectAttr "ArmRoll_L_twist_etq.oqx" "ArmRoll_L_twist_qnz.iqx";
connectAttr "ArmRoll_L_twist_etq.oqw" "ArmRoll_L_twist_qnz.iqw";
connectAttr "ArmRoll_L_twist_qnz.oq" "ArmRoll_L_twist_qte.iq";
connectAttr "ArmRoll_L_twist_qte.ort" "ArmRoll_L_twist_pb.ir2";
connectAttr "Arm_R.r" "ArmRoll_R_twist_etq.irt";
connectAttr "ArmRoll_R_twist_etq.oqx" "ArmRoll_R_twist_qnz.iqx";
connectAttr "ArmRoll_R_twist_etq.oqw" "ArmRoll_R_twist_qnz.iqw";
connectAttr "ArmRoll_R_twist_qnz.oq" "ArmRoll_R_twist_qte.iq";
connectAttr "ArmRoll_R_twist_qte.ort" "ArmRoll_R_twist_pb.ir2";
connectAttr "Wrist_L.r" "WristRoll_L_twist_etq.irt";
connectAttr "WristRoll_L_twist_etq.oqx" "WristRoll_L_twist_qnz.iqx";
connectAttr "WristRoll_L_twist_etq.oqw" "WristRoll_L_twist_qnz.iqw";
connectAttr "WristRoll_L_twist_qnz.oq" "WristRoll_L_twist_qte.iq";
connectAttr "WristRoll_L_twist_qte.ort" "WristRoll_L_twist_pb.ir2";
connectAttr "Wrist_R.r" "WristRoll_R_twist_etq.irt";
connectAttr "WristRoll_R_twist_etq.oqx" "WristRoll_R_twist_qnz.iqx";
connectAttr "WristRoll_R_twist_etq.oqw" "WristRoll_R_twist_qnz.iqw";
connectAttr "WristRoll_R_twist_qnz.oq" "WristRoll_R_twist_qte.iq";
connectAttr "WristRoll_R_twist_qte.ort" "WristRoll_R_twist_pb.ir2";
connectAttr "tx_enm_m_ghost01.oc" "mt_enm_m_ghost01.c";
connectAttr "mt_enm_m_ghost01.oc" "lambert19SG.ss";
connectAttr "lambert19SG.msg" "materialInfo29.sg";
connectAttr "mt_enm_m_ghost01.msg" "materialInfo29.m";
connectAttr "tx_enm_m_ghost01.msg" "materialInfo29.t" -na;
connectAttr "tx_enm_m_ghost01.oc" "mt_enm_m_ghost01_hair.c";
connectAttr "mt_enm_m_ghost01_hair.oc" "lambert20SG.ss";
connectAttr "lambert20SG.msg" "materialInfo30.sg";
connectAttr "mt_enm_m_ghost01_hair.msg" "materialInfo30.m";
connectAttr "tx_enm_m_ghost01.msg" "materialInfo30.t" -na;
connectAttr ":defaultColorMgtGlobals.cme" "tx_enm_m_ghost01.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "tx_enm_m_ghost01.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "tx_enm_m_ghost01.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "tx_enm_m_ghost01.ws";
connectAttr "place2dTexture15.c" "tx_enm_m_ghost01.c";
connectAttr "place2dTexture15.tf" "tx_enm_m_ghost01.tf";
connectAttr "place2dTexture15.rf" "tx_enm_m_ghost01.rf";
connectAttr "place2dTexture15.mu" "tx_enm_m_ghost01.mu";
connectAttr "place2dTexture15.mv" "tx_enm_m_ghost01.mv";
connectAttr "place2dTexture15.s" "tx_enm_m_ghost01.s";
connectAttr "place2dTexture15.wu" "tx_enm_m_ghost01.wu";
connectAttr "place2dTexture15.wv" "tx_enm_m_ghost01.wv";
connectAttr "place2dTexture15.re" "tx_enm_m_ghost01.re";
connectAttr "place2dTexture15.of" "tx_enm_m_ghost01.of";
connectAttr "place2dTexture15.r" "tx_enm_m_ghost01.ro";
connectAttr "place2dTexture15.n" "tx_enm_m_ghost01.n";
connectAttr "place2dTexture15.vt1" "tx_enm_m_ghost01.vt1";
connectAttr "place2dTexture15.vt2" "tx_enm_m_ghost01.vt2";
connectAttr "place2dTexture15.vt3" "tx_enm_m_ghost01.vt3";
connectAttr "place2dTexture15.vc1" "tx_enm_m_ghost01.vc1";
connectAttr "place2dTexture15.o" "tx_enm_m_ghost01.uv";
connectAttr "place2dTexture15.ofs" "tx_enm_m_ghost01.fs";
connectAttr "mt_enm_m_ghost01_face.oc" "lambert10SG1.ss";
connectAttr "lambert10SG1.msg" "materialInfo31.sg";
connectAttr "mt_enm_m_ghost01_face.msg" "materialInfo31.m";
connectAttr "tx_enm_m_ghost01_face.msg" "materialInfo31.t" -na;
connectAttr "tx_enm_m_ghost01_face.oc" "mt_enm_m_ghost01_face.c";
connectAttr ":defaultColorMgtGlobals.cme" "tx_enm_m_ghost01_face.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "tx_enm_m_ghost01_face.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "tx_enm_m_ghost01_face.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "tx_enm_m_ghost01_face.ws";
connectAttr "place2dTexture16.c" "tx_enm_m_ghost01_face.c";
connectAttr "place2dTexture16.tf" "tx_enm_m_ghost01_face.tf";
connectAttr "place2dTexture16.rf" "tx_enm_m_ghost01_face.rf";
connectAttr "place2dTexture16.mu" "tx_enm_m_ghost01_face.mu";
connectAttr "place2dTexture16.mv" "tx_enm_m_ghost01_face.mv";
connectAttr "place2dTexture16.s" "tx_enm_m_ghost01_face.s";
connectAttr "place2dTexture16.wu" "tx_enm_m_ghost01_face.wu";
connectAttr "place2dTexture16.wv" "tx_enm_m_ghost01_face.wv";
connectAttr "place2dTexture16.re" "tx_enm_m_ghost01_face.re";
connectAttr "place2dTexture16.of" "tx_enm_m_ghost01_face.of";
connectAttr "place2dTexture16.r" "tx_enm_m_ghost01_face.ro";
connectAttr "place2dTexture16.n" "tx_enm_m_ghost01_face.n";
connectAttr "place2dTexture16.vt1" "tx_enm_m_ghost01_face.vt1";
connectAttr "place2dTexture16.vt2" "tx_enm_m_ghost01_face.vt2";
connectAttr "place2dTexture16.vt3" "tx_enm_m_ghost01_face.vt3";
connectAttr "place2dTexture16.vc1" "tx_enm_m_ghost01_face.vc1";
connectAttr "place2dTexture16.o" "tx_enm_m_ghost01_face.uv";
connectAttr "place2dTexture16.ofs" "tx_enm_m_ghost01_face.fs";
connectAttr "mt_enm_m_ghost01_eye.oc" "lambert12SG1.ss";
connectAttr "lambert12SG1.msg" "materialInfo33.sg";
connectAttr "mt_enm_m_ghost01_eye.msg" "materialInfo33.m";
connectAttr "tx_enm_m_ghost01_eye.msg" "materialInfo33.t" -na;
connectAttr "tx_enm_m_ghost01_eye.oc" "mt_enm_m_ghost01_eye.c";
connectAttr ":defaultColorMgtGlobals.cme" "tx_enm_m_ghost01_eye.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "tx_enm_m_ghost01_eye.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "tx_enm_m_ghost01_eye.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "tx_enm_m_ghost01_eye.ws";
connectAttr "place2dTexture17.c" "tx_enm_m_ghost01_eye.c";
connectAttr "place2dTexture17.tf" "tx_enm_m_ghost01_eye.tf";
connectAttr "place2dTexture17.rf" "tx_enm_m_ghost01_eye.rf";
connectAttr "place2dTexture17.mu" "tx_enm_m_ghost01_eye.mu";
connectAttr "place2dTexture17.mv" "tx_enm_m_ghost01_eye.mv";
connectAttr "place2dTexture17.s" "tx_enm_m_ghost01_eye.s";
connectAttr "place2dTexture17.wu" "tx_enm_m_ghost01_eye.wu";
connectAttr "place2dTexture17.wv" "tx_enm_m_ghost01_eye.wv";
connectAttr "place2dTexture17.re" "tx_enm_m_ghost01_eye.re";
connectAttr "place2dTexture17.of" "tx_enm_m_ghost01_eye.of";
connectAttr "place2dTexture17.r" "tx_enm_m_ghost01_eye.ro";
connectAttr "place2dTexture17.n" "tx_enm_m_ghost01_eye.n";
connectAttr "place2dTexture17.vt1" "tx_enm_m_ghost01_eye.vt1";
connectAttr "place2dTexture17.vt2" "tx_enm_m_ghost01_eye.vt2";
connectAttr "place2dTexture17.vt3" "tx_enm_m_ghost01_eye.vt3";
connectAttr "place2dTexture17.vc1" "tx_enm_m_ghost01_eye.vc1";
connectAttr "place2dTexture17.o" "tx_enm_m_ghost01_eye.uv";
connectAttr "place2dTexture17.ofs" "tx_enm_m_ghost01_eye.fs";
connectAttr "mt_enm_m_ghost01_mouth.oc" "mt_mouth0001_00SG1.ss";
connectAttr "mt_mouth0001_00SG1.msg" "materialInfo32.sg";
connectAttr "mt_enm_m_ghost01_mouth.msg" "materialInfo32.m";
connectAttr "tx_enm_m_ghost01_mouth.msg" "materialInfo32.t" -na;
connectAttr "tx_enm_m_ghost01_mouth.oc" "mt_enm_m_ghost01_mouth.c";
connectAttr ":defaultColorMgtGlobals.cme" "tx_enm_m_ghost01_mouth.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "tx_enm_m_ghost01_mouth.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "tx_enm_m_ghost01_mouth.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "tx_enm_m_ghost01_mouth.ws";
connectAttr "pasted__place2dTexture3.c" "tx_enm_m_ghost01_mouth.c";
connectAttr "pasted__place2dTexture3.tf" "tx_enm_m_ghost01_mouth.tf";
connectAttr "pasted__place2dTexture3.rf" "tx_enm_m_ghost01_mouth.rf";
connectAttr "pasted__place2dTexture3.mu" "tx_enm_m_ghost01_mouth.mu";
connectAttr "pasted__place2dTexture3.mv" "tx_enm_m_ghost01_mouth.mv";
connectAttr "pasted__place2dTexture3.s" "tx_enm_m_ghost01_mouth.s";
connectAttr "pasted__place2dTexture3.wu" "tx_enm_m_ghost01_mouth.wu";
connectAttr "pasted__place2dTexture3.wv" "tx_enm_m_ghost01_mouth.wv";
connectAttr "pasted__place2dTexture3.re" "tx_enm_m_ghost01_mouth.re";
connectAttr "pasted__place2dTexture3.of" "tx_enm_m_ghost01_mouth.of";
connectAttr "pasted__place2dTexture3.r" "tx_enm_m_ghost01_mouth.ro";
connectAttr "pasted__place2dTexture3.n" "tx_enm_m_ghost01_mouth.n";
connectAttr "pasted__place2dTexture3.vt1" "tx_enm_m_ghost01_mouth.vt1";
connectAttr "pasted__place2dTexture3.vt2" "tx_enm_m_ghost01_mouth.vt2";
connectAttr "pasted__place2dTexture3.vt3" "tx_enm_m_ghost01_mouth.vt3";
connectAttr "pasted__place2dTexture3.vc1" "tx_enm_m_ghost01_mouth.vc1";
connectAttr "pasted__place2dTexture3.o" "tx_enm_m_ghost01_mouth.uv";
connectAttr "pasted__place2dTexture3.ofs" "tx_enm_m_ghost01_mouth.fs";
connectAttr "renderLayerManager1.rlmi[0]" "defaultRenderLayer1.rlid";
connectAttr "tx_enm_m_ghost01_face.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "tx_enm_m_ghost01.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "lambert19SG.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "mt_enm_m_ghost01.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "lambert20SG.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "place2dTexture16.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "lambert12SG1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "mt_mouth0001_00SG1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "place2dTexture17.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "place2dTexture15.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "tx_enm_m_ghost01_mouth.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "mt_enm_m_ghost01_eye.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "lambert10SG1.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "pasted__place2dTexture3.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "mt_enm_m_ghost01_hair.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "tx_enm_m_ghost01_eye.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "mt_enm_m_ghost01_face.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "mt_enm_m_ghost01_mouth.msg" "hyperShadePrimaryNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "Root.msg" "bindPose1.m[1]";
connectAttr "Hip.msg" "bindPose1.m[2]";
connectAttr "Spine1.msg" "bindPose1.m[3]";
connectAttr "Spine2.msg" "bindPose1.m[4]";
connectAttr "Spine3.msg" "bindPose1.m[5]";
connectAttr "Neck.msg" "bindPose1.m[6]";
connectAttr "Head.msg" "bindPose1.m[7]";
connectAttr "Shoulder_L.msg" "bindPose1.m[8]";
connectAttr "Arm_L.msg" "bindPose1.m[9]";
connectAttr "Elbow_L.msg" "bindPose1.m[10]";
connectAttr "Wrist_L.msg" "bindPose1.m[11]";
connectAttr "Thumb_01_L.msg" "bindPose1.m[12]";
connectAttr "Thumb_02_L.msg" "bindPose1.m[13]";
connectAttr "Thumb_03_L.msg" "bindPose1.m[14]";
connectAttr "Index_01_L.msg" "bindPose1.m[15]";
connectAttr "Index_02_L.msg" "bindPose1.m[16]";
connectAttr "Index_03_L.msg" "bindPose1.m[17]";
connectAttr "Middle_01_L.msg" "bindPose1.m[18]";
connectAttr "Middle_02_L.msg" "bindPose1.m[19]";
connectAttr "Middle_03_L.msg" "bindPose1.m[20]";
connectAttr "Ring_01_L.msg" "bindPose1.m[21]";
connectAttr "Ring_02_L.msg" "bindPose1.m[22]";
connectAttr "Ring_03_L.msg" "bindPose1.m[23]";
connectAttr "Pinky_01_L.msg" "bindPose1.m[24]";
connectAttr "Pinky_02_L.msg" "bindPose1.m[25]";
connectAttr "Pinky_03_L.msg" "bindPose1.m[26]";
connectAttr "HandattachOffset_L.msg" "bindPose1.m[27]";
connectAttr "Handattach_L.msg" "bindPose1.m[28]";
connectAttr "WristRoll_L.msg" "bindPose1.m[29]";
connectAttr "ArmRoll_L.msg" "bindPose1.m[30]";
connectAttr "Shoulder_R.msg" "bindPose1.m[31]";
connectAttr "Arm_R.msg" "bindPose1.m[32]";
connectAttr "Elbow_R.msg" "bindPose1.m[33]";
connectAttr "Wrist_R.msg" "bindPose1.m[34]";
connectAttr "Thumb_01_R.msg" "bindPose1.m[35]";
connectAttr "Thumb_02_R.msg" "bindPose1.m[36]";
connectAttr "Thumb_03_R.msg" "bindPose1.m[37]";
connectAttr "Index_01_R.msg" "bindPose1.m[38]";
connectAttr "Index_02_R.msg" "bindPose1.m[39]";
connectAttr "Index_03_R.msg" "bindPose1.m[40]";
connectAttr "Middle_01_R.msg" "bindPose1.m[41]";
connectAttr "Middle_02_R.msg" "bindPose1.m[42]";
connectAttr "Middle_03_R.msg" "bindPose1.m[43]";
connectAttr "Ring_01_R.msg" "bindPose1.m[44]";
connectAttr "Ring_02_R.msg" "bindPose1.m[45]";
connectAttr "Ring_03_R.msg" "bindPose1.m[46]";
connectAttr "Pinky_01_R.msg" "bindPose1.m[47]";
connectAttr "Pinky_02_R.msg" "bindPose1.m[48]";
connectAttr "Pinky_03_R.msg" "bindPose1.m[49]";
connectAttr "HandattachOffset_R.msg" "bindPose1.m[50]";
connectAttr "Handattach_R.msg" "bindPose1.m[51]";
connectAttr "WristRoll_R.msg" "bindPose1.m[52]";
connectAttr "ArmRoll_R.msg" "bindPose1.m[53]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "bindPose1.m[2]" "bindPose1.p[3]";
connectAttr "bindPose1.m[3]" "bindPose1.p[4]";
connectAttr "bindPose1.m[4]" "bindPose1.p[5]";
connectAttr "bindPose1.m[5]" "bindPose1.p[6]";
connectAttr "bindPose1.m[6]" "bindPose1.p[7]";
connectAttr "bindPose1.m[5]" "bindPose1.p[8]";
connectAttr "bindPose1.m[8]" "bindPose1.p[9]";
connectAttr "bindPose1.m[9]" "bindPose1.p[10]";
connectAttr "bindPose1.m[10]" "bindPose1.p[11]";
connectAttr "bindPose1.m[11]" "bindPose1.p[12]";
connectAttr "bindPose1.m[12]" "bindPose1.p[13]";
connectAttr "bindPose1.m[13]" "bindPose1.p[14]";
connectAttr "bindPose1.m[11]" "bindPose1.p[15]";
connectAttr "bindPose1.m[15]" "bindPose1.p[16]";
connectAttr "bindPose1.m[16]" "bindPose1.p[17]";
connectAttr "bindPose1.m[11]" "bindPose1.p[18]";
connectAttr "bindPose1.m[18]" "bindPose1.p[19]";
connectAttr "bindPose1.m[19]" "bindPose1.p[20]";
connectAttr "bindPose1.m[11]" "bindPose1.p[21]";
connectAttr "bindPose1.m[21]" "bindPose1.p[22]";
connectAttr "bindPose1.m[22]" "bindPose1.p[23]";
connectAttr "bindPose1.m[11]" "bindPose1.p[24]";
connectAttr "bindPose1.m[24]" "bindPose1.p[25]";
connectAttr "bindPose1.m[25]" "bindPose1.p[26]";
connectAttr "bindPose1.m[11]" "bindPose1.p[27]";
connectAttr "bindPose1.m[27]" "bindPose1.p[28]";
connectAttr "bindPose1.m[10]" "bindPose1.p[29]";
connectAttr "bindPose1.m[9]" "bindPose1.p[30]";
connectAttr "bindPose1.m[5]" "bindPose1.p[31]";
connectAttr "bindPose1.m[31]" "bindPose1.p[32]";
connectAttr "bindPose1.m[32]" "bindPose1.p[33]";
connectAttr "bindPose1.m[33]" "bindPose1.p[34]";
connectAttr "bindPose1.m[34]" "bindPose1.p[35]";
connectAttr "bindPose1.m[35]" "bindPose1.p[36]";
connectAttr "bindPose1.m[36]" "bindPose1.p[37]";
connectAttr "bindPose1.m[34]" "bindPose1.p[38]";
connectAttr "bindPose1.m[38]" "bindPose1.p[39]";
connectAttr "bindPose1.m[39]" "bindPose1.p[40]";
connectAttr "bindPose1.m[34]" "bindPose1.p[41]";
connectAttr "bindPose1.m[41]" "bindPose1.p[42]";
connectAttr "bindPose1.m[42]" "bindPose1.p[43]";
connectAttr "bindPose1.m[34]" "bindPose1.p[44]";
connectAttr "bindPose1.m[44]" "bindPose1.p[45]";
connectAttr "bindPose1.m[45]" "bindPose1.p[46]";
connectAttr "bindPose1.m[34]" "bindPose1.p[47]";
connectAttr "bindPose1.m[47]" "bindPose1.p[48]";
connectAttr "bindPose1.m[48]" "bindPose1.p[49]";
connectAttr "bindPose1.m[34]" "bindPose1.p[50]";
connectAttr "bindPose1.m[50]" "bindPose1.p[51]";
connectAttr "bindPose1.m[33]" "bindPose1.p[52]";
connectAttr "bindPose1.m[32]" "bindPose1.p[53]";
connectAttr "Root.bps" "bindPose1.wm[1]";
connectAttr "Hip.bps" "bindPose1.wm[2]";
connectAttr "Spine1.bps" "bindPose1.wm[3]";
connectAttr "Spine2.bps" "bindPose1.wm[4]";
connectAttr "Spine3.bps" "bindPose1.wm[5]";
connectAttr "Neck.bps" "bindPose1.wm[6]";
connectAttr "Head.bps" "bindPose1.wm[7]";
connectAttr "Shoulder_L.bps" "bindPose1.wm[8]";
connectAttr "Arm_L.bps" "bindPose1.wm[9]";
connectAttr "Elbow_L.bps" "bindPose1.wm[10]";
connectAttr "Wrist_L.bps" "bindPose1.wm[11]";
connectAttr "Thumb_01_L.bps" "bindPose1.wm[12]";
connectAttr "Thumb_02_L.bps" "bindPose1.wm[13]";
connectAttr "Thumb_03_L.bps" "bindPose1.wm[14]";
connectAttr "Index_01_L.bps" "bindPose1.wm[15]";
connectAttr "Index_02_L.bps" "bindPose1.wm[16]";
connectAttr "Index_03_L.bps" "bindPose1.wm[17]";
connectAttr "Middle_01_L.bps" "bindPose1.wm[18]";
connectAttr "Middle_02_L.bps" "bindPose1.wm[19]";
connectAttr "Middle_03_L.bps" "bindPose1.wm[20]";
connectAttr "Ring_01_L.bps" "bindPose1.wm[21]";
connectAttr "Ring_02_L.bps" "bindPose1.wm[22]";
connectAttr "Ring_03_L.bps" "bindPose1.wm[23]";
connectAttr "Pinky_01_L.bps" "bindPose1.wm[24]";
connectAttr "Pinky_02_L.bps" "bindPose1.wm[25]";
connectAttr "Pinky_03_L.bps" "bindPose1.wm[26]";
connectAttr "HandattachOffset_L.bps" "bindPose1.wm[27]";
connectAttr "Handattach_L.bps" "bindPose1.wm[28]";
connectAttr "WristRoll_L.bps" "bindPose1.wm[29]";
connectAttr "ArmRoll_L.bps" "bindPose1.wm[30]";
connectAttr "Shoulder_R.bps" "bindPose1.wm[31]";
connectAttr "Arm_R.bps" "bindPose1.wm[32]";
connectAttr "Elbow_R.bps" "bindPose1.wm[33]";
connectAttr "Wrist_R.bps" "bindPose1.wm[34]";
connectAttr "Thumb_01_R.bps" "bindPose1.wm[35]";
connectAttr "Thumb_02_R.bps" "bindPose1.wm[36]";
connectAttr "Thumb_03_R.bps" "bindPose1.wm[37]";
connectAttr "Index_01_R.bps" "bindPose1.wm[38]";
connectAttr "Index_02_R.bps" "bindPose1.wm[39]";
connectAttr "Index_03_R.bps" "bindPose1.wm[40]";
connectAttr "Middle_01_R.bps" "bindPose1.wm[41]";
connectAttr "Middle_02_R.bps" "bindPose1.wm[42]";
connectAttr "Middle_03_R.bps" "bindPose1.wm[43]";
connectAttr "Ring_01_R.bps" "bindPose1.wm[44]";
connectAttr "Ring_02_R.bps" "bindPose1.wm[45]";
connectAttr "Ring_03_R.bps" "bindPose1.wm[46]";
connectAttr "Pinky_01_R.bps" "bindPose1.wm[47]";
connectAttr "Pinky_02_R.bps" "bindPose1.wm[48]";
connectAttr "Pinky_03_R.bps" "bindPose1.wm[49]";
connectAttr "HandattachOffset_R.bps" "bindPose1.wm[50]";
connectAttr "Handattach_R.bps" "bindPose1.wm[51]";
connectAttr "WristRoll_R.bps" "bindPose1.wm[52]";
connectAttr "ArmRoll_R.bps" "bindPose1.wm[53]";
connectAttr "lambert19SG.pa" ":renderPartition.st" -na;
connectAttr "lambert20SG.pa" ":renderPartition.st" -na;
connectAttr "lambert10SG1.pa" ":renderPartition.st" -na;
connectAttr "mt_mouth0001_00SG1.pa" ":renderPartition.st" -na;
connectAttr "lambert12SG1.pa" ":renderPartition.st" -na;
connectAttr "mt_enm_m_ghost01.msg" ":defaultShaderList1.s" -na;
connectAttr "mt_enm_m_ghost01_hair.msg" ":defaultShaderList1.s" -na;
connectAttr "mt_enm_m_ghost01_face.msg" ":defaultShaderList1.s" -na;
connectAttr "mt_enm_m_ghost01_mouth.msg" ":defaultShaderList1.s" -na;
connectAttr "mt_enm_m_ghost01_eye.msg" ":defaultShaderList1.s" -na;
connectAttr "place2dTexture15.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "place2dTexture16.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "pasted__place2dTexture3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "place2dTexture17.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "defaultRenderLayer1.msg" ":defaultRenderingList1.r" -na;
connectAttr "tx_enm_m_ghost01.msg" ":defaultTextureList1.tx" -na;
connectAttr "tx_enm_m_ghost01_face.msg" ":defaultTextureList1.tx" -na;
connectAttr "tx_enm_m_ghost01_mouth.msg" ":defaultTextureList1.tx" -na;
connectAttr "tx_enm_m_ghost01_eye.msg" ":defaultTextureList1.tx" -na;
// End of enm_m_ghost01.ma
