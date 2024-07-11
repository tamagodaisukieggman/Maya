//UNITY_SHADER_NO_UPGRADE

#ifndef _DESIGNER_CHARATOON_PROPS_HLSLINC_
#define _DESIGNER_CHARATOON_PROPS_HLSLINC_

#if defined(MAYA_HLSL)

//------------------------------------
// structs for Maya
//------------------------------------
struct VertexPositionInputs
{
    float4 positionCS;
    float3 positionWS;
};

struct Light
{
    float3 color;
    float3 direction;
};

//------------------------------------
// Per Frame parameters
//------------------------------------
cbuffer UpdatePerFrame : register(b0)
{
    row_major float4x4 UNITY_MATRIX_V                : View;   
    row_major float4x4 ViewInvXf                    : ViewInverse;
    row_major float4x4 UNITY_MATRIX_P                : Projection;
}

//------------------------------------
// Per Object parameters
//------------------------------------
cbuffer UpdatePerObject : register(b1)
{
    row_major float4x4 UNITY_MATRIX_MVP            : WorldViewProjection;
    row_major float4x4 UNITY_MATRIX_MV            : WorldView;
    row_major float4x4 UNITY_MATRIX_T_MV            : WorldViewTranspose;
    row_major float4x4 UNITY_MATRIX_IT_MV            : WorldViewInverseTranspose;
    row_major float4x4 UNITY_MATRIX_M                : World;
    row_major float4x4 _Object2World                : World;
    row_major float4x4 unity_ObjectToWorld        : World;
}

#define SV_POSITION POSITION
#define SV_Target COLOR
#define _WorldSpaceCameraPos UNITY_MATRIX_V[3]
#define fixed4 float4
#define fixed3 float3
#define fixed2 float2
#define fixed float
#define UNITY_INITIALIZE_OUTPUT(a,b)
#define TRANSFORM_TEX(a,b)    float2( a[0], 1.0f - a[1] )
#define GallopObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)
#define UnityObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)
#define TEX2D_SAMPLE(a, b) tex2D(a, b)
#define ColorSaturation(a, b) a 

static const half4 OptionMaskMapDefault = half4(0.0, 0.0, 0.5, 0.0);
uniform float3 _OriginalDirectionalLightDir1 = float3(1.0f, 0.0f, 0.0f);
uniform float3 _OriginalDirectionalLightDir2 = float3(1.0f, 0.0f, 0.0f);

row_major float4x4 GetObjectToWorldMatrix(){
    return UNITY_MATRIX_M;
}

row_major float4x4 GetWorldToViewMatrix(){
    return UNITY_MATRIX_V;
}

VertexPositionInputs GallopGetVertexPositionInputs(float3 pos)
{
    VertexPositionInputs outVpi = (VertexPositionInputs)0;
    float4 tmpPos = float4(pos, 1);
    outVpi.positionCS = GallopObjectToClipPos(tmpPos);
    float4 tmpPosWs = mul(unity_ObjectToWorld, tmpPos);
    outVpi.positionWS = tmpPosWs.xyz;

    return outVpi;
}

float3 _WorldSpaceLightPos0
<
    string Object = "PointLight";
    string UIName = "Light Direction";
> = {1.0f, 0.0f, 0.0f};

float3 _LightColor0 : Specular <
    string UIName =  "Lamp 0";
    string Object = "Pointlight0";
    string UIWidget = "Color";
> = {1.0f,1.0f,1.0f};

Light GetMainLight()
{
    Light outLight = (Light)0;
    outLight.color = _LightColor0.rgb;
    outLight.direction = _WorldSpaceLightPos0;
    return outLight;
}

Texture2D mainTextureMap
<
    string ResourceName = "sample_texture/white.tga";
    string ResourceType = "2D";
    string UIName =  "mainTexture";
