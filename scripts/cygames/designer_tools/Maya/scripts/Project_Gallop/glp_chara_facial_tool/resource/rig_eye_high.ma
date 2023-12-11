//Maya ASCII 2017ff05 scene
//Name: rig_eye_high.ma
//Last modified: Thu, Sep 21, 2017 12:36:07 PM
//Codeset: 932
requires maya "2017ff05";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201706020738-1017329";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "A0E0A7E1-497C-4128-CB68-478DF10D07E9";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.38706045841670739 28.856100075404512 65.968045975439708 ;
	setAttr ".r" -type "double3" 4.4616472704161767 -0.59999999999952547 -7.4548337879467107e-017 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "9864F77B-4C42-3962-CB07-2EBAD73C974F";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 55.130668577016856;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -0.087172160638718077 -0.14402615614582137 0.19775315357090761 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "CC7E81EB-47E8-1140-3554-759E8AB9DCCC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "9EC0AC15-4720-151B-A54D-4DA13B517C1C";
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
	rename -uid "4CA3F1DB-4169-97B7-CD2F-A68B90FE0ADD";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "04E0BA8B-4C6B-A6C6-F2FD-409750BB374B";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 40.071764000040787;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "49D907D3-4C2C-1AFB-4907-EC9043581C8F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "724F1E13-4006-6172-E60C-379E48D99D84";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "Rig_eye_high";
	rename -uid "56AA9ABE-4709-6EEF-9B51-208D91F8FF11";
	setAttr ".ove" yes;
	setAttr ".ovc" 18;
	setAttr ".t" -type "double3" 0 42 10 ;
createNode nurbsCurve -n "Rig_eye_highShape" -p "Rig_eye_high";
	rename -uid "D78C8E88-4FCF-3FA6-E726-C6971D05FAFF";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.72628897884857846 0.72628897884857579 -1.1679617570969138e-016
		-2.4319688752245508e-016 0.041707295028771796 -6.7070445792514129e-018
		-0.72628897884857713 0.72628897884857579 -1.1679617570969151e-016
		-0.041707295028772275 0 -1.9435337220602207e-033
		-0.72628897884857846 -0.72628897884857668 1.1679617570969151e-016
		-2.5100580581212064e-016 -0.041707295028771796 6.7070445792514129e-018
		0.72628897884857557 -0.72628897884857668 1.1679617570969151e-016
		0.041707295028771789 0 3.6023667271789572e-033
		0.72628897884857846 0.72628897884857579 -1.1679617570969138e-016
		-2.4319688752245508e-016 0.041707295028771796 -6.7070445792514129e-018
		-0.72628897884857713 0.72628897884857579 -1.1679617570969151e-016
		;
createNode transform -n "Eye_high_root_L" -p "Rig_eye_high";
	rename -uid "03F9017E-4908-6599-1234-B88FA9C31E15";
	setAttr -l on ".v";
	setAttr ".t" -type "double3" 5 -10 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Eye_small_info_L_Ctrl" -p "Eye_high_root_L";
	rename -uid "29C0E68A-4D67-C4E5-F414-5E82FB659D7B";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 -1.1742305274023792 0 ;
	setAttr ".sp" -type "double3" 0 -1.1742305274023792 0 ;
	setAttr ".mntl" -type "double3" -5 -5 -1 ;
	setAttr ".mxtl" -type "double3" 5 5 1 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".mnsl" -type "double3" 0 -1 -1 ;
	setAttr ".msxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_small_info_L_CtrlShape" -p "Eye_small_info_L_Ctrl";
	rename -uid "36102A82-4006-2BD7-24D9-DFA660150EA4";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.40758917360003227 -0.76664135380234555 -6.5545338182919333e-016
		-6.5762417197992717e-017 -0.59781239022077037 -9.2695106208615648e-016
		-0.40758917360003183 -0.76664135380234544 -6.5545338182919352e-016
		-0.57641813718160684 -1.1742305274023772 -2.6860722730801626e-031
		-0.40758917360003188 -1.5818197010024093 6.5545338182919352e-016
		-1.7368603417740029e-016 -1.7506486645839847 9.2695106208615687e-016
		0.40758917360003155 -1.5818197010024093 6.5545338182919372e-016
		0.57641813718160684 -1.1742305274023774 4.9786722368185976e-031
		0.40758917360003227 -0.76664135380234555 -6.5545338182919333e-016
		-6.5762417197992717e-017 -0.59781239022077037 -9.2695106208615648e-016
		-0.40758917360003183 -0.76664135380234544 -6.5545338182919352e-016
		;
createNode transform -n "Eye_big_info_L_Ctrl" -p "Eye_high_root_L";
	rename -uid "1AB3E57F-45C3-FD49-1344-2D91569093BD";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr ".t" -type "double3" 0 -6.5138653226881615e-007 0 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 0.70088451674297758 0 ;
	setAttr ".sp" -type "double3" 0 0.70088451674297758 0 ;
	setAttr ".mntl" -type "double3" -5 -5 -1 ;
	setAttr ".mxtl" -type "double3" 5 5 1 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".mnsl" -type "double3" 0 -1 -1 ;
	setAttr ".msxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_big_info_L_CtrlShape" -p "Eye_big_info_L_Ctrl";
	rename -uid "18941F4F-4A32-307F-B0FA-1DAF7CBABDE4";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.81517834720006455 1.5160628639430409 -1.3109067636583867e-015
		-1.3152483439598543e-016 1.8537207911061917 -1.853902124172313e-015
		-0.81517834720006366 1.5160628639430414 -1.310906763658387e-015
		-1.1528362743632137 0.70088451674297791 -5.3721445461603251e-031
		-0.81517834720006377 -0.11429383045708619 1.310906763658387e-015
		-3.4737206835480059e-016 -0.45195175762023709 1.8539021241723137e-015
		0.8151783472000631 -0.11429383045708641 1.3109067636583874e-015
		1.1528362743632137 0.7008845167429768 9.9573444736371953e-031
		0.81517834720006455 1.5160628639430409 -1.3109067636583867e-015
		-1.3152483439598543e-016 1.8537207911061917 -1.853902124172313e-015
		-0.81517834720006366 1.5160628639430414 -1.310906763658387e-015
		;
