//Maya ASCII 2018ff09 scene
//Name: facial_cage.ma
//Last modified: Wed, Jan 15, 2020 10:51:00 AM
//Codeset: 932
requires maya "2018ff09";
requires "stereoCamera" "10.0";
requires "mtoa" "3.1.1.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811122215-49253d42f6";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -n "cage_grp";
	rename -uid "621566F1-454F-54C8-D9AC-2A94299A341B";
createNode transform -n "cage" -p "cage_grp";
	rename -uid "9EA4EE16-47E1-33AE-AD0D-9EA088C4E601";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 145.95659319869728 6.8355865673182565 ;
	setAttr ".sp" -type "double3" 0 145.95659319869728 6.8355865673182565 ;
createNode mesh -n "cageShape" -p "cage";
	rename -uid "F15063B7-40E1-92B6-ECA8-C4BCCE8A7DD0";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.47537184902057561 0.11232318729162223 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "polySurfaceShape1" -p "cage";
	rename -uid "D59174C2-4E8D-EAA0-84CE-91AB025B6354";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0 1 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 23 ".uvst[0].uvsp[0:22]" -type "float2" 0 0 1 0 0 1 1 1 0
		 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 0.27113798 0 0.56024796
		 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 11 ".vt[0:10]"  -1.847744e-06 0.65678549 -0.10113144 1.0842042e-13 0.2358316 0.4685733
		 0.22729973 0.20466068 -1.033798218 0.082712136 0.22776389 0.46327594 0.46131015 -0.063940451 -0.96756065
		 0.31670335 0.1047662 0.48979139 0.45173338 -0.098891631 -0.88509595 0.42621356 0.0022853911 0.52658975
		 1.0842042e-13 0.2105248 0.46382371 0.091066204 0.19728048 0.45405275 0.31259158 0.069874495 0.47978696;
	setAttr -s 17 ".ed[0:16]"  0 1 0 0 2 0 1 3 0 2 3 0 0 3 0 2 4 0 3 5 0
		 4 5 1 4 6 0 5 7 0 6 7 0 1 8 0 3 9 0 8 9 0 5 10 0 9 10 0 10 7 0;
	setAttr -s 7 -ch 25 ".fc[0:6]" -type "polyFaces" 
		f 3 4 -4 -2
		mu 0 3 0 3 2
		f 3 0 2 -5
		mu 0 3 0 1 3
		f 4 3 6 -8 -6
		mu 0 4 4 5 6 7
		f 4 7 9 -11 -9
		mu 0 4 8 9 10 11
		f 4 -3 11 13 -13
		mu 0 4 12 13 14 15
		f 4 -7 12 15 -15
		mu 0 4 16 17 18 19
		f 3 14 16 -10
		mu 0 3 20 21 22;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode mesh -n "cageShapeOrig" -p "cage";
	rename -uid "3E002421-4721-0525-E6C9-0DBB36573282";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 105 ".uvst[0].uvsp[0:104]" -type "float2" 0 1 1 1 0 0 1 0 1
		 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 1 0.80786288
		 1 0.29451859 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0 1 0 0
		 1 0 1 1 0 1 0 0 1 0 1 0 1 1 1 0 8.1290409e-06 1.4386046e-16 0 8.1290409e-06 1 -1.3161918e-12
		 2.2338956e-05 2.2338956e-05 0 1 1 0 1 1 0 0 1 0 1 1 0 1 0 1 1 0 1 1 0 0 1 1 0 1 0
		 0 1 0 1 0.29451859 0 1 1 0.80786288 1 1 1 0 0 0 0 1 1 0 1 1 0 1 1 0 1 1 0 0 0 0 1
		 0 1 1 0 1 0 0 1 0 1 1 0 0 1 0 1 1 0 1 0 1 1 0 1 1 0 0 1 0 0 0 0 0 0 8.1290409e-06
		 2.2338956e-05 2.2338956e-05 1 1 0 1 1 -1.3161918e-12 1 0;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 51 ".pt";
	setAttr ".pt[0]" -type "float3" 0.6420148 149.66766 8.8244486 ;
	setAttr ".pt[1]" -type "float3" 0.23362286 143.92058 7.1649985 ;
	setAttr ".pt[2]" -type "float3" 1.3029841 149.72816 7.7208385 ;
	setAttr ".pt[3]" -type "float3" 0.89453793 143.96291 6.6641021 ;
	setAttr ".pt[4]" -type "float3" 1.2759342 149.45387 7.4910197 ;
	setAttr ".pt[5]" -type "float3" 1.2038528 143.94174 6.2295189 ;
	setAttr ".pt[6]" -type "float3" 1.7573417 149.06691 7.2226071 ;
	setAttr ".pt[7]" -type "float3" 2.0299575 144.66652 6.0025063 ;
	setAttr ".pt[8]" -type "float3" 1.6585463 142.52057 4.164052 ;
	setAttr ".pt[9]" -type "float3" 2.8946698 145.46609 5.0061803 ;
	setAttr ".pt[10]" -type "float3" -1.9447739e-16 143.93855 7.0984726 ;
	setAttr ".pt[11]" -type "float3" 0.0001308119 140.8226 5.4384289 ;
	setAttr ".pt[12]" -type "float3" 0.25721917 143.99141 7.0592966 ;
	setAttr ".pt[13]" -type "float3" 0.88292426 144.04182 6.5424533 ;
	setAttr ".pt[14]" -type "float3" 2.4654064 149.07471 7.0043263 ;
	setAttr ".pt[15]" -type "float3" 2.9670386 149.18347 6.6985126 ;
	setAttr ".pt[16]" -type "float3" 3.2282996 149.5648 6.5288796 ;
	setAttr ".pt[17]" -type "float3" 2.4956055 150.57607 8.4165897 ;
	setAttr ".pt[18]" -type "float3" 1.5881416 150.04576 7.9291477 ;
	setAttr ".pt[19]" -type "float3" 3.8679729 151.63025 6.6796522 ;
	setAttr ".pt[20]" -type "float3" 2.7832742 150.28143 7.5487232 ;
	setAttr ".pt[21]" -type "float3" 3.353404 150.2439 6.9173985 ;
	setAttr ".pt[22]" -type "float3" 3.3426633 149.83557 6.5598531 ;
	setAttr ".pt[23]" -type "float3" 3.414012 150.08105 6.6884189 ;
	setAttr ".pt[24]" -type "float3" 1.3139746e-16 145.57619 9.4631023 ;
	setAttr ".pt[25]" -type "float3" 1.2384835e-08 143.89087 7.1896281 ;
	setAttr ".pt[26]" -type "float3" -2.7694745e-16 145.57614 9.4630642 ;
	setAttr ".pt[27]" -type "float3" -0.6420148 149.66766 8.8244486 ;
	setAttr ".pt[28]" -type "float3" -0.23362286 143.92058 7.1649985 ;
	setAttr ".pt[29]" -type "float3" -1.3029841 149.72816 7.7208385 ;
	setAttr ".pt[30]" -type "float3" -0.89453793 143.96291 6.6641021 ;
	setAttr ".pt[31]" -type "float3" -1.2759342 149.45387 7.4910197 ;
	setAttr ".pt[32]" -type "float3" -1.2038528 143.94174 6.2295189 ;
	setAttr ".pt[33]" -type "float3" -1.7573417 149.06691 7.2226071 ;
	setAttr ".pt[34]" -type "float3" -2.0299575 144.66652 6.0025063 ;
	setAttr ".pt[35]" -type "float3" -1.6585463 142.52057 4.164052 ;
	setAttr ".pt[36]" -type "float3" -2.8946698 145.46609 5.0061803 ;
	setAttr ".pt[37]" -type "float3" -0.0001308119 140.8226 5.4384289 ;
	setAttr ".pt[38]" -type "float3" -0.25721917 143.99141 7.0592966 ;
	setAttr ".pt[39]" -type "float3" -0.88292426 144.04182 6.5424533 ;
	setAttr ".pt[40]" -type "float3" -2.4654064 149.07471 7.0043263 ;
	setAttr ".pt[41]" -type "float3" -2.9670386 149.18347 6.6985126 ;
	setAttr ".pt[42]" -type "float3" -3.2282996 149.5648 6.5288796 ;
	setAttr ".pt[43]" -type "float3" -2.4956055 150.57607 8.4165897 ;
	setAttr ".pt[44]" -type "float3" -1.5881416 150.04576 7.9291477 ;
	setAttr ".pt[45]" -type "float3" -3.8679729 151.63025 6.6796522 ;
	setAttr ".pt[46]" -type "float3" -2.7832742 150.28143 7.5487232 ;
	setAttr ".pt[47]" -type "float3" -3.353404 150.2439 6.9173985 ;
	setAttr ".pt[48]" -type "float3" -3.3426633 149.83557 6.5598531 ;
	setAttr ".pt[49]" -type "float3" -3.414012 150.08105 6.6884189 ;
	setAttr ".pt[55]" -type "float3" -3.7252903e-09 4.6566129e-10 3.5855919e-08 ;
	setAttr -s 50 ".vt[0:49]"  0.22729973 0.20466068 -1.033798218 0.082712136 0.22776321 0.46327591
		 0.46131015 -0.063940018 -0.96756363 0.31670335 0.10476616 0.48978043 0.45173338 -0.098891705 -0.8850975
		 0.42621356 0.0022857487 0.5266304 0.62217152 -0.13484022 -0.77283478 0.71868873 -0.10506448 0.36973953
		 0.58719385 -0.38819179 1.017887115 1.024832606 -0.40203843 0.25121307 -6.8853025e-17 0.21052435 0.46384048
		 4.6312809e-05 0.041047722 1.33113098 0.091066204 0.19728044 0.45405197 0.31259164 0.069874436 0.47978592
		 0.87285566 -0.18766221 -0.75873947 1.05045414 -0.26882014 -0.7624054 1.14295137 -0.33731648 -0.84128189
		 0.88354737 0.040590554 -1.22141647 0.56226766 -0.037304372 -1.058822632 1.36942208 -0.452288 -1.34672165
		 0.98539394 -0.14560518 -1.087413788 1.18724346 -0.29398236 -1.032253265 1.1834408 -0.34970507 -0.90835953
		 1.20870113 -0.33688483 -0.97652817 4.6520121e-17 0.65678227 -0.10111237 3.7252899e-09 0.23583165 0.46858597
		 -9.8050833e-17 0.65677679 -0.10109711 -0.22729975 0.20466068 -1.033798099 -0.082712136 0.22776321 0.46327591
		 -0.46131015 -0.063940018 -0.96756363 -0.31670335 0.10476616 0.48978043 -0.45173338 -0.098891705 -0.8850975
		 -0.42621356 0.0022857487 0.5266304 -0.62217152 -0.13484022 -0.77283478 -0.71868873 -0.10506448 0.36973953
		 -0.58719385 -0.38819179 1.017887115 -1.024832606 -0.40203843 0.25121307 -4.6312809e-05 0.041047722 1.33113098
		 -0.091066204 0.19728044 0.45405197 -0.31259164 0.069874436 0.47978592 -0.87285566 -0.18766221 -0.75873947
		 -1.05045414 -0.26882014 -0.7624054 -1.14295137 -0.33731648 -0.84128189 -0.88354737 0.040590554 -1.22141647
		 -0.56226766 -0.037304372 -1.058822632 -1.36942208 -0.452288 -1.34672165 -0.98539394 -0.14560518 -1.087413788
		 -1.18724346 -0.29398236 -1.032253265 -1.1834408 -0.34970507 -0.90835953 -1.20870113 -0.33688483 -0.97652817;
	setAttr -s 103 ".ed[0:102]"  0 1 0 0 2 1 1 3 0 2 3 1 2 4 0 3 5 0 4 5 1
		 4 6 0 5 7 1 6 7 1 5 8 1 7 9 0 8 9 0 5 13 0 8 11 0 10 11 0 12 10 0 12 11 0 13 12 0
		 13 8 0 13 11 0 7 8 0 2 1 0 6 14 0 14 9 1 14 15 0 9 16 0 15 16 0 15 9 0 0 17 0 2 18 0
		 17 18 0 18 0 0 17 19 0 17 20 0 19 21 1 20 21 0 19 22 1 21 23 0 22 23 0 20 19 0 23 19 0
		 19 9 0 22 16 0 22 9 0 14 7 0 6 5 0 24 0 0 25 1 0 26 1 0 26 24 0 25 26 1 29 28 0 28 30 0
		 29 30 1 30 32 0 31 32 1 29 31 0 33 32 0 32 34 1 33 34 1 34 35 0 35 36 0 34 36 0 32 35 1
		 32 39 0 39 35 0 38 37 0 38 10 0 10 37 0 39 37 0 35 37 0 39 38 0 27 28 0 27 29 1 40 34 0
		 40 36 1 41 36 0 36 42 0 41 42 0 40 41 0 29 44 0 44 27 0 43 44 0 27 43 0 43 45 0 43 46 0
		 46 45 0 45 47 1 47 49 0 49 45 0 46 47 0 48 49 0 45 48 1 48 36 0 45 36 0 48 42 0 33 40 0
		 31 33 0 26 28 0 24 27 0 25 28 0 27 0 0;
	setAttr -s 51 -ch 157 ".fc[0:50]" -type "polyFaces" 
		f 3 22 2 -4
		mu 0 3 5 3 4
		f 4 3 5 -7 -5
		mu 0 4 6 7 8 9
		f 3 46 8 -10
		mu 0 3 13 11 12
		f 3 21 12 -12
		mu 0 3 14 16 17
		f 3 -11 13 19
		mu 0 3 18 19 23
		f 3 -18 16 15
		mu 0 3 21 22 20
		f 3 -20 20 -15
		mu 0 3 18 23 21
		f 3 -21 18 17
		mu 0 3 21 23 22
		f 3 -9 10 -22
		mu 0 3 14 15 16
		f 3 0 -23 -2
		mu 0 3 2 3 5
		f 3 45 11 -25
		mu 0 3 27 25 26
		f 3 28 26 -28
		mu 0 3 31 29 30
		f 3 24 -29 -26
		mu 0 3 28 29 31
		f 3 1 30 32
		mu 0 3 32 33 34
		f 3 -33 -32 -30
		mu 0 3 32 34 35
		f 3 -34 34 40
		mu 0 3 36 37 38
		f 3 35 38 41
		mu 0 3 40 41 42
		f 3 -41 36 -36
		mu 0 3 36 38 39
		f 3 -42 -40 -38
		mu 0 3 40 42 43
		f 3 44 -43 37
		mu 0 3 45 47 44
		f 3 -27 -45 43
		mu 0 3 46 47 45
		f 3 9 -46 -24
		mu 0 3 24 25 27
		f 3 6 -47 -8
		mu 0 3 10 11 13
		f 4 -51 49 -1 -48
		mu 0 4 50 52 1 0
		f 3 -52 48 -50
		mu 0 3 52 51 1
		f 3 54 -54 -53
		mu 0 3 53 55 54
		f 4 57 56 -56 -55
		mu 0 4 56 59 58 57
		f 3 60 -60 -59
		mu 0 3 60 62 61
		f 3 63 -63 -62
		mu 0 3 63 65 64
		f 3 -67 -66 64
		mu 0 3 66 68 67
		f 3 -70 -69 67
		mu 0 3 69 71 70
		f 3 71 -71 66
		mu 0 3 66 69 68
		f 3 -68 -73 70
		mu 0 3 69 70 68
		f 3 61 -65 59
		mu 0 3 63 64 72
		f 3 74 52 -74
		mu 0 3 73 53 54
		f 3 76 -64 -76
		mu 0 3 74 76 75
		f 3 79 -79 -78
		mu 0 3 77 79 78
		f 3 80 77 -77
		mu 0 3 80 77 78
		f 3 -83 -82 -75
		mu 0 3 81 83 82
		f 3 84 83 82
		mu 0 3 81 84 83
		f 3 -88 -87 85
		mu 0 3 85 87 86
		f 3 -91 -90 -89
		mu 0 3 88 90 89
		f 3 88 -92 87
		mu 0 3 85 91 87
		f 3 93 92 90
		mu 0 3 88 92 90
		f 3 -94 95 -95
		mu 0 3 93 95 94
		f 3 -97 94 78
		mu 0 3 96 93 94
		f 3 97 75 -61
		mu 0 3 97 74 75
		f 3 98 58 -57
		mu 0 3 98 60 61
		f 4 100 73 -100 50
		mu 0 4 99 102 101 100
		f 3 99 -102 51
		mu 0 3 100 101 103
		f 3 -103 -101 47
		mu 0 3 48 104 49;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode joint -n "cage_head" -p "cage_grp";
	rename -uid "03BD7568-4C2A-22AB-7C88-EBAF55A0814C";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 4.1465707927817712e-13 145.15697887486601 0.14704308164551205 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.1465707927817712e-13 145.15697887486601 0.14704308164551205 1;
	setAttr ".ds" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "head";
	setAttr -k on ".liw";
