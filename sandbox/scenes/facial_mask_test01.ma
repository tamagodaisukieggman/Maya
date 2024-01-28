//Maya ASCII 2024 scene
//Name: facial_mask_test01.ma
//Last modified: Mon, Jan 29, 2024 12:57:56 AM
//Codeset: 932
requires maya "2024";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2024";
fileInfo "version" "2024";
fileInfo "cutIdentifier" "202310181224-69282f2959";
fileInfo "osv" "Windows 11 Home v2009 (Build: 22621)";
fileInfo "UUID" "E36F4556-48E7-99B7-DE32-C68DF3D222DC";
createNode transform -n "eyeLid_grp";
	rename -uid "45A30EB8-4707-4BB6-4E8D-66883E9BFFC6";
	setAttr ".v" no;
createNode joint -n "uplid_L_001_jnt" -p "eyeLid_grp";
	rename -uid "03EF36D1-43A2-AA56-A129-9CACB9E606F5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.98892325162887573 10.892970085144043 3.9900758266448975 ;
	setAttr ".r" -type "double3" -0.00082784051826733491 0.0075519672286592406 0.00030293277407565997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.80680557084188798 10.924906089768044 3.9604287592674603 1;
	setAttr ".radi" 0.59999999999999987;
createNode joint -n "uplid_L_002_jnt" -p "eyeLid_grp";
	rename -uid "372F4649-43E0-3C00-5265-FD8FD6C19A52";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.329659104347229 10.96547794342041 3.9686803817749023 ;
	setAttr ".r" -type "double3" -0.00082784051826733491 0.0075519672286592406 0.00030293277407565997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.1002638157529689 10.974170243624219 4.0514820030696388 1;
	setAttr ".radi" 0.59999999999999987;
createNode joint -n "uplid_L_003_jnt" -p "eyeLid_grp";
	rename -uid "BB34DC2E-46AA-C45B-AB6D-1E950C1B9CD7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5702060461044312 10.961289405822754 3.8375277519226074 ;
	setAttr ".r" -type "double3" -0.00082784051826733491 0.0075519672286592406 0.00030293277407565997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.4352106173401626 10.883620046861394 3.9888796392877066 1;
	setAttr ".radi" 0.59999999999999987;
createNode joint -n "lowlid_L_001_jnt" -p "eyeLid_grp";
	rename -uid "D6455BC0-4CC7-D471-90E4-FFBA6A083B45";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0641301870346069 10.654171943664551 3.9671969413757324 ;
	setAttr ".r" -type "double3" -0.00082784051826733491 0.0075519672286592406 0.00030293277407565997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.84690120399309032 10.674279130679588 3.9449639165258601 1;
	setAttr ".radi" 0.5;
createNode joint -n "lowlid_L_002_jnt" -p "eyeLid_grp";
	rename -uid "BDFCCB10-4DCD-31FE-0DDA-FD934750DA3A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.3709912300109863 10.656102180480957 3.9184081554412842 ;
	setAttr ".r" -type "double3" -0.00082784051826733491 0.0075519672286592406 0.00030293277407565997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.1243990361243963 10.642323016317109 3.988941940938703 1;
	setAttr ".radi" 0.5;
createNode joint -n "lowlid_L_003_jnt" -p "eyeLid_grp";
	rename -uid "1A091574-4718-041B-CA01-EE837EC33A14";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6253969669342041 10.692380905151367 3.7676155567169189 ;
	setAttr ".r" -type "double3" -0.00082784051826733491 0.0075519672286592406 0.00030293277407565997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.4527935550425826 10.708661493132892 3.8604995774019302 1;
	setAttr ".radi" 0.5;
createNode transform -n "lip_grp";
	rename -uid "C55FCD45-498D-54B1-80F6-10987C977477";
	setAttr ".v" no;
createNode joint -n "upLipIn_R_002_jnt" -p "lip_grp";
	rename -uid "DB3A693E-43D7-3259-0120-EA97FFE9CCA2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.64786700000000019 8.1301228918957058 3.9954728697764397 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.63072238073356268 8.1135028462603582 4.1731391557800457 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_L_001_jnt" -p "lip_grp";
	rename -uid "769BFC53-4CD1-7F04-172A-37826D952F51";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.31326141942486602 8.0633418200471692 4.181688637913167 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.25505693686061659 8.0609700013362513 4.2733855747843572 1;
	setAttr ".radi" 2;
createNode joint -n "upLipIn_R_001_jnt" -p "lip_grp";
	rename -uid "876CE3AC-4692-91EE-9D24-FA8923D6044C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.30110000001296994 8.161098815079983 4.2165020418682539 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.34250219018285905 8.1293635311003971 4.3330695892933209 1;
	setAttr ".radi" 2;
createNode joint -n "upLip_L_002_jnt" -p "lip_grp";
	rename -uid "4E42E479-4D80-DB5B-F446-4BA2D52127AE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.71079620825590761 8.1679370447533195 4.056150883207251 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.63761972172807235 8.1582268318985989 4.2460503534388492 1;
	setAttr ".radi" 2;
createNode joint -n "lowLip_R_002_jnt" -p "lip_grp";
	rename -uid "F92D9FDE-42BB-6623-8321-68B3DEAAF89E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.71564968256741734 7.9897789269717805 3.9893967510287429 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.70108342217426978 7.9389883002423121 4.1630248313319473 1;
	setAttr ".radi" 2;
createNode joint -n "upLipIn_C_001_jnt" -p "lip_grp";
	rename -uid "EB9B4CAE-413A-5456-93CB-16BEFA06B8F5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.6842682468088218e-13 8.1674026750818776 4.2676919416120578 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.05816780574738975 8.1292099202335599 4.3723991513539664 1;
	setAttr ".radi" 2;
createNode joint -n "upLip_C_001_jnt" -p "lip_grp";
	rename -uid "F16F109C-4785-6E50-74A1-FCA6D73DD3FA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.0010749830582581271 8.2344608170866156 4.4072820963618575 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.058328795006488909 8.2057095964240006 4.5392144434160855 1;
	setAttr ".radi" 2;
createNode joint -n "upLip_R_001_jnt" -p "lip_grp";
	rename -uid "8FB975BA-4054-1774-EE6C-37BEFB4599BA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.38369615770296234 8.2473474190908789 4.2992878945819673 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.42208083953892084 8.2242210099545954 4.454867975823392 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_R_001_jnt" -p "lip_grp";
	rename -uid "60B25D5F-4D0D-5433-E57D-A388F495AAF6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.31326100025558412 8.063341819672674 4.1816881613708148 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.35008860501108874 8.0549841156068993 4.2731740881143736 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_R_003_jnt" -p "lip_grp";
	rename -uid "9D0DDECF-492B-7223-A620-DCBD3A3C61D8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.78575614900512725 8.0231395537776642 3.7208167110570107 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999863498 -1.6505110629665324e-06 -7.6563365475557565e-08 0
		 1.6513405714828629e-06 0.99992155464531751 0.012525356400695029 0 5.5884120128251341e-08 -0.012525356400804365 0.99992155464667809 0
		 -0.69151399422017912 8.0050147820985451 3.8707858199629843 1;
	setAttr ".radi" 2;
createNode joint -n "upLipIn_L_001_jnt" -p "lip_grp";
	rename -uid "051AA4A1-405A-7D64-E0E0-0689394934D0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.30110049247741616 8.1610997688925977 4.2165025190046359 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.24774696023374437 8.1320746173807006 4.3324419366540639 1;
	setAttr ".radi" 2;
createNode joint -n "upLipIn_L_002_jnt" -p "lip_grp";
	rename -uid "47DA43C7-4153-8F11-F5EE-75AC24930859";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.64786744129138663 8.1301228919096342 3.995472869760083 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.56583094306848802 8.1267665292340219 4.1722797620973706 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_L_002_jnt" -p "lip_grp";
	rename -uid "802F1EFA-4B7D-9069-FA52-62B7B3A9B0E0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.67235565168194689 8.0581417308885062 3.9490236853951681 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.57364095716747021 8.0619361069233619 4.1246007500214485 1;
	setAttr ".radi" 2;
createNode joint -n "lowLip_C_001_jnt" -p "lip_grp";
	rename -uid "99826257-4161-38ED-95DA-B9A1EFE9D99C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00077458090180501399 7.9105960588782667 4.2828073559271838 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.058566428999132586 7.851637756330943 4.3405108486626798 1;
	setAttr ".radi" 2;
createNode joint -n "upLip_L_001_jnt" -p "lip_grp";
	rename -uid "ABB7174C-4086-19F3-7020-618EED0A842B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.38368940393259743 8.24734486346944 4.29929123753488 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.32968598004266042 8.2259989762999481 4.453813287574639 1;
	setAttr ".radi" 2;
createNode joint -n "upLip_R_002_jnt" -p "lip_grp";
	rename -uid "9052CF1B-4432-EC0F-1BF3-5EBD4A5870F2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.71079095954459937 8.1679287198622355 4.0561383479618476 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.70216951594125132 8.1458058501349981 4.2469043169179352 1;
	setAttr ".radi" 2;
createNode joint -n "lowLip_L_002_jnt" -p "lip_grp";
	rename -uid "A39518BD-4940-781E-4258-1FB97F3433AB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.7156458677482519 7.989779584240094 3.9894035641463765 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.62393161048632162 7.9836842956574818 4.164859163151541 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_R_002_jnt" -p "lip_grp";
	rename -uid "161226C3-41DD-52F0-F3F6-E092F19C41CD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.67235600000000095 8.058141730848293 3.9490236853587164 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.64131238709492977 8.0385750812548924 4.1247852258606432 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_C_001_jnt" -p "lip_grp";
	rename -uid "0551E040-417E-DC32-2753-35B4CADDD092";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 8.4129017771314446e-12 8.0727015249604381 4.2523563817670844 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.057020475936618562 8.0739548240155976 4.2924521782712084 1;
	setAttr ".radi" 2;
createNode joint -n "lowLip_R_001_jnt" -p "lip_grp";
	rename -uid "5A69A3EB-4CAB-B854-27CF-F1BA874073E0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.41703396867426429 7.9169768882879534 4.2188904135334493 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.44901339209936025 7.850020661740464 4.3473501593432635 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipIn_L_003_jnt" -p "lip_grp";
	rename -uid "1342C622-4408-4816-EEF6-36BCF7A965E0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.78568140846864065 8.0229288847133944 3.7208563473774912 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999999863498 -1.6505110629665324e-06 -7.6563365475557565e-08 0
		 1.6513405714828629e-06 0.99992155464531751 0.012525356400695029 0 5.5884120128251341e-08 -0.012525356400804365 0.99992155464667809 0
		 0.69153224825820803 8.0050063987612869 3.8707875398585134 1;
	setAttr ".radi" 2;
createNode joint -n "lowLip_L_001_jnt" -p "lip_grp";
	rename -uid "B35F019D-44F3-1D3E-71BC-CA9F37886D7B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.41703396040218688 7.9169790420903734 4.2188916757353692 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.34274297582778651 7.8998521869012768 4.3474099290133523 1;
	setAttr ".radi" 2;
createNode joint -n "upLipIn_L_003_jnt" -p "lip_grp";
	rename -uid "6E3C3209-4D42-6B31-3105-FB968C8F448D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.84223817357473807 8.1611655502779499 3.693069440335726 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.73210296034970523 8.136051838972973 3.8749756052349942 1;
	setAttr ".radi" 2;
createNode joint -n "upLipIn_R_003_jnt" -p "lip_grp";
	rename -uid "1D1B23F6-4B1D-FB8C-296D-709844C8A97A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.84226150488043916 8.1613286504901943 3.6927776155540126 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.73208024848977926 8.1360367244831622 3.8749609379393872 1;
	setAttr ".radi" 2;
createNode transform -n "bs_mesh_grp";
	rename -uid "598377CD-46BD-3D7B-D063-E68F7B9C7B5B";
createNode transform -n "base_bs_mesh_grp" -p "bs_mesh_grp";
	rename -uid "7207A75A-44B7-7D70-F0C3-34975CA93650";
createNode transform -n "brow_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "48BDD17A-47A5-FF9E-A42D-EEB4B2120184";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 11.504711627960205 3.883679986000061 ;
	setAttr ".sp" -type "double3" 0 11.504711627960205 3.883679986000061 ;
createNode mesh -n "brow_bs_meshShape" -p "brow_bs_mesh";
	rename -uid "9E5028D2-4F0E-50BE-F688-B79B1F5D7619";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.49999997019767761 0.37382793426513672 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 18 ".pt";
	setAttr ".pt[0]" -type "float3" -4.1909516e-08 8.9406967e-08 9.3132257e-09 ;
	setAttr ".pt[1]" -type "float3" -4.1909516e-08 8.9406967e-08 9.3132257e-09 ;
	setAttr ".pt[2]" -type "float3" -2.2351742e-08 4.4703484e-08 3.7252903e-08 ;
	setAttr ".pt[3]" -type "float3" -2.2351742e-08 4.4703484e-08 3.7252903e-08 ;
	setAttr ".pt[4]" -type "float3" -2.2351742e-08 4.4703484e-08 3.7252903e-08 ;
	setAttr ".pt[5]" -type "float3" -2.2351742e-08 4.4703484e-08 3.7252903e-08 ;
	setAttr ".pt[6]" -type "float3" 2.6077032e-08 0 -4.1909516e-09 ;
	setAttr ".pt[7]" -type "float3" 2.6077032e-08 0 -4.1909516e-09 ;
	setAttr ".pt[8]" -type "float3" 2.6077032e-08 0 -4.1909516e-09 ;
	setAttr ".pt[9]" -type "float3" 2.6077032e-08 0 -4.1909516e-09 ;
	setAttr ".pt[14]" -type "float3" -4.1909516e-08 8.9406967e-08 9.3132257e-09 ;
	setAttr ".pt[15]" -type "float3" -4.1909516e-08 8.9406967e-08 9.3132257e-09 ;
	setAttr ".pt[20]" -type "float3" -3.7252903e-09 -2.9802322e-08 9.3132257e-10 ;
	setAttr ".pt[21]" -type "float3" -3.7252903e-09 -2.9802322e-08 9.3132257e-10 ;
	setAttr ".pt[22]" -type "float3" -3.7252903e-09 -2.9802322e-08 9.3132257e-10 ;
	setAttr ".pt[23]" -type "float3" -3.7252903e-09 -2.9802322e-08 9.3132257e-10 ;
	setAttr ".pt[30]" -type "float3" 6.9398642e-18 0 0 ;
	setAttr ".pt[31]" -type "float3" 6.9398642e-18 0 0 ;
	setAttr ".vcs" 2;
createNode mesh -n "brow_bs_meshShapeOrig" -p "brow_bs_mesh";
	rename -uid "C93D8CC2-4D01-BA4C-8214-10BE8D4CC1C2";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 28 ".uvst[0].uvsp[0:27]" -type "float2" 1 0 1 1 0 0 1 0 1
		 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1
		 0 1 1 0 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 28 ".vt[0:27]"  0.19371808 11.21143436 4.58365107 0.19371808 11.59783459 4.58365107
		 0.23106143 11.10812378 4.56689167 0.61746156 11.10812378 4.56689167 0.23106137 11.494524 4.56689167
		 0.6174615 11.494524 4.56689167 1.12642717 11.39643383 4.36986685 1.51282716 11.39643383 4.36986685
		 1.12642717 11.78283405 4.36986685 1.51282716 11.78283405 4.36986685 2.1004374 11.51489925 3.18370891
		 2.48683763 11.51489925 3.18370891 2.1004374 11.90129948 3.18370891 2.48683763 11.90129948 3.18370891
		 -0.19371808 11.21143436 4.58365107 -0.19371808 11.59783459 4.58365107 -0.23106143 11.10812378 4.56689167
		 -0.61746156 11.10812378 4.56689167 -0.23106137 11.494524 4.56689167 -0.6174615 11.494524 4.56689167
		 -1.12642717 11.39643383 4.36986685 -1.51282716 11.39643383 4.36986685 -1.12642717 11.78283405 4.36986685
		 -1.51282716 11.78283405 4.36986685 -2.1004374 11.51489925 3.18370891 -2.48683763 11.51489925 3.18370891
		 -2.1004374 11.90129948 3.18370891 -2.48683763 11.90129948 3.18370891;
	setAttr -s 28 ".ed[0:27]"  0 1 0 2 3 0 2 4 0 3 5 0 4 5 0 6 7 0 6 8 0
		 7 9 0 8 9 0 10 11 0 10 12 0 11 13 0 12 13 0 14 0 0 16 17 0 17 19 0 18 19 0 16 18 0
		 20 21 0 21 23 0 22 23 0 20 22 0 24 25 0 25 27 0 26 27 0 24 26 0 14 15 0 1 15 0;
	setAttr -s 7 -ch 28 ".fc[0:6]" -type "polyFaces" 
		f 4 1 3 -5 -3
		mu 0 4 2 3 4 5
		f 4 5 7 -9 -7
		mu 0 4 6 7 8 9
		f 4 9 11 -13 -11
		mu 0 4 10 11 12 13
		f 4 17 16 -16 -15
		mu 0 4 14 17 16 15
		f 4 21 20 -20 -19
		mu 0 4 18 21 20 19
		f 4 25 24 -24 -23
		mu 0 4 22 25 24 23
		f 4 27 -27 13 0
		mu 0 4 1 27 26 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".vcs" 2;
createNode transform -n "lowlid_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "DAD32AB4-4E60-51C8-3422-418A5C9B6B18";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 10.477306365966797 3.8336213827133179 ;
	setAttr ".sp" -type "double3" 0 10.477306365966797 3.8336213827133179 ;
createNode mesh -n "lowlid_bs_meshShape" -p "lowlid_bs_mesh";
	rename -uid "1A5170E3-4FCF-F671-9C57-3CA583221EB3";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "lowlid_bs_meshShapeOrig" -p "lowlid_bs_mesh";
	rename -uid "7D4A9E49-4ED9-9804-3831-E48923F1055E";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 5 ".gtag";
	setAttr ".gtag[0].gtagnm" -type "string" "back";
	setAttr ".gtag[0].gtagcmp" -type "componentList" 6 "e[3]" "e[7]" "e[11]" "e[14]" "e[18]" "e[22]";
	setAttr ".gtag[1].gtagnm" -type "string" "front";
	setAttr ".gtag[1].gtagcmp" -type "componentList" 6 "e[0]" "e[4]" "e[8]" "e[12]" "e[16]" "e[20]";
	setAttr ".gtag[2].gtagnm" -type "string" "left";
	setAttr ".gtag[2].gtagcmp" -type "componentList" 6 "e[1]" "e[5]" "e[9]" "e[15]" "e[19]" "e[23]";
	setAttr ".gtag[3].gtagnm" -type "string" "right";
	setAttr ".gtag[3].gtagcmp" -type "componentList" 6 "e[2]" "e[6]" "e[10]" "e[13]" "e[17]" "e[21]";
	setAttr ".gtag[4].gtagnm" -type "string" "rim";
	setAttr ".gtag[4].gtagcmp" -type "componentList" 1 "e[0:23]";
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 24 ".uvst[0].uvsp[0:23]" -type "float2" 0 0 1 0 0 1 1 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 24 ".vt[0:23]"  0.89198852 10.25975895 3.95996666 1.27838862 10.25975895 3.95996666
		 0.89198852 10.64615917 3.95996666 1.27838862 10.64615917 3.95996666 1.2436372 10.24388981 3.86620617
		 1.63003731 10.24388981 3.86620617 1.2436372 10.63029003 3.86620617 1.63003731 10.63029003 3.86620617
		 1.52633679 10.3243227 3.70727611 1.91273701 10.3243227 3.70727611 1.52633679 10.71072292 3.70727611
		 1.91273701 10.71072292 3.70727611 -0.89198852 10.25975895 3.95996666 -1.27838862 10.25975895 3.95996666
		 -0.89198852 10.64615917 3.95996666 -1.27838862 10.64615917 3.95996666 -1.2436372 10.24388981 3.86620617
		 -1.63003731 10.24388981 3.86620617 -1.2436372 10.63029003 3.86620617 -1.63003731 10.63029003 3.86620617
		 -1.52633679 10.3243227 3.70727611 -1.91273701 10.3243227 3.70727611 -1.52633679 10.71072292 3.70727611
		 -1.91273701 10.71072292 3.70727611;
	setAttr -s 24 ".ed[0:23]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 13 15 0 14 15 0 12 14 0 16 17 0 17 19 0
		 18 19 0 16 18 0 20 21 0 21 23 0 22 23 0 20 22 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 3 2
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 15 14 -14 -13
		mu 0 4 12 15 14 13
		f 4 19 18 -18 -17
		mu 0 4 16 19 18 17
		f 4 23 22 -22 -21
		mu 0 4 20 23 22 21;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "eyeFrame_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "3EAB50C1-4794-9652-D533-49A9A0FB31D9";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 10.594685077667236 3.0862222909927368 ;
	setAttr ".sp" -type "double3" 0 10.594685077667236 3.0862222909927368 ;
createNode mesh -n "eyeFrame_bs_meshShape" -p "eyeFrame_bs_mesh";
	rename -uid "46D8CCC0-48F3-156A-9E05-89B7E0D35A92";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "eyeFrame_bs_meshShapeOrig" -p "eyeFrame_bs_mesh";
	rename -uid "245B6616-4129-8BF2-55C3-F49AED6A41ED";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 5 ".gtag";
	setAttr ".gtag[0].gtagnm" -type "string" "back";
	setAttr ".gtag[0].gtagcmp" -type "componentList" 12 "e[3]" "e[7]" "e[11]" "e[15]" "e[19]" "e[23]" "e[26]" "e[30]" "e[34]" "e[38]" "e[42]" "e[46]";
	setAttr ".gtag[1].gtagnm" -type "string" "front";
	setAttr ".gtag[1].gtagcmp" -type "componentList" 12 "e[0]" "e[4]" "e[8]" "e[12]" "e[16]" "e[20]" "e[24]" "e[28]" "e[32]" "e[36]" "e[40]" "e[44]";
	setAttr ".gtag[2].gtagnm" -type "string" "left";
	setAttr ".gtag[2].gtagcmp" -type "componentList" 12 "e[1]" "e[5]" "e[9]" "e[13]" "e[17]" "e[21]" "e[27]" "e[31]" "e[35]" "e[39]" "e[43]" "e[47]";
	setAttr ".gtag[3].gtagnm" -type "string" "right";
	setAttr ".gtag[3].gtagcmp" -type "componentList" 12 "e[2]" "e[6]" "e[10]" "e[14]" "e[18]" "e[22]" "e[25]" "e[29]" "e[33]" "e[37]" "e[41]" "e[45]";
	setAttr ".gtag[4].gtagnm" -type "string" "rim";
	setAttr ".gtag[4].gtagcmp" -type "componentList" 1 "e[0:47]";
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 48 ".uvst[0].uvsp[0:47]" -type "float2" 0 0 1 0 0 1 1 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0
		 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1
		 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 48 ".vt[0:47]"  2.29549932 11.18450069 2.081173658 2.68189955 11.18450069 2.081173658
		 2.29549932 11.57090092 2.081173658 2.68189955 11.57090092 2.081173658 0.2922461 10.28654289 4.091270924
		 0.67864621 10.28654289 4.091270924 0.2922461 10.67294312 4.091270924 0.67864621 10.67294312 4.091270924
		 2.13614917 10.11901474 2.87536716 2.52254915 10.11901474 2.87536716 2.13614917 10.50541496 2.87536716
		 2.52254915 10.50541496 2.87536716 0.95517552 9.61846924 3.98405671 1.34157562 9.61846924 3.98405671
		 0.95517552 10.0048694611 3.98405671 1.34157562 10.0048694611 3.98405671 1.82429874 9.72488022 3.47359967
		 2.21069908 9.72488022 3.47359967 1.82429874 10.11128044 3.47359967 2.21069908 10.11128044 3.47359967
		 2.18157744 10.75324821 2.56306934 2.56797743 10.75324821 2.56306934 2.18157744 11.13964844 2.56306934
		 2.56797743 11.13964844 2.56306934 -2.29549932 11.18450069 2.081173658 -2.68189955 11.18450069 2.081173658
		 -2.29549932 11.57090092 2.081173658 -2.68189955 11.57090092 2.081173658 -0.2922461 10.28654289 4.091270924
		 -0.67864621 10.28654289 4.091270924 -0.2922461 10.67294312 4.091270924 -0.67864621 10.67294312 4.091270924
		 -2.13614917 10.11901474 2.87536716 -2.52254915 10.11901474 2.87536716 -2.13614917 10.50541496 2.87536716
		 -2.52254915 10.50541496 2.87536716 -0.95517552 9.61846924 3.98405671 -1.34157562 9.61846924 3.98405671
		 -0.95517552 10.0048694611 3.98405671 -1.34157562 10.0048694611 3.98405671 -1.82429874 9.72488022 3.47359967
		 -2.21069908 9.72488022 3.47359967 -1.82429874 10.11128044 3.47359967 -2.21069908 10.11128044 3.47359967
		 -2.18157744 10.75324821 2.56306934 -2.56797743 10.75324821 2.56306934 -2.18157744 11.13964844 2.56306934
		 -2.56797743 11.13964844 2.56306934;
	setAttr -s 48 ".ed[0:47]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 12 14 0 13 15 0 14 15 0 16 17 0 16 18 0
		 17 19 0 18 19 0 20 21 0 20 22 0 21 23 0 22 23 0 24 25 0 25 27 0 26 27 0 24 26 0 28 29 0
		 29 31 0 30 31 0 28 30 0 32 33 0 33 35 0 34 35 0 32 34 0 36 37 0 37 39 0 38 39 0 36 38 0
		 40 41 0 41 43 0 42 43 0 40 42 0 44 45 0 45 47 0 46 47 0 44 46 0;
	setAttr -s 12 -ch 48 ".fc[0:11]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 3 2
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 12 14 -16 -14
		mu 0 4 12 13 14 15
		f 4 16 18 -20 -18
		mu 0 4 16 17 18 19
		f 4 20 22 -24 -22
		mu 0 4 20 21 22 23
		f 4 27 26 -26 -25
		mu 0 4 24 27 26 25
		f 4 31 30 -30 -29
		mu 0 4 28 31 30 29
		f 4 35 34 -34 -33
		mu 0 4 32 35 34 33
		f 4 39 38 -38 -37
		mu 0 4 36 39 38 37
		f 4 43 42 -42 -41
		mu 0 4 40 43 42 41
		f 4 47 46 -46 -45
		mu 0 4 44 47 46 45;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "zyg_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "F5F079FB-40E6-FA01-9487-CC88361D55ED";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 9.4809842109680176 3.0008571147918701 ;
	setAttr ".sp" -type "double3" 0 9.4809842109680176 3.0008571147918701 ;
createNode mesh -n "zyg_bs_meshShape" -p "zyg_bs_mesh";
	rename -uid "B7016A97-45E5-F5F9-9346-729782FBF003";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "zyg_bs_meshShapeOrig" -p "zyg_bs_mesh";
	rename -uid "90A54E2F-4E29-4E12-E8DF-96B0D10883C3";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 24 ".uvst[0].uvsp[0:23]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 24 ".vt[0:23]"  1.32150531 8.93315125 3.7214303 1.70790553 8.93315125 3.7214303
		 1.32150531 9.31955147 3.7214303 1.70790553 9.31955147 3.7214303 1.82488203 9.16024971 3.15465593
		 2.21128225 9.16024971 3.15465593 1.82488203 9.54664993 3.15465593 2.21128225 9.54664993 3.15465593
		 2.27569556 9.64241695 2.28028393 2.66209579 9.64241695 2.28028393 2.27569556 10.028817177 2.28028393
		 2.66209579 10.028817177 2.28028393 -1.32150531 8.93315125 3.7214303 -1.70790553 8.93315125 3.7214303
		 -1.32150531 9.31955147 3.7214303 -1.70790553 9.31955147 3.7214303 -1.82488203 9.16024971 3.15465593
		 -2.21128225 9.16024971 3.15465593 -1.82488203 9.54664993 3.15465593 -2.21128225 9.54664993 3.15465593
		 -2.27569556 9.64241695 2.28028393 -2.66209579 9.64241695 2.28028393 -2.27569556 10.028817177 2.28028393
		 -2.66209579 10.028817177 2.28028393;
	setAttr -s 24 ".ed[0:23]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 13 15 0 14 15 0 12 14 0 16 17 0 17 19 0
		 18 19 0 16 18 0 20 21 0 21 23 0 22 23 0 20 22 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 15 14 -14 -13
		mu 0 4 12 15 14 13
		f 4 19 18 -18 -17
		mu 0 4 16 19 18 17
		f 4 23 22 -22 -21
		mu 0 4 20 23 22 21;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "cheek_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "7E82CEEB-49B7-8CCF-DBE7-02B07C8466ED";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 8.558504581451416 1.9668475389480591 ;
	setAttr ".sp" -type "double3" 0 8.558504581451416 1.9668475389480591 ;
createNode mesh -n "cheek_bs_meshShape" -p "cheek_bs_mesh";
	rename -uid "1C4305AF-4664-3415-3B1F-B0B93E2B6052";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "cheek_bs_meshShapeOrig" -p "cheek_bs_mesh";
	rename -uid "862CBE52-4AE5-8833-8186-54853737E68C";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 24 ".uvst[0].uvsp[0:23]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 24 ".vt[0:23]"  1.58897114 7.97185516 2.77455592 1.97537136 7.97185516 2.77455592
		 1.58897114 8.35825539 2.77455592 1.97537136 8.35825539 2.77455592 2.066412687 8.34551334 1.99803543
		 2.45281291 8.34551334 1.99803543 2.066412687 8.73191357 1.99803543 2.45281291 8.73191357 1.99803543
		 2.29216361 8.75875378 1.15913916 2.67856383 8.75875378 1.15913916 2.29216361 9.145154 1.15913916
		 2.67856383 9.145154 1.15913916 -1.58897114 7.97185516 2.77455592 -1.97537136 7.97185516 2.77455592
		 -1.58897114 8.35825539 2.77455592 -1.97537136 8.35825539 2.77455592 -2.066412687 8.34551334 1.99803543
		 -2.45281291 8.34551334 1.99803543 -2.066412687 8.73191357 1.99803543 -2.45281291 8.73191357 1.99803543
		 -2.29216361 8.75875378 1.15913916 -2.67856383 8.75875378 1.15913916 -2.29216361 9.145154 1.15913916
		 -2.67856383 9.145154 1.15913916;
	setAttr -s 24 ".ed[0:23]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 13 15 0 14 15 0 12 14 0 16 17 0 17 19 0
		 18 19 0 16 18 0 20 21 0 21 23 0 22 23 0 20 22 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 15 14 -14 -13
		mu 0 4 12 15 14 13
		f 4 19 18 -18 -17
		mu 0 4 16 19 18 17
		f 4 23 22 -22 -21
		mu 0 4 20 23 22 21;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "nosFlo_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "525C1CBB-4C5D-0FD3-69A8-3B99D0720CBD";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 8.4758648872375488 3.985405445098877 ;
	setAttr ".sp" -type "double3" 0 8.4758648872375488 3.985405445098877 ;
createNode mesh -n "nosFlo_bs_meshShape" -p "nosFlo_bs_mesh";
	rename -uid "6D81FF2F-4EA1-8F7E-700E-8E96D9C33362";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 4 ".pt";
	setAttr ".pt[16]" -type "float3" -2.2351742e-08 3.7252903e-09 1.1175871e-08 ;
	setAttr ".pt[17]" -type "float3" -2.2351742e-08 3.7252903e-09 1.1175871e-08 ;
	setAttr ".pt[94]" -type "float3" -2.2351742e-08 3.7252903e-09 1.1175871e-08 ;
	setAttr ".pt[95]" -type "float3" -2.2351742e-08 3.7252903e-09 1.1175871e-08 ;
	setAttr ".vcs" 2;
createNode mesh -n "nosFlo_bs_meshShapeOrig" -p "nosFlo_bs_mesh";
	rename -uid "E7C0495E-4A16-6A0E-6AC3-6FAD25FB7F04";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 60 ".uvst[0].uvsp[0:59]" -type "float2" 1 0 1 1 0 0 1 0 1
		 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1
		 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0
		 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 60 ".vt[0:59]"  0.19335288 7.17070961 4.017320633 0.19335288 7.55710983 4.017320633
		 0.69016916 7.25559378 3.69046354 1.076569319 7.25559378 3.69046354 0.69016916 7.641994 3.69046354
		 1.076569319 7.641994 3.69046354 0.40155536 7.17745113 3.85999751 0.78795558 7.17745113 3.85999751
		 0.40155533 7.56385136 3.85999751 0.78795558 7.56385136 3.85999751 0.78613305 8.95426846 4.029087067
		 1.17253304 8.95426846 4.029087067 0.78613305 9.34066868 4.029087067 1.17253304 9.34066868 4.029087067
		 0.91568041 7.4846406 3.57041836 1.30208063 7.4846406 3.57041836 0.91568041 7.87104082 3.57041836
		 1.30208063 7.87104082 3.57041836 0.36477876 9.39461994 4.40039253 0.75117874 9.39461994 4.40039253
		 0.36477876 9.78102016 4.40039253 0.75117874 9.78102016 4.40039253 1.16594505 8.087018967 3.59421587
		 1.55234528 8.087018967 3.59421587 1.16594505 8.47341919 3.59421587 1.55234528 8.47341919 3.59421587
		 0.11544472 7.17071724 3.97461462 0.50184494 7.17071724 3.97461462 0.11544472 7.55711746 3.97461462
		 0.50184494 7.55711746 3.97461462 -0.193353 7.17070961 4.017320633 -0.193353 7.55710983 4.017320633
		 -0.69016916 7.25559378 3.69046354 -1.076569319 7.25559378 3.69046354 -0.69016916 7.641994 3.69046354
		 -1.076569319 7.641994 3.69046354 -0.40155536 7.17745113 3.85999751 -0.78795558 7.17745113 3.85999751
		 -0.40155539 7.56385136 3.85999751 -0.78795558 7.56385136 3.85999751 -0.78613305 8.95426846 4.029087067
		 -1.17253304 8.95426846 4.029087067 -0.78613305 9.34066868 4.029087067 -1.17253304 9.34066868 4.029087067
		 -0.91568041 7.4846406 3.57041836 -1.30208063 7.4846406 3.57041836 -0.91568041 7.87104082 3.57041836
		 -1.30208063 7.87104082 3.57041836 -0.36477876 9.39461994 4.40039253 -0.75117874 9.39461994 4.40039253
		 -0.36477879 9.78102016 4.40039253 -0.75117874 9.78102016 4.40039253 -1.16594505 8.087018967 3.59421587
		 -1.55234528 8.087018967 3.59421587 -1.16594505 8.47341919 3.59421587 -1.55234528 8.47341919 3.59421587
		 -0.11544472 7.17071724 3.97461462 -0.50184494 7.17071724 3.97461462 -0.11544474 7.55711746 3.97461462
		 -0.50184494 7.55711746 3.97461462;
	setAttr -s 60 ".ed[0:59]"  0 1 0 2 3 0 2 4 0 3 5 0 4 5 0 6 7 0 6 8 0
		 7 9 0 8 9 0 10 11 0 10 12 0 11 13 0 12 13 0 14 15 0 14 16 0 15 17 0 16 17 0 18 19 0
		 18 20 0 19 21 0 20 21 0 22 23 0 22 24 0 23 25 0 24 25 0 26 27 0 26 28 0 27 29 0 28 29 0
		 30 0 0 32 33 0 33 35 0 34 35 0 32 34 0 36 37 0 37 39 0 38 39 0 36 38 0 40 41 0 41 43 0
		 42 43 0 40 42 0 44 45 0 45 47 0 46 47 0 44 46 0 48 49 0 49 51 0 50 51 0 48 50 0 52 53 0
		 53 55 0 54 55 0 52 54 0 56 57 0 57 59 0 58 59 0 56 58 0 30 31 0 1 31 0;
	setAttr -s 15 -ch 60 ".fc[0:14]" -type "polyFaces" 
		f 4 1 3 -5 -3
		mu 0 4 2 3 4 5
		f 4 5 7 -9 -7
		mu 0 4 6 7 8 9
		f 4 9 11 -13 -11
		mu 0 4 10 11 12 13
		f 4 13 15 -17 -15
		mu 0 4 14 15 16 17
		f 4 17 19 -21 -19
		mu 0 4 18 19 20 21
		f 4 21 23 -25 -23
		mu 0 4 22 23 24 25
		f 4 25 27 -29 -27
		mu 0 4 26 27 28 29
		f 4 33 32 -32 -31
		mu 0 4 30 33 32 31
		f 4 37 36 -36 -35
		mu 0 4 34 37 36 35
		f 4 41 40 -40 -39
		mu 0 4 38 41 40 39
		f 4 45 44 -44 -43
		mu 0 4 42 45 44 43
		f 4 49 48 -48 -47
		mu 0 4 46 49 48 47
		f 4 53 52 -52 -51
		mu 0 4 50 53 52 51
		f 4 57 56 -56 -55
		mu 0 4 54 57 56 55
		f 4 59 -59 29 0
		mu 0 4 1 59 58 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".vcs" 2;
createNode transform -n "chin_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "24A2E5EC-447E-03FE-D307-CDB33C2A3170";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 7.4078307151794434 2.4671060740947723 ;
	setAttr ".sp" -type "double3" 0 7.4078307151794434 2.4671060740947723 ;
createNode mesh -n "chin_bs_meshShape" -p "chin_bs_mesh";
	rename -uid "444713C5-477C-90BF-0C30-2FBBF2A2EC7C";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.4996533989906311 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 18 ".pt";
	setAttr ".pt[0]" -type "float3" -7.4505806e-09 0 -2.9802322e-08 ;
	setAttr ".pt[1]" -type "float3" -7.4505806e-09 0 -2.9802322e-08 ;
	setAttr ".pt[8]" -type "float3" 2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[9]" -type "float3" 2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[10]" -type "float3" 2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[11]" -type "float3" 2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[16]" -type "float3" -2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[17]" -type "float3" -2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[18]" -type "float3" -2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[19]" -type "float3" -2.9802322e-08 -5.9604645e-08 0 ;
	setAttr ".pt[20]" -type "float3" 5.9604645e-08 0 -1.4901161e-08 ;
	setAttr ".pt[21]" -type "float3" 5.9604645e-08 0 -1.4901161e-08 ;
	setAttr ".pt[22]" -type "float3" -1.1175871e-08 0 -2.9802322e-08 ;
	setAttr ".pt[23]" -type "float3" -1.1175871e-08 0 -2.9802322e-08 ;
	setAttr ".pt[24]" -type "float3" 0 -1.4901161e-08 0 ;
	setAttr ".pt[25]" -type "float3" 0 -1.4901161e-08 0 ;
	setAttr ".pt[46]" -type "float3" 6.3329935e-08 -1.4901161e-08 0 ;
	setAttr ".pt[47]" -type "float3" 6.3329935e-08 -1.4901161e-08 0 ;
	setAttr ".vcs" 2;
createNode mesh -n "chin_bs_meshShapeOrig" -p "chin_bs_mesh";
	rename -uid "8E5B9EC5-45B5-ED58-9E6A-AC91F0C4FCF2";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 44 ".uvst[0].uvsp[0:43]" -type "float2" 1 0 1 1 0 0 1 0 1
		 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1
		 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 44 ".vt[0:43]"  0.19333392 6.40701008 3.98384261 0.19333392 6.7934103 3.98384261
		 0.93467879 6.71683025 3.18136597 1.32107878 6.71683025 3.18136597 0.93467879 7.10323048 3.18136597
		 1.32107878 7.10323048 3.18136597 1.82266414 7.49680853 1.87655044 2.20906448 7.49680853 1.87655044
		 1.82266414 7.88320875 1.87655044 2.20906448 7.88320875 1.87655044 0.25925884 6.40698147 3.91733241
		 0.64565873 6.40698147 3.91733241 0.25925878 6.79338169 3.91733241 0.64565873 6.79338169 3.91733241
		 1.40536714 7.08535862 2.6469698 1.79176736 7.08535862 2.6469698 1.40536714 7.47175837 2.6469698
		 1.79176736 7.47175837 2.6469698 2.12827349 8.022279739 0.95036954 2.51467371 8.022279739 0.95036954
		 2.12827349 8.40867996 0.95036954 2.51467371 8.40867996 0.95036954 -0.19333394 6.40701008 3.98384261
		 -0.19333394 6.7934103 3.98384261 -0.93467879 6.71683025 3.18136597 -1.32107878 6.71683025 3.18136597
		 -0.93467879 7.10323048 3.18136597 -1.32107878 7.10323048 3.18136597 -1.82266414 7.49680853 1.87655044
		 -2.20906448 7.49680853 1.87655044 -1.82266414 7.88320875 1.87655044 -2.20906448 7.88320875 1.87655044
		 -0.25925878 6.40698147 3.91733241 -0.64565873 6.40698147 3.91733241 -0.25925878 6.79338169 3.91733241
		 -0.64565873 6.79338169 3.91733241 -1.40536714 7.08535862 2.6469698 -1.79176736 7.08535862 2.6469698
		 -1.40536714 7.47175837 2.6469698 -1.79176736 7.47175837 2.6469698 -2.12827349 8.022279739 0.95036954
		 -2.51467371 8.022279739 0.95036954 -2.12827349 8.40867996 0.95036954 -2.51467371 8.40867996 0.95036954;
	setAttr -s 44 ".ed[0:43]"  0 1 0 2 3 0 2 4 0 3 5 0 4 5 0 6 7 0 6 8 0
		 7 9 0 8 9 0 10 11 0 10 12 0 11 13 0 12 13 0 14 15 0 14 16 0 15 17 0 16 17 0 18 19 0
		 18 20 0 19 21 0 20 21 0 22 0 0 24 25 0 25 27 0 26 27 0 24 26 0 28 29 0 29 31 0 30 31 0
		 28 30 0 32 33 0 33 35 0 34 35 0 32 34 0 36 37 0 37 39 0 38 39 0 36 38 0 40 41 0 41 43 0
		 42 43 0 40 42 0 22 23 0 1 23 0;
	setAttr -s 11 -ch 44 ".fc[0:10]" -type "polyFaces" 
		f 4 1 3 -5 -3
		mu 0 4 2 3 4 5
		f 4 5 7 -9 -7
		mu 0 4 6 7 8 9
		f 4 9 11 -13 -11
		mu 0 4 10 11 12 13
		f 4 13 15 -17 -15
		mu 0 4 14 15 16 17
		f 4 17 19 -21 -19
		mu 0 4 18 19 20 21
		f 4 25 24 -24 -23
		mu 0 4 22 25 24 23
		f 4 29 28 -28 -27
		mu 0 4 26 29 28 27
		f 4 33 32 -32 -31
		mu 0 4 30 33 32 31
		f 4 37 36 -36 -35
		mu 0 4 34 37 36 35
		f 4 41 40 -40 -39
		mu 0 4 38 41 40 39
		f 4 43 -43 21 0
		mu 0 4 1 43 42 0;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "lipFrame_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "57F906D9-4702-BB5D-3B44-599D1989C466";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 8.1315779685974121 4.0205810070037842 ;
	setAttr ".sp" -type "double3" 0 8.1315779685974121 4.0205810070037842 ;
createNode mesh -n "lipFrame_bs_meshShape" -p "lipFrame_bs_mesh";
	rename -uid "81689E3E-43F9-53A2-87BC-C29FC8BB7A08";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".pt";
	setAttr ".pt[24]" -type "float3" 7.4505806e-09 0 0 ;
	setAttr ".pt[25]" -type "float3" 7.4505806e-09 0 0 ;
	setAttr ".pt[26]" -type "float3" -7.4505806e-09 0 0 ;
	setAttr ".pt[27]" -type "float3" -7.4505806e-09 0 0 ;
	setAttr ".pt[52]" -type "float3" -7.4505806e-09 0 0 ;
	setAttr ".pt[53]" -type "float3" -7.4505806e-09 0 0 ;
	setAttr ".pt[54]" -type "float3" 7.4505806e-09 0 0 ;
	setAttr ".pt[55]" -type "float3" 7.4505806e-09 0 0 ;
	setAttr ".vcs" 2;
createNode mesh -n "lipFrame_bs_meshShapeOrig" -p "lipFrame_bs_mesh";
	rename -uid "C800A044-40DD-E8AE-F972-3E833FEE9F4A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 48 ".uvst[0].uvsp[0:47]" -type "float2" 0 0 1 0 0 1 1 1 1
		 0 1 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0 1 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0
		 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0 1
		 1 1 0 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 48 ".vt[0:47]"  0.74755168 8.27432823 3.94066405 1.13395143 8.27432823 3.94066405
		 0.74755168 8.66072845 3.94066405 1.13395143 8.66072845 3.94066405 0.19334245 7.51615238 4.18528414
		 0.19334245 7.9025526 4.18528414 0.27348781 8.3494997 4.25924301 0.65988779 8.3494997 4.25924301
		 0.27348781 8.73589993 4.25924301 0.65988779 8.73589993 4.25924301 0.18563652 7.5051384 4.099388599
		 0.5720365 7.5051384 4.099388599 0.18563652 7.89153862 4.099388599 0.5720365 7.89153862 4.099388599
		 0.19333386 8.37161732 4.31395054 0.19333386 8.75801754 4.31395054 0.53247046 7.57572842 3.9046979
		 0.91887021 7.57572842 3.9046979 0.53247046 7.96212864 3.9046979 0.91887021 7.96212864 3.9046979
		 0.79964757 7.89533234 3.72721148 1.18604732 7.89533234 3.72721148 0.79964757 8.28173256 3.72721148
		 1.18604732 8.28173256 3.72721148 -0.74755168 8.27432823 3.94066405 -1.13395143 8.27432823 3.94066405
		 -0.74755168 8.66072845 3.94066405 -1.13395143 8.66072845 3.94066405 -0.19334245 7.51615238 4.18528414
		 -0.19334245 7.9025526 4.18528414 -0.27348781 8.3494997 4.25924301 -0.65988779 8.3494997 4.25924301
		 -0.27348781 8.73589993 4.25924301 -0.65988779 8.73589993 4.25924301 -0.18563652 7.5051384 4.099388599
		 -0.5720365 7.5051384 4.099388599 -0.18563652 7.89153862 4.099388599 -0.5720365 7.89153862 4.099388599
		 -0.19333386 8.37161732 4.31395054 -0.19333386 8.75801754 4.31395054 -0.53247046 7.57572842 3.9046979
		 -0.91887021 7.57572842 3.9046979 -0.53247046 7.96212864 3.9046979 -0.91887021 7.96212864 3.9046979
		 -0.79964757 7.89533234 3.72721148 -1.18604732 7.89533234 3.72721148 -0.79964757 8.28173256 3.72721148
		 -1.18604732 8.28173256 3.72721148;
	setAttr -s 48 ".ed[0:47]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 6 7 0 6 8 0
		 7 9 0 8 9 0 10 11 0 10 12 0 11 13 0 12 13 0 14 15 0 16 17 0 16 18 0 17 19 0 18 19 0
		 20 21 0 20 22 0 21 23 0 22 23 0 28 4 0 38 14 0 24 25 0 25 27 0 26 27 0 24 26 0 30 31 0
		 31 33 0 32 33 0 30 32 0 34 35 0 35 37 0 36 37 0 34 36 0 40 41 0 41 43 0 42 43 0 40 42 0
		 44 45 0 45 47 0 46 47 0 44 46 0 28 29 0 5 29 0 38 39 0 15 39 0;
	setAttr -s 12 -ch 48 ".fc[0:11]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 3 2
		f 4 5 7 -9 -7
		mu 0 4 6 7 8 9
		f 4 9 11 -13 -11
		mu 0 4 10 11 12 13
		f 4 14 16 -18 -16
		mu 0 4 16 17 18 19
		f 4 18 20 -22 -20
		mu 0 4 20 21 22 23
		f 4 27 26 -26 -25
		mu 0 4 24 27 26 25
		f 4 31 30 -30 -29
		mu 0 4 28 31 30 29
		f 4 35 34 -34 -33
		mu 0 4 32 35 34 33
		f 4 39 38 -38 -37
		mu 0 4 36 39 38 37
		f 4 43 42 -42 -41
		mu 0 4 40 43 42 41
		f 4 45 -45 22 4
		mu 0 4 5 45 44 4
		f 4 47 -47 23 13
		mu 0 4 15 47 46 14;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "nose_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "4D1EC254-4D76-8C2C-AD5D-C188D96D1E3C";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 9.7934451103210449 4.566899299621582 ;
	setAttr ".sp" -type "double3" 0 9.7934451103210449 4.566899299621582 ;
createNode mesh -n "nose_bs_meshShape" -p "nose_bs_mesh";
	rename -uid "05516DAB-46BF-AB8F-51EE-0EAA4BFC12F7";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 4 ".pt";
	setAttr ".pt[16]" -type "float3" -1.4901161e-08 0 0 ;
	setAttr ".pt[17]" -type "float3" -1.4901161e-08 0 0 ;
	setAttr ".pt[36]" -type "float3" 1.4901161e-08 0 0 ;
	setAttr ".pt[37]" -type "float3" 1.4901161e-08 0 0 ;
	setAttr ".vcs" 2;
createNode mesh -n "nose_bs_meshShapeOrig" -p "nose_bs_mesh";
	rename -uid "94284760-4A67-1ECE-A0F9-2B9801333CC1";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 28 ".uvst[0].uvsp[0:27]" -type "float2" 1 0 1 1 1 0 1 1 1
		 0 1 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0 1 1 1 0
		 1 1 1 0 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 28 ".vt[0:27]"  0.19333279 9.00088977814 4.9873991 0.19333279 9.38729 4.9873991
		 0.19674611 10.49175358 4.41661406 0.19674611 10.8781538 4.41661406 0.19334 8.70873642 4.35929441
		 0.19334 9.095136642 4.35929441 0.14754111 8.75581741 4.2669735 0.53394133 8.75581741 4.2669735
		 0.14754111 9.14221764 4.2669735 0.53394133 9.14221764 4.2669735 0.49086612 8.96612358 4.1463995
		 0.87726635 8.96612358 4.1463995 0.49086612 9.3525238 4.1463995 0.87726635 9.3525238 4.1463995
		 -0.19333279 9.00088977814 4.9873991 -0.19333279 9.38729 4.9873991 -0.19674613 10.49175358 4.41661406
		 -0.19674613 10.8781538 4.41661406 -0.19334 8.70873642 4.35929441 -0.19334 9.095136642 4.35929441
		 -0.14754111 8.75581741 4.2669735 -0.53394133 8.75581741 4.2669735 -0.14754111 9.14221764 4.2669735
		 -0.53394133 9.14221764 4.2669735 -0.49086612 8.96612358 4.1463995 -0.87726635 8.96612358 4.1463995
		 -0.49086612 9.3525238 4.1463995 -0.87726635 9.3525238 4.1463995;
	setAttr -s 28 ".ed[0:27]"  0 1 0 2 3 0 4 5 0 6 7 0 6 8 0 7 9 0 8 9 0
		 10 11 0 10 12 0 11 13 0 12 13 0 14 0 0 16 2 0 18 4 0 20 21 0 21 23 0 22 23 0 20 22 0
		 24 25 0 25 27 0 26 27 0 24 26 0 14 15 0 1 15 0 16 17 0 3 17 0 18 19 0 5 19 0;
	setAttr -s 7 -ch 28 ".fc[0:6]" -type "polyFaces" 
		f 4 3 5 -7 -5
		mu 0 4 6 7 8 9
		f 4 7 9 -11 -9
		mu 0 4 10 11 12 13
		f 4 17 16 -16 -15
		mu 0 4 14 17 16 15
		f 4 21 20 -20 -19
		mu 0 4 18 21 20 19
		f 4 23 -23 11 0
		mu 0 4 1 23 22 0
		f 4 25 -25 12 1
		mu 0 4 3 25 24 2
		f 4 27 -27 13 2
		mu 0 4 5 27 26 4;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "forehead_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "88799EAD-41DE-C8F1-FE93-789F07B796A9";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 12.436029434204102 4.2962100505828857 ;
	setAttr ".sp" -type "double3" 0 12.436029434204102 4.2962100505828857 ;
createNode mesh -n "forehead_bs_meshShape" -p "forehead_bs_mesh";
	rename -uid "78BBD48F-4835-D53C-549D-639FDC99A505";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 6 ".pt";
	setAttr ".pt[12]" -type "float3" -7.4505806e-09 0 0 ;
	setAttr ".pt[13]" -type "float3" -7.4505806e-09 0 0 ;
	setAttr ".pt[14]" -type "float3" 3.7252903e-09 0 0 ;
	setAttr ".pt[15]" -type "float3" 3.7252903e-09 0 0 ;
	setAttr ".pt[28]" -type "float3" 3.7252903e-09 0 0 ;
	setAttr ".pt[29]" -type "float3" 3.7252903e-09 0 0 ;
	setAttr ".vcs" 2;
createNode mesh -n "forehead_bs_meshShapeOrig" -p "forehead_bs_mesh";
	rename -uid "6764BA05-400D-E9FF-D10D-AD89E8B980DF";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 24 ".uvst[0].uvsp[0:23]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 1 0 1 1 1 0 1 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0 1 1 1 0 1 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 24 ".vt[0:23]"  1.073071599 12.62709332 4.1008544 1.45947158 12.62709332 4.1008544
		 1.073071599 13.013493538 4.1008544 1.45947158 13.013493538 4.1008544 1.076425076 12.056821823 4.24307823
		 1.46282506 12.056821823 4.24307823 1.076425076 12.44322205 4.24307823 1.46282506 12.44322205 4.24307823
		 0.20019317 12.60213661 4.38196802 0.20019317 12.98853683 4.38196802 0.19750285 11.85856533 4.4915657
		 0.19750285 12.24496555 4.4915657 -1.073071599 12.62709332 4.1008544 -1.45947158 12.62709332 4.1008544
		 -1.073071599 13.013493538 4.1008544 -1.45947158 13.013493538 4.1008544 -1.076425076 12.056821823 4.24307823
		 -1.46282506 12.056821823 4.24307823 -1.076425076 12.44322205 4.24307823 -1.46282506 12.44322205 4.24307823
		 -0.20019317 12.60213661 4.38196802 -0.20019317 12.98853683 4.38196802 -0.19750285 11.85856533 4.4915657
		 -0.19750285 12.24496555 4.4915657;
	setAttr -s 24 ".ed[0:23]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 10 11 0 20 8 0 22 10 0 12 13 0 13 15 0 14 15 0 12 14 0 16 17 0 17 19 0
		 18 19 0 16 18 0 20 21 0 9 21 0 22 23 0 11 23 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 15 14 -14 -13
		mu 0 4 12 15 14 13
		f 4 19 18 -18 -17
		mu 0 4 16 19 18 17
		f 4 21 -21 10 8
		mu 0 4 9 21 20 8
		f 4 23 -23 11 9
		mu 0 4 11 23 22 10;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "throat_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "007D15E1-4485-F350-9BF7-9D8439E2D730";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0.00018632411956787109 5.0796589851379395 1.7602410316467285 ;
	setAttr ".sp" -type "double3" 0.00018632411956787109 5.0796589851379395 1.7602410316467285 ;
createNode mesh -n "throat_bs_meshShape" -p "throat_bs_mesh";
	rename -uid "52296B4C-488E-590B-F1DA-91B14A123E46";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.50017115473747253 0.75391658024354413 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "throat_bs_meshShapeOrig" -p "throat_bs_mesh";
	rename -uid "9B8BAB84-4FF5-C211-0591-9AAFE0D3288A";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 20 ".uvst[0].uvsp[0:19]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 20 ".pt[0:19]" -type "float3"  1.5976022 -0.94197649 -0.33993834 
		1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 
		-0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 
		-0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 
		1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 
		-0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 
		-0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 
		1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 -0.33993834 1.5976022 -0.94197649 
		-0.33993834;
	setAttr -s 20 ".vt[0:19]"  -1.79059696 7.18516254 2.62014747 -1.40419698 7.18516254 2.62014747
		 -1.79059696 7.57156277 2.62014747 -1.40419698 7.57156277 2.62014747 -1.79063392 6.37866592 1.93635392
		 -1.40423393 6.37866592 1.93635392 -1.79063392 6.76506615 1.93635392 -1.40423393 6.76506615 1.93635392
		 -1.79063237 4.4717083 1.7086457 -1.40423203 4.4717083 1.7086457 -1.79063237 4.85810852 1.7086457
		 -1.40423203 4.85810852 1.7086457 -1.79054976 6.99479818 2.12523317 -1.40414977 6.99479818 2.12523317
		 -1.79054976 7.38119841 2.12523317 -1.40414977 7.38119841 2.12523317 -1.79068208 5.31533337 1.58021128
		 -1.40428185 5.31533337 1.58021128 -1.79068208 5.70173359 1.58021128 -1.40428185 5.70173359 1.58021128;
	setAttr -s 20 ".ed[0:19]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 12 14 0 13 15 0 14 15 0 16 17 0 16 18 0
		 17 19 0 18 19 0;
	setAttr -s 5 -ch 20 ".fc[0:4]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 12 14 -16 -14
		mu 0 4 12 13 14 15
		f 4 16 18 -20 -18
		mu 0 4 16 17 18 19;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "chinThroat_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "B123C541-4367-CA7B-880A-1B9ED209D0F2";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 6.3430089950561523 1.3779069185256958 ;
	setAttr ".sp" -type "double3" 0 6.3430089950561523 1.3779069185256958 ;
createNode mesh -n "chinThroat_bs_meshShape" -p "chinThroat_bs_mesh";
	rename -uid "860E9C34-404F-DBCB-0EFB-7BB9EADE1967";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "chinThroat_bs_meshShapeOrig" -p "chinThroat_bs_mesh";
	rename -uid "310EC321-48B6-1F0A-76B0-AD896E548C42";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 16 ".uvst[0].uvsp[0:15]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 16 ".pt[0:15]" -type "float3"  5.8629656 0.1271423 -1.062636 
		5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 
		5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 
		5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 
		5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 
		5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636 5.8629656 0.1271423 -1.062636;
	setAttr -s 16 ".vt[0:15]"  -4.7982707 6.69683456 2.55842185 -4.41187096 6.69683456 2.55842185
		 -4.7982707 7.083234787 2.55842185 -4.41187096 7.083234787 2.55842185 -5.238204 5.34849834 2.32266402
		 -4.85180378 5.34849834 2.32266402 -5.238204 5.73489857 2.32266402 -4.85180378 5.73489857 2.32266402
		 -6.92766047 6.69683456 2.55842185 -7.31406021 6.69683456 2.55842185 -6.92766047 7.083234787 2.55842185
		 -7.31406021 7.083234787 2.55842185 -6.48772717 5.34849834 2.32266402 -6.87412739 5.34849834 2.32266402
		 -6.48772717 5.73489857 2.32266402 -6.87412739 5.73489857 2.32266402;
	setAttr -s 16 ".ed[0:15]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 9 11 0 10 11 0 8 10 0 12 13 0 13 15 0 14 15 0 12 14 0;
	setAttr -s 4 -ch 16 ".fc[0:3]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 11 10 -10 -9
		mu 0 4 8 11 10 9
		f 4 15 14 -14 -13
		mu 0 4 12 15 14 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "clavicleNeck_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "E934E12B-4309-4937-D095-0BAE95493FC2";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 5.8404357433319092 0.51335811614990234 ;
	setAttr ".sp" -type "double3" 0 5.8404357433319092 0.51335811614990234 ;
createNode mesh -n "clavicleNeck_bs_meshShape" -p "clavicleNeck_bs_mesh";
	rename -uid "E08B0BC0-450E-7B78-E292-79A3C7AB88F8";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "clavicleNeck_bs_meshShapeOrig" -p "clavicleNeck_bs_mesh";
	rename -uid "58100AAE-40DC-7C3A-0F44-5F8B36D8A5F0";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 40 ".uvst[0].uvsp[0:39]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0
		 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 40 ".vt[0:39]"  2.091187954 7.068972588 0.20060849 2.4775877 7.068972588 0.20060849
		 2.091187954 7.45537281 0.20060849 2.4775877 7.45537281 0.20060849 2.030300617 6.29565811 0.40176344
		 2.41670036 6.29565811 0.40176344 2.030300617 6.68205833 0.40176344 2.41670036 6.68205833 0.40176344
		 1.94996929 5.42420626 0.64830494 2.33636904 5.42420626 0.64830494 1.94996929 5.81060648 0.64830494
		 2.33636904 5.81060648 0.64830494 1.4715085 4.29347754 1.026381493 1.85790825 4.29347754 1.026381493
		 1.4715085 4.67987776 1.026381493 1.85790825 4.67987776 1.026381493 2.49564695 4.22549868 0.00033473969
		 2.8820467 4.22549868 0.00033473969 2.49564695 4.6118989 0.00033473969 2.8820467 4.6118989 0.00033473969
		 -2.091187954 7.068972588 0.20060849 -2.4775877 7.068972588 0.20060849 -2.091187954 7.45537281 0.20060849
		 -2.4775877 7.45537281 0.20060849 -2.030300617 6.29565811 0.40176344 -2.41670036 6.29565811 0.40176344
		 -2.030300617 6.68205833 0.40176344 -2.41670036 6.68205833 0.40176344 -1.94996929 5.42420626 0.64830494
		 -2.33636904 5.42420626 0.64830494 -1.94996929 5.81060648 0.64830494 -2.33636904 5.81060648 0.64830494
		 -1.4715085 4.29347754 1.026381493 -1.85790825 4.29347754 1.026381493 -1.4715085 4.67987776 1.026381493
		 -1.85790825 4.67987776 1.026381493 -2.49564695 4.22549868 0.00033473969 -2.8820467 4.22549868 0.00033473969
		 -2.49564695 4.6118989 0.00033473969 -2.8820467 4.6118989 0.00033473969;
	setAttr -s 40 ".ed[0:39]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 12 14 0 13 15 0 14 15 0 16 17 0 16 18 0
		 17 19 0 18 19 0 20 21 0 21 23 0 22 23 0 20 22 0 24 25 0 25 27 0 26 27 0 24 26 0 28 29 0
		 29 31 0 30 31 0 28 30 0 32 33 0 33 35 0 34 35 0 32 34 0 36 37 0 37 39 0 38 39 0 36 38 0;
	setAttr -s 10 -ch 40 ".fc[0:9]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 12 14 -16 -14
		mu 0 4 12 13 14 15
		f 4 16 18 -20 -18
		mu 0 4 16 17 18 19
		f 4 23 22 -22 -21
		mu 0 4 20 23 22 21
		f 4 27 26 -26 -25
		mu 0 4 24 27 26 25
		f 4 31 30 -30 -29
		mu 0 4 28 31 30 29
		f 4 35 34 -34 -33
		mu 0 4 32 35 34 33
		f 4 39 38 -38 -37
		mu 0 4 36 39 38 37;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "browLid_bs_mesh" -p "base_bs_mesh_grp";
	rename -uid "5B389FA5-4D83-ABD7-AA27-79ADC7526A0A";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 11.048150062561035 3.7572503089904785 ;
	setAttr ".sp" -type "double3" 0 11.048150062561035 3.7572503089904785 ;
createNode mesh -n "browLid_bs_meshShape" -p "browLid_bs_mesh";
	rename -uid "B068E1AF-464F-E049-9359-839955A0D398";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "browLid_bs_meshShapeOrig" -p "browLid_bs_mesh";
	rename -uid "E703CC5B-4EF6-D203-E91A-30AB880A197B";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 24 ".uvst[0].uvsp[0:23]" -type "float2" 0 0 1 0 1 1 0 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 24 ".vt[0:23]"  1.10831046 10.95543003 4.11283207 1.49471068 10.95543003 4.11283207
		 1.10831046 11.34183025 4.11283207 1.49471068 11.34183025 4.11283207 0.41431224 10.75446987 4.148417
		 0.80071235 10.75446987 4.148417 0.41431224 11.14087009 4.148417 0.80071235 11.14087009 4.148417
		 1.91138089 10.92590046 3.36608362 2.29778099 10.92590046 3.36608362 1.91138089 11.31230068 3.36608362
		 2.29778099 11.31230068 3.36608362 -1.10831046 10.95543003 4.11283207 -1.49471068 10.95543003 4.11283207
		 -1.10831046 11.34183025 4.11283207 -1.49471068 11.34183025 4.11283207 -0.41431224 10.75446987 4.148417
		 -0.80071235 10.75446987 4.148417 -0.41431224 11.14087009 4.148417 -0.80071235 11.14087009 4.148417
		 -1.91138089 10.92590046 3.36608362 -2.29778099 10.92590046 3.36608362 -1.91138089 11.31230068 3.36608362
		 -2.29778099 11.31230068 3.36608362;
	setAttr -s 24 ".ed[0:23]"  0 1 0 0 2 0 1 3 0 2 3 0 4 5 0 4 6 0 5 7 0
		 6 7 0 8 9 0 8 10 0 9 11 0 10 11 0 12 13 0 13 15 0 14 15 0 12 14 0 16 17 0 17 19 0
		 18 19 0 16 18 0 20 21 0 21 23 0 22 23 0 20 22 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 2 -4 -2
		mu 0 4 0 1 2 3
		f 4 4 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 8 10 -12 -10
		mu 0 4 8 9 10 11
		f 4 15 14 -14 -13
		mu 0 4 12 15 14 13
		f 4 19 18 -18 -17
		mu 0 4 16 19 18 17
		f 4 23 22 -22 -21
		mu 0 4 20 23 22 21;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "base_bs_mesh" -p "bs_mesh_grp";
	rename -uid "5A6EAE69-4203-C2EF-16BB-C6A2C6CE7076";
	setAttr ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 8.2716126441955566 2.4938669204711914 ;
	setAttr ".sp" -type "double3" 0 8.2716126441955566 2.4938669204711914 ;
createNode mesh -n "base_bs_meshShape" -p "base_bs_mesh";
	rename -uid "AD7786BF-4831-3847-D2D6-7D8CAE1320A2";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "base_bs_meshShapeOrig" -p "base_bs_mesh";
	rename -uid "19D56732-4A9D-235F-7664-5984E8245593";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 5 ".gtag";
	setAttr ".gtag[0].gtagnm" -type "string" "back";
	setAttr ".gtag[0].gtagcmp" -type "componentList" 18 "e[31]" "e[35]" "e[39]" "e[42]" "e[46]" "e[50]" "e[55]" "e[59]" "e[63]" "e[67]" "e[71]" "e[75]" "e[78]" "e[82]" "e[86]" "e[90]" "e[94]" "e[98]";
	setAttr ".gtag[1].gtagnm" -type "string" "front";
	setAttr ".gtag[1].gtagcmp" -type "componentList" 18 "e[28]" "e[32]" "e[36]" "e[40]" "e[44]" "e[48]" "e[52]" "e[56]" "e[60]" "e[64]" "e[68]" "e[72]" "e[76]" "e[80]" "e[84]" "e[88]" "e[92]" "e[96]";
	setAttr ".gtag[2].gtagnm" -type "string" "left";
	setAttr ".gtag[2].gtagcmp" -type "componentList" 18 "e[29]" "e[33]" "e[37]" "e[43]" "e[47]" "e[51]" "e[53]" "e[57]" "e[61]" "e[65]" "e[69]" "e[73]" "e[79]" "e[83]" "e[87]" "e[91]" "e[95]" "e[99]";
	setAttr ".gtag[3].gtagnm" -type "string" "right";
	setAttr ".gtag[3].gtagcmp" -type "componentList" 18 "e[30]" "e[34]" "e[38]" "e[41]" "e[45]" "e[49]" "e[54]" "e[58]" "e[62]" "e[66]" "e[70]" "e[74]" "e[77]" "e[81]" "e[85]" "e[89]" "e[93]" "e[97]";
	setAttr ".gtag[4].gtagnm" -type "string" "rim";
	setAttr ".gtag[4].gtagcmp" -type "componentList" 1 "e[28:99]";
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 452 ".uvst[0].uvsp";
	setAttr ".uvst[0].uvsp[0:249]" -type "float2" 0.54645681 9.5367432e-07 0.62414587
		 9.5367432e-07 0.62414587 0.48715687 0.54645681 0.48715687 0.72647774 0.36348915 0.80416679
		 0.36348915 0.80416679 0.85064507 0.72647774 0.85064507 0.92231083 0.51284504 0.99999988
		 0.51284504 0.99999988 1.000000953674 0.92231083 1.000000953674 0.45354307 9.5367432e-07
		 0.45354307 0.48715687 0.37585402 0.48715687 0.37585402 9.5367432e-07 0.27352214 0.36348915
		 0.27352214 0.85064507 0.19583309 0.85064507 0.19583309 0.36348915 0.077689052 0.51284504
		 0.077689052 1.000000953674 -2.9802322e-08 1.000000953674 -2.9802322e-08 0.51284504
		 0.53894866 0.61740589 0.46105129 0.61740589 0.46105129 0.13024998 0.53894866 0.13024998
		 0.73317075 0.033992767 0.83417785 0.033992767 0.83417785 0.86169815 0.73317075 0.86169815
		 0.82509363 0 0.92610073 0 0.92610073 0.82770538 0.82509363 0.82770538 0.8989929 0.17229462
		 1 0.17229462 1 1 0.8989929 1 0.26682925 0.033992767 0.26682925 0.86169815 0.16582215
		 0.86169815 0.16582215 0.033992767 0.17490637 0 0.17490637 0.82770538 0.073899269
		 0.82770538 0.073899269 0 0.1010071 0.17229462 0.1010071 1 0 1 0 0.17229462 0.92796135
		 0.80209303 0.99999988 0.80209303 0.99999988 1 0.92796135 1 0.55448484 0.34217548
		 0.62652338 0.34217548 0.62652338 0.54008245 0.55448484 0.54008245 0.89825296 0.25637054
		 0.97029138 0.25637054 0.97029138 0.45427752 0.89825296 0.45427752 0.67807806 0 0.75011659
		 0 0.75011659 0.19790745 0.67807806 0.19790745 0.84011316 0.05450201 0.91215169 0.05450201
		 0.91215169 0.25240898 0.84011316 0.25240898 0.90672231 0.58121347 0.97876084 0.58121347
		 0.97876084 0.77912045 0.90672231 0.77912045 0.072038531 0.80209303 0.072038531 1
		 -2.9802322e-08 1 -2.9802322e-08 0.80209303 0.44551504 0.34217548 0.44551504 0.54008245
		 0.37347651 0.54008245 0.37347651 0.34217548 0.10174692 0.25637054 0.10174692 0.45427752
		 0.029708445 0.45427752 0.029708445 0.25637054 0.32192177 0 0.32192177 0.19790745
		 0.24988329 0.19790745 0.24988329 0 0.15988678 0.05450201 0.15988678 0.25240898 0.087848186
		 0.25240898 0.087848186 0.05450201 0.093277514 0.58121347 0.093277514 0.77912045 0.021239042
		 0.77912045 0.021239042 0.58121347 0.74820781 0 0.8207823 0 0.8207823 0.35266304 0.74820781
		 0.35266304 0.84275305 0.20727062 0.91532743 0.20727062 0.91532743 0.55993271 0.84275305
		 0.55993271 0.92742574 0.64733791 1.000000238419 0.64733791 1.000000238419 1.000000953674
		 0.92742574 1.000000953674 0.25179243 0 0.25179243 0.35266304 0.17921793 0.35266304
		 0.17921793 0 0.15724719 0.20727062 0.15724719 0.55993271 0.084672809 0.55993271 0.084672809
		 0.20727062 0.072574496 0.64733791 0.072574496 1.000000953674 5.9604645e-08 1.000000953674
		 5.9604645e-08 0.64733791 0.79660881 4.7683716e-07 0.86873698 4.7683716e-07 0.86873698
		 0.32932854 0.79660881 0.32932854 0.88573146 0.31846857 0.95785975 0.31846857 0.95785975
		 0.64779663 0.88573146 0.64779663 0.9278717 0.67067242 1 0.67067242 1 1.000000476837
		 0.9278717 1.000000476837 0.20339119 4.7683716e-07 0.20339119 0.32932854 0.13126296
		 0.32932854 0.13126296 4.7683716e-07 0.11426854 0.31846857 0.11426854 0.64779663 0.042140245
		 0.64779663 0.042140245 0.31846857 0.072128236 0.67067242 0.072128236 1.000000476837
		 0 1.000000476837 0 0.67067242 0.72229874 0.032519102 0.84675574 0.032519102 0.84675574
		 0.18054748 0.72229874 0.18054748 0.62933826 0.0025827885 0.75379515 0.0025827885
		 0.75379515 0.1506114 0.62933826 0.1506114 0.75320816 0.68327475 0.87766492 0.68327475
		 0.87766492 0.83130336 0.75320816 0.83130336 0.79493451 0.12026596 0.91939139 0.12026596
		 0.91939139 0.26829457 0.79493451 0.26829457 0.61749268 0.85197186 0.74194956 0.85197186
		 0.74194956 1.000000238419 0.61749268 1.000000238419 0.875543 0.35103488 0.99999988
		 0.35103488 0.99999988 0.49906325 0.875543 0.49906325 0.53718388 3.0994415e-06 0.66164088
		 3.0994415e-06 0.66164088 0.14803171 0.53718388 0.14803171 0.27770108 0.032519102
		 0.27770108 0.18054748 0.1532442 0.18054748 0.1532442 0.032519102 0.37066168 0.0025827885
		 0.37066162 0.1506114 0.24620473 0.1506114 0.24620473 0.0025827885 0.24679178 0.68327475
		 0.24679178 0.83130336 0.12233496 0.83130336 0.12233496 0.68327475 0.20506543 0.12026596
		 0.20506543 0.26829457 0.080608487 0.26829457 0.080608487 0.12026596 0.38250715 0.85197186
		 0.38250715 1.000000238419 0.25805032 1.000000238419 0.25805032 0.85197186 0.12445688
		 0.35103488 0.12445688 0.49906325 -2.9802322e-08 0.49906325 -2.9802322e-08 0.35103488
		 0.462816 3.0994415e-06 0.46281594 0.14803171 0.33835906 0.14803171 0.33835906 3.0994415e-06
		 0.56227756 0.14802861 0.43772227 0.14802861 0.43772227 2.3841858e-07 0.56227756 2.3841858e-07
		 0.6858449 0.15479279 0.76267385 0.15479279 0.76267385 0.3478291 0.6858449 0.3478291
		 0.86240566 0.544451 0.93923473 0.544451 0.93923473 0.73748732 0.86240566 0.73748732
		 0.5515492 0 0.62837815 0 0.62837815 0.19303608 0.55154908 0.19303608 0.77943325 0.3389008
		 0.85626233 0.3389008 0.85626233 0.53193665 0.77943325 0.53193665 0.9231708 0.80696368
		 0.99999988 0.80696368 0.99999988 0.99999976 0.9231708 0.99999976 0.31415498 0.15479279
		 0.31415498 0.3478291 0.23732597 0.3478291 0.23732597 0.15479279 0.13759422 0.544451
		 0.13759422 0.73748732 0.060765147 0.73748732 0.060765147 0.544451 0.44845074 0 0.44845074
		 0.19303608 0.37162173 0.19303608 0.37162173 0 0.22056663 0.3389008 0.22056663 0.53193665
		 0.14373755 0.53193665 0.14373755 0.3389008 0.076829076 0.80696368 0.076829076 0.99999976
		 -2.9802322e-08 0.99999976 -2.9802322e-08 0.80696368 0.53844106 0.19305038 0.46155876
		 0.19305038;
	setAttr ".uvst[0].uvsp[250:451]" 0.46155876 1.4305115e-05 0.53844106 1.4305115e-05
		 0.81514406 0.61393738 0.97803807 0.61393738 0.97803807 0.92234707 0.81514406 0.92234707
		 0.61529374 0.67393637 0.77818775 0.67393637 0.77818775 0.98234606 0.61529374 0.98234606
		 0.57825851 -4.7683716e-07 0.74115252 -4.7683716e-07 0.74115252 0.30840921 0.57825851
		 0.30840921 0.72447264 0.056341648 0.88736653 0.056341648 0.88736653 0.36475134 0.72447264
		 0.36475134 0.83710611 0.31143713 1 0.31143713 1 0.6198473 0.83710611 0.6198473 0.18485588
		 0.61393738 0.18485588 0.92234707 0.021961987 0.92234707 0.021961987 0.61393738 0.3847062
		 0.67393637 0.3847062 0.98234606 0.22181219 0.98234606 0.22181219 0.67393637 0.42174155
		 -4.7683716e-07 0.42174155 0.30840921 0.25884753 0.30840921 0.25884753 -4.7683716e-07
		 0.2755273 0.056341648 0.2755273 0.36475134 0.11263341 0.36475134 0.11263341 0.056341648
		 0.16289389 0.31143713 0.16289389 0.6198473 0 0.6198473 0 0.31143713 0.58150709 0.31720018
		 0.41849291 0.31720018 0.41849291 0.008790493 0.58150709 0.008790493 0.58150339 0.99999952
		 0.41849655 0.99999952 0.41849655 0.69158983 0.58150339 0.69158983 0.58409154 0.021702051
		 0.80432129 0.021702051 0.80432129 0.19981456 0.58409154 0.19981456 0.77977037 0.11864352
		 1.000000238419 0.11864352 1.000000238419 0.29675555 0.77977037 0.29675555 0.41590869
		 0.021702051 0.41590869 0.19981456 0.19567901 0.19981456 0.19567901 0.021702051 0.2202298
		 0.11864352 0.2202298 0.29675555 5.9604645e-08 0.29675555 5.9604645e-08 0.11864352
		 0.61019063 0.31278157 0.38980961 0.31278157 0.38980961 0.13466907 0.61019063 0.13466907
		 0.61213601 0.99999976 0.38786423 0.99999976 0.38786423 0.82188725 0.61213601 0.82188725
		 0.61019468 0.17811227 0.38980556 0.17811227 0.38980556 -2.3841858e-07 0.61019468
		 -2.3841858e-07 0.86678052 0.66543388 0.9988538 0.66543388 0.9988538 1 0.86678052
		 1 0.86792684 0.17166138 1 0.17166138 1 0.50622749 0.86792684 0.50622749 0.13321942
		 0.66543388 0.13321942 1 0.0011461973 1 0.0011461973 0.66543388 0.13207316 0.17166138
		 0.13207316 0.50622749 0 0.50622749 0 0.17166138 0.56842685 0.97839069 0.43157309
		 0.97839069 0.43157309 0.64382458 0.56842685 0.64382458 0.56750739 0.33456612 0.43249267
		 0.33456612 0.43249267 0 0.56750739 0 0.00022017956 0.87534904 0.99987781 0.87534904
		 0.99987781 1 0.00022017956 1 0.00012457371 0.49865538 0.9997822 0.49865538 0.9997822
		 0.62330645 0.00012457371 0.62330645 0.00012862682 0 0.99978709 0 0.99978709 0.12465107
		 0.00012862682 0.12465107 0.00034230947 0.69159102 1 0.69159102 1 0.8162421 0.00034230947
		 0.8162421 -2.9802322e-08 0.27214992 0.99965823 0.27214992 0.99965823 0.39680099 -2.9802322e-08
		 0.39680099 0.8668592 0.77725697 0.99999988 0.77725697 0.99999988 1 0.8668592 1 0.71527243
		 0 0.84841335 0 0.84841335 0.2227428 0.71527243 0.2227428 0.13314074 0.77725697 0.13314074
		 1 -2.9802322e-08 1 -2.9802322e-08 0.77725697 0.28472745 0 0.28472745 0.2227428 0.15158653
		 0.2227428 0.15158653 0 0.86279559 0.8803668 0.92983127 0.8803668 0.92983127 1 0.86279559
		 1 0.85223234 0.64094114 0.91926801 0.64094114 0.91926801 0.76057434 0.85223234 0.76057434
		 0.83829582 0.37113124 0.90533149 0.37113124 0.90533149 0.49076444 0.83829582 0.49076444
		 0.75528872 0.021046817 0.8223244 0.021046817 0.8223244 0.14068002 0.75528872 0.14068002
		 0.93296432 -5.9604645e-08 0.99999988 -5.9604645e-08 0.99999988 0.11963314 0.93296432
		 0.11963314 0.13720429 0.8803668 0.13720429 1 0.070168674 1 0.070168674 0.8803668
		 0.14776754 0.64094114 0.14776754 0.76057434 0.080731869 0.76057434 0.080731869 0.64094114
		 0.16170406 0.37113124 0.16170406 0.49076444 0.094668388 0.49076444 0.094668388 0.37113124
		 0.24471116 0.021046817 0.24471116 0.14068002 0.17767549 0.14068002 0.17767549 0.021046817
		 0.067035615 -5.9604645e-08 0.067035615 0.11963314 -2.9802322e-08 0.11963314 -2.9802322e-08
		 -5.9604645e-08 0.74116969 0.34214211 0.82525086 0.34214211 0.82525086 1 0.74116969
		 1 0.59015477 0 0.67423594 0 0.67423594 0.6578598 0.59015477 0.6578598 0.91591883
		 0.2918663 0.99999988 0.2918663 0.99999988 0.9497261 0.91591883 0.9497261 0.25883019
		 0.34214211 0.25883019 1 0.17474908 1 0.17474908 0.34214211 0.40984511 0 0.40984511
		 0.6578598 0.32576394 0.6578598 0.32576394 0 0.084081113 0.2918663 0.084081113 0.9497261
		 -2.9802322e-08 0.9497261 -2.9802322e-08 0.2918663;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 452 ".vt";
	setAttr ".vt[0:165]"  0.19371808 11.21143436 4.58365107 0.19371808 11.59783459 4.58365107
		 0.23106143 11.10812378 4.56689167 0.61746156 11.10812378 4.56689167 0.23106137 11.494524 4.56689167
		 0.6174615 11.494524 4.56689167 1.12642717 11.39643383 4.36986685 1.51282716 11.39643383 4.36986685
		 1.12642717 11.78283405 4.36986685 1.51282716 11.78283405 4.36986685 2.1004374 11.51489925 3.18370891
		 2.48683763 11.51489925 3.18370891 2.1004374 11.90129948 3.18370891 2.48683763 11.90129948 3.18370891
		 -0.19371808 11.21143436 4.58365107 -0.19371808 11.59783459 4.58365107 -0.23106143 11.10812378 4.56689167
		 -0.61746156 11.10812378 4.56689167 -0.23106137 11.494524 4.56689167 -0.6174615 11.494524 4.56689167
		 -1.12642717 11.39643383 4.36986685 -1.51282716 11.39643383 4.36986685 -1.12642717 11.78283405 4.36986685
		 -1.51282716 11.78283405 4.36986685 -2.1004374 11.51489925 3.18370891 -2.48683763 11.51489925 3.18370891
		 -2.1004374 11.90129948 3.18370891 -2.48683763 11.90129948 3.18370891 0.89198852 10.25975895 3.95996666
		 1.27838862 10.25975895 3.95996666 0.89198852 10.64615917 3.95996666 1.27838862 10.64615917 3.95996666
		 1.2436372 10.24388981 3.86620617 1.63003731 10.24388981 3.86620617 1.2436372 10.63029003 3.86620617
		 1.63003731 10.63029003 3.86620617 1.52633679 10.3243227 3.70727611 1.91273701 10.3243227 3.70727611
		 1.52633679 10.71072292 3.70727611 1.91273701 10.71072292 3.70727611 -0.89198852 10.25975895 3.95996666
		 -1.27838862 10.25975895 3.95996666 -0.89198852 10.64615917 3.95996666 -1.27838862 10.64615917 3.95996666
		 -1.2436372 10.24388981 3.86620617 -1.63003731 10.24388981 3.86620617 -1.2436372 10.63029003 3.86620617
		 -1.63003731 10.63029003 3.86620617 -1.52633679 10.3243227 3.70727611 -1.91273701 10.3243227 3.70727611
		 -1.52633679 10.71072292 3.70727611 -1.91273701 10.71072292 3.70727611 2.29549932 11.18450069 2.081173658
		 2.68189955 11.18450069 2.081173658 2.29549932 11.57090092 2.081173658 2.68189955 11.57090092 2.081173658
		 0.2922461 10.28654289 4.091270924 0.67864621 10.28654289 4.091270924 0.2922461 10.67294312 4.091270924
		 0.67864621 10.67294312 4.091270924 2.13614917 10.11901474 2.87536716 2.52254915 10.11901474 2.87536716
		 2.13614917 10.50541496 2.87536716 2.52254915 10.50541496 2.87536716 0.95517552 9.61846924 3.98405671
		 1.34157562 9.61846924 3.98405671 0.95517552 10.0048694611 3.98405671 1.34157562 10.0048694611 3.98405671
		 1.82429874 9.72488022 3.47359967 2.21069908 9.72488022 3.47359967 1.82429874 10.11128044 3.47359967
		 2.21069908 10.11128044 3.47359967 2.18157744 10.75324821 2.56306934 2.56797743 10.75324821 2.56306934
		 2.18157744 11.13964844 2.56306934 2.56797743 11.13964844 2.56306934 -2.29549932 11.18450069 2.081173658
		 -2.68189955 11.18450069 2.081173658 -2.29549932 11.57090092 2.081173658 -2.68189955 11.57090092 2.081173658
		 -0.2922461 10.28654289 4.091270924 -0.67864621 10.28654289 4.091270924 -0.2922461 10.67294312 4.091270924
		 -0.67864621 10.67294312 4.091270924 -2.13614917 10.11901474 2.87536716 -2.52254915 10.11901474 2.87536716
		 -2.13614917 10.50541496 2.87536716 -2.52254915 10.50541496 2.87536716 -0.95517552 9.61846924 3.98405671
		 -1.34157562 9.61846924 3.98405671 -0.95517552 10.0048694611 3.98405671 -1.34157562 10.0048694611 3.98405671
		 -1.82429874 9.72488022 3.47359967 -2.21069908 9.72488022 3.47359967 -1.82429874 10.11128044 3.47359967
		 -2.21069908 10.11128044 3.47359967 -2.18157744 10.75324821 2.56306934 -2.56797743 10.75324821 2.56306934
		 -2.18157744 11.13964844 2.56306934 -2.56797743 11.13964844 2.56306934 1.32150531 8.93315125 3.7214303
		 1.70790553 8.93315125 3.7214303 1.32150531 9.31955147 3.7214303 1.70790553 9.31955147 3.7214303
		 1.82488203 9.16024971 3.15465593 2.21128225 9.16024971 3.15465593 1.82488203 9.54664993 3.15465593
		 2.21128225 9.54664993 3.15465593 2.27569556 9.64241695 2.28028393 2.66209579 9.64241695 2.28028393
		 2.27569556 10.028817177 2.28028393 2.66209579 10.028817177 2.28028393 -1.32150531 8.93315125 3.7214303
		 -1.70790553 8.93315125 3.7214303 -1.32150531 9.31955147 3.7214303 -1.70790553 9.31955147 3.7214303
		 -1.82488203 9.16024971 3.15465593 -2.21128225 9.16024971 3.15465593 -1.82488203 9.54664993 3.15465593
		 -2.21128225 9.54664993 3.15465593 -2.27569556 9.64241695 2.28028393 -2.66209579 9.64241695 2.28028393
		 -2.27569556 10.028817177 2.28028393 -2.66209579 10.028817177 2.28028393 1.58897114 7.97185516 2.77455592
		 1.97537136 7.97185516 2.77455592 1.58897114 8.35825539 2.77455592 1.97537136 8.35825539 2.77455592
		 2.066412687 8.34551334 1.99803543 2.45281291 8.34551334 1.99803543 2.066412687 8.73191357 1.99803543
		 2.45281291 8.73191357 1.99803543 2.29216361 8.75875378 1.15913916 2.67856383 8.75875378 1.15913916
		 2.29216361 9.145154 1.15913916 2.67856383 9.145154 1.15913916 -1.58897114 7.97185516 2.77455592
		 -1.97537136 7.97185516 2.77455592 -1.58897114 8.35825539 2.77455592 -1.97537136 8.35825539 2.77455592
		 -2.066412687 8.34551334 1.99803543 -2.45281291 8.34551334 1.99803543 -2.066412687 8.73191357 1.99803543
		 -2.45281291 8.73191357 1.99803543 -2.29216361 8.75875378 1.15913916 -2.67856383 8.75875378 1.15913916
		 -2.29216361 9.145154 1.15913916 -2.67856383 9.145154 1.15913916 0.19335288 7.17070961 4.017320633
		 0.19335288 7.55710983 4.017320633 0.69016916 7.25559378 3.69046354 1.076569319 7.25559378 3.69046354
		 0.69016916 7.641994 3.69046354 1.076569319 7.641994 3.69046354 0.40155536 7.17745113 3.85999751
		 0.78795558 7.17745113 3.85999751 0.40155533 7.56385136 3.85999751 0.78795558 7.56385136 3.85999751
		 0.78613305 8.95426846 4.029087067 1.17253304 8.95426846 4.029087067 0.78613305 9.34066868 4.029087067
		 1.17253304 9.34066868 4.029087067 0.91568041 7.4846406 3.57041836 1.30208063 7.4846406 3.57041836
		 0.91568041 7.87104082 3.57041836 1.30208063 7.87104082 3.57041836;
	setAttr ".vt[166:331]" 0.36477876 9.39461994 4.40039253 0.75117874 9.39461994 4.40039253
		 0.36477876 9.78102016 4.40039253 0.75117874 9.78102016 4.40039253 1.16594505 8.087018967 3.59421587
		 1.55234528 8.087018967 3.59421587 1.16594505 8.47341919 3.59421587 1.55234528 8.47341919 3.59421587
		 0.11544472 7.17071724 3.97461462 0.50184494 7.17071724 3.97461462 0.11544472 7.55711746 3.97461462
		 0.50184494 7.55711746 3.97461462 -0.193353 7.17070961 4.017320633 -0.193353 7.55710983 4.017320633
		 -0.69016916 7.25559378 3.69046354 -1.076569319 7.25559378 3.69046354 -0.69016916 7.641994 3.69046354
		 -1.076569319 7.641994 3.69046354 -0.40155536 7.17745113 3.85999751 -0.78795558 7.17745113 3.85999751
		 -0.40155539 7.56385136 3.85999751 -0.78795558 7.56385136 3.85999751 -0.78613305 8.95426846 4.029087067
		 -1.17253304 8.95426846 4.029087067 -0.78613305 9.34066868 4.029087067 -1.17253304 9.34066868 4.029087067
		 -0.91568041 7.4846406 3.57041836 -1.30208063 7.4846406 3.57041836 -0.91568041 7.87104082 3.57041836
		 -1.30208063 7.87104082 3.57041836 -0.36477876 9.39461994 4.40039253 -0.75117874 9.39461994 4.40039253
		 -0.36477879 9.78102016 4.40039253 -0.75117874 9.78102016 4.40039253 -1.16594505 8.087018967 3.59421587
		 -1.55234528 8.087018967 3.59421587 -1.16594505 8.47341919 3.59421587 -1.55234528 8.47341919 3.59421587
		 -0.11544472 7.17071724 3.97461462 -0.50184494 7.17071724 3.97461462 -0.11544474 7.55711746 3.97461462
		 -0.50184494 7.55711746 3.97461462 0.19333392 6.40701008 3.98384261 0.19333392 6.7934103 3.98384261
		 0.93467879 6.71683025 3.18136597 1.32107878 6.71683025 3.18136597 0.93467879 7.10323048 3.18136597
		 1.32107878 7.10323048 3.18136597 1.82266414 7.49680853 1.87655044 2.20906448 7.49680853 1.87655044
		 1.82266414 7.88320875 1.87655044 2.20906448 7.88320875 1.87655044 0.25925887 6.40698147 3.91733241
		 0.64565873 6.40698147 3.91733241 0.25925878 6.79338169 3.91733241 0.64565873 6.79338169 3.91733241
		 1.40536714 7.08535862 2.6469698 1.79176736 7.08535862 2.6469698 1.40536714 7.47175837 2.6469698
		 1.79176736 7.47175837 2.6469698 2.12827349 8.022279739 0.95036954 2.51467371 8.022279739 0.95036954
		 2.12827349 8.40867996 0.95036954 2.51467371 8.40867996 0.95036954 -0.19333395 6.40701008 3.98384261
		 -0.19333395 6.7934103 3.98384261 -0.93467879 6.71683025 3.18136597 -1.32107878 6.71683025 3.18136597
		 -0.93467879 7.10323048 3.18136597 -1.32107878 7.10323048 3.18136597 -1.82266414 7.49680853 1.87655044
		 -2.20906448 7.49680853 1.87655044 -1.82266414 7.88320875 1.87655044 -2.20906448 7.88320875 1.87655044
		 -0.25925878 6.40698147 3.91733241 -0.64565873 6.40698147 3.91733241 -0.25925878 6.79338169 3.91733241
		 -0.64565873 6.79338169 3.91733241 -1.40536714 7.08535862 2.6469698 -1.79176736 7.08535862 2.6469698
		 -1.40536714 7.47175837 2.6469698 -1.79176736 7.47175837 2.6469698 -2.12827349 8.022279739 0.95036954
		 -2.51467371 8.022279739 0.95036954 -2.12827349 8.40867996 0.95036954 -2.51467371 8.40867996 0.95036954
		 0.74755168 8.27432823 3.94066405 1.13395143 8.27432823 3.94066405 0.74755168 8.66072845 3.94066405
		 1.13395143 8.66072845 3.94066405 0.19334245 7.51615238 4.18528414 0.19334245 7.9025526 4.18528414
		 0.27348781 8.3494997 4.25924301 0.65988779 8.3494997 4.25924301 0.27348781 8.73589993 4.25924301
		 0.65988779 8.73589993 4.25924301 0.18563652 7.5051384 4.099388599 0.5720365 7.5051384 4.099388599
		 0.18563652 7.89153862 4.099388599 0.5720365 7.89153862 4.099388599 0.19333386 8.37161732 4.31395054
		 0.19333386 8.75801754 4.31395054 0.53247046 7.57572842 3.9046979 0.91887021 7.57572842 3.9046979
		 0.53247046 7.96212864 3.9046979 0.91887021 7.96212864 3.9046979 0.79964757 7.89533234 3.72721148
		 1.18604732 7.89533234 3.72721148 0.79964757 8.28173256 3.72721148 1.18604732 8.28173256 3.72721148
		 -0.74755168 8.27432823 3.94066405 -1.13395143 8.27432823 3.94066405 -0.74755168 8.66072845 3.94066405
		 -1.13395143 8.66072845 3.94066405 -0.19334245 7.51615238 4.18528414 -0.19334245 7.9025526 4.18528414
		 -0.27348781 8.3494997 4.25924301 -0.65988779 8.3494997 4.25924301 -0.27348781 8.73589993 4.25924301
		 -0.65988779 8.73589993 4.25924301 -0.18563652 7.5051384 4.099388599 -0.5720365 7.5051384 4.099388599
		 -0.18563652 7.89153862 4.099388599 -0.5720365 7.89153862 4.099388599 -0.19333386 8.37161732 4.31395054
		 -0.19333386 8.75801754 4.31395054 -0.53247046 7.57572842 3.9046979 -0.91887021 7.57572842 3.9046979
		 -0.53247046 7.96212864 3.9046979 -0.91887021 7.96212864 3.9046979 -0.79964757 7.89533234 3.72721148
		 -1.18604732 7.89533234 3.72721148 -0.79964757 8.28173256 3.72721148 -1.18604732 8.28173256 3.72721148
		 0.19333279 9.00088977814 4.9873991 0.19333279 9.38729 4.9873991 0.19674611 10.49175358 4.41661406
		 0.19674611 10.8781538 4.41661406 0.19334 8.70873642 4.35929441 0.19334 9.095136642 4.35929441
		 0.14754111 8.75581741 4.2669735 0.53394133 8.75581741 4.2669735 0.14754111 9.14221764 4.2669735
		 0.53394133 9.14221764 4.2669735 0.49086612 8.96612358 4.1463995 0.87726635 8.96612358 4.1463995
		 0.49086612 9.3525238 4.1463995 0.87726635 9.3525238 4.1463995 -0.19333279 9.00088977814 4.9873991
		 -0.19333279 9.38729 4.9873991 -0.19674614 10.49175358 4.41661406 -0.19674614 10.8781538 4.41661406
		 -0.19334 8.70873642 4.35929441 -0.19334 9.095136642 4.35929441 -0.14754111 8.75581741 4.2669735
		 -0.53394133 8.75581741 4.2669735 -0.14754111 9.14221764 4.2669735 -0.53394133 9.14221764 4.2669735
		 -0.49086612 8.96612358 4.1463995 -0.87726635 8.96612358 4.1463995 -0.49086612 9.3525238 4.1463995
		 -0.87726635 9.3525238 4.1463995 1.073071599 12.62709332 4.1008544 1.45947158 12.62709332 4.1008544
		 1.073071599 13.013493538 4.1008544 1.45947158 13.013493538 4.1008544;
	setAttr ".vt[332:451]" 1.076425076 12.056821823 4.24307823 1.46282506 12.056821823 4.24307823
		 1.076425076 12.44322205 4.24307823 1.46282506 12.44322205 4.24307823 0.20019317 12.60213661 4.38196802
		 0.20019317 12.98853683 4.38196802 0.19750285 11.85856533 4.4915657 0.19750285 12.24496555 4.4915657
		 -1.073071599 12.62709332 4.1008544 -1.45947158 12.62709332 4.1008544 -1.073071599 13.013493538 4.1008544
		 -1.45947158 13.013493538 4.1008544 -1.076425076 12.056821823 4.24307823 -1.46282506 12.056821823 4.24307823
		 -1.076425076 12.44322205 4.24307823 -1.46282506 12.44322205 4.24307823 -0.20019317 12.60213661 4.38196802
		 -0.20019317 12.98853683 4.38196802 -0.19750285 11.85856533 4.4915657 -0.19750285 12.24496555 4.4915657
		 -0.19299471 6.243186 2.28020906 0.19340527 6.243186 2.28020906 -0.19299471 6.62958622 2.28020906
		 0.19340527 6.62958622 2.28020906 -0.19303167 5.43668938 1.59641552 0.19336832 5.43668938 1.59641552
		 -0.19303167 5.8230896 1.59641552 0.19336832 5.8230896 1.59641552 -0.19303012 3.52973175 1.36870742
		 0.19337022 3.52973175 1.36870742 -0.19303012 3.91613197 1.36870742 0.19337022 3.91613197 1.36870742
		 -0.19294751 6.052821636 1.78529477 0.19345248 6.052821636 1.78529477 -0.19294751 6.43922186 1.78529477
		 0.19345248 6.43922186 1.78529477 -0.19307983 4.37335682 1.240273 0.19332039 4.37335682 1.240273
		 -0.19307983 4.75975704 1.240273 0.19332039 4.75975704 1.240273 1.064694881 6.82397699 1.49578583
		 1.45109463 6.82397699 1.49578583 1.064694881 7.21037722 1.49578583 1.45109463 7.21037722 1.49578583
		 0.62476158 5.47564077 1.260028 1.011161804 5.47564077 1.260028 0.62476158 5.862041 1.260028
		 1.011161804 5.862041 1.260028 -1.064694881 6.82397699 1.49578583 -1.45109463 6.82397699 1.49578583
		 -1.064694881 7.21037722 1.49578583 -1.45109463 7.21037722 1.49578583 -0.62476158 5.47564077 1.260028
		 -1.011161804 5.47564077 1.260028 -0.62476158 5.862041 1.260028 -1.011161804 5.862041 1.260028
		 2.091187954 7.068972588 0.20060849 2.4775877 7.068972588 0.20060849 2.091187954 7.45537281 0.20060849
		 2.4775877 7.45537281 0.20060849 2.030300617 6.29565811 0.40176344 2.41670036 6.29565811 0.40176344
		 2.030300617 6.68205833 0.40176344 2.41670036 6.68205833 0.40176344 1.94996929 5.42420626 0.64830494
		 2.33636904 5.42420626 0.64830494 1.94996929 5.81060648 0.64830494 2.33636904 5.81060648 0.64830494
		 1.4715085 4.29347754 1.026381493 1.85790825 4.29347754 1.026381493 1.4715085 4.67987776 1.026381493
		 1.85790825 4.67987776 1.026381493 2.49564695 4.22549868 0.00033473969 2.8820467 4.22549868 0.00033473969
		 2.49564695 4.6118989 0.00033473969 2.8820467 4.6118989 0.00033473969 -2.091187954 7.068972588 0.20060849
		 -2.4775877 7.068972588 0.20060849 -2.091187954 7.45537281 0.20060849 -2.4775877 7.45537281 0.20060849
		 -2.030300617 6.29565811 0.40176344 -2.41670036 6.29565811 0.40176344 -2.030300617 6.68205833 0.40176344
		 -2.41670036 6.68205833 0.40176344 -1.94996929 5.42420626 0.64830494 -2.33636904 5.42420626 0.64830494
		 -1.94996929 5.81060648 0.64830494 -2.33636904 5.81060648 0.64830494 -1.4715085 4.29347754 1.026381493
		 -1.85790825 4.29347754 1.026381493 -1.4715085 4.67987776 1.026381493 -1.85790825 4.67987776 1.026381493
		 -2.49564695 4.22549868 0.00033473969 -2.8820467 4.22549868 0.00033473969 -2.49564695 4.6118989 0.00033473969
		 -2.8820467 4.6118989 0.00033473969 1.10831046 10.95543003 4.11283207 1.49471068 10.95543003 4.11283207
		 1.10831046 11.34183025 4.11283207 1.49471068 11.34183025 4.11283207 0.41431224 10.75446987 4.148417
		 0.80071235 10.75446987 4.148417 0.41431224 11.14087009 4.148417 0.80071235 11.14087009 4.148417
		 1.91138089 10.92590046 3.36608362 2.29778099 10.92590046 3.36608362 1.91138089 11.31230068 3.36608362
		 2.29778099 11.31230068 3.36608362 -1.10831046 10.95543003 4.11283207 -1.49471068 10.95543003 4.11283207
		 -1.10831046 11.34183025 4.11283207 -1.49471068 11.34183025 4.11283207 -0.41431224 10.75446987 4.148417
		 -0.80071235 10.75446987 4.148417 -0.41431224 11.14087009 4.148417 -0.80071235 11.14087009 4.148417
		 -1.91138089 10.92590046 3.36608362 -2.29778099 10.92590046 3.36608362 -1.91138089 11.31230068 3.36608362
		 -2.29778099 11.31230068 3.36608362;
	setAttr -s 452 ".ed";
	setAttr ".ed[0:165]"  0 1 0 2 3 0 2 4 0 3 5 0 4 5 0 6 7 0 6 8 0 7 9 0 8 9 0
		 10 11 0 10 12 0 11 13 0 12 13 0 14 0 0 16 17 0 17 19 0 18 19 0 16 18 0 20 21 0 21 23 0
		 22 23 0 20 22 0 24 25 0 25 27 0 26 27 0 24 26 0 14 15 0 1 15 0 28 29 0 28 30 0 29 31 0
		 30 31 0 32 33 0 32 34 0 33 35 0 34 35 0 36 37 0 36 38 0 37 39 0 38 39 0 40 41 0 41 43 0
		 42 43 0 40 42 0 44 45 0 45 47 0 46 47 0 44 46 0 48 49 0 49 51 0 50 51 0 48 50 0 52 53 0
		 52 54 0 53 55 0 54 55 0 56 57 0 56 58 0 57 59 0 58 59 0 60 61 0 60 62 0 61 63 0 62 63 0
		 64 65 0 64 66 0 65 67 0 66 67 0 68 69 0 68 70 0 69 71 0 70 71 0 72 73 0 72 74 0 73 75 0
		 74 75 0 76 77 0 77 79 0 78 79 0 76 78 0 80 81 0 81 83 0 82 83 0 80 82 0 84 85 0 85 87 0
		 86 87 0 84 86 0 88 89 0 89 91 0 90 91 0 88 90 0 92 93 0 93 95 0 94 95 0 92 94 0 96 97 0
		 97 99 0 98 99 0 96 98 0 100 101 0 100 102 0 101 103 0 102 103 0 104 105 0 104 106 0
		 105 107 0 106 107 0 108 109 0 108 110 0 109 111 0 110 111 0 112 113 0 113 115 0 114 115 0
		 112 114 0 116 117 0 117 119 0 118 119 0 116 118 0 120 121 0 121 123 0 122 123 0 120 122 0
		 124 125 0 124 126 0 125 127 0 126 127 0 128 129 0 128 130 0 129 131 0 130 131 0 132 133 0
		 132 134 0 133 135 0 134 135 0 136 137 0 137 139 0 138 139 0 136 138 0 140 141 0 141 143 0
		 142 143 0 140 142 0 144 145 0 145 147 0 146 147 0 144 146 0 148 149 0 150 151 0 150 152 0
		 151 153 0 152 153 0 154 155 0 154 156 0 155 157 0 156 157 0 158 159 0 158 160 0 159 161 0
		 160 161 0 162 163 0 162 164 0 163 165 0 164 165 0 166 167 0;
	setAttr ".ed[166:331]" 166 168 0 167 169 0 168 169 0 170 171 0 170 172 0 171 173 0
		 172 173 0 174 175 0 174 176 0 175 177 0 176 177 0 178 148 0 180 181 0 181 183 0 182 183 0
		 180 182 0 184 185 0 185 187 0 186 187 0 184 186 0 188 189 0 189 191 0 190 191 0 188 190 0
		 192 193 0 193 195 0 194 195 0 192 194 0 196 197 0 197 199 0 198 199 0 196 198 0 200 201 0
		 201 203 0 202 203 0 200 202 0 204 205 0 205 207 0 206 207 0 204 206 0 178 179 0 149 179 0
		 208 209 0 210 211 0 210 212 0 211 213 0 212 213 0 214 215 0 214 216 0 215 217 0 216 217 0
		 218 219 0 218 220 0 219 221 0 220 221 0 222 223 0 222 224 0 223 225 0 224 225 0 226 227 0
		 226 228 0 227 229 0 228 229 0 230 208 0 232 233 0 233 235 0 234 235 0 232 234 0 236 237 0
		 237 239 0 238 239 0 236 238 0 240 241 0 241 243 0 242 243 0 240 242 0 244 245 0 245 247 0
		 246 247 0 244 246 0 248 249 0 249 251 0 250 251 0 248 250 0 230 231 0 209 231 0 252 253 0
		 252 254 0 253 255 0 254 255 0 256 257 0 258 259 0 258 260 0 259 261 0 260 261 0 262 263 0
		 262 264 0 263 265 0 264 265 0 266 267 0 268 269 0 268 270 0 269 271 0 270 271 0 272 273 0
		 272 274 0 273 275 0 274 275 0 280 256 0 290 266 0 276 277 0 277 279 0 278 279 0 276 278 0
		 282 283 0 283 285 0 284 285 0 282 284 0 286 287 0 287 289 0 288 289 0 286 288 0 292 293 0
		 293 295 0 294 295 0 292 294 0 296 297 0 297 299 0 298 299 0 296 298 0 280 281 0 257 281 0
		 290 291 0 267 291 0 300 301 0 302 303 0 304 305 0 306 307 0 306 308 0 307 309 0 308 309 0
		 310 311 0 310 312 0 311 313 0 312 313 0 314 300 0 316 302 0 318 304 0 320 321 0 321 323 0
		 322 323 0 320 322 0 324 325 0 325 327 0 326 327 0 324 326 0 314 315 0 301 315 0 316 317 0
		 303 317 0 318 319 0 305 319 0 328 329 0 328 330 0 329 331 0 330 331 0;
	setAttr ".ed[332:451]" 332 333 0 332 334 0 333 335 0 334 335 0 336 337 0 338 339 0
		 348 336 0 350 338 0 340 341 0 341 343 0 342 343 0 340 342 0 344 345 0 345 347 0 346 347 0
		 344 346 0 348 349 0 337 349 0 350 351 0 339 351 0 352 353 0 352 354 0 353 355 0 354 355 0
		 356 357 0 356 358 0 357 359 0 358 359 0 360 361 0 360 362 0 361 363 0 362 363 0 364 365 0
		 364 366 0 365 367 0 366 367 0 368 369 0 368 370 0 369 371 0 370 371 0 372 373 0 372 374 0
		 373 375 0 374 375 0 376 377 0 376 378 0 377 379 0 378 379 0 380 381 0 381 383 0 382 383 0
		 380 382 0 384 385 0 385 387 0 386 387 0 384 386 0 388 389 0 388 390 0 389 391 0 390 391 0
		 392 393 0 392 394 0 393 395 0 394 395 0 396 397 0 396 398 0 397 399 0 398 399 0 400 401 0
		 400 402 0 401 403 0 402 403 0 404 405 0 404 406 0 405 407 0 406 407 0 408 409 0 409 411 0
		 410 411 0 408 410 0 412 413 0 413 415 0 414 415 0 412 414 0 416 417 0 417 419 0 418 419 0
		 416 418 0 420 421 0 421 423 0 422 423 0 420 422 0 424 425 0 425 427 0 426 427 0 424 426 0
		 428 429 0 428 430 0 429 431 0 430 431 0 432 433 0 432 434 0 433 435 0 434 435 0 436 437 0
		 436 438 0 437 439 0 438 439 0 440 441 0 441 443 0 442 443 0 440 442 0 444 445 0 445 447 0
		 446 447 0 444 446 0 448 449 0 449 451 0 450 451 0 448 450 0;
	setAttr -s 113 -ch 452 ".fc[0:112]" -type "polyFaces" 
		f 4 1 3 -5 -3
		mu 0 4 0 1 2 3
		f 4 5 7 -9 -7
		mu 0 4 4 5 6 7
		f 4 9 11 -13 -11
		mu 0 4 8 9 10 11
		f 4 17 16 -16 -15
		mu 0 4 12 13 14 15
		f 4 21 20 -20 -19
		mu 0 4 16 17 18 19
		f 4 25 24 -24 -23
		mu 0 4 20 21 22 23
		f 4 27 -27 13 0
		mu 0 4 24 25 26 27
		f 4 28 30 -32 -30
		mu 0 4 28 29 30 31
		f 4 32 34 -36 -34
		mu 0 4 32 33 34 35
		f 4 36 38 -40 -38
		mu 0 4 36 37 38 39
		f 4 43 42 -42 -41
		mu 0 4 40 41 42 43
		f 4 47 46 -46 -45
		mu 0 4 44 45 46 47
		f 4 51 50 -50 -49
		mu 0 4 48 49 50 51
		f 4 52 54 -56 -54
		mu 0 4 52 53 54 55
		f 4 56 58 -60 -58
		mu 0 4 56 57 58 59
		f 4 60 62 -64 -62
		mu 0 4 60 61 62 63
		f 4 64 66 -68 -66
		mu 0 4 64 65 66 67
		f 4 68 70 -72 -70
		mu 0 4 68 69 70 71
		f 4 72 74 -76 -74
		mu 0 4 72 73 74 75
		f 4 79 78 -78 -77
		mu 0 4 76 77 78 79
		f 4 83 82 -82 -81
		mu 0 4 80 81 82 83
		f 4 87 86 -86 -85
		mu 0 4 84 85 86 87
		f 4 91 90 -90 -89
		mu 0 4 88 89 90 91
		f 4 95 94 -94 -93
		mu 0 4 92 93 94 95
		f 4 99 98 -98 -97
		mu 0 4 96 97 98 99
		f 4 100 102 -104 -102
		mu 0 4 100 101 102 103
		f 4 104 106 -108 -106
		mu 0 4 104 105 106 107
		f 4 108 110 -112 -110
		mu 0 4 108 109 110 111
		f 4 115 114 -114 -113
		mu 0 4 112 113 114 115
		f 4 119 118 -118 -117
		mu 0 4 116 117 118 119
		f 4 123 122 -122 -121
		mu 0 4 120 121 122 123
		f 4 124 126 -128 -126
		mu 0 4 124 125 126 127
		f 4 128 130 -132 -130
		mu 0 4 128 129 130 131
		f 4 132 134 -136 -134
		mu 0 4 132 133 134 135
		f 4 139 138 -138 -137
		mu 0 4 136 137 138 139
		f 4 143 142 -142 -141
		mu 0 4 140 141 142 143
		f 4 147 146 -146 -145
		mu 0 4 144 145 146 147
		f 4 149 151 -153 -151
		mu 0 4 148 149 150 151
		f 4 153 155 -157 -155
		mu 0 4 152 153 154 155
		f 4 157 159 -161 -159
		mu 0 4 156 157 158 159
		f 4 161 163 -165 -163
		mu 0 4 160 161 162 163
		f 4 165 167 -169 -167
		mu 0 4 164 165 166 167
		f 4 169 171 -173 -171
		mu 0 4 168 169 170 171
		f 4 173 175 -177 -175
		mu 0 4 172 173 174 175
		f 4 181 180 -180 -179
		mu 0 4 176 177 178 179
		f 4 185 184 -184 -183
		mu 0 4 180 181 182 183
		f 4 189 188 -188 -187
		mu 0 4 184 185 186 187
		f 4 193 192 -192 -191
		mu 0 4 188 189 190 191
		f 4 197 196 -196 -195
		mu 0 4 192 193 194 195
		f 4 201 200 -200 -199
		mu 0 4 196 197 198 199
		f 4 205 204 -204 -203
		mu 0 4 200 201 202 203
		f 4 207 -207 177 148
		mu 0 4 204 205 206 207
		f 4 209 211 -213 -211
		mu 0 4 208 209 210 211
		f 4 213 215 -217 -215
		mu 0 4 212 213 214 215
		f 4 217 219 -221 -219
		mu 0 4 216 217 218 219
		f 4 221 223 -225 -223
		mu 0 4 220 221 222 223
		f 4 225 227 -229 -227
		mu 0 4 224 225 226 227
		f 4 233 232 -232 -231
		mu 0 4 228 229 230 231
		f 4 237 236 -236 -235
		mu 0 4 232 233 234 235
		f 4 241 240 -240 -239
		mu 0 4 236 237 238 239
		f 4 245 244 -244 -243
		mu 0 4 240 241 242 243
		f 4 249 248 -248 -247
		mu 0 4 244 245 246 247
		f 4 251 -251 229 208
		mu 0 4 248 249 250 251
		f 4 252 254 -256 -254
		mu 0 4 252 253 254 255
		f 4 257 259 -261 -259
		mu 0 4 256 257 258 259
		f 4 261 263 -265 -263
		mu 0 4 260 261 262 263
		f 4 266 268 -270 -268
		mu 0 4 264 265 266 267
		f 4 270 272 -274 -272
		mu 0 4 268 269 270 271
		f 4 279 278 -278 -277
		mu 0 4 272 273 274 275
		f 4 283 282 -282 -281
		mu 0 4 276 277 278 279
		f 4 287 286 -286 -285
		mu 0 4 280 281 282 283
		f 4 291 290 -290 -289
		mu 0 4 284 285 286 287
		f 4 295 294 -294 -293
		mu 0 4 288 289 290 291
		f 4 297 -297 274 256
		mu 0 4 292 293 294 295
		f 4 299 -299 275 265
		mu 0 4 296 297 298 299
		f 4 303 305 -307 -305
		mu 0 4 300 301 302 303
		f 4 307 309 -311 -309
		mu 0 4 304 305 306 307
		f 4 317 316 -316 -315
		mu 0 4 308 309 310 311
		f 4 321 320 -320 -319
		mu 0 4 312 313 314 315
		f 4 323 -323 311 300
		mu 0 4 316 317 318 319
		f 4 325 -325 312 301
		mu 0 4 320 321 322 323
		f 4 327 -327 313 302
		mu 0 4 324 325 326 327
		f 4 328 330 -332 -330
		mu 0 4 328 329 330 331
		f 4 332 334 -336 -334
		mu 0 4 332 333 334 335
		f 4 343 342 -342 -341
		mu 0 4 336 337 338 339
		f 4 347 346 -346 -345
		mu 0 4 340 341 342 343
		f 4 349 -349 338 336
		mu 0 4 344 345 346 347
		f 4 351 -351 339 337
		mu 0 4 348 349 350 351
		f 4 352 354 -356 -354
		mu 0 4 352 353 354 355
		f 4 356 358 -360 -358
		mu 0 4 356 357 358 359
		f 4 360 362 -364 -362
		mu 0 4 360 361 362 363
		f 4 364 366 -368 -366
		mu 0 4 364 365 366 367
		f 4 368 370 -372 -370
		mu 0 4 368 369 370 371
		f 4 372 374 -376 -374
		mu 0 4 372 373 374 375
		f 4 376 378 -380 -378
		mu 0 4 376 377 378 379
		f 4 383 382 -382 -381
		mu 0 4 380 381 382 383
		f 4 387 386 -386 -385
		mu 0 4 384 385 386 387
		f 4 388 390 -392 -390
		mu 0 4 388 389 390 391
		f 4 392 394 -396 -394
		mu 0 4 392 393 394 395
		f 4 396 398 -400 -398
		mu 0 4 396 397 398 399
		f 4 400 402 -404 -402
		mu 0 4 400 401 402 403
		f 4 404 406 -408 -406
		mu 0 4 404 405 406 407
		f 4 411 410 -410 -409
		mu 0 4 408 409 410 411
		f 4 415 414 -414 -413
		mu 0 4 412 413 414 415
		f 4 419 418 -418 -417
		mu 0 4 416 417 418 419
		f 4 423 422 -422 -421
		mu 0 4 420 421 422 423
		f 4 427 426 -426 -425
		mu 0 4 424 425 426 427
		f 4 428 430 -432 -430
		mu 0 4 428 429 430 431
		f 4 432 434 -436 -434
		mu 0 4 432 433 434 435
		f 4 436 438 -440 -438
		mu 0 4 436 437 438 439
		f 4 443 442 -442 -441
		mu 0 4 440 441 442 443
		f 4 447 446 -446 -445
		mu 0 4 444 445 446 447
		f 4 451 450 -450 -449
		mu 0 4 448 449 450 451;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".vcs" 2;
createNode transform -n "facial_jnt_grp";
	rename -uid "9304C831-4550-B8CE-BF81-DDB518D77DDD";
	setAttr ".v" no;
createNode transform -n "brow_jnt_grp" -p "facial_jnt_grp";
	rename -uid "D82FD2B7-4464-A591-BBD9-5883F92E6EFB";
createNode joint -n "brow_C_001_jnt" -p "brow_jnt_grp";
	rename -uid "10FB9126-4936-AB03-D37F-8EBE7D2BC668";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.0005179278627931651 11.404634076679233 4.5836510780331858 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.015217286368026111 11.42551540350355 4.767289607677121 1;
	setAttr ".radi" 2;
createNode joint -n "brow_L_001_jnt" -p "brow_jnt_grp";
	rename -uid "E6DA5370-4FBD-6CC8-57D8-1299678B3356";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.42426148056983948 11.301323890686035 4.5668916702270508 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.32905290732474329 11.388248643367225 4.755526585692925 1;
	setAttr ".radi" 2;
createNode joint -n "brow_L_002_jnt" -p "brow_jnt_grp";
	rename -uid "950C059C-42DB-0FC4-1533-15AD6716F3B5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.3196271154966632 11.589633941650392 4.3698666511290511 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2171762821596754 11.352030313876407 4.4726077757385427 1;
	setAttr ".radi" 2;
createNode joint -n "brow_L_003_jnt" -p "brow_jnt_grp";
	rename -uid "D1BB36D1-4330-B32A-8889-F8B55894E72F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.2936375099999999 11.708099369999999 3.18370891 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.8930743733749877 11.30790412090303 3.9231012613081999 1;
	setAttr ".radi" 2;
createNode joint -n "brow_R_001_jnt" -p "brow_jnt_grp";
	rename -uid "36FC598C-4AF2-4382-4742-D9B9E0051786";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.424261 11.3013 4.566889999999999 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.32905290732474329 11.388248643367225 4.755526585692925 1;
	setAttr ".radi" 2;
createNode joint -n "brow_R_002_jnt" -p "brow_jnt_grp";
	rename -uid "0996BD26-4A79-23AD-FDCC-0192F78D6900";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.31963 11.5896 4.3698699999999988 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2171762821596754 11.352030313876407 4.4726077757385427 1;
	setAttr ".radi" 2;
createNode joint -n "brow_R_003_jnt" -p "brow_jnt_grp";
	rename -uid "73CC8E4C-49AA-3422-6C43-B99D7F4FFBA1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2936375099999999 11.708099369999999 3.18370891 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.8930743733749877 11.30790412090303 3.9231012613081999 1;
	setAttr ".radi" 2;
createNode transform -n "browLid_jnt_grp" -p "facial_jnt_grp";
	rename -uid "205B0626-417C-194B-3696-B8BCA75ADA7C";
createNode joint -n "browLid_L_001_jnt" -p "browLid_jnt_grp";
	rename -uid "CDCF4820-4529-A52E-D959-2CA9604974D8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.60751229524612427 10.947669982910156 4.1484169960021973 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.53922577858462739 10.957744192397966 4.1996023639549396 1;
	setAttr ".radi" 2;
createNode joint -n "browLid_L_002_jnt" -p "browLid_jnt_grp";
	rename -uid "9CDCB29F-4AF5-93FA-9CCB-C5B44AE0D3C6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.3015105428506657 11.148630142211914 4.1128321184325092 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.152633719583994 11.101710250422993 4.2783248411792476 1;
	setAttr ".radi" 2;
createNode joint -n "browLid_L_003_jnt" -p "browLid_jnt_grp";
	rename -uid "9A13C135-4E61-F5F8-99A9-9CA6C639E994";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.1045808799999999 11.119100570000001 3.3660836199999999 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.7660606302646811 10.963294904453122 3.849013645045424 1;
	setAttr ".radi" 2;
createNode joint -n "browLid_R_001_jnt" -p "browLid_jnt_grp";
	rename -uid "732D5E50-49FF-F76A-A3B7-FF9059B27082";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.607512 10.9477 4.1484199999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.53922577858462739 10.957744192397966 4.1996023639549396 1;
	setAttr ".radi" 2;
createNode joint -n "browLid_R_002_jnt" -p "browLid_jnt_grp";
	rename -uid "AE45FF5B-4253-BC1C-CDA4-188693301732";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.30151 11.1486 4.1128299999999989 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.152633719583994 11.101710250422993 4.2783248411792476 1;
	setAttr ".radi" 2;
createNode joint -n "browLid_R_003_jnt" -p "browLid_jnt_grp";
	rename -uid "BBC45F38-45AF-39D7-BF3D-16B464C5E26F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.1045808799999999 11.119100570000001 3.3660836199999999 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.7660606302646811 10.963294904453122 3.849013645045424 1;
	setAttr ".radi" 2;
createNode transform -n "lowlid_jnt_grp" -p "facial_jnt_grp";
	rename -uid "0A3EB503-48ED-9AEE-41D1-9C8457F090B3";
createNode joint -n "lowlid_L_001_jnt" -p "lowlid_jnt_grp";
	rename -uid "7ACB1F5F-4F8C-E520-1B39-44995138F935";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.0851883888244629 10.452959060668945 3.9599666595458984 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.83179619342196953 10.564083121602124 3.9646738660980141 1;
	setAttr ".radi" 2;
createNode joint -n "lowlid_L_002_jnt" -p "lowlid_jnt_grp";
	rename -uid "6331F268-46B6-DF36-B07F-B5B5871E306E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.4368371963500977 10.437089920043945 3.866206169128418 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.1244277213473133 10.503314363659349 3.9560938309036837 1;
	setAttr ".radi" 2;
createNode joint -n "lowlid_L_003_jnt" -p "lowlid_jnt_grp";
	rename -uid "8A2E1574-4C50-E77C-AC19-BA98CAAC681B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.7195367813110352 10.517522811889648 3.7072761058807373 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.4492364458666473 10.552784917984287 3.8542814969296404 1;
	setAttr ".radi" 2;
createNode joint -n "lowlid_R_001_jnt" -p "lowlid_jnt_grp";
	rename -uid "57076DC5-4B52-0411-33EE-12B6DB5AB4F1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.08519 10.453 3.9599699999999998 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.83179619342196953 10.564083121602124 3.9646738660980141 1;
	setAttr ".radi" 2;
createNode joint -n "lowlid_R_002_jnt" -p "lowlid_jnt_grp";
	rename -uid "C25AD20C-4B66-6D04-E24E-8ABE44CFD62C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.43684 10.4371 3.8662099999999997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.1244277213473133 10.503314363659349 3.9560938309036837 1;
	setAttr ".radi" 2;
createNode joint -n "lowlid_R_003_jnt" -p "lowlid_jnt_grp";
	rename -uid "5195BFD6-404B-A3AE-ABD7-B8A57F2B6473";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.71954 10.5175 3.7072799999999995 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.4492364458666473 10.552784917984287 3.8542814969296404 1;
	setAttr ".radi" 2;
createNode transform -n "eyeFrame_jnt_grp" -p "facial_jnt_grp";
	rename -uid "E8E641BB-4967-DD33-89A7-63B8C49F63B1";
createNode joint -n "eyeFrame_L_001_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "62FD6D2F-4577-77A3-C7DB-D0B2BEB2FFF1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.48544615507125854 10.479743003845215 4.091270923614502 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.42738114194075155 10.514792968140812 4.2225639241796387 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_L_002_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "5233391C-470E-1CEE-B1B5-39854061CAB2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.1483757495880127 9.8116703033447266 3.9840564727783203 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.1209930182395302 10.186648159359207 3.9705262033427164 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_L_003_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "6636DB5B-43A9-2F32-7908-FF90ED89E4A7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0174989700317383 9.9180812835693359 3.4735996723175049 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.5898139997132339 10.217247323920287 3.6628698508455271 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_L_004_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "3D57950F-42D4-B05B-8DF1-E08AE038D4FB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3293492794036865 10.312215805053711 2.8753671646118164 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.9136604126185461 10.538418012372146 3.3017978152810787 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_L_005_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "3247D051-4A12-44EF-EE60-AB91361EAFA0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3747775554656982 10.946447372436523 2.5630693435668945 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.1537978446594752 10.732888958891047 3.0990507570985355 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_R_001_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "15F4B2CB-45D2-BCDA-C365-A78F8CDD16D6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.485446 10.4797 4.09127 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.42738114194075155 10.514792968140812 4.2225639241796387 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_R_002_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "E608A708-4349-4730-6E04-ACB7B932725C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.14838 9.81167 3.9840599999999995 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.1209930182395302 10.186648159359207 3.9705262033427164 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_R_003_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "D3BBF88A-472C-6ACB-5E37-7E99A602D372";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.0175 9.91808 3.4735999999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.5898139997132339 10.217247323920287 3.6628698508455271 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_R_004_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "3B3715BB-41AB-97B3-3D36-30B49E28A106";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.32935 10.3122 2.8753699999999998 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.9136604126185461 10.538418012372146 3.3017978152810787 1;
	setAttr ".radi" 2;
createNode joint -n "eyeFrame_R_005_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "03A64AF5-4B94-9C18-FA5E-D9AF5C652D34";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.37478 10.9464 2.5630699999999997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.1537978446594752 10.732888958891047 3.0990507570985355 1;
	setAttr ".radi" 2;
createNode joint -n "bite_L_001_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "0448123F-44BA-80C0-6517-CA86093B66ED";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.488699464537901 11.377700429276034 2.0811735543443213 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.4800764572128475 11.285006987355217 2.173872532052143 1;
	setAttr ".radi" 2;
createNode joint -n "bite_R_001_jnt" -p "eyeFrame_jnt_grp";
	rename -uid "0826BA71-4A63-32B2-599A-DCB58A84D7B1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.4887 11.3777 2.0811699999999997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.4800764572128475 11.285006987355217 2.173872532052143 1;
	setAttr ".radi" 2;
createNode transform -n "zyg_jnt_grp" -p "facial_jnt_grp";
	rename -uid "34050B61-4BF7-1DB3-7439-0F9867B8AD3F";
createNode joint -n "zyg_L_001_jnt" -p "zyg_jnt_grp";
	rename -uid "69F7E48A-484A-94F4-7093-06808E7F546F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5147054195404053 9.1263513565063477 3.7214303016662598 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2791429774528011 9.2527459032509842 3.9110284045572956 1;
	setAttr ".radi" 2;
createNode joint -n "zyg_L_002_jnt" -p "zyg_jnt_grp";
	rename -uid "DB3A094B-4852-A106-2B00-679590A3BAF4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0180821418762207 9.353449821472168 3.154655933380127 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.8866171533298954 9.5158492067027733 3.4046373961717271 1;
	setAttr ".radi" 2;
createNode joint -n "zyg_L_003_jnt" -p "zyg_jnt_grp";
	rename -uid "256A02C8-45F3-0423-CB33-4D848E26AE11";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4688956737518311 9.8356170654296875 2.2802839279174805 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.5033115117110016 9.6928638278192256 2.3482985893719759 1;
	setAttr ".radi" 2;
createNode joint -n "zyg_R_001_jnt" -p "zyg_jnt_grp";
	rename -uid "EA724307-4E72-ECAB-D5A0-36AE229C35F7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.51471 9.12635 3.7214299999999993 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2791429774528011 9.2527459032509842 3.9110284045572956 1;
	setAttr ".radi" 2;
createNode joint -n "zyg_R_002_jnt" -p "zyg_jnt_grp";
	rename -uid "86A1EEC8-467E-1411-4971-7287E89A5D8A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.01808 9.35345 3.1546599999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.8866171533298954 9.5158492067027733 3.4046373961717271 1;
	setAttr ".radi" 2;
createNode joint -n "zyg_R_003_jnt" -p "zyg_jnt_grp";
	rename -uid "4BAFA45D-47A2-EECB-B7F6-50AD62AFB882";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.4689 9.83562 2.2802799999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.5033115117110016 9.6928638278192256 2.3482985893719759 1;
	setAttr ".radi" 2;
createNode transform -n "cheek_jnt_grp" -p "facial_jnt_grp";
	rename -uid "2B5C6908-4652-9586-C16F-A0A8DB632BFB";
createNode joint -n "cheek_L_001_jnt" -p "cheek_jnt_grp";
	rename -uid "241B209B-4C55-C571-28AE-18B8ED5D6CAC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.7821712493896484 8.1650552749633789 2.7745559215545654 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.8461796647753808 8.668878672737188 3.0554157324023299 1;
	setAttr ".radi" 2;
createNode joint -n "cheek_L_002_jnt" -p "cheek_jnt_grp";
	rename -uid "96D2B6EB-49F9-1CF8-CACB-14B68899736A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.2596127986907959 8.5387134552001953 1.9980354309082031 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.3526303718210539 8.9589923486187875 2.2935625923394705 1;
	setAttr ".radi" 2;
createNode joint -n "cheek_L_003_jnt" -p "cheek_jnt_grp";
	rename -uid "3A34B928-4763-1067-F333-C4B4FFAE32BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4853637218475342 8.9519538879394531 1.1591391563415527 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 2.6140423418957219 9.500229323385831 1.2908165656840576 1;
	setAttr ".radi" 2;
createNode joint -n "cheek_R_001_jnt" -p "cheek_jnt_grp";
	rename -uid "525B6A60-4B39-43AE-910A-E9B218AC1824";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.78217 8.16506 2.77456 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.8461796647753808 8.668878672737188 3.0554157324023299 1;
	setAttr ".radi" 2;
createNode joint -n "cheek_R_002_jnt" -p "cheek_jnt_grp";
	rename -uid "5FE8548A-4BB0-50B5-22B9-62A1866647DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.25961 8.53871 1.99804 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.3526303718210539 8.9589923486187875 2.2935625923394705 1;
	setAttr ".radi" 2;
createNode joint -n "cheek_R_003_jnt" -p "cheek_jnt_grp";
	rename -uid "1654D3C6-40DE-1731-B5AE-BE91931F85C8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.48536 8.95195 1.15914 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 2.6140423418957219 9.500229323385831 1.2908165656840576 1;
	setAttr ".radi" 2;
createNode transform -n "nosFlo_jnt_grp" -p "facial_jnt_grp";
	rename -uid "E3574201-4415-60CF-A630-1F8AC8642ED1";
createNode joint -n "lipChin_C_001_jnt" -p "nosFlo_jnt_grp";
	rename -uid "148D7532-47F4-FD48-1F85-11BE88886DB4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00015288963913917542 7.3639101982116699 4.0173206329345703 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.041202995794827509 7.2334726192481229 4.2288960800590187 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_L_001_jnt" -p "nosFlo_jnt_grp";
	rename -uid "8FE353D5-449F-442C-3F71-A08CBE7ED55D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.55797863006591797 9.5878200531005859 4.4003925323486328 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.51075731845593564 9.7230196653636884 4.4515397210215752 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_L_002_jnt" -p "nosFlo_jnt_grp";
	rename -uid "120CC452-4748-D15B-6882-A8869A408A0C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.97933292388916016 9.1474685668945312 4.0290870666503906 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.97756107041373796 8.8540898362467484 4.1001274671245955 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_L_003_jnt" -p "nosFlo_jnt_grp";
	rename -uid "1E28FDFA-4269-D09D-E323-278A55494D51";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.3591451644897461 8.2802190780639648 3.5942158699035645 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.276360736842914 8.3242750618701589 3.8020045936035176 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_L_004_jnt" -p "nosFlo_jnt_grp";
	rename -uid "C5DAA159-4A74-556E-5538-71ABD56AF00B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1088805198669434 7.6778407096862793 3.5704183578491211 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.2033118640887073 7.9159290623120553 3.7387950000737322 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_L_005_jnt" -p "nosFlo_jnt_grp";
	rename -uid "812686E9-4B15-C6E1-97C0-79A9C27B37CB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.88336926698684692 7.448793888092041 3.6904635429382324 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.102047929939914 7.498712276857991 3.7141381560241817 1;
	setAttr ".radi" 2;
createNode joint -n "lipChin_L_002_jnt" -p "nosFlo_jnt_grp";
	rename -uid "5D058ED1-46E3-31E0-F7BF-0ABA6826BE2F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.59475547075271606 7.3706507682800293 3.8599975109100342 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.600958614428177 7.2748543042723464 4.0465199241233849 1;
	setAttr ".radi" 2;
createNode joint -n "lipChin_L_001_jnt" -p "nosFlo_jnt_grp";
	rename -uid "33516B59-4AA7-00FC-45D8-5580DAEB5970";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.30864483118057251 7.363917350769043 3.9746146202087402 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.041202995794827509 7.2334726192481229 4.2288960800590187 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_R_001_jnt" -p "nosFlo_jnt_grp";
	rename -uid "9B3B45E4-4DC9-630B-62AF-07BD3B673ED3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -0.557979 9.58782 4.40039 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.51075731845593564 9.7230196653636884 4.4515397210215752 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_R_002_jnt" -p "nosFlo_jnt_grp";
	rename -uid "A3358EDE-47A8-136F-C281-61808DE8FE68";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.979333 9.14747 4.02909 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.97756107041373796 8.8540898362467484 4.1001274671245955 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_R_003_jnt" -p "nosFlo_jnt_grp";
	rename -uid "E04DB78F-4B9A-382F-99A7-539A4D294ED3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.35915 8.28022 3.59422 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.276360736842914 8.3242750618701589 3.8020045936035176 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_R_004_jnt" -p "nosFlo_jnt_grp";
	rename -uid "6F24CEE4-4526-3EFB-022E-92BB6E01969C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.10888 7.67784 3.5704199999999995 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.2033118640887073 7.9159290623120553 3.7387950000737322 1;
	setAttr ".radi" 2;
createNode joint -n "nosFlo_R_005_jnt" -p "nosFlo_jnt_grp";
	rename -uid "ADF652C8-4D4C-2DBC-D88F-2FA0557335AC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.883369 7.4487900000000007 3.6904599999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.102047929939914 7.498712276857991 3.7141381560241817 1;
	setAttr ".radi" 2;
createNode joint -n "lipChin_R_002_jnt" -p "nosFlo_jnt_grp";
	rename -uid "150653E2-4258-5BEA-6F5B-D194C76E7CA9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.594755 7.3706500000000013 3.8599999999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.600958614428177 7.2748543042723464 4.0465199241233849 1;
	setAttr ".radi" 2;
createNode joint -n "lipChin_R_001_jnt" -p "nosFlo_jnt_grp";
	rename -uid "D89869DF-4587-8BAE-08FD-899F194D4FD7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.308645 7.36392 3.9746099999999998 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.041202995794827509 7.2334726192481229 4.2288960800590187 1;
	setAttr ".radi" 2;
createNode transform -n "chin_jnt_grp" -p "facial_jnt_grp";
	rename -uid "C581BF78-44F1-9C85-B8B6-85999EDFE747";
createNode joint -n "chin_C_001_jnt" -p "chin_jnt_grp";
	rename -uid "F76FAA2C-46C3-EE0C-227E-86AF3EE9325E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00013379007577896118 6.6002101898193359 3.9838423728942871 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.019686930378738317 6.6803677266927117 4.2140960238816589 1;
	setAttr ".radi" 2;
createNode joint -n "chin_L_001_jnt" -p "chin_jnt_grp";
	rename -uid "767D4927-4C47-6C00-5386-0792F904FA29";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.45245867967605591 6.6001815795898438 3.9173324108123779 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.019686930378738317 6.6803677266927117 4.2140960238816589 1;
	setAttr ".radi" 2;
createNode joint -n "chin_L_002_jnt" -p "chin_jnt_grp";
	rename -uid "89D824C7-45BD-681A-6026-978CBDDC5065";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1278786659240723 6.9100303649902344 3.181365966796875 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.51550022468915835 6.7261020991581413 4.1301696197946844 1;
	setAttr ".radi" 2;
createNode joint -n "chin_L_003_jnt" -p "chin_jnt_grp";
	rename -uid "52F55209-4095-2DB2-B0F8-758D6DA8729E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5985672473907471 7.2785587310791016 2.6469697952270508 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.99629947118216022 6.8562877932151132 3.7576267425318099 1;
	setAttr ".radi" 2;
createNode joint -n "chin_L_004_jnt" -p "chin_jnt_grp";
	rename -uid "D780602F-4B55-F596-7606-A6B23658719D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.0158641338348389 7.6900086402893066 1.8765504360198975 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.6827523595540876 7.2754696643437846 2.8732687202292841 1;
	setAttr ".radi" 2;
createNode joint -n "chin_R_001_jnt" -p "chin_jnt_grp";
	rename -uid "616647AA-4F3A-CC4D-8B31-CC9DF3636CEA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.452459 6.60018 3.9173299999999998 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.019686930378738317 6.6803677266927117 4.2140960238816589 1;
	setAttr ".radi" 2;
createNode joint -n "chin_R_002_jnt" -p "chin_jnt_grp";
	rename -uid "0E179490-426A-C7D1-B1E6-A082B6C97010";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.12788 6.910029999999999 3.1813699999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.51550022468915835 6.7261020991581413 4.1301696197946844 1;
	setAttr ".radi" 2;
createNode joint -n "chin_R_003_jnt" -p "chin_jnt_grp";
	rename -uid "2EC4D739-49CC-DF60-D382-928CC9D03791";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.59857 7.2785599999999988 2.6469699999999996 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.99629947118216022 6.8562877932151132 3.7576267425318099 1;
	setAttr ".radi" 2;
createNode joint -n "chin_R_004_jnt" -p "chin_jnt_grp";
	rename -uid "18626949-4957-CE95-533B-3A93014FF465";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.01586 7.6900099999999991 1.87655 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.6827523595540876 7.2754696643437846 2.8732687202292841 1;
	setAttr ".radi" 2;
createNode joint -n "chinNeck_L_001_jnt" -p "chin_jnt_grp";
	rename -uid "FBE4003B-4129-57A2-BF9C-89831228E89A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3214733600616455 8.2154808044433594 0.95036953687667847 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.2942956745170826 8.5639761377446622 0.56437783414500864 1;
	setAttr ".radi" 2;
createNode joint -n "chinNeck_R_001_jnt" -p "chin_jnt_grp";
	rename -uid "687335F4-4D4B-FC5E-55EA-32A6B49388DE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.32147 8.21548 0.95037 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 2.2942956745170826 8.5639761377446622 0.56437783414500864 1;
	setAttr ".radi" 2;
createNode transform -n "lip_jnt_grp" -p "facial_jnt_grp";
	rename -uid "3983FE2E-4275-18B6-04A7-66ADB091BAEA";
createNode joint -n "upLipFrame_C_001_jnt" -p "lip_jnt_grp";
	rename -uid "3CA83930-4380-2366-57D1-95A7F7E65177";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00013386458158493042 8.5648174285888672 4.3139505386352539 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.04663440206904533 8.5242589107157478 4.6079405048244393 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipFrame_C_001_jnt" -p "lip_jnt_grp";
	rename -uid "2EC30A2F-4358-DECC-24A2-92AFD3187E94";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00014242157340049744 7.7093524932861328 4.1852841377258301 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.055476020080101038 7.5645859217592051 4.225344121079087 1;
	setAttr ".radi" 2;
createNode joint -n "upLipFrame_L_001_jnt" -p "lip_jnt_grp";
	rename -uid "F252D1F9-4E66-36E1-7BF1-C79610EBCE80";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.46668782830238342 8.5426998138427734 4.2592430114746094 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.04663440206904533 8.5242589107157478 4.6079405048244393 1;
	setAttr ".radi" 2;
createNode joint -n "upLipFrame_L_002_jnt" -p "lip_jnt_grp";
	rename -uid "4E547A38-4295-8A8A-934F-79B0DBE3183B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.94075167179107666 8.4675283432006836 3.9406640529632568 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.04663440206904533 8.5242589107157478 4.6079405048244393 1;
	setAttr ".radi" 2;
createNode joint -n "mouth_L_001_jnt" -p "lip_jnt_grp";
	rename -uid "3794E3B6-427C-D320-FEE4-028BFF042568";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.99284723180255674 8.0885326186972737 3.7272114197051991 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.86052262585931572 8.0842548508622443 3.9103904179424327 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipFrame_L_002_jnt" -p "lip_jnt_grp";
	rename -uid "48413A46-4881-A5CC-425F-A08FEA7E1D49";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.7256704568862915 7.7689285278320312 3.9046978950500488 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.055476020080101038 7.5645859217592051 4.225344121079087 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipFrame_L_001_jnt" -p "lip_jnt_grp";
	rename -uid "63EEA617-4EE6-FC1F-1F28-578904316521";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.37883636430257894 7.6983378277550338 4.0993888126205738 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.055476020080101038 7.5645859217592051 4.225344121079087 1;
	setAttr ".radi" 2;
createNode joint -n "upLipFrame_R_001_jnt" -p "lip_jnt_grp";
	rename -uid "07D94E6C-4F2C-A1B3-1740-DA82D6FCE982";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.466688 8.5427 4.25924 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.04663440206904533 8.5242589107157478 4.6079405048244393 1;
	setAttr ".radi" 2;
createNode joint -n "upLipFrame_R_002_jnt" -p "lip_jnt_grp";
	rename -uid "AED26562-41DB-ECE4-D13C-F3ADC59E2816";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.940752 8.46753 3.94066 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.04663440206904533 8.5242589107157478 4.6079405048244393 1;
	setAttr ".radi" 2;
createNode joint -n "mouth_R_001_jnt" -p "lip_jnt_grp";
	rename -uid "01E3B166-40CE-AC96-882C-378ADD096C20";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.992847 8.08853 3.72721 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.86052262585931572 8.0842548508622443 3.9103904179424327 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipFrame_R_002_jnt" -p "lip_jnt_grp";
	rename -uid "A2E21300-4394-AE3E-317D-05A5112F92D8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.72567 7.768930000000001 3.9046999999999996 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.055476020080101038 7.5645859217592051 4.225344121079087 1;
	setAttr ".radi" 2;
createNode joint -n "lowLipFrame_R_001_jnt" -p "lip_jnt_grp";
	rename -uid "BBE6D124-4D27-3C33-BEDD-749BF8639B77";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.378836 7.69834 4.09939 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.055476020080101038 7.5645859217592051 4.225344121079087 1;
	setAttr ".radi" 2;
createNode transform -n "nose_jnt_grp" -p "facial_jnt_grp";
	rename -uid "4848132A-42EB-1F79-3718-D58A16F6CA73";
createNode joint -n "noseRoot_C_001_jnt" -p "nose_jnt_grp";
	rename -uid "3E3DD081-4546-2546-C279-CBBB15C11E8F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.0035460485101228433 10.684953592192102 4.4166141178970735 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.0081673659579232089 10.78945988455283 4.7066071699979615 1;
	setAttr ".radi" 2;
createNode joint -n "noseTip_C_001_jnt" -p "nose_jnt_grp";
	rename -uid "499931F0-4D32-FEFD-13F0-C79E7282D57B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 9.1940898895263672 4.9873991012573242 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.018984855697521143 9.3303266745728184 5.3644639453001988 1;
	setAttr ".radi" 2;
createNode joint -n "noseBottom_C_001_jnt" -p "nose_jnt_grp";
	rename -uid "DB842442-4C2E-A65D-B387-41B587A86EEA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.0001399647444486618 8.9019374847412109 4.3592944145202637 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226746e-05 0 0.00013180661635366 1.4449239609493174e-05 0.99999999120911764 0
		 -0.03360195484761673 8.9613885037220467 4.765638046243061 1;
	setAttr ".radi" 2;
createNode joint -n "noseWing_L_001_jnt" -p "nose_jnt_grp";
	rename -uid "A9429CF2-4567-DD33-B3E4-BF81037F0CF2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.34074118733406067 8.9490175247192383 4.2669734954833984 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.68590205772009238 9.2924148353584854 4.4117519888657695 1;
	setAttr ".radi" 2;
createNode joint -n "noseWing_L_002_jnt" -p "nose_jnt_grp";
	rename -uid "C98BCBF1-485A-2AF6-6853-5F8AE47DF3DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.68406617641448975 9.1593236923217773 4.1463994979858398 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.48769059376823864 8.7963323539167941 4.445731581235151 1;
	setAttr ".radi" 2;
createNode joint -n "noseWing_R_001_jnt" -p "nose_jnt_grp";
	rename -uid "B7748081-40BA-D56E-73FE-46AE8FA61B45";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.340741 8.94902 4.26697 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.68590205772009238 9.2924148353584854 4.4117519888657695 1;
	setAttr ".radi" 2;
createNode joint -n "noseWing_R_002_jnt" -p "nose_jnt_grp";
	rename -uid "2D926B72-45D0-72AC-1202-F19F1BA4DCB1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.684066 9.15932 4.1464 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.48769059376823864 8.7963323539167941 4.445731581235151 1;
	setAttr ".radi" 2;
createNode transform -n "forehead_jnt_grp" -p "facial_jnt_grp";
	rename -uid "5D85C661-44C3-A143-61CD-DB9D0220D85C";
createNode joint -n "forehead_C_001_jnt" -p "forehead_jnt_grp";
	rename -uid "42201924-408C-4126-6BCD-CFA5FB0703A9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.0043026869075206385 12.051765287669056 4.4915656175565815 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 -0.00072845586154334212 12.107496386945137 4.6019128576743968 1;
	setAttr ".radi" 2;
createNode joint -n "forehead_C_002_jnt" -p "forehead_jnt_grp";
	rename -uid "99CA2D3C-462E-883E-1B79-AFB496C6B06C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.006993131192672742 12.795336806528523 4.3819678173877969 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 0.0069235851753713766 12.818907166514308 4.4957481967060868 1;
	setAttr ".radi" 2;
createNode joint -n "forehead_L_001_jnt" -p "forehead_jnt_grp";
	rename -uid "2AD3EC06-4931-1D2C-6715-7AA207309C84";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2696250141666134 12.250022112576113 4.243078369847626 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2112109467378598 12.258016262149042 4.2401315645952717 1;
	setAttr ".radi" 2;
createNode joint -n "forehead_L_002_jnt" -p "forehead_jnt_grp";
	rename -uid "211D8B1A-484A-E4DF-C46B-1CA23821750A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.2662715789330123 12.820293228511485 4.1008545505959821 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2081035499624 12.822704374435206 4.093404100805853 1;
	setAttr ".radi" 2;
createNode joint -n "forehead_R_001_jnt" -p "forehead_jnt_grp";
	rename -uid "63DCF252-4D88-7361-F034-569B185A7ABF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.26963 12.25 4.2430799999999991 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2112109467378598 12.258016262149042 4.2401315645952717 1;
	setAttr ".radi" 2;
createNode joint -n "forehead_R_002_jnt" -p "forehead_jnt_grp";
	rename -uid "983992FD-4A89-552F-2284-81A08F3A3F2B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.26627 12.8203 4.1008499999999994 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742739242139e-06 -0.00013180669276122435 0
		 -5.2890787339311278e-06 0.99999999988163268 -1.4448542599226749e-05 0 0.00013180661635366 1.4449239609493178e-05 0.99999999120911764 0
		 1.2081035499624 12.822704374435206 4.093404100805853 1;
	setAttr ".radi" 2;
createNode transform -n "throat_jnt_grp" -p "facial_jnt_grp";
	rename -uid "89A76E15-46BA-9AE0-2CA6-DDBDC51DC4D2";
createNode joint -n "chinThroat_C_001_jnt" -p "throat_jnt_grp";
	rename -uid "715761DB-446E-60AD-ACFD-36A085592E7B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00020532310009002686 6.4363861083984375 2.2802090644836426 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 -0.0012774448180107461 6.2653784395059517 2.4825342328256497 1;
	setAttr ".radi" 2;
createNode joint -n "chinThroat_C_002_jnt" -p "throat_jnt_grp";
	rename -uid "D3FB15D7-446A-13F8-3250-978772174610";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.000252552330493927 6.2460217475891113 1.785294771194458 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 0.00019132546718531225 6.0582176225410418 2.0695743054538056 1;
	setAttr ".radi" 2;
createNode joint -n "throat_C_001_jnt" -p "throat_jnt_grp";
	rename -uid "5B7E11A4-478E-5B57-F80A-1EAB75B49374";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.0001681596040725708 5.6298894882202148 1.5964155197143555 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 0.00016758460840653777 5.2978457721373262 1.7116651417066409 1;
	setAttr ".radi" 2;
createNode joint -n "throat_C_003_jnt" -p "throat_jnt_grp";
	rename -uid "B34A16BF-4074-03C6-634D-5DB4FF91276D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.00012038276327075437 4.5665569305419922 1.2402728796005249 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 -0.0011885501049085619 4.7062554256643727 1.1434280493713047 1;
	setAttr ".radi" 2;
createNode joint -n "throat_C_002_jnt" -p "throat_jnt_grp";
	rename -uid "DF5FEDCE-4E82-9BE2-3F54-2BB395045DB1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.0001700669527053833 3.7229316234588623 1.3687072992324829 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0059217428878935319 3.7333176560233334 0.78342172177542646 1;
	setAttr ".radi" 2;
createNode transform -n "chinThroat_jnt_grp" -p "facial_jnt_grp";
	rename -uid "2710B1C9-4B6A-2680-AD67-4CB00C610AF8";
createNode joint -n "chinThroat_L_001_jnt" -p "chinThroat_jnt_grp";
	rename -uid "A3741D05-4AAA-3364-F627-CF8E8832EEC5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.25789475440979 7.0171771049499512 1.4957858324050903 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.5203500903363394 6.9170839333003729 2.027882753775256 1;
	setAttr ".radi" 2;
createNode joint -n "chinThroat_L_002_jnt" -p "chinThroat_jnt_grp";
	rename -uid "137C6EBF-488B-CDCE-54DA-6B8D99CF8EA2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.81796157360076904 5.6688408851623535 1.2600280046463013 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 0.99086198874697329 6.1565777382234588 1.3713137734575278 1;
	setAttr ".radi" 2;
createNode joint -n "chinThroat_R_001_jnt" -p "chinThroat_jnt_grp";
	rename -uid "EBBE1B9B-4AC4-DC7E-7E40-5C91AA62FFA2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.25789 7.01718 1.4957899999999997 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999129952077 5.2871742728139875e-06 -0.00013180669276022507 0
		 -5.2890787328209099e-06 0.99999999988163268 -1.4448542599393362e-05 0 0.00013180661635266077 1.4449239609659638e-05 0.99999999120911764 0
		 1.5203500903363394 6.9170839333003729 2.027882753775256 1;
	setAttr ".radi" 2;
createNode joint -n "chinThroat_R_002_jnt" -p "chinThroat_jnt_grp";
	rename -uid "CC70C0E8-400A-2651-7C67-0CAD3C0E1CA3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.817962 5.66884 1.26003 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 0.99086198874697329 6.1565777382234588 1.3713137734575278 1;
	setAttr ".radi" 2;
createNode transform -n "clavicleNeck_jnt_grp" -p "facial_jnt_grp";
	rename -uid "717247C5-47CF-1D77-CF8B-FFB64DAD6ABB";
createNode joint -n "clavicleNeck_L_001_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "0FAE3480-409E-8D9C-AB95-ABBB6D371397";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.2843880653381348 7.2621726989746094 0.2006085216999054 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 2.1555661764049834 7.5984624643867509 0.51644571464303302 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_L_002_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "B94F77BE-4B30-9E66-E49F-CABF6B64E8B2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.2235007286071777 6.4888582229614258 0.40176340937614441 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 1.5727015453337208 5.8940012050669148 0.76233466406020611 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_L_003_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "8B0B3F42-47EB-B14F-731A-46BBFF063795";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.1431691646575928 5.6174063682556152 0.64830487966537476 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1047634125760244 3.5591371399180121 0.85998908079583514 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_L_004_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "1D95EF58-4D07-9B2D-688E-01AFE028A090";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.6647086143493652 4.4866776466369629 1.0263814926147461 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 2.0723634016069923 6.0204128088227904 0.13626346675592951 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_L_005_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "3876213A-4078-3AAD-6786-A4A811A00F75";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.6888468265533447 4.418698787689209 0.0003346707671880722 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.6487635662306963 4.4388012957694531 -0.41846431534200146 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_R_001_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "15F0C32C-4FD6-87A8-B6BB-6F8DFF3E94D9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.28439 7.26217 0.200609 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 2.1555661764049834 7.5984624643867509 0.51644571464303302 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_R_002_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "6BA24C07-46E7-82D5-1B0B-3FB769A1A362";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2235 6.48886 0.40176300000000004 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 1.5727015453337208 5.8940012050669148 0.76233466406020611 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_R_003_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "CD2B59C3-4FDA-AADF-AE62-68ABB1CC877D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.14317 5.61741 0.648305 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1047634125760244 3.5591371399180121 0.85998908079583514 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_R_004_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "C548013F-4D8C-AF37-6052-2E96EB11D818";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.66471 4.48668 1.02638 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.99999999860792332 2.1150986001471774e-06 -5.2722668046884387e-05 0
		 -2.1154037794379486e-06 0.99999999998101008 -5.7883335088570984e-06 0 5.2722655802987084e-05 5.7884450305305421e-06 0.99999999859340771 0
		 2.0723634016069923 6.0204128088227904 0.13626346675592951 1;
	setAttr ".radi" 2;
createNode joint -n "clavicleNeck_R_005_jnt" -p "clavicleNeck_jnt_grp";
	rename -uid "F309BF42-4D83-C095-D9BE-9EA8CA0A86EA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.68885 4.4187 0.00033467100000000166 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.6487635662306963 4.4388012957694531 -0.41846431534200146 1;
	setAttr ".radi" 2;
createNode transform -n "adj_jnt_grp";
	rename -uid "B023A434-4835-BD95-14D3-60896D090778";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0.69231671 0 ;
createNode joint -n "adj_brow_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "2E91B65A-4586-68A5-952B-BCB7870D57E0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0005179278627931651 11.404634076679233 4.5836510780331858 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_brow_C_001_jnt_pointConstraint1" -p "adj_brow_C_001_jnt";
	rename -uid "6F2C7B7D-4650-5662-8649-EFBA6868DD4D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle115W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0036221559316888872 -0.010722559368129936 0.052592289733625286 ;
	setAttr ".rst" -type "double3" 0.00051792029579724634 11.404634076679233 4.5836510780331858 ;
	setAttr -k on ".w0";
createNode joint -n "adj_brow_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "3332C776-432E-6D17-7812-C9A6F70D618E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2936375099999999 11.708099369999999 3.18370891 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_brow_L_001_jnt_pointConstraint1" -p "adj_brow_L_001_jnt";
	rename -uid "7D620C46-4C2C-D826-7DD4-EC859B8D46A7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle116W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.015564437566528255 0.00086880206787043335 0.0026788749810791046 ;
	setAttr ".rst" -type "double3" 2.2936375099999999 11.708099369999999 3.18370891 ;
	setAttr -k on ".w0";
createNode joint -n "adj_brow_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "A1800F1A-42AB-3004-968C-5C8E3646BD60";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2936375099999999 11.708099369999999 3.18370891 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_brow_R_001_jnt_pointConstraint1" -p "adj_brow_R_001_jnt";
	rename -uid "7F9E5035-4065-5AB0-8AB0-CDBF5961509A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle114W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.015565391240844662 0.00086880206787043335 0.0026793518182373077 ;
	setAttr ".rst" -type "double3" -2.293637748418579 11.708099369999999 3.18370891 ;
	setAttr -k on ".w0";
createNode joint -n "adj_forehead_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "509A6240-44EA-223E-17ED-28BAF7B66B12";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0043026870116591454 12.051765441894531 4.4915657043457031 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_forehead_C_001_jnt_pointConstraint1" -p "adj_forehead_C_001_jnt";
	rename -uid "0910EE8C-41B5-EB32-7AF2-A4A4D05E0A7D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle119W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.00165202422067523 -0.00196075439453125 -0.0094714164733886719 ;
	setAttr ".rst" -type "double3" 0.0043026870116591454 12.051765441894531 4.4915657043457031 ;
	setAttr -k on ".w0";
createNode joint -n "adj_noseTip_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "9301A145-44D5-5995-02B8-18AEAA74DEB6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 9.1940898895263672 4.9873991012573242 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_noseTip_C_001_jnt_pointConstraint1" -p "adj_noseTip_C_001_jnt";
	rename -uid "D07517B1-49F9-8745-1002-FEA6588F52B4";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle148W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -2.049239091270064e-15 0.014444351196289062 0.039737224578857422 ;
	setAttr ".rst" -type "double3" 0 9.1940898895263672 4.9873991012573242 ;
	setAttr -k on ".w0";
createNode joint -n "adj_chin_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "16B0E2A5-441B-D3D6-3D48-23A73951939D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00013379007577896118 6.6002101898193359 3.9838423728942871 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_chin_C_001_jnt_pointConstraint1" -p "adj_chin_C_001_jnt";
	rename -uid "E7CAE7DE-429E-9C62-420B-53BA60B40F3C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle164W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.00013379007577937966 -0.027577400207519531 0.090257167816162109 ;
	setAttr ".rst" -type "double3" 0.00013379007577896118 6.6002101898193359 3.9838423728942871 ;
	setAttr -k on ".w0";
createNode joint -n "adj_chinThroat_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "7BE96646-4958-6AC9-93C3-A1AC80CE84FF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0.00020532310009002686 6.4363861083984375 2.2802090644836426 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00020532310009002686 6.4363861083984375 2.2802090644836426 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode joint -n "adj_forehead_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "853D4F28-40FB-FCD1-BDAF-2295B3868CB7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2696250677108765 12.250021934509277 4.2430782318115234 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_forehead_L_001_jnt_pointConstraint1" -p "adj_forehead_L_001_jnt";
	rename -uid "DFB31883-439D-FF43-4729-1C8703F129AF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle118W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.00050830841064453125 0.00060176849365234375 0.0029115676879882812 ;
	setAttr ".rst" -type "double3" 1.2696250677108765 12.250021934509277 4.2430782318115234 ;
	setAttr -k on ".w0";
createNode joint -n "adj_forehead_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "9A601F9F-4D5A-C226-7602-CBA9C88674C1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.269629955291748 12.25 4.2430801391601562 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_forehead_R_001_jnt_pointConstraint1" -p "adj_forehead_R_001_jnt";
	rename -uid "BCAC28F6-43C0-2692-BB92-C6BC4767705C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle120W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.00050771236419677734 0.00060272216796875 0.0029096603393554688 ;
	setAttr ".rst" -type "double3" -1.269629955291748 12.25 4.2430801391601562 ;
	setAttr -k on ".w0";
createNode joint -n "adj_forehead_C_002_jnt" -p "adj_jnt_grp";
	rename -uid "8E0429E9-4B76-6773-756A-6EA97E3823D7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.006993131192672742 12.795336806528523 4.3819678173877969 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_forehead_C_002_jnt_pointConstraint1" -p "adj_forehead_C_002_jnt";
	rename -uid "F7844E64-42C9-70DF-4540-EFADFFD20AD9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle122W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0057306412535642511 0.0094748375343822744 0.03327110870859773 ;
	setAttr ".rst" -type "double3" 0.006993131192672742 12.795336806528523 4.3819678173877969 ;
	setAttr -k on ".w0";
createNode joint -n "adj_forehead_L_002_jnt" -p "adj_jnt_grp";
	rename -uid "8C6C9F2F-4EB6-5B97-CC32-6EBD242ECF7A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2662715789330123 12.820293228511485 4.1008545505959821 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_forehead_L_002_jnt_pointConstraint1" -p "adj_forehead_L_002_jnt";
	rename -uid "3D4D690E-4A4A-CB99-403B-DE998654BE70";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle117W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0096247318732620712 -0.0025388790324605282 -0.009198511842982704 ;
	setAttr ".rst" -type "double3" 1.2662715789330123 12.820293228511485 4.1008545505959821 ;
	setAttr -k on ".w0";
createNode joint -n "adj_forehead_R_002_jnt" -p "adj_jnt_grp";
	rename -uid "B8D940D6-4B25-5279-A16F-57B1C59FFEB1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.26627 12.8203 4.1008499999999994 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_forehead_R_002_jnt_pointConstraint1" -p "adj_forehead_R_002_jnt";
	rename -uid "CFBF1942-444A-AA78-8A82-87A459ECC7E1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle121W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0096261915969848566 -0.0025387832641605712 -0.0092011550903325912 ;
	setAttr ".rst" -type "double3" -1.26627 12.8203 4.1008499999999994 ;
	setAttr -k on ".w0";
createNode joint -n "adj_noseRoot_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "0060BBDE-42B7-FAF3-A6C8-979104FD6321";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0035460485101228433 10.684953592192102 4.4166141178970735 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_noseRoot_C_001_jnt_pointConstraint1" -p "adj_noseRoot_C_001_jnt";
	rename -uid "5D983E72-4E44-BBDD-0B2F-6CB88DE38ABF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle157W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.003546048510121138 0.0051793078293087547 0.01424938706211254 ;
	setAttr ".rst" -type "double3" 0.0035460485101228433 10.684953592192102 4.4166141178970735 ;
	setAttr -k on ".w0";
createNode joint -n "adj_eyeFrame_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "26612016-4C24-9CDC-1C83-85AE2F34FB43";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.48544615507125854 10.479743003845215 4.091270923614502 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_eyeFrame_L_001_jnt_pointConstraint1" -p "adj_eyeFrame_L_001_jnt";
	rename -uid "9FA97F86-4856-04E8-924F-AFB65E211C7C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle129W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.032179832458496094 -0.0086088180541992188 -0.062544822692871094 ;
	setAttr ".rst" -type "double3" 0.48544615507125854 10.479743003845215 4.091270923614502 ;
	setAttr -k on ".w0";
createNode joint -n "adj_eyeFrame_L_003_jnt" -p "adj_jnt_grp";
	rename -uid "A1A890B8-4B0E-3F2C-431B-3E914773EF79";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0174989700317383 9.9180812835693359 3.4735996723175049 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_eyeFrame_L_003_jnt_pointConstraint1" -p "adj_eyeFrame_L_003_jnt";
	rename -uid "391BABDB-4443-AA5A-C7DE-2583340F455B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle128W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.017167329788208008 -0.0092926025390625 0.017134904861450195 ;
	setAttr ".rst" -type "double3" 2.0174989700317383 9.9180812835693359 3.4735996723175049 ;
	setAttr -k on ".w0";
createNode joint -n "adj_bite_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "0C7D3509-4FC6-CF65-8631-EF9636D4DECC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.488699464537901 11.377700429276034 2.0811735543443213 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_bite_L_001_jnt_pointConstraint1" -p "adj_bite_L_001_jnt";
	rename -uid "BBD1116A-4086-241E-B454-1FA7C1B54D6E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle127W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.004039077498716459 -0.00012816874642673781 0.000777617378378892 ;
	setAttr ".rst" -type "double3" 2.488699464537901 11.377700429276034 2.0811735543443213 ;
	setAttr -k on ".w0";
createNode joint -n "adj_lowlid_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "B0DE2E6D-4D8D-A3C6-FCEA-588413B0F222";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.0851883888244629 10.452959060668945 3.9599666595458984 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_lowlid_L_001_jnt_pointConstraint1" -p "adj_lowlid_L_001_jnt";
	rename -uid "C2DE0FEE-4D44-68AC-BA40-039E7D331283";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle123W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.00022208690643310547 5.817413330078125e-05 0.00081562995910644531 ;
	setAttr ".rst" -type "double3" 1.0851883888244629 10.452959060668945 3.9599666595458984 ;
	setAttr -k on ".w0";
createNode joint -n "adj_lowlid_L_003_jnt" -p "adj_jnt_grp";
	rename -uid "22874E90-4F50-C6F4-F96F-328717CA3C9C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7195367813110352 10.517522811889648 3.7072761058807373 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_lowlid_L_003_jnt_pointConstraint1" -p "adj_lowlid_L_003_jnt";
	rename -uid "1F4FD3E5-4657-C482-B5B9-3BB0EB37C0A1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle124W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0019501447677612305 -0.00016021728515625 0.0032744407653808594 ;
	setAttr ".rst" -type "double3" 1.7195367813110352 10.517522811889648 3.7072761058807373 ;
	setAttr -k on ".w0";
createNode joint -n "adj_eyeFrame_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "2D1C3FE7-4196-C700-A140-DC8635F9DFD0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.48544599999999999 10.479699999999999 4.0912699999999997 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_eyeFrame_R_001_jnt_pointConstraint1" -p "adj_eyeFrame_R_001_jnt";
	rename -uid "AB0F5620-46D9-6984-D186-D1AB14E545E2";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle130W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.032193160156250011 -0.0086460998535162759 -0.062540024261474869 ;
	setAttr ".rst" -type "double3" -0.485446 10.4797 4.09127 ;
	setAttr -k on ".w0";
createNode joint -n "adj_eyeFrame_R_003_jnt" -p "adj_jnt_grp";
	rename -uid "40F68306-41CB-7C47-21D6-60BE2638B3A1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0175000000000001 9.9180799999999998 3.4735999999999994 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_eyeFrame_R_003_jnt_pointConstraint1" -p "adj_eyeFrame_R_003_jnt";
	rename -uid "3434ADC9-4C1F-A4F8-C732-35B4EBFEBB8B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle131W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.017167882919311594 -0.0092919787597658399 0.017136186218261074 ;
	setAttr ".rst" -type "double3" -2.0175 9.91808 3.4735999999999994 ;
	setAttr -k on ".w0";
createNode joint -n "adj_bite_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "4B1C6535-4030-5303-C1E2-A5B093BF8DA6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4887000000000001 11.377700000000001 2.0811699999999997 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_bite_R_001_jnt_pointConstraint1" -p "adj_bite_R_001_jnt";
	rename -uid "0189ED74-4034-2318-6881-C9B4339128B6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle132W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0040388977050782593 -0.00012764434814371839 0.00077740089416478142 ;
	setAttr ".rst" -type "double3" -2.4887 11.3777 2.0811699999999997 ;
	setAttr -k on ".w0";
createNode joint -n "adj_lowlid_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "831AFDC0-477C-D8D8-8D68-C58AD958C5CE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0851900000000001 10.452999999999999 3.9599699999999998 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_lowlid_R_001_jnt_pointConstraint1" -p "adj_lowlid_R_001_jnt";
	rename -uid "DCCDC7C8-4E39-CCA0-7A56-7EAB8E53695D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle125W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.00022417491912851695 5.9059143065809394e-05 0.0008218314361569945 ;
	setAttr ".rst" -type "double3" -1.08519 10.453 3.9599699999999998 ;
	setAttr -k on ".w0";
createNode joint -n "adj_lowlid_R_003_jnt" -p "adj_jnt_grp";
	rename -uid "31C24E38-4053-F829-F03C-B6B691BE7A5E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7195400000000001 10.5175 3.7072799999999995 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_lowlid_R_003_jnt_pointConstraint1" -p "adj_lowlid_R_003_jnt";
	rename -uid "A73B7D9B-4341-1BE4-8BE6-2083E307B367";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle126W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0019536018753052442 -0.0001630020141600852 0.0032792885589594256 ;
	setAttr ".rst" -type "double3" -1.71954 10.5175 3.7072799999999995 ;
	setAttr -k on ".w0";
createNode joint -n "adj_browLid_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "510D6EDB-4C18-7BCA-534C-13BFC3E7E7CB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.60751229524612427 10.947669982910156 4.1484169960021973 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_browLid_L_001_jnt_pointConstraint1" -p "adj_browLid_L_001_jnt";
	rename -uid "A2F71BEA-43EB-605A-53CD-C5BED867C994";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle159W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.00065964460372924805 0.0018634796142578125 -0.001873016357421875 ;
	setAttr ".rst" -type "double3" 0.60751229524612427 10.947669982910156 4.1484169960021973 ;
	setAttr -k on ".w0";
createNode joint -n "adj_browLid_L_003_jnt" -p "adj_jnt_grp";
	rename -uid "E417D22D-4F0C-5F61-D5FF-A9A73A5D52DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1045808799999999 11.119100570000001 3.3660836199999999 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_browLid_L_003_jnt_pointConstraint1" -p "adj_browLid_L_003_jnt";
	rename -uid "992629A0-4367-25B7-A3AB-F2A7F506B319";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle158W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.013476849390869017 -0.0017690665356440149 0.010733125615234318 ;
	setAttr ".rst" -type "double3" 2.1045808799999999 11.119100570000001 3.3660836199999999 ;
	setAttr -k on ".w0";
createNode joint -n "adj_browLid_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "95F6F1C0-4F2E-EB85-906C-75878C84723B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.60751200000000005 10.947699999999999 4.1484199999999989 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_browLid_R_001_jnt_pointConstraint1" -p "adj_browLid_R_001_jnt";
	rename -uid "9B443000-4CD1-DDE5-CAF5-EC819383A461";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle160W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.00066423138427729178 0.0018763305664055707 -0.0018857479858409576 ;
	setAttr ".rst" -type "double3" -0.607512 10.9477 4.1484199999999989 ;
	setAttr -k on ".w0";
createNode joint -n "adj_browLid_R_003_jnt" -p "adj_jnt_grp";
	rename -uid "C13B9B1D-4135-C794-DEF1-469F0341E79C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1045808799999999 11.119100570000001 3.3660836199999999 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_browLid_R_003_jnt_pointConstraint1" -p "adj_browLid_R_003_jnt";
	rename -uid "D8DC3591-462B-BB1B-7031-B18024EF95F2";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle161W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.013476610972289915 -0.0017690665356440149 0.010732887196655216 ;
	setAttr ".rst" -type "double3" -2.1045808799999999 11.119100570000001 3.3660836199999999 ;
	setAttr -k on ".w0";
createNode joint -n "adj_noseWing_L_002_jnt" -p "adj_jnt_grp";
	rename -uid "BAFA72FC-4FB3-AF62-7812-77BD7CA250C7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.68406617641448975 9.1593236923217773 4.1463994979858398 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_noseWing_L_002_jnt_pointConstraint1" -p "adj_noseWing_L_002_jnt";
	rename -uid "4380D3C2-40BD-D23F-1549-89A9F0028D27";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle149W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.054818093776702881 -0.026422500610351562 0.042608261108398438 ;
	setAttr ".rst" -type "double3" 0.68406617641448975 9.1593236923217773 4.1463994979858398 ;
	setAttr -k on ".w0";
createNode joint -n "adj_zyg_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "80849C3D-4DDA-F2B2-D6DF-E88D7A2EFFED";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.5147054195404053 9.1263513565063477 3.7214303016662598 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_zyg_L_001_jnt_pointConstraint1" -p "adj_zyg_L_001_jnt";
	rename -uid "B0AABA74-42E0-520B-6439-02B0141CFE89";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle134W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.012210369110107422 -0.0037975311279296875 0.0090317726135253906 ;
	setAttr ".rst" -type "double3" 1.5147054195404053 9.1263513565063477 3.7214303016662598 ;
	setAttr -k on ".w0";
createNode joint -n "adj_zyg_L_003_jnt" -p "adj_jnt_grp";
	rename -uid "01361CA6-411A-DE13-5220-6EBF035BDB69";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4688956737518311 9.8356170654296875 2.2802839279174805 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_zyg_L_003_jnt_pointConstraint1" -p "adj_zyg_L_003_jnt";
	rename -uid "C848E6A0-48D6-6348-7867-88A403DAB3BD";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle133W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0083882808685302734 0.00019359588623046875 0.0017435550689697266 ;
	setAttr ".rst" -type "double3" 2.4688956737518311 9.8356170654296875 2.2802839279174805 ;
	setAttr -k on ".w0";
createNode joint -n "adj_cheek_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "C64BADFC-4E97-B851-1011-48A52E03B207";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7821712493896484 8.1650552749633789 2.7745559215545654 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_cheek_L_001_jnt_pointConstraint1" -p "adj_cheek_L_001_jnt";
	rename -uid "F62C51D1-474A-ED9D-E123-5391295FE122";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle138W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0025364160537719727 0.00071239471435546875 -0.0011007785797119141 ;
	setAttr ".rst" -type "double3" 1.7821712493896484 8.1650552749633789 2.7745559215545654 ;
	setAttr -k on ".w0";
createNode joint -n "adj_cheek_L_003_jnt" -p "adj_jnt_grp";
	rename -uid "C032B119-49F3-976C-16B0-46B1134FB1BD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4853637218475342 8.9519538879394531 1.1591391563415527 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_cheek_L_003_jnt_pointConstraint1" -p "adj_cheek_L_003_jnt";
	rename -uid "B1A35C23-46DC-CBE2-9FDF-879BFBBBEBFF";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle137W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.011245489120483398 -0.0013980865478515625 0.0023975372314453125 ;
	setAttr ".rst" -type "double3" 2.4853637218475342 8.9519538879394531 1.1591391563415527 ;
	setAttr -k on ".w0";
createNode joint -n "adj_noseWing_R_002_jnt" -p "adj_jnt_grp";
	rename -uid "7AD7FD80-40E2-C417-9361-1ABFFCA99E67";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.68406599999999995 9.1593199999999992 4.1463999999999999 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_noseWing_R_002_jnt_pointConstraint1" -p "adj_noseWing_R_002_jnt";
	rename -uid "5C551A17-405C-7F17-FBF4-889A2457D85F";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle151W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.054817202106475782 -0.02642523925781326 0.042610193634033067 ;
	setAttr ".rst" -type "double3" -0.684066 9.15932 4.1464 ;
	setAttr -k on ".w0";
createNode joint -n "adj_zyg_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "BBDBBEF4-4E08-2587-BD0E-C3A47F4A1841";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.51471 9.1263500000000004 3.7214299999999993 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_zyg_R_001_jnt_pointConstraint1" -p "adj_zyg_R_001_jnt";
	rename -uid "73D9192B-43E9-111A-A8AA-B79841E0E374";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle135W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.012212803802490235 -0.0038007949829097498 0.0090336167144768886 ;
	setAttr ".rst" -type "double3" -1.51471 9.12635 3.7214299999999993 ;
	setAttr -k on ".w0";
createNode joint -n "adj_zyg_R_003_jnt" -p "adj_jnt_grp";
	rename -uid "D523B8EE-4A6F-DB98-D0FA-08953C92EF6E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4689000000000001 9.8356200000000005 2.2802799999999994 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_zyg_R_003_jnt_pointConstraint1" -p "adj_zyg_R_003_jnt";
	rename -uid "EEC8F062-42AF-13FC-7C04-EA9CE714B9B3";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle136W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.008391653442382907 0.00019366943359422351 0.0017443955230707076 ;
	setAttr ".rst" -type "double3" -2.4689 9.83562 2.2802799999999994 ;
	setAttr -k on ".w0";
createNode joint -n "adj_cheek_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "187CF6BF-4EEE-D635-1DFD-6FB581ABDAD2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.78217 8.1650600000000004 2.7745600000000001 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_cheek_R_001_jnt_pointConstraint1" -p "adj_cheek_R_001_jnt";
	rename -uid "54642C03-4DA1-925B-A83C-78BB1E829EF7";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle139W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0025369501876830736 0.00071235137939495985 -0.0011009916687010346 ;
	setAttr ".rst" -type "double3" -1.78217 8.16506 2.77456 ;
	setAttr -k on ".w0";
createNode joint -n "adj_cheek_R_003_jnt" -p "adj_jnt_grp";
	rename -uid "73D63120-4F16-7F0D-1CC3-B1AF645A0E90";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.48536 8.9519500000000001 1.1591400000000001 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_cheek_R_003_jnt_pointConstraint1" -p "adj_cheek_R_003_jnt";
	rename -uid "B980F8BC-42FC-B4DB-BBF1-BF8A396C5DA1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle140W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.011242720947265639 -0.0013981597900389886 0.0023970695877075787 ;
	setAttr ".rst" -type "double3" -2.48536 8.95195 1.15914 ;
	setAttr -k on ".w0";
createNode joint -n "adj_noseBottom_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "51A2CDBC-4418-7CCB-D4FB-F587EC860449";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0001399647444486618 8.9019374847412109 4.3592944145202637 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_noseBottom_C_001_jnt_pointConstraint1" -p "adj_noseBottom_C_001_jnt";
	rename -uid "18FB9EA4-424E-3E24-46A1-ECBCAEDBDA28";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle152W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.00014638897846452892 -0.000331878662109375 0.00687408447265625 ;
	setAttr ".rst" -type "double3" 0.0001399647444486618 8.9019374847412109 4.3592944145202637 ;
	setAttr -k on ".w0";
createNode joint -n "adj_nosFlo_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "A10A5F5F-4298-5B8B-2437-3E879BC92473";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.55797863006591797 9.5878200531005859 4.4003925323486328 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_nosFlo_L_001_jnt_pointConstraint1" -p "adj_nosFlo_L_001_jnt";
	rename -uid "9CAE59FD-4435-0DB8-EDD8-3CB20E3936A0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle141W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.040563821792602539 -0.0017566680908203125 0.018890380859375 ;
	setAttr ".rst" -type "double3" 0.55797863006591797 9.5878200531005859 4.4003925323486328 ;
	setAttr -k on ".w0";
createNode joint -n "adj_nosFlo_L_003_jnt" -p "adj_jnt_grp";
	rename -uid "01CC7803-4F96-4B85-2E7B-EA86C171AE4F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3591451644897461 8.2802190780639648 3.5942158699035645 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_nosFlo_L_003_jnt_pointConstraint1" -p "adj_nosFlo_L_003_jnt";
	rename -uid "7E250BC4-4DA1-34B0-C6B4-1985DC0BA590";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle142W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.012271642684936523 -0.0048818588256835938 0.013617038726806641 ;
	setAttr ".rst" -type "double3" 1.3591451644897461 8.2802190780639648 3.5942158699035645 ;
	setAttr -k on ".w0";
createNode joint -n "adj_nosFlo_L_005_jnt" -p "adj_jnt_grp";
	rename -uid "223A8CA9-4303-D011-8E4D-2FB42A9EAE48";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.88336926698684692 7.448793888092041 3.6904635429382324 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_nosFlo_L_005_jnt_pointConstraint1" -p "adj_nosFlo_L_005_jnt";
	rename -uid "7CCAA1FD-4605-9234-A9FA-D5B2B5B2C6AE";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle143W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0016186833381652832 -0.00052738189697265625 0.0018444061279296875 ;
	setAttr ".rst" -type "double3" 0.88336926698684692 7.448793888092041 3.6904635429382324 ;
	setAttr -k on ".w0";
createNode joint -n "adj_nosFlo_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "3DF34528-42C9-A709-A625-1A8DC9741B1B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.557979 9.5878200000000007 4.4003899999999998 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_nosFlo_R_001_jnt_pointConstraint1" -p "adj_nosFlo_R_001_jnt";
	rename -uid "BE8FBC06-4267-98A1-C6C3-14A2E8A8BAD1";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle147W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.040563238052368167 -0.0017567211914055747 0.018889755859374802 ;
	setAttr ".rst" -type "double3" -0.557979 9.58782 4.40039 ;
	setAttr -k on ".w0";
createNode joint -n "adj_nosFlo_R_003_jnt" -p "adj_jnt_grp";
	rename -uid "62C55F9C-45D9-E6B6-37F0-49A47DE40D0E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3591500000000001 8.2802199999999999 3.59422 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_nosFlo_R_003_jnt_pointConstraint1" -p "adj_nosFlo_R_003_jnt";
	rename -uid "39834B36-4FFA-512F-936C-12AE9CC7D81C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle146W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.012275405311584553 -0.0048828442382813364 0.01362140724182126 ;
	setAttr ".rst" -type "double3" -1.35915 8.28022 3.59422 ;
	setAttr -k on ".w0";
createNode joint -n "adj_nosFlo_R_005_jnt" -p "adj_jnt_grp";
	rename -uid "2A1F80CB-41BB-3B59-9F62-C193A64DEA21";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.88336899999999996 7.4487900000000007 3.6904599999999994 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_nosFlo_R_005_jnt_pointConstraint1" -p "adj_nosFlo_R_005_jnt";
	rename -uid "D3195593-4913-2975-CF19-CA97DA71E831";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle145W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0016173434677123621 -0.00052697845458915538 0.0018430089569085872 ;
	setAttr ".rst" -type "double3" -0.883369 7.4487900000000007 3.6904599999999994 ;
	setAttr -k on ".w0";
createNode joint -n "adj_lipChin_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "CD0D0E86-40DE-F471-30FD-1993C6026ADF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00015288963913917542 7.3639101982116699 4.0173206329345703 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_lipChin_C_001_jnt_pointConstraint1" -p "adj_lipChin_C_001_jnt";
	rename -uid "529B0B43-4AFA-A934-C50B-36B88EF8D798";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle144W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.014262977987527847 0.020977973937988281 -0.083605289459228516 ;
	setAttr ".rst" -type "double3" 0.00015288963913917542 7.3639101982116699 4.0173206329345703 ;
	setAttr -k on ".w0";
createNode joint -n "adj_mouth_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "CD0C30B4-46AE-A0EA-D766-E4B73BE132A8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.99284723180255674 8.0885326186972737 3.7272114197051991 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_mouth_L_001_jnt_pointConstraint1" -p "adj_mouth_L_001_jnt";
	rename -uid "168EA964-4858-33F7-A508-41A1DDEEA545";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle154W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.015049310746576561 0.0086585800009846281 -0.032805021640015752 ;
	setAttr ".rst" -type "double3" 0.99284723180255674 8.0885326186972737 3.7272114197051991 ;
	setAttr -k on ".w0";
createNode joint -n "adj_mouth_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "E78386A2-4C57-2A74-59F1-B891808BCD13";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.99284700000000004 8.0885300000000004 3.7272099999999999 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_mouth_R_001_jnt_pointConstraint1" -p "adj_mouth_R_001_jnt";
	rename -uid "87B6D698-4A82-A11A-0C88-F3B5188B38E6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle156W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.015050615432739223 0.0086569149780277854 -0.032805487670898525 ;
	setAttr ".rst" -type "double3" -0.992847 8.08853 3.72721 ;
	setAttr -k on ".w0";
createNode joint -n "adj_upLipFrame_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "03411421-4DF3-E9EF-4325-5AB3FF60DC5B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00013386458158493042 8.5648174285888672 4.3139505386352539 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_upLipFrame_C_001_jnt_pointConstraint1" -p "adj_upLipFrame_C_001_jnt";
	rename -uid "4CCE9656-4BCE-3D0E-47CD-A48FCF5CC4E0";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle153W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.0001338645815849215 0.001068115234375 -0.022101402282714844 ;
	setAttr ".rst" -type "double3" 0.00013386458158493042 8.5648174285888672 4.3139505386352539 ;
	setAttr -k on ".w0";
createNode joint -n "adj_lowLipFrame_C_001_jnt" -p "adj_jnt_grp";
	rename -uid "0C892BA0-498E-6A5E-C8F4-04A103E915D0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00014242157340049744 7.7093524932861328 4.1852841377258301 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_lowLipFrame_C_001_jnt_pointConstraint1" -p "adj_lowLipFrame_C_001_jnt";
	rename -uid "070AE7BE-4D85-A17F-6353-78A709FC1F88";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle155W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.0015649466076865792 0.0023016929626464844 -0.0091724395751953125 ;
	setAttr ".rst" -type "double3" 0.00014242157340049744 7.7093524932861328 4.1852841377258301 ;
	setAttr -k on ".w0";
createNode joint -n "adj_chin_L_002_jnt" -p "adj_jnt_grp";
	rename -uid "2C6D41ED-45AE-6A7F-394B-EBBC1D671CC2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1278786659240723 6.9100303649902344 3.181365966796875 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_chin_L_002_jnt_pointConstraint1" -p "adj_chin_L_002_jnt";
	rename -uid "BC382EF9-4662-FE67-2DBF-FFA0C152163D";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle163W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.028945803642272949 -0.0096435546875 0.01696014404296875 ;
	setAttr ".rst" -type "double3" 1.1278786659240723 6.9100303649902344 3.181365966796875 ;
	setAttr -k on ".w0";
createNode joint -n "adj_chin_R_002_jnt" -p "adj_jnt_grp";
	rename -uid "AA0ADC5E-48ED-5C8F-390E-B3B5592058CE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.12788 6.910029999999999 3.1813699999999994 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_chin_R_002_jnt_pointConstraint1" -p "adj_chin_R_002_jnt";
	rename -uid "78FDD30A-45C9-29C8-7B5D-31AEB42E8741";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle165W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.028948687438964837 -0.0096439196777353686 0.016961316223143896 ;
	setAttr ".rst" -type "double3" -1.12788 6.910029999999999 3.1813699999999994 ;
	setAttr -k on ".w0";
createNode joint -n "adj_chinNeck_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "AC3D98B2-4A36-F7EC-A18C-76ADAF2663C8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3214733600616455 8.2154808044433594 0.95036953687667847 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode pointConstraint -n "adj_chinNeck_L_001_jnt_pointConstraint1" -p "adj_chinNeck_L_001_jnt";
	rename -uid "ACDDB9C5-4BA8-85A2-160D-1788FF24BC3B";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle162W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" 0.062248468399047852 -0.022549629211425781 3.5762786865234375e-07 ;
	setAttr ".rst" -type "double3" 2.3214733600616455 8.2154808044433594 0.95036953687667847 ;
	setAttr -k on ".w0";
createNode joint -n "adj_chinNeck_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "95094C15-4D7D-0CC5-E60B-54BD4F4288BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3214700000000001 8.2154799999999994 0.95036999999999994 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode pointConstraint -n "adj_chinNeck_R_001_jnt_pointConstraint1" -p "adj_chinNeck_R_001_jnt";
	rename -uid "29957733-485E-044D-3670-70AC82B56F7C";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "follicle166W0" -dv 1 -min 0 -at "double";
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
	setAttr ".o" -type "double3" -0.062245823593139793 -0.022548526306152894 -1.3713836732875961e-08 ;
	setAttr ".rst" -type "double3" -2.32147 8.21548 0.95036999999999994 ;
	setAttr -k on ".w0";
createNode joint -n "adj_throat_C_002_jnt" -p "adj_jnt_grp";
	rename -uid "390D676C-4750-A695-1BAF-1294F11B5285";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.0001700669527053833 3.7229316234588623 1.3687072992324829 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0001700669527053833 3.7229316234588623 1.3687072992324829 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
createNode joint -n "adj_clavicleNeck_L_001_jnt" -p "adj_jnt_grp";
	rename -uid "715E37BB-4527-E2F0-E046-D08D4F96F609";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 2.2843880653381348 7.2621726989746094 0.2006085216999054 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843880653381348 7.2621726989746094 0.2006085216999054 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode joint -n "adj_clavicleNeck_R_001_jnt" -p "adj_jnt_grp";
	rename -uid "F7A0BBAD-4CC2-4A04-33ED-8E81EAABCF68";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -2.28439 7.26217 0.20060900000000004 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843900000000001 7.2621700000000002 0.20060900000000004 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode joint -n "adj_chinThroat_L_002_jnt" -p "adj_jnt_grp";
	rename -uid "122C1D44-469A-B861-1EBC-AC9DDBE3FD8C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.81796157360076904 5.6688408851623535 1.2600280046463013 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.81796157360076904 5.6688408851623535 1.2600280046463013 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode joint -n "adj_chinThroat_R_002_jnt" -p "adj_jnt_grp";
	rename -uid "38C38F8D-4125-15E9-CA83-6FA1F406C086";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -0.817962 5.66884 1.26003 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.81796199999999997 5.6688400000000003 1.26003 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode joint -n "adj_clavicleNeck_L_005_jnt" -p "adj_jnt_grp";
	rename -uid "28CBF0DE-4207-4993-89C0-1C8BD196AC65";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 2.6888468265533447 4.418698787689209 0.0003346707671880722 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.6888468265533447 4.418698787689209 0.0003346707671880722 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode joint -n "adj_clavicleNeck_R_005_jnt" -p "adj_jnt_grp";
	rename -uid "982978F6-4609-06D8-870A-42BE5FDBCD55";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -2.68885 4.4187 0.00033467100000006411 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.68885 4.4187000000000003 0.00033467100000006411 1;
	setAttr ".ds" 3;
	setAttr ".radi" 3.5;
	setAttr ".liw" yes;
createNode transform -n "fol_grp";
	rename -uid "014CCF4C-4F58-2C40-093D-139CE6741108";
	setAttr ".v" no;
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0.26923347 1 ;
createNode joint -n "facial_root" -p "fol_grp";
	rename -uid "61D0D59C-48BD-625C-6BC6-7FBE6599E4D4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 0.5;
createNode transform -n "fol_joints_grp" -p "fol_grp";
	rename -uid "C628AE00-4C75-1BCD-8280-64963637B25E";
createNode transform -n "brow_fol_grp" -p "fol_joints_grp";
	rename -uid "C3EF71BF-425F-4EDC-D20F-A5ABEF0CFACA";
createNode transform -n "follicle7" -p "brow_fol_grp";
	rename -uid "46509258-40CB-822F-D7E1-33AEF4DF75C6";
createNode follicle -n "follicleShape7" -p "follicle7";
	rename -uid "9B315D67-40F2-28FF-0333-EE9BC178BB42";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.038844510912895203;
	setAttr ".pv" 0.75642299652099609;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_R_003_jnt" -p "follicle7";
	rename -uid "615E9465-49D8-DAAE-6D76-FB8DF71C47D8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -4.1143799478504661e-09 -4.7656243395977071e-09 3.8262939483502123e-09 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2936375099999999 11.708099369999999 3.18370891 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle6" -p "brow_fol_grp";
	rename -uid "77479054-4123-373D-97CC-13A109AA8438";
createNode follicle -n "follicleShape6" -p "follicle6";
	rename -uid "7FEAB106-45F2-BE37-D888-61A8DF43CF7E";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.2346770316362381;
	setAttr ".pv" 0.60702383518218994;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_R_002_jnt" -p "follicle6";
	rename -uid "352F4CF9-4FD0-2721-94D4-8CABB5C443C9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.4602661124740735e-07 -3.9062500079012352e-07 3.1520080554514607e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3196300000000001 11.589600000000001 4.3698699999999988 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle5" -p "brow_fol_grp";
	rename -uid "CCD27B31-4370-1D13-428F-33BA902E38F5";
createNode follicle -n "follicleShape5" -p "follicle5";
	rename -uid "0D7F7B4B-4864-CBE2-3C5E-03B6C7650B35";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.41469863057136536;
	setAttr ".pv" 0.24354882538318634;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_R_001_jnt" -p "follicle5";
	rename -uid "E9FAC9E3-40CC-79AA-59C1-C5BB0632BF8D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.3535003662876761e-08 4.882812554285465e-08 -1.6702270517754414e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.424261 11.301299999999999 4.566889999999999 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle4" -p "brow_fol_grp";
	rename -uid "7ED5A35A-4F8C-939C-C12B-4BAB6FDCD337";
createNode follicle -n "follicleShape4" -p "follicle4";
	rename -uid "4F93995C-402A-8533-B5CE-CC82BD9BF045";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.96115535497665405;
	setAttr ".pv" 0.75642299652099609;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_L_003_jnt" -p "follicle4";
	rename -uid "9058CE55-482A-385A-8C5B-A59DD7E91E8F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.1143799478504661e-09 -4.7656243395977071e-09 3.8262939483502123e-09 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2936375099999999 11.708099369999999 3.18370891 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle3" -p "brow_fol_grp";
	rename -uid "82FD914F-4828-C2A0-5F86-6DB6C11885AD";
createNode follicle -n "follicleShape3" -p "follicle3";
	rename -uid "A449C03D-4770-758E-E88B-1287F5D62E5C";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.76532226800918579;
	setAttr ".pv" 0.60706710815429688;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_L_002_jnt" -p "follicle3";
	rename -uid "C73732A7-4CD4-D9CB-1A01-4BA3B95CB7E0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.0297709330848761e-08 -1.7763568394002505e-15 -1.9686289220999242e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3196271154966632 11.589633941650392 4.3698666511290511 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle2" -p "brow_fol_grp";
	rename -uid "4262F84C-4B66-2C22-939F-3DA1C0C4ACEB";
createNode follicle -n "follicleShape2" -p "follicle2";
	rename -uid "CC7D2F88-42A1-AD82-82F8-A68351DA34A3";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.58530133962631226;
	setAttr ".pv" 0.24357891082763672;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_L_001_jnt" -p "follicle2";
	rename -uid "0D2447E8-4E22-8B12-4415-438F169ECED6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.9802322387695312e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.42426148056983948 11.301323890686035 4.5668916702270508 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle1" -p "brow_fol_grp";
	rename -uid "E6515123-490D-EABE-34DD-FB83D5A368DE";
createNode follicle -n "follicleShape1" -p "follicle1";
	rename -uid "0330593A-4D23-932D-A136-87863AD8B2DA";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50010406970977783;
	setAttr ".pv" 0.37382793426513672;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_brow_C_001_jnt" -p "follicle1";
	rename -uid "C4011CBB-4544-89CB-5895-8C8629AD12B1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.7269802834356598e-07 3.9902877446706952e-07 1.2206769817169061e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0005179278627931651 11.404634076679233 4.5836510780331858 1;
	setAttr ".radi" 2.7;
createNode transform -n "browLid_fol_grp" -p "fol_joints_grp";
	rename -uid "F5DC2369-4BB9-04BC-8CFA-C394A009AB5D";
createNode transform -n "follicle8" -p "browLid_fol_grp";
	rename -uid "FA45821C-4CD9-F616-CCAE-D69437634F65";
createNode follicle -n "follicleShape8" -p "follicle8";
	rename -uid "8F24B853-48AE-9379-FDC9-53B0E4D29C41";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.63219535350799561;
	setAttr ".pv" 0.32892990112304688;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_browLid_L_001_jnt" -p "follicle8";
	rename -uid "A9A325E8-4978-73EA-A8BA-97AB9A1188FD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.60751229524612427 10.947669982910156 4.1484169960021973 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle9" -p "browLid_fol_grp";
	rename -uid "6BC1DB95-41F6-2C43-F485-A2BFDF79819C";
createNode follicle -n "follicleShape9" -p "follicle9";
	rename -uid "02ADA9CF-4F9E-4F3D-DEAC-A6AC53C64470";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.78321027755737305;
	setAttr ".pv" 0.67107105255126953;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_browLid_L_002_jnt" -p "follicle9";
	rename -uid "1FF62C97-490B-7650-EFE7-EA93BD10596D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 2.9582805982641958e-08 0 4.9035536520136702e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3015105428506657 11.148630142211914 4.1128321184325092 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle10" -p "browLid_fol_grp";
	rename -uid "D6E83C00-4D0E-CC6A-99A6-888B1CFB0AF2";
createNode follicle -n "follicleShape10" -p "follicle10";
	rename -uid "3047F8DF-445E-08FD-1AED-A886BE4D6AA0";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.95795935392379761;
	setAttr ".pv" 0.62079626321792603;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_browLid_L_003_jnt" -p "follicle10";
	rename -uid "951645A2-4452-D423-627A-F6B7AAEF1E5E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.8857409491206454e-10 6.787104211980477e-10 -1.9787598226628234e-09 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1045808799999999 11.119100570000001 3.3660836199999999 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle11" -p "browLid_fol_grp";
	rename -uid "A56BC1BC-41FA-7309-C41F-1FA158FF9159";
createNode follicle -n "follicleShape11" -p "follicle11";
	rename -uid "CB21A5B8-4909-A184-7678-78850F2E9F67";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.36780458688735962;
	setAttr ".pv" 0.32898023724555969;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_browLid_R_001_jnt" -p "follicle11";
	rename -uid "6352BCD0-4E55-602D-A42B-DE9D66C26CA6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.7770996613440957e-09 -4.5318603447697114e-07 3.0039978016205282e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.60751200000000005 10.947699999999999 4.1484199999999989 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle12" -p "browLid_fol_grp";
	rename -uid "CEF1DA3B-41B0-B71D-E56E-F890EADBBB3A";
createNode follicle -n "follicleShape12" -p "follicle12";
	rename -uid "5D053B26-4CBB-2237-20E9-099C6546AB2E";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.21678979694843292;
	setAttr ".pv" 0.67101913690567017;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_browLid_R_002_jnt" -p "follicle12";
	rename -uid "9D424C9A-4029-1EDF-1403-95A4FE089A4F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.4282226556971978e-07 -3.7536621100286993e-07 -2.0693969737806128e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3015099999999999 11.1486 4.1128299999999989 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle13" -p "browLid_fol_grp";
	rename -uid "4338509F-425E-96F7-F79A-F1AA415D7527";
createNode follicle -n "follicleShape13" -p "follicle13";
	rename -uid "FC5CBBC3-47A8-4FA5-2E5D-DD8700DD1078";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.042040545493364334;
	setAttr ".pv" 0.62079626321792603;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_browLid_R_003_jnt" -p "follicle13";
	rename -uid "06243913-4A07-F418-70CD-99B9B158120F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.8857409491206454e-10 6.787104211980477e-10 -1.9787598226628234e-09 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1045808799999999 11.119100570000001 3.3660836199999999 1;
	setAttr ".radi" 2.7;
createNode transform -n "forehead_fol_grp" -p "fol_joints_grp";
	rename -uid "2E35B5F8-41F5-36B7-D8A6-12B1EFD4C486";
createNode transform -n "follicle14" -p "forehead_fol_grp";
	rename -uid "EB730E49-4976-2D02-12FA-4EA16C0A2ACB";
createNode follicle -n "follicleShape14" -p "follicle14";
	rename -uid "C211AC48-42FD-FB86-4D3F-AC85B758528E";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.93281716108322144;
	setAttr ".pv" 0.83271694183349609;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_forehead_L_002_jnt" -p "follicle14";
	rename -uid "51F8ACAC-46DF-235F-98E1-E1BB6C534ABF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.22535110946842e-08 1.980021870906512e-07 1.5377591378040734e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2662715789330123 12.820293228511485 4.1008545505959821 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle15" -p "forehead_fol_grp";
	rename -uid "559C519D-443B-85EA-2252-F58614F3C859";
createNode follicle -n "follicleShape15" -p "follicle15";
	rename -uid "449BF6A2-419C-DF66-39CC-92ACFF969EB0";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.06718338280916214;
	setAttr ".pv" 0.83272272348403931;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_forehead_R_002_jnt" -p "follicle15";
	rename -uid "D7677F80-44DF-71D5-8C0D-4D879E8D98E6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.7743530280116602e-08 1.0223388713370696e-07 -4.3968200689192827e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.26627 12.8203 4.1008499999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle16" -p "forehead_fol_grp";
	rename -uid "D97AE4A4-4FF3-E11D-DBB0-329C07293921";
createNode follicle -n "follicleShape16" -p "follicle16";
	rename -uid "302229D4-482E-0D7F-FFF1-4CB9E9D2FFE0";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50239026546478271;
	setAttr ".pv" 0.81110763549804688;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_forehead_C_002_jnt" -p "follicle16";
	rename -uid "959C190C-46F0-D34E-6DFD-C5BD8755FF7E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.103193830193308e-08 -8.320088618063437e-08 -2.0400502531714437e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.006993131192672742 12.795336806528523 4.3819678173877969 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle17" -p "forehead_fol_grp";
	rename -uid "B4E08ED6-4FA0-4CF3-B6A3-67A1E5CEBFBA";
createNode follicle -n "follicleShape17" -p "follicle17";
	rename -uid "C88ED58A-43CD-BA23-B28C-A6BF5F5EA8A3";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.066034913063049316;
	setAttr ".pv" 0.33892542123794556;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_forehead_R_001_jnt" -p "follicle17";
	rename -uid "E252971C-449B-1505-DF11-12812E85CD4A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.4708251989433734e-08 0 1.7681884756370891e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.26963 12.25 4.2430799999999991 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle18" -p "forehead_fol_grp";
	rename -uid "8EA0909A-42D6-638F-5D9C-DC8C0ED2F5B7";
createNode follicle -n "follicleShape18" -p "follicle18";
	rename -uid "3FB048EF-47D3-8144-FAA3-64AECE338B09";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.93396341800689697;
	setAttr ".pv" 0.33894443511962891;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_forehead_L_001_jnt" -p "follicle18";
	rename -uid "6F5DDEA5-465C-D847-F2F0-6282E68C1ADA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.354426302339732e-08 -1.7806683594301376e-07 1.3803610254825571e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2696250141666134 12.250022112576113 4.243078369847626 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle19" -p "forehead_fol_grp";
	rename -uid "D9EDD449-49C8-9150-AA1D-46BAFC5E1FC7";
createNode follicle -n "follicleShape19" -p "follicle19";
	rename -uid "B4A67BC7-41B0-7A01-E0EA-A8B714022CED";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50147068500518799;
	setAttr ".pv" 0.16728305816650391;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_forehead_C_001_jnt" -p "follicle19";
	rename -uid "057DF231-42FF-6A0F-BF7E-A8863AB1519F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.1142038451238454e-08 1.5422547505750117e-07 -8.6789121667152358e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0043026869075206385 12.051765287669056 4.4915656175565815 1;
	setAttr ".radi" 2.7;
createNode transform -n "eyeFrame_fol_grp" -p "fol_joints_grp";
	rename -uid "66DEC0B6-4A40-804C-7F1F-179AB6606C89";
createNode transform -n "follicle20" -p "eyeFrame_fol_grp";
	rename -uid "EB8BD11C-4465-3C11-7183-F7A98653AE97";
createNode follicle -n "follicleShape20" -p "follicle20";
	rename -uid "DFAFEEC0-44E7-C0E7-2427-80BE034DEFB9";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.59050410985946655;
	setAttr ".pv" 0.44112896919250488;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_L_001_jnt" -p "follicle20";
	rename -uid "3537170E-483E-7A33-F4D6-44AC5467172C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.48544615507125854 10.479743003845215 4.091270923614502 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle21" -p "eyeFrame_fol_grp";
	rename -uid "9E650C9A-4F82-5B71-3A4E-AF8CF9EE5A85";
createNode follicle -n "follicleShape21" -p "follicle21";
	rename -uid "ECC1A251-431D-93AA-5C28-B1A9F219FCFA";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.71409726142883301;
	setAttr ".pv" 0.09895392507314682;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_L_002_jnt" -p "follicle21";
	rename -uid "1D0B2F24-4333-1A17-00B4-9D956EBC77CE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -4.76837158203125e-07 -9.5367431640625e-07 -2.384185791015625e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1483757495880127 9.8116703033447266 3.9840564727783203 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle22" -p "eyeFrame_fol_grp";
	rename -uid "CE532F90-41AE-1EE1-47D3-F5A9078619D8";
createNode follicle -n "follicleShape22" -p "follicle22";
	rename -uid "1CF1D272-4CC5-A153-9BCD-06A2107AB74A";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.87613242864608765;
	setAttr ".pv" 0.15345598757266998;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_L_003_jnt" -p "follicle22";
	rename -uid "F2032434-4E76-2217-942C-C491284BEBA0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0174989700317383 9.9180812835693359 3.4735996723175049 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle23" -p "eyeFrame_fol_grp";
	rename -uid "C72AF72D-41EA-833A-FF08-58B0EE4B1D5A";
createNode follicle -n "follicleShape23" -p "follicle23";
	rename -uid "8A3ECB8E-4DCA-931A-2D33-80BA33C7464A";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.93427205085754395;
	setAttr ".pv" 0.35532450675964355;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_L_004_jnt" -p "follicle23";
	rename -uid "1CE076A0-4569-1F8D-8ED0-1294B3799C08";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.152557373046875e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3293492794036865 10.312215805053711 2.8753671646118164 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle24" -p "eyeFrame_fol_grp";
	rename -uid "4032F579-4C70-4796-A1BE-85BB8001313C";
createNode follicle -n "follicleShape24" -p "follicle24";
	rename -uid "26E3D31B-4186-6B67-E2EB-76A7BB8311F8";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.94274163246154785;
	setAttr ".pv" 0.68016648292541504;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_L_005_jnt" -p "follicle24";
	rename -uid "8B1E3753-4589-ECDF-9E41-49AA98458317";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.384185791015625e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3747775554656982 10.946447372436523 2.5630693435668945 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle25" -p "eyeFrame_fol_grp";
	rename -uid "D346C571-4A6C-FA80-8DDC-BD96AE6E86A5";
createNode follicle -n "follicleShape25" -p "follicle25";
	rename -uid "90A87BB5-4346-BAF5-6E62-D1BD1B750F80";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.40949580073356628;
	setAttr ".pv" 0.44110700488090515;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_R_001_jnt" -p "follicle25";
	rename -uid "DE00264F-4AA8-C9BA-212F-ECBEEB50EDAE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3742675769877764e-08 8.8500977213357146e-08 -9.2361450221289942e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.48544599999999999 10.479699999999999 4.0912699999999997 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle26" -p "eyeFrame_fol_grp";
	rename -uid "10E1F93E-47A4-DCBD-71F8-DDB0B885DBFB";
createNode follicle -n "follicleShape26" -p "follicle26";
	rename -uid "37F7236B-4E99-ADD0-8994-83BA9337D5FE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.28590169548988342;
	setAttr ".pv" 0.098953723907470703;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_R_002_jnt" -p "follicle26";
	rename -uid "87E3CDE5-4487-ACA3-0DBF-67A5EBC73E49";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.6033172611784607e-07 -6.5032958929123197e-07 3.2888031000766205e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.14838 9.8116699999999994 3.9840599999999995 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle27" -p "eyeFrame_fol_grp";
	rename -uid "F85FB94E-4CCE-8BF1-8164-329A55FBDE29";
createNode follicle -n "follicleShape27" -p "follicle27";
	rename -uid "F4FF6486-409B-8548-30FA-CDB69AF45DE0";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.12386729568243027;
	setAttr ".pv" 0.15345549583435059;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_R_003_jnt" -p "follicle27";
	rename -uid "6AC6114B-4E4B-BDAB-7302-7789335BAF5F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.6293945383554274e-08 3.2989501974611812e-07 3.276824944720147e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0175000000000001 9.9180799999999998 3.4735999999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle28" -p "eyeFrame_fol_grp";
	rename -uid "3E5703B9-46EC-3318-DB34-D282A19F14D4";
createNode follicle -n "follicleShape28" -p "follicle28";
	rename -uid "0EFBD4BC-42D0-E430-6A3A-F3BCBF144C37";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.065727531909942627;
	setAttr ".pv" 0.35531622171401978;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_R_004_jnt" -p "follicle28";
	rename -uid "4F5F992C-4BFA-5C78-0FA5-7CAEC439C832";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.3405759814495468e-09 -4.0740966866792405e-07 2.8353881833531602e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3293499999999998 10.312200000000001 2.8753699999999998 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle29" -p "eyeFrame_fol_grp";
	rename -uid "4F3F1024-4030-1B9A-0DD9-7C901ABE38A9";
createNode follicle -n "follicleShape29" -p "follicle29";
	rename -uid "D6B5A895-439A-C4D0-5459-0EA9689EC416";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.057257816195487976;
	setAttr ".pv" 0.68014204502105713;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_eyeFrame_R_005_jnt" -p "follicle29";
	rename -uid "D84C467A-43FC-4ABD-67E1-2D8CF5061695";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.0348510633190244e-08 -3.1127929744911853e-07 6.564331052061334e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3747799999999999 10.946400000000001 2.5630699999999997 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle30" -p "eyeFrame_fol_grp";
	rename -uid "4B484436-40DB-89EA-A763-D8AD36E162F5";
createNode follicle -n "follicleShape30" -p "follicle30";
	rename -uid "724093A6-435C-05A1-F537-B6AADB6A705B";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.96398061513900757;
	setAttr ".pv" 0.9010465145111084;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_bite_L_001_jnt" -p "follicle30";
	rename -uid "C415D055-435D-EE99-84BE-6D879D179BEF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.8350156888734546e-08 3.7638802830031182e-07 -1.0402665040487591e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.488699464537901 11.377700429276034 2.0811735543443213 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle31" -p "eyeFrame_fol_grp";
	rename -uid "85C7B215-4E48-2211-1343-87BF36EB3140";
createNode follicle -n "follicleShape31" -p "follicle31";
	rename -uid "1C3D078D-4050-AB81-C31C-09ACD47455B6";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.036019116640090942;
	setAttr ".pv" 0.9010465145111084;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_bite_R_001_jnt" -p "follicle31";
	rename -uid "E0256A1D-4085-1DCD-987B-11B2A86312E7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.5144348131101992e-07 8.0566406168713911e-07 -3.6583709719373303e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4887000000000001 11.377700000000001 2.0811699999999997 1;
	setAttr ".radi" 2.7;
createNode transform -n "lowlid_fol_grp" -p "fol_joints_grp";
	rename -uid "FFF0BFE3-4B8B-CBBF-1401-368CEB7FCAC0";
createNode transform -n "follicle32" -p "lowlid_fol_grp";
	rename -uid "5D5974D0-4BF8-9F91-A54D-F5929CD03471";
createNode follicle -n "follicleShape32" -p "follicle32";
	rename -uid "A5886CBA-4373-78D3-9E9B-1CBE54FBF2EC";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.78367424011230469;
	setAttr ".pv" 0.447845458984375;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowlid_L_001_jnt" -p "follicle32";
	rename -uid "FE0F7094-4409-7108-3D6F-178BEA992023";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -1.1920928955078125e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.0851883888244629 10.452959060668945 3.9599666595458984 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle33" -p "lowlid_fol_grp";
	rename -uid "D9DD0982-455F-52BC-8CB4-FA8F80AE1635";
createNode follicle -n "follicleShape33" -p "follicle33";
	rename -uid "88D22E53-4E21-A9C3-7C47-53B1D4B96DFC";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.87559717893600464;
	setAttr ".pv" 0.4138527512550354;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowlid_L_002_jnt" -p "follicle33";
	rename -uid "40813542-48A8-4F09-C492-79AA791E9FC6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.4368371963500977 10.437089920043945 3.866206169128418 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle34" -p "lowlid_fol_grp";
	rename -uid "5A272E00-47A9-9C6E-40EF-14AAB0FB3C7E";
createNode follicle -n "follicleShape34" -p "follicle34";
	rename -uid "B8F6467D-4B6F-75BD-6B63-8EBBE8994E6C";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.94949644804000854;
	setAttr ".pv" 0.58614742755889893;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowlid_L_003_jnt" -p "follicle34";
	rename -uid "46BB5E96-4261-3FBC-91E6-AF8A76141DC6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1920928955078125e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7195367813110352 10.517522811889648 3.7072761058807373 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle35" -p "lowlid_fol_grp";
	rename -uid "4AF8DAF2-4973-C9DE-0CB4-729EA933B1D9";
createNode follicle -n "follicleShape35" -p "follicle35";
	rename -uid "5DD186CF-4688-920A-3824-628F20D47DBC";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.2163253128528595;
	setAttr ".pv" 0.4479353129863739;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowlid_R_001_jnt" -p "follicle35";
	rename -uid "F067BAEB-4E58-3227-DAEC-F2945F52B057";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -5.7754516502583897e-08 1.0223388677843559e-06 3.3404541013304367e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0851900000000001 10.452999999999999 3.9599699999999998 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle36" -p "lowlid_fol_grp";
	rename -uid "5BECEC99-40D8-DD47-826F-908E3325343C";
createNode follicle -n "follicleShape36" -p "follicle36";
	rename -uid "89865812-4FC2-F01A-0371-8FB8CA7B8FDA";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.12440208345651627;
	setAttr ".pv" 0.41387516260147095;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowlid_R_002_jnt" -p "follicle36";
	rename -uid "2AFF7DFB-4C0B-4CA3-FB67-F19EFB6951F4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.7373046979947162e-08 4.1046142662537477e-07 3.8308715817336747e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4368399999999999 10.437099999999999 3.8662099999999997 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle37" -p "lowlid_fol_grp";
	rename -uid "E38AD621-4634-F74A-4A44-59B33FEFDB33";
createNode follicle -n "follicleShape37" -p "follicle37";
	rename -uid "E297103C-48F3-D49B-36CF-2286C61038D4";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.05050273984670639;
	setAttr ".pv" 0.58609825372695923;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowlid_R_003_jnt" -p "follicle37";
	rename -uid "85940ED2-43C7-3BFA-E52B-EDB9D1276AFC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.8147041081515454e-11 -7.6293945383554274e-08 3.8941192621599896e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7195400000000001 10.5175 3.7072799999999995 1;
	setAttr ".radi" 2.7;
createNode transform -n "nose_fol_grp" -p "fol_joints_grp";
	rename -uid "890F8D23-4D5B-7284-EA5B-4D8AB86B209D";
createNode transform -n "follicle38" -p "nose_fol_grp";
	rename -uid "87A6170F-4F73-B113-3D64-E183279E84C0";
createNode follicle -n "follicleShape38" -p "follicle38";
	rename -uid "8152F302-451C-1EA6-7FD5-85929BF16B06";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.5020211935043335;
	setAttr ".pv" 0.91094350814819336;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseRoot_C_001_jnt" -p "follicle38";
	rename -uid "20FBB2A6-49A7-C953-6374-D69A0C04A841";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2673282571317871e-08 9.7383093589087366e-08 6.2263528555206449e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0035460485101228433 10.684953592192102 4.4166141178970735 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle39" -p "nose_fol_grp";
	rename -uid "B5FB1987-426D-2204-3C1F-1FAFBBE09167";
createNode follicle -n "follicleShape39" -p "follicle39";
	rename -uid "2E02B928-49F8-B968-7314-D5BDB6C1B1FB";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50000011920928955;
	setAttr ".pv" 0.22372531890869141;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseTip_C_001_jnt" -p "follicle39";
	rename -uid "56570EAF-4F5B-7161-F337-1C9AE59E6009";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 9.1940898895263672 4.9873991012573242 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle40" -p "nose_fol_grp";
	rename -uid "2C90D22E-49CD-21C6-7AD8-6A80F3DCF9E9";
createNode follicle -n "follicleShape40" -p "follicle40";
	rename -uid "65159BDF-407F-DEC3-C559-20AE54F591C6";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50007987022399902;
	setAttr ".pv" 0.089056462049484253;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseBottom_C_001_jnt" -p "follicle40";
	rename -uid "870AE75D-4063-37FF-BA78-A0AF8BA43D93";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.2107193470001221e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0001399647444486618 8.9019374847412109 4.3592944145202637 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle41" -p "nose_fol_grp";
	rename -uid "8CBD8B6A-4B96-D741-2FEE-29B7DDC8A2F8";
createNode follicle -n "follicleShape41" -p "follicle41";
	rename -uid "E5898B0B-498C-EFFA-4FC4-58A8B67D35BD";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.69420641660690308;
	setAttr ".pv" 0.11075830459594727;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseWing_L_001_jnt" -p "follicle41";
	rename -uid "D2EBBF4B-4141-1ED5-6AB2-BD80910C2B67";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.9802322387695312e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.34074118733406067 8.9490175247192383 4.2669734954833984 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle42" -p "nose_fol_grp";
	rename -uid "9D513D1E-43EC-8763-5EFE-04B19C8CC3AF";
createNode follicle -n "follicleShape42" -p "follicle42";
	rename -uid "0343B9F7-4729-290D-AF8B-06B7207FB0FE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.8898853063583374;
	setAttr ".pv" 0.20769955217838287;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseWing_L_002_jnt" -p "follicle42";
	rename -uid "B5651AEF-4C81-4468-974A-04893F42B187";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.9604644775390625e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.68406617641448975 9.1593236923217773 4.1463994979858398 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle43" -p "nose_fol_grp";
	rename -uid "0551A478-4AB5-D8A7-AE5A-63B27650629E";
createNode follicle -n "follicleShape43" -p "follicle43";
	rename -uid "E4AAAA61-4054-E6C1-0904-FBA712B1612E";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.30579397082328796;
	setAttr ".pv" 0.11075963079929352;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseWing_R_001_jnt" -p "follicle43";
	rename -uid "842D3F03-40CE-578A-E265-EE83A13E765B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -8.5201263266831972e-09 3.857421866371169e-07 -3.4954833987299594e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.34074100000000002 8.9490200000000009 4.2669699999999997 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle44" -p "nose_fol_grp";
	rename -uid "5341732C-42AB-B91B-CD2F-AE81E6DC1444";
createNode follicle -n "follicleShape44" -p "follicle44";
	rename -uid "E23D65B9-4107-A3AB-DEF0-9EB161BE2969";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.11011505872011185;
	setAttr ".pv" 0.20769777894020081;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_noseWing_R_002_jnt" -p "follicle44";
	rename -uid "6E761E5E-4F99-CA5A-659E-B7A66421A2DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3994445319530655e-09 -1.2237548752125349e-07 5.0201416001982579e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.68406599999999995 9.1593199999999992 4.1463999999999999 1;
	setAttr ".radi" 2.7;
createNode transform -n "nosFlo_fol_grp" -p "fol_joints_grp";
	rename -uid "CB929A03-4D5A-0649-9E12-D8A9230082BD";
createNode transform -n "follicle45" -p "nosFlo_fol_grp";
	rename -uid "707FE80E-4B78-53C9-A947-1ABBACD7E3F7";
createNode follicle -n "follicleShape45" -p "follicle45";
	rename -uid "F0ECA0B3-4A51-4014-76D3-4D99773EE4CE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.5000491738319397;
	setAttr ".pv" 0.074014782905578613;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lipChin_C_001_jnt" -p "follicle45";
	rename -uid "DBA87D07-4842-10A5-1671-D387EDEE22F7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.9330992624163628e-09 4.76837158203125e-07 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00015288963913917542 7.3639101982116699 4.0173206329345703 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle46" -p "nosFlo_fol_grp";
	rename -uid "F8E0F54A-462F-CD55-E5CE-6EB0612EAB11";
createNode follicle -n "follicleShape46" -p "follicle46";
	rename -uid "5AF6B008-458D-E20A-658F-868C5B6F004A";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.67972111701965332;
	setAttr ".pv" 0.92598605155944824;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_L_001_jnt" -p "follicle46";
	rename -uid "8678D1A1-4765-97AD-9D65-559E75604D18";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 1.1920928955078125e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.55797863006591797 9.5878200531005859 4.4003925323486328 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle47" -p "nosFlo_fol_grp";
	rename -uid "906916E8-4B16-EAE2-A86D-BA8E722B9A4B";
createNode follicle -n "follicleShape47" -p "follicle47";
	rename -uid "93E11749-433D-01D4-21A1-95B804D611AC";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.81543654203414917;
	setAttr ".pv" 0.75728905200958252;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_L_002_jnt" -p "follicle47";
	rename -uid "030833E3-4379-4260-934B-94A478CE7446";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1920928955078125e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.97933292388916016 9.1474685668945312 4.0290870666503906 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle48" -p "nosFlo_fol_grp";
	rename -uid "D184591C-4F6D-7B49-32DA-2A917FA58105";
createNode follicle -n "follicleShape48" -p "follicle48";
	rename -uid "A7B7ECBB-4B8C-51F5-7E17-E98544F22709";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.93777143955230713;
	setAttr ".pv" 0.4250490665435791;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_L_003_jnt" -p "follicle48";
	rename -uid "191761AC-4321-B9CC-A0D4-1BB0EE8E2B17";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3591451644897461 8.2802190780639648 3.5942158699035645 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle49" -p "nosFlo_fol_grp";
	rename -uid "37D6E192-48EB-4F91-D057-D38B911BB0E3";
createNode follicle -n "follicleShape49" -p "follicle49";
	rename -uid "B2C7C111-42EC-9308-8BD1-B98A74941F4F";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.8571629524230957;
	setAttr ".pv" 0.19428026676177979;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_L_004_jnt" -p "follicle49";
	rename -uid "2305C118-4889-F3D4-F94F-21957C109D94";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1088805198669434 7.6778407096862793 3.5704183578491211 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle50" -p "nosFlo_fol_grp";
	rename -uid "8B1E7505-4098-7782-849A-4EAE3B65F3FE";
createNode follicle -n "follicleShape50" -p "follicle50";
	rename -uid "90BA2CAF-4C14-42F8-B970-1B873FDE195F";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.7845272421836853;
	setAttr ".pv" 0.10653328895568848;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_L_005_jnt" -p "follicle50";
	rename -uid "B4829E3E-4C04-BF51-BA05-7F9E55EE8FEE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.9604644775390625e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.88336926698684692 7.448793888092041 3.6904635429382324 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle51" -p "nosFlo_fol_grp";
	rename -uid "ADCC4501-4F61-756E-676E-C0A7F01EE79C";
createNode follicle -n "follicleShape51" -p "follicle51";
	rename -uid "78B696A4-47B5-8B5F-F6BC-2298183A18FE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.69156670570373535;
	setAttr ".pv" 0.076597094535827637;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lipChin_L_002_jnt" -p "follicle51";
	rename -uid "BE192C1B-4CFC-910B-DA0A-8BAC4C7DD568";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 4.76837158203125e-07 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.59475547075271606 7.3706507682800293 3.8599975109100342 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle52" -p "nosFlo_fol_grp";
	rename -uid "6015198E-4DE5-4B60-7E2E-A8A39C911DC7";
createNode follicle -n "follicleShape52" -p "follicle52";
	rename -uid "AD96D10D-410D-BC8A-718C-31B03D787FE0";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.59941238164901733;
	setAttr ".pv" 0.07401740550994873;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lipChin_L_001_jnt" -p "follicle52";
	rename -uid "8F2959B3-43C3-FDE1-FE92-14B36C6A3078";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.30864483118057251 7.363917350769043 3.9746146202087402 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle53" -p "nosFlo_fol_grp";
	rename -uid "474A0BDC-4B11-7E68-A2E1-2BB73C129DD5";
createNode follicle -n "follicleShape53" -p "follicle53";
	rename -uid "C49F0FA8-4726-23CF-7E12-5B99DE0663EE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.32027867436408997;
	setAttr ".pv" 0.92598605155944824;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_R_001_jnt" -p "follicle53";
	rename -uid "0A0E9DFA-48A6-E9EF-5093-8DAFE0B943C1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 7.1910858157053781e-08 5.3100585262200184e-08 -2.5323486330108835e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.557979 9.5878200000000007 4.4003899999999998 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle54" -p "nosFlo_fol_grp";
	rename -uid "F3994D07-4D65-52A3-BAF3-57B7A5915CF7";
createNode follicle -n "follicleShape54" -p "follicle54";
	rename -uid "D690DBDE-4360-2E53-F6E2-27921E0F7F00";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.18456368148326874;
	setAttr ".pv" 0.75728940963745117;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_R_002_jnt" -p "follicle54";
	rename -uid "E25F747C-4C7C-D27B-56B6-A996A14D3578";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.1057586670828528e-07 -4.7943115255577595e-07 2.933349609435254e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.97933300000000001 9.1474700000000002 4.0290900000000001 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle55" -p "nosFlo_fol_grp";
	rename -uid "F4FBBD62-42BF-C39A-9719-21865DE5BF53";
createNode follicle -n "follicleShape55" -p "follicle55";
	rename -uid "9A13B552-41BD-B08E-8C7C-108F0443238D";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.062226850539445877;
	setAttr ".pv" 0.42504942417144775;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_R_003_jnt" -p "follicle55";
	rename -uid "F572AE3A-40A6-C0F2-308F-7DB888619694";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.2070617595489921e-08 3.1738281336401997e-08 4.1300964355173164e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3591500000000001 8.2802199999999999 3.59422 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle56" -p "nosFlo_fol_grp";
	rename -uid "942E4D2D-4B54-80F9-1DEB-E4A74BA297B4";
createNode follicle -n "follicleShape56" -p "follicle56";
	rename -uid "E0864DCB-4254-5D43-71C6-5692FFC8ABE4";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.14283712208271027;
	setAttr ".pv" 0.19428008794784546;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_R_004_jnt" -p "follicle56";
	rename -uid "F9C888DB-4B40-E23C-C4DC-02BA8048BAE3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.3029785068426918e-08 2.3284912131771307e-07 1.6421508783892591e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1088800000000001 7.6778399999999998 3.5704199999999995 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle57" -p "nosFlo_fol_grp";
	rename -uid "096475E2-44A0-A3C0-C865-C3B9BA773392";
createNode follicle -n "follicleShape57" -p "follicle57";
	rename -uid "A8D0E914-4346-1CAD-9061-3D9AC77C83EE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.21547269821166992;
	setAttr ".pv" 0.106532022356987;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_nosFlo_R_005_jnt" -p "follicle57";
	rename -uid "5D4EEF2D-425A-2BAF-A752-A4AB5D64D622";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.8568267862461028e-08 5.502319329053762e-07 -3.5429382330143255e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.88336899999999996 7.4487900000000007 3.6904599999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle58" -p "nosFlo_fol_grp";
	rename -uid "6DD090F2-49E6-9779-3377-FC9E285D2F84";
createNode follicle -n "follicleShape58" -p "follicle58";
	rename -uid "44460D2C-40C6-CDE1-B7A7-35A59FE44F26";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.30843335390090942;
	setAttr ".pv" 0.076596543192863464;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lipChin_R_002_jnt" -p "follicle58";
	rename -uid "A7CFE5A8-4584-BDD9-5697-8C84526854DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.5689086947706699e-08 -1.8539428836561456e-07 2.4890899652518783e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.59475500000000003 7.3706500000000013 3.8599999999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle59" -p "nosFlo_fol_grp";
	rename -uid "EF000787-472C-E26D-C75C-BE85B2A2387B";
createNode follicle -n "follicleShape59" -p "follicle59";
	rename -uid "88DAB811-47CB-2B24-ACE8-1BA49CD0E34C";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.40058743953704834;
	setAttr ".pv" 0.074018508195877075;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lipChin_R_001_jnt" -p "follicle59";
	rename -uid "AE4B10FC-4865-BBC8-F7E9-04954A870B8B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -9.9945068332552012e-09 2.1179199194421017e-07 -4.6202087404800807e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.308645 7.3639200000000002 3.9746099999999998 1;
	setAttr ".radi" 2.7;
createNode transform -n "zyg_fol_grp" -p "fol_joints_grp";
	rename -uid "34C8D611-4F79-781E-2B57-368E4E3CD7D1";
createNode transform -n "follicle60" -p "zyg_fol_grp";
	rename -uid "27E27339-4E9C-4396-3052-DDA0CE7D0281";
createNode follicle -n "follicleShape60" -p "follicle60";
	rename -uid "81FF7AB6-4E21-9740-5DD1-9DAFDE1E0F2D";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.78449505567550659;
	setAttr ".pv" 0.17633152008056641;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_zyg_L_001_jnt" -p "follicle60";
	rename -uid "989728F7-407D-1727-789B-3E90C3EA3140";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.5147054195404053 9.1263513565063477 3.7214303016662598 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle61" -p "zyg_fol_grp";
	rename -uid "BDA2DBA9-4F91-1824-E7A4-40A98161F82F";
createNode follicle -n "follicleShape61" -p "follicle61";
	rename -uid "5B91F88C-408B-D886-3B7C-50B09B43C01D";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.87904024124145508;
	setAttr ".pv" 0.38360166549682617;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_zyg_L_002_jnt" -p "follicle61";
	rename -uid "A916EA10-4E09-3653-0A61-E28193EA0A6E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0180821418762207 9.353449821472168 3.154655933380127 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle62" -p "zyg_fol_grp";
	rename -uid "02E7498E-41F2-E52D-938F-18AB6351DD36";
createNode follicle -n "follicleShape62" -p "follicle62";
	rename -uid "838C2D9B-45D4-D553-F210-198511D27EF4";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.96371299028396606;
	setAttr ".pv" 0.82366943359375;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_zyg_L_003_jnt" -p "follicle62";
	rename -uid "04B97773-493F-A69C-89B4-F586084D8D24";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4688956737518311 9.8356170654296875 2.2802839279174805 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle63" -p "zyg_fol_grp";
	rename -uid "7D3A0EFE-4F5D-969A-0449-B79EDE46B1B8";
createNode follicle -n "follicleShape63" -p "follicle63";
	rename -uid "4B409C85-4437-EC83-2DDC-C09041CFA43C";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.21550433337688446;
	setAttr ".pv" 0.17633065581321716;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_zyg_R_001_jnt" -p "follicle63";
	rename -uid "9ED3ED4E-429F-DD97-E6A1-AB854269F056";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.0506591797727651e-08 4.0283203084356956e-07 -5.4008483951761832e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.51471 9.1263500000000004 3.7214299999999993 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle64" -p "zyg_fol_grp";
	rename -uid "F6E14AAB-45B7-B56D-31A2-69ACD2E36697";
createNode follicle -n "follicleShape64" -p "follicle64";
	rename -uid "73A1554C-4885-3483-0372-4BA583BFA89D";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.12096039950847626;
	setAttr ".pv" 0.38360252976417542;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_zyg_R_002_jnt" -p "follicle64";
	rename -uid "FD941092-4BFC-A9AA-FD3E-9387FC039565";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.8909910848872187e-09 7.7514648388898877e-07 4.0666198724004232e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0180799999999999 9.3534500000000005 3.1546599999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle65" -p "zyg_fol_grp";
	rename -uid "E1FBA4AD-4957-923A-3141-298A58645875";
createNode follicle -n "follicleShape65" -p "follicle65";
	rename -uid "CAF67560-4725-F754-2D6D-BEAFA28CD8B6";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.036286469548940659;
	setAttr ".pv" 0.82367205619812012;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_zyg_R_003_jnt" -p "follicle65";
	rename -uid "7F246221-4B50-F5E4-12F8-86B6BAC48563";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.4713745211689684e-08 -7.3547363754755679e-08 -3.9279174810502582e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4689000000000001 9.8356200000000005 2.2802799999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "cheek_fol_grp" -p "fol_joints_grp";
	rename -uid "0708663E-4483-462D-EAA2-0894B31C77FC";
createNode transform -n "follicle66" -p "cheek_fol_grp";
	rename -uid "4846E839-4A46-C51D-812C-D289531E03B9";
createNode follicle -n "follicleShape66" -p "follicle66";
	rename -uid "477CD90B-4C73-FC63-20C9-32A11991D380";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.83267289400100708;
	setAttr ".pv" 0.16466450691223145;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_cheek_L_001_jnt" -p "follicle66";
	rename -uid "EF407CB8-4AA3-9571-9F27-D3B1D3BE6B91";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7821712493896484 8.1650552749633789 2.7745559215545654 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle67" -p "cheek_fol_grp";
	rename -uid "741B354F-408B-C8C0-E9AB-2F898030E8C7";
createNode follicle -n "follicleShape67" -p "follicle67";
	rename -uid "F79615A7-4209-5C8F-3ED8-D89260DB7153";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.92179560661315918;
	setAttr ".pv" 0.48313260078430176;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_cheek_L_002_jnt" -p "follicle67";
	rename -uid "D6A0A682-47B0-5EE4-C1F6-B4BAFE006436";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2596127986907959 8.5387134552001953 1.9980354309082031 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle68" -p "cheek_fol_grp";
	rename -uid "AF65A6D8-426F-1CA5-7B8B-CCB67C5281AC";
createNode follicle -n "follicleShape68" -p "follicle68";
	rename -uid "D4121484-4B33-3183-6D6D-92A6CC637187";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.96393585205078125;
	setAttr ".pv" 0.83533644676208496;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_cheek_L_003_jnt" -p "follicle68";
	rename -uid "1515AB3C-4137-32E2-2643-03B43A191430";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4853637218475342 8.9519538879394531 1.1591391563415527 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle69" -p "cheek_fol_grp";
	rename -uid "E5A0A1CA-4623-1392-008B-64BCAE779FE2";
createNode follicle -n "follicleShape69" -p "follicle69";
	rename -uid "3B557EFA-4F5E-0792-8AC7-3EABDF74B4DC";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.16732729971408844;
	setAttr ".pv" 0.16466857492923737;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_cheek_R_001_jnt" -p "follicle69";
	rename -uid "0DE03EA8-4097-34C6-5289-93AA305684E3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.7296752897784131e-08 4.3334960508900622e-08 4.0784454347075894e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.78217 8.1650600000000004 2.7745600000000001 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle70" -p "cheek_fol_grp";
	rename -uid "0B872A62-4476-3BE6-F0BA-62A2DE7850D1";
createNode follicle -n "follicleShape70" -p "follicle70";
	rename -uid "6D3A2CB4-4800-2CFE-09FD-FBBB0DCEECF2";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.078204929828643799;
	setAttr ".pv" 0.4831293523311615;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_cheek_R_002_jnt" -p "follicle70";
	rename -uid "37DA96E8-4691-0275-6D8B-E1A098A21EE3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.2332153216715369e-08 -3.5949707033466893e-07 4.5690917969132272e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2596099999999999 8.53871 1.99804 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle71" -p "cheek_fol_grp";
	rename -uid "06C13EB3-4D4F-2539-A1A6-838408C13756";
createNode follicle -n "follicleShape71" -p "follicle71";
	rename -uid "67EC38EF-4BC4-09AC-6C8B-73A3B57B1455";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.036064829677343369;
	setAttr ".pv" 0.83533316850662231;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_cheek_R_003_jnt" -p "follicle71";
	rename -uid "DD6D1555-421F-1EF8-D689-7BBC06F2C066";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.2849731458954921e-08 7.3242187426103555e-08 8.4365844732481321e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.48536 8.9519500000000001 1.1591400000000001 1;
	setAttr ".radi" 2.7;
createNode transform -n "lip_fol_grp" -p "fol_joints_grp";
	rename -uid "86E03B5D-4FF6-A7ED-95FA-BC9BCBE70272";
createNode transform -n "follicle72" -p "lip_fol_grp";
	rename -uid "3373CA57-4403-4346-79A1-B9AF043E2141";
createNode follicle -n "follicleShape72" -p "follicle72";
	rename -uid "0B2CA38E-4D51-FCA8-D94B-AEB30E0570AE";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50005638599395752;
	setAttr ".pv" 0.845794677734375;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_upLipFrame_C_001_jnt" -p "follicle72";
	rename -uid "8BAB939E-4E7B-84FE-EC4A-F6AD880A0782";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.1807652451097965e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00013386458158493042 8.5648174285888672 4.3139505386352539 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle73" -p "lip_fol_grp";
	rename -uid "8B0B4643-4F15-97D4-7E36-2EA50D97BB0F";
createNode follicle -n "follicleShape73" -p "follicle73";
	rename -uid "B6BB9922-438F-E40B-FC3C-1FA285F6868F";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50006002187728882;
	setAttr ".pv" 0.16299533843994141;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowLipFrame_C_001_jnt" -p "follicle73";
	rename -uid "97200035-4B2C-C959-97AE-38A0F0893B02";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4034095481038094e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00014242157340049744 7.7093524932861328 4.1852841377258301 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle74" -p "lip_fol_grp";
	rename -uid "201BEFF0-4E2B-8FEF-AB24-D587D7F6EE4A";
createNode follicle -n "follicleShape74" -p "follicle74";
	rename -uid "45D97828-4D3C-716B-0241-08B8213B0BC8";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.69674074649810791;
	setAttr ".pv" 0.82814121246337891;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_upLipFrame_L_001_jnt" -p "follicle74";
	rename -uid "FAAEB2F8-452D-0620-DF55-348A9CB92D65";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.9802322387695312e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.46668782830238342 8.5426998138427734 4.2592430114746094 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle75" -p "lip_fol_grp";
	rename -uid "590777C7-4E4C-C1FB-B4FD-16B5AA696D78";
createNode follicle -n "follicleShape75" -p "follicle75";
	rename -uid "DECFC411-40F1-2FA0-C75E-128A795AB2E1";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.89659112691879272;
	setAttr ".pv" 0.7681422233581543;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_upLipFrame_L_002_jnt" -p "follicle75";
	rename -uid "E6F39704-4144-9090-66BE-D688FAD8B65F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.94075167179107666 8.4675283432006836 3.9406640529632568 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle76" -p "lip_fol_grp";
	rename -uid "1C4938BF-43C8-3C3A-7832-98A7EFE58ED3";
createNode follicle -n "follicleShape76" -p "follicle76";
	rename -uid "E32FB3ED-4E1C-712D-A100-D5A507C83318";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.9185529351234436;
	setAttr ".pv" 0.46564221382141113;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_mouth_L_001_jnt" -p "follicle76";
	rename -uid "C6C6FA28-41FA-6B10-7C0F-2CA51FF5918E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -8.7198827491974384e-08 -1.7088233228435001e-07 -5.5667115361757169e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.99284723180255674 8.0885326186972737 3.7272114197051991 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle77" -p "lip_fol_grp";
	rename -uid "990F0CA4-4626-46E4-D083-6E81F61F448D";
createNode follicle -n "follicleShape77" -p "follicle77";
	rename -uid "F3D1BDA2-444C-5119-D721-D99C1BB065CF";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.80591964721679688;
	setAttr ".pv" 0.21054649353027344;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowLipFrame_L_002_jnt" -p "follicle77";
	rename -uid "D8A05039-4A25-9F6A-4C16-96A4FE03E177";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.7256704568862915 7.7689285278320312 3.9046978950500488 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle78" -p "lip_fol_grp";
	rename -uid "4FCF73B1-4E0E-277A-8F41-DFA12FAA1A4C";
createNode follicle -n "follicleShape78" -p "follicle78";
	rename -uid "83535629-4658-8B8D-8EFD-439393201229";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.65970546007156372;
	setAttr ".pv" 0.15420436859130859;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowLipFrame_L_001_jnt" -p "follicle78";
	rename -uid "28108295-462D-2114-8B9C-229BBE36824C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.4857808840533835e-10 6.8085092319591922e-07 2.1322482179897406e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.37883636430257894 7.6983378277550338 4.0993888126205738 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle79" -p "lip_fol_grp";
	rename -uid "1F8B9219-4251-4FAB-D5A2-97B92EF36AFE";
createNode follicle -n "follicleShape79" -p "follicle79";
	rename -uid "F8929E61-4C8A-D131-4782-B490EAF50115";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.30325916409492493;
	setAttr ".pv" 0.82814115285873413;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_upLipFrame_R_001_jnt" -p "follicle79";
	rename -uid "C9D869FD-421C-B2EE-11DC-6E90CE2596A1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.4189529418118241e-07 -1.8615722652270961e-07 -3.0114746092380074e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.46668799999999999 8.5427 4.2592400000000001 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle80" -p "lip_fol_grp";
	rename -uid "1C851D16-4551-5B85-E54A-6FB1BE0E16D4";
createNode follicle -n "follicleShape80" -p "follicle80";
	rename -uid "1CA52684-4B02-13B2-4CF8-F595FBE9FCE0";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.10340876132249832;
	setAttr ".pv" 0.76814371347427368;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_upLipFrame_R_002_jnt" -p "follicle80";
	rename -uid "1DB94202-4232-2697-B717-B5B59E16FD3E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 8.9790344270923583e-08 2.5054931640511313e-07 -3.8145446779047631e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.94075200000000003 8.46753 3.9406599999999998 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle81" -p "lip_fol_grp";
	rename -uid "7465CA80-4F7A-997D-7028-259416F2FBFA";
createNode follicle -n "follicleShape81" -p "follicle81";
	rename -uid "7EDB5B63-4C78-FBDA-153B-5782F4400189";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.081447087228298187;
	setAttr ".pv" 0.46563988924026489;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_mouth_R_001_jnt" -p "follicle81";
	rename -uid "04092E1F-4490-A3ED-1B21-95A1BE82DF3C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -8.4999084437598071e-08 -4.1320800825417336e-07 -1.4753723145410902e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.99284700000000004 8.0885300000000004 3.7272099999999999 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle82" -p "lip_fol_grp";
	rename -uid "B9744F5F-4FEF-6874-393B-868154238B9E";
createNode follicle -n "follicleShape82" -p "follicle82";
	rename -uid "D9E7F51F-4495-54DA-C1F6-25A85BA9D2D5";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.19408048689365387;
	setAttr ".pv" 0.21054799854755402;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowLipFrame_R_002_jnt" -p "follicle82";
	rename -uid "E9D1F077-46E7-BAD1-9A9F-DF833308CFB2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.9653778038939436e-08 4.3518066306091896e-07 2.1049499507874714e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.72567000000000004 7.768930000000001 3.9046999999999996 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle83" -p "lip_fol_grp";
	rename -uid "49A522A8-4FF0-6C3A-6E3A-57ADD3B65162";
createNode follicle -n "follicleShape83" -p "follicle83";
	rename -uid "A0411134-4C9C-1636-AD60-CF9D970A4EB3";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.34029477834701538;
	setAttr ".pv" 0.15420587360858917;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_lowLipFrame_R_001_jnt" -p "follicle83";
	rename -uid "3A910B3B-464F-758A-A6DA-8BA395418714";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.3876190191618463e-08 4.1595458988297196e-07 1.4006042476921721e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.37883600000000001 7.69834 4.0993899999999996 1;
	setAttr ".radi" 2.7;
createNode transform -n "chin_fol_grp" -p "fol_joints_grp";
	rename -uid "AEC8C37B-45D7-AC6A-4B35-6082EEAE2D05";
createNode transform -n "follicle84" -p "chin_fol_grp";
	rename -uid "47D5B4F1-4909-8010-5E26-30A79A043153";
createNode follicle -n "follicleShape84" -p "follicle84";
	rename -uid "52D45985-4A22-A412-B34F-BCA05D1ADFC1";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50002652406692505;
	setAttr ".pv" 0.096532344818115234;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_C_001_jnt" -p "follicle84";
	rename -uid "98895622-4B08-6C92-BEA3-6B8B40168E59";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.0134182199835777e-08 0 -2.384185791015625e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00013379007577896118 6.6002101898193359 3.9838423728942871 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle85" -p "chin_fol_grp";
	rename -uid "BD937A59-4980-7115-8DED-87B8BF95837C";
createNode follicle -n "follicleShape85" -p "follicle85";
	rename -uid "3B31E19F-4C1A-2024-3918-3B9E55F4D3E2";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.58996361494064331;
	setAttr ".pv" 0.096518062055110931;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_L_001_jnt" -p "follicle85";
	rename -uid "51B748D9-4E78-DB2F-35F2-E6BE57E49E23";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.9604644775390625e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.45245867967605591 6.6001815795898438 3.9173324108123779 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle86" -p "chin_fol_grp";
	rename -uid "EA429975-4E40-E184-CD98-FE88A86F5325";
createNode follicle -n "follicleShape86" -p "follicle86";
	rename -uid "54FDC40C-4C60-98A3-8FAE-658998519679";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.72425937652587891;
	setAttr ".pv" 0.25131097435951233;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_L_002_jnt" -p "follicle86";
	rename -uid "2896D93F-4705-4005-2981-E3AE0F2FB782";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1920928955078125e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1278786659240723 6.9100303649902344 3.181365966796875 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle87" -p "chin_fol_grp";
	rename -uid "9896E171-4038-DCF0-FF81-4B9CA46FCC42";
createNode follicle -n "follicleShape87" -p "follicle87";
	rename -uid "98C92D27-45B8-C961-9458-17A0DDF65D97";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.81784778833389282;
	setAttr ".pv" 0.43541884422302246;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_L_003_jnt" -p "follicle87";
	rename -uid "142B2BF6-4587-E8DB-D61F-1882CFBD6A8B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 4.76837158203125e-07 -2.384185791015625e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.5985672473907471 7.2785587310791016 2.6469697952270508 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle88" -p "chin_fol_grp";
	rename -uid "5265F0BB-4310-AF42-C6C2-13A0782FE38F";
createNode follicle -n "follicleShape88" -p "follicle88";
	rename -uid "56F009BC-45C3-A37C-86D2-109E161B26FD";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.90082013607025146;
	setAttr ".pv" 0.64096915721893311;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_L_004_jnt" -p "follicle88";
	rename -uid "2E5DB5AF-4BE9-A095-F352-A9B05268F353";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0158641338348389 7.6900086402893066 1.8765504360198975 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle89" -p "chin_fol_grp";
	rename -uid "B2C14E34-453A-B1C4-5D95-029F183566C6";
createNode follicle -n "follicleShape89" -p "follicle89";
	rename -uid "84CA0129-4B68-7EDC-CC68-238E48D1059D";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.41003605723381042;
	setAttr ".pv" 0.096517547965049744;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_R_001_jnt" -p "follicle89";
	rename -uid "5DAD708A-43A0-90E4-FCBC-83B2A57C0679";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -6.3335037231437852e-07 6.2591552740798306e-07 -2.4108123781729773e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.452459 6.6001799999999999 3.9173299999999998 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle90" -p "chin_fol_grp";
	rename -uid "3BEB58EC-4D4E-9E44-2644-669F5C1BDE50";
createNode follicle -n "follicleShape90" -p "follicle90";
	rename -uid "2C0114CD-40D5-2447-7CE8-5CB2BFCB5C01";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.27574020624160767;
	setAttr ".pv" 0.25131094455718994;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_R_002_jnt" -p "follicle90";
	rename -uid "ABA47281-489D-85E8-EFEB-FF8127326328";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -9.643554688132383e-08 -1.1184692283450204e-07 4.2716217034666215e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.12788 6.910029999999999 3.1813699999999994 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle91" -p "chin_fol_grp";
	rename -uid "9AD42F05-4B9D-492E-C482-F5A3546A63E5";
createNode follicle -n "follicleShape91" -p "follicle91";
	rename -uid "338AC149-4E1E-4C57-77AE-6AB082B8DC76";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.18215152621269226;
	setAttr ".pv" 0.43541955947875977;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_R_003_jnt" -p "follicle91";
	rename -uid "F9536360-4DA6-0538-3E18-25A00C6CAA39";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.0795593308188245e-08 1.6159057736331306e-07 2.047729488197092e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.59857 7.2785599999999988 2.6469699999999996 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle92" -p "chin_fol_grp";
	rename -uid "958F0CC3-4917-F1F9-2677-369CBAD7D761";
createNode follicle -n "follicleShape92" -p "follicle92";
	rename -uid "93F5B13B-4901-70BB-83B3-5B876237DDA3";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.099180519580841064;
	setAttr ".pv" 0.64096987247467041;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chin_R_004_jnt" -p "follicle92";
	rename -uid "C656689D-4382-A9ED-7BE6-A293E343B4B6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -8.0718994155404289e-08 7.0800782125957085e-08 -4.3601989752062309e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.01586 7.6900099999999991 1.8765499999999999 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle93" -p "chin_fol_grp";
	rename -uid "C08FEE36-4CDF-1BB2-E410-2C821FC003C0";
createNode follicle -n "follicleShape93" -p "follicle93";
	rename -uid "10D00A9B-4862-443A-8591-09935A685E2B";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.96158522367477417;
	setAttr ".pv" 0.90348219871520996;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinNeck_L_001_jnt" -p "follicle93";
	rename -uid "BFF0157C-4863-0421-3467-40A5B0578221";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.384185791015625e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3214733600616455 8.2154808044433594 0.95036953687667847 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle94" -p "chin_fol_grp";
	rename -uid "21A96BB8-444D-237B-F164-65B866ADDFBF";
createNode follicle -n "follicleShape94" -p "follicle94";
	rename -uid "315F7274-4239-B2C1-B11C-A4852BBF92C4";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.038415279239416122;
	setAttr ".pv" 0.90348172187805176;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinNeck_R_001_jnt" -p "follicle94";
	rename -uid "D58F913D-44CE-2DC2-FA5C-42A36B2D2AE3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.1621704116014939e-07 -1.4923095648100571e-07 4.6312332158127134e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3214700000000001 8.2154799999999994 0.95037000000000005 1;
	setAttr ".radi" 2.7;
createNode transform -n "throat_fol_grp" -p "fol_joints_grp";
	rename -uid "F7302D24-4150-F4EF-09C9-7D8132B6A269";
createNode transform -n "follicle95" -p "throat_fol_grp";
	rename -uid "7CEC5B06-495E-BEDB-6A95-64ADC43864D5";
createNode follicle -n "follicleShape95" -p "follicle95";
	rename -uid "1012C82B-45BD-AFFA-57AE-5E86B749D280";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.49995297193527222;
	setAttr ".pv" 0.56098091602325439;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_throat_C_001_jnt" -p "follicle95";
	rename -uid "8CC3B734-46FB-F388-98F2-4E8DBE03D79C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4447217583656311e-09 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0001681596040725708 5.6298894882202148 1.5964155197143555 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle96" -p "throat_fol_grp";
	rename -uid "40C40EDF-4211-5962-16EA-4787AB722C36";
createNode follicle -n "follicleShape96" -p "follicle96";
	rename -uid "1E823BCB-4CBE-E24A-C63E-EA86DF837919";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.49982920289039612;
	setAttr ".pv" 0.33447545766830444;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_throat_C_003_jnt" -p "follicle96";
	rename -uid "7EA47B41-41F6-A509-E711-30843084E29B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.4453266784548759e-08 0 -1.1920928955078125e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00012038276327075437 4.5665569305419922 1.2402728796005249 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle97" -p "throat_fol_grp";
	rename -uid "5F698E0D-497A-FBBC-5A0C-5A9CD2EED592";
createNode follicle -n "follicleShape97" -p "follicle97";
	rename -uid "F499373D-415A-FD20-5525-43A4B0EDA917";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.49995803833007812;
	setAttr ".pv" 0.062325451523065567;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_throat_C_002_jnt" -p "follicle97";
	rename -uid "3E3B7EAB-41AD-1634-F40F-92B2F698A3FC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.5675627663731575e-08 0 -1.1920928955078125e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.0001700669527053833 3.7229316234588623 1.3687072992324829 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle98" -p "throat_fol_grp";
	rename -uid "3CD5FDFB-4B42-1234-AD72-6F9A294E39FD";
createNode follicle -n "follicleShape98" -p "follicle98";
	rename -uid "555923A7-476F-9031-083A-3F87CBC2BD4B";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50004899501800537;
	setAttr ".pv" 0.93767452239990234;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinThroat_C_001_jnt" -p "follicle98";
	rename -uid "32A06437-4843-1370-E851-6AAEA03DD363";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.4703483581542969e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00020532310009002686 6.4363861083984375 2.2802090644836426 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle99" -p "throat_fol_grp";
	rename -uid "443CABFF-4D0C-3201-B60A-27B1588205D9";
createNode follicle -n "follicleShape99" -p "follicle99";
	rename -uid "7BD730C0-4AFF-B1D8-52F2-A7BC77CB701B";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.50017118453979492;
	setAttr ".pv" 0.75391674041748047;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinThroat_C_002_jnt" -p "follicle99";
	rename -uid "567E3DFD-489D-37FB-633E-49BA8FD36BB6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.8545189201831818e-08 9.5367431640625e-07 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.000252552330493927 6.2460217475891113 1.785294771194458 1;
	setAttr ".radi" 2.7;
createNode transform -n "chinThroat_fol_grp" -p "fol_joints_grp";
	rename -uid "7D084B0A-4142-A136-5714-529C39E75B95";
createNode transform -n "follicle100" -p "chinThroat_fol_grp";
	rename -uid "A1B495E1-4E91-4E25-9D9D-098201BDC64A";
createNode follicle -n "follicleShape100" -p "follicle100";
	rename -uid "63D9D168-46C1-A292-0D67-DB84E76BDB1B";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.9334295392036438;
	setAttr ".pv" 0.88862848281860352;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinThroat_L_001_jnt" -p "follicle100";
	rename -uid "01745907-4C47-2ECA-B88F-C59BFDE67106";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.25789475440979 7.0171771049499512 1.4957858324050903 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle101" -p "chinThroat_fol_grp";
	rename -uid "8F9F2289-4302-F4AE-84B5-FEBA2841FCB9";
createNode follicle -n "follicleShape101" -p "follicle101";
	rename -uid "055F5552-48FD-A946-E0F5-DBA6E340F831";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.78184282779693604;
	setAttr ".pv" 0.11137139797210693;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinThroat_L_002_jnt" -p "follicle101";
	rename -uid "E9C95D4D-4078-6390-CA5E-31BA5890060A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -5.9604644775390625e-08 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.81796157360076904 5.6688408851623535 1.2600280046463013 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle102" -p "chinThroat_fol_grp";
	rename -uid "5F730BD2-4FF9-ACF4-A4F8-DEA2FF4AEDD4";
createNode follicle -n "follicleShape102" -p "follicle102";
	rename -uid "CBAC566E-4609-879B-C33B-6FA95DDC83DA";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.066572003066539764;
	setAttr ".pv" 0.88863009214401245;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinThroat_R_001_jnt" -p "follicle102";
	rename -uid "D17BC29D-4601-CE42-35F7-7892D4D45896";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.39617919447943e-08 -3.4027099360400825e-08 4.1675949093988862e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.25789 7.0171799999999998 1.4957899999999997 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle103" -p "chinThroat_fol_grp";
	rename -uid "198D099F-4275-393A-D7F1-E4BB86FE3971";
createNode follicle -n "follicleShape103" -p "follicle103";
	rename -uid "B1E31264-44BA-57C5-86C0-3CA30DA3F7CD";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.21815688908100128;
	setAttr ".pv" 0.11137082427740097;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_chinThroat_R_002_jnt" -p "follicle103";
	rename -uid "97A6F11A-4A30-79D9-2DBB-EBB31E8AA2AA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.1667174961784781e-09 -6.8511963213779836e-08 1.995353698713842e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.81796199999999997 5.6688400000000003 1.26003 1;
	setAttr ".radi" 2.7;
createNode transform -n "clavicleNeck_fol_grp" -p "fol_joints_grp";
	rename -uid "C86D2BC9-426A-E943-6B83-E4A91745DE35";
createNode transform -n "follicle104" -p "clavicleNeck_fol_grp";
	rename -uid "AFC0F2AE-424F-467D-8EC6-FBA23DA4B4BD";
createNode follicle -n "follicleShape104" -p "follicle104";
	rename -uid "D458BD15-4B53-140F-687F-C4B3325E1403";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.89631342887878418;
	setAttr ".pv" 0.94018334150314331;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_L_001_jnt" -p "follicle104";
	rename -uid "B8EDE28B-4FCC-9D1B-065C-C99223FDC449";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.384185791015625e-07 -4.76837158203125e-07 2.9802322387695312e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843880653381348 7.2621726989746094 0.2006085216999054 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle105" -p "clavicleNeck_fol_grp";
	rename -uid "8FEB2ECF-4A84-1E61-F79B-6F9FFEFFA25A";
createNode follicle -n "follicleShape105" -p "follicle105";
	rename -uid "12A7D16C-47DD-E5CA-1917-7199711E404A";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.88575023412704468;
	setAttr ".pv" 0.70075774192810059;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_L_002_jnt" -p "follicle105";
	rename -uid "2680F223-4217-AA25-132E-51B97423E7CE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0 -2.9802322387695312e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2235007286071777 6.4888582229614258 0.40176340937614441 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle106" -p "clavicleNeck_fol_grp";
	rename -uid "2E687C28-4B29-E11A-0F6F-D28FFEFA667B";
createNode follicle -n "follicleShape106" -p "follicle106";
	rename -uid "52B39019-4440-523A-2872-7882C627569D";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.87181365489959717;
	setAttr ".pv" 0.43094784021377563;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_L_003_jnt" -p "follicle106";
	rename -uid "B0534FBD-4FDE-DFB6-96F6-D390C65A5D6A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0 -5.9604644775390625e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1431691646575928 5.6174063682556152 0.64830487966537476 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle107" -p "clavicleNeck_fol_grp";
	rename -uid "C57F2C22-41D1-A344-764E-1BAA8B9AE6B2";
createNode follicle -n "follicleShape107" -p "follicle107";
	rename -uid "DA83C800-42C1-F1EB-31A1-15890E62CA02";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.78880661725997925;
	setAttr ".pv" 0.080863416194915771;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_L_004_jnt" -p "follicle107";
	rename -uid "3DC778AF-4462-1E47-F8E9-96BAD8F2F35E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.1920928955078125e-07 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6647086143493652 4.4866776466369629 1.0263814926147461 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle108" -p "clavicleNeck_fol_grp";
	rename -uid "76B5DD99-4B51-4F47-A6E6-50A6160AD264";
createNode follicle -n "follicleShape108" -p "follicle108";
	rename -uid "B272D289-408A-97F8-D657-3FBE82435EEB";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.96648210287094116;
	setAttr ".pv" 0.059816539287567139;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_L_005_jnt" -p "follicle108";
	rename -uid "94162CC9-4213-59BB-FF19-FEB6C7BD5C8E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 0 -6.891787052154541e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.6888468265533447 4.418698787689209 0.0003346707671880722 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle109" -p "clavicleNeck_fol_grp";
	rename -uid "F500F220-4A34-1F40-19C1-AFA04BDF5477";
createNode follicle -n "follicleShape109" -p "follicle109";
	rename -uid "8ADB2A4D-444D-97B1-5CD4-7985963CC765";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.10368610918521881;
	setAttr ".pv" 0.94018250703811646;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_R_001_jnt" -p "follicle109";
	rename -uid "314A41C2-493C-A3DE-E312-AA98CD453B32";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.7313232564551981e-08 -1.6204834007993441e-07 5.0810241700172121e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843900000000001 7.2621700000000002 0.20060900000000001 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle110" -p "clavicleNeck_fol_grp";
	rename -uid "C0C8140A-4FD7-DBE0-01A4-88894D4B102B";
createNode follicle -n "follicleShape110" -p "follicle110";
	rename -uid "F396684A-47B9-E813-687A-9EAA1F0F7632";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.11424974352121353;
	setAttr ".pv" 0.70075833797454834;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_R_002_jnt" -p "follicle110";
	rename -uid "E82683C9-4EE5-9F54-B71C-F191DE4D44BF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.5177001949927558e-07 1.3031005874353241e-07 -4.3917846676011507e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2235 6.4888599999999999 0.40176300000000004 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle111" -p "clavicleNeck_fol_grp";
	rename -uid "AED9B6C5-4B03-4FA5-BF26-3E829A11696A";
createNode follicle -n "follicleShape111" -p "follicle111";
	rename -uid "015489D7-472E-A707-9C93-A4B09225FED5";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.12818606197834015;
	setAttr ".pv" 0.43094903230667114;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_R_003_jnt" -p "follicle111";
	rename -uid "054CDD90-4DF9-BE6A-47C1-F497F3B737D0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.1833190916021863e-07 1.8295288128911125e-07 6.0729980488893887e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.14317 5.6174099999999996 0.64830500000000002 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle112" -p "clavicleNeck_fol_grp";
	rename -uid "4C1E1233-4A8A-0B4F-0257-4193E98336BB";
createNode follicle -n "follicleShape112" -p "follicle112";
	rename -uid "25959430-40B9-DE5A-6234-218FF476399E";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.21119305491447449;
	setAttr ".pv" 0.080864153802394867;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_R_004_jnt" -p "follicle112";
	rename -uid "DF3AA324-4FBE-76F8-E358-7BA5895375E5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.9355773916984731e-07 3.0822754126802465e-08 -1.4926147460236905e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6647099999999999 4.4866799999999998 1.0263800000000001 1;
	setAttr ".radi" 2.7;
createNode transform -n "follicle113" -p "clavicleNeck_fol_grp";
	rename -uid "F057D12B-405E-049B-7404-B0B407EC9111";
createNode follicle -n "follicleShape113" -p "follicle113";
	rename -uid "2B06883D-43D9-2F4A-D038-16B1D7014BFA";
	setAttr -k off ".v" no;
	setAttr ".pu" 0.033517256379127502;
	setAttr ".pv" 0.059816978871822357;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "fol_clavicleNeck_R_005_jnt" -p "follicle113";
	rename -uid "77CB1536-48BE-17A3-C59E-B2B82A679584";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.4005126915466235e-08 2.1820068329958531e-07 -6.8685058592088399e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -180 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.68885 4.4187000000000003 0.00033467100000000166 1;
	setAttr ".radi" 2.7;
createNode transform -n "mask_fol_grp" -p "fol_grp";
	rename -uid "841D7162-479F-4D62-9006-1C90369BED7D";
	setAttr ".v" no;
createNode transform -n "brow_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "D33ED3BB-46BE-2B92-05B6-54B0B4906D3A";
createNode transform -n "follicle114" -p "brow_mask_fol_grp";
	rename -uid "7EB8241E-4838-D0D8-159F-268C669316DF";
createNode follicle -n "follicleShape114" -p "follicle114";
	rename -uid "67B902A3-4B0E-A565-3BED-63A69D84A82B";
	setAttr -k off ".v";
	setAttr ".pu" 0.23230908811092377;
	setAttr ".pv" 0.78522753715515137;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle115" -p "brow_mask_fol_grp";
	rename -uid "EC7772F4-45C1-78D8-2AED-158322723B06";
createNode follicle -n "follicleShape115" -p "follicle115";
	rename -uid "A3744C21-4006-39A6-52B1-74A72A050687";
	setAttr -k off ".v";
	setAttr ".pu" 0.50044536590576172;
	setAttr ".pv" 0.74125689268112183;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle116" -p "brow_mask_fol_grp";
	rename -uid "A37AFF3B-4972-3994-4F63-75A294C660DA";
createNode follicle -n "follicleShape116" -p "follicle116";
	rename -uid "DB8B7117-4011-FF14-4A38-7DBC8976D004";
	setAttr -k off ".v";
	setAttr ".pu" 0.76773178577423096;
	setAttr ".pv" 0.78522753715515137;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "forehead_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "D4273C33-4CB1-AF3B-9BE0-88A294D0DA24";
createNode transform -n "follicle117" -p "forehead_mask_fol_grp";
	rename -uid "401033E1-4B6E-B61D-D70B-7E9D2FB8C62F";
createNode follicle -n "follicleShape117" -p "follicle117";
	rename -uid "5D45BE07-4C55-3B0A-559B-819BDD7A6057";
	setAttr -k off ".v";
	setAttr ".pu" 0.6415412425994873;
	setAttr ".pv" 0.9532923698425293;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle118" -p "forehead_mask_fol_grp";
	rename -uid "5F9911A9-4447-D9D2-DDC3-4AB6CD8FDE4F";
createNode follicle -n "follicleShape118" -p "follicle118";
	rename -uid "95CAA12E-4F73-E540-850B-458EE440D21D";
	setAttr -k off ".v";
	setAttr ".pu" 0.63208085298538208;
	setAttr ".pv" 0.86690819263458252;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle119" -p "forehead_mask_fol_grp";
	rename -uid "C7F04291-4540-EE52-9961-8EA919F5F2AD";
createNode follicle -n "follicleShape119" -p "follicle119";
	rename -uid "11D4141A-4895-7ED7-97F0-5292BF6C1872";
	setAttr -k off ".v";
	setAttr ".pu" 0.50064009428024292;
	setAttr ".pv" 0.83742696046829224;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle120" -p "forehead_mask_fol_grp";
	rename -uid "1FC8C962-4220-6D87-BDEB-25B086120237";
createNode follicle -n "follicleShape120" -p "follicle120";
	rename -uid "960E81C9-4870-3D02-8964-DFAFD960A31D";
	setAttr -k off ".v";
	setAttr ".pu" 0.36795946955680847;
	setAttr ".pv" 0.86690473556518555;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle121" -p "forehead_mask_fol_grp";
	rename -uid "C4101E08-4D70-CFCC-6B43-3C9C01279778";
createNode follicle -n "follicleShape121" -p "follicle121";
	rename -uid "27D200DE-4FD8-9A00-F370-EDB6EE6FEDB9";
	setAttr -k off ".v";
	setAttr ".pu" 0.35849955677986145;
	setAttr ".pv" 0.95329344272613525;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle122" -p "forehead_mask_fol_grp";
	rename -uid "EFC1B6C9-4E03-F759-E9B3-77AF602DB7CF";
createNode follicle -n "follicleShape122" -p "follicle122";
	rename -uid "2244D154-41D2-B50A-F132-2A82A26944E8";
	setAttr -k off ".v";
	setAttr ".pu" 0.50016075372695923;
	setAttr ".pv" 0.9477229118347168;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "lowlid_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "35C8665D-463C-4BA8-235E-1FB6C85E4CD8";
createNode transform -n "follicle123" -p "lowlid_mask_fol_grp";
	rename -uid "9429F807-4E29-AD44-11D2-22AD30E6D07D";
createNode follicle -n "follicleShape123" -p "follicle123";
	rename -uid "1C3A7558-41E9-8E3F-4C4C-D4927698B6CF";
	setAttr -k off ".v";
	setAttr ".pu" 0.63561660051345825;
	setAttr ".pv" 0.59626328945159912;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle124" -p "lowlid_mask_fol_grp";
	rename -uid "190E1CBA-4F73-F345-0AF1-F1B6CC3CA6A9";
createNode follicle -n "follicleShape124" -p "follicle124";
	rename -uid "A7D7562E-4B62-B6CB-3AA6-5D90331C8D46";
	setAttr -k off ".v";
	setAttr ".pu" 0.70193231105804443;
	setAttr ".pv" 0.60602271556854248;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle125" -p "lowlid_mask_fol_grp";
	rename -uid "617D3904-479C-CFDC-53B0-3BBECAC95333";
createNode follicle -n "follicleShape125" -p "follicle125";
	rename -uid "40E41019-4FB4-E9BE-1A98-1687D73607FB";
	setAttr -k off ".v";
	setAttr ".pu" 0.36442416906356812;
	setAttr ".pv" 0.59626936912536621;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle126" -p "lowlid_mask_fol_grp";
	rename -uid "2A75B393-48CF-C445-371A-A48CAB0CB654";
createNode follicle -n "follicleShape126" -p "follicle126";
	rename -uid "7E1D7A18-41BA-9215-994B-208ABA34103B";
	setAttr -k off ".v";
	setAttr ".pu" 0.29810863733291626;
	setAttr ".pv" 0.60601973533630371;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "eyeFrame_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "5809E942-4D81-801D-CFCA-009A237536A9";
createNode transform -n "follicle127" -p "eyeFrame_mask_fol_grp";
	rename -uid "5C3E1C88-47C5-2266-8DDD-D19F52CB23C8";
createNode follicle -n "follicleShape127" -p "follicle127";
	rename -uid "FB5B9B16-4FC1-64C8-4C1D-96B6A2072862";
	setAttr -k off ".v";
	setAttr ".pu" 0.86074984073638916;
	setAttr ".pv" 0.73560327291488647;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle128" -p "eyeFrame_mask_fol_grp";
	rename -uid "C27849A5-4DCE-A466-C474-5C9604A9CBB1";
createNode follicle -n "follicleShape128" -p "follicle128";
	rename -uid "7F2CC56C-415F-E1A4-6EBE-E185452CAA9C";
	setAttr -k off ".v";
	setAttr ".pu" 0.73584836721420288;
	setAttr ".pv" 0.51709276437759399;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle129" -p "eyeFrame_mask_fol_grp";
	rename -uid "CF64905F-451D-781D-4FCF-8E8D40A007B8";
createNode follicle -n "follicleShape129" -p "follicle129";
	rename -uid "5DE212CE-456F-47AF-D002-D8B4A09ED371";
	setAttr -k off ".v";
	setAttr ".pu" 0.55480533838272095;
	setAttr ".pv" 0.59712278842926025;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle130" -p "eyeFrame_mask_fol_grp";
	rename -uid "C0EEF230-4852-A3E3-56F3-68B208209F53";
createNode follicle -n "follicleShape130" -p "follicle130";
	rename -uid "3FCFFB41-4774-BD15-0257-0EA27471E2DA";
	setAttr -k off ".v";
	setAttr ".pu" 0.44523414969444275;
	setAttr ".pv" 0.59712183475494385;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle131" -p "eyeFrame_mask_fol_grp";
	rename -uid "7E58EAEF-4244-18E5-BB94-C7A749C74D64";
createNode follicle -n "follicleShape131" -p "follicle131";
	rename -uid "4915E7AF-4B92-D0EE-E201-B3BB7724214F";
	setAttr -k off ".v";
	setAttr ".pu" 0.26419246196746826;
	setAttr ".pv" 0.51709264516830444;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle132" -p "eyeFrame_mask_fol_grp";
	rename -uid "BB05FF0B-4CF9-3545-5573-11900292472F";
createNode follicle -n "follicleShape132" -p "follicle132";
	rename -uid "6986BDC9-489F-28C5-1E84-409F4268D780";
	setAttr -k off ".v";
	setAttr ".pu" 0.13929076492786407;
	setAttr ".pv" 0.73560315370559692;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "zyg_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "45E4FCE6-4ED1-3AB5-18BC-C3AECBB43B87";
createNode transform -n "follicle133" -p "zyg_mask_fol_grp";
	rename -uid "29B1CA5B-4128-812E-97C6-48A6AC2D3B07";
createNode follicle -n "follicleShape133" -p "follicle133";
	rename -uid "D7FCDBE6-41F2-2BC0-EEE1-8CB6187FB68A";
	setAttr -k off ".v";
	setAttr ".pu" 0.8454245924949646;
	setAttr ".pv" 0.50324064493179321;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle134" -p "zyg_mask_fol_grp";
	rename -uid "E641A22C-4BEB-7044-AE46-8EB16CD269BA";
createNode follicle -n "follicleShape134" -p "follicle134";
	rename -uid "DF1BAC8A-4376-6F17-C322-69842C50D998";
	setAttr -k off ".v";
	setAttr ".pu" 0.68852192163467407;
	setAttr ".pv" 0.3969913125038147;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle135" -p "zyg_mask_fol_grp";
	rename -uid "F0E711FB-46F8-1AF2-1A54-A0A2E725B9D4";
createNode follicle -n "follicleShape135" -p "follicle135";
	rename -uid "E8DF8550-45A2-A082-75FD-4C808C0CA5B9";
	setAttr -k off ".v";
	setAttr ".pu" 0.31151866912841797;
	setAttr ".pv" 0.39699161052703857;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle136" -p "zyg_mask_fol_grp";
	rename -uid "76EBE522-498A-2F95-46F0-A7ADE265C898";
createNode follicle -n "follicleShape136" -p "follicle136";
	rename -uid "5A2740DD-4D20-311E-1CE2-0C95B29BB0BF";
	setAttr -k off ".v";
	setAttr ".pu" 0.15461592376232147;
	setAttr ".pv" 0.50324106216430664;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "cheek_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "7EF65AA8-4813-908D-DD6F-5AAADF6D1FA6";
createNode transform -n "follicle137" -p "cheek_mask_fol_grp";
	rename -uid "99BF83AA-44AF-B1A2-5202-FD97D0061675";
createNode follicle -n "follicleShape137" -p "follicle137";
	rename -uid "560A4C29-4640-66A5-93F7-D59CA6ABDCF4";
	setAttr -k off ".v";
	setAttr ".pu" 0.92657679319381714;
	setAttr ".pv" 0.37035694718360901;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle138" -p "cheek_mask_fol_grp";
	rename -uid "60AE065C-4089-38D2-1FC2-66801F7049CF";
createNode follicle -n "follicleShape138" -p "follicle138";
	rename -uid "20565F3F-4A06-C021-1D3D-63ADD0058152";
	setAttr -k off ".v";
	setAttr ".pu" 0.79784905910491943;
	setAttr ".pv" 0.25149309635162354;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle139" -p "cheek_mask_fol_grp";
	rename -uid "2BA894A2-48BB-D117-1F71-7AAD586047A2";
createNode follicle -n "follicleShape139" -p "follicle139";
	rename -uid "8AE19513-461C-84D9-2902-5A9D72BF0EEB";
	setAttr -k off ".v";
	setAttr ".pu" 0.20219235122203827;
	setAttr ".pv" 0.25149381160736084;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle140" -p "cheek_mask_fol_grp";
	rename -uid "AD93ABAD-4684-AA0A-4D31-BBB8C6511501";
createNode follicle -n "follicleShape140" -p "follicle140";
	rename -uid "6396FDC1-4266-8F0A-5169-E0BE184A55A6";
	setAttr -k off ".v";
	setAttr ".pu" 0.073464184999465942;
	setAttr ".pv" 0.37035635113716125;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "nosFlo_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "EA15E71F-4365-5960-6B7B-7585A496FF41";
createNode transform -n "follicle141" -p "nosFlo_mask_fol_grp";
	rename -uid "638FF2F8-4574-312C-945E-ECA970DB9120";
createNode follicle -n "follicleShape141" -p "follicle141";
	rename -uid "4B8A8727-49F4-460A-23D2-1792EDD8E9EB";
	setAttr -k off ".v";
	setAttr ".pu" 0.56281286478042603;
	setAttr ".pv" 0.46620392799377441;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle142" -p "nosFlo_mask_fol_grp";
	rename -uid "DDF4780B-4E6C-83B8-FEC2-7DB70D96D435";
createNode follicle -n "follicleShape142" -p "follicle142";
	rename -uid "731602FA-41D6-B472-6393-A093C25FA8A5";
	setAttr -k off ".v";
	setAttr ".pu" 0.68929499387741089;
	setAttr ".pv" 0.26968523859977722;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle143" -p "nosFlo_mask_fol_grp";
	rename -uid "AF3A3BBB-4296-8CA1-5FA9-26B000C4138D";
createNode follicle -n "follicleShape143" -p "follicle143";
	rename -uid "61E7244E-42D7-B131-5783-C7B4568FAB82";
	setAttr -k off ".v";
	setAttr ".pu" 0.63663452863693237;
	setAttr ".pv" 0.14377538859844208;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle144" -p "nosFlo_mask_fol_grp";
	rename -uid "9CA057D8-4993-231D-5E98-2E95A8F0399F";
createNode follicle -n "follicleShape144" -p "follicle144";
	rename -uid "B966E162-4447-3A13-CCAB-9C9BDC73645B";
	setAttr -k off ".v";
	setAttr ".pu" 0.50187194347381592;
	setAttr ".pv" 0.12774792313575745;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle145" -p "nosFlo_mask_fol_grp";
	rename -uid "A70B83DB-432F-69B7-56CD-2398BC79AE1E";
createNode follicle -n "follicleShape145" -p "follicle145";
	rename -uid "B9328E5D-411B-6B62-13D0-1989B136ED94";
	setAttr -k off ".v";
	setAttr ".pu" 0.36340606212615967;
	setAttr ".pv" 0.14377473294734955;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle146" -p "nosFlo_mask_fol_grp";
	rename -uid "C274AABE-45B5-E2A0-CC7E-5A95BA6EC836";
createNode follicle -n "follicleShape146" -p "follicle146";
	rename -uid "661A91A2-43F9-2830-3C1A-769AE4B2A283";
	setAttr -k off ".v";
	setAttr ".pu" 0.31074580550193787;
	setAttr ".pv" 0.2696855366230011;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle147" -p "nosFlo_mask_fol_grp";
	rename -uid "7D87E3F4-412E-E3AB-725C-7F92EA687500";
createNode follicle -n "follicleShape147" -p "follicle147";
	rename -uid "E6A6702F-48FE-A7A9-0344-F49678BD3453";
	setAttr -k off ".v";
	setAttr ".pu" 0.43722784519195557;
	setAttr ".pv" 0.46620392799377441;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "nose_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "A7B46E9D-4A89-C30B-55C6-C8859F52453C";
createNode transform -n "follicle148" -p "nose_mask_fol_grp";
	rename -uid "287BB3B9-4FE5-6397-09EA-8CB0DC9A5148";
createNode follicle -n "follicleShape148" -p "follicle148";
	rename -uid "2800DDC3-4BE2-1683-B133-3AB54A4B4D8E";
	setAttr -k off ".v";
	setAttr ".pu" 0.50002044439315796;
	setAttr ".pv" 0.41517961025238037;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle149" -p "nose_mask_fol_grp";
	rename -uid "BC9E6823-4E7B-FDFB-31E1-3191D1FEC9C2";
createNode follicle -n "follicleShape149" -p "follicle149";
	rename -uid "AFA09C62-426E-3EC4-B21C-5BAA778DCC45";
	setAttr -k off ".v";
	setAttr ".pu" 0.60113853216171265;
	setAttr ".pv" 0.40536698698997498;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle151" -p "nose_mask_fol_grp";
	rename -uid "76C7D9BB-493F-140E-0DD1-D9A23F8F12C5";
createNode follicle -n "follicleShape151" -p "follicle151";
	rename -uid "D9E55A84-41B0-CE8C-3568-71A849BB00DE";
	setAttr -k off ".v";
	setAttr ".pu" 0.39890220761299133;
	setAttr ".pv" 0.40536689758300781;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle152" -p "nose_mask_fol_grp";
	rename -uid "D083691F-4C8E-89EA-5B08-A792FB3F2BBE";
createNode follicle -n "follicleShape152" -p "follicle152";
	rename -uid "946536BE-4524-3BFF-6C2B-CDB83B5FF892";
	setAttr -k off ".v";
	setAttr ".pu" 0.50005334615707397;
	setAttr ".pv" 0.36266139149665833;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle157" -p "nose_mask_fol_grp";
	rename -uid "F59DE86F-4C7B-0B63-A276-91B7AEA94130";
createNode follicle -n "follicleShape157" -p "follicle157";
	rename -uid "2654F704-4BD7-E2B7-5A85-71AE91E55051";
	setAttr -k off ".v";
	setAttr ".pu" 0.50002044439315796;
	setAttr ".pv" 0.63070672750473022;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "lipFrame_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "FACF28A1-4C28-DA32-4107-45BEAA97EA45";
createNode transform -n "follicle153" -p "lipFrame_mask_fol_grp";
	rename -uid "72D8E4BC-4F6F-9FDA-7411-219345B612B2";
createNode follicle -n "follicleShape153" -p "follicle153";
	rename -uid "F7186BCA-4943-D113-3198-49AD16CF9E59";
	setAttr -k off ".v";
	setAttr ".pu" 0.50002044439315796;
	setAttr ".pv" 0.31166350841522217;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle154" -p "lipFrame_mask_fol_grp";
	rename -uid "27EF385D-4811-297B-1C0C-478004CB4666";
createNode follicle -n "follicleShape154" -p "follicle154";
	rename -uid "F42A2E5F-4E51-FAFF-4D30-9A88807B1D28";
	setAttr -k off ".v";
	setAttr ".pu" 0.64378100633621216;
	setAttr ".pv" 0.23876787722110748;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle155" -p "lipFrame_mask_fol_grp";
	rename -uid "78C152B4-493D-E75F-D7A5-EFB95C65E4B7";
createNode follicle -n "follicleShape155" -p "follicle155";
	rename -uid "F42262C3-45D2-EE76-C386-FA87A10E7144";
	setAttr -k off ".v";
	setAttr ".pu" 0.50023972988128662;
	setAttr ".pv" 0.18260224163532257;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle156" -p "lipFrame_mask_fol_grp";
	rename -uid "DFCA5182-4A7F-AE2B-81B5-0F8D810437D9";
createNode follicle -n "follicleShape156" -p "follicle156";
	rename -uid "E0040833-4FA9-45CD-F8A5-8680451290F2";
	setAttr -k off ".v";
	setAttr ".pu" 0.35625976324081421;
	setAttr ".pv" 0.23876772820949554;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "chin_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "A88D9245-40AC-537B-8F81-E4B036C80DD1";
createNode transform -n "follicle162" -p "chin_mask_fol_grp";
	rename -uid "A25B8BF5-4885-3B96-7ADA-1B8C055D4062";
createNode follicle -n "follicleShape162" -p "follicle162";
	rename -uid "520A44E0-4829-06DA-7C4F-F5A260DA5389";
	setAttr -k off ".v";
	setAttr ".pu" 0.94745153188705444;
	setAttr ".pv" 0.262594074010849;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle163" -p "chin_mask_fol_grp";
	rename -uid "48E153FE-4D22-B492-A6AD-1CAB831079C6";
createNode follicle -n "follicleShape163" -p "follicle163";
	rename -uid "31E820AA-4B35-60BB-C68A-A7AC68378902";
	setAttr -k off ".v";
	setAttr ".pu" 0.7202942967414856;
	setAttr ".pv" 0.063984252512454987;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle164" -p "chin_mask_fol_grp";
	rename -uid "24321081-4271-8598-28C2-D6B9AF80E368";
createNode follicle -n "follicleShape164" -p "follicle164";
	rename -uid "F8334019-47ED-E6AC-018A-3E846E507D08";
	setAttr -k off ".v";
	setAttr ".pu" 0.50002044439315796;
	setAttr ".pv" 0.020011695101857185;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle165" -p "chin_mask_fol_grp";
	rename -uid "72230D89-4E36-AD6A-6ED7-91A10358C09E";
createNode follicle -n "follicleShape165" -p "follicle165";
	rename -uid "80666B4B-4EE8-683E-6C69-E484DDBB13B2";
	setAttr -k off ".v";
	setAttr ".pu" 0.27974709868431091;
	setAttr ".pv" 0.06398426741361618;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle166" -p "chin_mask_fol_grp";
	rename -uid "45B7DFDF-4613-178B-83E6-BDB890370120";
createNode follicle -n "follicleShape166" -p "follicle166";
	rename -uid "83F8D854-48BE-E242-B37A-40831E8412BF";
	setAttr -k off ".v";
	setAttr ".pu" 0.052589412778615952;
	setAttr ".pv" 0.26259380578994751;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "browLid_mask_fol_grp" -p "mask_fol_grp";
	rename -uid "E7DD78AB-443B-A8D1-3B3C-EFAF6C362C92";
createNode transform -n "follicle161" -p "browLid_mask_fol_grp";
	rename -uid "33B834AF-46B2-B1B0-2A05-C19E9CB4C989";
createNode follicle -n "follicleShape161" -p "follicle161";
	rename -uid "9EE7A532-41AC-1F04-BC61-A28A81DA18D4";
	setAttr -k off ".v";
	setAttr ".pu" 0.25240260362625122;
	setAttr ".pv" 0.69689249992370605;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle160" -p "browLid_mask_fol_grp";
	rename -uid "3AEEB007-4F02-E06A-9F3D-768C07C84D0D";
createNode follicle -n "follicleShape160" -p "follicle160";
	rename -uid "46E11E32-4D68-2A1D-74BB-FA91F4BA8D2B";
	setAttr -k off ".v";
	setAttr ".pu" 0.42487290501594543;
	setAttr ".pv" 0.67052191495895386;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle159" -p "browLid_mask_fol_grp";
	rename -uid "47F9A386-46E6-0CB0-8DD5-9A978FBDAC81";
createNode follicle -n "follicleShape159" -p "follicle159";
	rename -uid "E69997DF-4AA0-1538-9A4C-D4A51BEB3AF2";
	setAttr -k off ".v";
	setAttr ".pu" 0.57516813278198242;
	setAttr ".pv" 0.67051935195922852;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "follicle158" -p "browLid_mask_fol_grp";
	rename -uid "4F89C5FE-4E49-DEE8-4A0E-5FB75676CC9F";
createNode follicle -n "follicleShape158" -p "follicle158";
	rename -uid "AC054458-4427-5AD2-3199-709D0C5C8A54";
	setAttr -k off ".v";
	setAttr ".pu" 0.7476382851600647;
	setAttr ".pv" 0.69689249992370605;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "fol_base_mesh";
	rename -uid "1FFCCC4A-469C-14DC-4519-248C1E4579FB";
	addAttr -ci true -sn "dr" -ln "dropoff" -dv 4 -min 0 -max 20 -at "double";
	addAttr -ci true -sn "smt" -ln "smoothness" -min 0 -at "double";
	addAttr -ci true -sn "ift" -ln "inflType" -dv 2 -min 1 -max 2 -at "short";
	setAttr ".rp" -type "double3" 0 9.8139126300811768 2.5704403519630432 ;
	setAttr ".sp" -type "double3" 0 9.8139126300811768 2.5704403519630432 ;
	setAttr -k on ".dr";
	setAttr -k on ".smt";
createNode mesh -n "fol_base_meshShape" -p "fol_base_mesh";
	rename -uid "E7B2CED9-4E0F-0BE3-698E-328C29D9A1E7";
	setAttr -k off ".v";
	setAttr ".mb" no;
	setAttr ".csh" no;
	setAttr ".rcsh" no;
	setAttr ".vis" no;
	setAttr ".pv" -type "double2" 0.69899100065231323 0.7704317569732666 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 271 ".uvst[0].uvsp";
	setAttr ".uvst[0].uvsp[0:249]" -type "float2" 0.50002044 0.94462979 0.5000205
		 0.82949853 0.63640845 0.86447668 0.64076644 0.95804518 0.64192176 0.98642504 0.50002044
		 1 0.54519546 0.71924365 0.63279104 0.76345325 0.50002044 0.74151951 0.57482713 0.66897833
		 0.6445381 0.69678116 0.75255167 0.69288784 0.76519096 0.77741027 0.7706902 0.86948228
		 0.76725739 0.94355804 0.76416481 0.97468483 0.55868769 0.59435612 0.50002044 0.63616425
		 0.54088533 0.4588947 0.50002044 0.40416911 0.64114094 0.51942384 0.56499666 0.50733882
		 0.62377751 0.45269904 0.68499875 0.40269059 0.68736386 0.50309467 0.76747859 0.43320423
		 0.73771751 0.52321976 0.84727985 0.49980217 0.79430658 0.57310176 0.63453186 0.59899521
		 0.67213321 0.59350401 0.70412666 0.60509491 0.66558886 0.62440425 0.63364673 0.62407911
		 0.68977338 0.62949592 0.8850556 0.53233451 0.82104349 0.66370231 0.7644164 0.6500532
		 0.72875941 0.62791467 0.70470321 0.63861543 0.73080647 0.64693451 0.71120882 0.64640939
		 0.71481121 0.66776818 0.70325398 0.65622985 0.68381917 0.6729784 0.68847203 0.68539345
		 0.6513052 0.6750707 0.64720225 0.68669623 0.62411511 0.66341484 0.6185652 0.67504615
		 0.60604239 0.64259928 0.59634835 0.65140009 0.6045633 0.61007756 0.60973603 0.62809485
		 0.58672172 0.6179527 0.59971148 0.62934434 0.59676892 0.63245595 0.58375907 0.63512886
		 0.86564416 0.73570991 0.9289484 0.56730551 0.93561488 0.36222446 0.93266237 0.47022054
		 0.89224315 0.46045351 0.89517725 0.39015704 0.85215312 0.29195189 0.92521191 0.21436486
		 0.80178261 0.2489244 0.87062311 0.14663133 0.69579142 0.16024154 0.77083063 0.076836377
		 0.83015299 0.11034748 0.74850625 0.20046651 0.50002044 0.0024545789 0.55573285 2.9802322e-08
		 0.54236358 0.10546848 0.50002044 0.10373884 0.66963929 0.13959938 0.73513365 0.061883152
		 0.53350502 0.18190068 0.50002044 0.18691042 0.64704597 0.34841168 0.60478628 0.4021264
		 0.63590157 0.2040363 0.65969038 0.23097548 0.56798166 0.29592162 0.6034776 0.28490311
		 0.73301089 0.35108036 0.68222737 0.30548966 0.70738554 0.26368469 0.76446378 0.30447721
		 0.63950038 0.26827899 0.53520674 0.37727499 0.52932078 0.30335587 0.50002044 0.37086311
		 0.50002044 0.30564484 0.81920224 0.35002643 0.79537433 0.39348161 0.85959291 0.39385614
		 0.85213101 0.43922648 0.53082889 0.20965362 0.50002044 0.2109111 0.64091885 0.24016967
		 0.62038773 0.22443697 0.61470473 0.256625 0.5609659 0.27104795 0.58426553 0.2635814
		 0.52784836 0.27908993 0.50002044 0.28078321 0.64400506 0.029722184 0.59655094 0.1115301
		 0.57388729 0.18436903 0.5656268 0.21183115 0.60574901 0.1910364 0.59141964 0.21831265
		 0.63625216 0.12308365 0.68884546 0.045199662 0.52768099 0.22975814 0.50002044 0.22937843
		 0.52879804 0.238915 0.50002044 0.23931813 0.56291902 0.229653 0.56529969 0.23654214
		 0.58603197 0.23119703 0.58959198 0.23692358 0.61886328 0.23822698 0.61571079 0.23294246
		 0.63819224 0.23850828 0.64333653 0.24040315 0.63903761 0.24181083 0.6403091 0.24177319
		 0.61973834 0.2428681 0.61489034 0.24700812 0.59133506 0.24353099 0.58676279 0.24979603
		 0.56476766 0.24640787 0.56072336 0.25424868 0.52694499 0.25846311 0.50002044 0.25902846
		 0.50002044 0.24902037 0.52949703 0.24893618 0.35927448 0.95804518 0.3636325 0.86447668
		 0.35811919 0.98642504 0.45484543 0.71924365 0.36724991 0.76345354 0.42521378 0.66897833
		 0.35550281 0.69678116 0.23485002 0.77741027 0.24748921 0.69288784 0.22935066 0.86948228
		 0.23278353 0.94355804 0.23587608 0.97468483 0.4413532 0.59435612 0.45915559 0.4588947
		 0.35889995 0.51942384 0.37626341 0.45269904 0.43504426 0.50733882 0.31504217 0.40269059
		 0.31267703 0.50309467 0.26232344 0.52321976 0.2325623 0.43320423 0.20573434 0.57310176
		 0.15276107 0.49980217 0.36550903 0.59899521 0.32790768 0.59350401 0.29591429 0.60509491
		 0.33445203 0.62440425 0.36639416 0.62407911 0.31026751 0.62949592 0.11498532 0.53233451
		 0.17899749 0.66370231 0.23562452 0.6500532 0.27128148 0.62791467 0.29533771 0.63861543
		 0.26923445 0.64693451 0.2888321 0.64640939 0.2967869 0.65622985 0.28522974 0.66776818
		 0.31622177 0.6729784 0.31156892 0.68539345 0.34873569 0.6750707 0.3528387 0.68669623
		 0.37592578 0.66341484 0.38147572 0.67504615 0.3939985 0.64259928 0.40369257 0.65140009
		 0.39547765 0.61007756 0.39030486 0.62809485 0.4133192 0.6179527 0.40032944 0.62934434
		 0.40327203 0.63245595 0.41628185 0.63512886 0.13439673 0.73570991 0.071092486 0.56730551
		 0.064426035 0.36222446 0.10486364 0.39015704 0.10779774 0.46045351 0.067378581 0.47022054
		 0.14788777 0.29195189 0.074829012 0.21436486 0.19825831 0.2489244 0.12941778 0.14663133
		 0.30424953 0.16024154 0.25153467 0.20046651 0.16988796 0.11034748 0.22921032 0.076836377
		 0.45767733 0.10546848 0.44430807 2.9802322e-08 0.26490724 0.061883152 0.3304016 0.13959938
		 0.4665359 0.18190068 0.35299498 0.34841168 0.39525464 0.4021264 0.36413938 0.2040363
		 0.34035051 0.23097548 0.43205926 0.29592162 0.39656329 0.28490311 0.26703 0.35108036
		 0.23557711 0.30447721 0.29265538 0.26368469 0.31781352 0.30548966 0.36054051 0.26827899
		 0.47072014 0.30335587 0.46483418 0.37727499 0.18083867 0.35002643 0.20466655 0.39348161
		 0.14790991 0.43922648 0.140448 0.39385614 0.469212 0.20965362 0.3591221 0.24016967
		 0.37965322 0.22443697 0.38533616 0.256625 0.43907502 0.27104795 0.41577539 0.2635814
		 0.47219253 0.27908993 0.40349001 0.1115301 0.35603586 0.029722184 0.4261536 0.18436903
		 0.43441415 0.21183115 0.39429188 0.1910364 0.40862128 0.21831265 0.36378872 0.12308365
		 0.31119546 0.045199662 0.47235993 0.22975814 0.47124285 0.238915 0.43474123 0.23654214
		 0.43712193 0.229653 0.41044894 0.23692358 0.41400892 0.23119703 0.3811776 0.23822698;
	setAttr ".uvst[0].uvsp[250:270]" 0.38433012 0.23294246 0.35670441 0.24040315
		 0.36184865 0.23850828 0.35973179 0.24177319 0.36100334 0.24181083 0.38030255 0.2428681
		 0.38515055 0.24700812 0.40870589 0.24353099 0.41327816 0.24979603 0.43527323 0.24640787
		 0.43931752 0.25424868 0.47309592 0.25846311 0.47054389 0.24893618 0.97784179 0.36222446
		 0.97442788 0.47022054 0.97644627 0.21436486 0.97015667 0.56730551 0.02561307 0.47022054
		 0.022199124 0.36222446 0.023594648 0.21436486 0.029884219 0.56730551;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 38 ".pt";
	setAttr ".pt[0]" -type "float3" -4.4645276e-08 7.4505806e-08 4.6985224e-07 ;
	setAttr ".pt[1]" -type "float3" 2.2351742e-08 0 -5.5879354e-09 ;
	setAttr ".pt[2]" -type "float3" 0 -2.9802322e-08 -7.4505806e-09 ;
	setAttr ".pt[3]" -type "float3" -5.9604645e-08 1.1920929e-07 -6.7055225e-08 ;
	setAttr ".pt[6]" -type "float3" 1.5646219e-07 5.364418e-07 1.7462298e-07 ;
	setAttr ".pt[7]" -type "float3" 2.9802322e-08 3.5762787e-07 1.937151e-07 ;
	setAttr ".pt[8]" -type "float3" 0 1.1920929e-07 1.1920929e-07 ;
	setAttr ".pt[10]" -type "float3" -2.9802322e-08 1.1920929e-07 7.4505806e-08 ;
	setAttr ".pt[11]" -type "float3" -2.9802322e-08 1.1920929e-07 7.4505806e-08 ;
	setAttr ".pt[13]" -type "float3" 1.5646219e-07 1.7881393e-07 -6.3795596e-08 ;
	setAttr ".pt[17]" -type "float3" 0.092291713 0.031853653 -1.8626451e-09 ;
	setAttr ".pt[18]" -type "float3" 0 -0.074785106 0 ;
	setAttr ".pt[57]" -type "float3" 1.6391277e-07 5.9604645e-08 -7.4505806e-09 ;
	setAttr ".pt[58]" -type "float3" 1.6391277e-07 5.9604645e-08 -7.4505806e-09 ;
	setAttr ".pt[73]" -type "float3" -0.20246211 0 0 ;
	setAttr ".pt[74]" -type "float3" -1.8626451e-08 -1.937151e-07 -1.3038516e-08 ;
	setAttr ".pt[76]" -type "float3" 0 2.9802322e-08 0 ;
	setAttr ".pt[77]" -type "float3" 0 2.9802322e-08 0 ;
	setAttr ".pt[78]" -type "float3" 7.9162419e-09 -1.1175871e-08 -1.0477379e-09 ;
	setAttr ".pt[83]" -type "float3" 0 0 -0.1185432 ;
	setAttr ".pt[84]" -type "float3" -9.3132257e-10 0 -2.3283064e-10 ;
	setAttr ".pt[85]" -type "float3" 0 0 -0.26749259 ;
	setAttr ".pt[92]" -type "float3" 0 1.4901161e-08 1.8626451e-09 ;
	setAttr ".pt[93]" -type "float3" 0 1.4901161e-08 -3.7252903e-09 ;
	setAttr ".pt[94]" -type "float3" 4.6566129e-10 0 0 ;
	setAttr ".pt[113]" -type "float3" -1.8626451e-08 -1.937151e-07 -1.3038516e-08 ;
	setAttr ".pt[114]" -type "float3" 1.8626451e-09 -3.7252903e-09 -4.6566129e-10 ;
	setAttr ".pt[115]" -type "float3" 3.7252903e-09 -1.4901161e-08 0 ;
	setAttr ".pt[140]" -type "float3" 2.2351742e-08 0 1.8626451e-09 ;
	setAttr ".pt[141]" -type "float3" 1.4959369e-08 -4.4703484e-08 4.6985224e-07 ;
	setAttr ".pt[143]" -type "float3" -7.4505806e-09 1.6391277e-07 2.6077032e-08 ;
	setAttr ".pt[148]" -type "float3" -2.7567148e-07 1.0430813e-07 1.7508864e-07 ;
	setAttr ".pt[152]" -type "float3" -0.092291713 0.031853653 0 ;
	setAttr ".pt[156]" -type "float3" -2.682209e-07 2.9802322e-08 -1.1920929e-07 ;
	setAttr ".pt[162]" -type "float3" -3.2410026e-07 -7.4505806e-09 -1.4342368e-07 ;
	setAttr ".pt[164]" -type "float3" -5.5879354e-08 -3.7252903e-08 -2.4214387e-08 ;
	setAttr ".pt[204]" -type "float3" 0.20246211 0 0 ;
	setAttr ".pt[214]" -type "float3" 0 0 -0.1185432 ;
	setAttr -s 271 ".vt";
	setAttr ".vt[0:165]"  -2.1423128e-16 12.76533031 4.35476112 3.5762787e-07 12.0010976791 4.51297092
		 1.31070542 12.23328018 4.23625278 1.26641905 12.85438061 4.11126614 -6.3789331e-16 13.13287354 4.25009489
		 1.24695802 13.04276371 4.070241928 1.3533783 11.56269455 4.35451508 0.44015974 11.26923466 4.53129768
		 -1.1920929e-07 11.41709995 4.53112888 1.6963999e-15 10.71776009 4.38855696 1.29086304 11.12013054 4.083269119
		 0.60183197 10.93557739 4.14234495 2.12174892 11.094286919 3.31248903 2.27569294 11.65534019 3.21168423
		 2.25381398 12.26650715 3.14060211 2.19592404 12.7582159 3.16533303 2.16740894 12.96483326 3.19292307
		 0.46201599 10.44024086 4.13718081 2.0668193e-15 9.17779446 4.97551918 0.56799281 9.86262703 4.29829168
		 1.024953365 9.49993229 4.052915096 1.15903795 9.9428463 3.97536683 1.60425365 9.83445454 3.80289125
		 1.49114394 9.16798019 3.74365544 2.035317898 9.37052727 3.11946201 2.029020071 9.96804333 3.44977689
		 2.46558309 9.81259918 2.25665021 2.32482409 10.29915619 2.87992311 1.44498003 10.43458462 3.8623271
		 1.073591948 10.471035 3.96095705 1.73750365 10.5115242 3.69183111 1.068071008 10.63753986 3.96624899
		 1.39674103 10.63969803 3.90198803 1.60878396 10.67349625 3.77651 2.37449098 10.90055561 2.57436895
		 2.57180858 10.028546333 1.74312103 2.10244894 10.80995369 3.17146897 1.91471708 10.66300011 3.5018177
		 1.72943544 10.73403072 3.67973208 1.76637447 10.7857666 3.62570667 1.93069339 10.78925228 3.48581505
		 1.85483599 10.92754459 3.63469505 1.73083794 10.85095406 3.69801593 1.64221203 11.044539452 3.81796598
		 1.58215404 10.96212959 3.83009791 1.26706803 11.05318737 4.016807079 1.28497303 10.97601795 3.9792161
		 0.96500701 10.97585487 4.045156002 0.98754698 10.89864731 3.99378395 0.72244102 10.81889439 3.98969197
		 0.78031498 10.76047516 3.93890309 0.81011599 10.66419601 3.93337989 0.78930402 10.54459858 3.97822404
		 0.71796203 10.67249012 3.92532992 0.63505799 10.59687328 3.9781549 0.61190999 10.71088696 3.98098707
		 0.70629603 10.6931448 3.950948 2.49595094 11.37853622 2.021852016 2.70266366 10.26068115 1.0021905899
		 2.38049912 9.084783554 1.67249084 2.49879646 8.89936924 1.0095103979 2.14325261 7.91788864 1.37857628
		 2.10914969 8.4329052 2.25079346 1.78333199 7.46827888 2.1327281 1.7941606 8.14729214 2.74284935
		 1.27763307 7.0049853325 2.89271879 1.20415676 7.55862236 3.41902018 0.80788541 6.69224501 3.52225399
		 0.63709408 7.23527956 3.81896639 -4.0057342e-16 7.1835618 4.063396931 -4.2222827e-16 6.51124477 3.85797668
		 3.2100415e-18 7.73564816 4.20192337 0.54208952 7.71877861 4.0060210228 0.8448813 9.16423512 4.073507309
		 1.14767122 8.80768108 3.88253546 1.11548817 8.028148651 3.69700599 0.81288856 8.38611603 4.038497448
		 0.56403381 8.45925617 4.20544386 1.44967103 8.24526978 3.47368193 1.75494885 8.51604748 3.07168889
		 1.55292892 7.22742939 2.50382185 1.53138113 7.82563257 3.14024353 0.41168812 9.54105854 4.60402298
		 0.33076823 8.9992733 4.47463989 0.25500941 8.50860405 4.33881474 -4.3504769e-16 8.95671177 4.62253857
		 5.4051343e-17 8.52379799 4.33412123 2.044265747 8.81839943 2.59222126 2.24812269 9.10933781 2.14560008
		 4.1689141e-16 7.89496279 4.31024933 0.51247221 7.90107012 4.11336136 0.98854029 8.089179039 3.77135205
		 0.67930818 8.24458408 4.12579298 0.51331693 8.29414654 4.24229527 0.24881794 8.34752846 4.38840246
		 1.5655005e-16 8.35876846 4.40241861 0.33362752 6.49495173 3.76514077 0.30488396 7.19504309 4.022423267
		 0.26071265 7.70239401 4.14910221 0.25970635 7.88661575 4.2819767 0.67983902 7.9440937 3.9895575
		 0.74747378 7.76303625 3.88568783 0.86152828 7.31197119 3.66710353 0.97366828 6.79498339 3.30729985
		 0.84492087 7.98474646 3.83687329 0.93100762 7.84932852 3.75973582 1.050318122 7.4216013 3.53277183
		 1.14217865 6.90572691 3.082667112 2.58897042 9.61623859 1.0046640635 2.48673105 9.55140591 1.67294097
		 2.32131314 9.41050243 2.21889687 2.035321474 9.10685158 2.83058047 1.6796453 8.82539558 3.34473395
		 1.3502605 8.52276802 3.66274428 1.027675629 8.27576637 3.83668542 0.85099292 8.19840813 3.92607713
		 2.5084836e-16 8.017547607 4.32229424 0.235754 8.020068169 4.3035059 0.23477399 8.080850601 4.22846699
		 -1.4774531e-16 8.083526611 4.24886799 0.49106199 8.019370079 4.11703396 0.487856 8.065099716 4.047136784
		 0.64274102 8.029619217 4.0080962181 0.63950598 8.067631721 3.93655396 0.81281698 8.041205406 3.85123205
		 0.80151802 8.076283455 3.7914269 0.951424 8.078150749 3.75817394 0.93071902 8.09072876 3.67426205
		 0.957968 8.10007286 3.75626802 0.92282099 8.099822998 3.69834805 0.81965101 8.13457203 3.87352204
		 0.80432898 8.10709095 3.78435898 0.65936702 8.15307808 4.031258106 0.649459 8.1114912 3.92758107
		 0.48589176 8.18263435 4.15968418 0.48502034 8.13058758 4.051472187 -8.119675e-17 8.21436214 4.36041594
		 -4.4647067e-17 8.14792919 4.27616119 0.243968 8.14737034 4.25199223 0.236698 8.21060944 4.35858488
		 -1.31070495 12.23328018 4.23625278 -1.26641905 12.85438061 4.11126614 -1.24695802 13.04276371 4.070241928
		 -1.35337901 11.56269646 4.35451698 -0.44016001 11.26923466 4.53129816 -1.29086304 11.12013054 4.083269119
		 -0.60183197 10.93557739 4.14234495 -2.12174892 11.094286919 3.31248903 -2.27569199 11.65534019 3.21168494
		 -2.25381398 12.26650715 3.14060211 -2.19592404 12.7582159 3.16533303 -2.16740894 12.96483326 3.19292307
		 -0.46201599 10.44024086 4.13718081 -0.56799281 9.86262703 4.29829168 -1.024953365 9.49993229 4.052915096
		 -1.15903795 9.9428463 3.97536683 -1.60425365 9.83445454 3.80289125 -1.49114394 9.16798019 3.74365544
		 -2.035317898 9.37052727 3.11946201 -2.029020071 9.96804333 3.44977689 -2.46558309 9.81259918 2.25665021
		 -2.32482409 10.29915619 2.87992311 -1.44498003 10.43458462 3.8623271 -1.073591948 10.471035 3.96095705
		 -1.73750365 10.5115242 3.69183111 -1.068071008 10.63753986 3.96624899;
	setAttr ".vt[166:270]" -1.39674103 10.63969803 3.90198803 -1.60878396 10.67349625 3.77651
		 -2.37449098 10.90055561 2.57436895 -2.57180858 10.028546333 1.74312103 -2.10244894 10.80995369 3.17146897
		 -1.91471708 10.66300011 3.5018177 -1.72943544 10.73403072 3.67973208 -1.76637447 10.7857666 3.62570667
		 -1.93069339 10.78925228 3.48581505 -1.85483599 10.92754459 3.63469505 -1.73083794 10.85095406 3.69801593
		 -1.64221203 11.044539452 3.81796598 -1.58215404 10.96212959 3.83009791 -1.26706803 11.05318737 4.016807079
		 -1.28497303 10.97601795 3.9792161 -0.96500701 10.97585487 4.045156002 -0.98754698 10.89864731 3.99378395
		 -0.72244102 10.81889439 3.98969197 -0.78031498 10.76047516 3.93890309 -0.81011599 10.66419601 3.93337989
		 -0.78930402 10.54459858 3.97822404 -0.71796203 10.67249012 3.92532992 -0.63505799 10.59687328 3.9781549
		 -0.61190999 10.71088696 3.98098707 -0.70629603 10.6931448 3.950948 -2.49595094 11.37853622 2.021852016
		 -2.70266366 10.26068115 1.0021905899 -2.38049912 9.084783554 1.67249084 -2.49879646 8.89936924 1.0095103979
		 -2.14325261 7.91788864 1.37857628 -2.10914969 8.4329052 2.25079346 -1.78333199 7.46827888 2.1327281
		 -1.7941606 8.14729214 2.74284935 -1.27763307 7.0049853325 2.89271879 -1.20415676 7.55862236 3.41902018
		 -0.80788541 6.69224501 3.52225399 -0.63709408 7.23527956 3.81896639 -0.54208952 7.71877861 4.0060210228
		 -0.8448813 9.16423512 4.073507309 -1.14767122 8.80768108 3.88253546 -1.11548817 8.028148651 3.69700599
		 -0.81288856 8.38611603 4.038497448 -0.56403381 8.45925617 4.20544386 -1.44967103 8.24526978 3.47368193
		 -1.75494885 8.51604748 3.07168889 -1.55292892 7.22742939 2.50382185 -1.53138113 7.82563257 3.14024353
		 -0.41168812 9.54105854 4.60402298 -0.33076823 8.9992733 4.47463989 -0.25500941 8.50860405 4.33881474
		 -2.044265747 8.81839943 2.59222126 -2.24812269 9.10933781 2.14560008 -0.51247221 7.90107012 4.11336136
		 -0.98854029 8.089179039 3.77135205 -0.67930818 8.24458408 4.12579298 -0.51331693 8.29414654 4.24229527
		 -0.24881794 8.34752846 4.38840246 -0.33362752 6.49495173 3.76514077 -0.30488396 7.19504309 4.022423267
		 -0.26071265 7.70239401 4.14910221 -0.25970635 7.88661575 4.2819767 -0.67983902 7.9440937 3.9895575
		 -0.74747378 7.76303625 3.88568783 -0.86152828 7.31197119 3.66710353 -0.97366828 6.79498339 3.30729985
		 -0.84492087 7.98474646 3.83687329 -0.93100762 7.84932852 3.75973582 -1.050318122 7.4216013 3.53277183
		 -1.14217865 6.90572691 3.082667112 -2.58897042 9.61623859 1.0046640635 -2.48673105 9.55140591 1.67294097
		 -2.32131314 9.41050243 2.21889687 -2.035321474 9.10685158 2.83058047 -1.6796453 8.82539558 3.34473395
		 -1.3502605 8.52276802 3.66274428 -1.027675629 8.27576637 3.83668542 -0.85099292 8.19840813 3.92607713
		 -0.235754 8.020068169 4.3035059 -0.23477399 8.080850601 4.22846699 -0.49106199 8.019370079 4.11703396
		 -0.487856 8.065099716 4.047136784 -0.64274102 8.029619217 4.0080962181 -0.63950598 8.067631721 3.93655396
		 -0.81281698 8.041205406 3.85123205 -0.80151802 8.076283455 3.7914269 -0.951424 8.078150749 3.75817394
		 -0.93071902 8.09072876 3.67426205 -0.957968 8.10007286 3.75626802 -0.92282099 8.099822998 3.69834805
		 -0.81965101 8.13457203 3.87352204 -0.80432898 8.10709095 3.78435898 -0.65936702 8.15307808 4.031258106
		 -0.649459 8.1114912 3.92758107 -0.48589176 8.18263435 4.15968418 -0.48502034 8.13058758 4.051472187
		 -0.243968 8.14737034 4.25199223 -0.236698 8.21060944 4.35858488 2.49879646 8.89936924 0.17268133
		 2.58897042 9.61623859 0.167835 2.14325261 7.91788864 0.54174721 2.70266366 10.26068115 0.16536152
		 -2.49879646 8.89936924 0.17268133 -2.58897042 9.61623859 0.167835 -2.14325261 7.91788864 0.54174721
		 -2.70266366 10.26068115 0.16536152;
	setAttr -s 473 ".ed";
	setAttr ".ed[0:165]"  0 1 0 1 2 0 2 3 0 3 0 0 5 4 0 4 0 0 3 5 0 7 6 0 6 2 0
		 1 7 0 1 8 0 8 9 0 9 7 0 11 10 0 10 6 0 7 11 0 10 12 0 12 13 0 13 6 0 14 2 0 13 14 0
		 15 3 0 14 15 0 16 5 0 15 16 0 17 11 0 9 17 0 19 17 0 9 18 0 18 82 0 21 17 0 19 20 0
		 20 21 0 23 22 0 22 21 0 20 23 0 23 24 0 24 25 0 25 22 0 24 26 0 26 27 0 27 25 0 29 21 0
		 22 28 0 28 29 0 25 30 0 30 28 0 32 31 0 31 29 0 28 32 0 33 32 0 30 33 0 35 34 0 34 27 0
		 26 35 0 36 34 0 34 13 0 12 36 0 37 27 0 36 37 0 37 30 0 37 38 0 38 33 0 40 39 0 39 38 0
		 37 40 0 40 41 0 41 42 0 42 39 0 44 42 0 41 43 0 43 44 0 46 44 0 43 45 0 45 46 0 48 46 0
		 45 47 0 47 48 0 50 48 0 47 49 0 49 50 0 52 29 0 31 51 0 51 52 0 54 52 0 51 53 0 53 54 0
		 56 50 0 49 55 0 55 56 0 55 54 0 53 56 0 34 57 0 57 14 0 35 58 0 58 57 0 60 108 0
		 35 109 0 59 60 0 62 61 0 61 60 0 59 62 0 64 63 0 63 61 0 62 64 0 66 65 0 65 80 0
		 64 81 0 70 96 0 67 68 0 68 97 0 69 70 0 66 106 0 67 103 0 72 98 0 71 69 0 68 72 0
		 74 23 0 20 73 0 73 74 0 66 75 0 75 105 0 77 76 0 76 74 0 73 77 0 74 113 0 78 79 0
		 79 112 0 76 114 0 75 78 0 80 63 0 81 66 0 80 81 1 81 78 0 64 79 0 82 19 0 82 9 1
		 82 73 0 73 83 0 83 84 0 84 77 0 83 85 0 85 86 0 86 84 0 87 111 0 79 87 0 87 88 0
		 88 110 0 88 59 0 62 87 0 90 99 0 89 71 0 72 90 0 91 104 0 75 91 0 92 115 0 76 92 0
		 93 92 0 77 93 0 94 93 0 84 94 0 95 94 0 86 95 0 96 67 0 97 69 0 98 71 0;
	setAttr ".ed[166:331]" 99 89 0 96 97 1 97 98 1 98 99 1 100 90 0 101 72 0 102 68 0
		 103 107 0 100 101 1 101 102 1 102 103 1 104 100 0 105 101 0 106 102 0 107 65 0 104 105 1
		 105 106 1 106 107 1 108 58 0 109 59 0 110 26 0 111 24 0 112 23 0 113 78 0 114 75 0
		 115 91 0 108 109 1 109 110 1 110 111 1 111 112 1 112 113 1 113 114 1 114 115 1 117 116 0
		 116 89 0 99 117 0 117 118 0 118 119 0 119 116 0 117 120 0 120 121 0 121 118 0 120 122 0
		 122 123 0 123 121 0 125 123 0 122 124 0 124 125 0 124 126 0 126 127 0 127 125 0 126 128 0
		 128 129 0 129 127 0 131 129 0 128 130 0 130 131 0 133 131 0 130 132 0 132 133 0 135 133 0
		 132 134 0 134 135 0 139 136 0 136 137 0 137 138 0 138 139 0 138 135 0 139 134 0 1 140 0
		 140 141 0 141 0 0 142 4 0 141 142 0 144 143 0 143 140 0 1 144 0 9 144 0 146 145 0
		 145 143 0 144 146 0 145 147 0 147 148 0 148 143 0 149 140 0 148 149 0 150 141 0 149 150 0
		 151 142 0 150 151 0 152 146 0 9 152 0 213 9 1 18 213 0 155 152 0 153 152 0 153 154 0
		 154 155 0 157 156 0 156 155 0 154 157 0 157 158 0 158 159 0 159 156 0 158 160 0 160 161 0
		 161 159 0 163 155 0 156 162 0 162 163 0 159 164 0 164 162 0 166 165 0 165 163 0 162 166 0
		 167 166 0 164 167 0 169 168 0 168 161 0 160 169 0 170 168 0 168 148 0 147 170 0 171 161 0
		 170 171 0 171 164 0 171 172 0 172 167 0 174 173 0 173 172 0 171 174 0 174 175 0 175 176 0
		 176 173 0 178 176 0 175 177 0 177 178 0 180 178 0 177 179 0 179 180 0 182 180 0 179 181 0
		 181 182 0 184 182 0 181 183 0 183 184 0 186 163 0 165 185 0 185 186 0 188 186 0 185 187 0
		 187 188 0 190 184 0 183 189 0 189 190 0 189 188 0 187 190 0 168 191 0 191 149 0 169 192 0
		 192 191 0 194 235 0 235 236 1 236 193 0 193 194 0 196 195 0;
	setAttr ".ed[332:472]" 195 194 0 193 196 0 198 197 0 197 195 0 196 198 0 200 199 0
		 199 211 0 211 212 1 212 200 0 70 223 0 223 224 1 224 69 0 200 233 0 233 234 1 234 199 0
		 224 225 1 225 71 0 205 157 0 154 204 0 204 205 0 232 233 1 200 206 0 206 232 0 208 207 0
		 207 205 0 204 208 0 239 240 1 240 209 0 209 210 0 210 239 0 240 241 1 241 206 0 206 209 0
		 211 197 0 198 212 0 212 209 0 198 210 0 213 153 0 213 204 0 204 214 0 214 215 0 215 208 0
		 214 85 0 86 215 0 216 238 0 238 239 1 210 216 0 216 217 0 217 237 0 237 238 1 236 237 1
		 217 193 0 196 216 0 225 226 1 226 89 0 219 231 0 231 232 1 206 219 0 241 242 1 242 219 0
		 221 220 0 207 220 0 208 221 0 222 221 0 215 222 0 95 222 0 223 201 0 201 202 0 202 224 0
		 203 225 0 202 203 0 218 226 0 203 218 0 227 228 1 227 218 0 228 203 0 229 202 0 228 229 1
		 229 230 1 201 230 0 231 227 0 232 228 0 233 229 0 230 234 0 235 192 0 169 236 0 237 160 0
		 238 158 0 239 157 0 205 240 0 207 241 0 220 242 0 243 116 0 226 243 0 243 244 0 244 119 0
		 243 245 0 245 246 0 246 244 0 245 247 0 247 248 0 248 246 0 250 248 0 247 249 0 249 250 0
		 249 251 0 251 252 0 252 250 0 251 253 0 253 254 0 254 252 0 256 254 0 253 255 0 255 256 0
		 258 256 0 255 257 0 257 258 0 260 258 0 257 259 0 259 260 0 262 136 0 137 261 0 261 262 0
		 261 260 0 262 259 0 8 7 1 8 144 1 60 263 0 108 264 0 263 264 0 61 265 0 265 263 0
		 58 266 0 264 266 0 194 267 0 235 268 0 267 268 0 195 269 0 269 267 0 192 270 0 268 270 0;
	setAttr -s 196 -ch 778 ".fc[0:195]" -type "polyFaces" 
		f 4 0 1 2 3
		mu 0 4 0 1 2 3
		f 4 4 5 -4 6
		mu 0 4 4 5 0 3
		f 4 7 8 -2 9
		mu 0 4 6 7 2 1
		f 3 -10 10 457
		mu 0 3 6 1 8
		f 4 13 14 -8 15
		mu 0 4 9 10 7 6
		f 4 16 17 18 -15
		mu 0 4 10 11 12 7
		f 4 19 -9 -19 20
		mu 0 4 13 2 7 12
		f 4 21 -3 -20 22
		mu 0 4 14 3 2 13
		f 4 23 -7 -22 24
		mu 0 4 15 4 3 14
		f 4 25 -16 -13 26
		mu 0 4 16 9 6 17
		f 3 136 28 29
		mu 0 3 18 17 19
		f 4 30 -28 31 32
		mu 0 4 20 16 21 22
		f 4 33 34 -33 35
		mu 0 4 23 24 20 22
		f 4 36 37 38 -34
		mu 0 4 23 25 26 24
		f 4 39 40 41 -38
		mu 0 4 25 27 28 26
		f 4 42 -35 43 44
		mu 0 4 29 20 24 30
		f 4 45 46 -44 -39
		mu 0 4 26 31 30 24
		f 4 47 48 -45 49
		mu 0 4 32 33 29 30
		f 4 50 -50 -47 51
		mu 0 4 34 32 30 31
		f 4 52 53 -41 54
		mu 0 4 35 36 28 27
		f 4 55 56 -18 57
		mu 0 4 37 36 12 11
		f 4 58 -54 -56 59
		mu 0 4 38 28 36 37
		f 4 -59 60 -46 -42
		mu 0 4 28 38 31 26
		f 4 61 62 -52 -61
		mu 0 4 38 39 34 31
		f 4 63 64 -62 65
		mu 0 4 40 41 39 38
		f 4 -64 66 67 68
		mu 0 4 41 40 42 43
		f 4 69 -68 70 71
		mu 0 4 44 43 42 45
		f 4 72 -72 73 74
		mu 0 4 46 44 45 47
		f 4 75 -75 76 77
		mu 0 4 48 46 47 49
		f 4 78 -78 79 80
		mu 0 4 50 48 49 51
		f 4 81 -49 82 83
		mu 0 4 52 29 33 53
		f 4 84 -84 85 86
		mu 0 4 54 52 53 55
		f 4 87 -81 88 89
		mu 0 4 56 50 51 57
		f 4 -90 90 -87 91
		mu 0 4 56 57 54 55
		f 4 -57 92 93 -21
		mu 0 4 12 36 58 13
		f 4 -53 94 95 -93
		mu 0 4 36 35 59 58
		f 4 96 192 185 98
		mu 0 4 60 61 62 63
		f 4 99 100 -99 101
		mu 0 4 64 65 60 63
		f 4 102 103 -100 104
		mu 0 4 66 67 65 64
		f 4 105 106 132 131
		mu 0 4 68 69 70 71
		f 4 108 167 164 111
		mu 0 4 72 73 74 75
		f 4 -106 112 183 180
		mu 0 4 69 68 76 77
		f 4 168 165 115 -165
		mu 0 4 74 78 79 75
		f 4 117 -36 118 119
		mu 0 4 80 23 22 81
		f 4 182 -113 120 121
		mu 0 4 82 76 68 83
		f 4 122 123 -120 124
		mu 0 4 84 85 80 81
		f 4 196 189 126 127
		mu 0 4 86 87 88 89
		f 4 -190 197 190 129
		mu 0 4 88 87 90 83
		f 4 -133 130 -103 107
		mu 0 4 71 70 67 66
		f 4 -132 133 -130 -121
		mu 0 4 68 71 88 83
		f 4 -134 -108 134 -127
		mu 0 4 88 71 66 89
		f 4 27 -27 -137 135
		mu 0 4 21 16 17 18
		f 4 -32 -136 137 -119
		mu 0 4 22 21 18 81
		f 4 -125 138 139 140
		mu 0 4 84 81 91 92
		f 4 141 142 143 -140
		mu 0 4 91 93 94 92
		f 4 144 195 -128 145
		mu 0 4 95 96 86 89
		f 4 146 147 194 -145
		mu 0 4 95 97 98 96
		f 4 193 -148 148 -186
		mu 0 4 62 98 97 63
		f 4 149 -146 -135 -105
		mu 0 4 64 95 89 66
		f 4 -147 -150 -102 -149
		mu 0 4 97 95 64 63
		f 4 169 166 151 -166
		mu 0 4 78 99 100 79
		f 4 153 181 -122 154
		mu 0 4 101 102 82 83
		f 4 198 191 -155 -191
		mu 0 4 90 103 101 83
		f 4 157 -157 -123 158
		mu 0 4 104 105 85 84
		f 4 159 -159 -141 160
		mu 0 4 106 104 84 92
		f 4 161 -161 -144 162
		mu 0 4 107 106 92 94
		f 4 -168 163 109 110
		mu 0 4 74 73 108 109
		f 4 114 -169 -111 116
		mu 0 4 110 78 74 109
		f 4 150 -170 -115 152
		mu 0 4 111 99 78 110
		f 4 -175 170 -153 -172
		mu 0 4 112 113 111 110
		f 4 -173 -176 171 -117
		mu 0 4 109 114 112 110
		f 4 -177 172 -110 113
		mu 0 4 115 114 109 108
		f 4 -182 177 174 -179
		mu 0 4 82 102 113 112
		f 4 175 -180 -183 178
		mu 0 4 112 114 76 82
		f 4 -184 179 176 173
		mu 0 4 77 76 114 115
		f 4 -193 184 -95 97
		mu 0 4 62 61 59 35
		f 4 -187 -194 -98 -55
		mu 0 4 27 98 62 35
		f 4 -195 186 -40 -188
		mu 0 4 96 98 27 25
		f 4 -196 187 -37 -189
		mu 0 4 86 96 25 23
		f 4 125 -197 188 -118
		mu 0 4 80 87 86 23
		f 4 -198 -126 -124 128
		mu 0 4 90 87 80 85
		f 4 155 -199 -129 156
		mu 0 4 105 103 90 85
		f 4 199 200 -167 201
		mu 0 4 116 117 100 99
		f 4 -200 202 203 204
		mu 0 4 117 116 118 119
		f 4 205 206 207 -203
		mu 0 4 116 120 121 118
		f 4 208 209 210 -207
		mu 0 4 120 122 123 121
		f 4 211 -210 212 213
		mu 0 4 124 123 122 125
		f 4 214 215 216 -214
		mu 0 4 125 126 127 124
		f 4 -216 217 218 219
		mu 0 4 127 126 128 129
		f 4 220 -219 221 222
		mu 0 4 130 129 128 131
		f 4 223 -223 224 225
		mu 0 4 132 130 131 133
		f 4 226 -226 227 228
		mu 0 4 134 132 133 135
		f 4 229 230 231 232
		mu 0 4 136 137 138 139
		f 4 -233 233 -229 -235
		mu 0 4 136 139 134 135
		f 4 -238 -237 -236 -1
		mu 0 4 0 140 141 1
		f 4 -240 237 -6 -239
		mu 0 4 142 140 0 5
		f 4 -243 235 -242 -241
		mu 0 4 143 1 141 144
		f 3 -244 -12 458
		mu 0 3 143 17 8
		f 4 -247 240 -246 -245
		mu 0 4 145 143 144 146
		f 4 245 -250 -249 -248
		mu 0 4 146 144 147 148
		f 4 -252 249 241 -251
		mu 0 4 149 147 144 141
		f 4 -254 250 236 -253
		mu 0 4 150 149 141 140
		f 4 -256 252 239 -255
		mu 0 4 151 150 140 142
		f 4 -258 243 246 -257
		mu 0 4 152 17 143 145
		f 3 -260 -29 -259
		mu 0 3 153 19 17
		f 4 -264 -263 261 -261
		mu 0 4 154 155 156 152
		f 4 -267 263 -266 -265
		mu 0 4 157 155 154 158
		f 4 264 -270 -269 -268
		mu 0 4 157 158 159 160
		f 4 268 -273 -272 -271
		mu 0 4 160 159 161 162
		f 4 -276 -275 265 -274
		mu 0 4 163 164 158 154
		f 4 269 274 -278 -277
		mu 0 4 159 158 164 165
		f 4 -281 275 -280 -279
		mu 0 4 166 164 163 167
		f 4 -283 277 280 -282
		mu 0 4 168 165 164 166
		f 4 -286 271 -285 -284
		mu 0 4 169 162 161 170
		f 4 -289 248 -288 -287
		mu 0 4 171 148 147 170
		f 4 -291 286 284 -290
		mu 0 4 172 171 170 161
		f 4 272 276 -292 289
		mu 0 4 161 159 165 172
		f 4 291 282 -294 -293
		mu 0 4 172 165 168 173
		f 4 -297 292 -296 -295
		mu 0 4 174 172 173 175
		f 4 -300 -299 -298 294
		mu 0 4 175 176 177 174
		f 4 -303 -302 298 -301
		mu 0 4 178 179 177 176
		f 4 -306 -305 302 -304
		mu 0 4 180 181 179 178
		f 4 -309 -308 305 -307
		mu 0 4 182 183 181 180
		f 4 -312 -311 308 -310
		mu 0 4 184 185 183 182
		f 4 -315 -314 279 -313
		mu 0 4 186 187 167 163
		f 4 -318 -317 314 -316
		mu 0 4 188 189 187 186
		f 4 -321 -320 311 -319
		mu 0 4 190 191 185 184
		f 4 -323 317 -322 320
		mu 0 4 190 189 188 191
		f 4 251 -325 -324 287
		mu 0 4 147 149 192 170
		f 4 323 -327 -326 283
		mu 0 4 170 192 193 169
		f 4 -331 -330 -329 -328
		mu 0 4 194 195 196 197
		f 4 -334 330 -333 -332
		mu 0 4 198 195 194 199
		f 4 -337 331 -336 -335
		mu 0 4 200 198 199 201
		f 4 -341 -340 -339 -338
		mu 0 4 202 203 204 205
		f 4 -112 -344 -343 -342
		mu 0 4 72 75 206 207
		f 4 -347 -346 -345 337
		mu 0 4 205 208 209 202
		f 4 343 -116 -349 -348
		mu 0 4 206 75 79 210
		f 4 -352 -351 266 -350
		mu 0 4 211 212 155 157
		f 4 -355 -354 344 -353
		mu 0 4 213 214 202 209
		f 4 -358 351 -357 -356
		mu 0 4 215 212 211 216
		f 4 -362 -361 -360 -359
		mu 0 4 217 218 219 220
		f 4 -365 -364 -363 359
		mu 0 4 219 214 221 220
		f 4 -367 334 -366 339
		mu 0 4 203 200 201 204
		f 4 353 364 -368 340
		mu 0 4 202 214 219 203
		f 4 360 -369 366 367
		mu 0 4 219 218 200 203
		f 4 -370 258 257 -262
		mu 0 4 156 153 17 152
		f 4 350 -371 369 262
		mu 0 4 155 212 153 156
		f 4 -374 -373 -372 357
		mu 0 4 215 222 223 212
		f 4 372 -376 -143 -375
		mu 0 4 223 222 94 93
		f 4 -379 361 -378 -377
		mu 0 4 224 218 217 225
		f 4 376 -382 -381 -380
		mu 0 4 224 225 226 227
		f 4 329 -384 380 -383
		mu 0 4 196 195 227 226
		f 4 336 368 378 -385
		mu 0 4 198 200 218 224
		f 4 383 333 384 379
		mu 0 4 227 195 198 224
		f 4 348 -152 -387 -386
		mu 0 4 210 79 100 228
		f 4 -390 354 -389 -388
		mu 0 4 229 214 213 230
		f 4 363 389 -392 -391
		mu 0 4 221 214 229 231
		f 4 -395 355 393 -393
		mu 0 4 232 215 216 233
		f 4 -397 373 394 -396
		mu 0 4 234 222 215 232
		f 4 -163 375 396 -398
		mu 0 4 107 94 222 234
		f 4 -401 -400 -399 342
		mu 0 4 206 235 236 207
		f 4 -403 400 347 -402
		mu 0 4 237 235 206 210
		f 4 -405 401 385 -404
		mu 0 4 238 237 210 228
		f 4 407 404 -407 405
		mu 0 4 239 237 238 240
		f 4 402 -408 409 408
		mu 0 4 235 237 239 241
		f 4 -412 399 -409 410
		mu 0 4 242 236 235 241
		f 4 413 -406 -413 388
		mu 0 4 213 239 240 230
		f 4 -414 352 414 -410
		mu 0 4 239 213 209 241
		f 4 -416 -411 -415 345
		mu 0 4 208 242 241 209
		f 4 -418 325 -417 328
		mu 0 4 196 169 193 197
		f 4 285 417 382 418
		mu 0 4 162 169 196 226
		f 4 419 270 -419 381
		mu 0 4 225 160 162 226
		f 4 420 267 -420 377
		mu 0 4 217 157 160 225
		f 4 349 -421 358 -422
		mu 0 4 211 157 217 220
		f 4 -423 356 421 362
		mu 0 4 221 216 211 220
		f 4 -394 422 390 -424
		mu 0 4 233 216 221 231
		f 4 -426 386 -201 -425
		mu 0 4 243 228 100 117
		f 4 -205 -428 -427 424
		mu 0 4 117 119 244 243
		f 4 426 -431 -430 -429
		mu 0 4 243 244 245 246
		f 4 429 -434 -433 -432
		mu 0 4 246 245 247 248
		f 4 -437 -436 432 -435
		mu 0 4 249 250 248 247
		f 4 436 -440 -439 -438
		mu 0 4 250 249 251 252
		f 4 -443 -442 -441 438
		mu 0 4 251 253 254 252
		f 4 -446 -445 441 -444
		mu 0 4 255 256 254 253
		f 4 -449 -448 445 -447
		mu 0 4 257 258 256 255
		f 4 -452 -451 448 -450
		mu 0 4 259 260 258 257
		f 4 -455 -454 -231 -453
		mu 0 4 261 262 138 137
		f 4 456 451 -456 454
		mu 0 4 261 260 259 262
		f 3 -458 11 12
		mu 0 3 6 8 17
		f 3 -459 -11 242
		mu 0 3 143 8 1
		f 4 -97 459 461 -461
		mu 0 4 61 60 263 264
		f 4 -101 462 463 -460
		mu 0 4 60 65 265 263
		f 4 -185 460 465 -465
		mu 0 4 59 61 264 266
		f 4 327 467 -469 -467
		mu 0 4 194 197 267 268
		f 4 332 466 -471 -470
		mu 0 4 199 194 268 269
		f 4 416 471 -473 -468
		mu 0 4 197 193 270 267;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -s -n "persp";
	rename -uid "87F144EC-400D-6453-41FD-83B177F0D067";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 6.936831067966299 10.261190386904183 23.028866570663237 ;
	setAttr ".r" -type "double3" -3.938352729602459 14.200000000000156 -2.0504989539943818e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "E42485FC-4482-7ABE-08DC-B6B5E4A3BD66";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 26.080077868107672;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "959AFD61-4BCA-8A22-DA23-54940C9BA37A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "1CBA9788-445D-BADA-59DA-B6851B04A12D";
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
	rename -uid "E41C582F-4C90-8F8D-2BC9-2DAE55DA6D74";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "6D993A90-4C33-E099-E6EA-DFB8309D8D70";
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
	rename -uid "6F549EB5-4E36-56F0-512D-9786E4FC8638";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "A4C8F16E-4F3C-394C-68BC-B6AFEC0DA784";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode skinCluster -n "skinCluster62";
	rename -uid "7A95BD64-440B-147F-AFC4-41BF9276B651";
	setAttr -s 28 ".wl";
	setAttr ".wl[0:27].w"
		1 0 1
		1 0 1
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 0 1
		1 0 1
		2 0 0.79999999701976776 2 0.20000000298023224
		2 0 0.79999999701976776 2 0.20000000298023224
		2 0 0.79999999701976776 2 0.20000000298023224
		2 0 0.79999999701976776 2 0.20000000298023224
		2 0 0.5 2 0.5
		2 0 0.5 2 0.5
		2 0 0.5 2 0.5
		2 0 0.5 2 0.5
		1 2 1
		1 2 1
		1 2 1
		1 2 1;
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0005179278627931651 -11.404634076679233 -4.5836510780331858 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2936375099999999 -11.708099369999999 -3.18370891 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2936375099999999 -11.708099369999999 -3.18370891 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".ma";
	setAttr -s 3 ".dpf[0:2]"  4 4 4;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 3 ".ifcl";
	setAttr -s 3 ".ifcl";
createNode dagPose -n "bindPose1";
	rename -uid "30E713A4-4DCD-800F-CBC1-EFA1E132387D";
	setAttr -s 61 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 61 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.0005179278627931651
		 11.404634076679233 4.5836510780331858 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.2936375099999999 11.708099369999999
		 3.18370891 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.2936375099999999 11.708099369999999
		 3.18370891 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.0043026870116591454
		 12.051765441894531 4.4915657043457031 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 9.1940898895263672 4.9873991012573242 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.00013379007577896118
		 6.6002101898193359 3.9838423728942871 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.00020532310009002686
		 6.4363861083984375 2.2802090644836426 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.2696250677108765 12.250021934509277
		 4.2430782318115234 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.269629955291748 12.25
		 4.2430801391601562 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.006993131192672742
		 12.795336806528523 4.3819678173877969 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.2662715789330123 12.820293228511485
		 4.1008545505959821 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.26627 12.8203 4.1008499999999994 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.0035460485101228433
		 10.684953592192102 4.4166141178970735 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.48544615507125854 10.479743003845215
		 4.091270923614502 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.0174989700317383 9.9180812835693359
		 3.4735996723175049 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.488699464537901 11.377700429276034
		 2.0811735543443213 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[17]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.0851883888244629 10.452959060668945
		 3.9599666595458984 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.7195367813110352 10.517522811889648
		 3.7072761058807373 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.48544599999999999
		 10.479699999999999 4.0912699999999997 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.0175000000000001 9.9180799999999998
		 3.4735999999999994 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.4887000000000001 11.377700000000001
		 2.0811699999999997 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.0851900000000001 10.452999999999999
		 3.9599699999999998 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.7195400000000001 10.5175
		 3.7072799999999995 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[24]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.60751229524612427 10.947669982910156
		 4.1484169960021973 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.1045808799999999 11.119100570000001
		 3.3660836199999999 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.60751200000000005
		 10.947699999999999 4.1484199999999989 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[27]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.1045808799999999 11.119100570000001
		 3.3660836199999999 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[28]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.68406617641448975 9.1593236923217773
		 4.1463994979858398 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[29]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.5147054195404053 9.1263513565063477
		 3.7214303016662598 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[30]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.4688956737518311 9.8356170654296875
		 2.2802839279174805 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[31]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.7821712493896484 8.1650552749633789
		 2.7745559215545654 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[32]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.4853637218475342 8.9519538879394531
		 1.1591391563415527 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[33]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.68406599999999995
		 9.1593199999999992 4.1463999999999999 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[34]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.51471 9.1263500000000004
		 3.7214299999999993 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[35]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.4689000000000001 9.8356200000000005
		 2.2802799999999994 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[36]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.78217 8.1650600000000004
		 2.7745600000000001 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[37]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.48536 8.9519500000000001
		 1.1591400000000001 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[38]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.0001399647444486618
		 8.9019374847412109 4.3592944145202637 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[39]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.55797863006591797 9.5878200531005859
		 4.4003925323486328 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[40]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.3591451644897461 8.2802190780639648
		 3.5942158699035645 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[41]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.88336926698684692 7.448793888092041
		 3.6904635429382324 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[42]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.557979 9.5878200000000007
		 4.4003899999999998 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[43]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.3591500000000001 8.2802199999999999
		 3.59422 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[44]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.88336899999999996
		 7.4487900000000007 3.6904599999999994 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[45]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.00015288963913917542
		 7.3639101982116699 4.0173206329345703 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[46]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.99284723180255674 8.0885326186972737
		 3.7272114197051991 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[47]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.99284700000000004
		 8.0885300000000004 3.7272099999999999 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[48]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.00013386458158493042
		 8.5648174285888672 4.3139505386352539 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[49]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.00014242157340049744
		 7.7093524932861328 4.1852841377258301 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[50]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.1278786659240723 6.9100303649902344
		 3.181365966796875 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[51]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.12788 6.910029999999999
		 3.1813699999999994 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[52]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.3214733600616455 8.2154808044433594
		 0.95036953687667847 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[53]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.3214700000000001 8.2154799999999994
		 0.95036999999999994 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[54]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.0001700669527053833
		 3.7229316234588623 1.3687072992324829 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[55]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.2843880653381348 7.2621726989746094
		 0.2006085216999054 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[56]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.2843900000000001 7.2621700000000002
		 0.20060900000000004 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[57]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.81796157360076904 5.6688408851623535
		 1.2600280046463013 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[58]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.81796199999999997
		 5.6688400000000003 1.26003 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[59]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.6888468265533447 4.418698787689209
		 0.0003346707671880722 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[60]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.68885 4.4187000000000003
		 0.00033467100000006411 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 61 ".m";
	setAttr -s 61 ".p";
	setAttr ".bp" yes;
createNode groupParts -n "groupParts310";
	rename -uid "4294EF8F-45B1-059D-3780-2CAA7AAF6349";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0:6]";
createNode polyPlanarProj -n "polyPlanarProj1";
	rename -uid "D2361638-47DA-41B5-A720-E28593D89CA9";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:6]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 11.504711151123047 3.8836798667907715 ;
	setAttr ".ps" -type "double2" 4.9736752510070801 0.79317569732666016 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode groupId -n "groupId3038";
	rename -uid "F885B01F-4CA2-5D34-B866-8CAD74516D27";
	setAttr ".ihi" 0;
createNode shadingEngine -n "lambert3SG";
	rename -uid "C0F12F41-4305-7608-DDE0-2BA09002F956";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo36";
	rename -uid "F874C3D5-4CDC-D148-CA86-3DAAB09FCA11";
createNode lambert -n "lambert3";
	rename -uid "0BBD60FB-4E27-B1E6-3187-ED9FF459E453";
	setAttr ".c" -type "float3" 1 0.5 0 ;
createNode skinCluster -n "skinCluster66";
	rename -uid "E290AE57-4AE8-AC4C-E2EA-39AEF9F5E159";
	setAttr -s 24 ".wl";
	setAttr ".wl[0:23].w"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		1 3 1
		1 3 1
		1 3 1
		1 3 1;
	setAttr -s 4 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0851883888244629 -10.452959060668945 -3.9599666595458984 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7195367813110352 -10.517522811889648 -3.7072761058807373 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.0851900000000001 -10.452999999999999 -3.9599699999999998 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7195400000000001 -10.5175 -3.7072799999999995 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 4 ".dpf[0:3]"  4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj2";
	rename -uid "2ED69631-4076-7D3C-18A8-6C874FA4C7F7";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:5]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 10.477306365966797 3.8336215019226074 ;
	setAttr ".ps" -type "double2" 3.8254740238189697 0.46683311462402344 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo38";
	rename -uid "AAD5A12C-4873-9A39-13D8-859C64DBDB12";
createNode shadingEngine -n "lambert5SG";
	rename -uid "76F8A0D9-4190-62C5-6678-1CA18C96804B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert5";
	rename -uid "CE23974E-4666-56D5-5B4C-DFA3F4551D66";
	setAttr ".c" -type "float3" 1 0.31400001 0.31400001 ;
createNode groupId -n "groupId3041";
	rename -uid "5BD530D3-4837-63F2-2E6D-E096524EBC8A";
	setAttr ".ihi" 0;
createNode shadingEngine -n "lambert4SG";
	rename -uid "84BB09D9-4E9B-FF4A-717F-2CBF74EFED0E";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo37";
	rename -uid "0E633A66-45A8-B9E7-DEC7-A2B182E24B17";
createNode lambert -n "lambert4";
	rename -uid "A789E88E-4631-442E-42D2-F6BA91857BE7";
	setAttr ".c" -type "float3" 0 1 0.38461661 ;
createNode skinCluster -n "skinCluster65";
	rename -uid "5555EDFE-48B2-CA52-AFF0-F2A72A75276A";
	setAttr -s 48 ".wl";
	setAttr ".wl[0:47].w"
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		1 5 1
		1 5 1
		1 5 1
		1 5 1
		1 3 1
		1 3 1
		1 3 1
		1 3 1
		2 4 0.69999998807907104 5 0.30000001192092896
		2 4 0.69999998807907104 5 0.30000001192092896
		2 4 0.69999998807907104 5 0.30000001192092896
		2 4 0.69999998807907104 5 0.30000001192092896
		2 3 0.5 4 0.5
		2 3 0.5 4 0.5
		2 3 0.5 4 0.5
		2 3 0.5 4 0.5
		1 4 1
		1 4 1
		1 4 1
		1 4 1
		2 4 0.30000001192092896 5 0.69999998807907104
		2 4 0.30000001192092896 5 0.69999998807907104
		2 4 0.30000001192092896 5 0.69999998807907104
		2 4 0.30000001192092896 5 0.69999998807907104;
	setAttr -s 6 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.48544615507125854 -10.479743003845215 -4.091270923614502 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0174989700317383 -9.9180812835693359 -3.4735996723175049 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.488699464537901 -11.377700429276034 -2.0811735543443213 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.48544599999999999 -10.479699999999999 -4.0912699999999997 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0175000000000001 -9.9180799999999998 -3.4735999999999994 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4887000000000001 -11.377700000000001 -2.0811699999999997 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 6 ".ma";
	setAttr -s 6 ".dpf[0:5]"  4 4 4 4 4 4;
	setAttr -s 6 ".lw";
	setAttr -s 6 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 6 ".ifcl";
	setAttr -s 6 ".ifcl";
createNode groupParts -n "groupParts313";
	rename -uid "9621FAC0-4830-5F5E-DD94-A18CB0FD4D35";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0:11]";
createNode polyPlanarProj -n "polyPlanarProj3";
	rename -uid "C1966094-48F3-22E0-4086-2CB9E1653317";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:11]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 10.594684600830078 3.0862221717834473 ;
	setAttr ".ps" -type "double2" 5.3637990951538086 1.9524316787719727 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode skinCluster -n "skinCluster69";
	rename -uid "7B69370C-4F5F-7E31-178D-CBB3FBD9A50B";
	setAttr -s 24 ".wl";
	setAttr ".wl[0:23].w"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		1 3 1
		1 3 1
		1 3 1
		1 3 1;
	setAttr -s 4 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5147054195404053 -9.1263513565063477 -3.7214303016662598 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4688956737518311 -9.8356170654296875 -2.2802839279174805 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.51471 -9.1263500000000004 -3.7214299999999993 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4689000000000001 -9.8356200000000005 -2.2802799999999994 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 4 ".dpf[0:3]"  4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj4";
	rename -uid "9E78AD44-4EC7-9DD5-37C1-ED8F57811487";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:5]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 9.4809837341308594 3.0008571147918701 ;
	setAttr ".ps" -type "double2" 5.3241915702819824 1.0956659317016602 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo40";
	rename -uid "404EA08C-4BF1-74F3-971D-DCB6318C1B37";
createNode shadingEngine -n "lambert7SG";
	rename -uid "CD0B2FCC-4EAD-DA5D-FB44-078CFD48B0A2";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert7";
	rename -uid "679A7463-4BFB-B8C7-3ADA-08945F85AE8E";
	setAttr ".c" -type "float3" 0.84614992 1 0 ;
createNode skinCluster -n "skinCluster70";
	rename -uid "C6F79FE6-480A-C27F-3EF8-579F7192DB64";
	setAttr -s 24 ".wl";
	setAttr ".wl[0:23].w"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.52941179275512695 1 0.47058820724487305
		2 0 0.5 1 0.5
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.52941179275512695 3 0.47058820724487305
		2 2 0.5 3 0.5
		1 3 1
		1 3 1
		1 3 1
		1 3 1;
	setAttr -s 4 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7821712493896484 -8.1650552749633789 -2.7745559215545654 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4853637218475342 -8.9519538879394531 -1.1591391563415527 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.78217 -8.1650600000000004 -2.7745600000000001 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.48536 -8.9519500000000001 -1.1591400000000001 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 4 ".dpf[0:3]"  4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj5";
	rename -uid "BB04F8D4-408F-1E09-51E0-80BFA24865CF";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:5]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 8.5585041046142578 1.9668475389480591 ;
	setAttr ".ps" -type "double2" 5.3571276664733887 1.1732988357543945 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo41";
	rename -uid "FAC09822-4162-B7E1-ED95-A5869B379067";
createNode shadingEngine -n "lambert8SG";
	rename -uid "473DA6B6-4428-5CBD-DF48-A4BE9C93CEAA";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
createNode lambert -n "lambert8";
	rename -uid "EC725979-4B86-5128-FAE3-C8A8E9727B51";
	setAttr ".c" -type "float3" 1 0.69231671 0 ;
createNode groupId -n "groupId3044";
	rename -uid "43C6F7D3-437B-4A78-55A3-898F3F527B5A";
	setAttr ".ihi" 0;
createNode shadingEngine -n "lambert6SG";
	rename -uid "B71D0DBF-4297-699B-F877-E5976AEA7DC7";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo39";
	rename -uid "2861B305-422B-7C99-DED0-EC995AA0FFFF";
createNode lambert -n "lambert6";
	rename -uid "B2E8CD43-46CA-4826-33E0-87997C659AEC";
	setAttr ".c" -type "float3" 0 1 1 ;
createNode skinCluster -n "skinCluster75";
	rename -uid "CDDD273F-4DC6-9D3B-0176-268E1FF574BE";
	setAttr -s 60 ".wl";
	setAttr ".wl[0:59].w"
		1 6 1
		1 6 1
		1 4 1
		1 4 1
		1 4 1
		1 4 1
		2 4 0.69999998807907104 6 0.30000001192092896
		2 4 0.69999998807907104 6 0.30000001192092896
		2 4 0.69999998807907104 6 0.30000001192092896
		2 4 0.69999998807907104 6 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 3 0.30000001192092896 4 0.69999998807907104
		2 3 0.30000001192092896 4 0.69999998807907104
		2 3 0.30000001192092896 4 0.69999998807907104
		2 3 0.30000001192092896 4 0.69999998807907104
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 3 1
		1 3 1
		1 3 1
		1 3 1
		2 4 0.30000001192092896 6 0.69999998807907104
		2 4 0.30000001192092896 6 0.69999998807907104
		2 4 0.30000001192092896 6 0.69999998807907104
		2 4 0.30000001192092896 6 0.69999998807907104
		1 6 1
		1 6 1
		1 5 1
		1 5 1
		1 5 1
		1 5 1
		2 5 0.69999998807907104 6 0.30000001192092896
		2 5 0.69999998807907104 6 0.30000001192092896
		2 5 0.69999998807907104 6 0.30000001192092896
		2 5 0.69999998807907104 6 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 2 0.30000001192092896 5 0.69999998807907104
		2 2 0.30000001192092896 5 0.69999998807907104
		2 2 0.30000001192092896 5 0.69999998807907104
		2 2 0.30000001192092896 5 0.69999998807907104
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		2 5 0.30000001192092896 6 0.69999998807907104
		2 5 0.30000001192092896 6 0.69999998807907104
		2 5 0.30000001192092896 6 0.69999998807907104
		2 5 0.30000001192092896 6 0.69999998807907104;
	setAttr -s 7 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.55797863006591797 -9.5878200531005859 -4.4003925323486328 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.557979 -9.5878200000000007 -4.4003899999999998 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3591500000000001 -8.2802199999999999 -3.59422 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3591451644897461 -8.2802190780639648 -3.5942158699035645 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.88336926698684692 -7.448793888092041 -3.6904635429382324 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.88336899999999996 -7.4487900000000007 -3.6904599999999994 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00015288963913917542 -7.3639101982116699 -4.0173206329345703 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 7 ".ma";
	setAttr -s 7 ".dpf[0:6]"  4 4 4 4 4 4 4;
	setAttr -s 7 ".lw";
	setAttr -s 7 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 7 ".ifcl";
	setAttr -s 7 ".ifcl";
createNode groupParts -n "groupParts316";
	rename -uid "C6ACAB4A-4214-8894-B007-779DA3379344";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0:14]";
createNode polyPlanarProj -n "polyPlanarProj6";
	rename -uid "8A76EAAC-43F8-7A47-F232-828CF760F6E2";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:14]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 8.4758644104003906 3.985405445098877 ;
	setAttr ".ps" -type "double2" 3.1046905517578125 2.6103105545043945 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode groupId -n "groupId3043";
	rename -uid "7C723EE1-4524-C0E8-1377-C5B707C94CC0";
	setAttr ".ihi" 0;
createNode shadingEngine -n "lambert9SG";
	rename -uid "5356569C-421B-57A4-7F76-A09A6E165254";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo42";
	rename -uid "DBA2E0B5-47A5-453D-2410-44B23F68596C";
createNode lambert -n "lambert9";
	rename -uid "106FB3D0-44EA-4199-F67D-DB9F3F83B809";
	setAttr ".c" -type "float3" 0 0.68400002 0.052611019 ;
createNode skinCluster -n "skinCluster71";
	rename -uid "E0D7C78D-4CF8-ECD9-1FE1-8B905C3BD929";
	setAttr -s 44 ".wl";
	setAttr ".wl[0:43].w"
		1 0 1
		1 0 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 0 0.69999998807907104 1 0.30000001192092896
		2 0 0.69999998807907104 1 0.30000001192092896
		2 0 0.69999998807907104 1 0.30000001192092896
		2 0 0.69999998807907104 1 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 0 1
		1 0 1
		1 3 1
		1 3 1
		1 3 1
		1 3 1
		2 3 0.30000001192092896 4 0.69999998807907104
		2 3 0.30000001192092896 4 0.69999998807907104
		2 3 0.30000001192092896 4 0.69999998807907104
		2 3 0.30000001192092896 4 0.69999998807907104
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 3 0.69999998807907104 4 0.30000001192092896
		2 3 0.69999998807907104 4 0.30000001192092896
		2 3 0.69999998807907104 4 0.30000001192092896
		2 3 0.69999998807907104 4 0.30000001192092896
		1 4 1
		1 4 1
		1 4 1
		1 4 1;
	setAttr -s 5 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00013379007577896118 -6.6002101898193359 -3.9838423728942871 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1278786659240723 -6.9100303649902344 -3.181365966796875 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3214733600616455 -8.2154808044433594 -0.95036953687667847 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.12788 -6.910029999999999 -3.1813699999999994 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3214700000000001 -8.2154799999999994 -0.95036999999999994 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 5 ".ma";
	setAttr -s 5 ".dpf[0:4]"  4 4 4 4 4;
	setAttr -s 5 ".lw";
	setAttr -s 5 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 5 ".ifcl";
	setAttr -s 5 ".ifcl";
createNode groupParts -n "groupParts315";
	rename -uid "E77E9B9E-45D4-65F9-D0CF-49B05E598619";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0:10]";
createNode polyPlanarProj -n "polyPlanarProj7";
	rename -uid "D777BB99-4C15-4314-207B-178506083A99";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:10]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 7.4078307151794434 2.4671061038970947 ;
	setAttr ".ps" -type "double2" 5.0293474197387695 2.0016984939575195 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode skinCluster -n "skinCluster68";
	rename -uid "740DB158-4FC4-08B6-5627-A3AE8867C3B9";
	setAttr -s 48 ".wl";
	setAttr ".wl[0:47].w"
		2 1 0.69999998807907116 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		1 0 1
		1 0 1
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 1 0.30000001192092896 2 0.69999998807907104
		2 0 0.69999998807907104 1 0.30000001192092896
		2 0 0.69999998807907104 1 0.30000001192092896
		2 0 0.69999998807907104 1 0.30000001192092896
		2 0 0.69999998807907104 1 0.30000001192092896
		1 2 1
		1 2 1
		2 0 0.30000001192092896 1 0.69999998807907104
		2 0 0.30000001192092896 1 0.69999998807907104
		2 0 0.30000001192092896 1 0.69999998807907104
		2 0 0.30000001192092896 1 0.69999998807907104
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 2 0.30000001192092896 3 0.69999998807907116
		2 2 0.30000001192092896 3 0.69999998807907104
		2 2 0.30000001192092896 3 0.69999998807907104
		2 2 0.30000001192092896 3 0.69999998807907104
		1 0 1
		1 0 1
		2 2 0.69999998807907104 3 0.30000001192092896
		2 2 0.69999998807907104 3 0.30000001192092896
		2 2 0.69999998807907104 3 0.30000001192092896
		2 2 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		2 0 0.69999998807907104 3 0.30000001192092896
		1 2 1
		1 2 1
		2 0 0.30000001192092896 3 0.69999998807907104
		2 0 0.30000001192092896 3 0.69999998807907104
		2 0 0.30000001192092896 3 0.69999998807907104
		2 0 0.30000001192092896 3 0.69999998807907104
		1 3 1
		1 3 1
		1 3 1
		1 3 1;
	setAttr -s 4 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00014242157340049744 -7.7093524932861328 -4.1852841377258301 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.99284723180255674 -8.0885326186972737 -3.7272114197051991 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00013386458158493042 -8.5648174285888672 -4.3139505386352539 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.99284700000000004 -8.0885300000000004 -3.7272099999999999 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 4 ".dpf[0:3]"  4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj8";
	rename -uid "CE1C2CB4-43D8-6270-BB61-6A9A2441FD3C";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:11]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 8.1315784454345703 4.0205812454223633 ;
	setAttr ".ps" -type "double2" 2.3720946311950684 1.2528791427612305 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo43";
	rename -uid "3051C15B-4FE7-8F0E-1525-BE89719C5C4E";
createNode shadingEngine -n "lambert10SG";
	rename -uid "090C8E8E-4029-D3D1-5691-59B0DCB05FEC";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert10";
	rename -uid "ED7F3B5C-4BDE-61FE-3AC7-2E8346DD07BE";
	setAttr ".c" -type "float3" 1 0.28799999 0.28799999 ;
createNode groupId -n "groupId3040";
	rename -uid "20DBE450-402D-99A1-7CAA-37BFBB4557C6";
	setAttr ".ihi" 0;
createNode skinCluster -n "skinCluster64";
	rename -uid "84734638-4877-5645-B086-588414ACC688";
	setAttr -s 28 ".wl";
	setAttr ".wl[0:27].w"
		1 0 1
		1 0 1
		1 1 1
		1 1 1
		1 4 1
		1 4 1
		2 2 0.5 4 0.5
		2 2 0.5 4 0.5
		2 2 0.5 4 0.5
		2 2 0.5 4 0.5
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 0 1
		1 0 1
		1 1 1
		1 1 1
		1 4 1
		1 4 1
		2 3 0.5 4 0.5
		2 3 0.5 4 0.5
		2 3 0.5 4 0.5
		2 3 0.5 4 0.5
		1 3 1
		1 3 1
		1 3 1
		1 3 1;
	setAttr -s 5 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -9.1940898895263672 -4.9873991012573242 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0035460485101228433 -10.684953592192102 -4.4166141178970735 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.68406617641448975 -9.1593236923217773 -4.1463994979858398 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.68406599999999995 -9.1593199999999992 -4.1463999999999999 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001399647444486618 -8.9019374847412109 -4.3592944145202637 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 5 ".ma";
	setAttr -s 5 ".dpf[0:4]"  4 4 4 4 4;
	setAttr -s 5 ".lw";
	setAttr -s 5 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 5 ".ifcl";
	setAttr -s 5 ".ifcl";
createNode groupParts -n "groupParts312";
	rename -uid "0F7E4C58-41AF-A857-C50F-ECA3A02126ED";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0:6]";
createNode polyPlanarProj -n "polyPlanarProj9";
	rename -uid "FB10F051-407A-9275-8EE3-B593FDA54032";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:6]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 9.7934455871582031 4.566899299621582 ;
	setAttr ".ps" -type "double2" 1.7545326948165894 2.1694173812866211 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode groupId -n "groupId3039";
	rename -uid "924D5E2B-4B5B-5D04-0007-E9B9F57080E9";
	setAttr ".ihi" 0;
createNode shadingEngine -n "lambert11SG";
	rename -uid "C938F6B3-490A-AEC6-D745-7AB47E813D62";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo44";
	rename -uid "280980FD-471C-B83E-D8A1-B88E0531EF3A";
createNode lambert -n "lambert11";
	rename -uid "3832FD00-4FB3-9A8E-F9C3-139C980C4EB1";
	setAttr ".c" -type "float3" 0 0.38461661 1 ;
createNode skinCluster -n "skinCluster63";
	rename -uid "593FEB7F-4092-11A2-D2D9-F398BCA0D015";
	setAttr -s 24 ".wl";
	setAttr ".wl[0:23].w"
		1 4 1
		1 4 1
		1 4 1
		1 4 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 3 1
		1 3 1
		1 0 1
		1 0 1
		1 5 1
		1 5 1
		1 5 1
		1 5 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 3 1
		1 3 1
		1 0 1
		1 0 1;
	setAttr -s 6 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0043026870116591454 -12.051765441894531 -4.4915657043457031 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2696250677108765 -12.250021934509277 -4.2430782318115234 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.269629955291748 -12.25 -4.2430801391601562 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.006993131192672742 -12.795336806528523 -4.3819678173877969 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2662715789330123 -12.820293228511485 -4.1008545505959821 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.26627 -12.8203 -4.1008499999999994 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 6 ".ma";
	setAttr -s 6 ".dpf[0:5]"  4 4 4 4 4 4;
	setAttr -s 6 ".lw";
	setAttr -s 6 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 6 ".ifcl";
	setAttr -s 6 ".ifcl";
createNode groupParts -n "groupParts311";
	rename -uid "DAAA72DF-4A07-C6BD-FE59-99963DFEB322";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0:5]";
createNode polyPlanarProj -n "polyPlanarProj10";
	rename -uid "5A694A23-47D1-B2EA-A792-55A72D63AD10";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:5]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 12.436029434204102 4.2962102890014648 ;
	setAttr ".ps" -type "double2" 2.9256501197814941 1.1549282073974609 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode polyTweakUV -n "polyTweakUV1";
	rename -uid "FF902BC2-4309-5D80-F330-CF961C31A37C";
	setAttr ".uopa" yes;
	setAttr -s 9 ".uvtk";
	setAttr ".uvtk[4]" -type "float2" 0 -0.11652116 ;
	setAttr ".uvtk[5]" -type "float2" 0 -0.11652116 ;
	setAttr ".uvtk[6]" -type "float2" 0 -0.11652116 ;
	setAttr ".uvtk[7]" -type "float2" 0 -0.11652116 ;
	setAttr ".uvtk[12]" -type "float2" 0 -0.12234721 ;
	setAttr ".uvtk[13]" -type "float2" 0 -0.12234721 ;
	setAttr ".uvtk[14]" -type "float2" 0 -0.12234721 ;
	setAttr ".uvtk[15]" -type "float2" 0 -0.12234721 ;
createNode skinCluster -n "skinCluster72";
	rename -uid "C1C03DFF-43DB-F98E-9FF8-03B13570041C";
	setAttr -s 20 ".wl";
	setAttr ".wl[0:19].w"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 0 0.59999999403953552 1 0.40000000596046448
		2 0 0.59999999403953552 1 0.40000000596046448
		2 0 0.59999999403953552 1 0.40000000596046448
		2 0 0.59999999403953552 1 0.40000000596046448
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.79999999701976776 1 0.20000000298023224
		2 0 0.19999998807907104 1 0.80000001192092896
		2 0 0.19999998807907104 1 0.80000001192092896
		2 0 0.19999998807907104 1 0.80000001192092896
		2 0 0.19999998807907104 1 0.80000001192092896;
	setAttr -s 8 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00020532310009002686 -6.4363861083984375 -2.2802090644836426 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001700669527053833 -3.7229316234588623 -1.3687072992324829 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.81796157360076904 -5.6688408851623535 -1.2600280046463013 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.81796199999999997 -5.6688400000000003 -1.26003 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843880653381348 -7.2621726989746094 -0.2006085216999054 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843900000000001 -7.2621700000000002 -0.20060900000000004 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.6888468265533447 -4.418698787689209 -0.0003346707671880722 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.68885 -4.4187000000000003 -0.00033467100000006411 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 8 ".dpf[0:7]"  4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
	setAttr -s 8 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj11";
	rename -uid "92AF400B-4789-C75C-E49A-CBB6A619FEBA";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:4]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0.00018632411956787109 5.0796589851379395 1.7602410316467285 ;
	setAttr ".ps" -type "double2" 0.38653230667114258 3.0998544692993164 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo46";
	rename -uid "616A13B8-438C-8B42-537B-7EB7CBDCF5D0";
createNode shadingEngine -n "lambert13SG";
	rename -uid "8013E574-4733-DCC1-2969-F08BF7A49DD4";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert13";
	rename -uid "C9E314BA-4190-6BFD-DAB2-D48B1C20A14C";
	setAttr ".c" -type "float3" 1 0.5 0 ;
createNode skinCluster -n "skinCluster74";
	rename -uid "A09CF827-41A3-FFA7-ED0E-A68A7EC3A404";
	setAttr -s 16 ".wl";
	setAttr ".wl[0:15].w"
		2 4 0.5 5 0.5
		2 4 0.5 5 0.5
		2 4 0.5 5 0.5
		2 4 0.5 5 0.5
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		2 4 0.5 6 0.5
		2 4 0.5 6 0.5
		2 4 0.5 6 0.5
		2 4 0.5 6 0.5
		1 0 1
		1 0 1
		1 0 1
		1 0 1;
	setAttr -s 10 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.81796199999999997 -5.6688400000000003 -1.26003 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843900000000001 -7.2621700000000002 -0.20060900000000004 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.81796157360076904 -5.6688408851623535 -1.2600280046463013 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843880653381348 -7.2621726989746094 -0.2006085216999054 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00020532310009002686 -6.4363861083984375 -2.2802090644836426 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843880653381348 -7.2621726989746094 -0.2006085216999054 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843900000000001 -7.2621700000000002 -0.20060900000000004 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001700669527053833 -3.7229316234588623 -1.3687072992324829 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.6888468265533447 -4.418698787689209 -0.0003346707671880722 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.68885 -4.4187000000000003 -0.00033467100000006411 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 10 ".dpf[0:9]"  4 4 4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj12";
	rename -uid "F014F0DC-48AE-E55E-EB9D-239F8FDB300C";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:3]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 6.3430089950561523 1.3779069185256958 ;
	setAttr ".ps" -type "double2" 2.9021892547607422 1.734736442565918 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo47";
	rename -uid "6F885602-4AA7-748F-47E8-5194220261AB";
createNode shadingEngine -n "lambert14SG";
	rename -uid "13C93EA6-4134-F028-C585-398F5A99622C";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert14";
	rename -uid "5A9DB2CD-413C-A2D3-DB27-5DA273B6B8DE";
	setAttr ".c" -type "float3" 0 1 0.53846669 ;
createNode skinCluster -n "skinCluster73";
	rename -uid "47FFB74C-4096-CD79-CB5E-4688BC5066BF";
	setAttr -s 40 ".wl";
	setAttr ".wl[0:39].w"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		2 0 0.69999998807907104 4 0.30000001192092896
		2 0 0.69999998807907104 4 0.30000001192092896
		2 0 0.69999998807907104 4 0.30000001192092896
		2 0 0.69999998807907104 4 0.30000001192092896
		3 0 0.30000001192092896 4 0.39999997615814209 7 0.30000001192092896
		3 0 0.30000001192092896 4 0.39999997615814209 7 0.30000001192092896
		3 0 0.30000001192092896 4 0.39999997615814209 7 0.30000001192092896
		3 0 0.30000001192092896 4 0.39999997615814209 7 0.30000001192092896
		3 4 0.4899999833106996 6 0.30000001192092896 7 0.21000000476837144
		3 4 0.4899999833106996 6 0.30000001192092896 7 0.21000000476837144
		3 4 0.4899999833106996 6 0.30000001192092896 7 0.21000000476837144
		3 4 0.4899999833106996 6 0.30000001192092896 7 0.21000000476837144
		1 4 1
		1 4 1
		1 4 1
		1 4 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		2 1 0.69999998807907104 2 0.30000001192092896
		3 1 0.30000001192092896 2 0.39999997615814209 8 0.30000001192092896
		3 1 0.30000001192092896 2 0.39999997615814209 8 0.30000001192092896
		3 1 0.30000001192092896 2 0.39999997615814209 8 0.30000001192092896
		3 1 0.30000001192092896 2 0.39999997615814209 8 0.30000001192092896
		3 2 0.4899999833106996 6 0.30000001192092896 8 0.21000000476837144
		3 2 0.4899999833106996 6 0.30000001192092896 8 0.21000000476837144
		3 2 0.4899999833106996 6 0.30000001192092896 8 0.21000000476837144
		3 2 0.4899999833106996 6 0.30000001192092896 8 0.21000000476837144
		1 2 1
		1 2 1
		1 2 1
		1 2 1;
	setAttr -s 9 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843880653381348 -7.2621726989746094 -0.2006085216999054 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843900000000001 -7.2621700000000002 -0.20060900000000004 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.68885 -4.4187000000000003 -0.00033467100000006411 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001700669527053833 -3.7229316234588623 -1.3687072992324829 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.6888468265533447 -4.418698787689209 -0.0003346707671880722 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00020532310009002686 -6.4363861083984375 -2.2802090644836426 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001700669527053833 -3.7229316234588623 -1.3687072992324829 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.81796157360076904 -5.6688408851623535 -1.2600280046463013 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.81796199999999997 -5.6688400000000003 -1.26003 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 9 ".dpf[0:8]"  4 4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 3;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj13";
	rename -uid "A94689E7-45EE-A10B-418A-4C8A90870A0C";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:9]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 5.8404359817504883 0.51335811614990234 ;
	setAttr ".ps" -type "double2" 5.7640933990478516 3.2298741340637207 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo48";
	rename -uid "294C8629-4A0B-8EA7-84B1-32B513FE4A13";
createNode shadingEngine -n "lambert15SG";
	rename -uid "72E41C69-42CB-846C-2D36-D4A5E071B375";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert15";
	rename -uid "5F238082-4729-2073-A4EC-B9A7682787FE";
	setAttr ".c" -type "float3" 1 0.42299998 0.88903338 ;
createNode skinCluster -n "skinCluster76";
	rename -uid "A910FAB7-491E-7843-31E2-C7A32D095E3B";
	setAttr -s 24 ".wl";
	setAttr ".wl[0:23].w"
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		2 0 0.5 1 0.5
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		2 2 0.5 3 0.5
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 3 1
		1 3 1
		1 3 1
		1 3 1;
	setAttr -s 4 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.60751229524612427 -10.947669982910156 -4.1484169960021973 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1045808799999999 -11.119100570000001 -3.3660836199999999 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.60751200000000005 -10.947699999999999 -4.1484199999999989 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1045808799999999 -11.119100570000001 -3.3660836199999999 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".ma";
	setAttr -s 4 ".dpf[0:3]"  4 4 4 4;
	setAttr -s 4 ".lw";
	setAttr -s 4 ".lw";
	setAttr ".mmi" yes;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 4 ".ifcl";
	setAttr -s 4 ".ifcl";
createNode polyPlanarProj -n "polyPlanarProj14";
	rename -uid "EF851D29-4F3D-BE85-530D-37A768EE4F52";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[0:5]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ws" yes;
	setAttr ".pc" -type "double3" 0 11.048150062561035 3.7572503089904785 ;
	setAttr ".ps" -type "double2" 4.5955619812011719 0.58736038208007812 ;
	setAttr ".cam" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode materialInfo -n "materialInfo49";
	rename -uid "98F4F7CA-41AF-B665-43F2-63A22E0E877D";
createNode shadingEngine -n "lambert16SG";
	rename -uid "9C43613D-4D15-8943-8414-74AC43C4BF30";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert16";
	rename -uid "1D67CE2E-4862-0013-FA16-3597CB32935B";
	setAttr ".c" -type "float3" 0 0.96153331 1 ;
createNode skinCluster -n "skinCluster77";
	rename -uid "4F60DB4A-4F1A-F11D-1035-16AF2E4A165A";
	setAttr -s 452 ".wl";
	setAttr ".wl[0:451].w"
		1 6 1
		1 6 1
		1 5 1
		1 5 1
		1 5 1
		1 5 1
		1 4 1
		1 4 1
		1 4 1
		1 4 1
		1 3 1
		1 3 1
		1 3 1
		1 3 1
		1 6 1
		1 6 1
		1 2 1
		1 2 1
		1 2 1
		1 2 1
		1 1 1
		1 1 1
		1 1 1
		1 1 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 31 1
		1 31 1
		1 31 1
		1 31 1
		1 32 1
		1 32 1
		1 32 1
		1 32 1
		1 33 1
		1 33 1
		1 33 1
		1 33 1
		1 34 1
		1 34 1
		1 34 1
		1 34 1
		1 35 1
		1 35 1
		1 35 1
		1 35 1
		1 36 1
		1 36 1
		1 36 1
		1 36 1
		1 29 1
		1 29 1
		1 29 1
		1 29 1
		1 19 1
		1 19 1
		1 19 1
		1 19 1
		1 22 1
		1 22 1
		1 22 1
		1 22 1
		1 20 1
		1 20 1
		1 20 1
		1 20 1
		1 21 1
		1 21 1
		1 21 1
		1 21 1
		1 23 1
		1 23 1
		1 23 1
		1 23 1
		1 30 1
		1 30 1
		1 30 1
		1 30 1
		1 24 1
		1 24 1
		1 24 1
		1 24 1
		1 27 1
		1 27 1
		1 27 1
		1 27 1
		1 25 1
		1 25 1
		1 25 1
		1 25 1
		1 26 1
		1 26 1
		1 26 1
		1 26 1
		1 28 1
		1 28 1
		1 28 1
		1 28 1
		1 59 1
		1 59 1
		1 59 1
		1 59 1
		1 60 1
		1 60 1
		1 60 1
		1 60 1
		1 61 1
		1 61 1
		1 61 1
		1 61 1
		1 62 1
		1 62 1
		1 62 1
		1 62 1
		1 63 1
		1 63 1
		1 63 1
		1 63 1
		1 64 1
		1 64 1
		1 64 1
		1 64 1
		1 65 1
		1 65 1
		1 65 1
		1 65 1
		1 66 1
		1 66 1
		1 66 1
		1 66 1
		1 67 1
		1 67 1
		1 67 1
		1 67 1
		1 68 1
		1 68 1
		1 68 1
		1 68 1
		1 69 1
		1 69 1
		1 69 1
		1 69 1
		1 70 1
		1 70 1
		1 70 1
		1 70 1
		1 44 1
		1 44 1
		1 49 1
		1 49 1
		1 49 1
		1 49 1
		1 50 1
		1 50 1
		1 50 1
		1 50 1
		1 46 1
		1 46 1
		1 46 1
		1 46 1
		1 48 1
		1 48 1
		1 48 1
		1 48 1
		1 45 1
		1 45 1
		1 45 1
		1 45 1
		1 47 1
		1 47 1
		1 47 1
		1 47 1
		1 51 1
		1 51 1
		1 51 1
		1 51 1
		1 44 1
		1 44 1
		1 56 1
		1 56 1
		1 56 1
		1 56 1
		1 57 1
		1 57 1
		1 57 1
		1 57 1
		1 53 1
		1 53 1
		1 53 1
		1 53 1
		1 55 1
		1 55 1
		1 55 1
		1 55 1
		1 52 1
		1 52 1
		1 52 1
		1 52 1
		1 54 1
		1 54 1
		1 54 1
		1 54 1
		1 58 1
		1 58 1
		1 58 1
		1 58 1
		1 83 1
		1 83 1
		1 85 1
		1 85 1
		1 85 1
		1 85 1
		1 87 1
		1 87 1
		1 87 1
		1 87 1
		1 84 1
		1 84 1
		1 84 1
		1 84 1
		1 86 1
		1 86 1
		1 86 1
		1 86 1
		1 92 1
		1 92 1
		1 92 1
		1 92 1
		1 83 1
		1 83 1
		1 89 1
		1 89 1
		1 89 1
		1 89 1
		1 91 1
		1 91 1
		1 91 1
		1 91 1
		1 88 1
		1 88 1
		1 88 1
		1 88 1
		1 90 1
		1 90 1
		1 90 1
		1 90 1
		1 93 1
		1 93 1
		1 93 1
		1 93 1
		1 74 1
		1 74 1
		1 74 1
		1 74 1
		1 72 1
		1 72 1
		1 73 1
		1 73 1
		1 73 1
		1 73 1
		1 77 1
		1 77 1
		1 77 1
		1 77 1
		1 71 1
		1 71 1
		1 76 1
		1 76 1
		1 76 1
		1 76 1
		1 75 1
		1 75 1
		1 75 1
		1 75 1
		1 79 1
		1 79 1
		1 79 1
		1 79 1
		1 72 1
		1 72 1
		1 78 1
		1 78 1
		1 78 1
		1 78 1
		1 82 1
		1 82 1
		1 82 1
		1 82 1
		1 71 1
		1 71 1
		1 81 1
		1 81 1
		1 81 1
		1 81 1
		1 80 1
		1 80 1
		1 80 1
		1 80 1
		1 38 1
		1 38 1
		1 37 1
		1 37 1
		1 39 1
		1 39 1
		1 40 1
		1 40 1
		1 40 1
		1 40 1
		1 41 1
		1 41 1
		1 41 1
		1 41 1
		1 38 1
		1 38 1
		1 37 1
		1 37 1
		1 39 1
		1 39 1
		1 42 1
		1 42 1
		1 42 1
		1 42 1
		1 43 1
		1 43 1
		1 43 1
		1 43 1
		1 13 1
		1 13 1
		1 13 1
		1 13 1
		1 17 1
		1 17 1
		1 17 1
		1 17 1
		1 15 1
		1 15 1
		1 18 1
		1 18 1
		1 14 1
		1 14 1
		1 14 1
		1 14 1
		1 16 1
		1 16 1
		1 16 1
		1 16 1
		1 15 1
		1 15 1
		1 18 1
		1 18 1
		1 97 1
		1 97 1
		1 97 1
		1 97 1
		1 94 1
		1 94 1
		1 94 1
		1 94 1
		1 96 1
		1 96 1
		1 96 1
		1 96 1
		1 98 1
		1 98 1
		1 98 1
		1 98 1
		1 95 1
		1 95 1
		1 95 1
		1 95 1
		1 99 1
		1 99 1
		1 99 1
		1 99 1
		1 100 1
		1 100 1
		1 100 1
		1 100 1
		1 101 1
		1 101 1
		1 101 1
		1 101 1
		1 102 1
		1 102 1
		1 102 1
		1 102 1
		1 103 1
		1 103 1
		1 103 1
		1 103 1
		1 104 1
		1 104 1
		1 104 1
		1 104 1
		1 105 1
		1 105 1
		1 105 1
		1 105 1
		1 106 1
		1 106 1
		1 106 1
		1 106 1
		1 107 1
		1 107 1
		1 107 1
		1 107 1
		1 108 1
		1 108 1
		1 108 1
		1 108 1
		1 109 1
		1 109 1
		1 109 1
		1 109 1
		1 110 1
		1 110 1
		1 110 1
		1 110 1
		1 111 1
		1 111 1
		1 111 1
		1 111 1
		1 112 1
		1 112 1
		1 112 1
		1 112 1
		1 8 1
		1 8 1
		1 8 1
		1 8 1
		1 7 1
		1 7 1
		1 7 1
		1 7 1
		1 9 1
		1 9 1
		1 9 1
		1 9 1
		1 11 1
		1 11 1
		1 11 1
		1 11 1
		1 10 1
		1 10 1
		1 10 1
		1 10 1
		1 12 1
		1 12 1
		1 12 1
		1 12 1;
	setAttr -s 113 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2936375099999999 -11.708099369999999 -3.18370891 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3196300000000001 -11.589600000000001 -4.3698699999999988 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.424261 -11.301299999999999 -4.566889999999999 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2936375099999999 -11.708099369999999 -3.18370891 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3196271154966632 -11.589633941650392 -4.3698666511290511 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.42426148056983948 -11.301323890686035 -4.5668916702270508 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0005179278627931651 -11.404634076679233 -4.5836510780331858 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.60751229524612427 -10.947669982910156 -4.1484169960021973 1;
	setAttr ".pm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3015105428506657 -11.148630142211914 -4.1128321184325092 1;
	setAttr ".pm[9]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1045808799999999 -11.119100570000001 -3.3660836199999999 1;
	setAttr ".pm[10]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.60751200000000005 -10.947699999999999 -4.1484199999999989 1;
	setAttr ".pm[11]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3015099999999999 -11.1486 -4.1128299999999989 1;
	setAttr ".pm[12]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1045808799999999 -11.119100570000001 -3.3660836199999999 1;
	setAttr ".pm[13]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2662715789330123 -12.820293228511485 -4.1008545505959821 1;
	setAttr ".pm[14]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.26627 -12.8203 -4.1008499999999994 1;
	setAttr ".pm[15]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.006993131192672742 -12.795336806528523 -4.3819678173877969 1;
	setAttr ".pm[16]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.26963 -12.25 -4.2430799999999991 1;
	setAttr ".pm[17]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2696250141666134 -12.250022112576113 -4.243078369847626 1;
	setAttr ".pm[18]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0043026869075206385 -12.051765287669056 -4.4915656175565815 1;
	setAttr ".pm[19]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.48544615507125854 -10.479743003845215 -4.091270923614502 1;
	setAttr ".pm[20]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1483757495880127 -9.8116703033447266 -3.9840564727783203 1;
	setAttr ".pm[21]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0174989700317383 -9.9180812835693359 -3.4735996723175049 1;
	setAttr ".pm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3293492794036865 -10.312215805053711 -2.8753671646118164 1;
	setAttr ".pm[23]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3747775554656982 -10.946447372436523 -2.5630693435668945 1;
	setAttr ".pm[24]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.48544599999999999 -10.479699999999999 -4.0912699999999997 1;
	setAttr ".pm[25]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.14838 -9.8116699999999994 -3.9840599999999995 1;
	setAttr ".pm[26]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0175000000000001 -9.9180799999999998 -3.4735999999999994 1;
	setAttr ".pm[27]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3293499999999998 -10.312200000000001 -2.8753699999999998 1;
	setAttr ".pm[28]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3747799999999999 -10.946400000000001 -2.5630699999999997 1;
	setAttr ".pm[29]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.488699464537901 -11.377700429276034 -2.0811735543443213 1;
	setAttr ".pm[30]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4887000000000001 -11.377700000000001 -2.0811699999999997 1;
	setAttr ".pm[31]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.0851883888244629 -10.452959060668945 -3.9599666595458984 1;
	setAttr ".pm[32]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.4368371963500977 -10.437089920043945 -3.866206169128418 1;
	setAttr ".pm[33]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7195367813110352 -10.517522811889648 -3.7072761058807373 1;
	setAttr ".pm[34]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.0851900000000001 -10.452999999999999 -3.9599699999999998 1;
	setAttr ".pm[35]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.4368399999999999 -10.437099999999999 -3.8662099999999997 1;
	setAttr ".pm[36]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7195400000000001 -10.5175 -3.7072799999999995 1;
	setAttr ".pm[37]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0035460485101228433 -10.684953592192102 -4.4166141178970735 1;
	setAttr ".pm[38]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 -9.1940898895263672 -4.9873991012573242 1;
	setAttr ".pm[39]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001399647444486618 -8.9019374847412109 -4.3592944145202637 1;
	setAttr ".pm[40]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.34074118733406067 -8.9490175247192383 -4.2669734954833984 1;
	setAttr ".pm[41]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.68406617641448975 -9.1593236923217773 -4.1463994979858398 1;
	setAttr ".pm[42]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.34074100000000002 -8.9490200000000009 -4.2669699999999997 1;
	setAttr ".pm[43]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.68406599999999995 -9.1593199999999992 -4.1463999999999999 1;
	setAttr ".pm[44]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00015288963913917542 -7.3639101982116699 -4.0173206329345703 1;
	setAttr ".pm[45]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.55797863006591797 -9.5878200531005859 -4.4003925323486328 1;
	setAttr ".pm[46]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.97933292388916016 -9.1474685668945312 -4.0290870666503906 1;
	setAttr ".pm[47]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3591451644897461 -8.2802190780639648 -3.5942158699035645 1;
	setAttr ".pm[48]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1088805198669434 -7.6778407096862793 -3.5704183578491211 1;
	setAttr ".pm[49]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.88336926698684692 -7.448793888092041 -3.6904635429382324 1;
	setAttr ".pm[50]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.59475547075271606 -7.3706507682800293 -3.8599975109100342 1;
	setAttr ".pm[51]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.30864483118057251 -7.363917350769043 -3.9746146202087402 1;
	setAttr ".pm[52]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.557979 -9.5878200000000007 -4.4003899999999998 1;
	setAttr ".pm[53]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.97933300000000001 -9.1474700000000002 -4.0290900000000001 1;
	setAttr ".pm[54]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.3591500000000001 -8.2802199999999999 -3.59422 1;
	setAttr ".pm[55]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1088800000000001 -7.6778399999999998 -3.5704199999999995 1;
	setAttr ".pm[56]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.88336899999999996 -7.4487900000000007 -3.6904599999999994 1;
	setAttr ".pm[57]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.59475500000000003 -7.3706500000000013 -3.8599999999999994 1;
	setAttr ".pm[58]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.308645 -7.3639200000000002 -3.9746099999999998 1;
	setAttr ".pm[59]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5147054195404053 -9.1263513565063477 -3.7214303016662598 1;
	setAttr ".pm[60]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0180821418762207 -9.353449821472168 -3.154655933380127 1;
	setAttr ".pm[61]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4688956737518311 -9.8356170654296875 -2.2802839279174805 1;
	setAttr ".pm[62]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.51471 -9.1263500000000004 -3.7214299999999993 1;
	setAttr ".pm[63]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.0180799999999999 -9.3534500000000005 -3.1546599999999994 1;
	setAttr ".pm[64]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.4689000000000001 -9.8356200000000005 -2.2802799999999994 1;
	setAttr ".pm[65]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7821712493896484 -8.1650552749633789 -2.7745559215545654 1;
	setAttr ".pm[66]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2596127986907959 -8.5387134552001953 -1.9980354309082031 1;
	setAttr ".pm[67]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.4853637218475342 -8.9519538879394531 -1.1591391563415527 1;
	setAttr ".pm[68]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.78217 -8.1650600000000004 -2.7745600000000001 1;
	setAttr ".pm[69]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2596099999999999 -8.53871 -1.99804 1;
	setAttr ".pm[70]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.48536 -8.9519500000000001 -1.1591400000000001 1;
	setAttr ".pm[71]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00013386458158493042 -8.5648174285888672 -4.3139505386352539 1;
	setAttr ".pm[72]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00014242157340049744 -7.7093524932861328 -4.1852841377258301 1;
	setAttr ".pm[73]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.46668782830238342 -8.5426998138427734 -4.2592430114746094 1;
	setAttr ".pm[74]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.94075167179107666 -8.4675283432006836 -3.9406640529632568 1;
	setAttr ".pm[75]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.99284723180255674 -8.0885326186972737 -3.7272114197051991 1;
	setAttr ".pm[76]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.7256704568862915 -7.7689285278320312 -3.9046978950500488 1;
	setAttr ".pm[77]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.37883636430257894 -7.6983378277550338 -4.0993888126205738 1;
	setAttr ".pm[78]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.46668799999999999 -8.5427 -4.2592400000000001 1;
	setAttr ".pm[79]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.94075200000000003 -8.46753 -3.9406599999999998 1;
	setAttr ".pm[80]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.99284700000000004 -8.0885300000000004 -3.7272099999999999 1;
	setAttr ".pm[81]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.72567000000000004 -7.768930000000001 -3.9046999999999996 1;
	setAttr ".pm[82]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.37883600000000001 -7.69834 -4.0993899999999996 1;
	setAttr ".pm[83]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00013379007577896118 -6.6002101898193359 -3.9838423728942871 1;
	setAttr ".pm[84]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.45245867967605591 -6.6001815795898438 -3.9173324108123779 1;
	setAttr ".pm[85]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.1278786659240723 -6.9100303649902344 -3.181365966796875 1;
	setAttr ".pm[86]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.5985672473907471 -7.2785587310791016 -2.6469697952270508 1;
	setAttr ".pm[87]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.0158641338348389 -7.6900086402893066 -1.8765504360198975 1;
	setAttr ".pm[88]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.452459 -6.6001799999999999 -3.9173299999999998 1;
	setAttr ".pm[89]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.12788 -6.910029999999999 -3.1813699999999994 1;
	setAttr ".pm[90]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.59857 -7.2785599999999988 -2.6469699999999996 1;
	setAttr ".pm[91]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.01586 -7.6900099999999991 -1.8765499999999999 1;
	setAttr ".pm[92]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3214733600616455 -8.2154808044433594 -0.95036953687667847 1;
	setAttr ".pm[93]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3214700000000001 -8.2154799999999994 -0.95037000000000005 1;
	setAttr ".pm[94]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001681596040725708 -5.6298894882202148 -1.5964155197143555 1;
	setAttr ".pm[95]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00012038276327075437 -4.5665569305419922 -1.2402728796005249 1;
	setAttr ".pm[96]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.0001700669527053833 -3.7229316234588623 -1.3687072992324829 1;
	setAttr ".pm[97]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.00020532310009002686 -6.4363861083984375 -2.2802090644836426 1;
	setAttr ".pm[98]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.000252552330493927 -6.2460217475891113 -1.785294771194458 1;
	setAttr ".pm[99]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.25789475440979 -7.0171771049499512 -1.4957858324050903 1;
	setAttr ".pm[100]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.81796157360076904 -5.6688408851623535 -1.2600280046463013 1;
	setAttr ".pm[101]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.25789 -7.0171799999999998 -1.4957899999999997 1;
	setAttr ".pm[102]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.81796199999999997 -5.6688400000000003 -1.26003 1;
	setAttr ".pm[103]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2843880653381348 -7.2621726989746094 -0.2006085216999054 1;
	setAttr ".pm[104]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2235007286071777 -6.4888582229614258 -0.40176340937614441 1;
	setAttr ".pm[105]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1431691646575928 -5.6174063682556152 -0.64830487966537476 1;
	setAttr ".pm[106]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6647086143493652 -4.4866776466369629 -1.0263814926147461 1;
	setAttr ".pm[107]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.6888468265533447 -4.418698787689209 -0.0003346707671880722 1;
	setAttr ".pm[108]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2843900000000001 -7.2621700000000002 -0.20060900000000001 1;
	setAttr ".pm[109]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2235 -6.4888599999999999 -0.40176300000000004 1;
	setAttr ".pm[110]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.14317 -5.6174099999999996 -0.64830500000000002 1;
	setAttr ".pm[111]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6647099999999999 -4.4866799999999998 -1.0263800000000001 1;
	setAttr ".pm[112]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.68885 -4.4187000000000003 -0.00033467100000000166 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 113 ".ma";
	setAttr -s 113 ".dpf[0:112]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 113 ".lw";
	setAttr -s 113 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 4;
	setAttr ".bm" 3;
	setAttr ".ucm" yes;
	setAttr -s 113 ".ifcl";
	setAttr -s 113 ".ifcl";
createNode materialInfo -n "materialInfo50";
	rename -uid "6A5C052B-4689-7A94-BC66-28B4E182D50C";
createNode shadingEngine -n "lambert17SG";
	rename -uid "EB760B37-4E7E-53B1-12FA-3B8D15D41919";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert17";
	rename -uid "33C68A1E-4B66-DAD6-1370-0C8907C4A139";
createNode materialInfo -n "materialInfo51";
	rename -uid "40B3E915-4917-5AA6-77D4-A1A89081DF54";
createNode shadingEngine -n "lambert18SG";
	rename -uid "F6DFB3F4-4DBB-994C-E174-D2B66A0EE60B";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode lambert -n "lambert18";
	rename -uid "9C364ED9-4A96-825E-B576-9E9AE8E7016E";
	setAttr ".c" -type "float3" 0.88461637 0 1 ;
	setAttr ".it" -type "float3" 0.76282054 0.76282054 0.76282054 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "D9D611ED-4D72-236C-1A7B-47995D5F661C";
	setAttr -s 17 ".lnk";
	setAttr -s 17 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "3FD081D7-41A5-711A-5135-398D1D35C240";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "B4CF3E80-45E4-F8E2-1D54-9E8EEC99350B";
createNode displayLayerManager -n "layerManager";
	rename -uid "062984F9-4386-29C3-5382-5DABE374FF34";
createNode displayLayer -n "defaultLayer";
	rename -uid "31D6E991-4EBA-63B8-2B6B-67B66F224F66";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "8FE81C72-42CB-F722-E546-9D9EB4DC1A70";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "560F75C3-437C-32AD-A752-79920090F853";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "878F00A3-4E31-5EA3-8302-378833AC15E8";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n"
		+ "            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n"
		+ "            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n"
		+ "            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n"
		+ "            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n"
		+ "            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n"
		+ "            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n"
		+ "            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 879\n            -height 672\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n"
		+ "            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -autoExpandAllAnimatedShapes 1\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n"
		+ "            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"print \\\"\\\"\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -autoExpandAllAnimatedShapes 1\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n"
		+ "            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n"
		+ "            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n"
		+ "                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -autoExpandAllAnimatedShapes 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n"
		+ "                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n"
		+ "                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -limitToSelectedCurves 0\n                -constrainDrag 0\n                -valueLinesToggle 0\n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n"
		+ "                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -autoExpandAllAnimatedShapes 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n"
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
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n"
		+ "                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n"
		+ "\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 879\\n    -height 672\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 879\\n    -height 672\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "E8F2B2BA-4286-A4CA-4DA8-D39D8662189C";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 30 -ast 0 -aet 30 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av -k on ".unw";
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
	setAttr -av ".tq" 1;
	setAttr -av ".etmr" no;
	setAttr -av ".tmr" 6144;
	setAttr -av ".aoon";
	setAttr -av ".aoam" 1.5;
	setAttr -av ".aora" 8;
	setAttr ".aosm" 8;
	setAttr -k on ".hff";
	setAttr -av ".hfd";
	setAttr -av ".hfs";
	setAttr -av ".hfe";
	setAttr -av ".hfc";
	setAttr -av -k on ".hfcr";
	setAttr -av -k on ".hfcg";
	setAttr -av -k on ".hfcb";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr -k on ".blen";
	setAttr -k on ".blat";
	setAttr -av ".msaa" yes;
	setAttr ".dli" 1;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 17 ".st";
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
	setAttr -s 20 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :standardSurface1;
	setAttr ".b" 0.80000001192092896;
	setAttr ".bc" -type "float3" 1 1 1 ;
	setAttr ".s" 0.20000000298023224;
	setAttr ".sr" 0.5;
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
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -av -k on ".macc";
	setAttr -av -k on ".macd";
	setAttr -av -k on ".macq";
	setAttr -av -k on ".mcfr";
	setAttr -k on ".ifg";
	setAttr -av -k on ".clip";
	setAttr -av -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -av -cb on ".ren" -type "string" "mayaHardware2";
	setAttr -av -k on ".esr";
	setAttr -av -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -k on ".exrc";
	setAttr -k on ".expt";
	setAttr -av -k on ".an";
	setAttr -k on ".ar";
	setAttr -k on ".fs";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -k on ".me";
	setAttr -k on ".se";
	setAttr -av -k on ".be";
	setAttr -av -k on ".ep";
	setAttr -av -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -k on ".ofe";
	setAttr -k on ".efe";
	setAttr -cb on ".oft";
	setAttr -k on ".umfn";
	setAttr -k on ".ufe";
	setAttr -av -k on ".pff";
	setAttr -av -k on ".peie";
	setAttr -av -cb on ".ifp";
	setAttr -k on ".rv";
	setAttr -av -k on ".comp";
	setAttr -av -k on ".cth";
	setAttr -av -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -av -k on ".rd";
	setAttr -av -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -av -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -k on ".gv";
	setAttr -k on ".sv";
	setAttr -av -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -av -k on ".itf";
	setAttr -av -k on ".shp";
	setAttr -k on ".isp";
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
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -cb on ".prm";
	setAttr -cb on ".pom";
	setAttr -k on ".pfrm";
	setAttr -k on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -av -k on ".ubc";
	setAttr -av -k on ".mbc";
	setAttr -k on ".mbt";
	setAttr -av -k on ".udbx";
	setAttr -av -k on ".smc";
	setAttr -av -k on ".kmv";
	setAttr -k on ".isl";
	setAttr -k on ".ism";
	setAttr -k on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -av -k on ".tlwd";
	setAttr -av -k on ".tlht";
	setAttr -av -k on ".jfc";
	setAttr -k on ".rsb";
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
	setAttr -av -k on ".w" 2048;
	setAttr -av -k on ".h" 2048;
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar" 1;
	setAttr -av -k on ".ldar";
	setAttr -av -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -cb on ".isu";
	setAttr -av -cb on ".pdu";
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
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
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "skinCluster62.og[0]" "brow_bs_meshShape.i";
connectAttr "groupId3038.id" "brow_bs_meshShape.iog.og[0].gid";
connectAttr "lambert3SG.mwc" "brow_bs_meshShape.iog.og[0].gco";
connectAttr "skinCluster66.og[0]" "lowlid_bs_meshShape.i";
connectAttr "groupId3041.id" "eyeFrame_bs_meshShape.iog.og[0].gid";
connectAttr "lambert4SG.mwc" "eyeFrame_bs_meshShape.iog.og[0].gco";
connectAttr "skinCluster65.og[0]" "eyeFrame_bs_meshShape.i";
connectAttr "skinCluster69.og[0]" "zyg_bs_meshShape.i";
connectAttr "skinCluster70.og[0]" "cheek_bs_meshShape.i";
connectAttr "groupId3044.id" "nosFlo_bs_meshShape.iog.og[0].gid";
connectAttr "lambert6SG.mwc" "nosFlo_bs_meshShape.iog.og[0].gco";
connectAttr "skinCluster75.og[0]" "nosFlo_bs_meshShape.i";
connectAttr "groupId3043.id" "chin_bs_meshShape.iog.og[0].gid";
connectAttr "lambert9SG.mwc" "chin_bs_meshShape.iog.og[0].gco";
connectAttr "skinCluster71.og[0]" "chin_bs_meshShape.i";
connectAttr "skinCluster68.og[0]" "lipFrame_bs_meshShape.i";
connectAttr "groupId3040.id" "nose_bs_meshShape.iog.og[0].gid";
connectAttr "lambert8SG.mwc" "nose_bs_meshShape.iog.og[0].gco";
connectAttr "skinCluster64.og[0]" "nose_bs_meshShape.i";
connectAttr "groupId3039.id" "forehead_bs_meshShape.iog.og[0].gid";
connectAttr "lambert11SG.mwc" "forehead_bs_meshShape.iog.og[0].gco";
connectAttr "skinCluster63.og[0]" "forehead_bs_meshShape.i";
connectAttr "polyTweakUV1.out" "throat_bs_meshShape.i";
connectAttr "polyTweakUV1.uvtk[0]" "throat_bs_meshShape.uvst[0].uvtw";
connectAttr "skinCluster74.og[0]" "chinThroat_bs_meshShape.i";
connectAttr "skinCluster73.og[0]" "clavicleNeck_bs_meshShape.i";
connectAttr "skinCluster76.og[0]" "browLid_bs_meshShape.i";
connectAttr "skinCluster77.og[0]" "base_bs_meshShape.i";
connectAttr "adj_brow_C_001_jnt_pointConstraint1.ctx" "adj_brow_C_001_jnt.tx";
connectAttr "adj_brow_C_001_jnt_pointConstraint1.cty" "adj_brow_C_001_jnt.ty";
connectAttr "adj_brow_C_001_jnt_pointConstraint1.ctz" "adj_brow_C_001_jnt.tz";
connectAttr "adj_brow_C_001_jnt.pim" "adj_brow_C_001_jnt_pointConstraint1.cpim";
connectAttr "adj_brow_C_001_jnt.rp" "adj_brow_C_001_jnt_pointConstraint1.crp";
connectAttr "adj_brow_C_001_jnt.rpt" "adj_brow_C_001_jnt_pointConstraint1.crt";
connectAttr "follicle115.t" "adj_brow_C_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle115.rp" "adj_brow_C_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle115.rpt" "adj_brow_C_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle115.pm" "adj_brow_C_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_brow_C_001_jnt_pointConstraint1.w0" "adj_brow_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_brow_L_001_jnt_pointConstraint1.ctx" "adj_brow_L_001_jnt.tx";
connectAttr "adj_brow_L_001_jnt_pointConstraint1.cty" "adj_brow_L_001_jnt.ty";
connectAttr "adj_brow_L_001_jnt_pointConstraint1.ctz" "adj_brow_L_001_jnt.tz";
connectAttr "adj_brow_L_001_jnt.pim" "adj_brow_L_001_jnt_pointConstraint1.cpim";
connectAttr "adj_brow_L_001_jnt.rp" "adj_brow_L_001_jnt_pointConstraint1.crp";
connectAttr "adj_brow_L_001_jnt.rpt" "adj_brow_L_001_jnt_pointConstraint1.crt";
connectAttr "follicle116.t" "adj_brow_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle116.rp" "adj_brow_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle116.rpt" "adj_brow_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle116.pm" "adj_brow_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_brow_L_001_jnt_pointConstraint1.w0" "adj_brow_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_brow_R_001_jnt_pointConstraint1.ctx" "adj_brow_R_001_jnt.tx";
connectAttr "adj_brow_R_001_jnt_pointConstraint1.cty" "adj_brow_R_001_jnt.ty";
connectAttr "adj_brow_R_001_jnt_pointConstraint1.ctz" "adj_brow_R_001_jnt.tz";
connectAttr "adj_brow_R_001_jnt.pim" "adj_brow_R_001_jnt_pointConstraint1.cpim";
connectAttr "adj_brow_R_001_jnt.rp" "adj_brow_R_001_jnt_pointConstraint1.crp";
connectAttr "adj_brow_R_001_jnt.rpt" "adj_brow_R_001_jnt_pointConstraint1.crt";
connectAttr "follicle114.t" "adj_brow_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle114.rp" "adj_brow_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle114.rpt" "adj_brow_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle114.pm" "adj_brow_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_brow_R_001_jnt_pointConstraint1.w0" "adj_brow_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_forehead_C_001_jnt_pointConstraint1.ctx" "adj_forehead_C_001_jnt.tx"
		;
connectAttr "adj_forehead_C_001_jnt_pointConstraint1.cty" "adj_forehead_C_001_jnt.ty"
		;
connectAttr "adj_forehead_C_001_jnt_pointConstraint1.ctz" "adj_forehead_C_001_jnt.tz"
		;
connectAttr "adj_forehead_C_001_jnt.pim" "adj_forehead_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_forehead_C_001_jnt.rp" "adj_forehead_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_forehead_C_001_jnt.rpt" "adj_forehead_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle119.t" "adj_forehead_C_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle119.rp" "adj_forehead_C_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle119.rpt" "adj_forehead_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle119.pm" "adj_forehead_C_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_forehead_C_001_jnt_pointConstraint1.w0" "adj_forehead_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_noseTip_C_001_jnt_pointConstraint1.ctx" "adj_noseTip_C_001_jnt.tx"
		;
connectAttr "adj_noseTip_C_001_jnt_pointConstraint1.cty" "adj_noseTip_C_001_jnt.ty"
		;
connectAttr "adj_noseTip_C_001_jnt_pointConstraint1.ctz" "adj_noseTip_C_001_jnt.tz"
		;
connectAttr "adj_noseTip_C_001_jnt.pim" "adj_noseTip_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_noseTip_C_001_jnt.rp" "adj_noseTip_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_noseTip_C_001_jnt.rpt" "adj_noseTip_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle148.t" "adj_noseTip_C_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle148.rp" "adj_noseTip_C_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle148.rpt" "adj_noseTip_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle148.pm" "adj_noseTip_C_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_noseTip_C_001_jnt_pointConstraint1.w0" "adj_noseTip_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_chin_C_001_jnt_pointConstraint1.ctx" "adj_chin_C_001_jnt.tx";
connectAttr "adj_chin_C_001_jnt_pointConstraint1.cty" "adj_chin_C_001_jnt.ty";
connectAttr "adj_chin_C_001_jnt_pointConstraint1.ctz" "adj_chin_C_001_jnt.tz";
connectAttr "adj_chin_C_001_jnt.pim" "adj_chin_C_001_jnt_pointConstraint1.cpim";
connectAttr "adj_chin_C_001_jnt.rp" "adj_chin_C_001_jnt_pointConstraint1.crp";
connectAttr "adj_chin_C_001_jnt.rpt" "adj_chin_C_001_jnt_pointConstraint1.crt";
connectAttr "follicle164.t" "adj_chin_C_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle164.rp" "adj_chin_C_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle164.rpt" "adj_chin_C_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle164.pm" "adj_chin_C_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_chin_C_001_jnt_pointConstraint1.w0" "adj_chin_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_forehead_L_001_jnt_pointConstraint1.ctx" "adj_forehead_L_001_jnt.tx"
		;
connectAttr "adj_forehead_L_001_jnt_pointConstraint1.cty" "adj_forehead_L_001_jnt.ty"
		;
connectAttr "adj_forehead_L_001_jnt_pointConstraint1.ctz" "adj_forehead_L_001_jnt.tz"
		;
connectAttr "adj_forehead_L_001_jnt.pim" "adj_forehead_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_forehead_L_001_jnt.rp" "adj_forehead_L_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_forehead_L_001_jnt.rpt" "adj_forehead_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle118.t" "adj_forehead_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle118.rp" "adj_forehead_L_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle118.rpt" "adj_forehead_L_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle118.pm" "adj_forehead_L_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_forehead_L_001_jnt_pointConstraint1.w0" "adj_forehead_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_forehead_R_001_jnt_pointConstraint1.ctx" "adj_forehead_R_001_jnt.tx"
		;
connectAttr "adj_forehead_R_001_jnt_pointConstraint1.cty" "adj_forehead_R_001_jnt.ty"
		;
connectAttr "adj_forehead_R_001_jnt_pointConstraint1.ctz" "adj_forehead_R_001_jnt.tz"
		;
connectAttr "adj_forehead_R_001_jnt.pim" "adj_forehead_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_forehead_R_001_jnt.rp" "adj_forehead_R_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_forehead_R_001_jnt.rpt" "adj_forehead_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle120.t" "adj_forehead_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle120.rp" "adj_forehead_R_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle120.rpt" "adj_forehead_R_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle120.pm" "adj_forehead_R_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_forehead_R_001_jnt_pointConstraint1.w0" "adj_forehead_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_forehead_C_002_jnt_pointConstraint1.ctx" "adj_forehead_C_002_jnt.tx"
		;
connectAttr "adj_forehead_C_002_jnt_pointConstraint1.cty" "adj_forehead_C_002_jnt.ty"
		;
connectAttr "adj_forehead_C_002_jnt_pointConstraint1.ctz" "adj_forehead_C_002_jnt.tz"
		;
connectAttr "adj_forehead_C_002_jnt.pim" "adj_forehead_C_002_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_forehead_C_002_jnt.rp" "adj_forehead_C_002_jnt_pointConstraint1.crp"
		;
connectAttr "adj_forehead_C_002_jnt.rpt" "adj_forehead_C_002_jnt_pointConstraint1.crt"
		;
connectAttr "follicle122.t" "adj_forehead_C_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle122.rp" "adj_forehead_C_002_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle122.rpt" "adj_forehead_C_002_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle122.pm" "adj_forehead_C_002_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_forehead_C_002_jnt_pointConstraint1.w0" "adj_forehead_C_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_forehead_L_002_jnt_pointConstraint1.ctx" "adj_forehead_L_002_jnt.tx"
		;
connectAttr "adj_forehead_L_002_jnt_pointConstraint1.cty" "adj_forehead_L_002_jnt.ty"
		;
connectAttr "adj_forehead_L_002_jnt_pointConstraint1.ctz" "adj_forehead_L_002_jnt.tz"
		;
connectAttr "adj_forehead_L_002_jnt.pim" "adj_forehead_L_002_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_forehead_L_002_jnt.rp" "adj_forehead_L_002_jnt_pointConstraint1.crp"
		;
connectAttr "adj_forehead_L_002_jnt.rpt" "adj_forehead_L_002_jnt_pointConstraint1.crt"
		;
connectAttr "follicle117.t" "adj_forehead_L_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle117.rp" "adj_forehead_L_002_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle117.rpt" "adj_forehead_L_002_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle117.pm" "adj_forehead_L_002_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_forehead_L_002_jnt_pointConstraint1.w0" "adj_forehead_L_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_forehead_R_002_jnt_pointConstraint1.ctx" "adj_forehead_R_002_jnt.tx"
		;
connectAttr "adj_forehead_R_002_jnt_pointConstraint1.cty" "adj_forehead_R_002_jnt.ty"
		;
connectAttr "adj_forehead_R_002_jnt_pointConstraint1.ctz" "adj_forehead_R_002_jnt.tz"
		;
connectAttr "adj_forehead_R_002_jnt.pim" "adj_forehead_R_002_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_forehead_R_002_jnt.rp" "adj_forehead_R_002_jnt_pointConstraint1.crp"
		;
connectAttr "adj_forehead_R_002_jnt.rpt" "adj_forehead_R_002_jnt_pointConstraint1.crt"
		;
connectAttr "follicle121.t" "adj_forehead_R_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle121.rp" "adj_forehead_R_002_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle121.rpt" "adj_forehead_R_002_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle121.pm" "adj_forehead_R_002_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_forehead_R_002_jnt_pointConstraint1.w0" "adj_forehead_R_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_noseRoot_C_001_jnt_pointConstraint1.ctx" "adj_noseRoot_C_001_jnt.tx"
		;
connectAttr "adj_noseRoot_C_001_jnt_pointConstraint1.cty" "adj_noseRoot_C_001_jnt.ty"
		;
connectAttr "adj_noseRoot_C_001_jnt_pointConstraint1.ctz" "adj_noseRoot_C_001_jnt.tz"
		;
connectAttr "adj_noseRoot_C_001_jnt.pim" "adj_noseRoot_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_noseRoot_C_001_jnt.rp" "adj_noseRoot_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_noseRoot_C_001_jnt.rpt" "adj_noseRoot_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle157.t" "adj_noseRoot_C_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle157.rp" "adj_noseRoot_C_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle157.rpt" "adj_noseRoot_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle157.pm" "adj_noseRoot_C_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_noseRoot_C_001_jnt_pointConstraint1.w0" "adj_noseRoot_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_eyeFrame_L_001_jnt_pointConstraint1.ctx" "adj_eyeFrame_L_001_jnt.tx"
		;
connectAttr "adj_eyeFrame_L_001_jnt_pointConstraint1.cty" "adj_eyeFrame_L_001_jnt.ty"
		;
connectAttr "adj_eyeFrame_L_001_jnt_pointConstraint1.ctz" "adj_eyeFrame_L_001_jnt.tz"
		;
connectAttr "adj_eyeFrame_L_001_jnt.pim" "adj_eyeFrame_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_eyeFrame_L_001_jnt.rp" "adj_eyeFrame_L_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_eyeFrame_L_001_jnt.rpt" "adj_eyeFrame_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle129.t" "adj_eyeFrame_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle129.rp" "adj_eyeFrame_L_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle129.rpt" "adj_eyeFrame_L_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle129.pm" "adj_eyeFrame_L_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_eyeFrame_L_001_jnt_pointConstraint1.w0" "adj_eyeFrame_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_eyeFrame_L_003_jnt_pointConstraint1.ctx" "adj_eyeFrame_L_003_jnt.tx"
		;
connectAttr "adj_eyeFrame_L_003_jnt_pointConstraint1.cty" "adj_eyeFrame_L_003_jnt.ty"
		;
connectAttr "adj_eyeFrame_L_003_jnt_pointConstraint1.ctz" "adj_eyeFrame_L_003_jnt.tz"
		;
connectAttr "adj_eyeFrame_L_003_jnt.pim" "adj_eyeFrame_L_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_eyeFrame_L_003_jnt.rp" "adj_eyeFrame_L_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_eyeFrame_L_003_jnt.rpt" "adj_eyeFrame_L_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle128.t" "adj_eyeFrame_L_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle128.rp" "adj_eyeFrame_L_003_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle128.rpt" "adj_eyeFrame_L_003_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle128.pm" "adj_eyeFrame_L_003_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_eyeFrame_L_003_jnt_pointConstraint1.w0" "adj_eyeFrame_L_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_bite_L_001_jnt_pointConstraint1.ctx" "adj_bite_L_001_jnt.tx";
connectAttr "adj_bite_L_001_jnt_pointConstraint1.cty" "adj_bite_L_001_jnt.ty";
connectAttr "adj_bite_L_001_jnt_pointConstraint1.ctz" "adj_bite_L_001_jnt.tz";
connectAttr "adj_bite_L_001_jnt.pim" "adj_bite_L_001_jnt_pointConstraint1.cpim";
connectAttr "adj_bite_L_001_jnt.rp" "adj_bite_L_001_jnt_pointConstraint1.crp";
connectAttr "adj_bite_L_001_jnt.rpt" "adj_bite_L_001_jnt_pointConstraint1.crt";
connectAttr "follicle127.t" "adj_bite_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle127.rp" "adj_bite_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle127.rpt" "adj_bite_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle127.pm" "adj_bite_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_bite_L_001_jnt_pointConstraint1.w0" "adj_bite_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_lowlid_L_001_jnt_pointConstraint1.ctx" "adj_lowlid_L_001_jnt.tx"
		;
connectAttr "adj_lowlid_L_001_jnt_pointConstraint1.cty" "adj_lowlid_L_001_jnt.ty"
		;
connectAttr "adj_lowlid_L_001_jnt_pointConstraint1.ctz" "adj_lowlid_L_001_jnt.tz"
		;
connectAttr "adj_lowlid_L_001_jnt.pim" "adj_lowlid_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_lowlid_L_001_jnt.rp" "adj_lowlid_L_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_lowlid_L_001_jnt.rpt" "adj_lowlid_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle123.t" "adj_lowlid_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle123.rp" "adj_lowlid_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle123.rpt" "adj_lowlid_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle123.pm" "adj_lowlid_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_lowlid_L_001_jnt_pointConstraint1.w0" "adj_lowlid_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_lowlid_L_003_jnt_pointConstraint1.ctx" "adj_lowlid_L_003_jnt.tx"
		;
connectAttr "adj_lowlid_L_003_jnt_pointConstraint1.cty" "adj_lowlid_L_003_jnt.ty"
		;
connectAttr "adj_lowlid_L_003_jnt_pointConstraint1.ctz" "adj_lowlid_L_003_jnt.tz"
		;
connectAttr "adj_lowlid_L_003_jnt.pim" "adj_lowlid_L_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_lowlid_L_003_jnt.rp" "adj_lowlid_L_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_lowlid_L_003_jnt.rpt" "adj_lowlid_L_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle124.t" "adj_lowlid_L_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle124.rp" "adj_lowlid_L_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle124.rpt" "adj_lowlid_L_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle124.pm" "adj_lowlid_L_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_lowlid_L_003_jnt_pointConstraint1.w0" "adj_lowlid_L_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_eyeFrame_R_001_jnt_pointConstraint1.ctx" "adj_eyeFrame_R_001_jnt.tx"
		;
connectAttr "adj_eyeFrame_R_001_jnt_pointConstraint1.cty" "adj_eyeFrame_R_001_jnt.ty"
		;
connectAttr "adj_eyeFrame_R_001_jnt_pointConstraint1.ctz" "adj_eyeFrame_R_001_jnt.tz"
		;
connectAttr "adj_eyeFrame_R_001_jnt.pim" "adj_eyeFrame_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_eyeFrame_R_001_jnt.rp" "adj_eyeFrame_R_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_eyeFrame_R_001_jnt.rpt" "adj_eyeFrame_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle130.t" "adj_eyeFrame_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle130.rp" "adj_eyeFrame_R_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle130.rpt" "adj_eyeFrame_R_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle130.pm" "adj_eyeFrame_R_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_eyeFrame_R_001_jnt_pointConstraint1.w0" "adj_eyeFrame_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_eyeFrame_R_003_jnt_pointConstraint1.ctx" "adj_eyeFrame_R_003_jnt.tx"
		;
connectAttr "adj_eyeFrame_R_003_jnt_pointConstraint1.cty" "adj_eyeFrame_R_003_jnt.ty"
		;
connectAttr "adj_eyeFrame_R_003_jnt_pointConstraint1.ctz" "adj_eyeFrame_R_003_jnt.tz"
		;
connectAttr "adj_eyeFrame_R_003_jnt.pim" "adj_eyeFrame_R_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_eyeFrame_R_003_jnt.rp" "adj_eyeFrame_R_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_eyeFrame_R_003_jnt.rpt" "adj_eyeFrame_R_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle131.t" "adj_eyeFrame_R_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle131.rp" "adj_eyeFrame_R_003_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle131.rpt" "adj_eyeFrame_R_003_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle131.pm" "adj_eyeFrame_R_003_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_eyeFrame_R_003_jnt_pointConstraint1.w0" "adj_eyeFrame_R_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_bite_R_001_jnt_pointConstraint1.ctx" "adj_bite_R_001_jnt.tx";
connectAttr "adj_bite_R_001_jnt_pointConstraint1.cty" "adj_bite_R_001_jnt.ty";
connectAttr "adj_bite_R_001_jnt_pointConstraint1.ctz" "adj_bite_R_001_jnt.tz";
connectAttr "adj_bite_R_001_jnt.pim" "adj_bite_R_001_jnt_pointConstraint1.cpim";
connectAttr "adj_bite_R_001_jnt.rp" "adj_bite_R_001_jnt_pointConstraint1.crp";
connectAttr "adj_bite_R_001_jnt.rpt" "adj_bite_R_001_jnt_pointConstraint1.crt";
connectAttr "follicle132.t" "adj_bite_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle132.rp" "adj_bite_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle132.rpt" "adj_bite_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle132.pm" "adj_bite_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_bite_R_001_jnt_pointConstraint1.w0" "adj_bite_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_lowlid_R_001_jnt_pointConstraint1.ctx" "adj_lowlid_R_001_jnt.tx"
		;
connectAttr "adj_lowlid_R_001_jnt_pointConstraint1.cty" "adj_lowlid_R_001_jnt.ty"
		;
connectAttr "adj_lowlid_R_001_jnt_pointConstraint1.ctz" "adj_lowlid_R_001_jnt.tz"
		;
connectAttr "adj_lowlid_R_001_jnt.pim" "adj_lowlid_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_lowlid_R_001_jnt.rp" "adj_lowlid_R_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_lowlid_R_001_jnt.rpt" "adj_lowlid_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle125.t" "adj_lowlid_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle125.rp" "adj_lowlid_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle125.rpt" "adj_lowlid_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle125.pm" "adj_lowlid_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_lowlid_R_001_jnt_pointConstraint1.w0" "adj_lowlid_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_lowlid_R_003_jnt_pointConstraint1.ctx" "adj_lowlid_R_003_jnt.tx"
		;
connectAttr "adj_lowlid_R_003_jnt_pointConstraint1.cty" "adj_lowlid_R_003_jnt.ty"
		;
connectAttr "adj_lowlid_R_003_jnt_pointConstraint1.ctz" "adj_lowlid_R_003_jnt.tz"
		;
connectAttr "adj_lowlid_R_003_jnt.pim" "adj_lowlid_R_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_lowlid_R_003_jnt.rp" "adj_lowlid_R_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_lowlid_R_003_jnt.rpt" "adj_lowlid_R_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle126.t" "adj_lowlid_R_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle126.rp" "adj_lowlid_R_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle126.rpt" "adj_lowlid_R_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle126.pm" "adj_lowlid_R_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_lowlid_R_003_jnt_pointConstraint1.w0" "adj_lowlid_R_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_browLid_L_001_jnt_pointConstraint1.ctx" "adj_browLid_L_001_jnt.tx"
		;
connectAttr "adj_browLid_L_001_jnt_pointConstraint1.cty" "adj_browLid_L_001_jnt.ty"
		;
connectAttr "adj_browLid_L_001_jnt_pointConstraint1.ctz" "adj_browLid_L_001_jnt.tz"
		;
connectAttr "adj_browLid_L_001_jnt.pim" "adj_browLid_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_browLid_L_001_jnt.rp" "adj_browLid_L_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_browLid_L_001_jnt.rpt" "adj_browLid_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle159.t" "adj_browLid_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle159.rp" "adj_browLid_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle159.rpt" "adj_browLid_L_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle159.pm" "adj_browLid_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_browLid_L_001_jnt_pointConstraint1.w0" "adj_browLid_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_browLid_L_003_jnt_pointConstraint1.ctx" "adj_browLid_L_003_jnt.tx"
		;
connectAttr "adj_browLid_L_003_jnt_pointConstraint1.cty" "adj_browLid_L_003_jnt.ty"
		;
connectAttr "adj_browLid_L_003_jnt_pointConstraint1.ctz" "adj_browLid_L_003_jnt.tz"
		;
connectAttr "adj_browLid_L_003_jnt.pim" "adj_browLid_L_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_browLid_L_003_jnt.rp" "adj_browLid_L_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_browLid_L_003_jnt.rpt" "adj_browLid_L_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle158.t" "adj_browLid_L_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle158.rp" "adj_browLid_L_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle158.rpt" "adj_browLid_L_003_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle158.pm" "adj_browLid_L_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_browLid_L_003_jnt_pointConstraint1.w0" "adj_browLid_L_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_browLid_R_001_jnt_pointConstraint1.ctx" "adj_browLid_R_001_jnt.tx"
		;
connectAttr "adj_browLid_R_001_jnt_pointConstraint1.cty" "adj_browLid_R_001_jnt.ty"
		;
connectAttr "adj_browLid_R_001_jnt_pointConstraint1.ctz" "adj_browLid_R_001_jnt.tz"
		;
connectAttr "adj_browLid_R_001_jnt.pim" "adj_browLid_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_browLid_R_001_jnt.rp" "adj_browLid_R_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_browLid_R_001_jnt.rpt" "adj_browLid_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle160.t" "adj_browLid_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle160.rp" "adj_browLid_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle160.rpt" "adj_browLid_R_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle160.pm" "adj_browLid_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_browLid_R_001_jnt_pointConstraint1.w0" "adj_browLid_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_browLid_R_003_jnt_pointConstraint1.ctx" "adj_browLid_R_003_jnt.tx"
		;
connectAttr "adj_browLid_R_003_jnt_pointConstraint1.cty" "adj_browLid_R_003_jnt.ty"
		;
connectAttr "adj_browLid_R_003_jnt_pointConstraint1.ctz" "adj_browLid_R_003_jnt.tz"
		;
connectAttr "adj_browLid_R_003_jnt.pim" "adj_browLid_R_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_browLid_R_003_jnt.rp" "adj_browLid_R_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_browLid_R_003_jnt.rpt" "adj_browLid_R_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle161.t" "adj_browLid_R_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle161.rp" "adj_browLid_R_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle161.rpt" "adj_browLid_R_003_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle161.pm" "adj_browLid_R_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_browLid_R_003_jnt_pointConstraint1.w0" "adj_browLid_R_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_noseWing_L_002_jnt_pointConstraint1.ctx" "adj_noseWing_L_002_jnt.tx"
		;
connectAttr "adj_noseWing_L_002_jnt_pointConstraint1.cty" "adj_noseWing_L_002_jnt.ty"
		;
connectAttr "adj_noseWing_L_002_jnt_pointConstraint1.ctz" "adj_noseWing_L_002_jnt.tz"
		;
connectAttr "adj_noseWing_L_002_jnt.pim" "adj_noseWing_L_002_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_noseWing_L_002_jnt.rp" "adj_noseWing_L_002_jnt_pointConstraint1.crp"
		;
connectAttr "adj_noseWing_L_002_jnt.rpt" "adj_noseWing_L_002_jnt_pointConstraint1.crt"
		;
connectAttr "follicle149.t" "adj_noseWing_L_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle149.rp" "adj_noseWing_L_002_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle149.rpt" "adj_noseWing_L_002_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle149.pm" "adj_noseWing_L_002_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_noseWing_L_002_jnt_pointConstraint1.w0" "adj_noseWing_L_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_zyg_L_001_jnt_pointConstraint1.ctx" "adj_zyg_L_001_jnt.tx";
connectAttr "adj_zyg_L_001_jnt_pointConstraint1.cty" "adj_zyg_L_001_jnt.ty";
connectAttr "adj_zyg_L_001_jnt_pointConstraint1.ctz" "adj_zyg_L_001_jnt.tz";
connectAttr "adj_zyg_L_001_jnt.pim" "adj_zyg_L_001_jnt_pointConstraint1.cpim";
connectAttr "adj_zyg_L_001_jnt.rp" "adj_zyg_L_001_jnt_pointConstraint1.crp";
connectAttr "adj_zyg_L_001_jnt.rpt" "adj_zyg_L_001_jnt_pointConstraint1.crt";
connectAttr "follicle134.t" "adj_zyg_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle134.rp" "adj_zyg_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle134.rpt" "adj_zyg_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle134.pm" "adj_zyg_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_zyg_L_001_jnt_pointConstraint1.w0" "adj_zyg_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_zyg_L_003_jnt_pointConstraint1.ctx" "adj_zyg_L_003_jnt.tx";
connectAttr "adj_zyg_L_003_jnt_pointConstraint1.cty" "adj_zyg_L_003_jnt.ty";
connectAttr "adj_zyg_L_003_jnt_pointConstraint1.ctz" "adj_zyg_L_003_jnt.tz";
connectAttr "adj_zyg_L_003_jnt.pim" "adj_zyg_L_003_jnt_pointConstraint1.cpim";
connectAttr "adj_zyg_L_003_jnt.rp" "adj_zyg_L_003_jnt_pointConstraint1.crp";
connectAttr "adj_zyg_L_003_jnt.rpt" "adj_zyg_L_003_jnt_pointConstraint1.crt";
connectAttr "follicle133.t" "adj_zyg_L_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle133.rp" "adj_zyg_L_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle133.rpt" "adj_zyg_L_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle133.pm" "adj_zyg_L_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_zyg_L_003_jnt_pointConstraint1.w0" "adj_zyg_L_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_cheek_L_001_jnt_pointConstraint1.ctx" "adj_cheek_L_001_jnt.tx";
connectAttr "adj_cheek_L_001_jnt_pointConstraint1.cty" "adj_cheek_L_001_jnt.ty";
connectAttr "adj_cheek_L_001_jnt_pointConstraint1.ctz" "adj_cheek_L_001_jnt.tz";
connectAttr "adj_cheek_L_001_jnt.pim" "adj_cheek_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_cheek_L_001_jnt.rp" "adj_cheek_L_001_jnt_pointConstraint1.crp";
connectAttr "adj_cheek_L_001_jnt.rpt" "adj_cheek_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle138.t" "adj_cheek_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle138.rp" "adj_cheek_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle138.rpt" "adj_cheek_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle138.pm" "adj_cheek_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_cheek_L_001_jnt_pointConstraint1.w0" "adj_cheek_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_cheek_L_003_jnt_pointConstraint1.ctx" "adj_cheek_L_003_jnt.tx";
connectAttr "adj_cheek_L_003_jnt_pointConstraint1.cty" "adj_cheek_L_003_jnt.ty";
connectAttr "adj_cheek_L_003_jnt_pointConstraint1.ctz" "adj_cheek_L_003_jnt.tz";
connectAttr "adj_cheek_L_003_jnt.pim" "adj_cheek_L_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_cheek_L_003_jnt.rp" "adj_cheek_L_003_jnt_pointConstraint1.crp";
connectAttr "adj_cheek_L_003_jnt.rpt" "adj_cheek_L_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle137.t" "adj_cheek_L_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle137.rp" "adj_cheek_L_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle137.rpt" "adj_cheek_L_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle137.pm" "adj_cheek_L_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_cheek_L_003_jnt_pointConstraint1.w0" "adj_cheek_L_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_noseWing_R_002_jnt_pointConstraint1.ctx" "adj_noseWing_R_002_jnt.tx"
		;
connectAttr "adj_noseWing_R_002_jnt_pointConstraint1.cty" "adj_noseWing_R_002_jnt.ty"
		;
connectAttr "adj_noseWing_R_002_jnt_pointConstraint1.ctz" "adj_noseWing_R_002_jnt.tz"
		;
connectAttr "adj_noseWing_R_002_jnt.pim" "adj_noseWing_R_002_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_noseWing_R_002_jnt.rp" "adj_noseWing_R_002_jnt_pointConstraint1.crp"
		;
connectAttr "adj_noseWing_R_002_jnt.rpt" "adj_noseWing_R_002_jnt_pointConstraint1.crt"
		;
connectAttr "follicle151.t" "adj_noseWing_R_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle151.rp" "adj_noseWing_R_002_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle151.rpt" "adj_noseWing_R_002_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle151.pm" "adj_noseWing_R_002_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_noseWing_R_002_jnt_pointConstraint1.w0" "adj_noseWing_R_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_zyg_R_001_jnt_pointConstraint1.ctx" "adj_zyg_R_001_jnt.tx";
connectAttr "adj_zyg_R_001_jnt_pointConstraint1.cty" "adj_zyg_R_001_jnt.ty";
connectAttr "adj_zyg_R_001_jnt_pointConstraint1.ctz" "adj_zyg_R_001_jnt.tz";
connectAttr "adj_zyg_R_001_jnt.pim" "adj_zyg_R_001_jnt_pointConstraint1.cpim";
connectAttr "adj_zyg_R_001_jnt.rp" "adj_zyg_R_001_jnt_pointConstraint1.crp";
connectAttr "adj_zyg_R_001_jnt.rpt" "adj_zyg_R_001_jnt_pointConstraint1.crt";
connectAttr "follicle135.t" "adj_zyg_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle135.rp" "adj_zyg_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle135.rpt" "adj_zyg_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle135.pm" "adj_zyg_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_zyg_R_001_jnt_pointConstraint1.w0" "adj_zyg_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_zyg_R_003_jnt_pointConstraint1.ctx" "adj_zyg_R_003_jnt.tx";
connectAttr "adj_zyg_R_003_jnt_pointConstraint1.cty" "adj_zyg_R_003_jnt.ty";
connectAttr "adj_zyg_R_003_jnt_pointConstraint1.ctz" "adj_zyg_R_003_jnt.tz";
connectAttr "adj_zyg_R_003_jnt.pim" "adj_zyg_R_003_jnt_pointConstraint1.cpim";
connectAttr "adj_zyg_R_003_jnt.rp" "adj_zyg_R_003_jnt_pointConstraint1.crp";
connectAttr "adj_zyg_R_003_jnt.rpt" "adj_zyg_R_003_jnt_pointConstraint1.crt";
connectAttr "follicle136.t" "adj_zyg_R_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle136.rp" "adj_zyg_R_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle136.rpt" "adj_zyg_R_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle136.pm" "adj_zyg_R_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_zyg_R_003_jnt_pointConstraint1.w0" "adj_zyg_R_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_cheek_R_001_jnt_pointConstraint1.ctx" "adj_cheek_R_001_jnt.tx";
connectAttr "adj_cheek_R_001_jnt_pointConstraint1.cty" "adj_cheek_R_001_jnt.ty";
connectAttr "adj_cheek_R_001_jnt_pointConstraint1.ctz" "adj_cheek_R_001_jnt.tz";
connectAttr "adj_cheek_R_001_jnt.pim" "adj_cheek_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_cheek_R_001_jnt.rp" "adj_cheek_R_001_jnt_pointConstraint1.crp";
connectAttr "adj_cheek_R_001_jnt.rpt" "adj_cheek_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle139.t" "adj_cheek_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle139.rp" "adj_cheek_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle139.rpt" "adj_cheek_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle139.pm" "adj_cheek_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_cheek_R_001_jnt_pointConstraint1.w0" "adj_cheek_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_cheek_R_003_jnt_pointConstraint1.ctx" "adj_cheek_R_003_jnt.tx";
connectAttr "adj_cheek_R_003_jnt_pointConstraint1.cty" "adj_cheek_R_003_jnt.ty";
connectAttr "adj_cheek_R_003_jnt_pointConstraint1.ctz" "adj_cheek_R_003_jnt.tz";
connectAttr "adj_cheek_R_003_jnt.pim" "adj_cheek_R_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_cheek_R_003_jnt.rp" "adj_cheek_R_003_jnt_pointConstraint1.crp";
connectAttr "adj_cheek_R_003_jnt.rpt" "adj_cheek_R_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle140.t" "adj_cheek_R_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle140.rp" "adj_cheek_R_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle140.rpt" "adj_cheek_R_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle140.pm" "adj_cheek_R_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_cheek_R_003_jnt_pointConstraint1.w0" "adj_cheek_R_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_noseBottom_C_001_jnt_pointConstraint1.ctx" "adj_noseBottom_C_001_jnt.tx"
		;
connectAttr "adj_noseBottom_C_001_jnt_pointConstraint1.cty" "adj_noseBottom_C_001_jnt.ty"
		;
connectAttr "adj_noseBottom_C_001_jnt_pointConstraint1.ctz" "adj_noseBottom_C_001_jnt.tz"
		;
connectAttr "adj_noseBottom_C_001_jnt.pim" "adj_noseBottom_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_noseBottom_C_001_jnt.rp" "adj_noseBottom_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_noseBottom_C_001_jnt.rpt" "adj_noseBottom_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle152.t" "adj_noseBottom_C_001_jnt_pointConstraint1.tg[0].tt"
		;
connectAttr "follicle152.rp" "adj_noseBottom_C_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle152.rpt" "adj_noseBottom_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle152.pm" "adj_noseBottom_C_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_noseBottom_C_001_jnt_pointConstraint1.w0" "adj_noseBottom_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_nosFlo_L_001_jnt_pointConstraint1.ctx" "adj_nosFlo_L_001_jnt.tx"
		;
connectAttr "adj_nosFlo_L_001_jnt_pointConstraint1.cty" "adj_nosFlo_L_001_jnt.ty"
		;
connectAttr "adj_nosFlo_L_001_jnt_pointConstraint1.ctz" "adj_nosFlo_L_001_jnt.tz"
		;
connectAttr "adj_nosFlo_L_001_jnt.pim" "adj_nosFlo_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_nosFlo_L_001_jnt.rp" "adj_nosFlo_L_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_nosFlo_L_001_jnt.rpt" "adj_nosFlo_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle141.t" "adj_nosFlo_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle141.rp" "adj_nosFlo_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle141.rpt" "adj_nosFlo_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle141.pm" "adj_nosFlo_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_nosFlo_L_001_jnt_pointConstraint1.w0" "adj_nosFlo_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_nosFlo_L_003_jnt_pointConstraint1.ctx" "adj_nosFlo_L_003_jnt.tx"
		;
connectAttr "adj_nosFlo_L_003_jnt_pointConstraint1.cty" "adj_nosFlo_L_003_jnt.ty"
		;
connectAttr "adj_nosFlo_L_003_jnt_pointConstraint1.ctz" "adj_nosFlo_L_003_jnt.tz"
		;
connectAttr "adj_nosFlo_L_003_jnt.pim" "adj_nosFlo_L_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_nosFlo_L_003_jnt.rp" "adj_nosFlo_L_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_nosFlo_L_003_jnt.rpt" "adj_nosFlo_L_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle142.t" "adj_nosFlo_L_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle142.rp" "adj_nosFlo_L_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle142.rpt" "adj_nosFlo_L_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle142.pm" "adj_nosFlo_L_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_nosFlo_L_003_jnt_pointConstraint1.w0" "adj_nosFlo_L_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_nosFlo_L_005_jnt_pointConstraint1.ctx" "adj_nosFlo_L_005_jnt.tx"
		;
connectAttr "adj_nosFlo_L_005_jnt_pointConstraint1.cty" "adj_nosFlo_L_005_jnt.ty"
		;
connectAttr "adj_nosFlo_L_005_jnt_pointConstraint1.ctz" "adj_nosFlo_L_005_jnt.tz"
		;
connectAttr "adj_nosFlo_L_005_jnt.pim" "adj_nosFlo_L_005_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_nosFlo_L_005_jnt.rp" "adj_nosFlo_L_005_jnt_pointConstraint1.crp"
		;
connectAttr "adj_nosFlo_L_005_jnt.rpt" "adj_nosFlo_L_005_jnt_pointConstraint1.crt"
		;
connectAttr "follicle143.t" "adj_nosFlo_L_005_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle143.rp" "adj_nosFlo_L_005_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle143.rpt" "adj_nosFlo_L_005_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle143.pm" "adj_nosFlo_L_005_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_nosFlo_L_005_jnt_pointConstraint1.w0" "adj_nosFlo_L_005_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_nosFlo_R_001_jnt_pointConstraint1.ctx" "adj_nosFlo_R_001_jnt.tx"
		;
connectAttr "adj_nosFlo_R_001_jnt_pointConstraint1.cty" "adj_nosFlo_R_001_jnt.ty"
		;
connectAttr "adj_nosFlo_R_001_jnt_pointConstraint1.ctz" "adj_nosFlo_R_001_jnt.tz"
		;
connectAttr "adj_nosFlo_R_001_jnt.pim" "adj_nosFlo_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_nosFlo_R_001_jnt.rp" "adj_nosFlo_R_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_nosFlo_R_001_jnt.rpt" "adj_nosFlo_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle147.t" "adj_nosFlo_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle147.rp" "adj_nosFlo_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle147.rpt" "adj_nosFlo_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle147.pm" "adj_nosFlo_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_nosFlo_R_001_jnt_pointConstraint1.w0" "adj_nosFlo_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_nosFlo_R_003_jnt_pointConstraint1.ctx" "adj_nosFlo_R_003_jnt.tx"
		;
connectAttr "adj_nosFlo_R_003_jnt_pointConstraint1.cty" "adj_nosFlo_R_003_jnt.ty"
		;
connectAttr "adj_nosFlo_R_003_jnt_pointConstraint1.ctz" "adj_nosFlo_R_003_jnt.tz"
		;
connectAttr "adj_nosFlo_R_003_jnt.pim" "adj_nosFlo_R_003_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_nosFlo_R_003_jnt.rp" "adj_nosFlo_R_003_jnt_pointConstraint1.crp"
		;
connectAttr "adj_nosFlo_R_003_jnt.rpt" "adj_nosFlo_R_003_jnt_pointConstraint1.crt"
		;
connectAttr "follicle146.t" "adj_nosFlo_R_003_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle146.rp" "adj_nosFlo_R_003_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle146.rpt" "adj_nosFlo_R_003_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle146.pm" "adj_nosFlo_R_003_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_nosFlo_R_003_jnt_pointConstraint1.w0" "adj_nosFlo_R_003_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_nosFlo_R_005_jnt_pointConstraint1.ctx" "adj_nosFlo_R_005_jnt.tx"
		;
connectAttr "adj_nosFlo_R_005_jnt_pointConstraint1.cty" "adj_nosFlo_R_005_jnt.ty"
		;
connectAttr "adj_nosFlo_R_005_jnt_pointConstraint1.ctz" "adj_nosFlo_R_005_jnt.tz"
		;
connectAttr "adj_nosFlo_R_005_jnt.pim" "adj_nosFlo_R_005_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_nosFlo_R_005_jnt.rp" "adj_nosFlo_R_005_jnt_pointConstraint1.crp"
		;
connectAttr "adj_nosFlo_R_005_jnt.rpt" "adj_nosFlo_R_005_jnt_pointConstraint1.crt"
		;
connectAttr "follicle145.t" "adj_nosFlo_R_005_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle145.rp" "adj_nosFlo_R_005_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle145.rpt" "adj_nosFlo_R_005_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle145.pm" "adj_nosFlo_R_005_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_nosFlo_R_005_jnt_pointConstraint1.w0" "adj_nosFlo_R_005_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_lipChin_C_001_jnt_pointConstraint1.ctx" "adj_lipChin_C_001_jnt.tx"
		;
connectAttr "adj_lipChin_C_001_jnt_pointConstraint1.cty" "adj_lipChin_C_001_jnt.ty"
		;
connectAttr "adj_lipChin_C_001_jnt_pointConstraint1.ctz" "adj_lipChin_C_001_jnt.tz"
		;
connectAttr "adj_lipChin_C_001_jnt.pim" "adj_lipChin_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_lipChin_C_001_jnt.rp" "adj_lipChin_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_lipChin_C_001_jnt.rpt" "adj_lipChin_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle144.t" "adj_lipChin_C_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle144.rp" "adj_lipChin_C_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle144.rpt" "adj_lipChin_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle144.pm" "adj_lipChin_C_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_lipChin_C_001_jnt_pointConstraint1.w0" "adj_lipChin_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_mouth_L_001_jnt_pointConstraint1.ctx" "adj_mouth_L_001_jnt.tx";
connectAttr "adj_mouth_L_001_jnt_pointConstraint1.cty" "adj_mouth_L_001_jnt.ty";
connectAttr "adj_mouth_L_001_jnt_pointConstraint1.ctz" "adj_mouth_L_001_jnt.tz";
connectAttr "adj_mouth_L_001_jnt.pim" "adj_mouth_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_mouth_L_001_jnt.rp" "adj_mouth_L_001_jnt_pointConstraint1.crp";
connectAttr "adj_mouth_L_001_jnt.rpt" "adj_mouth_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle154.t" "adj_mouth_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle154.rp" "adj_mouth_L_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle154.rpt" "adj_mouth_L_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle154.pm" "adj_mouth_L_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_mouth_L_001_jnt_pointConstraint1.w0" "adj_mouth_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_mouth_R_001_jnt_pointConstraint1.ctx" "adj_mouth_R_001_jnt.tx";
connectAttr "adj_mouth_R_001_jnt_pointConstraint1.cty" "adj_mouth_R_001_jnt.ty";
connectAttr "adj_mouth_R_001_jnt_pointConstraint1.ctz" "adj_mouth_R_001_jnt.tz";
connectAttr "adj_mouth_R_001_jnt.pim" "adj_mouth_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_mouth_R_001_jnt.rp" "adj_mouth_R_001_jnt_pointConstraint1.crp";
connectAttr "adj_mouth_R_001_jnt.rpt" "adj_mouth_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle156.t" "adj_mouth_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle156.rp" "adj_mouth_R_001_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle156.rpt" "adj_mouth_R_001_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle156.pm" "adj_mouth_R_001_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_mouth_R_001_jnt_pointConstraint1.w0" "adj_mouth_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_upLipFrame_C_001_jnt_pointConstraint1.ctx" "adj_upLipFrame_C_001_jnt.tx"
		;
connectAttr "adj_upLipFrame_C_001_jnt_pointConstraint1.cty" "adj_upLipFrame_C_001_jnt.ty"
		;
connectAttr "adj_upLipFrame_C_001_jnt_pointConstraint1.ctz" "adj_upLipFrame_C_001_jnt.tz"
		;
connectAttr "adj_upLipFrame_C_001_jnt.pim" "adj_upLipFrame_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_upLipFrame_C_001_jnt.rp" "adj_upLipFrame_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_upLipFrame_C_001_jnt.rpt" "adj_upLipFrame_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle153.t" "adj_upLipFrame_C_001_jnt_pointConstraint1.tg[0].tt"
		;
connectAttr "follicle153.rp" "adj_upLipFrame_C_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle153.rpt" "adj_upLipFrame_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle153.pm" "adj_upLipFrame_C_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_upLipFrame_C_001_jnt_pointConstraint1.w0" "adj_upLipFrame_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_lowLipFrame_C_001_jnt_pointConstraint1.ctx" "adj_lowLipFrame_C_001_jnt.tx"
		;
connectAttr "adj_lowLipFrame_C_001_jnt_pointConstraint1.cty" "adj_lowLipFrame_C_001_jnt.ty"
		;
connectAttr "adj_lowLipFrame_C_001_jnt_pointConstraint1.ctz" "adj_lowLipFrame_C_001_jnt.tz"
		;
connectAttr "adj_lowLipFrame_C_001_jnt.pim" "adj_lowLipFrame_C_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_lowLipFrame_C_001_jnt.rp" "adj_lowLipFrame_C_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_lowLipFrame_C_001_jnt.rpt" "adj_lowLipFrame_C_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle155.t" "adj_lowLipFrame_C_001_jnt_pointConstraint1.tg[0].tt"
		;
connectAttr "follicle155.rp" "adj_lowLipFrame_C_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle155.rpt" "adj_lowLipFrame_C_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle155.pm" "adj_lowLipFrame_C_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_lowLipFrame_C_001_jnt_pointConstraint1.w0" "adj_lowLipFrame_C_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_chin_L_002_jnt_pointConstraint1.ctx" "adj_chin_L_002_jnt.tx";
connectAttr "adj_chin_L_002_jnt_pointConstraint1.cty" "adj_chin_L_002_jnt.ty";
connectAttr "adj_chin_L_002_jnt_pointConstraint1.ctz" "adj_chin_L_002_jnt.tz";
connectAttr "adj_chin_L_002_jnt.pim" "adj_chin_L_002_jnt_pointConstraint1.cpim";
connectAttr "adj_chin_L_002_jnt.rp" "adj_chin_L_002_jnt_pointConstraint1.crp";
connectAttr "adj_chin_L_002_jnt.rpt" "adj_chin_L_002_jnt_pointConstraint1.crt";
connectAttr "follicle163.t" "adj_chin_L_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle163.rp" "adj_chin_L_002_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle163.rpt" "adj_chin_L_002_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle163.pm" "adj_chin_L_002_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_chin_L_002_jnt_pointConstraint1.w0" "adj_chin_L_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_chin_R_002_jnt_pointConstraint1.ctx" "adj_chin_R_002_jnt.tx";
connectAttr "adj_chin_R_002_jnt_pointConstraint1.cty" "adj_chin_R_002_jnt.ty";
connectAttr "adj_chin_R_002_jnt_pointConstraint1.ctz" "adj_chin_R_002_jnt.tz";
connectAttr "adj_chin_R_002_jnt.pim" "adj_chin_R_002_jnt_pointConstraint1.cpim";
connectAttr "adj_chin_R_002_jnt.rp" "adj_chin_R_002_jnt_pointConstraint1.crp";
connectAttr "adj_chin_R_002_jnt.rpt" "adj_chin_R_002_jnt_pointConstraint1.crt";
connectAttr "follicle165.t" "adj_chin_R_002_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle165.rp" "adj_chin_R_002_jnt_pointConstraint1.tg[0].trp";
connectAttr "follicle165.rpt" "adj_chin_R_002_jnt_pointConstraint1.tg[0].trt";
connectAttr "follicle165.pm" "adj_chin_R_002_jnt_pointConstraint1.tg[0].tpm";
connectAttr "adj_chin_R_002_jnt_pointConstraint1.w0" "adj_chin_R_002_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_chinNeck_L_001_jnt_pointConstraint1.ctx" "adj_chinNeck_L_001_jnt.tx"
		;
connectAttr "adj_chinNeck_L_001_jnt_pointConstraint1.cty" "adj_chinNeck_L_001_jnt.ty"
		;
connectAttr "adj_chinNeck_L_001_jnt_pointConstraint1.ctz" "adj_chinNeck_L_001_jnt.tz"
		;
connectAttr "adj_chinNeck_L_001_jnt.pim" "adj_chinNeck_L_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_chinNeck_L_001_jnt.rp" "adj_chinNeck_L_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_chinNeck_L_001_jnt.rpt" "adj_chinNeck_L_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle162.t" "adj_chinNeck_L_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle162.rp" "adj_chinNeck_L_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle162.rpt" "adj_chinNeck_L_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle162.pm" "adj_chinNeck_L_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_chinNeck_L_001_jnt_pointConstraint1.w0" "adj_chinNeck_L_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "adj_chinNeck_R_001_jnt_pointConstraint1.ctx" "adj_chinNeck_R_001_jnt.tx"
		;
connectAttr "adj_chinNeck_R_001_jnt_pointConstraint1.cty" "adj_chinNeck_R_001_jnt.ty"
		;
connectAttr "adj_chinNeck_R_001_jnt_pointConstraint1.ctz" "adj_chinNeck_R_001_jnt.tz"
		;
connectAttr "adj_chinNeck_R_001_jnt.pim" "adj_chinNeck_R_001_jnt_pointConstraint1.cpim"
		;
connectAttr "adj_chinNeck_R_001_jnt.rp" "adj_chinNeck_R_001_jnt_pointConstraint1.crp"
		;
connectAttr "adj_chinNeck_R_001_jnt.rpt" "adj_chinNeck_R_001_jnt_pointConstraint1.crt"
		;
connectAttr "follicle166.t" "adj_chinNeck_R_001_jnt_pointConstraint1.tg[0].tt";
connectAttr "follicle166.rp" "adj_chinNeck_R_001_jnt_pointConstraint1.tg[0].trp"
		;
connectAttr "follicle166.rpt" "adj_chinNeck_R_001_jnt_pointConstraint1.tg[0].trt"
		;
connectAttr "follicle166.pm" "adj_chinNeck_R_001_jnt_pointConstraint1.tg[0].tpm"
		;
connectAttr "adj_chinNeck_R_001_jnt_pointConstraint1.w0" "adj_chinNeck_R_001_jnt_pointConstraint1.tg[0].tw"
		;
connectAttr "follicleShape7.ot" "follicle7.t";
connectAttr "follicleShape7.or" "follicle7.r";
connectAttr "brow_bs_meshShape.o" "follicleShape7.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape7.iwm";
connectAttr "follicleShape6.ot" "follicle6.t";
connectAttr "follicleShape6.or" "follicle6.r";
connectAttr "brow_bs_meshShape.o" "follicleShape6.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape6.iwm";
connectAttr "follicleShape5.ot" "follicle5.t";
connectAttr "follicleShape5.or" "follicle5.r";
connectAttr "brow_bs_meshShape.o" "follicleShape5.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape5.iwm";
connectAttr "follicleShape4.ot" "follicle4.t";
connectAttr "follicleShape4.or" "follicle4.r";
connectAttr "brow_bs_meshShape.o" "follicleShape4.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape4.iwm";
connectAttr "follicleShape3.ot" "follicle3.t";
connectAttr "follicleShape3.or" "follicle3.r";
connectAttr "brow_bs_meshShape.o" "follicleShape3.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape3.iwm";
connectAttr "follicleShape2.ot" "follicle2.t";
connectAttr "follicleShape2.or" "follicle2.r";
connectAttr "brow_bs_meshShape.o" "follicleShape2.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape2.iwm";
connectAttr "follicleShape1.ot" "follicle1.t";
connectAttr "follicleShape1.or" "follicle1.r";
connectAttr "brow_bs_meshShape.o" "follicleShape1.inm";
connectAttr "brow_bs_meshShape.wm" "follicleShape1.iwm";
connectAttr "follicleShape8.ot" "follicle8.t";
connectAttr "follicleShape8.or" "follicle8.r";
connectAttr "browLid_bs_meshShape.o" "follicleShape8.inm";
connectAttr "browLid_bs_meshShape.wm" "follicleShape8.iwm";
connectAttr "follicleShape9.ot" "follicle9.t";
connectAttr "follicleShape9.or" "follicle9.r";
connectAttr "browLid_bs_meshShape.o" "follicleShape9.inm";
connectAttr "browLid_bs_meshShape.wm" "follicleShape9.iwm";
connectAttr "follicleShape10.ot" "follicle10.t";
connectAttr "follicleShape10.or" "follicle10.r";
connectAttr "browLid_bs_meshShape.o" "follicleShape10.inm";
connectAttr "browLid_bs_meshShape.wm" "follicleShape10.iwm";
connectAttr "follicleShape11.ot" "follicle11.t";
connectAttr "follicleShape11.or" "follicle11.r";
connectAttr "browLid_bs_meshShape.o" "follicleShape11.inm";
connectAttr "browLid_bs_meshShape.wm" "follicleShape11.iwm";
connectAttr "follicleShape12.ot" "follicle12.t";
connectAttr "follicleShape12.or" "follicle12.r";
connectAttr "browLid_bs_meshShape.o" "follicleShape12.inm";
connectAttr "browLid_bs_meshShape.wm" "follicleShape12.iwm";
connectAttr "follicleShape13.ot" "follicle13.t";
connectAttr "follicleShape13.or" "follicle13.r";
connectAttr "browLid_bs_meshShape.o" "follicleShape13.inm";
connectAttr "browLid_bs_meshShape.wm" "follicleShape13.iwm";
connectAttr "follicleShape14.ot" "follicle14.t";
connectAttr "follicleShape14.or" "follicle14.r";
connectAttr "forehead_bs_meshShape.o" "follicleShape14.inm";
connectAttr "forehead_bs_meshShape.wm" "follicleShape14.iwm";
connectAttr "follicleShape15.ot" "follicle15.t";
connectAttr "follicleShape15.or" "follicle15.r";
connectAttr "forehead_bs_meshShape.o" "follicleShape15.inm";
connectAttr "forehead_bs_meshShape.wm" "follicleShape15.iwm";
connectAttr "follicleShape16.ot" "follicle16.t";
connectAttr "follicleShape16.or" "follicle16.r";
connectAttr "forehead_bs_meshShape.o" "follicleShape16.inm";
connectAttr "forehead_bs_meshShape.wm" "follicleShape16.iwm";
connectAttr "follicleShape17.ot" "follicle17.t";
connectAttr "follicleShape17.or" "follicle17.r";
connectAttr "forehead_bs_meshShape.o" "follicleShape17.inm";
connectAttr "forehead_bs_meshShape.wm" "follicleShape17.iwm";
connectAttr "follicleShape18.ot" "follicle18.t";
connectAttr "follicleShape18.or" "follicle18.r";
connectAttr "forehead_bs_meshShape.o" "follicleShape18.inm";
connectAttr "forehead_bs_meshShape.wm" "follicleShape18.iwm";
connectAttr "follicleShape19.ot" "follicle19.t";
connectAttr "follicleShape19.or" "follicle19.r";
connectAttr "forehead_bs_meshShape.o" "follicleShape19.inm";
connectAttr "forehead_bs_meshShape.wm" "follicleShape19.iwm";
connectAttr "follicleShape20.ot" "follicle20.t";
connectAttr "follicleShape20.or" "follicle20.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape20.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape20.iwm";
connectAttr "follicleShape21.ot" "follicle21.t";
connectAttr "follicleShape21.or" "follicle21.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape21.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape21.iwm";
connectAttr "follicleShape22.ot" "follicle22.t";
connectAttr "follicleShape22.or" "follicle22.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape22.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape22.iwm";
connectAttr "follicleShape23.ot" "follicle23.t";
connectAttr "follicleShape23.or" "follicle23.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape23.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape23.iwm";
connectAttr "follicleShape24.ot" "follicle24.t";
connectAttr "follicleShape24.or" "follicle24.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape24.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape24.iwm";
connectAttr "follicleShape25.ot" "follicle25.t";
connectAttr "follicleShape25.or" "follicle25.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape25.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape25.iwm";
connectAttr "follicleShape26.ot" "follicle26.t";
connectAttr "follicleShape26.or" "follicle26.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape26.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape26.iwm";
connectAttr "follicleShape27.ot" "follicle27.t";
connectAttr "follicleShape27.or" "follicle27.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape27.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape27.iwm";
connectAttr "follicleShape28.ot" "follicle28.t";
connectAttr "follicleShape28.or" "follicle28.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape28.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape28.iwm";
connectAttr "follicleShape29.ot" "follicle29.t";
connectAttr "follicleShape29.or" "follicle29.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape29.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape29.iwm";
connectAttr "follicleShape30.ot" "follicle30.t";
connectAttr "follicleShape30.or" "follicle30.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape30.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape30.iwm";
connectAttr "follicleShape31.ot" "follicle31.t";
connectAttr "follicleShape31.or" "follicle31.r";
connectAttr "eyeFrame_bs_meshShape.o" "follicleShape31.inm";
connectAttr "eyeFrame_bs_meshShape.wm" "follicleShape31.iwm";
connectAttr "follicleShape32.ot" "follicle32.t";
connectAttr "follicleShape32.or" "follicle32.r";
connectAttr "lowlid_bs_meshShape.o" "follicleShape32.inm";
connectAttr "lowlid_bs_meshShape.wm" "follicleShape32.iwm";
connectAttr "follicleShape33.ot" "follicle33.t";
connectAttr "follicleShape33.or" "follicle33.r";
connectAttr "lowlid_bs_meshShape.o" "follicleShape33.inm";
connectAttr "lowlid_bs_meshShape.wm" "follicleShape33.iwm";
connectAttr "follicleShape34.ot" "follicle34.t";
connectAttr "follicleShape34.or" "follicle34.r";
connectAttr "lowlid_bs_meshShape.o" "follicleShape34.inm";
connectAttr "lowlid_bs_meshShape.wm" "follicleShape34.iwm";
connectAttr "follicleShape35.ot" "follicle35.t";
connectAttr "follicleShape35.or" "follicle35.r";
connectAttr "lowlid_bs_meshShape.o" "follicleShape35.inm";
connectAttr "lowlid_bs_meshShape.wm" "follicleShape35.iwm";
connectAttr "follicleShape36.ot" "follicle36.t";
connectAttr "follicleShape36.or" "follicle36.r";
connectAttr "lowlid_bs_meshShape.o" "follicleShape36.inm";
connectAttr "lowlid_bs_meshShape.wm" "follicleShape36.iwm";
connectAttr "follicleShape37.ot" "follicle37.t";
connectAttr "follicleShape37.or" "follicle37.r";
connectAttr "lowlid_bs_meshShape.o" "follicleShape37.inm";
connectAttr "lowlid_bs_meshShape.wm" "follicleShape37.iwm";
connectAttr "follicleShape38.ot" "follicle38.t";
connectAttr "follicleShape38.or" "follicle38.r";
connectAttr "nose_bs_meshShape.o" "follicleShape38.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape38.iwm";
connectAttr "follicleShape39.ot" "follicle39.t";
connectAttr "follicleShape39.or" "follicle39.r";
connectAttr "nose_bs_meshShape.o" "follicleShape39.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape39.iwm";
connectAttr "follicleShape40.ot" "follicle40.t";
connectAttr "follicleShape40.or" "follicle40.r";
connectAttr "nose_bs_meshShape.o" "follicleShape40.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape40.iwm";
connectAttr "follicleShape41.ot" "follicle41.t";
connectAttr "follicleShape41.or" "follicle41.r";
connectAttr "nose_bs_meshShape.o" "follicleShape41.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape41.iwm";
connectAttr "follicleShape42.ot" "follicle42.t";
connectAttr "follicleShape42.or" "follicle42.r";
connectAttr "nose_bs_meshShape.o" "follicleShape42.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape42.iwm";
connectAttr "follicleShape43.ot" "follicle43.t";
connectAttr "follicleShape43.or" "follicle43.r";
connectAttr "nose_bs_meshShape.o" "follicleShape43.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape43.iwm";
connectAttr "follicleShape44.ot" "follicle44.t";
connectAttr "follicleShape44.or" "follicle44.r";
connectAttr "nose_bs_meshShape.o" "follicleShape44.inm";
connectAttr "nose_bs_meshShape.wm" "follicleShape44.iwm";
connectAttr "follicleShape45.ot" "follicle45.t";
connectAttr "follicleShape45.or" "follicle45.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape45.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape45.iwm";
connectAttr "follicleShape46.ot" "follicle46.t";
connectAttr "follicleShape46.or" "follicle46.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape46.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape46.iwm";
connectAttr "follicleShape47.ot" "follicle47.t";
connectAttr "follicleShape47.or" "follicle47.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape47.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape47.iwm";
connectAttr "follicleShape48.ot" "follicle48.t";
connectAttr "follicleShape48.or" "follicle48.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape48.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape48.iwm";
connectAttr "follicleShape49.ot" "follicle49.t";
connectAttr "follicleShape49.or" "follicle49.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape49.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape49.iwm";
connectAttr "follicleShape50.ot" "follicle50.t";
connectAttr "follicleShape50.or" "follicle50.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape50.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape50.iwm";
connectAttr "follicleShape51.ot" "follicle51.t";
connectAttr "follicleShape51.or" "follicle51.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape51.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape51.iwm";
connectAttr "follicleShape52.ot" "follicle52.t";
connectAttr "follicleShape52.or" "follicle52.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape52.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape52.iwm";
connectAttr "follicleShape53.ot" "follicle53.t";
connectAttr "follicleShape53.or" "follicle53.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape53.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape53.iwm";
connectAttr "follicleShape54.ot" "follicle54.t";
connectAttr "follicleShape54.or" "follicle54.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape54.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape54.iwm";
connectAttr "follicleShape55.ot" "follicle55.t";
connectAttr "follicleShape55.or" "follicle55.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape55.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape55.iwm";
connectAttr "follicleShape56.ot" "follicle56.t";
connectAttr "follicleShape56.or" "follicle56.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape56.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape56.iwm";
connectAttr "follicleShape57.ot" "follicle57.t";
connectAttr "follicleShape57.or" "follicle57.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape57.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape57.iwm";
connectAttr "follicleShape58.ot" "follicle58.t";
connectAttr "follicleShape58.or" "follicle58.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape58.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape58.iwm";
connectAttr "follicleShape59.ot" "follicle59.t";
connectAttr "follicleShape59.or" "follicle59.r";
connectAttr "nosFlo_bs_meshShape.o" "follicleShape59.inm";
connectAttr "nosFlo_bs_meshShape.wm" "follicleShape59.iwm";
connectAttr "follicleShape60.ot" "follicle60.t";
connectAttr "follicleShape60.or" "follicle60.r";
connectAttr "zyg_bs_meshShape.o" "follicleShape60.inm";
connectAttr "zyg_bs_meshShape.wm" "follicleShape60.iwm";
connectAttr "follicleShape61.ot" "follicle61.t";
connectAttr "follicleShape61.or" "follicle61.r";
connectAttr "zyg_bs_meshShape.o" "follicleShape61.inm";
connectAttr "zyg_bs_meshShape.wm" "follicleShape61.iwm";
connectAttr "follicleShape62.ot" "follicle62.t";
connectAttr "follicleShape62.or" "follicle62.r";
connectAttr "zyg_bs_meshShape.o" "follicleShape62.inm";
connectAttr "zyg_bs_meshShape.wm" "follicleShape62.iwm";
connectAttr "follicleShape63.ot" "follicle63.t";
connectAttr "follicleShape63.or" "follicle63.r";
connectAttr "zyg_bs_meshShape.o" "follicleShape63.inm";
connectAttr "zyg_bs_meshShape.wm" "follicleShape63.iwm";
connectAttr "follicleShape64.ot" "follicle64.t";
connectAttr "follicleShape64.or" "follicle64.r";
connectAttr "zyg_bs_meshShape.o" "follicleShape64.inm";
connectAttr "zyg_bs_meshShape.wm" "follicleShape64.iwm";
connectAttr "follicleShape65.ot" "follicle65.t";
connectAttr "follicleShape65.or" "follicle65.r";
connectAttr "zyg_bs_meshShape.o" "follicleShape65.inm";
connectAttr "zyg_bs_meshShape.wm" "follicleShape65.iwm";
connectAttr "follicleShape66.ot" "follicle66.t";
connectAttr "follicleShape66.or" "follicle66.r";
connectAttr "cheek_bs_meshShape.o" "follicleShape66.inm";
connectAttr "cheek_bs_meshShape.wm" "follicleShape66.iwm";
connectAttr "follicleShape67.ot" "follicle67.t";
connectAttr "follicleShape67.or" "follicle67.r";
connectAttr "cheek_bs_meshShape.o" "follicleShape67.inm";
connectAttr "cheek_bs_meshShape.wm" "follicleShape67.iwm";
connectAttr "follicleShape68.ot" "follicle68.t";
connectAttr "follicleShape68.or" "follicle68.r";
connectAttr "cheek_bs_meshShape.o" "follicleShape68.inm";
connectAttr "cheek_bs_meshShape.wm" "follicleShape68.iwm";
connectAttr "follicleShape69.ot" "follicle69.t";
connectAttr "follicleShape69.or" "follicle69.r";
connectAttr "cheek_bs_meshShape.o" "follicleShape69.inm";
connectAttr "cheek_bs_meshShape.wm" "follicleShape69.iwm";
connectAttr "follicleShape70.ot" "follicle70.t";
connectAttr "follicleShape70.or" "follicle70.r";
connectAttr "cheek_bs_meshShape.o" "follicleShape70.inm";
connectAttr "cheek_bs_meshShape.wm" "follicleShape70.iwm";
connectAttr "follicleShape71.ot" "follicle71.t";
connectAttr "follicleShape71.or" "follicle71.r";
connectAttr "cheek_bs_meshShape.o" "follicleShape71.inm";
connectAttr "cheek_bs_meshShape.wm" "follicleShape71.iwm";
connectAttr "follicleShape72.ot" "follicle72.t";
connectAttr "follicleShape72.or" "follicle72.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape72.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape72.iwm";
connectAttr "follicleShape73.ot" "follicle73.t";
connectAttr "follicleShape73.or" "follicle73.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape73.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape73.iwm";
connectAttr "follicleShape74.ot" "follicle74.t";
connectAttr "follicleShape74.or" "follicle74.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape74.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape74.iwm";
connectAttr "follicleShape75.ot" "follicle75.t";
connectAttr "follicleShape75.or" "follicle75.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape75.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape75.iwm";
connectAttr "follicleShape76.ot" "follicle76.t";
connectAttr "follicleShape76.or" "follicle76.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape76.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape76.iwm";
connectAttr "follicleShape77.ot" "follicle77.t";
connectAttr "follicleShape77.or" "follicle77.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape77.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape77.iwm";
connectAttr "follicleShape78.ot" "follicle78.t";
connectAttr "follicleShape78.or" "follicle78.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape78.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape78.iwm";
connectAttr "follicleShape79.ot" "follicle79.t";
connectAttr "follicleShape79.or" "follicle79.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape79.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape79.iwm";
connectAttr "follicleShape80.ot" "follicle80.t";
connectAttr "follicleShape80.or" "follicle80.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape80.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape80.iwm";
connectAttr "follicleShape81.ot" "follicle81.t";
connectAttr "follicleShape81.or" "follicle81.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape81.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape81.iwm";
connectAttr "follicleShape82.ot" "follicle82.t";
connectAttr "follicleShape82.or" "follicle82.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape82.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape82.iwm";
connectAttr "follicleShape83.ot" "follicle83.t";
connectAttr "follicleShape83.or" "follicle83.r";
connectAttr "lipFrame_bs_meshShape.o" "follicleShape83.inm";
connectAttr "lipFrame_bs_meshShape.wm" "follicleShape83.iwm";
connectAttr "follicleShape84.ot" "follicle84.t";
connectAttr "follicleShape84.or" "follicle84.r";
connectAttr "chin_bs_meshShape.o" "follicleShape84.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape84.iwm";
connectAttr "follicleShape85.ot" "follicle85.t";
connectAttr "follicleShape85.or" "follicle85.r";
connectAttr "chin_bs_meshShape.o" "follicleShape85.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape85.iwm";
connectAttr "follicleShape86.ot" "follicle86.t";
connectAttr "follicleShape86.or" "follicle86.r";
connectAttr "chin_bs_meshShape.o" "follicleShape86.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape86.iwm";
connectAttr "follicleShape87.ot" "follicle87.t";
connectAttr "follicleShape87.or" "follicle87.r";
connectAttr "chin_bs_meshShape.o" "follicleShape87.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape87.iwm";
connectAttr "follicleShape88.ot" "follicle88.t";
connectAttr "follicleShape88.or" "follicle88.r";
connectAttr "chin_bs_meshShape.o" "follicleShape88.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape88.iwm";
connectAttr "follicleShape89.ot" "follicle89.t";
connectAttr "follicleShape89.or" "follicle89.r";
connectAttr "chin_bs_meshShape.o" "follicleShape89.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape89.iwm";
connectAttr "follicleShape90.ot" "follicle90.t";
connectAttr "follicleShape90.or" "follicle90.r";
connectAttr "chin_bs_meshShape.o" "follicleShape90.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape90.iwm";
connectAttr "follicleShape91.ot" "follicle91.t";
connectAttr "follicleShape91.or" "follicle91.r";
connectAttr "chin_bs_meshShape.o" "follicleShape91.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape91.iwm";
connectAttr "follicleShape92.ot" "follicle92.t";
connectAttr "follicleShape92.or" "follicle92.r";
connectAttr "chin_bs_meshShape.o" "follicleShape92.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape92.iwm";
connectAttr "follicleShape93.ot" "follicle93.t";
connectAttr "follicleShape93.or" "follicle93.r";
connectAttr "chin_bs_meshShape.o" "follicleShape93.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape93.iwm";
connectAttr "follicleShape94.ot" "follicle94.t";
connectAttr "follicleShape94.or" "follicle94.r";
connectAttr "chin_bs_meshShape.o" "follicleShape94.inm";
connectAttr "chin_bs_meshShape.wm" "follicleShape94.iwm";
connectAttr "follicleShape95.ot" "follicle95.t";
connectAttr "follicleShape95.or" "follicle95.r";
connectAttr "throat_bs_meshShape.o" "follicleShape95.inm";
connectAttr "throat_bs_meshShape.wm" "follicleShape95.iwm";
connectAttr "follicleShape96.ot" "follicle96.t";
connectAttr "follicleShape96.or" "follicle96.r";
connectAttr "throat_bs_meshShape.o" "follicleShape96.inm";
connectAttr "throat_bs_meshShape.wm" "follicleShape96.iwm";
connectAttr "follicleShape97.ot" "follicle97.t";
connectAttr "follicleShape97.or" "follicle97.r";
connectAttr "throat_bs_meshShape.o" "follicleShape97.inm";
connectAttr "throat_bs_meshShape.wm" "follicleShape97.iwm";
connectAttr "follicleShape98.ot" "follicle98.t";
connectAttr "follicleShape98.or" "follicle98.r";
connectAttr "throat_bs_meshShape.o" "follicleShape98.inm";
connectAttr "throat_bs_meshShape.wm" "follicleShape98.iwm";
connectAttr "follicleShape99.ot" "follicle99.t";
connectAttr "follicleShape99.or" "follicle99.r";
connectAttr "throat_bs_meshShape.o" "follicleShape99.inm";
connectAttr "throat_bs_meshShape.wm" "follicleShape99.iwm";
connectAttr "follicleShape100.ot" "follicle100.t";
connectAttr "follicleShape100.or" "follicle100.r";
connectAttr "chinThroat_bs_meshShape.o" "follicleShape100.inm";
connectAttr "chinThroat_bs_meshShape.wm" "follicleShape100.iwm";
connectAttr "follicleShape101.ot" "follicle101.t";
connectAttr "follicleShape101.or" "follicle101.r";
connectAttr "chinThroat_bs_meshShape.o" "follicleShape101.inm";
connectAttr "chinThroat_bs_meshShape.wm" "follicleShape101.iwm";
connectAttr "follicleShape102.ot" "follicle102.t";
connectAttr "follicleShape102.or" "follicle102.r";
connectAttr "chinThroat_bs_meshShape.o" "follicleShape102.inm";
connectAttr "chinThroat_bs_meshShape.wm" "follicleShape102.iwm";
connectAttr "follicleShape103.ot" "follicle103.t";
connectAttr "follicleShape103.or" "follicle103.r";
connectAttr "chinThroat_bs_meshShape.o" "follicleShape103.inm";
connectAttr "chinThroat_bs_meshShape.wm" "follicleShape103.iwm";
connectAttr "follicleShape104.ot" "follicle104.t";
connectAttr "follicleShape104.or" "follicle104.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape104.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape104.iwm";
connectAttr "follicleShape105.ot" "follicle105.t";
connectAttr "follicleShape105.or" "follicle105.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape105.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape105.iwm";
connectAttr "follicleShape106.ot" "follicle106.t";
connectAttr "follicleShape106.or" "follicle106.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape106.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape106.iwm";
connectAttr "follicleShape107.ot" "follicle107.t";
connectAttr "follicleShape107.or" "follicle107.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape107.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape107.iwm";
connectAttr "follicleShape108.ot" "follicle108.t";
connectAttr "follicleShape108.or" "follicle108.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape108.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape108.iwm";
connectAttr "follicleShape109.ot" "follicle109.t";
connectAttr "follicleShape109.or" "follicle109.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape109.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape109.iwm";
connectAttr "follicleShape110.ot" "follicle110.t";
connectAttr "follicleShape110.or" "follicle110.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape110.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape110.iwm";
connectAttr "follicleShape111.ot" "follicle111.t";
connectAttr "follicleShape111.or" "follicle111.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape111.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape111.iwm";
connectAttr "follicleShape112.ot" "follicle112.t";
connectAttr "follicleShape112.or" "follicle112.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape112.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape112.iwm";
connectAttr "follicleShape113.ot" "follicle113.t";
connectAttr "follicleShape113.or" "follicle113.r";
connectAttr "clavicleNeck_bs_meshShape.o" "follicleShape113.inm";
connectAttr "clavicleNeck_bs_meshShape.wm" "follicleShape113.iwm";
connectAttr "follicleShape114.ot" "follicle114.t";
connectAttr "follicleShape114.or" "follicle114.r";
connectAttr "fol_base_meshShape.o" "follicleShape114.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape114.iwm";
connectAttr "follicleShape115.ot" "follicle115.t";
connectAttr "follicleShape115.or" "follicle115.r";
connectAttr "fol_base_meshShape.o" "follicleShape115.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape115.iwm";
connectAttr "follicleShape116.ot" "follicle116.t";
connectAttr "follicleShape116.or" "follicle116.r";
connectAttr "fol_base_meshShape.o" "follicleShape116.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape116.iwm";
connectAttr "follicleShape117.ot" "follicle117.t";
connectAttr "follicleShape117.or" "follicle117.r";
connectAttr "fol_base_meshShape.o" "follicleShape117.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape117.iwm";
connectAttr "follicleShape118.ot" "follicle118.t";
connectAttr "follicleShape118.or" "follicle118.r";
connectAttr "fol_base_meshShape.o" "follicleShape118.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape118.iwm";
connectAttr "follicleShape119.ot" "follicle119.t";
connectAttr "follicleShape119.or" "follicle119.r";
connectAttr "fol_base_meshShape.o" "follicleShape119.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape119.iwm";
connectAttr "follicleShape120.ot" "follicle120.t";
connectAttr "follicleShape120.or" "follicle120.r";
connectAttr "fol_base_meshShape.o" "follicleShape120.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape120.iwm";
connectAttr "follicleShape121.ot" "follicle121.t";
connectAttr "follicleShape121.or" "follicle121.r";
connectAttr "fol_base_meshShape.o" "follicleShape121.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape121.iwm";
connectAttr "follicleShape122.ot" "follicle122.t";
connectAttr "follicleShape122.or" "follicle122.r";
connectAttr "fol_base_meshShape.o" "follicleShape122.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape122.iwm";
connectAttr "follicleShape123.ot" "follicle123.t";
connectAttr "follicleShape123.or" "follicle123.r";
connectAttr "fol_base_meshShape.o" "follicleShape123.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape123.iwm";
connectAttr "follicleShape124.ot" "follicle124.t";
connectAttr "follicleShape124.or" "follicle124.r";
connectAttr "fol_base_meshShape.o" "follicleShape124.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape124.iwm";
connectAttr "follicleShape125.ot" "follicle125.t";
connectAttr "follicleShape125.or" "follicle125.r";
connectAttr "fol_base_meshShape.o" "follicleShape125.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape125.iwm";
connectAttr "follicleShape126.ot" "follicle126.t";
connectAttr "follicleShape126.or" "follicle126.r";
connectAttr "fol_base_meshShape.o" "follicleShape126.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape126.iwm";
connectAttr "follicleShape127.ot" "follicle127.t";
connectAttr "follicleShape127.or" "follicle127.r";
connectAttr "fol_base_meshShape.o" "follicleShape127.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape127.iwm";
connectAttr "follicleShape128.ot" "follicle128.t";
connectAttr "follicleShape128.or" "follicle128.r";
connectAttr "fol_base_meshShape.o" "follicleShape128.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape128.iwm";
connectAttr "follicleShape129.ot" "follicle129.t";
connectAttr "follicleShape129.or" "follicle129.r";
connectAttr "fol_base_meshShape.o" "follicleShape129.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape129.iwm";
connectAttr "follicleShape130.ot" "follicle130.t";
connectAttr "follicleShape130.or" "follicle130.r";
connectAttr "fol_base_meshShape.o" "follicleShape130.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape130.iwm";
connectAttr "follicleShape131.ot" "follicle131.t";
connectAttr "follicleShape131.or" "follicle131.r";
connectAttr "fol_base_meshShape.o" "follicleShape131.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape131.iwm";
connectAttr "follicleShape132.ot" "follicle132.t";
connectAttr "follicleShape132.or" "follicle132.r";
connectAttr "fol_base_meshShape.o" "follicleShape132.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape132.iwm";
connectAttr "follicleShape133.ot" "follicle133.t";
connectAttr "follicleShape133.or" "follicle133.r";
connectAttr "fol_base_meshShape.o" "follicleShape133.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape133.iwm";
connectAttr "follicleShape134.ot" "follicle134.t";
connectAttr "follicleShape134.or" "follicle134.r";
connectAttr "fol_base_meshShape.o" "follicleShape134.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape134.iwm";
connectAttr "follicleShape135.ot" "follicle135.t";
connectAttr "follicleShape135.or" "follicle135.r";
connectAttr "fol_base_meshShape.o" "follicleShape135.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape135.iwm";
connectAttr "follicleShape136.ot" "follicle136.t";
connectAttr "follicleShape136.or" "follicle136.r";
connectAttr "fol_base_meshShape.o" "follicleShape136.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape136.iwm";
connectAttr "follicleShape137.ot" "follicle137.t";
connectAttr "follicleShape137.or" "follicle137.r";
connectAttr "fol_base_meshShape.o" "follicleShape137.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape137.iwm";
connectAttr "follicleShape138.ot" "follicle138.t";
connectAttr "follicleShape138.or" "follicle138.r";
connectAttr "fol_base_meshShape.o" "follicleShape138.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape138.iwm";
connectAttr "follicleShape139.ot" "follicle139.t";
connectAttr "follicleShape139.or" "follicle139.r";
connectAttr "fol_base_meshShape.o" "follicleShape139.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape139.iwm";
connectAttr "follicleShape140.ot" "follicle140.t";
connectAttr "follicleShape140.or" "follicle140.r";
connectAttr "fol_base_meshShape.o" "follicleShape140.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape140.iwm";
connectAttr "follicleShape141.ot" "follicle141.t";
connectAttr "follicleShape141.or" "follicle141.r";
connectAttr "fol_base_meshShape.o" "follicleShape141.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape141.iwm";
connectAttr "follicleShape142.ot" "follicle142.t";
connectAttr "follicleShape142.or" "follicle142.r";
connectAttr "fol_base_meshShape.o" "follicleShape142.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape142.iwm";
connectAttr "follicleShape143.ot" "follicle143.t";
connectAttr "follicleShape143.or" "follicle143.r";
connectAttr "fol_base_meshShape.o" "follicleShape143.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape143.iwm";
connectAttr "follicleShape144.ot" "follicle144.t";
connectAttr "follicleShape144.or" "follicle144.r";
connectAttr "fol_base_meshShape.o" "follicleShape144.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape144.iwm";
connectAttr "follicleShape145.ot" "follicle145.t";
connectAttr "follicleShape145.or" "follicle145.r";
connectAttr "fol_base_meshShape.o" "follicleShape145.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape145.iwm";
connectAttr "follicleShape146.ot" "follicle146.t";
connectAttr "follicleShape146.or" "follicle146.r";
connectAttr "fol_base_meshShape.o" "follicleShape146.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape146.iwm";
connectAttr "follicleShape147.ot" "follicle147.t";
connectAttr "follicleShape147.or" "follicle147.r";
connectAttr "fol_base_meshShape.o" "follicleShape147.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape147.iwm";
connectAttr "follicleShape148.ot" "follicle148.t";
connectAttr "follicleShape148.or" "follicle148.r";
connectAttr "fol_base_meshShape.o" "follicleShape148.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape148.iwm";
connectAttr "follicleShape149.ot" "follicle149.t";
connectAttr "follicleShape149.or" "follicle149.r";
connectAttr "fol_base_meshShape.o" "follicleShape149.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape149.iwm";
connectAttr "follicleShape151.ot" "follicle151.t";
connectAttr "follicleShape151.or" "follicle151.r";
connectAttr "fol_base_meshShape.o" "follicleShape151.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape151.iwm";
connectAttr "follicleShape152.ot" "follicle152.t";
connectAttr "follicleShape152.or" "follicle152.r";
connectAttr "fol_base_meshShape.o" "follicleShape152.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape152.iwm";
connectAttr "follicleShape157.ot" "follicle157.t";
connectAttr "follicleShape157.or" "follicle157.r";
connectAttr "fol_base_meshShape.o" "follicleShape157.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape157.iwm";
connectAttr "follicleShape153.ot" "follicle153.t";
connectAttr "follicleShape153.or" "follicle153.r";
connectAttr "fol_base_meshShape.o" "follicleShape153.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape153.iwm";
connectAttr "follicleShape154.ot" "follicle154.t";
connectAttr "follicleShape154.or" "follicle154.r";
connectAttr "fol_base_meshShape.o" "follicleShape154.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape154.iwm";
connectAttr "follicleShape155.ot" "follicle155.t";
connectAttr "follicleShape155.or" "follicle155.r";
connectAttr "fol_base_meshShape.o" "follicleShape155.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape155.iwm";
connectAttr "follicleShape156.ot" "follicle156.t";
connectAttr "follicleShape156.or" "follicle156.r";
connectAttr "fol_base_meshShape.o" "follicleShape156.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape156.iwm";
connectAttr "follicleShape162.ot" "follicle162.t";
connectAttr "follicleShape162.or" "follicle162.r";
connectAttr "fol_base_meshShape.o" "follicleShape162.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape162.iwm";
connectAttr "follicleShape163.ot" "follicle163.t";
connectAttr "follicleShape163.or" "follicle163.r";
connectAttr "fol_base_meshShape.o" "follicleShape163.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape163.iwm";
connectAttr "follicleShape164.ot" "follicle164.t";
connectAttr "follicleShape164.or" "follicle164.r";
connectAttr "fol_base_meshShape.o" "follicleShape164.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape164.iwm";
connectAttr "follicleShape165.ot" "follicle165.t";
connectAttr "follicleShape165.or" "follicle165.r";
connectAttr "fol_base_meshShape.o" "follicleShape165.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape165.iwm";
connectAttr "follicleShape166.ot" "follicle166.t";
connectAttr "follicleShape166.or" "follicle166.r";
connectAttr "fol_base_meshShape.o" "follicleShape166.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape166.iwm";
connectAttr "follicleShape161.ot" "follicle161.t";
connectAttr "follicleShape161.or" "follicle161.r";
connectAttr "fol_base_meshShape.o" "follicleShape161.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape161.iwm";
connectAttr "follicleShape160.ot" "follicle160.t";
connectAttr "follicleShape160.or" "follicle160.r";
connectAttr "fol_base_meshShape.o" "follicleShape160.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape160.iwm";
connectAttr "follicleShape159.ot" "follicle159.t";
connectAttr "follicleShape159.or" "follicle159.r";
connectAttr "fol_base_meshShape.o" "follicleShape159.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape159.iwm";
connectAttr "follicleShape158.ot" "follicle158.t";
connectAttr "follicleShape158.or" "follicle158.r";
connectAttr "fol_base_meshShape.o" "follicleShape158.inm";
connectAttr "fol_base_meshShape.wm" "follicleShape158.iwm";
connectAttr "groupParts310.og" "skinCluster62.ip[0].ig";
connectAttr "brow_bs_meshShapeOrig.o" "skinCluster62.orggeom[0]";
connectAttr "adj_brow_C_001_jnt.wm" "skinCluster62.ma[0]";
connectAttr "adj_brow_L_001_jnt.wm" "skinCluster62.ma[1]";
connectAttr "adj_brow_R_001_jnt.wm" "skinCluster62.ma[2]";
connectAttr "adj_brow_C_001_jnt.liw" "skinCluster62.lw[0]";
connectAttr "adj_brow_L_001_jnt.liw" "skinCluster62.lw[1]";
connectAttr "adj_brow_R_001_jnt.liw" "skinCluster62.lw[2]";
connectAttr "adj_brow_C_001_jnt.obcc" "skinCluster62.ifcl[0]";
connectAttr "adj_brow_L_001_jnt.obcc" "skinCluster62.ifcl[1]";
connectAttr "adj_brow_R_001_jnt.obcc" "skinCluster62.ifcl[2]";
connectAttr "adj_brow_R_001_jnt.msg" "skinCluster62.ptt";
connectAttr "adj_jnt_grp.msg" "bindPose1.m[0]";
connectAttr "adj_brow_C_001_jnt.msg" "bindPose1.m[1]";
connectAttr "adj_brow_L_001_jnt.msg" "bindPose1.m[2]";
connectAttr "adj_brow_R_001_jnt.msg" "bindPose1.m[3]";
connectAttr "adj_forehead_C_001_jnt.msg" "bindPose1.m[4]";
connectAttr "adj_noseTip_C_001_jnt.msg" "bindPose1.m[5]";
connectAttr "adj_chin_C_001_jnt.msg" "bindPose1.m[6]";
connectAttr "adj_chinThroat_C_001_jnt.msg" "bindPose1.m[7]";
connectAttr "adj_forehead_L_001_jnt.msg" "bindPose1.m[8]";
connectAttr "adj_forehead_R_001_jnt.msg" "bindPose1.m[9]";
connectAttr "adj_forehead_C_002_jnt.msg" "bindPose1.m[10]";
connectAttr "adj_forehead_L_002_jnt.msg" "bindPose1.m[11]";
connectAttr "adj_forehead_R_002_jnt.msg" "bindPose1.m[12]";
connectAttr "adj_noseRoot_C_001_jnt.msg" "bindPose1.m[13]";
connectAttr "adj_eyeFrame_L_001_jnt.msg" "bindPose1.m[14]";
connectAttr "adj_eyeFrame_L_003_jnt.msg" "bindPose1.m[15]";
connectAttr "adj_bite_L_001_jnt.msg" "bindPose1.m[16]";
connectAttr "adj_lowlid_L_001_jnt.msg" "bindPose1.m[17]";
connectAttr "adj_lowlid_L_003_jnt.msg" "bindPose1.m[18]";
connectAttr "adj_eyeFrame_R_001_jnt.msg" "bindPose1.m[19]";
connectAttr "adj_eyeFrame_R_003_jnt.msg" "bindPose1.m[20]";
connectAttr "adj_bite_R_001_jnt.msg" "bindPose1.m[21]";
connectAttr "adj_lowlid_R_001_jnt.msg" "bindPose1.m[22]";
connectAttr "adj_lowlid_R_003_jnt.msg" "bindPose1.m[23]";
connectAttr "adj_browLid_L_001_jnt.msg" "bindPose1.m[24]";
connectAttr "adj_browLid_L_003_jnt.msg" "bindPose1.m[25]";
connectAttr "adj_browLid_R_001_jnt.msg" "bindPose1.m[26]";
connectAttr "adj_browLid_R_003_jnt.msg" "bindPose1.m[27]";
connectAttr "adj_noseWing_L_002_jnt.msg" "bindPose1.m[28]";
connectAttr "adj_zyg_L_001_jnt.msg" "bindPose1.m[29]";
connectAttr "adj_zyg_L_003_jnt.msg" "bindPose1.m[30]";
connectAttr "adj_cheek_L_001_jnt.msg" "bindPose1.m[31]";
connectAttr "adj_cheek_L_003_jnt.msg" "bindPose1.m[32]";
connectAttr "adj_noseWing_R_002_jnt.msg" "bindPose1.m[33]";
connectAttr "adj_zyg_R_001_jnt.msg" "bindPose1.m[34]";
connectAttr "adj_zyg_R_003_jnt.msg" "bindPose1.m[35]";
connectAttr "adj_cheek_R_001_jnt.msg" "bindPose1.m[36]";
connectAttr "adj_cheek_R_003_jnt.msg" "bindPose1.m[37]";
connectAttr "adj_noseBottom_C_001_jnt.msg" "bindPose1.m[38]";
connectAttr "adj_nosFlo_L_001_jnt.msg" "bindPose1.m[39]";
connectAttr "adj_nosFlo_L_003_jnt.msg" "bindPose1.m[40]";
connectAttr "adj_nosFlo_L_005_jnt.msg" "bindPose1.m[41]";
connectAttr "adj_nosFlo_R_001_jnt.msg" "bindPose1.m[42]";
connectAttr "adj_nosFlo_R_003_jnt.msg" "bindPose1.m[43]";
connectAttr "adj_nosFlo_R_005_jnt.msg" "bindPose1.m[44]";
connectAttr "adj_lipChin_C_001_jnt.msg" "bindPose1.m[45]";
connectAttr "adj_mouth_L_001_jnt.msg" "bindPose1.m[46]";
connectAttr "adj_mouth_R_001_jnt.msg" "bindPose1.m[47]";
connectAttr "adj_upLipFrame_C_001_jnt.msg" "bindPose1.m[48]";
connectAttr "adj_lowLipFrame_C_001_jnt.msg" "bindPose1.m[49]";
connectAttr "adj_chin_L_002_jnt.msg" "bindPose1.m[50]";
connectAttr "adj_chin_R_002_jnt.msg" "bindPose1.m[51]";
connectAttr "adj_chinNeck_L_001_jnt.msg" "bindPose1.m[52]";
connectAttr "adj_chinNeck_R_001_jnt.msg" "bindPose1.m[53]";
connectAttr "adj_throat_C_002_jnt.msg" "bindPose1.m[54]";
connectAttr "adj_clavicleNeck_L_001_jnt.msg" "bindPose1.m[55]";
connectAttr "adj_clavicleNeck_R_001_jnt.msg" "bindPose1.m[56]";
connectAttr "adj_chinThroat_L_002_jnt.msg" "bindPose1.m[57]";
connectAttr "adj_chinThroat_R_002_jnt.msg" "bindPose1.m[58]";
connectAttr "adj_clavicleNeck_L_005_jnt.msg" "bindPose1.m[59]";
connectAttr "adj_clavicleNeck_R_005_jnt.msg" "bindPose1.m[60]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[0]" "bindPose1.p[2]";
connectAttr "bindPose1.m[0]" "bindPose1.p[3]";
connectAttr "bindPose1.m[0]" "bindPose1.p[4]";
connectAttr "bindPose1.m[0]" "bindPose1.p[5]";
connectAttr "bindPose1.m[0]" "bindPose1.p[6]";
connectAttr "bindPose1.m[0]" "bindPose1.p[7]";
connectAttr "bindPose1.m[0]" "bindPose1.p[8]";
connectAttr "bindPose1.m[0]" "bindPose1.p[9]";
connectAttr "bindPose1.m[0]" "bindPose1.p[10]";
connectAttr "bindPose1.m[0]" "bindPose1.p[11]";
connectAttr "bindPose1.m[0]" "bindPose1.p[12]";
connectAttr "bindPose1.m[0]" "bindPose1.p[13]";
connectAttr "bindPose1.m[0]" "bindPose1.p[14]";
connectAttr "bindPose1.m[0]" "bindPose1.p[15]";
connectAttr "bindPose1.m[0]" "bindPose1.p[16]";
connectAttr "bindPose1.m[0]" "bindPose1.p[17]";
connectAttr "bindPose1.m[0]" "bindPose1.p[18]";
connectAttr "bindPose1.m[0]" "bindPose1.p[19]";
connectAttr "bindPose1.m[0]" "bindPose1.p[20]";
connectAttr "bindPose1.m[0]" "bindPose1.p[21]";
connectAttr "bindPose1.m[0]" "bindPose1.p[22]";
connectAttr "bindPose1.m[0]" "bindPose1.p[23]";
connectAttr "bindPose1.m[0]" "bindPose1.p[24]";
connectAttr "bindPose1.m[0]" "bindPose1.p[25]";
connectAttr "bindPose1.m[0]" "bindPose1.p[26]";
connectAttr "bindPose1.m[0]" "bindPose1.p[27]";
connectAttr "bindPose1.m[0]" "bindPose1.p[28]";
connectAttr "bindPose1.m[0]" "bindPose1.p[29]";
connectAttr "bindPose1.m[0]" "bindPose1.p[30]";
connectAttr "bindPose1.m[0]" "bindPose1.p[31]";
connectAttr "bindPose1.m[0]" "bindPose1.p[32]";
connectAttr "bindPose1.m[0]" "bindPose1.p[33]";
connectAttr "bindPose1.m[0]" "bindPose1.p[34]";
connectAttr "bindPose1.m[0]" "bindPose1.p[35]";
connectAttr "bindPose1.m[0]" "bindPose1.p[36]";
connectAttr "bindPose1.m[0]" "bindPose1.p[37]";
connectAttr "bindPose1.m[0]" "bindPose1.p[38]";
connectAttr "bindPose1.m[0]" "bindPose1.p[39]";
connectAttr "bindPose1.m[0]" "bindPose1.p[40]";
connectAttr "bindPose1.m[0]" "bindPose1.p[41]";
connectAttr "bindPose1.m[0]" "bindPose1.p[42]";
connectAttr "bindPose1.m[0]" "bindPose1.p[43]";
connectAttr "bindPose1.m[0]" "bindPose1.p[44]";
connectAttr "bindPose1.m[0]" "bindPose1.p[45]";
connectAttr "bindPose1.m[0]" "bindPose1.p[46]";
connectAttr "bindPose1.m[0]" "bindPose1.p[47]";
connectAttr "bindPose1.m[0]" "bindPose1.p[48]";
connectAttr "bindPose1.m[0]" "bindPose1.p[49]";
connectAttr "bindPose1.m[0]" "bindPose1.p[50]";
connectAttr "bindPose1.m[0]" "bindPose1.p[51]";
connectAttr "bindPose1.m[0]" "bindPose1.p[52]";
connectAttr "bindPose1.m[0]" "bindPose1.p[53]";
connectAttr "bindPose1.m[0]" "bindPose1.p[54]";
connectAttr "bindPose1.m[0]" "bindPose1.p[55]";
connectAttr "bindPose1.m[0]" "bindPose1.p[56]";
connectAttr "bindPose1.m[0]" "bindPose1.p[57]";
connectAttr "bindPose1.m[0]" "bindPose1.p[58]";
connectAttr "bindPose1.m[0]" "bindPose1.p[59]";
connectAttr "bindPose1.m[0]" "bindPose1.p[60]";
connectAttr "adj_brow_C_001_jnt.bps" "bindPose1.wm[1]";
connectAttr "adj_brow_L_001_jnt.bps" "bindPose1.wm[2]";
connectAttr "adj_brow_R_001_jnt.bps" "bindPose1.wm[3]";
connectAttr "adj_forehead_C_001_jnt.bps" "bindPose1.wm[4]";
connectAttr "adj_noseTip_C_001_jnt.bps" "bindPose1.wm[5]";
connectAttr "adj_chin_C_001_jnt.bps" "bindPose1.wm[6]";
connectAttr "adj_chinThroat_C_001_jnt.bps" "bindPose1.wm[7]";
connectAttr "adj_forehead_L_001_jnt.bps" "bindPose1.wm[8]";
connectAttr "adj_forehead_R_001_jnt.bps" "bindPose1.wm[9]";
connectAttr "adj_forehead_C_002_jnt.bps" "bindPose1.wm[10]";
connectAttr "adj_forehead_L_002_jnt.bps" "bindPose1.wm[11]";
connectAttr "adj_forehead_R_002_jnt.bps" "bindPose1.wm[12]";
connectAttr "adj_noseRoot_C_001_jnt.bps" "bindPose1.wm[13]";
connectAttr "adj_eyeFrame_L_001_jnt.bps" "bindPose1.wm[14]";
connectAttr "adj_eyeFrame_L_003_jnt.bps" "bindPose1.wm[15]";
connectAttr "adj_bite_L_001_jnt.bps" "bindPose1.wm[16]";
connectAttr "adj_lowlid_L_001_jnt.bps" "bindPose1.wm[17]";
connectAttr "adj_lowlid_L_003_jnt.bps" "bindPose1.wm[18]";
connectAttr "adj_eyeFrame_R_001_jnt.bps" "bindPose1.wm[19]";
connectAttr "adj_eyeFrame_R_003_jnt.bps" "bindPose1.wm[20]";
connectAttr "adj_bite_R_001_jnt.bps" "bindPose1.wm[21]";
connectAttr "adj_lowlid_R_001_jnt.bps" "bindPose1.wm[22]";
connectAttr "adj_lowlid_R_003_jnt.bps" "bindPose1.wm[23]";
connectAttr "adj_browLid_L_001_jnt.bps" "bindPose1.wm[24]";
connectAttr "adj_browLid_L_003_jnt.bps" "bindPose1.wm[25]";
connectAttr "adj_browLid_R_001_jnt.bps" "bindPose1.wm[26]";
connectAttr "adj_browLid_R_003_jnt.bps" "bindPose1.wm[27]";
connectAttr "adj_noseWing_L_002_jnt.bps" "bindPose1.wm[28]";
connectAttr "adj_zyg_L_001_jnt.bps" "bindPose1.wm[29]";
connectAttr "adj_zyg_L_003_jnt.bps" "bindPose1.wm[30]";
connectAttr "adj_cheek_L_001_jnt.bps" "bindPose1.wm[31]";
connectAttr "adj_cheek_L_003_jnt.bps" "bindPose1.wm[32]";
connectAttr "adj_noseWing_R_002_jnt.bps" "bindPose1.wm[33]";
connectAttr "adj_zyg_R_001_jnt.bps" "bindPose1.wm[34]";
connectAttr "adj_zyg_R_003_jnt.bps" "bindPose1.wm[35]";
connectAttr "adj_cheek_R_001_jnt.bps" "bindPose1.wm[36]";
connectAttr "adj_cheek_R_003_jnt.bps" "bindPose1.wm[37]";
connectAttr "adj_noseBottom_C_001_jnt.bps" "bindPose1.wm[38]";
connectAttr "adj_nosFlo_L_001_jnt.bps" "bindPose1.wm[39]";
connectAttr "adj_nosFlo_L_003_jnt.bps" "bindPose1.wm[40]";
connectAttr "adj_nosFlo_L_005_jnt.bps" "bindPose1.wm[41]";
connectAttr "adj_nosFlo_R_001_jnt.bps" "bindPose1.wm[42]";
connectAttr "adj_nosFlo_R_003_jnt.bps" "bindPose1.wm[43]";
connectAttr "adj_nosFlo_R_005_jnt.bps" "bindPose1.wm[44]";
connectAttr "adj_lipChin_C_001_jnt.bps" "bindPose1.wm[45]";
connectAttr "adj_mouth_L_001_jnt.bps" "bindPose1.wm[46]";
connectAttr "adj_mouth_R_001_jnt.bps" "bindPose1.wm[47]";
connectAttr "adj_upLipFrame_C_001_jnt.bps" "bindPose1.wm[48]";
connectAttr "adj_lowLipFrame_C_001_jnt.bps" "bindPose1.wm[49]";
connectAttr "adj_chin_L_002_jnt.bps" "bindPose1.wm[50]";
connectAttr "adj_chin_R_002_jnt.bps" "bindPose1.wm[51]";
connectAttr "adj_chinNeck_L_001_jnt.bps" "bindPose1.wm[52]";
connectAttr "adj_chinNeck_R_001_jnt.bps" "bindPose1.wm[53]";
connectAttr "adj_throat_C_002_jnt.bps" "bindPose1.wm[54]";
connectAttr "adj_clavicleNeck_L_001_jnt.bps" "bindPose1.wm[55]";
connectAttr "adj_clavicleNeck_R_001_jnt.bps" "bindPose1.wm[56]";
connectAttr "adj_chinThroat_L_002_jnt.bps" "bindPose1.wm[57]";
connectAttr "adj_chinThroat_R_002_jnt.bps" "bindPose1.wm[58]";
connectAttr "adj_clavicleNeck_L_005_jnt.bps" "bindPose1.wm[59]";
connectAttr "adj_clavicleNeck_R_005_jnt.bps" "bindPose1.wm[60]";
connectAttr "polyPlanarProj1.out" "groupParts310.ig";
connectAttr "groupId3038.id" "groupParts310.gi";
connectAttr "brow_bs_meshShapeOrig.w" "polyPlanarProj1.ip";
connectAttr "brow_bs_meshShape.wm" "polyPlanarProj1.mp";
connectAttr "lambert3.oc" "lambert3SG.ss";
connectAttr "brow_bs_meshShape.iog.og[0]" "lambert3SG.dsm" -na;
connectAttr "groupId3038.msg" "lambert3SG.gn" -na;
connectAttr "lambert3SG.msg" "materialInfo36.sg";
connectAttr "lambert3.msg" "materialInfo36.m";
connectAttr "polyPlanarProj2.out" "skinCluster66.ip[0].ig";
connectAttr "lowlid_bs_meshShapeOrig.o" "skinCluster66.orggeom[0]";
connectAttr "adj_lowlid_L_001_jnt.wm" "skinCluster66.ma[0]";
connectAttr "adj_lowlid_L_003_jnt.wm" "skinCluster66.ma[1]";
connectAttr "adj_lowlid_R_001_jnt.wm" "skinCluster66.ma[2]";
connectAttr "adj_lowlid_R_003_jnt.wm" "skinCluster66.ma[3]";
connectAttr "adj_lowlid_L_001_jnt.liw" "skinCluster66.lw[0]";
connectAttr "adj_lowlid_L_003_jnt.liw" "skinCluster66.lw[1]";
connectAttr "adj_lowlid_R_001_jnt.liw" "skinCluster66.lw[2]";
connectAttr "adj_lowlid_R_003_jnt.liw" "skinCluster66.lw[3]";
connectAttr "adj_lowlid_L_001_jnt.obcc" "skinCluster66.ifcl[0]";
connectAttr "adj_lowlid_L_003_jnt.obcc" "skinCluster66.ifcl[1]";
connectAttr "adj_lowlid_R_001_jnt.obcc" "skinCluster66.ifcl[2]";
connectAttr "adj_lowlid_R_003_jnt.obcc" "skinCluster66.ifcl[3]";
connectAttr "adj_lowlid_R_003_jnt.msg" "skinCluster66.ptt";
connectAttr "lowlid_bs_meshShapeOrig.w" "polyPlanarProj2.ip";
connectAttr "lowlid_bs_meshShape.wm" "polyPlanarProj2.mp";
connectAttr "lambert5SG.msg" "materialInfo38.sg";
connectAttr "lambert5.msg" "materialInfo38.m";
connectAttr "lambert5.oc" "lambert5SG.ss";
connectAttr "lowlid_bs_meshShape.iog" "lambert5SG.dsm" -na;
connectAttr "lambert4.oc" "lambert4SG.ss";
connectAttr "eyeFrame_bs_meshShape.iog.og[0]" "lambert4SG.dsm" -na;
connectAttr "groupId3041.msg" "lambert4SG.gn" -na;
connectAttr "lambert4SG.msg" "materialInfo37.sg";
connectAttr "lambert4.msg" "materialInfo37.m";
connectAttr "groupParts313.og" "skinCluster65.ip[0].ig";
connectAttr "eyeFrame_bs_meshShapeOrig.o" "skinCluster65.orggeom[0]";
connectAttr "adj_eyeFrame_L_001_jnt.wm" "skinCluster65.ma[0]";
connectAttr "adj_eyeFrame_L_003_jnt.wm" "skinCluster65.ma[1]";
connectAttr "adj_bite_L_001_jnt.wm" "skinCluster65.ma[2]";
connectAttr "adj_eyeFrame_R_001_jnt.wm" "skinCluster65.ma[3]";
connectAttr "adj_eyeFrame_R_003_jnt.wm" "skinCluster65.ma[4]";
connectAttr "adj_bite_R_001_jnt.wm" "skinCluster65.ma[5]";
connectAttr "adj_eyeFrame_L_001_jnt.liw" "skinCluster65.lw[0]";
connectAttr "adj_eyeFrame_L_003_jnt.liw" "skinCluster65.lw[1]";
connectAttr "adj_bite_L_001_jnt.liw" "skinCluster65.lw[2]";
connectAttr "adj_eyeFrame_R_001_jnt.liw" "skinCluster65.lw[3]";
connectAttr "adj_eyeFrame_R_003_jnt.liw" "skinCluster65.lw[4]";
connectAttr "adj_bite_R_001_jnt.liw" "skinCluster65.lw[5]";
connectAttr "adj_eyeFrame_L_001_jnt.obcc" "skinCluster65.ifcl[0]";
connectAttr "adj_eyeFrame_L_003_jnt.obcc" "skinCluster65.ifcl[1]";
connectAttr "adj_bite_L_001_jnt.obcc" "skinCluster65.ifcl[2]";
connectAttr "adj_eyeFrame_R_001_jnt.obcc" "skinCluster65.ifcl[3]";
connectAttr "adj_eyeFrame_R_003_jnt.obcc" "skinCluster65.ifcl[4]";
connectAttr "adj_bite_R_001_jnt.obcc" "skinCluster65.ifcl[5]";
connectAttr "adj_eyeFrame_R_003_jnt.msg" "skinCluster65.ptt";
connectAttr "polyPlanarProj3.out" "groupParts313.ig";
connectAttr "groupId3041.id" "groupParts313.gi";
connectAttr "eyeFrame_bs_meshShapeOrig.w" "polyPlanarProj3.ip";
connectAttr "eyeFrame_bs_meshShape.wm" "polyPlanarProj3.mp";
connectAttr "polyPlanarProj4.out" "skinCluster69.ip[0].ig";
connectAttr "zyg_bs_meshShapeOrig.o" "skinCluster69.orggeom[0]";
connectAttr "adj_zyg_L_001_jnt.wm" "skinCluster69.ma[0]";
connectAttr "adj_zyg_L_003_jnt.wm" "skinCluster69.ma[1]";
connectAttr "adj_zyg_R_001_jnt.wm" "skinCluster69.ma[2]";
connectAttr "adj_zyg_R_003_jnt.wm" "skinCluster69.ma[3]";
connectAttr "adj_zyg_L_001_jnt.liw" "skinCluster69.lw[0]";
connectAttr "adj_zyg_L_003_jnt.liw" "skinCluster69.lw[1]";
connectAttr "adj_zyg_R_001_jnt.liw" "skinCluster69.lw[2]";
connectAttr "adj_zyg_R_003_jnt.liw" "skinCluster69.lw[3]";
connectAttr "adj_zyg_L_001_jnt.obcc" "skinCluster69.ifcl[0]";
connectAttr "adj_zyg_L_003_jnt.obcc" "skinCluster69.ifcl[1]";
connectAttr "adj_zyg_R_001_jnt.obcc" "skinCluster69.ifcl[2]";
connectAttr "adj_zyg_R_003_jnt.obcc" "skinCluster69.ifcl[3]";
connectAttr "adj_zyg_L_003_jnt.msg" "skinCluster69.ptt";
connectAttr "zyg_bs_meshShapeOrig.w" "polyPlanarProj4.ip";
connectAttr "zyg_bs_meshShape.wm" "polyPlanarProj4.mp";
connectAttr "lambert7SG.msg" "materialInfo40.sg";
connectAttr "lambert7.msg" "materialInfo40.m";
connectAttr "lambert7.oc" "lambert7SG.ss";
connectAttr "zyg_bs_meshShape.iog" "lambert7SG.dsm" -na;
connectAttr "polyPlanarProj5.out" "skinCluster70.ip[0].ig";
connectAttr "cheek_bs_meshShapeOrig.o" "skinCluster70.orggeom[0]";
connectAttr "adj_cheek_L_001_jnt.wm" "skinCluster70.ma[0]";
connectAttr "adj_cheek_L_003_jnt.wm" "skinCluster70.ma[1]";
connectAttr "adj_cheek_R_001_jnt.wm" "skinCluster70.ma[2]";
connectAttr "adj_cheek_R_003_jnt.wm" "skinCluster70.ma[3]";
connectAttr "adj_cheek_L_001_jnt.liw" "skinCluster70.lw[0]";
connectAttr "adj_cheek_L_003_jnt.liw" "skinCluster70.lw[1]";
connectAttr "adj_cheek_R_001_jnt.liw" "skinCluster70.lw[2]";
connectAttr "adj_cheek_R_003_jnt.liw" "skinCluster70.lw[3]";
connectAttr "adj_cheek_L_001_jnt.obcc" "skinCluster70.ifcl[0]";
connectAttr "adj_cheek_L_003_jnt.obcc" "skinCluster70.ifcl[1]";
connectAttr "adj_cheek_R_001_jnt.obcc" "skinCluster70.ifcl[2]";
connectAttr "adj_cheek_R_003_jnt.obcc" "skinCluster70.ifcl[3]";
connectAttr "adj_cheek_L_003_jnt.msg" "skinCluster70.ptt";
connectAttr "cheek_bs_meshShapeOrig.w" "polyPlanarProj5.ip";
connectAttr "cheek_bs_meshShape.wm" "polyPlanarProj5.mp";
connectAttr "lambert8SG.msg" "materialInfo41.sg";
connectAttr "lambert8.msg" "materialInfo41.m";
connectAttr "lambert8.oc" "lambert8SG.ss";
connectAttr "cheek_bs_meshShape.iog" "lambert8SG.dsm" -na;
connectAttr "nose_bs_meshShape.iog.og[0]" "lambert8SG.dsm" -na;
connectAttr "groupId3040.msg" "lambert8SG.gn" -na;
connectAttr "lambert6.oc" "lambert6SG.ss";
connectAttr "nosFlo_bs_meshShape.iog.og[0]" "lambert6SG.dsm" -na;
connectAttr "groupId3044.msg" "lambert6SG.gn" -na;
connectAttr "lambert6SG.msg" "materialInfo39.sg";
connectAttr "lambert6.msg" "materialInfo39.m";
connectAttr "groupParts316.og" "skinCluster75.ip[0].ig";
connectAttr "nosFlo_bs_meshShapeOrig.o" "skinCluster75.orggeom[0]";
connectAttr "adj_nosFlo_L_001_jnt.wm" "skinCluster75.ma[0]";
connectAttr "adj_nosFlo_R_001_jnt.wm" "skinCluster75.ma[1]";
connectAttr "adj_nosFlo_R_003_jnt.wm" "skinCluster75.ma[2]";
connectAttr "adj_nosFlo_L_003_jnt.wm" "skinCluster75.ma[3]";
connectAttr "adj_nosFlo_L_005_jnt.wm" "skinCluster75.ma[4]";
connectAttr "adj_nosFlo_R_005_jnt.wm" "skinCluster75.ma[5]";
connectAttr "adj_lipChin_C_001_jnt.wm" "skinCluster75.ma[6]";
connectAttr "adj_nosFlo_L_001_jnt.liw" "skinCluster75.lw[0]";
connectAttr "adj_nosFlo_R_001_jnt.liw" "skinCluster75.lw[1]";
connectAttr "adj_nosFlo_R_003_jnt.liw" "skinCluster75.lw[2]";
connectAttr "adj_nosFlo_L_003_jnt.liw" "skinCluster75.lw[3]";
connectAttr "adj_nosFlo_L_005_jnt.liw" "skinCluster75.lw[4]";
connectAttr "adj_nosFlo_R_005_jnt.liw" "skinCluster75.lw[5]";
connectAttr "adj_lipChin_C_001_jnt.liw" "skinCluster75.lw[6]";
connectAttr "adj_nosFlo_L_001_jnt.obcc" "skinCluster75.ifcl[0]";
connectAttr "adj_nosFlo_R_001_jnt.obcc" "skinCluster75.ifcl[1]";
connectAttr "adj_nosFlo_R_003_jnt.obcc" "skinCluster75.ifcl[2]";
connectAttr "adj_nosFlo_L_003_jnt.obcc" "skinCluster75.ifcl[3]";
connectAttr "adj_nosFlo_L_005_jnt.obcc" "skinCluster75.ifcl[4]";
connectAttr "adj_nosFlo_R_005_jnt.obcc" "skinCluster75.ifcl[5]";
connectAttr "adj_lipChin_C_001_jnt.obcc" "skinCluster75.ifcl[6]";
connectAttr "adj_nosFlo_L_001_jnt.msg" "skinCluster75.ptt";
connectAttr "polyPlanarProj6.out" "groupParts316.ig";
connectAttr "groupId3044.id" "groupParts316.gi";
connectAttr "nosFlo_bs_meshShapeOrig.w" "polyPlanarProj6.ip";
connectAttr "nosFlo_bs_meshShape.wm" "polyPlanarProj6.mp";
connectAttr "lambert9.oc" "lambert9SG.ss";
connectAttr "chin_bs_meshShape.iog.og[0]" "lambert9SG.dsm" -na;
connectAttr "groupId3043.msg" "lambert9SG.gn" -na;
connectAttr "lambert9SG.msg" "materialInfo42.sg";
connectAttr "lambert9.msg" "materialInfo42.m";
connectAttr "groupParts315.og" "skinCluster71.ip[0].ig";
connectAttr "chin_bs_meshShapeOrig.o" "skinCluster71.orggeom[0]";
connectAttr "adj_chin_C_001_jnt.wm" "skinCluster71.ma[0]";
connectAttr "adj_chin_L_002_jnt.wm" "skinCluster71.ma[1]";
connectAttr "adj_chinNeck_L_001_jnt.wm" "skinCluster71.ma[2]";
connectAttr "adj_chin_R_002_jnt.wm" "skinCluster71.ma[3]";
connectAttr "adj_chinNeck_R_001_jnt.wm" "skinCluster71.ma[4]";
connectAttr "adj_chin_C_001_jnt.liw" "skinCluster71.lw[0]";
connectAttr "adj_chin_L_002_jnt.liw" "skinCluster71.lw[1]";
connectAttr "adj_chinNeck_L_001_jnt.liw" "skinCluster71.lw[2]";
connectAttr "adj_chin_R_002_jnt.liw" "skinCluster71.lw[3]";
connectAttr "adj_chinNeck_R_001_jnt.liw" "skinCluster71.lw[4]";
connectAttr "adj_chin_C_001_jnt.obcc" "skinCluster71.ifcl[0]";
connectAttr "adj_chin_L_002_jnt.obcc" "skinCluster71.ifcl[1]";
connectAttr "adj_chinNeck_L_001_jnt.obcc" "skinCluster71.ifcl[2]";
connectAttr "adj_chin_R_002_jnt.obcc" "skinCluster71.ifcl[3]";
connectAttr "adj_chinNeck_R_001_jnt.obcc" "skinCluster71.ifcl[4]";
connectAttr "adj_chin_L_002_jnt.msg" "skinCluster71.ptt";
connectAttr "polyPlanarProj7.out" "groupParts315.ig";
connectAttr "groupId3043.id" "groupParts315.gi";
connectAttr "chin_bs_meshShapeOrig.w" "polyPlanarProj7.ip";
connectAttr "chin_bs_meshShape.wm" "polyPlanarProj7.mp";
connectAttr "polyPlanarProj8.out" "skinCluster68.ip[0].ig";
connectAttr "lipFrame_bs_meshShapeOrig.o" "skinCluster68.orggeom[0]";
connectAttr "adj_lowLipFrame_C_001_jnt.wm" "skinCluster68.ma[0]";
connectAttr "adj_mouth_L_001_jnt.wm" "skinCluster68.ma[1]";
connectAttr "adj_upLipFrame_C_001_jnt.wm" "skinCluster68.ma[2]";
connectAttr "adj_mouth_R_001_jnt.wm" "skinCluster68.ma[3]";
connectAttr "adj_lowLipFrame_C_001_jnt.liw" "skinCluster68.lw[0]";
connectAttr "adj_mouth_L_001_jnt.liw" "skinCluster68.lw[1]";
connectAttr "adj_upLipFrame_C_001_jnt.liw" "skinCluster68.lw[2]";
connectAttr "adj_mouth_R_001_jnt.liw" "skinCluster68.lw[3]";
connectAttr "adj_lowLipFrame_C_001_jnt.obcc" "skinCluster68.ifcl[0]";
connectAttr "adj_mouth_L_001_jnt.obcc" "skinCluster68.ifcl[1]";
connectAttr "adj_upLipFrame_C_001_jnt.obcc" "skinCluster68.ifcl[2]";
connectAttr "adj_mouth_R_001_jnt.obcc" "skinCluster68.ifcl[3]";
connectAttr "adj_upLipFrame_C_001_jnt.msg" "skinCluster68.ptt";
connectAttr "lipFrame_bs_meshShapeOrig.w" "polyPlanarProj8.ip";
connectAttr "lipFrame_bs_meshShape.wm" "polyPlanarProj8.mp";
connectAttr "lambert10SG.msg" "materialInfo43.sg";
connectAttr "lambert10.msg" "materialInfo43.m";
connectAttr "lambert10.oc" "lambert10SG.ss";
connectAttr "lipFrame_bs_meshShape.iog" "lambert10SG.dsm" -na;
connectAttr "groupParts312.og" "skinCluster64.ip[0].ig";
connectAttr "nose_bs_meshShapeOrig.o" "skinCluster64.orggeom[0]";
connectAttr "adj_noseTip_C_001_jnt.wm" "skinCluster64.ma[0]";
connectAttr "adj_noseRoot_C_001_jnt.wm" "skinCluster64.ma[1]";
connectAttr "adj_noseWing_L_002_jnt.wm" "skinCluster64.ma[2]";
connectAttr "adj_noseWing_R_002_jnt.wm" "skinCluster64.ma[3]";
connectAttr "adj_noseBottom_C_001_jnt.wm" "skinCluster64.ma[4]";
connectAttr "adj_noseTip_C_001_jnt.liw" "skinCluster64.lw[0]";
connectAttr "adj_noseRoot_C_001_jnt.liw" "skinCluster64.lw[1]";
connectAttr "adj_noseWing_L_002_jnt.liw" "skinCluster64.lw[2]";
connectAttr "adj_noseWing_R_002_jnt.liw" "skinCluster64.lw[3]";
connectAttr "adj_noseBottom_C_001_jnt.liw" "skinCluster64.lw[4]";
connectAttr "adj_noseTip_C_001_jnt.obcc" "skinCluster64.ifcl[0]";
connectAttr "adj_noseRoot_C_001_jnt.obcc" "skinCluster64.ifcl[1]";
connectAttr "adj_noseWing_L_002_jnt.obcc" "skinCluster64.ifcl[2]";
connectAttr "adj_noseWing_R_002_jnt.obcc" "skinCluster64.ifcl[3]";
connectAttr "adj_noseBottom_C_001_jnt.obcc" "skinCluster64.ifcl[4]";
connectAttr "adj_noseBottom_C_001_jnt.msg" "skinCluster64.ptt";
connectAttr "polyPlanarProj9.out" "groupParts312.ig";
connectAttr "groupId3040.id" "groupParts312.gi";
connectAttr "nose_bs_meshShapeOrig.w" "polyPlanarProj9.ip";
connectAttr "nose_bs_meshShape.wm" "polyPlanarProj9.mp";
connectAttr "lambert11.oc" "lambert11SG.ss";
connectAttr "forehead_bs_meshShape.iog.og[0]" "lambert11SG.dsm" -na;
connectAttr "groupId3039.msg" "lambert11SG.gn" -na;
connectAttr "lambert11SG.msg" "materialInfo44.sg";
connectAttr "lambert11.msg" "materialInfo44.m";
connectAttr "groupParts311.og" "skinCluster63.ip[0].ig";
connectAttr "forehead_bs_meshShapeOrig.o" "skinCluster63.orggeom[0]";
connectAttr "adj_forehead_C_001_jnt.wm" "skinCluster63.ma[0]";
connectAttr "adj_forehead_L_001_jnt.wm" "skinCluster63.ma[1]";
connectAttr "adj_forehead_R_001_jnt.wm" "skinCluster63.ma[2]";
connectAttr "adj_forehead_C_002_jnt.wm" "skinCluster63.ma[3]";
connectAttr "adj_forehead_L_002_jnt.wm" "skinCluster63.ma[4]";
connectAttr "adj_forehead_R_002_jnt.wm" "skinCluster63.ma[5]";
connectAttr "adj_forehead_C_001_jnt.liw" "skinCluster63.lw[0]";
connectAttr "adj_forehead_L_001_jnt.liw" "skinCluster63.lw[1]";
connectAttr "adj_forehead_R_001_jnt.liw" "skinCluster63.lw[2]";
connectAttr "adj_forehead_C_002_jnt.liw" "skinCluster63.lw[3]";
connectAttr "adj_forehead_L_002_jnt.liw" "skinCluster63.lw[4]";
connectAttr "adj_forehead_R_002_jnt.liw" "skinCluster63.lw[5]";
connectAttr "adj_forehead_C_001_jnt.obcc" "skinCluster63.ifcl[0]";
connectAttr "adj_forehead_L_001_jnt.obcc" "skinCluster63.ifcl[1]";
connectAttr "adj_forehead_R_001_jnt.obcc" "skinCluster63.ifcl[2]";
connectAttr "adj_forehead_C_002_jnt.obcc" "skinCluster63.ifcl[3]";
connectAttr "adj_forehead_L_002_jnt.obcc" "skinCluster63.ifcl[4]";
connectAttr "adj_forehead_R_002_jnt.obcc" "skinCluster63.ifcl[5]";
connectAttr "adj_forehead_R_002_jnt.msg" "skinCluster63.ptt";
connectAttr "polyPlanarProj10.out" "groupParts311.ig";
connectAttr "groupId3039.id" "groupParts311.gi";
connectAttr "forehead_bs_meshShapeOrig.w" "polyPlanarProj10.ip";
connectAttr "forehead_bs_meshShape.wm" "polyPlanarProj10.mp";
connectAttr "skinCluster72.og[0]" "polyTweakUV1.ip";
connectAttr "polyPlanarProj11.out" "skinCluster72.ip[0].ig";
connectAttr "throat_bs_meshShapeOrig.o" "skinCluster72.orggeom[0]";
connectAttr "adj_chinThroat_C_001_jnt.wm" "skinCluster72.ma[0]";
connectAttr "adj_throat_C_002_jnt.wm" "skinCluster72.ma[1]";
connectAttr "adj_chinThroat_L_002_jnt.wm" "skinCluster72.ma[2]";
connectAttr "adj_chinThroat_R_002_jnt.wm" "skinCluster72.ma[3]";
connectAttr "adj_clavicleNeck_L_001_jnt.wm" "skinCluster72.ma[4]";
connectAttr "adj_clavicleNeck_R_001_jnt.wm" "skinCluster72.ma[5]";
connectAttr "adj_clavicleNeck_L_005_jnt.wm" "skinCluster72.ma[6]";
connectAttr "adj_clavicleNeck_R_005_jnt.wm" "skinCluster72.ma[7]";
connectAttr "adj_chinThroat_C_001_jnt.liw" "skinCluster72.lw[0]";
connectAttr "adj_throat_C_002_jnt.liw" "skinCluster72.lw[1]";
connectAttr "adj_chinThroat_L_002_jnt.liw" "skinCluster72.lw[2]";
connectAttr "adj_chinThroat_R_002_jnt.liw" "skinCluster72.lw[3]";
connectAttr "adj_clavicleNeck_L_001_jnt.liw" "skinCluster72.lw[4]";
connectAttr "adj_clavicleNeck_R_001_jnt.liw" "skinCluster72.lw[5]";
connectAttr "adj_clavicleNeck_L_005_jnt.liw" "skinCluster72.lw[6]";
connectAttr "adj_clavicleNeck_R_005_jnt.liw" "skinCluster72.lw[7]";
connectAttr "adj_chinThroat_C_001_jnt.obcc" "skinCluster72.ifcl[0]";
connectAttr "adj_throat_C_002_jnt.obcc" "skinCluster72.ifcl[1]";
connectAttr "adj_chinThroat_L_002_jnt.obcc" "skinCluster72.ifcl[2]";
connectAttr "adj_chinThroat_R_002_jnt.obcc" "skinCluster72.ifcl[3]";
connectAttr "adj_clavicleNeck_L_001_jnt.obcc" "skinCluster72.ifcl[4]";
connectAttr "adj_clavicleNeck_R_001_jnt.obcc" "skinCluster72.ifcl[5]";
connectAttr "adj_clavicleNeck_L_005_jnt.obcc" "skinCluster72.ifcl[6]";
connectAttr "adj_clavicleNeck_R_005_jnt.obcc" "skinCluster72.ifcl[7]";
connectAttr "adj_chinThroat_C_001_jnt.msg" "skinCluster72.ptt";
connectAttr "throat_bs_meshShapeOrig.w" "polyPlanarProj11.ip";
connectAttr "throat_bs_meshShape.wm" "polyPlanarProj11.mp";
connectAttr "lambert13SG.msg" "materialInfo46.sg";
connectAttr "lambert13.msg" "materialInfo46.m";
connectAttr "lambert13.oc" "lambert13SG.ss";
connectAttr "throat_bs_meshShape.iog" "lambert13SG.dsm" -na;
connectAttr "polyPlanarProj12.out" "skinCluster74.ip[0].ig";
connectAttr "chinThroat_bs_meshShapeOrig.o" "skinCluster74.orggeom[0]";
connectAttr "adj_chinThroat_R_002_jnt.wm" "skinCluster74.ma[0]";
connectAttr "adj_chinThroat_L_002_jnt.wm" "skinCluster74.ma[2]";
connectAttr "adj_chinThroat_C_001_jnt.wm" "skinCluster74.ma[4]";
connectAttr "adj_clavicleNeck_L_001_jnt.wm" "skinCluster74.ma[5]";
connectAttr "adj_clavicleNeck_R_001_jnt.wm" "skinCluster74.ma[6]";
connectAttr "adj_throat_C_002_jnt.wm" "skinCluster74.ma[7]";
connectAttr "adj_clavicleNeck_L_005_jnt.wm" "skinCluster74.ma[8]";
connectAttr "adj_clavicleNeck_R_005_jnt.wm" "skinCluster74.ma[9]";
connectAttr "adj_chinThroat_R_002_jnt.liw" "skinCluster74.lw[0]";
connectAttr "adj_chinThroat_L_002_jnt.liw" "skinCluster74.lw[2]";
connectAttr "adj_chinThroat_C_001_jnt.liw" "skinCluster74.lw[4]";
connectAttr "adj_clavicleNeck_L_001_jnt.liw" "skinCluster74.lw[5]";
connectAttr "adj_clavicleNeck_R_001_jnt.liw" "skinCluster74.lw[6]";
connectAttr "adj_throat_C_002_jnt.liw" "skinCluster74.lw[7]";
connectAttr "adj_clavicleNeck_L_005_jnt.liw" "skinCluster74.lw[8]";
connectAttr "adj_clavicleNeck_R_005_jnt.liw" "skinCluster74.lw[9]";
connectAttr "adj_chinThroat_R_002_jnt.obcc" "skinCluster74.ifcl[0]";
connectAttr "adj_chinThroat_L_002_jnt.obcc" "skinCluster74.ifcl[2]";
connectAttr "adj_chinThroat_C_001_jnt.obcc" "skinCluster74.ifcl[4]";
connectAttr "adj_clavicleNeck_L_001_jnt.obcc" "skinCluster74.ifcl[5]";
connectAttr "adj_clavicleNeck_R_001_jnt.obcc" "skinCluster74.ifcl[6]";
connectAttr "adj_throat_C_002_jnt.obcc" "skinCluster74.ifcl[7]";
connectAttr "adj_clavicleNeck_L_005_jnt.obcc" "skinCluster74.ifcl[8]";
connectAttr "adj_clavicleNeck_R_005_jnt.obcc" "skinCluster74.ifcl[9]";
connectAttr "adj_chinThroat_C_001_jnt.msg" "skinCluster74.ptt";
connectAttr "chinThroat_bs_meshShapeOrig.w" "polyPlanarProj12.ip";
connectAttr "chinThroat_bs_meshShape.wm" "polyPlanarProj12.mp";
connectAttr "lambert14SG.msg" "materialInfo47.sg";
connectAttr "lambert14.msg" "materialInfo47.m";
connectAttr "lambert14.oc" "lambert14SG.ss";
connectAttr "chinThroat_bs_meshShape.iog" "lambert14SG.dsm" -na;
connectAttr "polyPlanarProj13.out" "skinCluster73.ip[0].ig";
connectAttr "clavicleNeck_bs_meshShapeOrig.o" "skinCluster73.orggeom[0]";
connectAttr "adj_clavicleNeck_L_001_jnt.wm" "skinCluster73.ma[0]";
connectAttr "adj_clavicleNeck_R_001_jnt.wm" "skinCluster73.ma[1]";
connectAttr "adj_clavicleNeck_R_005_jnt.wm" "skinCluster73.ma[2]";
connectAttr "adj_clavicleNeck_L_005_jnt.wm" "skinCluster73.ma[4]";
connectAttr "adj_chinThroat_C_001_jnt.wm" "skinCluster73.ma[5]";
connectAttr "adj_throat_C_002_jnt.wm" "skinCluster73.ma[6]";
connectAttr "adj_chinThroat_L_002_jnt.wm" "skinCluster73.ma[7]";
connectAttr "adj_chinThroat_R_002_jnt.wm" "skinCluster73.ma[8]";
connectAttr "adj_clavicleNeck_L_001_jnt.liw" "skinCluster73.lw[0]";
connectAttr "adj_clavicleNeck_R_001_jnt.liw" "skinCluster73.lw[1]";
connectAttr "adj_clavicleNeck_R_005_jnt.liw" "skinCluster73.lw[2]";
connectAttr "adj_clavicleNeck_L_005_jnt.liw" "skinCluster73.lw[4]";
connectAttr "adj_chinThroat_C_001_jnt.liw" "skinCluster73.lw[5]";
connectAttr "adj_throat_C_002_jnt.liw" "skinCluster73.lw[6]";
connectAttr "adj_chinThroat_L_002_jnt.liw" "skinCluster73.lw[7]";
connectAttr "adj_chinThroat_R_002_jnt.liw" "skinCluster73.lw[8]";
connectAttr "adj_clavicleNeck_L_001_jnt.obcc" "skinCluster73.ifcl[0]";
connectAttr "adj_clavicleNeck_R_001_jnt.obcc" "skinCluster73.ifcl[1]";
connectAttr "adj_clavicleNeck_R_005_jnt.obcc" "skinCluster73.ifcl[2]";
connectAttr "adj_clavicleNeck_L_005_jnt.obcc" "skinCluster73.ifcl[4]";
connectAttr "adj_chinThroat_C_001_jnt.obcc" "skinCluster73.ifcl[5]";
connectAttr "adj_throat_C_002_jnt.obcc" "skinCluster73.ifcl[6]";
connectAttr "adj_chinThroat_L_002_jnt.obcc" "skinCluster73.ifcl[7]";
connectAttr "adj_chinThroat_R_002_jnt.obcc" "skinCluster73.ifcl[8]";
connectAttr "adj_chinThroat_L_002_jnt.msg" "skinCluster73.ptt";
connectAttr "clavicleNeck_bs_meshShapeOrig.w" "polyPlanarProj13.ip";
connectAttr "clavicleNeck_bs_meshShape.wm" "polyPlanarProj13.mp";
connectAttr "lambert15SG.msg" "materialInfo48.sg";
connectAttr "lambert15.msg" "materialInfo48.m";
connectAttr "lambert15.oc" "lambert15SG.ss";
connectAttr "clavicleNeck_bs_meshShape.iog" "lambert15SG.dsm" -na;
connectAttr "polyPlanarProj14.out" "skinCluster76.ip[0].ig";
connectAttr "browLid_bs_meshShapeOrig.o" "skinCluster76.orggeom[0]";
connectAttr "adj_browLid_L_001_jnt.wm" "skinCluster76.ma[0]";
connectAttr "adj_browLid_L_003_jnt.wm" "skinCluster76.ma[1]";
connectAttr "adj_browLid_R_001_jnt.wm" "skinCluster76.ma[2]";
connectAttr "adj_browLid_R_003_jnt.wm" "skinCluster76.ma[3]";
connectAttr "adj_browLid_L_001_jnt.liw" "skinCluster76.lw[0]";
connectAttr "adj_browLid_L_003_jnt.liw" "skinCluster76.lw[1]";
connectAttr "adj_browLid_R_001_jnt.liw" "skinCluster76.lw[2]";
connectAttr "adj_browLid_R_003_jnt.liw" "skinCluster76.lw[3]";
connectAttr "adj_browLid_L_001_jnt.obcc" "skinCluster76.ifcl[0]";
connectAttr "adj_browLid_L_003_jnt.obcc" "skinCluster76.ifcl[1]";
connectAttr "adj_browLid_R_001_jnt.obcc" "skinCluster76.ifcl[2]";
connectAttr "adj_browLid_R_003_jnt.obcc" "skinCluster76.ifcl[3]";
connectAttr "adj_browLid_L_001_jnt.msg" "skinCluster76.ptt";
connectAttr "browLid_bs_meshShapeOrig.w" "polyPlanarProj14.ip";
connectAttr "browLid_bs_meshShape.wm" "polyPlanarProj14.mp";
connectAttr "lambert16SG.msg" "materialInfo49.sg";
connectAttr "lambert16.msg" "materialInfo49.m";
connectAttr "lambert16.oc" "lambert16SG.ss";
connectAttr "browLid_bs_meshShape.iog" "lambert16SG.dsm" -na;
connectAttr "base_bs_meshShapeOrig.w" "skinCluster77.ip[0].ig";
connectAttr "base_bs_meshShapeOrig.o" "skinCluster77.orggeom[0]";
connectAttr "fol_brow_R_003_jnt.wm" "skinCluster77.ma[0]";
connectAttr "fol_brow_R_002_jnt.wm" "skinCluster77.ma[1]";
connectAttr "fol_brow_R_001_jnt.wm" "skinCluster77.ma[2]";
connectAttr "fol_brow_L_003_jnt.wm" "skinCluster77.ma[3]";
connectAttr "fol_brow_L_002_jnt.wm" "skinCluster77.ma[4]";
connectAttr "fol_brow_L_001_jnt.wm" "skinCluster77.ma[5]";
connectAttr "fol_brow_C_001_jnt.wm" "skinCluster77.ma[6]";
connectAttr "fol_browLid_L_001_jnt.wm" "skinCluster77.ma[7]";
connectAttr "fol_browLid_L_002_jnt.wm" "skinCluster77.ma[8]";
connectAttr "fol_browLid_L_003_jnt.wm" "skinCluster77.ma[9]";
connectAttr "fol_browLid_R_001_jnt.wm" "skinCluster77.ma[10]";
connectAttr "fol_browLid_R_002_jnt.wm" "skinCluster77.ma[11]";
connectAttr "fol_browLid_R_003_jnt.wm" "skinCluster77.ma[12]";
connectAttr "fol_forehead_L_002_jnt.wm" "skinCluster77.ma[13]";
connectAttr "fol_forehead_R_002_jnt.wm" "skinCluster77.ma[14]";
connectAttr "fol_forehead_C_002_jnt.wm" "skinCluster77.ma[15]";
connectAttr "fol_forehead_R_001_jnt.wm" "skinCluster77.ma[16]";
connectAttr "fol_forehead_L_001_jnt.wm" "skinCluster77.ma[17]";
connectAttr "fol_forehead_C_001_jnt.wm" "skinCluster77.ma[18]";
connectAttr "fol_eyeFrame_L_001_jnt.wm" "skinCluster77.ma[19]";
connectAttr "fol_eyeFrame_L_002_jnt.wm" "skinCluster77.ma[20]";
connectAttr "fol_eyeFrame_L_003_jnt.wm" "skinCluster77.ma[21]";
connectAttr "fol_eyeFrame_L_004_jnt.wm" "skinCluster77.ma[22]";
connectAttr "fol_eyeFrame_L_005_jnt.wm" "skinCluster77.ma[23]";
connectAttr "fol_eyeFrame_R_001_jnt.wm" "skinCluster77.ma[24]";
connectAttr "fol_eyeFrame_R_002_jnt.wm" "skinCluster77.ma[25]";
connectAttr "fol_eyeFrame_R_003_jnt.wm" "skinCluster77.ma[26]";
connectAttr "fol_eyeFrame_R_004_jnt.wm" "skinCluster77.ma[27]";
connectAttr "fol_eyeFrame_R_005_jnt.wm" "skinCluster77.ma[28]";
connectAttr "fol_bite_L_001_jnt.wm" "skinCluster77.ma[29]";
connectAttr "fol_bite_R_001_jnt.wm" "skinCluster77.ma[30]";
connectAttr "fol_lowlid_L_001_jnt.wm" "skinCluster77.ma[31]";
connectAttr "fol_lowlid_L_002_jnt.wm" "skinCluster77.ma[32]";
connectAttr "fol_lowlid_L_003_jnt.wm" "skinCluster77.ma[33]";
connectAttr "fol_lowlid_R_001_jnt.wm" "skinCluster77.ma[34]";
connectAttr "fol_lowlid_R_002_jnt.wm" "skinCluster77.ma[35]";
connectAttr "fol_lowlid_R_003_jnt.wm" "skinCluster77.ma[36]";
connectAttr "fol_noseRoot_C_001_jnt.wm" "skinCluster77.ma[37]";
connectAttr "fol_noseTip_C_001_jnt.wm" "skinCluster77.ma[38]";
connectAttr "fol_noseBottom_C_001_jnt.wm" "skinCluster77.ma[39]";
connectAttr "fol_noseWing_L_001_jnt.wm" "skinCluster77.ma[40]";
connectAttr "fol_noseWing_L_002_jnt.wm" "skinCluster77.ma[41]";
connectAttr "fol_noseWing_R_001_jnt.wm" "skinCluster77.ma[42]";
connectAttr "fol_noseWing_R_002_jnt.wm" "skinCluster77.ma[43]";
connectAttr "fol_lipChin_C_001_jnt.wm" "skinCluster77.ma[44]";
connectAttr "fol_nosFlo_L_001_jnt.wm" "skinCluster77.ma[45]";
connectAttr "fol_nosFlo_L_002_jnt.wm" "skinCluster77.ma[46]";
connectAttr "fol_nosFlo_L_003_jnt.wm" "skinCluster77.ma[47]";
connectAttr "fol_nosFlo_L_004_jnt.wm" "skinCluster77.ma[48]";
connectAttr "fol_nosFlo_L_005_jnt.wm" "skinCluster77.ma[49]";
connectAttr "fol_lipChin_L_002_jnt.wm" "skinCluster77.ma[50]";
connectAttr "fol_lipChin_L_001_jnt.wm" "skinCluster77.ma[51]";
connectAttr "fol_nosFlo_R_001_jnt.wm" "skinCluster77.ma[52]";
connectAttr "fol_nosFlo_R_002_jnt.wm" "skinCluster77.ma[53]";
connectAttr "fol_nosFlo_R_003_jnt.wm" "skinCluster77.ma[54]";
connectAttr "fol_nosFlo_R_004_jnt.wm" "skinCluster77.ma[55]";
connectAttr "fol_nosFlo_R_005_jnt.wm" "skinCluster77.ma[56]";
connectAttr "fol_lipChin_R_002_jnt.wm" "skinCluster77.ma[57]";
connectAttr "fol_lipChin_R_001_jnt.wm" "skinCluster77.ma[58]";
connectAttr "fol_zyg_L_001_jnt.wm" "skinCluster77.ma[59]";
connectAttr "fol_zyg_L_002_jnt.wm" "skinCluster77.ma[60]";
connectAttr "fol_zyg_L_003_jnt.wm" "skinCluster77.ma[61]";
connectAttr "fol_zyg_R_001_jnt.wm" "skinCluster77.ma[62]";
connectAttr "fol_zyg_R_002_jnt.wm" "skinCluster77.ma[63]";
connectAttr "fol_zyg_R_003_jnt.wm" "skinCluster77.ma[64]";
connectAttr "fol_cheek_L_001_jnt.wm" "skinCluster77.ma[65]";
connectAttr "fol_cheek_L_002_jnt.wm" "skinCluster77.ma[66]";
connectAttr "fol_cheek_L_003_jnt.wm" "skinCluster77.ma[67]";
connectAttr "fol_cheek_R_001_jnt.wm" "skinCluster77.ma[68]";
connectAttr "fol_cheek_R_002_jnt.wm" "skinCluster77.ma[69]";
connectAttr "fol_cheek_R_003_jnt.wm" "skinCluster77.ma[70]";
connectAttr "fol_upLipFrame_C_001_jnt.wm" "skinCluster77.ma[71]";
connectAttr "fol_lowLipFrame_C_001_jnt.wm" "skinCluster77.ma[72]";
connectAttr "fol_upLipFrame_L_001_jnt.wm" "skinCluster77.ma[73]";
connectAttr "fol_upLipFrame_L_002_jnt.wm" "skinCluster77.ma[74]";
connectAttr "fol_mouth_L_001_jnt.wm" "skinCluster77.ma[75]";
connectAttr "fol_lowLipFrame_L_002_jnt.wm" "skinCluster77.ma[76]";
connectAttr "fol_lowLipFrame_L_001_jnt.wm" "skinCluster77.ma[77]";
connectAttr "fol_upLipFrame_R_001_jnt.wm" "skinCluster77.ma[78]";
connectAttr "fol_upLipFrame_R_002_jnt.wm" "skinCluster77.ma[79]";
connectAttr "fol_mouth_R_001_jnt.wm" "skinCluster77.ma[80]";
connectAttr "fol_lowLipFrame_R_002_jnt.wm" "skinCluster77.ma[81]";
connectAttr "fol_lowLipFrame_R_001_jnt.wm" "skinCluster77.ma[82]";
connectAttr "fol_chin_C_001_jnt.wm" "skinCluster77.ma[83]";
connectAttr "fol_chin_L_001_jnt.wm" "skinCluster77.ma[84]";
connectAttr "fol_chin_L_002_jnt.wm" "skinCluster77.ma[85]";
connectAttr "fol_chin_L_003_jnt.wm" "skinCluster77.ma[86]";
connectAttr "fol_chin_L_004_jnt.wm" "skinCluster77.ma[87]";
connectAttr "fol_chin_R_001_jnt.wm" "skinCluster77.ma[88]";
connectAttr "fol_chin_R_002_jnt.wm" "skinCluster77.ma[89]";
connectAttr "fol_chin_R_003_jnt.wm" "skinCluster77.ma[90]";
connectAttr "fol_chin_R_004_jnt.wm" "skinCluster77.ma[91]";
connectAttr "fol_chinNeck_L_001_jnt.wm" "skinCluster77.ma[92]";
connectAttr "fol_chinNeck_R_001_jnt.wm" "skinCluster77.ma[93]";
connectAttr "fol_throat_C_001_jnt.wm" "skinCluster77.ma[94]";
connectAttr "fol_throat_C_003_jnt.wm" "skinCluster77.ma[95]";
connectAttr "fol_throat_C_002_jnt.wm" "skinCluster77.ma[96]";
connectAttr "fol_chinThroat_C_001_jnt.wm" "skinCluster77.ma[97]";
connectAttr "fol_chinThroat_C_002_jnt.wm" "skinCluster77.ma[98]";
connectAttr "fol_chinThroat_L_001_jnt.wm" "skinCluster77.ma[99]";
connectAttr "fol_chinThroat_L_002_jnt.wm" "skinCluster77.ma[100]";
connectAttr "fol_chinThroat_R_001_jnt.wm" "skinCluster77.ma[101]";
connectAttr "fol_chinThroat_R_002_jnt.wm" "skinCluster77.ma[102]";
connectAttr "fol_clavicleNeck_L_001_jnt.wm" "skinCluster77.ma[103]";
connectAttr "fol_clavicleNeck_L_002_jnt.wm" "skinCluster77.ma[104]";
connectAttr "fol_clavicleNeck_L_003_jnt.wm" "skinCluster77.ma[105]";
connectAttr "fol_clavicleNeck_L_004_jnt.wm" "skinCluster77.ma[106]";
connectAttr "fol_clavicleNeck_L_005_jnt.wm" "skinCluster77.ma[107]";
connectAttr "fol_clavicleNeck_R_001_jnt.wm" "skinCluster77.ma[108]";
connectAttr "fol_clavicleNeck_R_002_jnt.wm" "skinCluster77.ma[109]";
connectAttr "fol_clavicleNeck_R_003_jnt.wm" "skinCluster77.ma[110]";
connectAttr "fol_clavicleNeck_R_004_jnt.wm" "skinCluster77.ma[111]";
connectAttr "fol_clavicleNeck_R_005_jnt.wm" "skinCluster77.ma[112]";
connectAttr "fol_brow_R_003_jnt.liw" "skinCluster77.lw[0]";
connectAttr "fol_brow_R_002_jnt.liw" "skinCluster77.lw[1]";
connectAttr "fol_brow_R_001_jnt.liw" "skinCluster77.lw[2]";
connectAttr "fol_brow_L_003_jnt.liw" "skinCluster77.lw[3]";
connectAttr "fol_brow_L_002_jnt.liw" "skinCluster77.lw[4]";
connectAttr "fol_brow_L_001_jnt.liw" "skinCluster77.lw[5]";
connectAttr "fol_brow_C_001_jnt.liw" "skinCluster77.lw[6]";
connectAttr "fol_browLid_L_001_jnt.liw" "skinCluster77.lw[7]";
connectAttr "fol_browLid_L_002_jnt.liw" "skinCluster77.lw[8]";
connectAttr "fol_browLid_L_003_jnt.liw" "skinCluster77.lw[9]";
connectAttr "fol_browLid_R_001_jnt.liw" "skinCluster77.lw[10]";
connectAttr "fol_browLid_R_002_jnt.liw" "skinCluster77.lw[11]";
connectAttr "fol_browLid_R_003_jnt.liw" "skinCluster77.lw[12]";
connectAttr "fol_forehead_L_002_jnt.liw" "skinCluster77.lw[13]";
connectAttr "fol_forehead_R_002_jnt.liw" "skinCluster77.lw[14]";
connectAttr "fol_forehead_C_002_jnt.liw" "skinCluster77.lw[15]";
connectAttr "fol_forehead_R_001_jnt.liw" "skinCluster77.lw[16]";
connectAttr "fol_forehead_L_001_jnt.liw" "skinCluster77.lw[17]";
connectAttr "fol_forehead_C_001_jnt.liw" "skinCluster77.lw[18]";
connectAttr "fol_eyeFrame_L_001_jnt.liw" "skinCluster77.lw[19]";
connectAttr "fol_eyeFrame_L_002_jnt.liw" "skinCluster77.lw[20]";
connectAttr "fol_eyeFrame_L_003_jnt.liw" "skinCluster77.lw[21]";
connectAttr "fol_eyeFrame_L_004_jnt.liw" "skinCluster77.lw[22]";
connectAttr "fol_eyeFrame_L_005_jnt.liw" "skinCluster77.lw[23]";
connectAttr "fol_eyeFrame_R_001_jnt.liw" "skinCluster77.lw[24]";
connectAttr "fol_eyeFrame_R_002_jnt.liw" "skinCluster77.lw[25]";
connectAttr "fol_eyeFrame_R_003_jnt.liw" "skinCluster77.lw[26]";
connectAttr "fol_eyeFrame_R_004_jnt.liw" "skinCluster77.lw[27]";
connectAttr "fol_eyeFrame_R_005_jnt.liw" "skinCluster77.lw[28]";
connectAttr "fol_bite_L_001_jnt.liw" "skinCluster77.lw[29]";
connectAttr "fol_bite_R_001_jnt.liw" "skinCluster77.lw[30]";
connectAttr "fol_lowlid_L_001_jnt.liw" "skinCluster77.lw[31]";
connectAttr "fol_lowlid_L_002_jnt.liw" "skinCluster77.lw[32]";
connectAttr "fol_lowlid_L_003_jnt.liw" "skinCluster77.lw[33]";
connectAttr "fol_lowlid_R_001_jnt.liw" "skinCluster77.lw[34]";
connectAttr "fol_lowlid_R_002_jnt.liw" "skinCluster77.lw[35]";
connectAttr "fol_lowlid_R_003_jnt.liw" "skinCluster77.lw[36]";
connectAttr "fol_noseRoot_C_001_jnt.liw" "skinCluster77.lw[37]";
connectAttr "fol_noseTip_C_001_jnt.liw" "skinCluster77.lw[38]";
connectAttr "fol_noseBottom_C_001_jnt.liw" "skinCluster77.lw[39]";
connectAttr "fol_noseWing_L_001_jnt.liw" "skinCluster77.lw[40]";
connectAttr "fol_noseWing_L_002_jnt.liw" "skinCluster77.lw[41]";
connectAttr "fol_noseWing_R_001_jnt.liw" "skinCluster77.lw[42]";
connectAttr "fol_noseWing_R_002_jnt.liw" "skinCluster77.lw[43]";
connectAttr "fol_lipChin_C_001_jnt.liw" "skinCluster77.lw[44]";
connectAttr "fol_nosFlo_L_001_jnt.liw" "skinCluster77.lw[45]";
connectAttr "fol_nosFlo_L_002_jnt.liw" "skinCluster77.lw[46]";
connectAttr "fol_nosFlo_L_003_jnt.liw" "skinCluster77.lw[47]";
connectAttr "fol_nosFlo_L_004_jnt.liw" "skinCluster77.lw[48]";
connectAttr "fol_nosFlo_L_005_jnt.liw" "skinCluster77.lw[49]";
connectAttr "fol_lipChin_L_002_jnt.liw" "skinCluster77.lw[50]";
connectAttr "fol_lipChin_L_001_jnt.liw" "skinCluster77.lw[51]";
connectAttr "fol_nosFlo_R_001_jnt.liw" "skinCluster77.lw[52]";
connectAttr "fol_nosFlo_R_002_jnt.liw" "skinCluster77.lw[53]";
connectAttr "fol_nosFlo_R_003_jnt.liw" "skinCluster77.lw[54]";
connectAttr "fol_nosFlo_R_004_jnt.liw" "skinCluster77.lw[55]";
connectAttr "fol_nosFlo_R_005_jnt.liw" "skinCluster77.lw[56]";
connectAttr "fol_lipChin_R_002_jnt.liw" "skinCluster77.lw[57]";
connectAttr "fol_lipChin_R_001_jnt.liw" "skinCluster77.lw[58]";
connectAttr "fol_zyg_L_001_jnt.liw" "skinCluster77.lw[59]";
connectAttr "fol_zyg_L_002_jnt.liw" "skinCluster77.lw[60]";
connectAttr "fol_zyg_L_003_jnt.liw" "skinCluster77.lw[61]";
connectAttr "fol_zyg_R_001_jnt.liw" "skinCluster77.lw[62]";
connectAttr "fol_zyg_R_002_jnt.liw" "skinCluster77.lw[63]";
connectAttr "fol_zyg_R_003_jnt.liw" "skinCluster77.lw[64]";
connectAttr "fol_cheek_L_001_jnt.liw" "skinCluster77.lw[65]";
connectAttr "fol_cheek_L_002_jnt.liw" "skinCluster77.lw[66]";
connectAttr "fol_cheek_L_003_jnt.liw" "skinCluster77.lw[67]";
connectAttr "fol_cheek_R_001_jnt.liw" "skinCluster77.lw[68]";
connectAttr "fol_cheek_R_002_jnt.liw" "skinCluster77.lw[69]";
connectAttr "fol_cheek_R_003_jnt.liw" "skinCluster77.lw[70]";
connectAttr "fol_upLipFrame_C_001_jnt.liw" "skinCluster77.lw[71]";
connectAttr "fol_lowLipFrame_C_001_jnt.liw" "skinCluster77.lw[72]";
connectAttr "fol_upLipFrame_L_001_jnt.liw" "skinCluster77.lw[73]";
connectAttr "fol_upLipFrame_L_002_jnt.liw" "skinCluster77.lw[74]";
connectAttr "fol_mouth_L_001_jnt.liw" "skinCluster77.lw[75]";
connectAttr "fol_lowLipFrame_L_002_jnt.liw" "skinCluster77.lw[76]";
connectAttr "fol_lowLipFrame_L_001_jnt.liw" "skinCluster77.lw[77]";
connectAttr "fol_upLipFrame_R_001_jnt.liw" "skinCluster77.lw[78]";
connectAttr "fol_upLipFrame_R_002_jnt.liw" "skinCluster77.lw[79]";
connectAttr "fol_mouth_R_001_jnt.liw" "skinCluster77.lw[80]";
connectAttr "fol_lowLipFrame_R_002_jnt.liw" "skinCluster77.lw[81]";
connectAttr "fol_lowLipFrame_R_001_jnt.liw" "skinCluster77.lw[82]";
connectAttr "fol_chin_C_001_jnt.liw" "skinCluster77.lw[83]";
connectAttr "fol_chin_L_001_jnt.liw" "skinCluster77.lw[84]";
connectAttr "fol_chin_L_002_jnt.liw" "skinCluster77.lw[85]";
connectAttr "fol_chin_L_003_jnt.liw" "skinCluster77.lw[86]";
connectAttr "fol_chin_L_004_jnt.liw" "skinCluster77.lw[87]";
connectAttr "fol_chin_R_001_jnt.liw" "skinCluster77.lw[88]";
connectAttr "fol_chin_R_002_jnt.liw" "skinCluster77.lw[89]";
connectAttr "fol_chin_R_003_jnt.liw" "skinCluster77.lw[90]";
connectAttr "fol_chin_R_004_jnt.liw" "skinCluster77.lw[91]";
connectAttr "fol_chinNeck_L_001_jnt.liw" "skinCluster77.lw[92]";
connectAttr "fol_chinNeck_R_001_jnt.liw" "skinCluster77.lw[93]";
connectAttr "fol_throat_C_001_jnt.liw" "skinCluster77.lw[94]";
connectAttr "fol_throat_C_003_jnt.liw" "skinCluster77.lw[95]";
connectAttr "fol_throat_C_002_jnt.liw" "skinCluster77.lw[96]";
connectAttr "fol_chinThroat_C_001_jnt.liw" "skinCluster77.lw[97]";
connectAttr "fol_chinThroat_C_002_jnt.liw" "skinCluster77.lw[98]";
connectAttr "fol_chinThroat_L_001_jnt.liw" "skinCluster77.lw[99]";
connectAttr "fol_chinThroat_L_002_jnt.liw" "skinCluster77.lw[100]";
connectAttr "fol_chinThroat_R_001_jnt.liw" "skinCluster77.lw[101]";
connectAttr "fol_chinThroat_R_002_jnt.liw" "skinCluster77.lw[102]";
connectAttr "fol_clavicleNeck_L_001_jnt.liw" "skinCluster77.lw[103]";
connectAttr "fol_clavicleNeck_L_002_jnt.liw" "skinCluster77.lw[104]";
connectAttr "fol_clavicleNeck_L_003_jnt.liw" "skinCluster77.lw[105]";
connectAttr "fol_clavicleNeck_L_004_jnt.liw" "skinCluster77.lw[106]";
connectAttr "fol_clavicleNeck_L_005_jnt.liw" "skinCluster77.lw[107]";
connectAttr "fol_clavicleNeck_R_001_jnt.liw" "skinCluster77.lw[108]";
connectAttr "fol_clavicleNeck_R_002_jnt.liw" "skinCluster77.lw[109]";
connectAttr "fol_clavicleNeck_R_003_jnt.liw" "skinCluster77.lw[110]";
connectAttr "fol_clavicleNeck_R_004_jnt.liw" "skinCluster77.lw[111]";
connectAttr "fol_clavicleNeck_R_005_jnt.liw" "skinCluster77.lw[112]";
connectAttr "fol_brow_R_003_jnt.obcc" "skinCluster77.ifcl[0]";
connectAttr "fol_brow_R_002_jnt.obcc" "skinCluster77.ifcl[1]";
connectAttr "fol_brow_R_001_jnt.obcc" "skinCluster77.ifcl[2]";
connectAttr "fol_brow_L_003_jnt.obcc" "skinCluster77.ifcl[3]";
connectAttr "fol_brow_L_002_jnt.obcc" "skinCluster77.ifcl[4]";
connectAttr "fol_brow_L_001_jnt.obcc" "skinCluster77.ifcl[5]";
connectAttr "fol_brow_C_001_jnt.obcc" "skinCluster77.ifcl[6]";
connectAttr "fol_browLid_L_001_jnt.obcc" "skinCluster77.ifcl[7]";
connectAttr "fol_browLid_L_002_jnt.obcc" "skinCluster77.ifcl[8]";
connectAttr "fol_browLid_L_003_jnt.obcc" "skinCluster77.ifcl[9]";
connectAttr "fol_browLid_R_001_jnt.obcc" "skinCluster77.ifcl[10]";
connectAttr "fol_browLid_R_002_jnt.obcc" "skinCluster77.ifcl[11]";
connectAttr "fol_browLid_R_003_jnt.obcc" "skinCluster77.ifcl[12]";
connectAttr "fol_forehead_L_002_jnt.obcc" "skinCluster77.ifcl[13]";
connectAttr "fol_forehead_R_002_jnt.obcc" "skinCluster77.ifcl[14]";
connectAttr "fol_forehead_C_002_jnt.obcc" "skinCluster77.ifcl[15]";
connectAttr "fol_forehead_R_001_jnt.obcc" "skinCluster77.ifcl[16]";
connectAttr "fol_forehead_L_001_jnt.obcc" "skinCluster77.ifcl[17]";
connectAttr "fol_forehead_C_001_jnt.obcc" "skinCluster77.ifcl[18]";
connectAttr "fol_eyeFrame_L_001_jnt.obcc" "skinCluster77.ifcl[19]";
connectAttr "fol_eyeFrame_L_002_jnt.obcc" "skinCluster77.ifcl[20]";
connectAttr "fol_eyeFrame_L_003_jnt.obcc" "skinCluster77.ifcl[21]";
connectAttr "fol_eyeFrame_L_004_jnt.obcc" "skinCluster77.ifcl[22]";
connectAttr "fol_eyeFrame_L_005_jnt.obcc" "skinCluster77.ifcl[23]";
connectAttr "fol_eyeFrame_R_001_jnt.obcc" "skinCluster77.ifcl[24]";
connectAttr "fol_eyeFrame_R_002_jnt.obcc" "skinCluster77.ifcl[25]";
connectAttr "fol_eyeFrame_R_003_jnt.obcc" "skinCluster77.ifcl[26]";
connectAttr "fol_eyeFrame_R_004_jnt.obcc" "skinCluster77.ifcl[27]";
connectAttr "fol_eyeFrame_R_005_jnt.obcc" "skinCluster77.ifcl[28]";
connectAttr "fol_bite_L_001_jnt.obcc" "skinCluster77.ifcl[29]";
connectAttr "fol_bite_R_001_jnt.obcc" "skinCluster77.ifcl[30]";
connectAttr "fol_lowlid_L_001_jnt.obcc" "skinCluster77.ifcl[31]";
connectAttr "fol_lowlid_L_002_jnt.obcc" "skinCluster77.ifcl[32]";
connectAttr "fol_lowlid_L_003_jnt.obcc" "skinCluster77.ifcl[33]";
connectAttr "fol_lowlid_R_001_jnt.obcc" "skinCluster77.ifcl[34]";
connectAttr "fol_lowlid_R_002_jnt.obcc" "skinCluster77.ifcl[35]";
connectAttr "fol_lowlid_R_003_jnt.obcc" "skinCluster77.ifcl[36]";
connectAttr "fol_noseRoot_C_001_jnt.obcc" "skinCluster77.ifcl[37]";
connectAttr "fol_noseTip_C_001_jnt.obcc" "skinCluster77.ifcl[38]";
connectAttr "fol_noseBottom_C_001_jnt.obcc" "skinCluster77.ifcl[39]";
connectAttr "fol_noseWing_L_001_jnt.obcc" "skinCluster77.ifcl[40]";
connectAttr "fol_noseWing_L_002_jnt.obcc" "skinCluster77.ifcl[41]";
connectAttr "fol_noseWing_R_001_jnt.obcc" "skinCluster77.ifcl[42]";
connectAttr "fol_noseWing_R_002_jnt.obcc" "skinCluster77.ifcl[43]";
connectAttr "fol_lipChin_C_001_jnt.obcc" "skinCluster77.ifcl[44]";
connectAttr "fol_nosFlo_L_001_jnt.obcc" "skinCluster77.ifcl[45]";
connectAttr "fol_nosFlo_L_002_jnt.obcc" "skinCluster77.ifcl[46]";
connectAttr "fol_nosFlo_L_003_jnt.obcc" "skinCluster77.ifcl[47]";
connectAttr "fol_nosFlo_L_004_jnt.obcc" "skinCluster77.ifcl[48]";
connectAttr "fol_nosFlo_L_005_jnt.obcc" "skinCluster77.ifcl[49]";
connectAttr "fol_lipChin_L_002_jnt.obcc" "skinCluster77.ifcl[50]";
connectAttr "fol_lipChin_L_001_jnt.obcc" "skinCluster77.ifcl[51]";
connectAttr "fol_nosFlo_R_001_jnt.obcc" "skinCluster77.ifcl[52]";
connectAttr "fol_nosFlo_R_002_jnt.obcc" "skinCluster77.ifcl[53]";
connectAttr "fol_nosFlo_R_003_jnt.obcc" "skinCluster77.ifcl[54]";
connectAttr "fol_nosFlo_R_004_jnt.obcc" "skinCluster77.ifcl[55]";
connectAttr "fol_nosFlo_R_005_jnt.obcc" "skinCluster77.ifcl[56]";
connectAttr "fol_lipChin_R_002_jnt.obcc" "skinCluster77.ifcl[57]";
connectAttr "fol_lipChin_R_001_jnt.obcc" "skinCluster77.ifcl[58]";
connectAttr "fol_zyg_L_001_jnt.obcc" "skinCluster77.ifcl[59]";
connectAttr "fol_zyg_L_002_jnt.obcc" "skinCluster77.ifcl[60]";
connectAttr "fol_zyg_L_003_jnt.obcc" "skinCluster77.ifcl[61]";
connectAttr "fol_zyg_R_001_jnt.obcc" "skinCluster77.ifcl[62]";
connectAttr "fol_zyg_R_002_jnt.obcc" "skinCluster77.ifcl[63]";
connectAttr "fol_zyg_R_003_jnt.obcc" "skinCluster77.ifcl[64]";
connectAttr "fol_cheek_L_001_jnt.obcc" "skinCluster77.ifcl[65]";
connectAttr "fol_cheek_L_002_jnt.obcc" "skinCluster77.ifcl[66]";
connectAttr "fol_cheek_L_003_jnt.obcc" "skinCluster77.ifcl[67]";
connectAttr "fol_cheek_R_001_jnt.obcc" "skinCluster77.ifcl[68]";
connectAttr "fol_cheek_R_002_jnt.obcc" "skinCluster77.ifcl[69]";
connectAttr "fol_cheek_R_003_jnt.obcc" "skinCluster77.ifcl[70]";
connectAttr "fol_upLipFrame_C_001_jnt.obcc" "skinCluster77.ifcl[71]";
connectAttr "fol_lowLipFrame_C_001_jnt.obcc" "skinCluster77.ifcl[72]";
connectAttr "fol_upLipFrame_L_001_jnt.obcc" "skinCluster77.ifcl[73]";
connectAttr "fol_upLipFrame_L_002_jnt.obcc" "skinCluster77.ifcl[74]";
connectAttr "fol_mouth_L_001_jnt.obcc" "skinCluster77.ifcl[75]";
connectAttr "fol_lowLipFrame_L_002_jnt.obcc" "skinCluster77.ifcl[76]";
connectAttr "fol_lowLipFrame_L_001_jnt.obcc" "skinCluster77.ifcl[77]";
connectAttr "fol_upLipFrame_R_001_jnt.obcc" "skinCluster77.ifcl[78]";
connectAttr "fol_upLipFrame_R_002_jnt.obcc" "skinCluster77.ifcl[79]";
connectAttr "fol_mouth_R_001_jnt.obcc" "skinCluster77.ifcl[80]";
connectAttr "fol_lowLipFrame_R_002_jnt.obcc" "skinCluster77.ifcl[81]";
connectAttr "fol_lowLipFrame_R_001_jnt.obcc" "skinCluster77.ifcl[82]";
connectAttr "fol_chin_C_001_jnt.obcc" "skinCluster77.ifcl[83]";
connectAttr "fol_chin_L_001_jnt.obcc" "skinCluster77.ifcl[84]";
connectAttr "fol_chin_L_002_jnt.obcc" "skinCluster77.ifcl[85]";
connectAttr "fol_chin_L_003_jnt.obcc" "skinCluster77.ifcl[86]";
connectAttr "fol_chin_L_004_jnt.obcc" "skinCluster77.ifcl[87]";
connectAttr "fol_chin_R_001_jnt.obcc" "skinCluster77.ifcl[88]";
connectAttr "fol_chin_R_002_jnt.obcc" "skinCluster77.ifcl[89]";
connectAttr "fol_chin_R_003_jnt.obcc" "skinCluster77.ifcl[90]";
connectAttr "fol_chin_R_004_jnt.obcc" "skinCluster77.ifcl[91]";
connectAttr "fol_chinNeck_L_001_jnt.obcc" "skinCluster77.ifcl[92]";
connectAttr "fol_chinNeck_R_001_jnt.obcc" "skinCluster77.ifcl[93]";
connectAttr "fol_throat_C_001_jnt.obcc" "skinCluster77.ifcl[94]";
connectAttr "fol_throat_C_003_jnt.obcc" "skinCluster77.ifcl[95]";
connectAttr "fol_throat_C_002_jnt.obcc" "skinCluster77.ifcl[96]";
connectAttr "fol_chinThroat_C_001_jnt.obcc" "skinCluster77.ifcl[97]";
connectAttr "fol_chinThroat_C_002_jnt.obcc" "skinCluster77.ifcl[98]";
connectAttr "fol_chinThroat_L_001_jnt.obcc" "skinCluster77.ifcl[99]";
connectAttr "fol_chinThroat_L_002_jnt.obcc" "skinCluster77.ifcl[100]";
connectAttr "fol_chinThroat_R_001_jnt.obcc" "skinCluster77.ifcl[101]";
connectAttr "fol_chinThroat_R_002_jnt.obcc" "skinCluster77.ifcl[102]";
connectAttr "fol_clavicleNeck_L_001_jnt.obcc" "skinCluster77.ifcl[103]";
connectAttr "fol_clavicleNeck_L_002_jnt.obcc" "skinCluster77.ifcl[104]";
connectAttr "fol_clavicleNeck_L_003_jnt.obcc" "skinCluster77.ifcl[105]";
connectAttr "fol_clavicleNeck_L_004_jnt.obcc" "skinCluster77.ifcl[106]";
connectAttr "fol_clavicleNeck_L_005_jnt.obcc" "skinCluster77.ifcl[107]";
connectAttr "fol_clavicleNeck_R_001_jnt.obcc" "skinCluster77.ifcl[108]";
connectAttr "fol_clavicleNeck_R_002_jnt.obcc" "skinCluster77.ifcl[109]";
connectAttr "fol_clavicleNeck_R_003_jnt.obcc" "skinCluster77.ifcl[110]";
connectAttr "fol_clavicleNeck_R_004_jnt.obcc" "skinCluster77.ifcl[111]";
connectAttr "fol_clavicleNeck_R_005_jnt.obcc" "skinCluster77.ifcl[112]";
connectAttr "fol_zyg_R_003_jnt.msg" "skinCluster77.ptt";
connectAttr "lambert17SG.msg" "materialInfo50.sg";
connectAttr "lambert17.msg" "materialInfo50.m";
connectAttr "lambert17.oc" "lambert17SG.ss";
connectAttr "base_bs_meshShape.iog" "lambert17SG.dsm" -na;
connectAttr "lambert18SG.msg" "materialInfo51.sg";
connectAttr "lambert18.msg" "materialInfo51.m";
connectAttr "lambert18.oc" "lambert18SG.ss";
connectAttr "fol_base_meshShape.iog" "lambert18SG.dsm" -na;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert3SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert4SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert5SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert6SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert7SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert8SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert9SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert10SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert11SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert13SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert14SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert15SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert16SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert17SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "lambert18SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert3SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert4SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert5SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert6SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert7SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert8SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert9SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert10SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert11SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert13SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert14SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert15SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert16SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert17SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "lambert18SG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "lambert3SG.pa" ":renderPartition.st" -na;
connectAttr "lambert4SG.pa" ":renderPartition.st" -na;
connectAttr "lambert5SG.pa" ":renderPartition.st" -na;
connectAttr "lambert6SG.pa" ":renderPartition.st" -na;
connectAttr "lambert7SG.pa" ":renderPartition.st" -na;
connectAttr "lambert8SG.pa" ":renderPartition.st" -na;
connectAttr "lambert9SG.pa" ":renderPartition.st" -na;
connectAttr "lambert10SG.pa" ":renderPartition.st" -na;
connectAttr "lambert11SG.pa" ":renderPartition.st" -na;
connectAttr "lambert13SG.pa" ":renderPartition.st" -na;
connectAttr "lambert14SG.pa" ":renderPartition.st" -na;
connectAttr "lambert15SG.pa" ":renderPartition.st" -na;
connectAttr "lambert16SG.pa" ":renderPartition.st" -na;
connectAttr "lambert17SG.pa" ":renderPartition.st" -na;
connectAttr "lambert18SG.pa" ":renderPartition.st" -na;
connectAttr "lambert3.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert4.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert5.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert6.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert7.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert8.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert9.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert10.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert11.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert13.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert14.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert15.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert16.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert17.msg" ":defaultShaderList1.s" -na;
connectAttr "lambert18.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of facial_mask_test01.ma