createNode transform -n "Eye_frame_L" -p "Eye_high_root_L";
	rename -uid "621283CE-44CF-FC94-F2B5-C9BE17027C5D";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "Eye_frame_LShape" -p "Eye_frame_L";
	rename -uid "9E07B0D8-4203-03BE-80C9-7EB9F3AE1B94";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.6982882233334675 1.6982882233334651 -2.7310557576216385e-016
		-2.7401007165830299e-016 2.4017422382566957 -3.8622960920256525e-016
		-1.698288223333466 1.6982882233334662 -2.7310557576216405e-016
		-2.4017422382566957 6.9596481380018979e-016 -1.1191967804500679e-031
		-1.6982882233334662 -1.698288223333466 2.73105575762164e-016
		-7.2369180907250123e-016 -2.4017422382566966 3.862296092025653e-016
		1.6982882233334649 -1.6982882233334664 2.731055757621641e-016
		2.4017422382566957 -1.2899804413290342e-015 2.0744467653410834e-031
		1.6982882233334675 1.6982882233334651 -2.7310557576216385e-016
		-2.7401007165830299e-016 2.4017422382566957 -3.8622960920256525e-016
		-1.698288223333466 1.6982882233334662 -2.7310557576216405e-016
		;
createNode transform -n "Eye_big_center_L" -p "Eye_high_root_L";
	rename -uid "F2CA9B02-4047-62FC-E802-FA87B306C986";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 0.70088386535644531 0 ;
	setAttr ".sp" -type "double3" 0 0.70088386535644531 0 ;
	setAttr ".dsp" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_big_center_LShape" -p "Eye_big_center_L";
	rename -uid "BFDEAE3E-46B2-3A00-C974-B6AE9E3FADA6";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.091559374404159899 0.79244323976060504 -1.4723870376955256e-017
		-1.4772634230619082e-017 0.83036837440120415 -2.0822697177713595e-017
		-0.091559374404159816 0.79244323976060516 -1.4723870376955268e-017
		-0.12948450904475883 0.70088386535644531 -6.0338966993494253e-033
		-0.091559374404159816 0.60932449095228547 1.4723870376955265e-017
		-3.9016209610188354e-017 0.57139935631168637 2.0822697177713598e-017
		0.091559374404159746 0.60932449095228547 1.4723870376955271e-017
		0.12948450904475883 0.7008838653564452 1.1183911273703037e-032
		0.091559374404159899 0.79244323976060504 -1.4723870376955256e-017
		-1.4772634230619082e-017 0.83036837440120415 -2.0822697177713595e-017
		-0.091559374404159816 0.79244323976060516 -1.4723870376955268e-017
		;
createNode transform -n "Eye_small_center_L" -p "Eye_high_root_L";
	rename -uid "4D685B9B-48CB-6B93-C759-E295F08D309E";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 -1.1742305755615234 0 ;
	setAttr ".sp" -type "double3" 0 -1.1742305755615234 0 ;
	setAttr ".dsp" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_small_center_LShape" -p "Eye_small_center_L";
	rename -uid "764F80AC-4D20-259D-484C-7B8DA176B297";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.091559374404159899 -1.0826712011573636 -1.4723870376955256e-017
		-1.4772634230619082e-017 -1.0447460665167645 -2.0822697177713595e-017
		-0.091559374404159816 -1.0826712011573636 -1.4723870376955268e-017
		-0.12948450904475883 -1.1742305755615234 -6.0338966993494253e-033
		-0.091559374404159816 -1.2657899499656833 1.4723870376955265e-017
		-3.9016209610188354e-017 -1.3037150846062824 2.0822697177713598e-017
		0.091559374404159746 -1.2657899499656833 1.4723870376955271e-017
		0.12948450904475883 -1.1742305755615234 1.1183911273703037e-032
		0.091559374404159899 -1.0826712011573636 -1.4723870376955256e-017
		-1.4772634230619082e-017 -1.0447460665167645 -2.0822697177713595e-017
		-0.091559374404159816 -1.0826712011573636 -1.4723870376955268e-017
		;
createNode transform -n "Eye_high_base_root" -p "Eye_high_root_L";
	rename -uid "8624A4B0-4A7C-9FE4-9C61-6CB9E0D1D655";
	setAttr -l on ".v";
	setAttr ".t" -type "double3" -1.5 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Eye_base_info_L_Ctrl" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root";
	rename -uid "595EA700-4FA1-9CE0-83DE-4CB9DC2BD7C9";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 4 0 ;
	setAttr ".sp" -type "double3" 0 4 0 ;
	setAttr ".mntl" -type "double3" 0 -1 -1 ;
	setAttr ".mxtl" -type "double3" 3 1 1 ;
	setAttr ".mtxe" yes;
	setAttr ".xtxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_base_info_L_CtrlShape" -p "Eye_base_info_L_Ctrl";
	rename -uid "D8BF4FFB-47E4-EBD2-9D71-418F9BDFCBC1";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.33965764466669346 4.3396576446666932 -5.4621115152432773e-017
		0 4.4803484476513393 -7.7245921840513052e-017
		-0.33965764466669324 4.3396576446666932 -5.462111515243281e-017
		-0.48034844765133933 4 -2.2383935609001356e-032
		-0.33965764466669324 3.6603423553333068 5.4621115152432798e-017
		0 3.5196515523486607 7.7245921840513065e-017
		0.33965764466669301 3.6603423553333068 5.4621115152432816e-017
		0.48034844765133911 3.9999999999999996 4.1488935306821658e-032
		0.33965764466669346 4.3396576446666932 -5.4621115152432773e-017
		0 4.4803484476513393 -7.7245921840513052e-017
		-0.33965764466669324 4.3396576446666932 -5.462111515243281e-017
		;