createNode joint -n "cage_L_D_eye_top" -p "cage_head";
	rename -uid "D9B6F449-405A-287D-03F4-EEAEF8115BA9";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 4.5406475067134524 4.7929265206418279 5.7380987678723114 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.5406475067138672 149.94990539550784 5.8851418495178232 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_D";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_chin" -p "cage_head";
	rename -uid "D3BE91B5-4E7F-1C94-1F7C-7B8C36CECE13";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.00017713675292186938 -4.2933314139284562 6.6225167785839822 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.00017713675333652645 140.86364746093756 6.769559860229494 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "chin";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_nose_top" -p "cage_head";
	rename -uid "C6FE8501-4C17-68BC-E1DE-DD91EDDB0679";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -7.0771529462220132e-06 1.0761143868527654 9.2149650131420877 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -7.0771525315649342e-06 146.23309326171878 9.3620080947875994 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "nose_top";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_C_eyebrow" -p "cage_head";
	rename -uid "4241B7E0-4BB5-734B-38B6-DF95157A6078";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 5.2373948097224856 6.0209691231808904 5.1858874832348594 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.2373948097229004 151.1779479980469 5.3329305648803711 1;
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_A_eyebrow" -p "cage_head";
	rename -uid "3370D2B3-4327-3DFF-72A6-90B0F1842B3B";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".t" -type "double3" 0.86931443214375037 4.7153508370480779 7.6436072860913074 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.86931443214416504 149.87232971191409 7.7906503677368191 1;
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_B_cheek" -p "cage_head";
	rename -uid "8B292973-4E2D-A0E7-AC62-61B13EAD8B71";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 3.9195022583003665 -0.092861443225331186 5.1103564773754844 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.9195022583007813 145.06411743164068 5.2573995590209961 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "cheek_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_B_eye_top" -p "cage_head";
	rename -uid "BF397DFF-4D1D-3666-227B-EEB9C9679272";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 2.1504092216487551 4.8514744942746404 6.7232834373669403 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.1504092216491699 150.00845336914065 6.8703265190124521 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_B_eyebrow" -p "cage_head";
	rename -uid "3E2B9073-46F3-73FF-CC81-61BD1115BEAC";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 3.379152297973218 5.4596745675168563 7.0481297050671348 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.3791522979736328 150.61665344238287 7.1951727867126465 1;
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_A_cheek" -p "cage_head";
	rename -uid "FB57BE11-4093-C1E6-E369-3AA1809FC9E8";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 2.7486462593074465 -0.59547069615507553 6.2252093826489219 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.7486462593078613 144.56150817871094 6.3722524642944336 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "cheek_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_C_cheek" -p "cage_head";
	rename -uid "FFB2E980-4E41-4845-6001-9E879B19EDFE";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 2.2457401752467776 -3.0246088797487971 5.0348960434155252 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.2457401752471924 142.13236999511722 5.1819391250610369 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "cheek_C";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_C_eye_top" -p "cage_head";
	rename -uid "B6758806-4EA1-9878-200C-6484C7620E2B";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 3.7686681747432376 4.9788090890012313 6.314262536640622 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.7686681747436523 150.13578796386724 6.4613056182861337 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_C";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_A_eye_top" -p "cage_head";
	rename -uid "FA04E45F-4231-D8F0-A965-68AC392AAAC8";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 1.7642942667003301 4.507236213024612 6.6062294517712363 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7642942667007446 149.66421508789063 6.753272533416748 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_D_eye_bottom" -p "cage_head";
	rename -uid "C6AB36DB-4A46-DAC3-D4AC-5F94A559AAEB";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 4.0174927711482669 3.7576634591183904 5.7890640770153761 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.0174927711486816 148.9146423339844 5.9361071586608878 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_D";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_E_eye_top" -p "cage_head";
	rename -uid "ECF47C6A-4C96-A9FC-5EC7-ADABACE6EE31";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 4.622713088988843 4.5871922677121404 5.5648480926708954 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.6227130889892578 149.74417114257815 5.7118911743164071 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_E";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_B_cheek" -p "cage_head";
	rename -uid "A9E428DB-4C14-E348-12DC-B8A4D5D6AFF9";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -3.9194300174717283 -0.092327385608172108 5.1103097473339822 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.9194300174713135 145.06465148925784 5.257352828979494 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "cheek_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_A_cheek" -p "cage_head";
	rename -uid "E01373DA-481C-B863-F473-6B9037BBFA62";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -2.7486045360569333 -0.59493663853785961 6.2251497780041465 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.7486045360565186 144.56204223632815 6.3721928596496582 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "cheek_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_F_eye_top" -p "cage_head";
	rename -uid "D6EE6B0B-498D-C51C-86A7-2D8E1DCBDE61";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 4.5261039733882571 4.3288762276730495 5.5044485603527775 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.5261039733886719 149.48585510253906 5.6514916419982892 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_F";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_B_eye_bottom" -p "cage_head";
	rename -uid "3926F08B-44BE-B974-B02B-D3B3BB58ADD2";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 2.3795132637019778 3.7751042550168279 6.3027297531323194 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 2.3795132637023926 148.93208312988284 6.4497728347778311 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_A_eye_bottom" -p "cage_head";
	rename -uid "D1327400-4A94-97E1-5F46-799A2B9BAD82";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 1.7276675701137212 4.1980015938840438 6.4588791404919421 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.7276675701141357 149.35498046875006 6.6059222221374538 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_C_eye_bottom" -p "cage_head";
	rename -uid "ADB5F360-4FE6-9366-BFB3-E3AA117CBAE9";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 3.3382620811458255 3.7301366036496404 6.0985452209667939 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.3382620811462402 148.88711547851565 6.2455883026123056 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_C";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_E_eye_bottom" -p "cage_head";
	rename -uid "E96C7882-4318-D95B-07B1-6397E68B6FC9";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 4.3712511062617923 4.0705144112667995 5.5405575309948709 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.371251106262207 149.22749328613281 5.6876006126403826 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_E";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_B_eye_top" -p "cage_head";
	rename -uid "AA4B6A72-4BEC-3E87-DA3F-D8BFE7F46A40";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -2.1503961086277341 4.8510319893918279 6.723770288105464 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.1503961086273193 150.00801086425784 6.8708133697509757 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_A_eyebrow" -p "cage_head";
	rename -uid "F2C98321-49D5-AE3D-F157-67A159D9DF87";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.86931216716807824 4.7153508370480779 7.6436072860913074 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.86931216716766357 149.87232971191409 7.7906503677368191 1;
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_B_eyebrow" -p "cage_head";
	rename -uid "0C14BD32-4C02-F10E-333F-DC858412B3BA";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -3.3791527748112058 5.4596745675168563 7.0481297050671348 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.379152774810791 150.61665344238287 7.1951727867126465 1;
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_C_eyebrow" -p "cage_head";
	rename -uid "C5670F54-423B-E9DD-6C36-1EBC6CDD338C";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -5.2373924255375242 6.0209691231808904 5.1858874832348594 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -5.2373924255371094 151.1779479980469 5.3329305648803711 1;
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_A_eye_top" -p "cage_head";
	rename -uid "B5604DDA-4499-808D-C0F1-04A17B6B9154";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -1.7643244266514155 4.5070988839230779 6.6062966858105439 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.764324426651001 149.66407775878909 6.7533397674560556 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_E_eye_top" -p "cage_head";
	rename -uid "B20BFE43-4333-1272-FDD8-B3ADBC16B8A6";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -4.6227979660038327 4.5871464913449813 5.5650016342358368 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.622797966003418 149.74412536621099 5.7120447158813485 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_E";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_C_cheek" -p "cage_head";
	rename -uid "5C191D6F-4B88-131F-1695-3C96677DF7E1";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -2.24574208259624 -3.0246088797487971 5.0348979507641571 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.2457420825958252 142.13236999511722 5.1819410324096689 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "cheek_C";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_C_eye_top" -p "cage_head";
	rename -uid "06BFD8A8-4495-7836-1AA5-66A4B81F7A8A";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -3.7686965465549802 4.9786870186887313 6.3143269096569794 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.7686965465545654 150.13566589355474 6.4613699913024911 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_C";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_D_eye_top" -p "cage_head";
	rename -uid "62AFCB02-4CCE-6EF7-24FF-949435DEB1D4";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -4.540626525879321 4.792957038219896 5.7380591903881788 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.5406265258789063 149.94993591308591 5.8851022720336905 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_D";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_B_eye_bottom" -p "cage_head";
	rename -uid "142C8416-4483-0E22-59C0-329AEBD32F39";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -2.379512310028491 3.7753636544308904 6.3027364288525369 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -2.3795123100280762 148.9323425292969 6.4497795104980487 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_A_eye_bottom" -p "cage_head";
	rename -uid "B0748AF4-41AA-5233-100B-86A087ECBA24";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -1.72773134708446 4.198001593883987 6.4588715110974082 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.7277313470840454 149.35498046875 6.6059145927429199 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_C_eye_bottom" -p "cage_head";
	rename -uid "6522F565-444B-31B5-C78A-89BE9564AC28";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -3.3382802009586667 3.730716437633987 6.0985948120312479 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -3.338280200958252 148.8876953125 6.2456378936767596 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_C";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_D_eye_bottom" -p "cage_head";
	rename -uid "89BB7DA8-469C-E31B-7B80-68A263419F4D";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -4.0180191993717527 3.7582127755246404 5.7901760612683075 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.0180191993713379 148.91519165039065 5.9372191429138192 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_D";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_E_eye_bottom" -p "cage_head";
	rename -uid "31F07F67-4838-C495-504F-ACB0FE3AD648";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -4.3723621368412351 4.0704838936887313 5.5427304779248034 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.3723621368408203 149.22746276855474 5.6897735595703152 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_bottom_E";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_F_eye_top" -p "cage_head";
	rename -uid "0F3CA254-40E4-8CD3-C341-43A61C828456";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -4.5269403457645749 4.3284947579465154 5.5060144935803175 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -4.5269403457641602 149.48547363281253 5.6530575752258292 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "eye_top_F";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_mouth_top" -p "cage_head";
	rename -uid "91CBAE46-4786-3EFD-0341-F497F199887B";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -5.0487097934144756e-29 -1.0302241141237687 7.5111729179577607 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.1465707927817707e-13 144.12675476074224 7.6582159996032724 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_top";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_A_mouth_bottom" -p "cage_head";
	rename -uid "DE3B0139-47E3-C2EB-6E9D-3D94961A5E55";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.34828537702518958 -0.96828868931910961 7.3663054977612266 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.34828537702560425 144.1886901855469 7.5133485794067383 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_bottom_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_B_mouth_top" -p "cage_head";
	rename -uid "0A3C5FC3-4B2F-EBC0-A084-7998E0F9C44E";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 1.2112413644786504 -1.0893519217409846 7.006837514515377 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.2112413644790649 144.06762695312503 7.1538805961608887 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_top_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_B_mouth_top" -p "cage_head";
	rename -uid "5A41EBF1-4915-1121-29FD-5DB99F2BA18F";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -1.2113769054416987 -1.0893214041628312 7.0068799530224588 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2113769054412842 144.06765747070318 7.1539230346679705 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_top_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_mouth" -p "cage_head";
	rename -uid "70FEC74C-4A12-C054-2102-489D8B89B221";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 1.6300662755962041 -1.2127955252565812 6.609111455555416 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.6300662755966187 143.94418334960943 6.7561545372009277 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_A_mouth_top" -p "cage_head";
	rename -uid "ACC00C7E-45AB-1B2A-7AEF-87A2B6E6D483";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.31633499264675635 -1.0086329276003312 7.4812342201428201 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0.31633499264717102 144.14834594726568 7.6282773017883319 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_top_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_mouth" -p "cage_head";
	rename -uid "06012F68-4837-3BAE-23EE-38A52DAFF406";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -1.6296802759174678 -1.2129633719363255 6.6091400657849082 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.6296802759170532 143.94401550292969 6.7561831474304199 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_A_mouth_top" -p "cage_head";
	rename -uid "1A0F32A2-49A5-93CF-B4FD-99AB61C4B02B";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.31629562377971154 -1.0090143973269505 7.4808451210217246 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.31629562377929688 144.14796447753906 7.6278882026672363 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_top_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_L_B_mouth_bottom" -p "cage_head";
	rename -uid "E237C135-4A36-5ABD-4E71-238B12B204D1";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 1.1955157518382695 -1.0452845389284562 6.8751961265759238 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 1.1955157518386841 144.11169433593756 7.0222392082214355 1;
	setAttr ".sd" 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_bottom_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_mouth_bottom" -p "cage_head";
	rename -uid "1EBE683C-4483-2833-3793-958C71555FFA";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -5.0487097934144756e-29 -1.0078394705691096 7.4152742897228974 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 4.1465707927817707e-13 144.1491394042969 7.5623173713684091 1;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_bottom";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_A_mouth_bottom" -p "cage_head";
	rename -uid "07F0E5F0-435F-20E1-0EAF-F2802D0B2830";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.34839239716571313 -0.96853282994413803 7.3683268104748496 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.34839239716529846 144.18844604492188 7.5153698921203613 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_bottom_A";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode joint -n "cage_R_B_mouth_bottom" -p "cage_head";
	rename -uid "97767AC8-4878-D905-9666-09ACE9F54AB9";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -1.2289222478870723 -1.0844691092409846 6.9027511154370105 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.2289222478866577 144.07250976562503 7.0497941970825222 1;
	setAttr ".sd" 2;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "mouse_bottom_B";
	setAttr ".radi" 0.5;
	setAttr -k on ".liw";
	setAttr -k on ".filmboxTypeID";