>;
sampler2D _MainTex = sampler_state
{
    Texture = <mainTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
float4 _MainTex_ST;

Texture2D tripleMaskMap
<
    string ResourceName = "sample_texture/base_blend.tga";
    string ResourceType = "2D";
    string UIName =  "tripleMask";
>;
sampler2D _TripleMaskMap = sampler_state
{
    Texture = <tripleMaskMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};

Texture2D optionMaskMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName =  "optionMask";
>;
sampler2D _OptionMaskMap = sampler_state
{
    Texture = <optionMaskMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
int _UseOptionMaskMap <
    string UIWidget = "slider";
    int UIMin = 0;
    int UIMax = 1;
    int UIStep = 1;
> = 0;

float4 _SpecularColor : Ambient <
    string UIWidget = "Color";
> = {1,1,1,1};

float _SpecularPower <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 2.0;

Texture2D envTextureMap
<
    string ResourceName = "sample_texture/env.tga";
    string ResourceType = "2D";
    string UIName =  "Map with dot-half-angle factors";
>;
sampler2D _EnvMap = sampler_state
{
    Texture = <envTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;
    AddressV = Clamp;
};
float _EnvRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _EnvBias <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 8.0;
    float UIStep = 0.1;
> = 1.5;
float _ToonStep <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.5;
float _ToonFeather <
    string UIWidget = "slider";
    float UIMin = 0.0001;
    float UIMax = 1.0;
    float UIStep = 0.0001;
> = 0.0001;

Texture2D toonTextureMap
<
    string ResourceName = "sample_texture/gray.tga";
    string ResourceType = "2D";
    string UIName =  "toonTexture";
>;
sampler2D _ToonMap = sampler_state
{
    Texture = <toonTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;
    AddressV = Clamp;
};
float4 _ToonColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };
float4 _ToonBrightColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,0 };
float4 _ToonDarkColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,0 };


float _RimStep <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.5;
float _RimFeather <
    string UIWidget = "slider";
    float UIMin = 0.0001;
    float UIMax = 1.0;
    float UIStep = 0.0001;
> = 0.3;
float4 _RimColor : Ambient <
    string UIWidget = "Color";
> = {1,1,1,1};
float _RimShadow <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 0.0;
float _RimSpecRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

#if defined(TOON_RIM_CONTROLL)
float _RimHorizonOffset <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1000.0;
    float UIStep = 0.01;
> = 0.0;
float _RimVerticalOffset <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1000.0;
    float UIStep = 0.01;
> = 0.0;
float _RimStep2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.1;
float _RimFeather2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.01;
> = 0.01;
float4 _RimColor2 : Ambient <
    string UIWidget = "Color";
> = {1,1,1,1};
float _RimSpecRate2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.01;
> = 0.5;
float _RimHorizonOffset2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1000.0;
    float UIStep = 0.01;
> = 0.0;
float _RimVerticalOffset2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1000.0;
    float UIStep = 0.01;
> = 0.0;
float _RimShadowRate2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;
#endif // TOON_RIM_CONTROLL

float _RimShadowRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;
float4 _GlobalToonColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };
Texture2D dirtTextureMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName =  "dirtTexture";
>;
sampler2D _DirtTex = sampler_state
{
    Texture = <dirtTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;
    AddressV = Clamp;
};

float _DirtRate1 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

float _DirtRate2 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

float _DirtRate3 <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

float4 _GlobalDirtColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };

float3 _GlobalDirtToonColor : Ambient <
    string UIWidget = "Color";
> = { 0.25,0.15,0.12 };


float4 _GlobalDirtRimSpecularColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };

float _DirtScale <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 1.0;


float _Cutoff <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

float3 _RainColor : Ambient <
    string UIWidget = "Color";
> = {1,1,1};
float4 _CharaColor : Ambient <
    string UIWidget = "Color";
> = {1,1,1,1};

float _Saturation <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 1.0;

float4 _GlobalRimColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };

float3 _Global_FogColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

float _Global_FogMinDistance <
    string UIWidget = "slider";
    float UIMin = 0.001;
    float UIMax = 100000.0;
    float UIStep = 0.1;
> = 0.001;

float _Global_FogLength <
    string UIWidget = "slider";
    float UIMin = 0.001;
    float UIMax = 100000.0;
    float UIStep = 0.1;
> = 0.001;

float _Global_MaxDensity <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 200.0;
    float UIStep = 0.1;
> = 0.0;

float _Global_MaxHeight <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 10000.0;
    float UIStep = 0.1;
> = 100.0;

float3 _LightProbeColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

#define DITHER_SIZE (4)