createNode transform -n "Eye_base_memori_L" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root";
	rename -uid "A78AF03B-42EA-9CFB-EB35-F699CA648389";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 4 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "memo0" -p "Eye_base_memori_L";
	rename -uid "9E819546-4888-7B20-072A-E080065521DD";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape0" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root|Eye_base_memori_L|memo0";
	rename -uid "7630459D-4077-45F3-E481-4F848E5FB695";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "memo1" -p "Eye_base_memori_L";
	rename -uid "5578AAD4-4F58-10C3-083B-03AA6828D600";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 1 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape1" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root|Eye_base_memori_L|memo1";
	rename -uid "BBDF1D32-42D6-D29D-8AA0-449FFFC02ECB";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "memo2" -p "Eye_base_memori_L";
	rename -uid "FA28B929-45C7-5796-3778-F79EED1FC891";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 2 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape2" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root|Eye_base_memori_L|memo2";
	rename -uid "C5A0925C-4826-51E1-2AD5-87BE708CF5E9";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "memo3" -p "Eye_base_memori_L";
	rename -uid "8532D1B6-4494-1676-EF18-869B8D866937";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 3 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape3" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root|Eye_base_memori_L|memo3";
	rename -uid "23EED712-4836-693D-B48A-3CAFDB29B32C";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "line" -p "Eye_base_memori_L";
	rename -uid "C5A8FC4A-4A7B-44A9-2B59-5681B2FD1D92";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 1.5 0 0 ;
	setAttr ".sp" -type "double3" 1.5 0 0 ;
createNode nurbsCurve -n "lineShape" -p "|Rig_eye_high|Eye_high_root_L|Eye_high_base_root|Eye_base_memori_L|line";
	rename -uid "5E802CB4-4807-B9F2-5E26-FEB1D3A0C7E1";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.32458256266316354 7.8369862325805678e-013 -1.9023711996539993e-015
		-0.16229128133158222 1.2303427027773864e-016 -1.9545680567248713e-015
		0.3245825626631631 -7.8352462652439251e-013 -1.9023711996539993e-015
		1.4999999999999991 -1.1081941875543879e-012 -1.7763568394002505e-015
		2.6754174373368365 -7.8369862325805628e-013 -1.6503424791465015e-015
		3.1622912813315818 -1.2303427027819902e-016 -1.5981456220756295e-015
		2.6754174373368365 7.8352462652439201e-013 -1.6503424791465015e-015
		1.5000000000000009 1.1081941875543879e-012 -1.7763568394002505e-015
		0.32458256266316354 7.8369862325805678e-013 -1.9023711996539993e-015
		-0.16229128133158222 1.2303427027773864e-016 -1.9545680567248713e-015
		0.3245825626631631 -7.8352462652439251e-013 -1.9023711996539993e-015
		;
createNode transform -n "Eye_high_root_R" -p "Rig_eye_high";
	rename -uid "8B97704C-4025-2060-3043-6DA46128E804";
	setAttr -l on ".v";
	setAttr ".t" -type "double3" -5 -10 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Eye_small_info_R_Ctrl" -p "Eye_high_root_R";
	rename -uid "E98FE8C0-4E99-6DA5-3C60-05B2B279C1B2";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 -1.1742305274023792 0 ;
	setAttr ".sp" -type "double3" 0 -1.1742305274023792 0 ;
	setAttr ".mntl" -type "double3" -5 -5 -1 ;
	setAttr ".mxtl" -type "double3" 5 5 1 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".mnsl" -type "double3" 0 -1 -1 ;
	setAttr ".msxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_small_info_R_CtrlShape" -p "Eye_small_info_R_Ctrl";
	rename -uid "CE91B765-4584-200D-8FB9-B89979692295";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.40758917360003227 -0.76664135380234555 -6.5545338182919333e-016
		-6.5762417197992717e-017 -0.59781239022077037 -9.2695106208615648e-016
		-0.40758917360003183 -0.76664135380234544 -6.5545338182919352e-016
		-0.57641813718160684 -1.1742305274023772 -2.6860722730801626e-031
		-0.40758917360003188 -1.5818197010024093 6.5545338182919352e-016
		-1.7368603417740029e-016 -1.7506486645839847 9.2695106208615687e-016
		0.40758917360003155 -1.5818197010024093 6.5545338182919372e-016
		0.57641813718160684 -1.1742305274023774 4.9786722368185976e-031
		0.40758917360003227 -0.76664135380234555 -6.5545338182919333e-016
		-6.5762417197992717e-017 -0.59781239022077037 -9.2695106208615648e-016
		-0.40758917360003183 -0.76664135380234544 -6.5545338182919352e-016
		;
createNode transform -n "Eye_big_info_R_Ctrl" -p "Eye_high_root_R";
	rename -uid "E1F5C520-468B-5D18-B1E6-7D8301142AE0";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr ".t" -type "double3" 0 -6.5138653226881615e-007 0 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 0.70088451674297758 0 ;
	setAttr ".sp" -type "double3" 0 0.70088451674297758 0 ;
	setAttr ".mntl" -type "double3" -5 -5 -1 ;
	setAttr ".mxtl" -type "double3" 5 5 1 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".mnsl" -type "double3" 0 -1 -1 ;
	setAttr ".msxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_big_info_R_CtrlShape" -p "Eye_big_info_R_Ctrl";
	rename -uid "60B4C9B2-40CD-A55E-51A2-CB8E0BD1CAF5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.81517834720006455 1.5160628639430409 -1.3109067636583867e-015
		-1.3152483439598543e-016 1.8537207911061917 -1.853902124172313e-015
		-0.81517834720006366 1.5160628639430414 -1.310906763658387e-015
		-1.1528362743632137 0.70088451674297791 -5.3721445461603251e-031
		-0.81517834720006377 -0.11429383045708619 1.310906763658387e-015
		-3.4737206835480059e-016 -0.45195175762023709 1.8539021241723137e-015
		0.8151783472000631 -0.11429383045708641 1.3109067636583874e-015
		1.1528362743632137 0.7008845167429768 9.9573444736371953e-031
		0.81517834720006455 1.5160628639430409 -1.3109067636583867e-015
		-1.3152483439598543e-016 1.8537207911061917 -1.853902124172313e-015
		-0.81517834720006366 1.5160628639430414 -1.310906763658387e-015
		;