createNode groupId -n "skinCluster172GroupId";
	rename -uid "4429FCE9-4A48-EB4A-FB58-2D8AE46E9048";
	setAttr ".ihi" 0;
createNode objectSet -n "skinCluster172Set";
	rename -uid "41C76B51-4417-72D3-FCEA-B4A28C937801";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode skinCluster -n "skinCluster172";
	rename -uid "78157ACB-4CD0-E74E-9678-AD8CE35AB75B";
	setAttr -s 50 ".wl";
	setAttr ".wl[0:49].w"
		1 4 1
		1 41 1
		1 11 1
		1 38 1
		1 18 1
		1 40 1
		1 17 1
		1 8 1
		1 9 1
		1 5 1
		1 45 1
		1 1 1
		1 37 1
		1 44 1
		1 19 1
		1 12 1
		1 20 1
		1 7 1
		1 6 1
		1 3 1
		1 10 1
		1 0 1
		1 16 1
		1 13 1
		1 2 1
		1 36 1
		1 2 1
		1 22 1
		1 43 1
		1 25 1
		1 39 1
		1 31 1
		1 42 1
		1 30 1
		1 15 1
		1 27 1
		1 14 1
		1 1 1
		1 46 1
		1 47 1
		1 32 1
		1 33 1
		1 34 1
		1 23 1
		1 21 1
		1 24 1
		1 28 1
		1 29 1
		1 35 1
		1 26 1;
	setAttr -s 48 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.5406475067138672 -149.94990539550784 -5.8851418495178232 1;
	setAttr ".pm[1]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -0.00017713675333652645 -140.86364746093756 -6.769559860229494 1;
	setAttr ".pm[2]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 7.0771525315649342e-06 -146.23309326171878 -9.3620080947875994 1;
	setAttr ".pm[3]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -5.2373948097229004 -151.1779479980469 -5.3329305648803711 1;
	setAttr ".pm[4]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -0.86931443214416504 -149.87232971191409 -7.7906503677368191 1;
	setAttr ".pm[5]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -3.9195022583007813 -145.06411743164068 -5.2573995590209961 1;
	setAttr ".pm[6]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -2.1504092216491699 -150.00845336914065 -6.8703265190124521 1;
	setAttr ".pm[7]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -3.3791522979736328 -150.61665344238287 -7.1951727867126465 1;
	setAttr ".pm[8]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -2.7486462593078613 -144.56150817871094 -6.3722524642944336 1;
	setAttr ".pm[9]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -2.2457401752471924 -142.13236999511722 -5.1819391250610369 1;
	setAttr ".pm[10]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -3.7686681747436523 -150.13578796386724 -6.4613056182861337 1;
	setAttr ".pm[11]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -1.7642942667007446 -149.66421508789063 -6.753272533416748 1;
	setAttr ".pm[12]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.0174927711486816 -148.9146423339844 -5.9361071586608878 1;
	setAttr ".pm[13]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.6227130889892578 -149.74417114257815 -5.7118911743164071 1;
	setAttr ".pm[14]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 3.9194300174713135 -145.06465148925784 -5.257352828979494 1;
	setAttr ".pm[15]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 2.7486045360565186 -144.56204223632815 -6.3721928596496582 1;
	setAttr ".pm[16]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.5261039733886719 -149.48585510253906 -5.6514916419982892 1;
	setAttr ".pm[17]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -2.3795132637023926 -148.93208312988284 -6.4497728347778311 1;
	setAttr ".pm[18]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -1.7276675701141357 -149.35498046875006 -6.6059222221374538 1;
	setAttr ".pm[19]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -3.3382620811462402 -148.88711547851565 -6.2455883026123056 1;
	setAttr ".pm[20]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.371251106262207 -149.22749328613281 -5.6876006126403826 1;
	setAttr ".pm[21]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 2.1503961086273193 -150.00801086425784 -6.8708133697509757 1;
	setAttr ".pm[22]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 0.86931216716766357 -149.87232971191409 -7.7906503677368191 1;
	setAttr ".pm[23]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 3.379152774810791 -150.61665344238287 -7.1951727867126465 1;
	setAttr ".pm[24]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 5.2373924255371094 -151.1779479980469 -5.3329305648803711 1;
	setAttr ".pm[25]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 1.764324426651001 -149.66407775878909 -6.7533397674560556 1;
	setAttr ".pm[26]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 4.622797966003418 -149.74412536621099 -5.7120447158813485 1;
	setAttr ".pm[27]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 2.2457420825958252 -142.13236999511722 -5.1819410324096689 1;
	setAttr ".pm[28]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 3.7686965465545654 -150.13566589355474 -6.4613699913024911 1;
	setAttr ".pm[29]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 4.5406265258789063 -149.94993591308591 -5.8851022720336905 1;
	setAttr ".pm[30]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 2.3795123100280762 -148.9323425292969 -6.4497795104980487 1;
	setAttr ".pm[31]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 1.7277313470840454 -149.35498046875 -6.6059145927429199 1;
	setAttr ".pm[32]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 3.338280200958252 -148.8876953125 -6.2456378936767596 1;
	setAttr ".pm[33]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 4.0180191993713379 -148.91519165039065 -5.9372191429138192 1;
	setAttr ".pm[34]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 4.3723621368408203 -149.22746276855474 -5.6897735595703152 1;
	setAttr ".pm[35]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 4.5269403457641602 -149.48547363281253 -5.6530575752258292 1;
	setAttr ".pm[36]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.1465707927817707e-13 -144.12675476074224 -7.6582159996032724 1;
	setAttr ".pm[37]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -0.34828537702560425 -144.1886901855469 -7.5133485794067383 1;
	setAttr ".pm[38]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -1.2112413644790649 -144.06762695312503 -7.1538805961608887 1;
	setAttr ".pm[39]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 1.2113769054412842 -144.06765747070318 -7.1539230346679705 1;
	setAttr ".pm[40]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -1.6300662755966187 -143.94418334960943 -6.7561545372009277 1;
	setAttr ".pm[41]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -0.31633499264717102 -144.14834594726568 -7.6282773017883319 1;
	setAttr ".pm[42]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 1.6296802759170532 -143.94401550292969 -6.7561831474304199 1;
	setAttr ".pm[43]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 0.31629562377929688 -144.14796447753906 -7.6278882026672363 1;
	setAttr ".pm[44]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -1.1955157518386841 -144.11169433593756 -7.0222392082214355 1;
	setAttr ".pm[45]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 -4.1465707927817707e-13 -144.1491394042969 -7.5623173713684091 1;
	setAttr ".pm[46]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 0.34839239716529846 -144.18844604492188 -7.5153698921203613 1;
	setAttr ".pm[47]" -type "matrix" 1 -0 0 -0 -0 1 -0 0 0 -0 1 -0 1.2289222478866577 -144.07250976562503 -7.0497941970825222 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 48 ".ma";
	setAttr -s 48 ".dpf[0:47]"  4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 
		4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4;
	setAttr -s 48 ".lw";
	setAttr -s 48 ".lw";
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 48 ".ifcl";
	setAttr -s 48 ".ifcl";
