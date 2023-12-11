//2017/09/28
string Category = "Gallop/3D/Chara/AlphaNolineToonTSERRfl";
string keywords = "bumpmap,texture";
string description = "AlphaNolineToonTSERRfl";

#define ALPHA_TOON
#define TOON_SHADING
#define TOON_RIM
#define TOON_RIM_CONTROLL
#define TOON_SPECULAR
#define TOON_ENVIRONMENT
#define TOON_CUTOUT
#define USE_DIRT
#define USE_MASK_COLOR
#define USE_REFLECTION_MAP
#define MAYA_HLSL
#include "GallopCharaToon.fx"

//////// DepthStencilState ////////////////////////////

BlendState AlphaBlendDefault {
	BlendEnable[0] = TRUE;
    DestBlend = INV_SRC_ALPHA;
    SrcBlend = SRC_ALPHA;
};

//////// DepthStencilState ////////////////////////////

DepthStencilState ToonDefault {
	DepthEnable = true;
	DepthWriteMask = true;
	DepthFunc = LESS_EQUAL;
};

//////// RasterizerState ////////////////////////////

RasterizerState AlphaDefault {
	FrontCounterClockwise = true;
	CullMode = Back;
};

//////// techniques ////////////////////////////

technique11 SERDefault<
	bool overridesDrawState = true; // カリングの反映のために必要
	int isTransparent = 1; // このシェーダーは半透明として扱う
>
{
	pass
	{
		SetRasterizerState(AlphaDefault);
		SetBlendState( AlphaBlendDefault, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF );
		SetDepthStencilState(ToonDefault, 0); 
		SetVertexShader(CompileShader(vs_4_0, vert()));
		SetPixelShader(CompileShader(ps_4_0, frag()));
	}
}