createNode transform -n "Eye_frame_R" -p "Eye_high_root_R";
	rename -uid "BBBFE6E5-456F-9503-E2B6-E2913D12E92B";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "Eye_frame_RShape" -p "Eye_frame_R";
	rename -uid "57009A81-4B76-D029-284B-C6AD2BEE0BCC";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		1.6982882233334675 1.6982882233334651 -2.7310557576216385e-016
		-2.7401007165830299e-016 2.4017422382566957 -3.8622960920256525e-016
		-1.698288223333466 1.6982882233334662 -2.7310557576216405e-016
		-2.4017422382566957 6.9596481380018979e-016 -1.1191967804500679e-031
		-1.6982882233334662 -1.698288223333466 2.73105575762164e-016
		-7.2369180907250123e-016 -2.4017422382566966 3.862296092025653e-016
		1.6982882233334649 -1.6982882233334664 2.731055757621641e-016
		2.4017422382566957 -1.2899804413290342e-015 2.0744467653410834e-031
		1.6982882233334675 1.6982882233334651 -2.7310557576216385e-016
		-2.7401007165830299e-016 2.4017422382566957 -3.8622960920256525e-016
		-1.698288223333466 1.6982882233334662 -2.7310557576216405e-016
		;
createNode transform -n "Eye_small_center_R" -p "Eye_high_root_R";
	rename -uid "0F9F7FEE-46F2-E870-4204-00A9270B751D";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 -1.1742305755615234 0 ;
	setAttr ".sp" -type "double3" 0 -1.1742305755615234 0 ;
	setAttr ".dsp" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_small_center_RShape" -p "Eye_small_center_R";
	rename -uid "4C78BC13-499A-02D5-2F8C-A9BA4B5EF1C6";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.091559374404159899 -1.0826712011573636 -1.4723870376955256e-017
		-1.4772634230619082e-017 -1.0447460665167645 -2.0822697177713595e-017
		-0.091559374404159816 -1.0826712011573636 -1.4723870376955268e-017
		-0.12948450904475883 -1.1742305755615234 -6.0338966993494253e-033
		-0.091559374404159816 -1.2657899499656833 1.4723870376955265e-017
		-3.9016209610188354e-017 -1.3037150846062824 2.0822697177713598e-017
		0.091559374404159746 -1.2657899499656833 1.4723870376955271e-017
		0.12948450904475883 -1.1742305755615234 1.1183911273703037e-032
		0.091559374404159899 -1.0826712011573636 -1.4723870376955256e-017
		-1.4772634230619082e-017 -1.0447460665167645 -2.0822697177713595e-017
		-0.091559374404159816 -1.0826712011573636 -1.4723870376955268e-017
		;
createNode transform -n "Eye_big_center_R" -p "Eye_high_root_R";
	rename -uid "DC37E716-4478-2C29-9E55-BBBEDFE2BE71";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 0.70088386535644531 0 ;
	setAttr ".sp" -type "double3" 0 0.70088386535644531 0 ;
	setAttr ".dsp" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_big_center_RShape" -p "Eye_big_center_R";
	rename -uid "4AFF89CA-45D1-C315-292C-E690DAC5C75B";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.091559374404159899 0.79244323976060504 -1.4723870376955256e-017
		-1.4772634230619082e-017 0.83036837440120415 -2.0822697177713595e-017
		-0.091559374404159816 0.79244323976060516 -1.4723870376955268e-017
		-0.12948450904475883 0.70088386535644531 -6.0338966993494253e-033
		-0.091559374404159816 0.60932449095228547 1.4723870376955265e-017
		-3.9016209610188354e-017 0.57139935631168637 2.0822697177713598e-017
		0.091559374404159746 0.60932449095228547 1.4723870376955271e-017
		0.12948450904475883 0.7008838653564452 1.1183911273703037e-032
		0.091559374404159899 0.79244323976060504 -1.4723870376955256e-017
		-1.4772634230619082e-017 0.83036837440120415 -2.0822697177713595e-017
		-0.091559374404159816 0.79244323976060516 -1.4723870376955268e-017
		;
createNode transform -n "Eye_high_base_root" -p "Eye_high_root_R";
	rename -uid "067B2BC0-4F12-C1D7-E239-C5AEC52582E4";
	setAttr -l on ".v";
	setAttr ".t" -type "double3" -1.5 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Eye_base_info_R_Ctrl" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root";
	rename -uid "5E7655E6-44BD-F786-C2B3-EAB1F1B97CF5";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 4 0 ;
	setAttr ".sp" -type "double3" 0 4 0 ;
	setAttr ".mntl" -type "double3" 0 -1 -1 ;
	setAttr ".mxtl" -type "double3" 3 1 1 ;
	setAttr ".mtxe" yes;
	setAttr ".xtxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_base_info_R_CtrlShape" -p "Eye_base_info_R_Ctrl";
	rename -uid "600763AD-4FAA-E965-D49D-CCA44D2155BC";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.33965764466669346 4.3396576446666932 -5.4621115152432773e-017
		0 4.4803484476513393 -7.7245921840513052e-017
		-0.33965764466669324 4.3396576446666932 -5.462111515243281e-017
		-0.48034844765133933 4 -2.2383935609001356e-032
		-0.33965764466669324 3.6603423553333068 5.4621115152432798e-017
		0 3.5196515523486607 7.7245921840513065e-017
		0.33965764466669301 3.6603423553333068 5.4621115152432816e-017
		0.48034844765133911 3.9999999999999996 4.1488935306821658e-032
		0.33965764466669346 4.3396576446666932 -5.4621115152432773e-017
		0 4.4803484476513393 -7.7245921840513052e-017
		-0.33965764466669324 4.3396576446666932 -5.462111515243281e-017
		;
