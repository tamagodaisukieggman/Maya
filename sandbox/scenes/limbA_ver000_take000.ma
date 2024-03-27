//Maya ASCII 2024 scene
//Name: limbA_ver000_take000.ma
//Last modified: Thu, Mar 28, 2024 02:21:14 AM
//Codeset: 932
file -rdi 1 -ns "rig" -rfn "rigRN" -op "v=0;" -typ "mayaAscii" "F:/myTechData/Maya/sandbox/scenes/sheriff_public.ma";
file -r -ns "rig" -dr 1 -rfn "rigRN" -op "v=0;" -typ "mayaAscii" "F:/myTechData/Maya/sandbox/scenes/sheriff_public.ma";
requires maya "2024";
requires "stereoCamera" "10.0";
requires -nodeType "aiOptions" -nodeType "aiAOVDriver" -nodeType "aiAOVFilter" "mtoa" "5.3.4.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202310181224-69282f2959";
fileInfo "osv" "Windows 11 Home v2009 (Build: 22621)";
fileInfo "UUID" "F6D754B1-4DA8-9522-C809-E289E4B8741C";
createNode joint -n "BIND_Chest_C";
	rename -uid "E2764E8F-48C2-DB44-A087-C8B67F86E5E1";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 105.049 -1.1 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999933 4.3710553501741204e-08 -1.1436028885673988e-16 0
		 -4.3710553437273811e-08 0.99999999999999911 8.6736173798840355e-18 0 1.1482049200142649e-16 -1.214306433183765e-17 0.99999999999999989 0
		 -1.2811594138854995e-28 105.04879351239208 -1.1004180029751793 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Chest";
createNode joint -n "BIND_Clavicle_L" -p "BIND_Chest_C";
	rename -uid "C254DCFE-4D59-D42C-7137-ECBCC01B9EB6";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.026 8.865 -1.542 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 -6.6174449004242214e-24 -1.1436028923586835e-16 0
		 6.4467406300283881e-17 0.99999999999999989 8.6736123811325012e-18 0 1.1482049200142652e-16 -1.2143064331837653e-17 1 0
		 4.0260253782354685 113.91371115676378 -2.642038275836132 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Clavicle";
createNode joint -n "BIND_Arm_L" -p "BIND_Clavicle_L";
	rename -uid "9DF44D79-4F6A-B7BC-484A-62942FC12D08";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 26.404 8.466 -9.062 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.21000000000000002 -1.222 -9.762 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439612 -0.16952484750455285 0.021321074998423905 0
		 0.16948517073621269 0.98552591344852991 0.0036675362246039642 0 -0.021634210432719719 -1.1747525411052479e-13 0.99976595308049554 0
		 30.430489621480859 122.380143709444 -11.704340738304499 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm";
createNode joint -n "BIND_ForeArm_L" -p "BIND_Arm_L";
	rename -uid "C3918661-4CC3-4DA4-D8E5-1C861A816904";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 26.882 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.037 -11.933000000000002 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012563 -0.16586152129859458 0.22757700045776189 0
		 0.16138450661701506 0.9861490535170212 0.038276432324170884 0 -0.23077343089883465 6.0947389996795216e-15 0.97300751466326385 0
		 56.917241716559026 117.82296900376835 -11.131186624846158 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm";
createNode joint -n "BIND_Hand_L" -p "BIND_ForeArm_L";
	rename -uid "240D8F7F-4535-FCF1-0702-469E5F2A2188";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 32.707 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.061 -0.146 -13.225 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89656909193257572 -0.3870701856452341 0.21526851784634216 0
		 0.37637337363557832 0.9220502542619704 0.09036820366483532 0 -0.23346722898379171 -1.0065375522609562e-15 0.9723646707849013 0
		 88.30041051211505 112.39816963888347 -3.687871515471894 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Hand";
createNode joint -n "BIND_Front_Hand_L" -p "BIND_Hand_L";
	rename -uid "D073661A-46FC-24FD-1526-D99F0B785146";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.152 9.933 -0.003 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.018 0.077 6.613 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.93426053266779263 -0.2783173218769589 0.22292762377625994 0
		 0.27069781410264032 0.96048917846280712 0.064677905778513317 0 -0.23212055173841206 -7.9994245141848356e-05 0.97268702215130609 0
		 91.007388653141462 122.00306142351162 -3.0410924576867506 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Front_Hand";
createNode joint -n "BIND_Back_Hand_L" -p "BIND_Hand_L";
	rename -uid "F19372A5-4B14-B9A2-28B9-15A06128AF98";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.152 -9.933 0.003 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.982 0.077 6.613 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.93426053266779263 -0.2783173218769589 0.22292762377625994 0
		 -0.27069778941492334 -0.96048917845429393 -0.064678009230879796 0 0.23212058052909987 8.0096400178942067e-05 -0.97268701527233348 0
		 85.593432371088682 102.79327785425548 -4.3346505732570213 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Back_Hand";
