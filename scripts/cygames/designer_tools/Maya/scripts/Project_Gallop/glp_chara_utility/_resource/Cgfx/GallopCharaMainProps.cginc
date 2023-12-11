//UNITY_SHADER_NO_UPGRADE

#if defined(MAYA_CGFX)
float4x4 UNITY_MATRIX_MVP            : WorldViewProjection;
float4x4 UNITY_MATRIX_MV            : WorldView;
float4x4 UNITY_MATRIX_V                : View;
float4x4 UNITY_MATRIX_P                : Projection;
float4x4 UNITY_MATRIX_T_MV            : WorldViewTranspose;
float4x4 UNITY_MATRIX_IT_MV            : WorldViewInverseTranspose;
float4x4 UNITY_MATRIX_M                : World;
float4x4 _Object2World                : World;
float4x4 unity_ObjectToWorld        : World;
float4x4 ViewInvXf                    : ViewInverse;
#define SV_POSITION POSITION
#define SV_Target COLOR
#define UNITY_INITIALIZE_OUTPUT(a,b)
#define TRANSFORM_TEX(a,b)    a
#define _WorldSpaceCameraPos UNITY_MATRIX_V[3]
#define GallopObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)
#define UnityObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)


float4 _WorldSpaceLightPos0 : Position
<
    string Object = "PointLight";
    string UIName = "Light Position";
    string Space = "World";
> = {0.0f, 0.0f, 0.0f, 1.0f};

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
    MinFilter = Linear;
    MagFilter = Linear;
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
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
};
float3 _EmissiveColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
#endif // USE_EMISSIVE

#else // MAYA_CGFX

#include "../../../Common/ShaderCommon.cginc"

#ifdef USE_FIXPROJECTION
uniform float  _FixProjection; // 正射影率.
uniform float  _CameraLength;
#endif // USE_FIXPROJECTION
uniform fixed4 _CharaColor;
uniform sampler2D _MainTex;
uniform float4 _MainTex_ST;

#ifdef USE_EMISSIVE
uniform sampler2D _EmissiveTex;
uniform half4 _EmissiveColor;
#endif // USE_EMISSIVE

#endif // MAYA_CGFX