createNode transform -n "Eye_base_memori_R" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root";
	rename -uid "7F9222EB-415B-8526-5C6E-F39F194FA643";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 4 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "memo0" -p "Eye_base_memori_R";
	rename -uid "9ED1ACCA-4066-0B4F-F796-E4B09B9D26AE";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape0" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root|Eye_base_memori_R|memo0";
	rename -uid "86662EAA-4418-D727-DAE5-9684C5B6EBF5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "memo1" -p "Eye_base_memori_R";
	rename -uid "029FCA26-49B6-40D5-023E-B1978D21E347";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 1 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape1" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root|Eye_base_memori_R|memo1";
	rename -uid "F3D0B1C6-454F-494A-D43B-4FB8CDCE8BFA";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "memo2" -p "Eye_base_memori_R";
	rename -uid "7ED9D276-424D-CB54-5E47-D6A6F86C18DB";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 2 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape2" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root|Eye_base_memori_R|memo2";
	rename -uid "6C844526-4DE3-4188-CEC4-FBBCFB8F63B2";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "memo3" -p "Eye_base_memori_R";
	rename -uid "B5CDBB0D-4B17-EF44-E3F4-25A091D085AC";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 3 0 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsCurve -n "memoShape3" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root|Eye_base_memori_R|memo3";
	rename -uid "145DEE3D-4DBF-B900-DF2B-019D8ADDC9A5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		-1.1081941875543879e-012 1.6056347536186113e-016 -1.7763568394002505e-015
		-7.836116248912245e-013 -0.39180581244561213 -1.6503424791465015e-015
		-3.3392053635905194e-028 -0.55409709377719418 -1.5981456220756295e-015
		7.8361162489122379e-013 -0.3918058124456123 -1.6503424791465015e-015
		1.1081941875543879e-012 -2.976066299640297e-016 -1.7763568394002505e-015
		7.83611624891225e-013 0.39180581244561202 -1.9023711996539993e-015
		-1.2643170607829326e-028 0.55409709377719407 -1.9545680567248713e-015
		-7.8361162489122429e-013 0.39180581244561224 -1.9023711996539993e-015
		;
createNode transform -n "line" -p "Eye_base_memori_R";
	rename -uid "28EA3669-4AAB-AAC5-D470-A18B6396E3F6";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 1.5 0 0 ;
	setAttr ".sp" -type "double3" 1.5 0 0 ;
createNode nurbsCurve -n "lineShape" -p "|Rig_eye_high|Eye_high_root_R|Eye_high_base_root|Eye_base_memori_R|line";
	rename -uid "CF377CE1-40C8-0DD3-C6E6-4B8B04B921BF";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.32458256266316354 7.8369862325805678e-013 -1.9023711996539993e-015
		-0.16229128133158222 1.2303427027773864e-016 -1.9545680567248713e-015
		0.3245825626631631 -7.8352462652439251e-013 -1.9023711996539993e-015
		1.4999999999999991 -1.1081941875543879e-012 -1.7763568394002505e-015
		2.6754174373368365 -7.8369862325805628e-013 -1.6503424791465015e-015
		3.1622912813315818 -1.2303427027819902e-016 -1.5981456220756295e-015
		2.6754174373368365 7.8352462652439201e-013 -1.6503424791465015e-015
		1.5000000000000009 1.1081941875543879e-012 -1.7763568394002505e-015
		0.32458256266316354 7.8369862325805678e-013 -1.9023711996539993e-015
		-0.16229128133158222 1.2303427027773864e-016 -1.9545680567248713e-015
		0.3245825626631631 -7.8352462652439251e-013 -1.9023711996539993e-015
		;
createNode transform -n "Eye_kira_root" -p "Rig_eye_high";
	rename -uid "99BC8B14-4FAA-D35D-719E-EFBE78C4EEFE";
	setAttr -l on ".v";
	setAttr ".t" -type "double3" 0 -10 0 ;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode transform -n "Eye_kira_info_Ctrl" -p "Eye_kira_root";
	rename -uid "44E72248-4DD5-311B-CF55-F7B9FF67FF0D";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 21;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".s" -type "double3" 0.1 0.1 1 ;
	setAttr -l on ".sz";
	setAttr ".mntl" -type "double3" -5 -5 -1 ;
	setAttr ".mxtl" -type "double3" 5 5 1 ;
	setAttr ".mtxe" yes;
	setAttr ".mtye" yes;
	setAttr ".xtxe" yes;
	setAttr ".xtye" yes;
	setAttr ".mnsl" -type "double3" 0 -1 -1 ;
	setAttr ".msxe" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_kira_info_CtrlShape" -p "Eye_kira_info_Ctrl";
	rename -uid "C546B27D-416C-9658-2111-F1A86BD39902";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.043228070574071908 0.043228070574071603 -6.9516039391984759e-017
		-1.3377934175035608e-016 1.6251510501142317 -1.8856804266687534e-015
		-0.043228070574071457 0.043228070574071638 -6.9516039391984796e-017
		-1.1725973930209421 3.3978938842694633e-016 -5.4642301164914471e-031
		-0.043228070574071457 -0.043228070574071638 6.9516039391984759e-017
		-3.5332647906670454e-016 -1.1725973930209426 1.8856804266687538e-015
		0.043228070574071797 -0.043228070574071638 6.9516039391984796e-017
		1.1725973930209421 -6.2980434721769755e-016 1.0128026356255878e-030
		0.043228070574071908 0.043228070574071603 -6.9516039391984759e-017
		-1.3377934175035608e-016 1.6251510501142317 -1.8856804266687534e-015
		-0.043228070574071457 0.043228070574071638 -6.9516039391984796e-017
		;
createNode transform -n "Eye_kira_center" -p "Eye_kira_root";
	rename -uid "819B1518-4867-C741-5A18-20887C135352";
	setAttr -l on ".v";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".dsp" yes;
	setAttr ".drp" yes;
