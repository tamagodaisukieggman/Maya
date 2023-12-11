//UNITY_SHADER_NO_UPGRADE

#if defined(MAYA_HLSL)
row_major float4x4 UNITY_MATRIX_MVP            : WorldViewProjection;
row_major float4x4 UNITY_MATRIX_MV            : WorldView;
row_major float4x4 UNITY_MATRIX_V                : View;
row_major float4x4 UNITY_MATRIX_P                : Projection;
row_major float4x4 UNITY_MATRIX_T_MV            : WorldViewTranspose;
row_major float4x4 UNITY_MATRIX_IT_MV            : WorldViewInverseTranspose;
row_major float4x4 UNITY_MATRIX_M                : World;
row_major float4x4 _Object2World                : World;
row_major float4x4 unity_ObjectToWorld        : World;
row_major float4x4 ViewInvXf                    : ViewInverse;
#define SV_POSITION POSITION
#define SV_Target COLOR
#define UNITY_INITIALIZE_OUTPUT(a,b)
#define TRANSFORM_TEX(a,b)    float2( a[0], 1.0f - a[1] )
#define _WorldSpaceCameraPos UNITY_MATRIX_V[3]
#define GallopObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)
#define UnityObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)
#define TEX2D_SAMPLE(a, b) tex2D(a, b)
#define ColorSaturation(a, b) a
#define fixed4 float4
#define fixed3 float3
#define fixed2 float2
#define fixed float

float3 _WorldSpaceLightPos0
<
    string Object = "PointLight";
    string UIName = "Light Position";
    string Space = "World";
> = {0.0f, 0.0f, 0.0f};

float3 _LightColor0 : Specular <
    string UIName =  "Lamp 0";
    string Object = "Pointlight0";
    string UIWidget = "Color";
> = {1.0f,1.0f,1.0f};

float3 _CharaColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

texture mainTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName =  "mainTexture";
>;
sampler2D _MainTex = sampler_state
{
    Texture = <mainTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
float4 _MainTex_ST;

#ifdef USE_EMISSIVE
texture emissiveTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "emissiveTexture";
> ;
sampler2D _EmissiveTex = sampler_state
{
    Texture = <emissiveTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;
    AddressV = Clamp;
};
float3 _EmissiveColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
#endif // USE_EMISSIVE

#else // MAYA_HLSL

#include "../../../Common/ShaderCommon.hlsl"

CBUFFER_START(UnityPerMaterial)

#ifdef USE_FIXPROJECTION
uniform float  _FixProjection; // 正射影率.
uniform float  _CameraLength;
#endif // USE_FIXPROJECTION
uniform fixed4 _CharaColor;
TEXTURE2D_SAMPLER_TO(_MainTex);

#ifdef USE_EMISSIVE
TEXTURE2D_SAMPLER(_EmissiveTex);
uniform half4 _EmissiveColor;
#endif // USE_EMISSIVE

CBUFFER_END

#endif // MAYA_HLSL