Texture2D ditherTextureMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName = "dirtTexture";
>;
sampler2D _DitherTex = sampler_state
{
    Texture = <dirtTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;
    AddressV = Clamp;
};
float _DitherCutt <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

Texture2D emissiveTextureMap
<
    string ResourceName = "sample_texture/black.tga";
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

#if defined(TOON_FACE) || defined(TOON_HAIR)
float _CheekPretenseThreshold <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 100.0;
    float UIStep = 0.001;
> = 0.775;
float _NosePretenseThreshold <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 100.0;
    float UIStep = 0.001;
> = 0.775;
float _NoseVisibility <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 1.0;
> = 1.0;
float _HairNormalBlend <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.001;
> = 1.0;
#endif // defined(TOON_FACE) || defined(TOON_HAIR)

#if defined(TOON_FACE) || defined(TOON_HAIR) || defined(TOON_EYE)
float _TkglinderBlend <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.001;
> = 0.0;
float3 _FaceUp = { 0,1,0 };
float3 _FaceForward = { 0,0,1 };
float3 _FaceCenterPos = { 0,0,0 };
#endif // defined(TOON_FACE) || defined(TOON_HAIR) || defined(TOON_EYE)

int _UseOriginalDirectionalLight <
    string UIWidget = "slider";
    int UIMin = 0;
    int UIMax = 2;
    int UIStep = 1;
> = 0;
float3 _OriginalDirectionalLightDir = { 0,0,1 };

#ifdef TOON_SHADING

float _VertexColorToonPower <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.001;
> = 1.0;

#endif

#ifdef USE_MASK_COLOR
Texture2D maskColorTextureMap
<
    string ResourceName = "sample_texture/gray.tga";
    string ResourceType = "2D";
    string UIName = "maskColorTexture";
