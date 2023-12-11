string Category = "Gallop/3D/Chara/MiniCharaBody";
string keywords = "bumpmap,texture";
string description = "MiniCharaBody";

#define USE_EMISSIVE
#define MAYA_HLSL
#include "GallopCharaMain.fx"

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