createNode dagPose -n "bindPose3";
	rename -uid "48F2E3FF-4BF2-C104-C17B-8E97C3BF6D6F";
	setAttr -s 49 ".wm";
	setAttr -s 49 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.1465707927817712e-13
		 145.15697887486601 0.14704308164551205 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.5406475067134524 4.7929265206418279
		 5.7380987678723114 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.00017713675292186938
		 -4.2933314139284562 6.6225167785839822 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 -7.0771529462220132e-06
		 1.0761143868527654 9.2149650131420877 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 5.2373948097224856 6.0209691231808904
		 5.1858874832348594 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.86931443214375037 4.7153508370480779
		 7.6436072860913074 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.9195022583003665 -0.092861443225331186
		 5.1103564773754844 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.1504092216487551 4.8514744942746404
		 6.7232834373669403 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.379152297973218 5.4596745675168563
		 7.0481297050671348 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.7486462593074465 -0.59547069615507553
		 6.2252093826489219 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.2457401752467776 -3.0246088797487971
		 5.0348960434155252 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.7686681747432376 4.9788090890012313
		 6.314262536640622 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.7642942667003301 4.507236213024612
		 6.6062294517712363 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.0174927711482669 3.7576634591183904
		 5.7890640770153761 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.622713088988843 4.5871922677121404
		 5.5648480926708954 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.9194300174717283 -0.092327385608172108
		 5.1103097473339822 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.7486045360569333 -0.59493663853785961
		 6.2251497780041465 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[17]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.5261039733882571 4.3288762276730495
		 5.5044485603527775 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.3795132637019778 3.7751042550168279
		 6.3027297531323194 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.7276675701137212 4.1980015938840438
		 6.4588791404919421 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 0 0 0 0 3.3382620811458255 3.7301366036496404
		 6.0985452209667939 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 0 0 0 0 4.3712511062617923 4.0705144112667995
		 5.5405575309948709 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.1503961086277341 4.8510319893918279
		 6.723770288105464 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.86931216716807824
		 4.7153508370480779 7.6436072860913074 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[24]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.3791527748112058 5.4596745675168563
		 7.0481297050671348 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 0 0 0 0 -5.2373924255375242 6.0209691231808904
		 5.1858874832348594 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.7643244266514155 4.5070988839230779
		 6.6062966858105439 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[27]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.6227979660038327 4.5871464913449813
		 5.5650016342358368 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[28]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.24574208259624 -3.0246088797487971
		 5.0348979507641571 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[29]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.7686965465549802 4.9786870186887313
		 6.3143269096569794 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[30]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.540626525879321 4.792957038219896
		 5.7380591903881788 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[31]" -type "matrix" "xform" 1 1 1 0 0 0 0 -2.379512310028491 3.7753636544308904
		 6.3027364288525369 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[32]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.72773134708446 4.198001593883987
		 6.4588715110974082 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[33]" -type "matrix" "xform" 1 1 1 0 0 0 0 -3.3382802009586667 3.730716437633987
		 6.0985948120312479 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[34]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.0180191993717527 3.7582127755246404
		 5.7901760612683075 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[35]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.3723621368412351 4.0704838936887313
		 5.5427304779248034 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[36]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4.5269403457645749 4.3284947579465154
		 5.5060144935803175 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[37]" -type "matrix" "xform" 1 1 1 0 0 0 0 -5.0487097934144756e-29
		 -1.0302241141237687 7.5111729179577607 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[38]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.34828537702518958 -0.96828868931910961
		 7.3663054977612266 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[39]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.2112413644786504 -1.0893519217409846
		 7.006837514515377 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[40]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.2113769054416987 -1.0893214041628312
		 7.0068799530224588 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[41]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.6300662755962041 -1.2127955252565812
		 6.609111455555416 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[42]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.31633499264675635 -1.0086329276003312
		 7.4812342201428201 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[43]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.6296802759174678 -1.2129633719363255
		 6.6091400657849082 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[44]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.31629562377971154
		 -1.0090143973269505 7.4808451210217246 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[45]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.1955157518382695 -1.0452845389284562
		 6.8751961265759238 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[46]" -type "matrix" "xform" 1 1 1 0 0 0 0 -5.0487097934144756e-29
		 -1.0078394705691096 7.4152742897228974 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[47]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.34839239716571313
		 -0.96853282994413803 7.3683268104748496 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[48]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.2289222478870723 -1.0844691092409846
		 6.9027511154370105 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 49 ".m";
	setAttr -s 49 ".p";
	setAttr -s 49 ".g[0:48]" yes no no no no no no no no no no no no no 
		no no no no no no no no no no no no no no no no no no no no no no no no no no no 
		no no no no no no no no;
	setAttr ".bp" yes;
