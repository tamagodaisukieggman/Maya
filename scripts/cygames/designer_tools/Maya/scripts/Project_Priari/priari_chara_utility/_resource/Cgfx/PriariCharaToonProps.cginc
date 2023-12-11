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
#define TRANSFORM_TEX(a,b)    (a.xy * b##_ST.xy + b##_ST.zw)
#define _WorldSpaceCameraPos UNITY_MATRIX_V[3]
#define UnityObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)
#define PriariObjectToClipPos(a) mul(UNITY_MATRIX_MVP,a)

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
float4 _MainTex_ST = {1.0f, 1.0f, 0.0f, 0.0f};

texture tripleMaskMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName =  "tripleMask";
>;
sampler2D _TripleMaskMap = sampler_state
{
    Texture = <tripleMaskMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};

texture optionMaskMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName =  "optionMask";
>;
sampler2D _OptionMaskMap = sampler_state
{
    Texture = <optionMaskMap>;
    MinFilter = Linear;
    MagFilter = Linear;
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

texture envTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName =  "Map with dot-half-angle factors";
>;
sampler2D _EnvMap = sampler_state
{
    Texture = <envTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
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

texture toonTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName =  "toonTexture";
>;
sampler2D _ToonMap = sampler_state
{
    Texture = <toonTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
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
texture dirtTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName =  "dirtTexture";
>;
sampler2D _DirtTex = sampler_state
{
    Texture = <dirtTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
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

float3 _GlobalDirtColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

float3 _GlobalDirtToonColor : Ambient <
    string UIWidget = "Color";
> = { 0.25,0.15,0.12 };


float3 _GlobalDirtRimSpecularColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

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
float3 _CharaColor : Ambient <
    string UIWidget = "Color";
> = {1,1,1};

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

texture ditherTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "dirtTexture";
>;
sampler2D _DitherTex = sampler_state
{
    Texture = <dirtTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
};
float _DitherCutt <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.1;
> = 0.0;

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
float _CylinderBlend <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.001;
> = 0.0;
float _HairNormalBlend <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.001;
> = 1.0;
float3 _FaceUp = { 0,1,0 };
float3 _FaceForward = { 0,0,1 };
float3 _FaceCenterPos = { 0,0,0 };
#endif

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
texture maskColorTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "maskColorTexture";
> ;
sampler2D _MaskColorTex = sampler_state
{
    Texture = <maskColorTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
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

#else

uniform sampler2D _MainTex;
uniform float4 _MainTex_ST;

uniform sampler2D _TripleMaskMap;
uniform sampler2D _OptionMaskMap;
// _OptionMaskMapを使用するか否か
uniform int _UseOptionMaskMap;

//uniform sampler2D _SpecularMap;
uniform half4 _SpecularColor;
uniform half _SpecularPower;

uniform sampler2D _EnvMap;
uniform half _EnvRate;
uniform half _EnvBias;

uniform half _ToonStep;
uniform half _ToonFeather;
uniform sampler2D _ToonMap;
uniform half4 _ToonColor;

uniform half4 _ToonBrightColor;
uniform half4 _ToonDarkColor;

//uniform sampler2D _RimMask;
uniform half _RimStep;
uniform half _RimFeather;
uniform half4 _RimColor;
uniform half _RimShadow;
uniform half _RimSpecRate;
uniform float _RimShadowRate = 0;

#if defined(TOON_RIM_CONTROLL)

uniform half _RimHorizonOffset = 0.0;
uniform half _RimVerticalOffset = 0.0;

uniform half _RimStep2 = 0.1;
uniform half _RimFeather2 = 0.01;
uniform half4 _RimColor2 = half4(1,1,1,1);
uniform half _RimSpecRate2 = 0.5;

uniform half _RimHorizonOffset2 = 0.0;
uniform half _RimVerticalOffset2 = 0.0;

uniform float _RimShadowRate2 = 0.0;

#endif // TOON_RIM_CONTROLL

uniform float _FixProjection;
uniform float _CameraLength;
uniform half _Cutoff;
uniform half4 _CharaColor;

#if defined(USE_DIRT)
uniform sampler2D _DirtTex;
uniform float4 _DirtTex_ST;
uniform float _DirtRate[3];
uniform float4 _GlobalDirtColor;
uniform float4 _GlobalDirtRimSpecularColor;
uniform float4 _GlobalDirtToonColor;
uniform float _DirtScale;
#endif
#if defined(USE_WET)
uniform sampler2D _WetTex;
uniform float4 _WetTex_ST;
uniform float _WetRate;
#endif

half4 _GlobalToonColor;
uniform half _GlobalSpecRate = 1;
uniform half4 _GlobalEnvColor;
uniform half4 _GlobalRimColor;
uniform half _GlobalEnvRate;
uniform half _GlobalRimRate = 1;

#ifdef USE_DITHER
uniform sampler2D _DitherTex;
#define DITHER_SIZE (4)
uniform float _DitherCutt;
#endif

uniform half4 _LightProbeColor;

uniform float _StencilComp;
uniform float _StencilOp;

uniform sampler2D _EmissiveTex;
uniform half4 _EmissiveColor;

#ifdef ZEKKEN_TEX
uniform sampler2D _ZekkenNumberTex;
uniform sampler2D _ZekkenNameTex;
uniform half4 _ZekkenFontColor;
#endif

#if defined(TOON_FACE) || defined(TOON_HAIR)

uniform half _CheekPretenseThreshold;

uniform half _NosePretenseThreshold;

uniform half _NoseVisibility;

uniform half _CylinderBlend;

uniform half _HairNormalBlend;

// 顔オブジェクトの上要素ベクトル
uniform float3 _FaceUp;

uniform float3 _FaceForward;

// 顔の中心から球形に法線を出したいので顔の中心位置をプログラムから渡す
uniform float3 _FaceCenterPos;

#endif

// オリジナルのDirectionalライトを使用するか否か
uniform int _UseOriginalDirectionalLight = 0;

// 顔に当てるライトの位置（0,0,0に顔があるとしてライトの位置）
uniform float3 _OriginalDirectionalLightDir;

#ifdef TOON_SHADING
// 頂点カラーによるToon補正の強さ（値が1の場合は影響を受けない）
uniform half _VertexColorToonPower;
#endif

#ifdef TOON_FACE_SHADOW
uniform float _faceShadowAlpha;
uniform float _faceShadowEndY;
uniform float _faceShadowLength;
uniform half4 _faceShadowColor;
uniform float4x4 _faceShadowHeadMat;
#endif

#ifdef USE_HIGHT_LIGHT
//高さライトに使用する
half4 _HightLightParam;
float4 _HightLightColor;

#endif

#ifdef USE_MASK_COLOR
uniform sampler2D _MaskColorTex;
uniform half4 _MaskColorR1;
uniform half4 _MaskColorR2;
uniform half4 _MaskColorG1;
uniform half4 _MaskColorG2;
uniform half4 _MaskColorB1;
uniform half4 _MaskColorB2;
uniform half4 _MaskToonColorR1;
uniform half4 _MaskToonColorR2;
uniform half4 _MaskToonColorG1;
uniform half4 _MaskToonColorG2;
uniform half4 _MaskToonColorB1;
uniform half4 _MaskToonColorB2;
#endif

#endif