createNode nurbsCurve -n "Eye_kira_centerShape" -p "Eye_kira_center";
	rename -uid "9F42F849-4ABD-FA99-49BA-ACA256D979D4";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.091559374404160287 0.091559374404159732 -1.4723870376955256e-017
		0 0.12948450904475883 -2.0822697177713595e-017
		-0.091559374404159399 0.091559374404159843 -1.4723870376955268e-017
		-0.12948450904475894 0 -6.0338966993494253e-033
		-0.091559374404159399 -0.091559374404159843 1.4723870376955265e-017
		0 -0.12948450904475894 2.0822697177713598e-017
		0.091559374404159399 -0.091559374404159843 1.4723870376955271e-017
		0.12948450904475894 -1.1102230246251565e-016 1.1183911273703037e-032
		0.091559374404160287 0.091559374404159732 -1.4723870376955256e-017
		0 0.12948450904475883 -2.0822697177713595e-017
		-0.091559374404159399 0.091559374404159843 -1.4723870376955268e-017
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "79126466-4B0C-D1D4-AAFF-17BC2E053343";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "BC197521-455E-88CD-35CB-529B096A4EFA";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "8E17917D-4C47-95D7-8EC8-C2B3F4C639FD";
createNode displayLayerManager -n "layerManager";
	rename -uid "007A2B73-4B9C-C941-913C-BBAC0D6929DA";
createNode displayLayer -n "defaultLayer";
	rename -uid "71D88E7F-44B3-A550-940D-9F80C7FCD1F4";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "DC0E44B0-4DFA-5B82-6766-1C9FBEF15179";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "78769C8C-4323-62F9-12A0-EEBAE76DFC59";
	setAttr ".g" yes;
createNode mentalrayItemsList -s -n "mentalrayItemsList";
	rename -uid "F40BAFC7-4113-341D-5499-A09BA761CDD5";
createNode mentalrayGlobals -s -n "mentalrayGlobals";
	rename -uid "3CE4C03F-4C49-252F-7CC0-DBAEDE5EA07D";