createNode joint -n "BIND_Left_Hand_L" -p "BIND_Hand_L";
	rename -uid "F7CFE87E-4393-A6B9-56FE-4F9270BD889E";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.013 -0.005 -10 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -90.018 0.077 6.613 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.93426053266779263 -0.2783173218769589 0.22292762377625994 0
		 0.23212055173841206 7.9994245141781135e-05 -0.97268702215130609 0 0.27069781410264027 0.9604891784628069 0.064677905778513109 0
		 90.621616029499194 112.39896958133497 -13.414741736984956 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Left_Hand";
createNode joint -n "BIND_Right_Hand_L" -p "BIND_Hand_L";
	rename -uid "EFBCB3C3-4A9F-7D87-FA61-4FA06064368E";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.013 0.005 10 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 89.982 0.077 6.613 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.93426053266779263 -0.27831732187695885 0.22292762377625994 0
		 -0.23212056009198481 -8.0023885263898201e-05 0.97268702015538422 0 -0.27069780693953871 -0.96048917846033821 -0.06467793579505357 0
		 85.979204994730964 112.39736969643214 6.0389987060411769 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Right_Hand";
createNode joint -n "BIND_Index_Meta_L" -p "BIND_Hand_L";
	rename -uid "9912C309-4843-1B1D-3E7E-94BCCD52A8AE";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.394 -0.198 3.932 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.274 1.54 -0.389 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89994695677261671 -0.39317176694500955 0.18844478414921731 0
		 0.3969833951522892 0.91763523489930821 0.01870186206377189 0 -0.18027661792109187 0.057978766360023797 0.98190569999481203 0
		 90.351203361731876 110.90140369744074 0.84811265525244828 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_Meta";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Index_00_L" -p "BIND_Index_Meta_L";
	rename -uid "D074CA49-41F2-DD70-3AA7-C7A95A6A51F3";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.674 -0.008 1.75 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.5050000000000008 0 -16.133 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.75419898261622842 -0.6326679099811261 0.17582721717856836 0
		 0.60245933061895307 0.7732071277640008 0.19797346419433834 0 -0.26120231540093375 -0.043382637714386746 0.96430871466254686 0
		 96.039084295213755 108.37181107953495 3.824123589660068 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_00";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Index_01_L" -p "BIND_Index_00_L";
	rename -uid "CBCD53A4-49A9-90AD-5084-1FB41F238B74";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.647 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -6.828 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.67722301312372035 -0.72010763941478995 0.15104296790015873 0
		 0.68785342982703845 0.69250482626578225 0.21747350338323529 0 -0.26120231540093386 -0.043382637714386767 0.96430871466254731 0
		 98.035736762381163 106.69689773109866 4.2896053193714696 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_01";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Index_02_L" -p "BIND_Index_01_L";
	rename -uid "6B26EEBC-472E-1502-EB2E-668A4F62F34E";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.314 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.67722301312372024 -0.72010763941478984 0.1510429679001587 0
		 0.68785342982703845 0.69250482626578225 0.21747350338323529 0 -0.26120231540093375 -0.043382637714386753 0.96430871466254697 0
		 99.60290953484612 105.03048494850637 4.6391363042586748 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_02";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Index_03_L" -p "BIND_Index_02_L";
	rename -uid "882969BE-4F24-7947-E0E0-229AF3A3F523";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.711 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.67722301312372024 -0.72010763941478984 0.1510429679001587 0
		 0.68785342982703845 0.69250482626578225 0.21747350338323529 0 -0.26120231540093369 -0.043382637714386746 0.96430871466254686 0
		 102.11627189424161 102.35796585133332 5.199698634266646 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Index_03";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Middle_Meta_L" -p "BIND_Hand_L";
	rename -uid "38ADD274-44AC-953B-BEC1-8694CAA29961";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.396 -0.386 1.785 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.698 2.527 -0.98100000000000009 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89942261302113025 -0.40240645092385979 0.1706107014260991 0
		 0.39400031467254504 0.9154372416637383 0.082087810380234758 0 -0.18921605435104508 -0.0066109628609872005 0.9819132242443176 0
		 90.783058705945891 110.72824091329491 -1.2556750951170961 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_Meta";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Middle_00_L" -p "BIND_Middle_Meta_L";
	rename -uid "04186215-41AE-8B8A-D6B9-78A130911078";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.62 -0.027 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 1 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.90616188022879929 -0.3863685796629428 0.17201734642020303 0
		 0.37824321751490819 0.92232077707232174 0.079097740705274214 0 -0.18921605435104524 -0.0066109628609872066 0.98191322424431848 0
		 96.726407903853584 108.03961919523081 -0.12848515693804274 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_00";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Middle_01_L" -p "BIND_Middle_00_L";
	rename -uid "27AE0A81-4A5A-B212-3D33-1ABC1CE2CF2F";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.855 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -17.001 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.75596327028722832 -0.63916628183654423 0.14137184351873586 0
		 0.62667122061928204 0.76904015456496011 0.12593816702747804 0 -0.18921605435104519 -0.0066109628609872049 0.98191322424431826 0
		 99.313135835924541 106.93669220294051 0.36255522391922362 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_01";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Middle_02_L" -p "BIND_Middle_01_L";
	rename -uid "259B87BC-425C-0200-44EC-3381E7DF4C7D";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.504 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -4.008 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.71031530858004843 -0.69135299297348207 0.13222405796011244 0
		 0.67797451808504772 0.72248690941542948 0.13551095361884119 0 -0.18921605435104519 -0.0066109628609872049 0.98191322424431826 0
		 101.20581189111464 105.33643625868336 0.71650245075270202 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_02";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Middle_03_L" -p "BIND_Middle_02_L";
	rename -uid "05EB7F6C-43B4-F41E-2929-83A7F2D14B43";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.174 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.71031530858004843 -0.69135299297348207 0.13222405796011244 0
		 0.67797451808504783 0.72248690941542959 0.13551095361884122 0 -0.18921605435104524 -0.0066109628609872066 0.98191322424431848 0
		 104.17098080056142 102.450424405277 1.268463898026235 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Middle_03";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Ring_Meta_L" -p "BIND_Hand_L";
	rename -uid "AB16460D-49E9-ED52-8050-029BA6B9CF36";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.475 -0.468 -1.374 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.8569999999999998 6.608 -1.1710000000000003 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.90965397338006215 -0.40313418872282297 0.10006235354345676 0
		 0.4024420734985753 0.91501988699008652 0.027910282886705579 0 -0.10281063267985285 0.014880601313122932 0.99458963473008755 0
		 90.663711307538875 111.00844524902794 -4.5333943798652925 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_Meta";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Ring_00_L" -p "BIND_Ring_Meta_L";
	rename -uid "44FF47C4-4D78-4F3A-1A09-3AB160389B63";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.16 -0.027 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 2 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.92314486257451833 -0.37095487673864147 0.10097545308684287 0
		 0.37045045081662703 0.9285316618879399 0.024401154918947298 0 -0.10281063267985283 0.014880601313122929 0.99458963473008732 0
		 97.166072442093608 108.09748723466741 -3.8176935089221367 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_00";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Ring_01_L" -p "BIND_Ring_00_L";
	rename -uid "AA5ADD9F-4595-0037-1B84-0598508AEAF6";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.091 -0.014 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -20.256 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.73779885516427846 -0.66948349056937673 0.086282704949041569 0
		 0.66714527887578479 0.74267787334725655 0.057851130621175487 0 -0.10281063267985285 0.014880601313122932 0.99458963473008755 0
		 100.01463901300106 106.93789173773337 -3.5058881182051715 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_01";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Ring_02_L" -p "BIND_Ring_01_L";
	rename -uid "5CA92F38-400B-E34C-9141-C087D30993FE";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.368 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -2.843 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70379547785033825 -0.70550118767075998 0.083306659713140135 0
		 0.70292382173702317 0.70855249763140848 0.062060123548948416 0 -0.10281063267985283 0.014880601313122929 0.99458963473008732 0
		 101.76210099712469 105.35223334238673 -3.3015292394532829 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_02";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Ring_03_L" -p "BIND_Ring_02_L";
	rename -uid "A6C2FABA-4822-2DBB-3E1A-C1950447AFC6";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.121 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.70379547785033825 -0.70550118767075998 0.083306659713140135 0
		 0.70292382173702306 0.70855249763140837 0.062060123548948402 0 -0.10281063267985281 0.014880601313122927 0.99458963473008721 0
		 104.66231344565419 102.44497494964871 -2.9580433414908667 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Ring_03";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Pinky_Meta_L" -p "BIND_Hand_L";
	rename -uid "029DEE0B-4E8B-FD3B-E0A9-14BCCF2F0FC3";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.197 -0.748 -4.114 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -6.761 12.45 -2.767 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.90705750093428605 -0.42098845521317524 -0.0039256306590547962 0
		 0.42086847941769173 0.90695912514563692 -0.017171731063014187 0 0.010789487081735438 0.013923573258501376 0.99984484850212019 0
		 90.94891462754498 110.85787743135026 -7.2826670538498286 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_Meta";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Pinky_00_L" -p "BIND_Pinky_Meta_L";
	rename -uid "93F573CD-4E29-C43B-967F-148A27F79CFF";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.903 -0.011 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -10.316 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.81702532400106331 -0.57660124911669297 -0.00078705655874466551 0
		 0.57650082992955887 0.81690705323481239 -0.017597143681436896 0 0.010789487081735438 0.013923573258501376 0.99984484850212019 0
		 97.205974951803626 107.94201949029684 -7.3095825397123706 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_00";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Pinky_01_L" -p "BIND_Pinky_00_L";
	rename -uid "CE0D543C-41F2-69AB-4C7B-309F19C99C12";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.255 -0.022 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -8.498 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.72286133693530574 -0.69099071465271156 0.0018220394718148852 0
		 0.69090887570837789 0.72272952504477772 -0.017520248169901758 0 0.010789487081735438 0.013923573258501376 0.99984484850212019 0
		 99.03595638277001 106.62374548066714 -7.3109722315865175 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_01";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Pinky_02_L" -p "BIND_Pinky_01_L";
	rename -uid "10693EFA-496B-5586-BF42-AF91BE35020C";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.846 0.011 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -4.425 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.66740250866517437 -0.7446904412048263 0.0031683127359270107 0
		 0.74461901560190125 0.66726477569693166 -0.017327455617578716 0 0.010789487081735438 0.013923573258501376 0.99984484850212019 0
		 100.37807104430885 105.35554896058866 -7.3077946402278604 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_02";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Pinky_03_L" -p "BIND_Pinky_02_L";
	rename -uid "91EAFF1C-4654-9242-EDB2-AEB25469BD60";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.407 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.66740250866517448 -0.74469044120482641 0.0031683127359270116 0
		 0.74461901560190125 0.66726477569693166 -0.017327455617578716 0 0.010789487081735438 0.013923573258501376 0.99984484850212019 0
		 102.65161976552957 102.81871402466211 -7.2970015831510855 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Pinky_03";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Thumb_00_L" -p "BIND_Hand_L";
	rename -uid "B2A44357-451A-C90C-B5DC-1D9786BF9757";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.938 -0.641 4.817 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 86.534 -38.111 -38.801 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.22010577876250176 -0.69194404664768516 0.6875804552662752 0
		 -0.41682803391382284 0.57055902164102423 0.70761344883175703 0 -0.88193414510318702 -0.44235261854414626 -0.16283833875426024 0
		 89.568458090185146 110.66960805818042 1.5702029206844124 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_00";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Thumb_01_L" -p "BIND_Thumb_00_L";
	rename -uid "0DE0DA23-47F4-84BF-3692-369D35AA7586";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.664 0.007 -0.005 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -3.199 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.2430264644975649 -0.72270927474749858 0.6470157971392646 0
		 -0.4038938661575297 0.5310513200590572 0.74488538738778853 0 -0.88193417125890849 -0.44235257392432692 -0.16283831830495402 0
		 90.375858509244324 108.14053984331932 4.0953552222502783 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_01";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Thumb_02_L" -p "BIND_Thumb_01_L";
	rename -uid "87DE096D-45A4-5FC3-5DD3-AA9FC6EAE487";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.174 -0.065 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -5 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.27730334532463885 -0.76624332000206019 0.57963266749207931 0
		 -0.38117577603728525 0.46604224582621523 0.79844201597087172 0 -0.88193417125890849 -0.44235257392432692 -0.16283831830495402 0
		 91.173676966100388 105.81185235912949 6.1002736366188435 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_02";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_Thumb_03_L" -p "BIND_Thumb_02_L";
	rename -uid "87DF7001-40A1-8FF6-2EAF-7890233E4E07";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.612 -0.141 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -5 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.30946978025345412 -0.80394579092103946 0.50783818325350671 0
		 -0.35555670810117113 0.39748630869863488 0.84592201869994543 0 -0.88193417125890838 -0.44235257392432686 -0.16283831830495399 0
		 92.783525972309732 101.44631944930602 9.240344569498955 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Thumb_03";
	setAttr ".radi" 0.5;
