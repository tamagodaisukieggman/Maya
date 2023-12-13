//2017/09/28
string Category = "Gallop/3D/Chara/Outline/Default";
string keywords = "bumpmap,texture";
string description = "OutlineDefault";

#define TOON_SHADING
#define TOON_RIM
#define TOON_RIM_CONTROLL
#define TOON_SPECULAR
#define TOON_ENVIRONMENT
#define TOON_CUTOUT
#define USE_DIRT
#define USE_MASK_COLOR
#define USE_OUTLINE_MAINTEX
#define MAYA_HLSL
#include "GallopCharaOutline.fx"

//////// DepthStencilState ////////////////////////////

DepthStencilState ToonDefault {
	DepthEnable = true;
	DepthWriteMask = true;
	DepthFunc = LESS_EQUAL;
};

//////// RasterizerState ////////////////////////////

RasterizerState OutlineDefault {
	// CullModeをFrontにするだけでは何故か駄目だった
	FrontCounterClockwise = true;
	CullMode = Front;
};

//////// techniques ////////////////////////////

technique11 SERDefault
{
	pass
	{
		SetDepthStencilState(ToonDefault, 0);
		SetRasterizerState(OutlineDefault); 
		SetVertexShader(CompileShader(vs_4_0, vert()));
		SetPixelShader(CompileShader(ps_4_0, frag()));
	}
}