createNode mentalrayOptions -s -n "miDefaultOptions";
	rename -uid "F13D4D90-4068-0767-38F1-40B8598BB873";
	addAttr -ci true -m -sn "stringOptions" -ln "stringOptions" -at "compound" -nc 
		3;
	addAttr -ci true -sn "name" -ln "name" -dt "string" -p "stringOptions";
	addAttr -ci true -sn "value" -ln "value" -dt "string" -p "stringOptions";
	addAttr -ci true -sn "type" -ln "type" -dt "string" -p "stringOptions";
	setAttr -s 48 ".stringOptions";
	setAttr ".stringOptions[0].name" -type "string" "rast motion factor";
	setAttr ".stringOptions[0].value" -type "string" "1.0";
	setAttr ".stringOptions[0].type" -type "string" "scalar";
	setAttr ".stringOptions[1].name" -type "string" "rast transparency depth";
	setAttr ".stringOptions[1].value" -type "string" "8";
	setAttr ".stringOptions[1].type" -type "string" "integer";
	setAttr ".stringOptions[2].name" -type "string" "rast useopacity";
	setAttr ".stringOptions[2].value" -type "string" "true";
	setAttr ".stringOptions[2].type" -type "string" "boolean";
	setAttr ".stringOptions[3].name" -type "string" "importon";
	setAttr ".stringOptions[3].value" -type "string" "false";
	setAttr ".stringOptions[3].type" -type "string" "boolean";
	setAttr ".stringOptions[4].name" -type "string" "importon density";
	setAttr ".stringOptions[4].value" -type "string" "1.0";
	setAttr ".stringOptions[4].type" -type "string" "scalar";
	setAttr ".stringOptions[5].name" -type "string" "importon merge";
	setAttr ".stringOptions[5].value" -type "string" "0.0";
	setAttr ".stringOptions[5].type" -type "string" "scalar";
	setAttr ".stringOptions[6].name" -type "string" "importon trace depth";
	setAttr ".stringOptions[6].value" -type "string" "0";
	setAttr ".stringOptions[6].type" -type "string" "integer";
	setAttr ".stringOptions[7].name" -type "string" "importon traverse";
	setAttr ".stringOptions[7].value" -type "string" "true";
	setAttr ".stringOptions[7].type" -type "string" "boolean";
	setAttr ".stringOptions[8].name" -type "string" "shadowmap pixel samples";
	setAttr ".stringOptions[8].value" -type "string" "3";
	setAttr ".stringOptions[8].type" -type "string" "integer";
	setAttr ".stringOptions[9].name" -type "string" "ambient occlusion";
	setAttr ".stringOptions[9].value" -type "string" "false";
	setAttr ".stringOptions[9].type" -type "string" "boolean";
	setAttr ".stringOptions[10].name" -type "string" "ambient occlusion rays";
	setAttr ".stringOptions[10].value" -type "string" "64";
	setAttr ".stringOptions[10].type" -type "string" "integer";
	setAttr ".stringOptions[11].name" -type "string" "ambient occlusion cache";
	setAttr ".stringOptions[11].value" -type "string" "false";
	setAttr ".stringOptions[11].type" -type "string" "boolean";
	setAttr ".stringOptions[12].name" -type "string" "ambient occlusion cache density";
	setAttr ".stringOptions[12].value" -type "string" "1.0";
	setAttr ".stringOptions[12].type" -type "string" "scalar";
	setAttr ".stringOptions[13].name" -type "string" "ambient occlusion cache points";
	setAttr ".stringOptions[13].value" -type "string" "64";
	setAttr ".stringOptions[13].type" -type "string" "integer";
	setAttr ".stringOptions[14].name" -type "string" "irradiance particles";
	setAttr ".stringOptions[14].value" -type "string" "false";
	setAttr ".stringOptions[14].type" -type "string" "boolean";
	setAttr ".stringOptions[15].name" -type "string" "irradiance particles rays";
	setAttr ".stringOptions[15].value" -type "string" "256";
	setAttr ".stringOptions[15].type" -type "string" "integer";
	setAttr ".stringOptions[16].name" -type "string" "irradiance particles interpolate";
	setAttr ".stringOptions[16].value" -type "string" "1";
	setAttr ".stringOptions[16].type" -type "string" "integer";
	setAttr ".stringOptions[17].name" -type "string" "irradiance particles interppoints";
	setAttr ".stringOptions[17].value" -type "string" "64";
	setAttr ".stringOptions[17].type" -type "string" "integer";
	setAttr ".stringOptions[18].name" -type "string" "irradiance particles indirect passes";
	setAttr ".stringOptions[18].value" -type "string" "0";
	setAttr ".stringOptions[18].type" -type "string" "integer";
	setAttr ".stringOptions[19].name" -type "string" "irradiance particles scale";
	setAttr ".stringOptions[19].value" -type "string" "1.0";
	setAttr ".stringOptions[19].type" -type "string" "scalar";
	setAttr ".stringOptions[20].name" -type "string" "irradiance particles env";
	setAttr ".stringOptions[20].value" -type "string" "true";
	setAttr ".stringOptions[20].type" -type "string" "boolean";
	setAttr ".stringOptions[21].name" -type "string" "irradiance particles env rays";
	setAttr ".stringOptions[21].value" -type "string" "256";
	setAttr ".stringOptions[21].type" -type "string" "integer";
	setAttr ".stringOptions[22].name" -type "string" "irradiance particles env scale";
	setAttr ".stringOptions[22].value" -type "string" "1";
	setAttr ".stringOptions[22].type" -type "string" "integer";
	setAttr ".stringOptions[23].name" -type "string" "irradiance particles rebuild";
	setAttr ".stringOptions[23].value" -type "string" "true";
	setAttr ".stringOptions[23].type" -type "string" "boolean";
	setAttr ".stringOptions[24].name" -type "string" "irradiance particles file";
	setAttr ".stringOptions[24].value" -type "string" "";
	setAttr ".stringOptions[24].type" -type "string" "string";
	setAttr ".stringOptions[25].name" -type "string" "geom displace motion factor";
	setAttr ".stringOptions[25].value" -type "string" "1.0";
	setAttr ".stringOptions[25].type" -type "string" "scalar";
	setAttr ".stringOptions[26].name" -type "string" "contrast all buffers";
	setAttr ".stringOptions[26].value" -type "string" "true";
	setAttr ".stringOptions[26].type" -type "string" "boolean";
	setAttr ".stringOptions[27].name" -type "string" "finalgather normal tolerance";
	setAttr ".stringOptions[27].value" -type "string" "25.842";
	setAttr ".stringOptions[27].type" -type "string" "scalar";
	setAttr ".stringOptions[28].name" -type "string" "trace camera clip";
	setAttr ".stringOptions[28].value" -type "string" "false";
	setAttr ".stringOptions[28].type" -type "string" "boolean";
	setAttr ".stringOptions[29].name" -type "string" "unified sampling";
	setAttr ".stringOptions[29].value" -type "string" "true";
	setAttr ".stringOptions[29].type" -type "string" "boolean";
	setAttr ".stringOptions[30].name" -type "string" "samples quality";
	setAttr ".stringOptions[30].value" -type "string" "0.25 0.25 0.25 0.25";
	setAttr ".stringOptions[30].type" -type "string" "color";
	setAttr ".stringOptions[31].name" -type "string" "samples min";
	setAttr ".stringOptions[31].value" -type "string" "1.0";
	setAttr ".stringOptions[31].type" -type "string" "scalar";
	setAttr ".stringOptions[32].name" -type "string" "samples max";
	setAttr ".stringOptions[32].value" -type "string" "100.0";
	setAttr ".stringOptions[32].type" -type "string" "scalar";
	setAttr ".stringOptions[33].name" -type "string" "samples error cutoff";
	setAttr ".stringOptions[33].value" -type "string" "0.0 0.0 0.0 0.0";
	setAttr ".stringOptions[33].type" -type "string" "color";
	setAttr ".stringOptions[34].name" -type "string" "samples per object";
	setAttr ".stringOptions[34].value" -type "string" "false";
	setAttr ".stringOptions[34].type" -type "string" "boolean";
	setAttr ".stringOptions[35].name" -type "string" "progressive";
	setAttr ".stringOptions[35].value" -type "string" "false";
	setAttr ".stringOptions[35].type" -type "string" "boolean";
	setAttr ".stringOptions[36].name" -type "string" "progressive max time";
	setAttr ".stringOptions[36].value" -type "string" "0";
	setAttr ".stringOptions[36].type" -type "string" "integer";
	setAttr ".stringOptions[37].name" -type "string" "progressive subsampling size";
	setAttr ".stringOptions[37].value" -type "string" "4";
	setAttr ".stringOptions[37].type" -type "string" "integer";
	setAttr ".stringOptions[38].name" -type "string" "iray";
	setAttr ".stringOptions[38].value" -type "string" "false";
	setAttr ".stringOptions[38].type" -type "string" "boolean";
	setAttr ".stringOptions[39].name" -type "string" "light relative scale";
	setAttr ".stringOptions[39].value" -type "string" "0.31831";
	setAttr ".stringOptions[39].type" -type "string" "scalar";
	setAttr ".stringOptions[40].name" -type "string" "trace camera motion vectors";
	setAttr ".stringOptions[40].value" -type "string" "false";
	setAttr ".stringOptions[40].type" -type "string" "boolean";
	setAttr ".stringOptions[41].name" -type "string" "ray differentials";
	setAttr ".stringOptions[41].value" -type "string" "true";
	setAttr ".stringOptions[41].type" -type "string" "boolean";
	setAttr ".stringOptions[42].name" -type "string" "environment lighting mode";
	setAttr ".stringOptions[42].value" -type "string" "off";
	setAttr ".stringOptions[42].type" -type "string" "string";
	setAttr ".stringOptions[43].name" -type "string" "environment lighting quality";
	setAttr ".stringOptions[43].value" -type "string" "0.2";
	setAttr ".stringOptions[43].type" -type "string" "scalar";
	setAttr ".stringOptions[44].name" -type "string" "environment lighting shadow";
	setAttr ".stringOptions[44].value" -type "string" "transparent";
	setAttr ".stringOptions[44].type" -type "string" "string";
	setAttr ".stringOptions[45].name" -type "string" "environment lighting resolution";
	setAttr ".stringOptions[45].value" -type "string" "512";
	setAttr ".stringOptions[45].type" -type "string" "integer";
	setAttr ".stringOptions[46].name" -type "string" "environment lighting shader samples";
	setAttr ".stringOptions[46].value" -type "string" "2";
	setAttr ".stringOptions[46].type" -type "string" "integer";
	setAttr ".stringOptions[47].name" -type "string" "environment lighting scale";
	setAttr ".stringOptions[47].value" -type "string" "1.0 1.0 1.0";
	setAttr ".stringOptions[47].type" -type "string" "color";