createNode joint -n "BIND_ForeArm_00_L" -p "BIND_ForeArm_L";
	rename -uid "D650732B-41A3-8AD8-C2B9-FEBA82AAF420";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012552 -0.16586152129859455 0.22757700045776186 0
		 0.16138450661701509 0.98614905351702142 0.038276432324170891 0 -0.23077343089883456 6.0947389996795192e-15 0.97300751466326352 0
		 56.917241716558983 117.82296900376826 -11.131186624846139 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_00";
createNode joint -n "BIND_Front_ForeArm_00_L" -p "BIND_ForeArm_00_L";
	rename -uid "5CA324FC-4B56-8688-5814-B79DD7E1C9C2";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.039 0.176 9.944 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.024 5.965 -0.16 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.97786570305146725 -0.16769347303755475 0.12513019578128237 0
		 0.16634980941899313 0.98583918032076545 0.021186114574118717 0 -0.1269110227755022 9.8209397828084502e-05 0.9919141004406532 0
		 55.64813148880377 117.8239510977466 -1.2120456204396248 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Front_ForeArm_00";
createNode joint -n "BIND_Back_ForeArm_00_L" -p "BIND_ForeArm_00_L";
	rename -uid "243ADCF9-4CBB-C78D-1122-ABBA1B212783";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.039 -0.176 -9.944 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 178.976 5.965 -0.16 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.97786570305146714 -0.16769347303755472 0.1251301957812824 0
		 -0.16634982009232269 -0.98583918031250217 -0.021186031153258161 0 0.1269110087853344 -9.829230778235116e-05 -0.99191410222242071 0
		 58.186351944314211 117.82198690978997 -21.050327629252642 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Back_ForeArm_00";
