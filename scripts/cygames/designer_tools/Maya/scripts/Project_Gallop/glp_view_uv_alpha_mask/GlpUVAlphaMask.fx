#define TRANSFORM_TEX(a,b) float2(a[0], 1.0f - a[1])
float4x4 gWVP : WorldViewProjection;

//------------------------------------
// Textures
//------------------------------------
SamplerState MainTexSampler
{
    AddressU = Wrap;
	AddressV = Wrap;
    Filter = MIN_MAG_MIP_LINEAR;
};

//------------------------------------
// Textures
//------------------------------------
Texture2D MainTexture
<
    string ResourceName = "";
    string ResourceType = "2D";
    string UIWidget = "FilePicker";
    string UIName =  "MainTexture";
>;

struct VS_INPUT
{
    float4 Vertex : POSITION;
    float2 Uv : TEXCOORD0;
    float2 Uv2 : TEXCOORD1;
};


struct VS_TO_PS
{
    float4 Pos : SV_POSITION;
    float2 Uv : TEXCOORD0;
    float2 Uv2 : TEXCOORD1;
};


VS_TO_PS VS(VS_INPUT In)
{
    VS_TO_PS Out = (VS_TO_PS)0;
    Out.Pos = mul(float4(In.Vertex.x, In.Vertex.y, In.Vertex.z, 1), gWVP);
    Out.Uv = TRANSFORM_TEX(In.Uv, _MainTex);
    Out.Uv2 = TRANSFORM_TEX(In.Uv2, _MainTex);
    return Out;
};


float4 PS(VS_TO_PS In) : SV_Target
{
    float4 diffuseSample = MainTexture.Sample(MainTexSampler, In.Uv);
    float4 alphaSample = MainTexture.Sample(MainTexSampler, In.Uv2);
    return float4(diffuseSample.r, diffuseSample.g, diffuseSample.b, alphaSample.a);
};


//////// BlendState ////////////////////////////

BlendState AlphaBlendDefault {
	BlendEnable[0] = TRUE;
    DestBlend = INV_SRC_ALPHA;
    SrcBlend = SRC_ALPHA;
};

//////// DepthStencilState ////////////////////////////

DepthStencilState ToonDefault {
	DepthEnable = false;
	DepthWriteMask = true;
	DepthFunc = LESS_EQUAL;
};

//////// techniques ////////////////////////////

technique11 SERDefault<
    int isTransparent = 1; // このシェーダーは半透明として扱う
>
{
	pass
	{
		SetBlendState( AlphaBlendDefault, float4( 0.0f, 0.0f, 0.0f, 0.0f ), 0xFFFFFFFF );
		SetDepthStencilState(ToonDefault, 0); 
		SetVertexShader(CompileShader(vs_4_0, VS()));
		SetPixelShader(CompileShader(ps_4_0, PS()));
	}
}