> ;
sampler2D _MaskColorTex = sampler_state
{
    Texture = <maskColorTextureMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
float3 _MaskColorR1 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskColorR2 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskColorG1 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskColorG2 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskColorB1 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskColorB2 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskToonColorR1 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskToonColorR2 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskToonColorG1 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskToonColorG2 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskToonColorB1 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _MaskToonColorB2 : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
#endif

#ifdef TOON_EYE

float _RepeatUV = 0.25;
float _RepeatUVAdd = 0;

texture high0TexMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName = "high0Tex";
> ;
sampler2D _High0Tex = sampler_state
{
    Texture = <high0TexMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
float4 _High0Tex_ST;
texture high1TexMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName = "high1Tex";
> ;
sampler2D _High1Tex = sampler_state
{
    Texture = <high1TexMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
texture high2TexMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName = "high2Tex";
> ;
sampler2D _High2Tex = sampler_state
{
    Texture = <high2TexMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
float _Limit;
float4 _Offset;
float _EyePupliScale = 1.0f;

#ifdef USE_EYE_REFLECTION

TEXTURE2D_SAMPLER(_ReflectionTex);
TEXTURE2D_SAMPLER(_ReflectionMask);
texture reflectionTexMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName = "reflectionTex";
> ;
sampler2D _ReflectionTex = sampler_state
{
    Texture = <reflectionTexMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
texture reflectionMaskMap
<
    string ResourceName = "sample_texture/black.tga";
    string ResourceType = "2D";
    string UIName = "reflectionMask";
> ;
sampler2D _ReflectionMask = sampler_state
{
    Texture = <reflectionMaskMap>;
    FILTER = MIN_MAG_MIP_LINEAR;
};
uniform float _ReflectionRate;

#endif  // USE_EYE_REFLECTION

float4 _MainParam0;
float4 _MainParam1;
float4 _HighParam10;// 左目＋共通パラメータ
float4 _HighParam11;// 左目＋共通パラメータ
float4 _HighParam12;// 左目＋共通パラメータ
float4 _HighParam20;// 右目パラメータ
float4 _HighParam21;// 右目パラメータ

#endif // TOON_EYE

// outline
float _OutlineWidth;
float4 _OutlineColor;
float _GlobalOutlineOffset;
float _GlobalOutlineWidth;
float _GlobalCameraFov;

#define PLATFORM_SCALE( x )     (x)
#define OUTLINE_DISTANCE_SCALE  PLATFORM_SCALE(0.0028*_GlobalOutlineWidth)
#define OUTLINE_Z_OFFSET        PLATFORM_SCALE(0.0015 * 0.125 * 100)//gallopではoutlineが負けてしまう
#define OUTLINE_OFFSET          (0.75)    // アウトラインサイズのオフセット

#else // MAYA_HLSL

#include "../../../Common/ShaderCommon.hlsl"
#include "../../../Common/FogCommon.hlsl"

//変数はcbuffer内に定義する
CBUFFER_START(UnityPerMaterial)

TEXTURE2D_SAMPLER_TO(_MainTex);

TEXTURE2D_SAMPLER(_TripleMaskMap);
TEXTURE2D_SAMPLER(_OptionMaskMap);

// _OptionMaskMapを使用するか否か
uniform int _UseOptionMaskMap;

//uniform sampler2D _SpecularMap;
uniform float4 _SpecularColor;
uniform float _SpecularPower;

TEXTURE2D_SAMPLER(_EnvMap);
uniform float _EnvRate;
uniform float _EnvBias;

uniform float _ToonStep;
uniform float _ToonFeather;
TEXTURE2D_SAMPLER(_ToonMap);
uniform float4 _ToonColor;

uniform float4 _ToonBrightColor;
uniform float4 _ToonDarkColor;

// RIM Control
//uniform sampler2D _RimMask;
uniform float _RimStep;
uniform float _RimFeather;
uniform float4 _RimColor;
uniform float _RimShadow;
uniform float _RimSpecRate;

uniform float _FixProjection;
uniform float _CameraLength;
uniform float4 _CharaColor;

TEXTURE2D_SAMPLER_TO(_DirtTex);
uniform float _DirtScale;

uniform sampler2D _WetTex;
uniform float4 _WetTex_ST;
uniform float _WetRate;

TEXTURE2D_SAMPLER(_DitherTex);
#define DITHER_SIZE (4)
uniform float _DitherCutt;

uniform float4 _LightProbeColor;

uniform float _StencilComp;
uniform float _StencilOp;

TEXTURE2D_SAMPLER(_EmissiveTex);
uniform float4 _EmissiveColor;

TEXTURE2D_SAMPLER(_ZekkenNumberTex);
TEXTURE2D_SAMPLER(_ZekkenNameTex);
uniform float4 _ZekkenFontColor;

//TOON Face
uniform float _CheekPretenseThreshold;
uniform float _NosePretenseThreshold;
uniform float _NoseVisibility;
uniform float _TkglinderBlend;
uniform float _HairNormalBlend;
// 顔オブジェクトの上要素ベクトル
uniform float3 _FaceUp;
uniform float3 _FaceForward;
// オリジナルのDirectionalライトを使用するか否か
uniform int _UseOriginalDirectionalLight = 0;
// 顔に当てるライトの位置（0,0,0に顔があるとしてライトの位置）
uniform float3 _OriginalDirectionalLightDir1;
uniform float3 _OriginalDirectionalLightDir2;

//Shadow
// 頂点カラーによるToon補正の強さ（値が1の場合は影響を受けない）
uniform float _faceShadowAlpha;
uniform float _faceShadowEndY;
uniform float _faceShadowLength;
uniform float4 _faceShadowColor;
uniform float4x4 _faceShadowHeadMat;

//Mask Color
TEXTURE2D_SAMPLER(_MaskColorTex);
uniform float4 _MaskColorR1;
uniform float4 _MaskColorR2;
uniform float4 _MaskColorG1;
uniform float4 _MaskColorG2;
uniform float4 _MaskColorB1;
uniform float4 _MaskColorB2;
uniform float4 _MaskToonColorR1;
uniform float4 _MaskToonColorR2;
uniform float4 _MaskToonColorG1;
uniform float4 _MaskToonColorG2;
uniform float4 _MaskToonColorB1;
uniform float4 _MaskToonColorB2;

//UV Emissive
TEXTURE2D_SAMPLER(_UVEmissiveTex);
TEXTURE2D_SAMPLER(_UVEmissiveMaskTex);
uniform float4 _UVEmissiveScroll;
uniform float4 _UVEmissiveRange;
uniform float _UVEmissivePower;

//Color Fade
uniform float4 _FadeColor;
uniform float _FadeRate;

TEXTURE2D_SAMPLER(_OutlineTex);
uniform float _OutlineWidth;
uniform float4 _OutlineColor;
uniform float4 _OutlineParam;
uniform float _OutlineBrightness;

//Cut Off
uniform float _Cutoff;

//高さライトに使用する
uniform float4 _HightLightParam;
uniform float4 _HightLightColor;

//Cheek
uniform float _CheekRate;

#if defined(MINI_EYE)
uniform float4 _UVOffset;
#endif

#ifdef TOON_EYE

TEXTURE2D_SAMPLER_TO(_High0Tex);
TEXTURE2D_SAMPLER(_High1Tex);
TEXTURE2D_SAMPLER(_High2Tex);
uniform float _Limit;
uniform float4 _Offset;
uniform float _EyePupliScale;

#ifdef USE_EYE_REFLECTION

TEXTURE2D_SAMPLER(_ReflectionTex);
TEXTURE2D_SAMPLER(_ReflectionMask);
uniform float _ReflectionRate;

#endif  // USE_EYE_REFLECTION

#endif

#ifdef TOON_SHADING
uniform float _VertexColorToonPower;
#endif

#ifdef TOON_EYE
uniform float4 _MainParam0;
uniform float4 _MainParam1;

uniform float4 _HighParam10;// 左目＋共通パラメータ
uniform float4 _HighParam11;// 左目＋共通パラメータ
uniform float4 _HighParam12;// 左目＋共通パラメータ
uniform float4 _HighParam20;// 右目パラメータ
uniform float4 _HighParam21;// 右目パラメータ

#endif  // TOON_EYE

#if defined(TOON_FACE) || defined(TOON_EYE) || defined(TOON_HAIR)

// 顔の中心から球形に法線を出したいので顔の中心位置をプログラムから渡す
uniform float3 _FaceCenterPos;

#endif

#ifdef TOON_RIM

uniform float _RimShadowRate = 0;

#endif


#if defined(TOON_RIM_CONTROLL)

uniform float _RimHorizonOffset = 0.0;
uniform float _RimVerticalOffset = 0.0;

uniform float _RimStep2 = 0.1;
uniform float _RimFeather2 = 0.01;

uniform float4 _RimColor2 = float4(1, 1, 1, 1);
uniform float _RimSpecRate2 = 0.5;

uniform float _RimHorizonOffset2 = 0.0;
uniform float _RimVerticalOffset2 = 0.0;

uniform float _RimShadowRate2 = 0.0;

#endif

#if defined(USE_DIRT)

uniform float4 _DirtRate;

#endif

#if defined(USE_BLOOM_MASK)
float _BloomMask;
#endif

CBUFFER_END

//以下はshaderのPropertiesに定義されていないもの

uniform float4 _GlobalDirtColor;
uniform float4 _GlobalDirtRimSpecularColor;
uniform float4 _GlobalDirtToonColor;

uniform half4 _GlobalToonColor;
uniform half _GlobalSpecRate = 1;
uniform half4 _GlobalEnvColor;
uniform half4 _GlobalRimColor;
uniform half _GlobalEnvRate;
uniform half _GlobalRimRate = 1;

uniform float _GlobalOutlineOffset;
uniform half _GlobalOutlineWidth;
uniform float _GlobalOutlineColorOffsetScale;

uniform float _GlobalCameraFov;
uniform float4 _GlobalOutlineDepthOffset;

// OptionMaskMapの初期値
static const half4 OptionMaskMapDefault = half4(0.0, 0.0, 0.5, 0.0);

// ゼッケン表示位置。(UVCenter.xy - (UVSize / 2).xy, UVSize.xy)
static const float4 ZekkenNumberFrontOffset = float4(0.51445, 0.66505, 0.2957, 0.2399);
static const float4 ZekkenNumberBackOffset = float4(0.52545, 0.1911, 0.2697, 0.2410);
static const float4 ZekkenNameFrontOffset = float4(0.4173, 0.5361, 0.4588, 0.0626);
static const float4 ZekkenNameBackOffset = float4(0.4212, 0.0676, 0.4568, 0.0676);

#endif  // MAYA_HLSL

#endif  //_DESIGNER_CHARATOON_PROPS_HLSLINC_

