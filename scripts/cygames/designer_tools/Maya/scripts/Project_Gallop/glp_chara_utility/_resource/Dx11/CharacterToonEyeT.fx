//2017/09/28
string Category = "Gallop/3D/Chara/ToonEye/T";
string keywords = "bumpmap,texture";
string description = "CharacterToonEyeT";

#define TOON_EYE
#define USE_MASK_COLOR
#define MAYA_HLSL
#include "GallopCharaEye.fx"

//////// DepthStencilState ////////////////////////////

DepthStencilState ToonDefault {
	DepthEnable = true;
	DepthWriteMask = true;
	DepthFunc = LESS_EQUAL;
};

//////// techniques ////////////////////////////

technique11 SERDefault
{
	pass
	{
		SetDepthStencilState(ToonDefault, 0); 
		SetVertexShader(CompileShader(vs_4_0, vert()));
		SetPixelShader(CompileShader(ps_4_0, frag()));
	}
}