createNode mentalrayFramebuffer -s -n "miDefaultFramebuffer";
	rename -uid "8C2E503F-40A7-2D5C-15CD-F2B427B7F414";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "1D88FE17-4726-8CD0-BC50-FBB2D4907C94";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n"
		+ "                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n"
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n"
		+ "            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n"
		+ "            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n"
		+ "            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 4 4 \n            -bumpResolution 4 4 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n"
		+ "            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 2210\n            -height 1054\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n"
		+ "            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n"
		+ "            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n"
		+ "            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 0\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n"
		+ "            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n"
		+ "                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n"
		+ "                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n"
		+ "                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n"
		+ "                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n"
		+ "                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n"
		+ "                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n"
		+ "                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n"
		+ "                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -image \"Z:/ppgo1/Graphic/Unit/USNW/model/HG_layout.iff\" \n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n"
		+ "                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 4 4 \\n    -bumpResolution 4 4 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2210\\n    -height 1054\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 4 4 \\n    -bumpResolution 4 4 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 2210\\n    -height 1054\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "BA6FA3D6-4063-6E93-87EB-3989BE388D98";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 250 -ast 0 -aet 250 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "305FEC81-47C9-45D8-B754-7D8DEE65C8DD";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1013.095197838452 -252.38094235223474 ;
	setAttr ".tgi[0].vh" -type "double2" 964.28567596844437 646.42854574180888 ;
select -ne :time1;
	setAttr -av -cb on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1000;
	setAttr -av -k on ".unw" 1000;
	setAttr -k on ".etw";
	setAttr -av -k on ".tps";
	setAttr -av -k on ".tms";
lockNode -l 1 ;
select -ne :hardwareRenderingGlobals;
	setAttr -k on ".ihi";
	setAttr ".otfna" -type "stringArray" 18 "NURBS カーブ" "NURBS サーフェス" "ポリゴン" "サブディビジョン サーフェス" "パーティクル" "流体" "イメージ プレーン" "UI:" "ライト" "カメラ" "ロケータ" "ジョイント" "IK ハンドル" "デフォーマ" "モーション軌跡" "コンポーネント" "その他の UI" "装飾"  ;
	setAttr ".otfva" -type "Int32Array" 18 0 1 1 1 1 1
		 1 0 0 0 0 0 0 0 0 0 0 0 ;
	setAttr -av ".aoam";
	setAttr -av ".aora";
	setAttr -k on ".mbsof";
select -ne :renderPartition;
	setAttr -av -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
lockNode -l 1 ;
select -ne :renderGlobalsList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
lockNode -l 1 ;
select -ne :defaultShaderList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
lockNode -l 1 ;
select -ne :postProcessList1;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
lockNode -l 1 ;
select -ne :defaultRenderingList1;
	setAttr -k on ".ihi";
lockNode -l 1 ;
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
lockNode -l 1 ;
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
lockNode -l 1 ;
select -ne :defaultRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".macc";
	setAttr -k on ".macd";
	setAttr -k on ".macq";
	setAttr -k on ".mcfr" 30;
	setAttr -cb on ".ifg";
	setAttr -k on ".clip";
	setAttr -k on ".edm";
	setAttr -k on ".edl";
	setAttr -k on ".ren";
	setAttr -av -k on ".esr";
	setAttr -k on ".ors";
	setAttr -k on ".sdf";
	setAttr -av -k on ".outf";
	setAttr -av -cb on ".imfkey";
	setAttr -av -k on ".gama";
	setAttr -av -k on ".an";
	setAttr -k on ".ar";
	setAttr -k on ".fs";
	setAttr -k on ".ef";
	setAttr -av -k on ".bfs";
	setAttr -k on ".me";
	setAttr -k on ".se";
	setAttr -av -k on ".be";
	setAttr -av -k on ".ep" 1;
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
	setAttr -k on ".npu";
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
	setAttr -av -k on ".w" 640;
	setAttr -av -k on ".h" 480;
	setAttr -av -k on ".pa";
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar" 1.3333332538604736;
	setAttr -av -k on ".ldar";
	setAttr -av -k on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -av -k on ".isu";
	setAttr -av -k on ".pdu";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
lockNode -l 1 ;
select -ne :defaultObjectSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".bbx";
	setAttr -k on ".vwm";
	setAttr -k on ".tpv";
	setAttr -k on ".uit";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
lockNode -l 1 ;
select -ne :hardwareRenderGlobals;
	setAttr -cb on ".cch";
	setAttr -cb on ".ihi";
	setAttr -cb on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off -cb on ".ctrs" 256;
	setAttr -av -k off -cb on ".btrs" 512;
	setAttr -k off -cb on ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off -cb on ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr" 30;
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
lockNode -l 1 ;
connectAttr "Eye_small_info_L_Ctrl.sx" "Eye_small_info_L_Ctrl.sy";
connectAttr "Eye_big_info_L_Ctrl.sx" "Eye_big_info_L_Ctrl.sy";
connectAttr "Eye_small_info_R_Ctrl.sx" "Eye_small_info_R_Ctrl.sy";
connectAttr "Eye_big_info_R_Ctrl.sx" "Eye_big_info_R_Ctrl.sy";
connectAttr "Eye_kira_info_Ctrl.sx" "Eye_kira_info_Ctrl.sy";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of rig_eye_high.ma
