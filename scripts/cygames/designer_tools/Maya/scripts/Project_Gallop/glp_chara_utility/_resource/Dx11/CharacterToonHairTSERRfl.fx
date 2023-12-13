//2017/09/28
string Category = "Gallop/3D/Chara/ToonHairTSERRfl";
string keywords = "bumpmap,texture";
string description = "ToonHairTSERRfl";

#define TOON_SHADING
#define TOON_RIM
#define TOON_RIM_CONTROLL
#define TOON_SPECULAR
#define TOON_ENVIRONMENT
#define TOON_HAIR
#define TOON_CUTOUT
#define USE_DIRT
#define USE_MASK_COLOR
#define USE_REFLECTION_MAP
#define MAYA_HLSL
#include "GallopCharaToon.fx"

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