createNode joint -n "BIND_ForeArm_01_L" -p "BIND_ForeArm_L";
	rename -uid "619FD717-4492-2A4F-F368-6998B4A3EC2A";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.672 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012563 -0.16586152129859458 0.22757700045776189 0
		 0.16138450661701509 0.98614905351702142 0.038276432324170891 0 -0.23077343089883459 6.09473899967952e-15 0.97300751466326363 0
		 61.400551718796436 117.04799763579848 -10.067855853595656 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_01";
createNode joint -n "BIND_ForeArm_02_L" -p "BIND_ForeArm_L";
	rename -uid "6FE66178-42E7-D650-33EF-7B93093FDD3F";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.345 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012563 -0.16586152129859458 0.22757700045776189 0
		 0.16138450661701506 0.9861490535170212 0.038276432324170884 0 -0.2307734308988347 6.0947389996795232e-15 0.97300751466326407 0
		 65.883861420453812 116.27302631978606 -9.0045251536353703 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_02";
createNode joint -n "BIND_ForeArm_03_L" -p "BIND_ForeArm_L";
	rename -uid "26C1965D-4DCB-FD78-965B-64A1AD42ECF6";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 14.017 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012552 -0.16586152129859455 0.22757700045776186 0
		 0.16138450661701506 0.9861490535170212 0.038276432324170884 0 -0.23077343089883459 6.09473899967952e-15 0.97300751466326363 0
		 70.367171202147318 115.49805498993882 -7.9411944346924779 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_03";
