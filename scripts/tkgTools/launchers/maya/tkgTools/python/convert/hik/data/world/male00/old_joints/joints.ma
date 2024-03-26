//Maya ASCII 2018ff09 scene
//Name: import_joints.ma
//Last modified: Fri, Oct 30, 2020 03:09:18 PM
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
	rename -uid "12C20680-41B9-9C8E-97B9-11B6FAF50302";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".ssc" no;
	setAttr ".sd" 2;
	setAttr -l on -k on ".txInitVal" -3.1554436208840472e-30;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "cog_jnt" -p "root_jnt";
	rename -uid "BE75793E-4985-DCE4-E465-EE8F7F35A375";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 0 103.33699798583984 2.8875401020050049 ;
	setAttr ".jo" -type "double3" 180 0 89.999999999999986 ;
	setAttr ".typ" 1;
	setAttr -l on -k on ".TypeID" -type "string" "spineA";
	setAttr -l on -k on ".txInitVal" -3.5527136788005009e-13;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_01_jnt" -p "cog_jnt";
	rename -uid "9C9E37F1-46FA-DA1D-2768-BBA2D0AA9FAD";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 0 -1.2621774483536189e-29 0 ;
	setAttr ".jo" -type "double3" 0 3.0000000000000004 0 ;
	setAttr ".typ" 6;
	setAttr -l on -k on ".TypeID" -type "string" "spineA";
	setAttr -l on -k on ".txInitVal" -3.5527136788005009e-13;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_02_jnt" -p "spine_01_jnt";
	rename -uid "DADFC136-425A-B9DB-F1AE-53A29A61B963";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 15.50000197279094 8.2156503646684907e-15 1.3072857818485772e-07 ;
	setAttr ".jo" -type "double3" 0 -7 0 ;
	setAttr ".typ" 6;
	setAttr -l on -k on ".TypeID" -type "string" "spineB";
	setAttr -l on -k on ".txInitVal" 12.314499855041504;
	setAttr -l on -k on ".tyInitVal" 6.3108872417680944e-29;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" -5.5;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_03_jnt" -p "spine_02_jnt";
	rename -uid "8035C4B9-41D6-3108-5C59-CE8B0F14F0B1";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 15.000002073084914 1.0658140459960264e-14 -1.0977451125881998e-07 ;
	setAttr ".jo" -type "double3" 0 -3.0000000000000004 0 ;
	setAttr ".typ" 6;
	setAttr -l on -k on ".txInitVal" 12.102499961853027;
	setAttr -l on -k on ".tyInitVal" -5.9953428796796897e-29;
	setAttr -l on -k on ".tzInitVal" 1.7763568394002505e-15;
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" 1.4124500318633039e-30;
	setAttr -l on -k on ".jyInitVal" -7.2786216412308517e-32;
	setAttr -l on -k on ".jzInitVal" 6.3611094371790206e-15;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "neck_jnt" -p "spine_03_jnt";
	rename -uid "E5CC3AD8-43D7-C24F-2592-AB802E742BEB";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 15.820499413130108 1.4210855748421511e-14 1.033502844194345e-06 ;
	setAttr ".jo" -type "double3" 0 18 0 ;
	setAttr ".typ" 7;
	setAttr -l on -k on ".txInitVal" 21.482999801635742;
	setAttr -l on -k on ".tyInitVal" -2.2088105346188331e-29;
	setAttr -l on -k on ".tzInitVal" -2.074493378592451e-15;
	setAttr -l on -k on ".rxInitVal" 1.4433913565498289e-29;
	setAttr -l on -k on ".ryInitVal" 24;
	setAttr -l on -k on ".rzInitVal" 6.5048988039814808e-29;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "head_jnt" -p "neck_jnt";
	rename -uid "61AF6E51-4CE3-C706-BC2F-379B3EFCFDDD";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 16.523259294234606 1.4743761435863178e-13 1.5919469866787495e-06 ;
	setAttr ".jo" -type "double3" 0 79 0 ;
	setAttr ".typ" 8;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "shoulderL_jnt" -p "spine_03_jnt";
	rename -uid "E50F5E7B-4BEC-5F92-ADF5-0A9B42B1F41B";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 11.706383072204375 2.700000047683687 8.3486653323916471e-07 ;
	setAttr ".jo" -type "double3" -173.02637433070194 -5.0000000000000808 90.000000000000028 ;
	setAttr ".sd" 1;
	setAttr ".typ" 9;
	setAttr -l on -k on ".txInitVal" 18.151584625244141;
	setAttr -l on -k on ".tyInitVal" 3.5165271759033203;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal" 2.4842250347137451;
	setAttr -l on -k on ".ryInitVal" 0.23229819536209106;
	setAttr -l on -k on ".rzInitVal" -17.669713973999023;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -180;
	setAttr -l on -k on ".jyInitVal" -8.130000114440918;
	setAttr -l on -k on ".jzInitVal" 90;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "armL_jnt" -p "shoulderL_jnt";
	rename -uid "F2784D13-4A22-A77F-F34B-61861E811DB2";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 14.830370003375991 5.9737829474215687e-06 2.235036156150727e-08 ;
	setAttr ".jo" -type "double3" -5.076970227647884e-06 -4.9628940675363653 0.60864373450697085 ;
	setAttr ".sd" 1;
	setAttr ".typ" 10;
	setAttr -l on -k on ".txInitVal" 18.01679801940918;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" -1.7763568394002505e-15;
	setAttr -l on -k on ".rxInitVal" 3.9295766353607178;
	setAttr -l on -k on ".ryInitVal" 4.136939525604248;
	setAttr -l on -k on ".rzInitVal" -27.157051086425781;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" -8.130000114440918;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "forearmL_jnt" -p "armL_jnt";
	rename -uid "26CE77F9-4472-2E91-60B4-55B5C66FD0A0";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 26.000001907368429 3.9864851260063006e-06 -2.4716860502760341e-09 ;
	setAttr ".sd" 1;
	setAttr ".typ" 11;
	setAttr -l on -k on ".txInitVal" 27.350000381469727;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "handL_jnt" -p "forearmL_jnt";
	rename -uid "436ECE5B-4F4D-EBFB-730A-438D328F0BBB";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 25.999999999987381 -1.1272302060660877e-05 4.1057677200091736e-05 ;
	setAttr ".sd" 1;
	setAttr ".typ" 12;
	setAttr -l on -k on ".txInitVal" 28.200000762939453;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -90;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "handWeaponL_offset_jnt" -p "handL_jnt";
	rename -uid "9939A20C-41E2-02CA-8031-6DB8EB19E800";
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
	setAttr ".t" -type "double3" 6.689 -0.526 0 ;
	setAttr -av ".tx";
	setAttr -av ".ty";
	setAttr -av ".tz";
	setAttr -l on -k on ".txInitVal" 28.200000762939453;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -90;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "handWeaponL_bind_jnt" -p "handWeaponL_offset_jnt";
	rename -uid "A016F325-474D-B75C-7725-7B86E9C1F858";
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
	setAttr -av ".tx";
	setAttr -av ".ty";
	setAttr -av ".tz";
	setAttr -l on -k on ".txInitVal" 28.200000762939453;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -90;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "shoulderR_jnt" -p "spine_03_jnt";
	rename -uid "87432F6D-4C94-D489-77F2-E49D43374318";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 11.706761480594082 -2.7000000476837447 -4.7429409395505218e-05 ;
	setAttr ".jo" -type "double3" 6.9736256692981691 5.0000000000000684 89.999999999999929 ;
	setAttr ".sd" 2;
	setAttr ".typ" 9;
	setAttr -l on -k on ".txInitVal" 18.151584625244141;
	setAttr -l on -k on ".tyInitVal" 3.5165271759033203;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal" 2.4842250347137451;
	setAttr -l on -k on ".ryInitVal" 0.23229819536209106;
	setAttr -l on -k on ".rzInitVal" -17.669713973999023;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -180;
	setAttr -l on -k on ".jyInitVal" -8.130000114440918;
	setAttr -l on -k on ".jzInitVal" 90;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "armR_jnt" -p "shoulderR_jnt";
	rename -uid "FC504A53-48A6-70FE-16FA-91961B6BAB10";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -14.830339247185822 0.00048266171188515727 4.9461688857999064e-06 ;
	setAttr ".jo" -type "double3" -5.0769702287764919e-06 -4.9628940675363653 0.60864373450699716 ;
	setAttr ".sd" 2;
	setAttr ".typ" 10;
	setAttr -l on -k on ".txInitVal" 18.01679801940918;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal" -1.7763568394002505e-15;
	setAttr -l on -k on ".rxInitVal" 3.9295766353607178;
	setAttr -l on -k on ".ryInitVal" 4.136939525604248;
	setAttr -l on -k on ".rzInitVal" -27.157051086425781;
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" -8.130000114440918;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "forearmR_jnt" -p "armR_jnt";
	rename -uid "EF2E01F6-476A-82BF-E9BE-A58EE7C024C9";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -25.999999999988663 2.6531091009474039e-05 2.4824213344654122e-08 ;
	setAttr ".sd" 2;
	setAttr ".typ" 11;
	setAttr -l on -k on ".txInitVal" 27.350000381469727;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "handR_jnt" -p "forearmR_jnt";
	rename -uid "F9287334-4D13-C6C6-D90A-9096D60C0731";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -25.999999999971777 2.6531091094739168e-05 -4.1072578358405942e-05 ;
	setAttr ".sd" 2;
	setAttr ".typ" 12;
	setAttr -l on -k on ".txInitVal" 28.200000762939453;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -90;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "handWeaponR_offset_jnt" -p "handR_jnt";
	rename -uid "D35179E1-47CC-CE12-FE2E-86B7FC7EAEF1";
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
	setAttr ".t" -type "double3" -6.689 0.526 0 ;
	setAttr -av ".tx";
	setAttr -av ".ty";
	setAttr -av ".tz";
	setAttr ".jo" -type "double3" -180 7.016709298534876e-15 -180 ;
	setAttr -l on -k on ".txInitVal" 28.200000762939453;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -90;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "handWeaponR_bind_jnt" -p "handWeaponR_offset_jnt";
	rename -uid "F419B4EC-404D-A99F-2C21-5E8894134BC7";
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
	setAttr -av ".tx";
	setAttr -av ".tz";
	setAttr -l on -k on ".txInitVal" 28.200000762939453;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" -90;
	setAttr -l on -k on ".jyInitVal";
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "hip_jnt" -p "cog_jnt";
	rename -uid "6617E1AF-4448-6B44-52C2-6FB417BA1108";
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
	setAttr -av ".rx";
	setAttr -av ".ry";
	setAttr -av ".rz";
	setAttr ".ssc" no;
	setAttr -l on -k on ".txInitVal";
	setAttr -l on -k on ".tyInitVal" 104;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal" 180;
	setAttr -l on -k on ".jyInitVal" 7.0622501593165195e-31;
	setAttr -l on -k on ".jzInitVal" 90;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "uplegL_jnt" -p "hip_jnt";
	rename -uid "DAFA59C4-4655-CDF5-3E08-50AA4A2AA155";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -8 10.527000427246096 1.2156271934509291 ;
	setAttr ".jo" -type "double3" 0 0 179.99999999999983 ;
	setAttr ".sd" 1;
	setAttr ".typ" 2;
	setAttr -l on -k on ".txInitVal" -10.5;
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
	setAttr -l on -k on ".jzInitVal" 180;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "legL_jnt" -p "uplegL_jnt";
	rename -uid "6C93E550-465F-FDC0-19F1-598FAC6B4DB8";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 41.999996185302749 1.2612133559741778e-13 0 ;
	setAttr ".sd" 1;
	setAttr ".typ" 3;
	setAttr -l on -k on ".txInitVal" 42;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "footL_jnt" -p "legL_jnt";
	rename -uid "BFB5ED67-49F6-960B-8F09-DCAF094376F3";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 42.855188369750962 1.2967404927621828e-13 0 ;
	setAttr ".jo" -type "double3" 0 59.000000000000007 0 ;
	setAttr ".sd" 1;
	setAttr ".typ" 4;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRX" 10.000244140625;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRY" 1.4033219031261979e-13;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRZ" -5.1832566261291504;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRX" 10.000244140625;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRY" 1.5987211554602254e-13;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRZ" 21.488872528076172;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRX" 15.016303062438965;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRY" 2.5401902803423582e-13;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRZ" 12.32030200958252;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRX" 5.8441362380981445;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRY" 8.8817841970012523e-14;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRZ" 12.32030200958252;
	setAttr -l on -k on ".txInitVal" 41.5;
	setAttr -l on -k on ".tyInitVal" -5.737632591262809e-13;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" 4;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 54.118396759033203;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".bend_twist_angle";
	setAttr -k on ".bend_twist_angle0";
	setAttr -k on ".bend_twist_angle1";
	setAttr -k on ".bend_twist_angle2";
	setAttr -k on ".twist_bend_angle";
	setAttr -k on ".twist_bend_angle0";
	setAttr -k on ".twist_bend_angle1";
	setAttr -k on ".twist_bend_angle2";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "toebaseL_jnt" -p "footL_jnt";
	rename -uid "13981B81-4981-1185-F453-7F99417FBAD9";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" 15.719441153131534 -0.22522544860837712 -0.46763436585608531 ;
	setAttr ".jo" -type "double3" 0 31 0 ;
	setAttr ".sd" 1;
	setAttr ".typ" 5;
	setAttr -l on -k on ".txInitVal" 17.408615112304688;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 35.881603240966797;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "uplegR_jnt" -p "hip_jnt";
	rename -uid "99A5C675-4476-BB73-B241-69AB2AB5884A";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -7.999969482421875 -10.527000427246092 1.2156251668930043 ;
	setAttr ".jo" -type "double3" -180 0 0 ;
	setAttr ".sd" 2;
	setAttr ".typ" 2;
	setAttr -l on -k on ".txInitVal" -10.5;
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
	setAttr -l on -k on ".jzInitVal" 180;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "legR_jnt" -p "uplegR_jnt";
	rename -uid "56490285-4248-7FFA-7DA1-5784563BF0B6";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -42 -8.8817841970012523e-15 0 ;
	setAttr ".sd" 2;
	setAttr ".typ" 3;
	setAttr -l on -k on ".txInitVal" 42;
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
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "footR_jnt" -p "legR_jnt";
	rename -uid "F2D3BA24-40B0-3603-FD42-8AB29446C170";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -42.855000495910645 -1.0658141036401503e-14 -2.86102294921875e-06 ;
	setAttr ".jo" -type "double3" 0 59.000000000000007 0 ;
	setAttr ".sd" 2;
	setAttr ".typ" 4;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRX" 10.000244140625;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRY" 1.4033219031261979e-13;
	setAttr -l on -k on ".heel_L_PivCtrl_GuideLoc_TRZ" -5.1832566261291504;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRX" 10.000244140625;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRY" 1.5987211554602254e-13;
	setAttr -l on -k on ".toe_L_PivCtrl_GuideLoc_TRZ" 21.488872528076172;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRX" 15.016303062438965;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRY" 2.5401902803423582e-13;
	setAttr -l on -k on ".foot_L_APivCtrl_GuideLoc_TRZ" 12.32030200958252;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRX" 5.8441362380981445;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRY" 8.8817841970012523e-14;
	setAttr -l on -k on ".foot_L_BPivCtrl_GuideLoc_TRZ" 12.32030200958252;
	setAttr -l on -k on ".txInitVal" 41.5;
	setAttr -l on -k on ".tyInitVal" -5.737632591262809e-13;
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal" 4;
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 54.118396759033203;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".bend_twist_angle";
	setAttr -k on ".bend_twist_angle0";
	setAttr -k on ".bend_twist_angle1";
	setAttr -k on ".bend_twist_angle2";
	setAttr -k on ".twist_bend_angle";
	setAttr -k on ".twist_bend_angle0";
	setAttr -k on ".twist_bend_angle1";
	setAttr -k on ".twist_bend_angle2";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "toebaseR_jnt" -p "footR_jnt";
	rename -uid "C05B2439-4C21-EB7F-C537-51B133246325";
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
	addAttr -s false -ci true -sn "ch" -ln "Character" -at "message";
	setAttr -k off -cb on ".v";
	setAttr ".t" -type "double3" -15.719410145392054 0.22519969940185369 0.46762463523300646 ;
	setAttr ".jo" -type "double3" 0 31 0 ;
	setAttr ".sd" 2;
	setAttr ".typ" 5;
	setAttr -l on -k on ".txInitVal" 17.408615112304688;
	setAttr -l on -k on ".tyInitVal";
	setAttr -l on -k on ".tzInitVal";
	setAttr -l on -k on ".rxInitVal";
	setAttr -l on -k on ".ryInitVal";
	setAttr -l on -k on ".rzInitVal";
	setAttr -l on -k on ".sxInitVal" 1;
	setAttr -l on -k on ".syInitVal" 1;
	setAttr -l on -k on ".szInitVal" 1;
	setAttr -l on -k on ".jxInitVal";
	setAttr -l on -k on ".jyInitVal" 35.881603240966797;
	setAttr -l on -k on ".jzInitVal";
	setAttr -k on ".filmboxTypeID" 5;
