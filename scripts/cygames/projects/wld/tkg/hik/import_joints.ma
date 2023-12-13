//Maya ASCII 2018ff09 scene
//Name: import_joints.ma
//Last modified: Wed, Oct 28, 2020 12:57:37 AM
//Codeset: 932
requires maya "2018ff09";
requires -dataType "HIKCharacter" -dataType "HIKCharacterState" -dataType "HIKEffectorState"
		 -dataType "HIKPropertySetState" "mayaHIK" "1.0_HIK_2016.5";
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
select -ne :defaultRenderUtilityList1;
	setAttr -s 27 ".u";
select -ne :defaultRenderingList1;
	setAttr -s 2 ".r";
select -ne :initialShadingGroup;
	setAttr -s 2 ".dsm";
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
select -ne :ikSystem;
	setAttr -s 2 ".sol";
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
// End of import_joints.ma