createNode joint -n "BIND_ForeArm_04_L" -p "BIND_ForeArm_L";
	rename -uid "590F9E11-40D5-3BBE-DF1A-E891C259320D";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 18.69 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012519 -0.16586152129859449 0.22757700045776177 0
		 0.16138450661701503 0.98614905351702109 0.038276432324170877 0 -0.23077343089883448 6.0947389996795177e-15 0.97300751466326318 0
		 74.850481026526722 114.72308365271306 -6.8778637056255478 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_04";
createNode joint -n "BIND_ForeArm_05_L" -p "BIND_ForeArm_L";
	rename -uid "7645AE40-474B-9ED2-E5F1-DCA9004FCBC9";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 23.362 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012563 -0.16586152129859458 0.22757700045776189 0
		 0.16138450661701503 0.98614905351702109 0.038276432324170877 0 -0.23077343089883454 6.0947389996795192e-15 0.97300751466326341 0
		 79.333790808220215 113.94811232286585 -5.8145329866826616 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_05";
createNode joint -n "BIND_ForeArm_06_L" -p "BIND_ForeArm_L";
	rename -uid "ACD85216-4FB6-80B8-C2EB-89ADEF5C7D24";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 28.034 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012541 -0.16586152129859455 0.22757700045776183 0
		 0.16138450661701503 0.98614905351702109 0.038276432324170877 0 -0.23077343089883448 6.0947389996795169e-15 0.97300751466326307 0
		 83.817100509877605 113.1731410068534 -4.7512022867223758 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_06";
createNode joint -n "BIND_ForeArm_07_L" -p "BIND_ForeArm_L";
	rename -uid "4A7C9371-4ED2-FCBD-A392-06A4917C8CA6";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 32.707 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95953043965012585 -0.16586152129859461 0.22757700045776194 0
		 0.16138450661701514 0.98614905351702165 0.038276432324170898 0 -0.2307734308988347 6.0947389996795232e-15 0.97300751466326407 0
		 88.300410512115093 112.39816963888366 -3.687871515471894 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ForeArm_07";
createNode joint -n "BIND_Arm_00_L" -p "BIND_Arm_L";
	rename -uid "476FEB45-4627-C215-A2D5-CCAEBF9D46D0";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439578 -0.16952484750455279 0.021321074998423898 0
		 0.16948517073621264 0.98552591344852958 0.0036675362246039629 0 -0.021634210432719733 -1.1747525411052487e-13 0.99976595308049621 0
		 30.43048962148087 122.38014370944406 -11.704340738304499 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_00";
createNode joint -n "BIND_Left_Arm_00_L" -p "BIND_Arm_00_L";
	rename -uid "F643A77A-4B11-6EDD-FB63-88BD8BCFD407";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 10 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -90 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439578 -0.16952484750455279 0.021321074998423898 0
		 0.021634217841152045 4.3078824657629142e-08 -0.99976595292018211 0 0.16948516979055114 0.98552591344852902 0.0036675799257630637 0
		 32.125341328842929 132.23540284392936 -11.667665376058464 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Left_Arm_00";
createNode joint -n "BIND_Arm_01_L" -p "BIND_Arm_L";
	rename -uid "EFB5D1E0-4A55-8E2D-C773-11A1B7D96AA9";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.84 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439589 -0.16952484750455282 0.021321074998423901 0
		 0.16948517073621261 0.98552591344852947 0.0036675362246039625 0 -0.021634210432719739 -1.1747525411052489e-13 0.99976595308049643 0
		 34.214311349349181 121.72911875149038 -11.622461579239022 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_01";
createNode joint -n "BIND_Arm_02_L" -p "BIND_Arm_L";
	rename -uid "064BBE73-465E-7F4D-C60A-F48B577C73AD";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.681 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439589 -0.16952484750455282 0.021321074998423901 0
		 0.16948517073621264 0.98552591344852958 0.0036675362246039629 0 -0.021634210432719722 -1.1747525411052482e-13 0.99976595308049576 0
		 37.998133077217489 121.07809379353671 -11.540582420173548 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_02";