createNode groupParts -n "skinCluster172GroupParts";
	rename -uid "AE39D0D7-497C-0917-8101-9982687D01ED";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode tweak -n "tweak177";
	rename -uid "47E69D5D-4153-1D2D-5066-98944F9B22CF";
createNode objectSet -n "tweakSet177";
	rename -uid "AD70FA06-41DE-7243-56BE-BB8B61A9055B";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId4689";
	rename -uid "9AA5BDD5-4309-5222-458A-75B9F73A21A8";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts406";
	rename -uid "0E9C8643-4598-2FC0-E251-979B23284044";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
select -ne :time1;
	setAttr -av -cb on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -cb on ".nds";
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
	setAttr -av ".ta";
	setAttr -av ".tq";
	setAttr ".etmr" no;
	setAttr ".tmr" 4096;
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -av ".hfd";
	setAttr -av ".hfe";
	setAttr -av ".hfa";
	setAttr -av ".mbe";
	setAttr -av -k on ".mbsof";
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -av -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 8 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 10 ".s";
select -ne :postProcessList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".u";
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
select -ne :lightList1;
select -ne :defaultTextureList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 6 ".tx";
select -ne :initialShadingGroup;
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
	setAttr -s 20 ".gn";
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -cb on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr";
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr -av -k on ".edl";
	setAttr -k on ".ren" -type "string" "turtle";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey" -type "string" "exr";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".an";
	setAttr -k on ".ar";
	setAttr -k on ".fs" 1;
	setAttr -k on ".ef" 10;
	setAttr -av -k on ".bfs";
	setAttr -k on ".me";
	setAttr -k on ".se";
	setAttr -av -k on ".be";
	setAttr -av -k on ".ep";
	setAttr -k on ".fec";
	setAttr -av -k on ".ofc";
	setAttr -k on ".ofe";
	setAttr -k on ".efe";
	setAttr -k on ".oft";
	setAttr -k on ".umfn";
	setAttr -k on ".ufe";
	setAttr -av -k on ".pff";
	setAttr -av -k on ".peie";
	setAttr -av -k on ".ifp";
	setAttr -k on ".rv";
	setAttr -k on ".comp";
	setAttr -k on ".cth";
	setAttr -k on ".soll";
	setAttr -cb on ".sosl";
	setAttr -k on ".rd";
	setAttr -k on ".lp";
	setAttr -av -k on ".sp";
	setAttr -k on ".shs";
	setAttr -av -k on ".lpr";
	setAttr -cb on ".gv";
	setAttr -cb on ".sv";
	setAttr -k on ".mm";
	setAttr -av -k on ".npu";
	setAttr -k on ".itf";
	setAttr -k on ".shp";
	setAttr -cb on ".isp";
	setAttr -k on ".uf";
	setAttr -k on ".oi";
	setAttr -k on ".rut";
	setAttr -k on ".mot";
	setAttr -av -cb on ".mb";
	setAttr -av -k on ".mbf";
	setAttr -k on ".mbso";
	setAttr -k on ".mbsc";
	setAttr -av -k on ".afp";
	setAttr -k on ".pfb";
	setAttr -k on ".pram";
	setAttr -k on ".poam";
	setAttr -k on ".prlm";
	setAttr -k on ".polm";
	setAttr -k on ".prm";
	setAttr -k on ".pom";
	setAttr -k on ".pfrm";
	setAttr -k on ".pfom";
	setAttr -av -k on ".bll";
	setAttr -av -k on ".bls";
	setAttr -av -k on ".smv";
	setAttr -k on ".ubc";
	setAttr -k on ".mbc";
	setAttr -cb on ".mbt";
	setAttr -k on ".udbx";
	setAttr -k on ".smc";
	setAttr -k on ".kmv";
	setAttr -cb on ".isl";
	setAttr -cb on ".ism";
	setAttr -cb on ".imb";
	setAttr -av -k on ".rlen";
	setAttr -av -k on ".frts";
	setAttr -k on ".tlwd";
	setAttr -k on ".tlht";
	setAttr -k on ".jfc";
	setAttr -cb on ".rsb";
	setAttr -cb on ".ope";
	setAttr -cb on ".oppf";
	setAttr -av -k on ".rcp";
	setAttr -av -k on ".icp";
	setAttr -av -k on ".ocp";
	setAttr -k on ".hbl";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w" 1950;
	setAttr -av -k on ".h" 1350;
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar" 1.444443941116333;
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :defaultLightSet;
select -ne :hardwareRenderGlobals;
	setAttr -av -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -cb on ".nds";
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
	setAttr -s 4 ".sol";
