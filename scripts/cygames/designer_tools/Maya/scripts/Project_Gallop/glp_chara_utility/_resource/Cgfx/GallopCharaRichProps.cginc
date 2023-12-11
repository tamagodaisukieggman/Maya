//UNITY_SHADER_NO_UPGRADE

#if defined(MAYA_CGFX)

// un-tweakables

float4x4    UNITY_MATRIX_MVP        : WorldViewProjection;
float4x4    UNITY_MATRIX_MV            : WorldView;
float4x4    UNITY_MATRIX_P            : Projection;
float4x4    UNITY_MATRIX_T_MV        : WorldViewTranspose;
float4x4    UNITY_MATRIX_IT_MV        : WorldViewInverseTranspose;
float4x4    _Object2World            : World;
float4x4    ViewInvXf                : ViewInverse;
float4x4    UNITY_MATRIX_V             : View;
#define        SV_POSITION        POSITION
#define        SV_Target        COLOR
#define        TRANSFORM_TEX(a,b)    a

struct appdata
{
    float4 vertex : POSITION;
    float4 normal : NORMAL;
    float2 uv : TEXCOORD0;
    float4 tangent : TANGENT;
};

struct v2f
{
    float2 uv : TEXCOORD0;
    float3 normal : TEXCOORD1;
    float3 eyedir : TEXCOORD2;
    float3 vnormal : TEXCOORD3;
    float4 vertex : SV_POSITION;
};

texture mainTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "mainTexture";
>;
sampler2D _MainTex = sampler_state
{
    Texture = <mainTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};
float4 _MainTex_ST;
texture controlTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "controlTexture";
>;
sampler2D _ControlMap = sampler_state
{
    Texture = <controlTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};

float _RimNormalAdjust <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 0.0;
float _RimPower <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 8.0;
    float UIStep = 0.1;
> = 4.0;
float _RimRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float4 _RimColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };
float _RimShadow <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 0.0;
float _RimSpecRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 0.0;

float _ToonRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _ToonOffset <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 0.0;

texture specularTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "Map with dot-half-angle factors";
>;
sampler2D _SpecTex = sampler_state
{
    Texture = <specularTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
};
float _SpecPower <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 64.0;
    float UIStep = 0.1;
> = 16.0;
float _SpecRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float3 _SpecColor : Ambient<
    string UIWidget = "Color";
> = { 1,1,1 };
float3 _CharaColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

float3 _ShadowColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
texture toonTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "Map with dot-half-angle factors";
>;
sampler2D _ShadowTex = sampler_state
{
    Texture = <toonTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
};

texture envTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "Map with dot-half-angle factors";
>;
sampler2D _GlobalEnvTex = sampler_state
{
    Texture = <envTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
    WrapS = ClampToEdge;
    WrapT = ClampToEdge;
};
float3 _GlobalEnvColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };
float _GlobalEnvRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _EnvRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _EnvBias <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.5;

float _GlobalToonRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _GlobalSpecRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _GlobalRimRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 1.0;
float _GlobalRimShadowRate <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 2.0;
    float UIStep = 0.1;
> = 0.0;
float4 _GlobalLightDir = { 0,1,0,0 };


#else

struct appdata
{
    float4 vertex : POSITION;
    float4 normal : NORMAL;
    float2 uv : TEXCOORD0;
    float4 tangent : TANGENT;
};

struct v2f
{
    float2 uv : TEXCOORD0;
    float3 normal : TEXCOORD1;
    float3 vnormal : TEXCOORD2;
    float4 vertex : SV_POSITION;
};

uniform sampler2D _MainTex;
uniform float4 _MainTex_ST;
uniform sampler2D _ControlMap;

uniform float _RimNormalAdjust;
uniform float _RimPower;
uniform float _RimRate;
uniform float4 _RimColor;
uniform float _RimShadow;
uniform float _RimSpecRate;

uniform float _ToonRate;
uniform float _ToonOffset;

uniform sampler2D _SpecTex;
uniform float _SpecPower;
uniform float _SpecRate;
uniform float4 _SpecColor;
uniform float4 _CharaColor;

uniform float4 _ShadowColor;
uniform sampler2D _ShadowTex;

uniform sampler2D _GlobalEnvTex;
uniform float4 _GlobalEnvColor;
uniform half _GlobalEnvRate;
uniform half _EnvRate;
uniform half _EnvBias;

uniform half _GlobalToonRate = 1;
uniform half _GlobalSpecRate = 1;
uniform half _GlobalRimRate = 1;
uniform half _GlobalRimShadowRate = 0;
uniform half4 _GlobalLightDir;

#endif