createNode joint -n "BIND_Arm_03_L" -p "BIND_Arm_L";
	rename -uid "E589DB6A-4D09-D923-EAA8-7893EB787790";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 11.521 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439589 -0.16952484750455282 0.021321074998423901 0
		 0.16948517073621269 0.98552591344852991 0.0036675362246039642 0 -0.021634210432719743 -1.1747525411052492e-13 0.99976595308049665 0
		 41.781954805085789 120.42706883558306 -11.458703261108072 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_03";
createNode joint -n "BIND_Arm_04_L" -p "BIND_Arm_L";
	rename -uid "859D2482-4A1F-E927-DA2F-5BB18D72FDF8";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 15.361 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439589 -0.16952484750455282 0.021321074998423901 0
		 0.16948517073621269 0.98552591344852991 0.0036675362246039642 0 -0.021634210432719743 -1.1747525411052492e-13 0.99976595308049665 0
		 45.565776532954096 119.77604387762941 -11.376824102042594 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_04";
createNode joint -n "BIND_Arm_05_L" -p "BIND_Arm_L";
	rename -uid "55237B59-44B5-BC74-1DE2-E1BC70AB514C";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 19.201 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439589 -0.16952484750455282 0.021321074998423901 0
		 0.16948517073621264 0.98552591344852958 0.0036675362246039629 0 -0.021634210432719729 -1.1747525411052484e-13 0.99976595308049598 0
		 49.349598260822418 119.12501891967574 -11.294944942977121 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_05";
createNode joint -n "BIND_Arm_06_L" -p "BIND_Arm_L";
	rename -uid "8818FE71-4109-6FD8-67BE-CCB729208595";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 23.042 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439567 -0.16952484750455277 0.021321074998423895 0
		 0.16948517073621261 0.98552591344852936 0.0036675362246039621 0 -0.021634210432719733 -1.1747525411052487e-13 0.99976595308049621 0
		 53.133419988690733 118.47399396172209 -11.213065783911643 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_06";
createNode joint -n "BIND_Arm_07_L" -p "BIND_Arm_L";
	rename -uid "EB7C1106-4F65-E1E8-2DE5-0987DDFB98E8";
	addAttr -s false -ci true -sn "Guide" -ln "Guide" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 26.882 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.98529525414439556 -0.16952484750455277 0.021321074998423895 0
		 0.16948517073621264 0.98552591344852958 0.0036675362246039629 0 -0.021634210432719729 -1.1747525411052484e-13 0.99976595308049598 0
		 56.917241716559033 117.82296900376843 -11.131186624846169 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Arm_07";
createNode transform -s -n "persp";
	rename -uid "6F045CB2-462F-89AB-1BB9-E08BFF2250BE";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 144.95903613868438 336.70587037067685 52.122100036698214 ;
	setAttr ".r" -type "double3" -65.138352729631748 49.800000000008353 4.9275959399903007e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "F6CB4546-4AA8-48C0-6C83-33B1B0F45C25";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 252.3627326541752;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 99.275111541403163 104.92662620605991 4.5532557938752856 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "96D43CBD-4658-32EF-92EF-F99BBB51A2D5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "9517FA35-4FA6-5D6A-E9EC-2B8A9601FC96";
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
	rename -uid "762A2C9F-4F55-AC04-9F49-3D9A67E07315";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "04366741-422A-5810-D001-CABB2B38747B";
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
	rename -uid "21064D5E-4C2B-E6A0-3BE1-0C959D685BD1";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "06487572-431E-C002-92D4-EF9C49EBE2B9";
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
createNode lightLinker -s -n "lightLinker1";
	rename -uid "BA359761-4E6B-5A8A-5ADC-94954D8281D6";
	setAttr -s 14 ".lnk";
	setAttr -s 14 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "3B66DBA6-4B1D-68A9-4AF8-2582FB8E97EF";
	setAttr ".bsdt[0].bscd" -type "Int32Array" 1 0 ;
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "E493A372-4F68-93E5-E60B-1889B1145676";
createNode displayLayerManager -n "layerManager";
	rename -uid "7827147B-4402-4C34-152A-4DB103E4397A";
createNode displayLayer -n "defaultLayer";
	rename -uid "144C619C-4D99-6055-ECC4-8793DB8066EE";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "C1968F11-4553-098D-0B7F-2A8FE0F68E94";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "0A01AB68-4892-E6EF-0A7E-C7AEE00C4F2F";
	setAttr ".g" yes;
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "27123656-4FF7-0CFB-3E2C-6D9CF7923195";
	setAttr ".version" -type "string" "5.3.4.1";
createNode aiAOVFilter -s -n "defaultArnoldFilter";
	rename -uid "682C350C-43F2-8520-B591-E49B93F345BE";
	setAttr ".ai_translator" -type "string" "gaussian";
createNode aiAOVDriver -s -n "defaultArnoldDriver";
	rename -uid "5B34A13F-4BE4-C05A-637D-9C85B2412DDE";
	setAttr ".ai_translator" -type "string" "exr";
createNode aiAOVDriver -s -n "defaultArnoldDisplayDriver";
	rename -uid "86BE2E11-498E-8EBD-0CC5-C3AF6607AC69";
	setAttr ".ai_translator" -type "string" "maya";
	setAttr ".output_mode" 0;