connectAttr "skinCluster172GroupId.id" "cageShape.iog.og[0].gid";
connectAttr "skinCluster172Set.mwc" "cageShape.iog.og[0].gco";
connectAttr "groupId4689.id" "cageShape.iog.og[1].gid";
connectAttr "tweakSet177.mwc" "cageShape.iog.og[1].gco";
connectAttr "skinCluster172.og[0]" "cageShape.i";
connectAttr "tweak177.vl[0].vt[0]" "cageShape.twl";
connectAttr "cage_head.s" "cage_L_D_eye_top.is";
connectAttr "cage_head.s" "cage_chin.is";
connectAttr "cage_head.s" "cage_nose_top.is";
connectAttr "cage_head.s" "cage_L_C_eyebrow.is";
connectAttr "cage_head.s" "cage_L_A_eyebrow.is";
connectAttr "cage_head.s" "cage_L_B_cheek.is";
connectAttr "cage_head.s" "cage_L_B_eye_top.is";
connectAttr "cage_head.s" "cage_L_B_eyebrow.is";
connectAttr "cage_head.s" "cage_L_A_cheek.is";
connectAttr "cage_head.s" "cage_L_C_cheek.is";
connectAttr "cage_head.s" "cage_L_C_eye_top.is";
connectAttr "cage_head.s" "cage_L_A_eye_top.is";
connectAttr "cage_head.s" "cage_L_D_eye_bottom.is";
connectAttr "cage_head.s" "cage_L_E_eye_top.is";
connectAttr "cage_head.s" "cage_R_B_cheek.is";
connectAttr "cage_head.s" "cage_R_A_cheek.is";
connectAttr "cage_head.s" "cage_L_F_eye_top.is";
connectAttr "cage_head.s" "cage_L_B_eye_bottom.is";
connectAttr "cage_head.s" "cage_L_A_eye_bottom.is";
connectAttr "cage_head.s" "cage_L_C_eye_bottom.is";
connectAttr "cage_head.s" "cage_L_E_eye_bottom.is";
connectAttr "cage_head.s" "cage_R_B_eye_top.is";
connectAttr "cage_head.s" "cage_R_A_eyebrow.is";
connectAttr "cage_head.s" "cage_R_B_eyebrow.is";
connectAttr "cage_head.s" "cage_R_C_eyebrow.is";
connectAttr "cage_head.s" "cage_R_A_eye_top.is";
connectAttr "cage_head.s" "cage_R_E_eye_top.is";
connectAttr "cage_head.s" "cage_R_C_cheek.is";
connectAttr "cage_head.s" "cage_R_C_eye_top.is";
connectAttr "cage_head.s" "cage_R_D_eye_top.is";
connectAttr "cage_head.s" "cage_R_B_eye_bottom.is";
connectAttr "cage_head.s" "cage_R_A_eye_bottom.is";
connectAttr "cage_head.s" "cage_R_C_eye_bottom.is";
connectAttr "cage_head.s" "cage_R_D_eye_bottom.is";
connectAttr "cage_head.s" "cage_R_E_eye_bottom.is";
connectAttr "cage_head.s" "cage_R_F_eye_top.is";
connectAttr "cage_head.s" "cage_mouth_top.is";
connectAttr "cage_head.s" "cage_L_A_mouth_bottom.is";
connectAttr "cage_head.s" "cage_L_B_mouth_top.is";
connectAttr "cage_head.s" "cage_R_B_mouth_top.is";
connectAttr "cage_head.s" "cage_L_mouth.is";
connectAttr "cage_head.s" "cage_L_A_mouth_top.is";
connectAttr "cage_head.s" "cage_R_mouth.is";
connectAttr "cage_head.s" "cage_R_A_mouth_top.is";
connectAttr "cage_head.s" "cage_L_B_mouth_bottom.is";
connectAttr "cage_head.s" "cage_mouth_bottom.is";
connectAttr "cage_head.s" "cage_R_A_mouth_bottom.is";
connectAttr "cage_head.s" "cage_R_B_mouth_bottom.is";
connectAttr "skinCluster172GroupId.msg" "skinCluster172Set.gn" -na;
connectAttr "cageShape.iog.og[0]" "skinCluster172Set.dsm" -na;
connectAttr "skinCluster172.msg" "skinCluster172Set.ub[0]";
connectAttr "skinCluster172GroupParts.og" "skinCluster172.ip[0].ig";
connectAttr "skinCluster172GroupId.id" "skinCluster172.ip[0].gi";
connectAttr "bindPose3.msg" "skinCluster172.bp";
connectAttr "cage_L_D_eye_top.wm" "skinCluster172.ma[0]";
connectAttr "cage_chin.wm" "skinCluster172.ma[1]";
connectAttr "cage_nose_top.wm" "skinCluster172.ma[2]";
connectAttr "cage_L_C_eyebrow.wm" "skinCluster172.ma[3]";
connectAttr "cage_L_A_eyebrow.wm" "skinCluster172.ma[4]";
connectAttr "cage_L_B_cheek.wm" "skinCluster172.ma[5]";
connectAttr "cage_L_B_eye_top.wm" "skinCluster172.ma[6]";
connectAttr "cage_L_B_eyebrow.wm" "skinCluster172.ma[7]";
connectAttr "cage_L_A_cheek.wm" "skinCluster172.ma[8]";
connectAttr "cage_L_C_cheek.wm" "skinCluster172.ma[9]";
connectAttr "cage_L_C_eye_top.wm" "skinCluster172.ma[10]";
connectAttr "cage_L_A_eye_top.wm" "skinCluster172.ma[11]";
connectAttr "cage_L_D_eye_bottom.wm" "skinCluster172.ma[12]";
connectAttr "cage_L_E_eye_top.wm" "skinCluster172.ma[13]";
connectAttr "cage_R_B_cheek.wm" "skinCluster172.ma[14]";
connectAttr "cage_R_A_cheek.wm" "skinCluster172.ma[15]";
connectAttr "cage_L_F_eye_top.wm" "skinCluster172.ma[16]";
connectAttr "cage_L_B_eye_bottom.wm" "skinCluster172.ma[17]";
connectAttr "cage_L_A_eye_bottom.wm" "skinCluster172.ma[18]";
connectAttr "cage_L_C_eye_bottom.wm" "skinCluster172.ma[19]";
connectAttr "cage_L_E_eye_bottom.wm" "skinCluster172.ma[20]";
connectAttr "cage_R_B_eye_top.wm" "skinCluster172.ma[21]";
connectAttr "cage_R_A_eyebrow.wm" "skinCluster172.ma[22]";
connectAttr "cage_R_B_eyebrow.wm" "skinCluster172.ma[23]";
connectAttr "cage_R_C_eyebrow.wm" "skinCluster172.ma[24]";
connectAttr "cage_R_A_eye_top.wm" "skinCluster172.ma[25]";
connectAttr "cage_R_E_eye_top.wm" "skinCluster172.ma[26]";
connectAttr "cage_R_C_cheek.wm" "skinCluster172.ma[27]";
connectAttr "cage_R_C_eye_top.wm" "skinCluster172.ma[28]";
connectAttr "cage_R_D_eye_top.wm" "skinCluster172.ma[29]";
connectAttr "cage_R_B_eye_bottom.wm" "skinCluster172.ma[30]";
connectAttr "cage_R_A_eye_bottom.wm" "skinCluster172.ma[31]";
connectAttr "cage_R_C_eye_bottom.wm" "skinCluster172.ma[32]";
connectAttr "cage_R_D_eye_bottom.wm" "skinCluster172.ma[33]";
connectAttr "cage_R_E_eye_bottom.wm" "skinCluster172.ma[34]";
connectAttr "cage_R_F_eye_top.wm" "skinCluster172.ma[35]";
connectAttr "cage_mouth_top.wm" "skinCluster172.ma[36]";
connectAttr "cage_L_A_mouth_bottom.wm" "skinCluster172.ma[37]";
connectAttr "cage_L_B_mouth_top.wm" "skinCluster172.ma[38]";
connectAttr "cage_R_B_mouth_top.wm" "skinCluster172.ma[39]";
connectAttr "cage_L_mouth.wm" "skinCluster172.ma[40]";
connectAttr "cage_L_A_mouth_top.wm" "skinCluster172.ma[41]";
connectAttr "cage_R_mouth.wm" "skinCluster172.ma[42]";
connectAttr "cage_R_A_mouth_top.wm" "skinCluster172.ma[43]";
connectAttr "cage_L_B_mouth_bottom.wm" "skinCluster172.ma[44]";
connectAttr "cage_mouth_bottom.wm" "skinCluster172.ma[45]";
connectAttr "cage_R_A_mouth_bottom.wm" "skinCluster172.ma[46]";
connectAttr "cage_R_B_mouth_bottom.wm" "skinCluster172.ma[47]";
connectAttr "cage_L_D_eye_top.liw" "skinCluster172.lw[0]";
connectAttr "cage_chin.liw" "skinCluster172.lw[1]";
connectAttr "cage_nose_top.liw" "skinCluster172.lw[2]";
connectAttr "cage_L_C_eyebrow.liw" "skinCluster172.lw[3]";
connectAttr "cage_L_A_eyebrow.liw" "skinCluster172.lw[4]";
connectAttr "cage_L_B_cheek.liw" "skinCluster172.lw[5]";
connectAttr "cage_L_B_eye_top.liw" "skinCluster172.lw[6]";
connectAttr "cage_L_B_eyebrow.liw" "skinCluster172.lw[7]";
connectAttr "cage_L_A_cheek.liw" "skinCluster172.lw[8]";
connectAttr "cage_L_C_cheek.liw" "skinCluster172.lw[9]";
connectAttr "cage_L_C_eye_top.liw" "skinCluster172.lw[10]";
connectAttr "cage_L_A_eye_top.liw" "skinCluster172.lw[11]";
connectAttr "cage_L_D_eye_bottom.liw" "skinCluster172.lw[12]";
connectAttr "cage_L_E_eye_top.liw" "skinCluster172.lw[13]";
connectAttr "cage_R_B_cheek.liw" "skinCluster172.lw[14]";
connectAttr "cage_R_A_cheek.liw" "skinCluster172.lw[15]";
connectAttr "cage_L_F_eye_top.liw" "skinCluster172.lw[16]";
connectAttr "cage_L_B_eye_bottom.liw" "skinCluster172.lw[17]";
connectAttr "cage_L_A_eye_bottom.liw" "skinCluster172.lw[18]";
connectAttr "cage_L_C_eye_bottom.liw" "skinCluster172.lw[19]";
connectAttr "cage_L_E_eye_bottom.liw" "skinCluster172.lw[20]";
connectAttr "cage_R_B_eye_top.liw" "skinCluster172.lw[21]";
connectAttr "cage_R_A_eyebrow.liw" "skinCluster172.lw[22]";
connectAttr "cage_R_B_eyebrow.liw" "skinCluster172.lw[23]";
connectAttr "cage_R_C_eyebrow.liw" "skinCluster172.lw[24]";
connectAttr "cage_R_A_eye_top.liw" "skinCluster172.lw[25]";
connectAttr "cage_R_E_eye_top.liw" "skinCluster172.lw[26]";
connectAttr "cage_R_C_cheek.liw" "skinCluster172.lw[27]";
connectAttr "cage_R_C_eye_top.liw" "skinCluster172.lw[28]";
connectAttr "cage_R_D_eye_top.liw" "skinCluster172.lw[29]";
connectAttr "cage_R_B_eye_bottom.liw" "skinCluster172.lw[30]";
connectAttr "cage_R_A_eye_bottom.liw" "skinCluster172.lw[31]";
connectAttr "cage_R_C_eye_bottom.liw" "skinCluster172.lw[32]";
connectAttr "cage_R_D_eye_bottom.liw" "skinCluster172.lw[33]";
connectAttr "cage_R_E_eye_bottom.liw" "skinCluster172.lw[34]";
connectAttr "cage_R_F_eye_top.liw" "skinCluster172.lw[35]";
connectAttr "cage_mouth_top.liw" "skinCluster172.lw[36]";
connectAttr "cage_L_A_mouth_bottom.liw" "skinCluster172.lw[37]";
connectAttr "cage_L_B_mouth_top.liw" "skinCluster172.lw[38]";
connectAttr "cage_R_B_mouth_top.liw" "skinCluster172.lw[39]";
connectAttr "cage_L_mouth.liw" "skinCluster172.lw[40]";
connectAttr "cage_L_A_mouth_top.liw" "skinCluster172.lw[41]";
connectAttr "cage_R_mouth.liw" "skinCluster172.lw[42]";
connectAttr "cage_R_A_mouth_top.liw" "skinCluster172.lw[43]";
connectAttr "cage_L_B_mouth_bottom.liw" "skinCluster172.lw[44]";
connectAttr "cage_mouth_bottom.liw" "skinCluster172.lw[45]";
connectAttr "cage_R_A_mouth_bottom.liw" "skinCluster172.lw[46]";
connectAttr "cage_R_B_mouth_bottom.liw" "skinCluster172.lw[47]";
connectAttr "cage_L_D_eye_top.obcc" "skinCluster172.ifcl[0]";
connectAttr "cage_chin.obcc" "skinCluster172.ifcl[1]";
connectAttr "cage_nose_top.obcc" "skinCluster172.ifcl[2]";
connectAttr "cage_L_C_eyebrow.obcc" "skinCluster172.ifcl[3]";
connectAttr "cage_L_A_eyebrow.obcc" "skinCluster172.ifcl[4]";
connectAttr "cage_L_B_cheek.obcc" "skinCluster172.ifcl[5]";
connectAttr "cage_L_B_eye_top.obcc" "skinCluster172.ifcl[6]";
connectAttr "cage_L_B_eyebrow.obcc" "skinCluster172.ifcl[7]";
connectAttr "cage_L_A_cheek.obcc" "skinCluster172.ifcl[8]";
connectAttr "cage_L_C_cheek.obcc" "skinCluster172.ifcl[9]";
connectAttr "cage_L_C_eye_top.obcc" "skinCluster172.ifcl[10]";
connectAttr "cage_L_A_eye_top.obcc" "skinCluster172.ifcl[11]";
connectAttr "cage_L_D_eye_bottom.obcc" "skinCluster172.ifcl[12]";
connectAttr "cage_L_E_eye_top.obcc" "skinCluster172.ifcl[13]";
connectAttr "cage_R_B_cheek.obcc" "skinCluster172.ifcl[14]";
connectAttr "cage_R_A_cheek.obcc" "skinCluster172.ifcl[15]";
connectAttr "cage_L_F_eye_top.obcc" "skinCluster172.ifcl[16]";
connectAttr "cage_L_B_eye_bottom.obcc" "skinCluster172.ifcl[17]";
connectAttr "cage_L_A_eye_bottom.obcc" "skinCluster172.ifcl[18]";
connectAttr "cage_L_C_eye_bottom.obcc" "skinCluster172.ifcl[19]";
connectAttr "cage_L_E_eye_bottom.obcc" "skinCluster172.ifcl[20]";
connectAttr "cage_R_B_eye_top.obcc" "skinCluster172.ifcl[21]";
connectAttr "cage_R_A_eyebrow.obcc" "skinCluster172.ifcl[22]";
connectAttr "cage_R_B_eyebrow.obcc" "skinCluster172.ifcl[23]";
connectAttr "cage_R_C_eyebrow.obcc" "skinCluster172.ifcl[24]";
connectAttr "cage_R_A_eye_top.obcc" "skinCluster172.ifcl[25]";
connectAttr "cage_R_E_eye_top.obcc" "skinCluster172.ifcl[26]";
connectAttr "cage_R_C_cheek.obcc" "skinCluster172.ifcl[27]";
connectAttr "cage_R_C_eye_top.obcc" "skinCluster172.ifcl[28]";
connectAttr "cage_R_D_eye_top.obcc" "skinCluster172.ifcl[29]";
connectAttr "cage_R_B_eye_bottom.obcc" "skinCluster172.ifcl[30]";
connectAttr "cage_R_A_eye_bottom.obcc" "skinCluster172.ifcl[31]";
connectAttr "cage_R_C_eye_bottom.obcc" "skinCluster172.ifcl[32]";
connectAttr "cage_R_D_eye_bottom.obcc" "skinCluster172.ifcl[33]";
connectAttr "cage_R_E_eye_bottom.obcc" "skinCluster172.ifcl[34]";
connectAttr "cage_R_F_eye_top.obcc" "skinCluster172.ifcl[35]";
connectAttr "cage_mouth_top.obcc" "skinCluster172.ifcl[36]";
connectAttr "cage_L_A_mouth_bottom.obcc" "skinCluster172.ifcl[37]";
connectAttr "cage_L_B_mouth_top.obcc" "skinCluster172.ifcl[38]";
connectAttr "cage_R_B_mouth_top.obcc" "skinCluster172.ifcl[39]";
connectAttr "cage_L_mouth.obcc" "skinCluster172.ifcl[40]";
connectAttr "cage_L_A_mouth_top.obcc" "skinCluster172.ifcl[41]";
connectAttr "cage_R_mouth.obcc" "skinCluster172.ifcl[42]";
connectAttr "cage_R_A_mouth_top.obcc" "skinCluster172.ifcl[43]";
connectAttr "cage_L_B_mouth_bottom.obcc" "skinCluster172.ifcl[44]";
connectAttr "cage_mouth_bottom.obcc" "skinCluster172.ifcl[45]";
connectAttr "cage_R_A_mouth_bottom.obcc" "skinCluster172.ifcl[46]";
connectAttr "cage_R_B_mouth_bottom.obcc" "skinCluster172.ifcl[47]";
connectAttr "cage_head.msg" "bindPose3.m[0]";
connectAttr "cage_L_D_eye_top.msg" "bindPose3.m[1]";
connectAttr "cage_chin.msg" "bindPose3.m[2]";
connectAttr "cage_nose_top.msg" "bindPose3.m[3]";
connectAttr "cage_L_C_eyebrow.msg" "bindPose3.m[4]";
connectAttr "cage_L_A_eyebrow.msg" "bindPose3.m[5]";
connectAttr "cage_L_B_cheek.msg" "bindPose3.m[6]";
connectAttr "cage_L_B_eye_top.msg" "bindPose3.m[7]";
connectAttr "cage_L_B_eyebrow.msg" "bindPose3.m[8]";
connectAttr "cage_L_A_cheek.msg" "bindPose3.m[9]";
connectAttr "cage_L_C_cheek.msg" "bindPose3.m[10]";
connectAttr "cage_L_C_eye_top.msg" "bindPose3.m[11]";
connectAttr "cage_L_A_eye_top.msg" "bindPose3.m[12]";
connectAttr "cage_L_D_eye_bottom.msg" "bindPose3.m[13]";
connectAttr "cage_L_E_eye_top.msg" "bindPose3.m[14]";
connectAttr "cage_R_B_cheek.msg" "bindPose3.m[15]";
connectAttr "cage_R_A_cheek.msg" "bindPose3.m[16]";
connectAttr "cage_L_F_eye_top.msg" "bindPose3.m[17]";
connectAttr "cage_L_B_eye_bottom.msg" "bindPose3.m[18]";
connectAttr "cage_L_A_eye_bottom.msg" "bindPose3.m[19]";
connectAttr "cage_L_C_eye_bottom.msg" "bindPose3.m[20]";
connectAttr "cage_L_E_eye_bottom.msg" "bindPose3.m[21]";
connectAttr "cage_R_B_eye_top.msg" "bindPose3.m[22]";
connectAttr "cage_R_A_eyebrow.msg" "bindPose3.m[23]";
connectAttr "cage_R_B_eyebrow.msg" "bindPose3.m[24]";
connectAttr "cage_R_C_eyebrow.msg" "bindPose3.m[25]";
connectAttr "cage_R_A_eye_top.msg" "bindPose3.m[26]";
connectAttr "cage_R_E_eye_top.msg" "bindPose3.m[27]";
connectAttr "cage_R_C_cheek.msg" "bindPose3.m[28]";
connectAttr "cage_R_C_eye_top.msg" "bindPose3.m[29]";
connectAttr "cage_R_D_eye_top.msg" "bindPose3.m[30]";
connectAttr "cage_R_B_eye_bottom.msg" "bindPose3.m[31]";
connectAttr "cage_R_A_eye_bottom.msg" "bindPose3.m[32]";
connectAttr "cage_R_C_eye_bottom.msg" "bindPose3.m[33]";
connectAttr "cage_R_D_eye_bottom.msg" "bindPose3.m[34]";
connectAttr "cage_R_E_eye_bottom.msg" "bindPose3.m[35]";
connectAttr "cage_R_F_eye_top.msg" "bindPose3.m[36]";
connectAttr "cage_mouth_top.msg" "bindPose3.m[37]";
connectAttr "cage_L_A_mouth_bottom.msg" "bindPose3.m[38]";
connectAttr "cage_L_B_mouth_top.msg" "bindPose3.m[39]";
connectAttr "cage_R_B_mouth_top.msg" "bindPose3.m[40]";
connectAttr "cage_L_mouth.msg" "bindPose3.m[41]";
connectAttr "cage_L_A_mouth_top.msg" "bindPose3.m[42]";
connectAttr "cage_R_mouth.msg" "bindPose3.m[43]";
connectAttr "cage_R_A_mouth_top.msg" "bindPose3.m[44]";
connectAttr "cage_L_B_mouth_bottom.msg" "bindPose3.m[45]";
connectAttr "cage_mouth_bottom.msg" "bindPose3.m[46]";
connectAttr "cage_R_A_mouth_bottom.msg" "bindPose3.m[47]";
connectAttr "cage_R_B_mouth_bottom.msg" "bindPose3.m[48]";
connectAttr "bindPose3.w" "bindPose3.p[0]";
connectAttr "bindPose3.m[0]" "bindPose3.p[1]";
connectAttr "bindPose3.m[0]" "bindPose3.p[2]";
connectAttr "bindPose3.m[0]" "bindPose3.p[3]";
connectAttr "bindPose3.m[0]" "bindPose3.p[4]";
connectAttr "bindPose3.m[0]" "bindPose3.p[5]";
connectAttr "bindPose3.m[0]" "bindPose3.p[6]";
connectAttr "bindPose3.m[0]" "bindPose3.p[7]";
connectAttr "bindPose3.m[0]" "bindPose3.p[8]";
connectAttr "bindPose3.m[0]" "bindPose3.p[9]";
connectAttr "bindPose3.m[0]" "bindPose3.p[10]";
connectAttr "bindPose3.m[0]" "bindPose3.p[11]";
connectAttr "bindPose3.m[0]" "bindPose3.p[12]";
connectAttr "bindPose3.m[0]" "bindPose3.p[13]";
connectAttr "bindPose3.m[0]" "bindPose3.p[14]";
connectAttr "bindPose3.m[0]" "bindPose3.p[15]";
connectAttr "bindPose3.m[0]" "bindPose3.p[16]";
connectAttr "bindPose3.m[0]" "bindPose3.p[17]";
connectAttr "bindPose3.m[0]" "bindPose3.p[18]";
connectAttr "bindPose3.m[0]" "bindPose3.p[19]";
connectAttr "bindPose3.m[0]" "bindPose3.p[20]";
connectAttr "bindPose3.m[0]" "bindPose3.p[21]";
connectAttr "bindPose3.m[0]" "bindPose3.p[22]";
connectAttr "bindPose3.m[0]" "bindPose3.p[23]";
connectAttr "bindPose3.m[0]" "bindPose3.p[24]";
connectAttr "bindPose3.m[0]" "bindPose3.p[25]";
connectAttr "bindPose3.m[0]" "bindPose3.p[26]";
connectAttr "bindPose3.m[0]" "bindPose3.p[27]";
connectAttr "bindPose3.m[0]" "bindPose3.p[28]";
connectAttr "bindPose3.m[0]" "bindPose3.p[29]";
connectAttr "bindPose3.m[0]" "bindPose3.p[30]";
connectAttr "bindPose3.m[0]" "bindPose3.p[31]";
connectAttr "bindPose3.m[0]" "bindPose3.p[32]";
connectAttr "bindPose3.m[0]" "bindPose3.p[33]";
connectAttr "bindPose3.m[0]" "bindPose3.p[34]";
connectAttr "bindPose3.m[0]" "bindPose3.p[35]";
connectAttr "bindPose3.m[0]" "bindPose3.p[36]";
connectAttr "bindPose3.m[0]" "bindPose3.p[37]";
connectAttr "bindPose3.m[0]" "bindPose3.p[38]";
connectAttr "bindPose3.m[0]" "bindPose3.p[39]";
connectAttr "bindPose3.m[0]" "bindPose3.p[40]";
connectAttr "bindPose3.m[0]" "bindPose3.p[41]";
connectAttr "bindPose3.m[0]" "bindPose3.p[42]";
connectAttr "bindPose3.m[0]" "bindPose3.p[43]";
connectAttr "bindPose3.m[0]" "bindPose3.p[44]";
connectAttr "bindPose3.m[0]" "bindPose3.p[45]";
connectAttr "bindPose3.m[0]" "bindPose3.p[46]";
connectAttr "bindPose3.m[0]" "bindPose3.p[47]";
connectAttr "bindPose3.m[0]" "bindPose3.p[48]";
connectAttr "cage_head.bps" "bindPose3.wm[0]";
connectAttr "cage_L_D_eye_top.bps" "bindPose3.wm[1]";
connectAttr "cage_chin.bps" "bindPose3.wm[2]";
connectAttr "cage_nose_top.bps" "bindPose3.wm[3]";
connectAttr "cage_L_C_eyebrow.bps" "bindPose3.wm[4]";
connectAttr "cage_L_A_eyebrow.bps" "bindPose3.wm[5]";
connectAttr "cage_L_B_cheek.bps" "bindPose3.wm[6]";
connectAttr "cage_L_B_eye_top.bps" "bindPose3.wm[7]";
connectAttr "cage_L_B_eyebrow.bps" "bindPose3.wm[8]";
connectAttr "cage_L_A_cheek.bps" "bindPose3.wm[9]";
connectAttr "cage_L_C_cheek.bps" "bindPose3.wm[10]";
connectAttr "cage_L_C_eye_top.bps" "bindPose3.wm[11]";
connectAttr "cage_L_A_eye_top.bps" "bindPose3.wm[12]";
connectAttr "cage_L_D_eye_bottom.bps" "bindPose3.wm[13]";
connectAttr "cage_L_E_eye_top.bps" "bindPose3.wm[14]";
connectAttr "cage_R_B_cheek.bps" "bindPose3.wm[15]";
connectAttr "cage_R_A_cheek.bps" "bindPose3.wm[16]";
connectAttr "cage_L_F_eye_top.bps" "bindPose3.wm[17]";
connectAttr "cage_L_B_eye_bottom.bps" "bindPose3.wm[18]";
connectAttr "cage_L_A_eye_bottom.bps" "bindPose3.wm[19]";
connectAttr "cage_L_C_eye_bottom.bps" "bindPose3.wm[20]";
connectAttr "cage_L_E_eye_bottom.bps" "bindPose3.wm[21]";
connectAttr "cage_R_B_eye_top.bps" "bindPose3.wm[22]";
connectAttr "cage_R_A_eyebrow.bps" "bindPose3.wm[23]";
connectAttr "cage_R_B_eyebrow.bps" "bindPose3.wm[24]";
connectAttr "cage_R_C_eyebrow.bps" "bindPose3.wm[25]";
connectAttr "cage_R_A_eye_top.bps" "bindPose3.wm[26]";
connectAttr "cage_R_E_eye_top.bps" "bindPose3.wm[27]";
connectAttr "cage_R_C_cheek.bps" "bindPose3.wm[28]";
connectAttr "cage_R_C_eye_top.bps" "bindPose3.wm[29]";
connectAttr "cage_R_D_eye_top.bps" "bindPose3.wm[30]";
connectAttr "cage_R_B_eye_bottom.bps" "bindPose3.wm[31]";
connectAttr "cage_R_A_eye_bottom.bps" "bindPose3.wm[32]";
connectAttr "cage_R_C_eye_bottom.bps" "bindPose3.wm[33]";
connectAttr "cage_R_D_eye_bottom.bps" "bindPose3.wm[34]";
connectAttr "cage_R_E_eye_bottom.bps" "bindPose3.wm[35]";
connectAttr "cage_R_F_eye_top.bps" "bindPose3.wm[36]";
connectAttr "cage_mouth_top.bps" "bindPose3.wm[37]";
connectAttr "cage_L_A_mouth_bottom.bps" "bindPose3.wm[38]";
connectAttr "cage_L_B_mouth_top.bps" "bindPose3.wm[39]";
connectAttr "cage_R_B_mouth_top.bps" "bindPose3.wm[40]";
connectAttr "cage_L_mouth.bps" "bindPose3.wm[41]";
connectAttr "cage_L_A_mouth_top.bps" "bindPose3.wm[42]";
connectAttr "cage_R_mouth.bps" "bindPose3.wm[43]";
connectAttr "cage_R_A_mouth_top.bps" "bindPose3.wm[44]";
connectAttr "cage_L_B_mouth_bottom.bps" "bindPose3.wm[45]";
connectAttr "cage_mouth_bottom.bps" "bindPose3.wm[46]";
connectAttr "cage_R_A_mouth_bottom.bps" "bindPose3.wm[47]";
connectAttr "cage_R_B_mouth_bottom.bps" "bindPose3.wm[48]";
connectAttr "tweak177.og[0]" "skinCluster172GroupParts.ig";
connectAttr "skinCluster172GroupId.id" "skinCluster172GroupParts.gi";
connectAttr "groupParts406.og" "tweak177.ip[0].ig";
connectAttr "groupId4689.id" "tweak177.ip[0].gi";
connectAttr "groupId4689.msg" "tweakSet177.gn" -na;
connectAttr "cageShape.iog.og[1]" "tweakSet177.dsm" -na;
connectAttr "tweak177.msg" "tweakSet177.ub[0]";
connectAttr "cageShapeOrig.w" "groupParts406.ig";
connectAttr "groupId4689.id" "groupParts406.gi";
connectAttr "cageShape.iog" ":initialShadingGroup.dsm" -na;
dataStructure -fmt "raw" -as "name=idStructure:int32=ID";
// End of facial_cage.ma