createNode transform -s -n "persp";
	rename -uid "2B0AE7E7-411E-BE66-09FC-DEB6F1A13539";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 24.426199138850123 30.530135629732996 24.426199138850119 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "293F1A52-4616-5E7B-6950-63BBD70D9B77";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "FC3E4225-47CB-A4AE-00B5-EDAB4C606765";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "8FAD308C-47D4-DB44-9706-49A087EC79EC";
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
	rename -uid "F9BC9EC3-4CC1-50A4-775A-349241753B12";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "027AF576-4551-FE69-7EBC-ECB3705F24CA";
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
	rename -uid "9A98953C-4D1F-CA77-ED48-01A4C7112676";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "1024B46A-496F-1584-2936-A7AB49249783";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "CD8C80B1-4B68-C3E3-B639-008F68CEA2B5";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "F593AD60-4F2F-4B7F-ABAC-1A9D71B033C9";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "E7793B1C-49D3-3C20-6A55-63B1ABE1F81F";
createNode displayLayerManager -n "layerManager";
	rename -uid "384FCE73-40AD-1CD5-5DE1-F3889AF26B9A";
createNode displayLayer -n "defaultLayer";
	rename -uid "2B46861B-4401-9253-9046-4AA546F85486";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "9D4F677D-4D04-1894-971E-AD94F227D727";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "1E157B21-4453-0B8D-8AED-6F87BE613D01";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "C4FC3E61-4287-0DD6-6DA8-01A198C13247";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n"
		+ "            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n"
		+ "            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n"
		+ "            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n"
		+ "            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 765\n            -height 830\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n"
		+ "            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n"
		+ "            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n"
		+ "                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n                -outliner \"graphEditor1OutlineEd\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n"
		+ "                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n"
		+ "                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n"
		+ "                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n"
		+ "            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n"
		+ "                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n"
		+ "                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n"
		+ "                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n"
		+ "                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n"
		+ "                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n"
		+ "                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"MG-PickerStudio_3DPanel\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"MG-PickerStudio_3DPanel\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n"
		+ "\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 765\\n    -height 830\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 765\\n    -height 830\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "17215107-4C9C-E72B-6CCF-24A022637B42";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 120 -ast 0 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr ".o" 32;
	setAttr ".unw" 32;
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
connectAttr "cog_jnt.s" "hip_jnt.is";
connectAttr "hip_jnt.s" "uplegL_jnt.is";
connectAttr "uplegL_jnt.s" "legL_jnt.is";
connectAttr "legL_jnt.s" "footL_jnt.is";
connectAttr "footL_jnt.s" "toebaseL_jnt.is";
connectAttr "hip_jnt.s" "uplegR_jnt.is";
connectAttr "uplegR_jnt.s" "legR_jnt.is";
connectAttr "legR_jnt.s" "footR_jnt.is";
connectAttr "footR_jnt.s" "toebaseR_jnt.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of import_joints.ma