createNode reference -n "rigRN";
	rename -uid "3FC61314-4CE8-E2D4-73D5-C1BBE30925E5";
	setAttr ".ed" -type "dataReferenceEdits" 
		"rigRN"
		"rigRN" 0
		"rigRN" 5
		2 "|rig:GRP_Character_Rig" "visibility" " 0"
		2 "|rig:GRP_Character_Rig|rig:GRP_CTL_Root|rig:OFF_CTL_Root|rig:CTL_Root|rig:OFF_CTL_Main|rig:CTL_Main|rig:GRP_Spine_C|rig:OFF_CTL_COG_C|rig:CTL_COG_C|rig:OFF_CTL_FK_Spine_01_C|rig:CTL_FK_Spine_01_C|rig:OFF_CTL_FK_Spine_02_C|rig:CTL_FK_Spine_02_C|rig:OFF_CTL_Chest_C|rig:OFF_Global_CTL_Chest_C|rig:CTL_Chest_C|rig:OFF_CTL_Clavicle_L|rig:OFF_Extra_CTL_Clavicle_L|rig:CTL_Clavicle_L|rig:GRP_Arm_L|rig:OFF_CTL_SWITCH_Arm_L|rig:CTL_SWITCH_Arm_L" 
		"FK_IK" " -k 1 0"
		2 "|rig:GRP_Character_Rig|rig:GRP_CTL_Root|rig:OFF_CTL_Root|rig:CTL_Root|rig:OFF_CTL_Main|rig:CTL_Main|rig:GRP_Spine_C|rig:OFF_CTL_COG_C|rig:CTL_COG_C|rig:OFF_CTL_FK_Spine_01_C|rig:CTL_FK_Spine_01_C|rig:OFF_CTL_FK_Spine_02_C|rig:CTL_FK_Spine_02_C|rig:OFF_CTL_Chest_C|rig:OFF_Global_CTL_Chest_C|rig:CTL_Chest_C|rig:OFF_CTL_Clavicle_L|rig:OFF_Extra_CTL_Clavicle_L|rig:CTL_Clavicle_L|rig:GRP_Arm_L|rig:OFF_CTL_FK_Arm_L|rig:OFF_Global_CTL_FK_Arm_L|rig:OFF_Extra_CTL_FK_Arm_L|rig:CTL_FK_Arm_L" 
		"scale" " -type \"double3\" 0.99999999999999989 1 1"
		2 "|rig:GRP_Character_Rig|rig:GRP_CTL_Root|rig:OFF_CTL_Root|rig:CTL_Root|rig:OFF_CTL_Main|rig:CTL_Main|rig:GRP_Spine_C|rig:OFF_CTL_COG_C|rig:CTL_COG_C|rig:OFF_CTL_FK_Spine_01_C|rig:CTL_FK_Spine_01_C|rig:OFF_CTL_FK_Spine_02_C|rig:CTL_FK_Spine_02_C|rig:OFF_CTL_Chest_C|rig:OFF_Global_CTL_Chest_C|rig:CTL_Chest_C|rig:OFF_CTL_Clavicle_L|rig:OFF_Extra_CTL_Clavicle_L|rig:CTL_Clavicle_L|rig:GRP_Arm_L|rig:OFF_CTL_FK_Arm_L|rig:OFF_Global_CTL_FK_Arm_L|rig:OFF_Extra_CTL_FK_Arm_L|rig:CTL_FK_Arm_L|rig:OFF_CTL_FK_ForeArm_L|rig:CTL_FK_ForeArm_L" 
		"rotate" " -type \"double3\" 0 0 0"
		2 "|rig:GRP_Character_Rig|rig:GRP_CTL_Root|rig:OFF_CTL_Root|rig:CTL_Root|rig:OFF_CTL_Main|rig:CTL_Main|rig:GRP_Spine_C|rig:OFF_CTL_COG_C|rig:CTL_COG_C|rig:OFF_CTL_FK_Spine_01_C|rig:CTL_FK_Spine_01_C|rig:OFF_CTL_FK_Spine_02_C|rig:CTL_FK_Spine_02_C|rig:OFF_CTL_Chest_C|rig:OFF_Global_CTL_Chest_C|rig:CTL_Chest_C|rig:OFF_CTL_Clavicle_L|rig:OFF_Extra_CTL_Clavicle_L|rig:CTL_Clavicle_L|rig:GRP_Arm_L|rig:GRP_CTL_Hand_L|rig:GRP_Fingers_L|rig:OFF_CTL_FK_Index_Meta_L|rig:OFF_00_CTL_FK_Index_Meta_L|rig:OFF_01_CTL_FK_Index_Meta_L|rig:CTL_FK_Index_Meta_L" 
		"rotate" " -type \"double3\" 0 0 0";
	setAttr ".ptag" -type "string" "";
lockNode -l 1 ;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "A86E8413-4423-C8D9-378D-6196EE83BF0D";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n"
		+ "            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n"
		+ "            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n"
		+ "            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n"
		+ "            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n"
		+ "            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 1\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n"
		+ "            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 0\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n"
		+ "            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 501\n            -height 671\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n"
		+ "            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -autoExpandAllAnimatedShapes 1\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n"
		+ "            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"print \\\"\\\"\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -autoExpandAllAnimatedShapes 1\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n"
		+ "            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n"
		+ "            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n"
		+ "                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -autoExpandAllAnimatedShapes 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n"
		+ "                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n"
		+ "                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -limitToSelectedCurves 0\n                -constrainDrag 0\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n"
		+ "                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -autoExpandAllAnimatedShapes 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n"
		+ "                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n"
		+ "                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n"
		+ "                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n"
		+ "                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n"
		+ "                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n"
		+ "                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n"
		+ "\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 1\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 0\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 501\\n    -height 671\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 1\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 0\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 501\\n    -height 671\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "6C2E5F22-47E4-D607-C7E8-89B264681CA2";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
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
	setAttr -k on ".hwi";
	setAttr -av ".ta";
	setAttr -av ".tq";
	setAttr ".aoon" yes;
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -k on ".hff";
	setAttr -av -k on ".hfd";
	setAttr -av -k on ".hfs";
	setAttr -av -k on ".hfe";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av -k on ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".blen";
	setAttr -k on ".blat";
	setAttr ".msaa" yes;
	setAttr ".dli" 1;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 14 ".st";
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
	setAttr -s 16 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3975 ".u";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
	setAttr -s 3 ".r";
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.40000000596046448;
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
	setAttr -s 25 ".dsm";
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
	setAttr -av -k on ".an";
	setAttr -cb on ".ar";
	setAttr -av -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -cb on ".me";
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
	setAttr -k on ".sosl";
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
	setAttr -av -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -av -k on ".mbso";
	setAttr -av -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -av -k on ".pfb";
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -cb on ".prm";
	setAttr -cb on ".pom";
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
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
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
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :ikSystem;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".gsn";
	setAttr -k on ".gsv";
	setAttr -s 2 ".sol";
connectAttr "BIND_Chest_C.s" "BIND_Clavicle_L.is";
connectAttr "BIND_Clavicle_L.s" "BIND_Arm_L.is";
connectAttr "BIND_Arm_L.s" "BIND_ForeArm_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_Hand_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Front_Hand_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Back_Hand_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Left_Hand_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Right_Hand_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Index_Meta_L.is";
connectAttr "BIND_Index_Meta_L.s" "BIND_Index_00_L.is";
connectAttr "BIND_Index_00_L.s" "BIND_Index_01_L.is";
connectAttr "BIND_Index_01_L.s" "BIND_Index_02_L.is";
connectAttr "BIND_Index_02_L.s" "BIND_Index_03_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Middle_Meta_L.is";
connectAttr "BIND_Middle_Meta_L.s" "BIND_Middle_00_L.is";
connectAttr "BIND_Middle_00_L.s" "BIND_Middle_01_L.is";
connectAttr "BIND_Middle_01_L.s" "BIND_Middle_02_L.is";
connectAttr "BIND_Middle_02_L.s" "BIND_Middle_03_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Ring_Meta_L.is";
connectAttr "BIND_Ring_Meta_L.s" "BIND_Ring_00_L.is";
connectAttr "BIND_Ring_00_L.s" "BIND_Ring_01_L.is";
connectAttr "BIND_Ring_01_L.s" "BIND_Ring_02_L.is";
connectAttr "BIND_Ring_02_L.s" "BIND_Ring_03_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Pinky_Meta_L.is";
connectAttr "BIND_Pinky_Meta_L.s" "BIND_Pinky_00_L.is";
connectAttr "BIND_Pinky_00_L.s" "BIND_Pinky_01_L.is";
connectAttr "BIND_Pinky_01_L.s" "BIND_Pinky_02_L.is";
connectAttr "BIND_Pinky_02_L.s" "BIND_Pinky_03_L.is";
connectAttr "BIND_Hand_L.s" "BIND_Thumb_00_L.is";
connectAttr "BIND_Thumb_00_L.s" "BIND_Thumb_01_L.is";
connectAttr "BIND_Thumb_01_L.s" "BIND_Thumb_02_L.is";
connectAttr "BIND_Thumb_02_L.s" "BIND_Thumb_03_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_00_L.is";
connectAttr "BIND_ForeArm_00_L.s" "BIND_Front_ForeArm_00_L.is";
connectAttr "BIND_ForeArm_00_L.s" "BIND_Back_ForeArm_00_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_01_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_02_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_03_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_04_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_05_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_06_L.is";
connectAttr "BIND_ForeArm_L.s" "BIND_ForeArm_07_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_00_L.is";
connectAttr "BIND_Arm_00_L.s" "BIND_Left_Arm_00_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_01_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_02_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_03_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_04_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_05_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_06_L.is";
connectAttr "BIND_Arm_L.s" "BIND_Arm_07_L.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":defaultArnoldDisplayDriver.msg" ":defaultArnoldRenderOptions.drivers"
		 -na;
connectAttr ":defaultArnoldFilter.msg" ":defaultArnoldRenderOptions.filt";
connectAttr ":defaultArnoldDriver.msg" ":defaultArnoldRenderOptions.drvr";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of limbA_ver000_take000.ma
