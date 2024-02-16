//UNITY_SHADER_NO_UPGRADE

#if defined(MAYA_HLSL)
// Maya用コード

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

static const half4 OptionMaskMapDefault = half4(0.0, 0.0, 0.5, 0.0);

row_major float4x4 GetObjectToWorldMatrix(){
    return UNITY_MATRIX_M;
}

float _RepeatUV = 0.25;
float _RepeatUVAdd = 0;

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
    string UIName = "Light Position";
    string Space = "World";
> = {1.0f, 0.0f, 0.0f};

float4 _CharaColor : Ambient <
    string UIWidget = "Color";
> = {1,1,1,1};

float3 _LightProbeColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1 };

float3 _LightColor0 : Specular <
    string UIName = "Lamp 0";
    string Object = "Pointlight0";
    string UIWidget = "Color";
> = { 1.0f,1.0f,1.0f };


Light GetMainLight()
{
    Light outLight = (Light)0;
    outLight.color = _LightColor0.rgb;
    outLight.direction = _WorldSpaceLightPos0;
    return outLight;
}

texture mainTextureMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "mainTexture";
> ;
sampler2D _MainTex = sampler_state
{
    Texture = <mainTextureMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};
float4 _MainTex_ST;

texture high0TexMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "high0Tex";
> ;
sampler2D _High0Tex = sampler_state
{
    Texture = <high0TexMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};
float4 _High0Tex_ST;
texture high1TexMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "high1Tex";
> ;
sampler2D _High1Tex = sampler_state
{
    Texture = <high1TexMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};
texture high2TexMap
<
    string ResourceName = "ctHalf.dds";
    string ResourceType = "2D";
    string UIName = "high2Tex";
> ;
sampler2D _High2Tex = sampler_state
{
    Texture = <high2TexMap>;
    MinFilter = Linear;
    MagFilter = Linear;
};

float4 _MainParam0;
float4 _MainParam1;
float4 _HighParam10;
float4 _HighParam11;
float4 _HighParam12;
float4 _HighParam20;
float4 _HighParam21;

float _Limit;

float4 _Offset;

#ifdef TOON_EYE
float4 _GlobalToonColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };

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
float4 _ToonColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,1 };
float4 _ToonBrightColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,0 };
float4 _ToonDarkColor : Ambient <
    string UIWidget = "Color";
> = { 1,1,1,0 };

float _CylinderBlend <
    string UIWidget = "slider";
    float UIMin = 0.0;
    float UIMax = 1.0;
    float UIStep = 0.001;
> = 0.0;

float3 _FaceUp = { 0,1,0 };
float3 _FaceForward = { 0,0,1 };
float3 _FaceCenterPos = { 0,0,0 };

int _UseOriginalDirectionalLight <
    string UIWidget = "slider";
    int UIMin = 0;
    int UIMax = 2;
    int UIStep = 1;
> = 0;

float3 _OriginalDirectionalLightDir = { 0,0,1 };
float _EyePupliScale = 1.0;

#endif // TOON_EYE

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
#endif

// outline
float _OutlineWidth;
float4 _OutlineColor;
float _GlobalOutlineOffset;
float _GlobalOutlineWidth;
float _GlobalCameraFov;

// MayaではShaderCommon.hlslを参照しないためこちらで定義
#define PLATFORM_SCALE( x )     (x)
#define OUTLINE_DISTANCE_SCALE  PLATFORM_SCALE(0.0028*_GlobalOutlineWidth)
#define OUTLINE_Z_OFFSET        PLATFORM_SCALE(0.0015 * 0.125 * 100)//gallopではoutlineが負けてしまう
#define OUTLINE_OFFSET          (0.75)    // アウトラインサイズのオフセット

#else

// Unity用のコード
#include "../../../Common/ShaderCommon.hlsl"
#include "../../../Common/FogCommon.hlsl"

CBUFFER_START(UnityPerMaterial)

uniform fixed4 _CharaColor;
uniform fixed4 _LightProbeColor;
TEXTURE2D_SAMPLER_TO(_MainTex);
uniform float _FixProjection;// 正射影率.
uniform float _CameraLength;
uniform float _Saturation = 1.0;

TEXTURE2D_SAMPLER_TO(_High0Tex);
TEXTURE2D_SAMPLER(_High1Tex);
TEXTURE2D_SAMPLER(_High2Tex);

uniform half4 _MainParam[2];
// SHV33で、4つ以上の配列を分割しないと値が正しく取得出来ないため
uniform half4 _HighParam1[3];// 左目＋共通パラメータ
uniform half4 _HighParam2[2];// 右目パラメータ

uniform float _Limit;

uniform half4 _Offset;

uniform float _StencilComp;
uniform float _StencilOp;

#ifdef USE_DITHER
#define DITHER_SIZE (4)
uniform float _DitherCutt;
TEXTURE2D_SAMPLER(_DitherTex);
#endif

#ifdef TOON_EYE
uniform half4 _GlobalToonColor;

uniform half _ToonStep;
uniform half _ToonFeather;
uniform half4 _ToonColor;
uniform half4 _ToonBrightColor;
uniform half4 _ToonDarkColor;

uniform half _CylinderBlend;

// 顔オブジェクトの上要素ベクトル
uniform float3 _FaceUp;

uniform float3 _FaceForward;

// 顔の中心から球形に法線を出したいので顔の中心位置をプログラムから渡す
uniform float3 _FaceCenterPos;

// オリジナルのDirectionalライトを使用するか否か
uniform int _UseOriginalDirectionalLight;

// 顔に当てるライトの位置（0,0,0に顔があるとしてライトの位置）
uniform float3 _OriginalDirectionalLightDir;

uniform half _EyePupliScale;

#endif // TOON_EYE

#ifdef USE_MASK_COLOR
TEXTURE2D_SAMPLER(_MaskColorTex);
uniform float4 _MaskColorR1;
uniform float4 _MaskColorR2;
uniform float4 _MaskColorG1;
uniform float4 _MaskColorG2;
uniform float4 _MaskColorB1;
uniform float4 _MaskColorB2;
#endif

#ifdef USE_EYE_REFLECTION

TEXTURE2D_SAMPLER(_ReflectionTex);
TEXTURE2D_SAMPLER(_ReflectionMask);
uniform float _ReflectionRate;
uniform half4 _ReflectionOffsetScaleUV;

#endif

#ifdef USE_COLOR_FADE
uniform float4 _FadeColor;
uniform float _FadeRate;
#endif

CBUFFER_END

#endif

struct appdata_t
{
    float3 vertex : POSITION;
    float3 normal : NORMAL;
    float2 uv : TEXCOORD0;
    float2 uv2 : TEXCOORD1;
    float2 uv3 : TEXCOORD2;
};

#if defined(MAYA_HLSL)
// Maya用のコード.Mayaだと TEXCOORD0～7までらしい。Fog,Dither使わないので消して代用する。
struct v2f
{
    float4 pos : SV_POSITION;
    float2 uv  : TEXCOORD0;
    float2 uv0  : TEXCOORD1;
    float2 uv1  : TEXCOORD2;
    float2 uv2  : TEXCOORD3;

    float2 kiraParam  : TEXCOORD6;

#ifdef TOON_EYE
    float3 normalDir : TEXCOORD7;
    float3 posWorld : TEXCOORD4;
    float3 vnormal : TEXCOORD5;
#endif // TOON_EYE
};
#else
// Unity用のコード
struct v2f
{
    float4 pos : SV_POSITION;
    float2 uv  : TEXCOORD0;
    float2 uv0  : TEXCOORD1;
    float2 uv1  : TEXCOORD2;
    float2 uv2  : TEXCOORD3;

#ifdef USE_FOG
    float2 fogParam : TEXCOORD4;
#endif

#ifdef USE_DITHER
    float4 ditherPos : TEXCOORD5;
#endif

    float2 kiraParam  : TEXCOORD6;

#ifdef TOON_EYE
    float3 normalDir : TEXCOORD7;
    float3 posWorld : TEXCOORD8;
    float3 vnormal : TEXCOORD9;
#endif // TOON_EYE

#ifdef USE_EYE_REFLECTION

    float2 refl  : TEXCOORD10;  //Reflection UV

#endif
};

#endif

float2 CalcUV(float2 uv, float angle)
{
    float s = sin(angle);
    float c = cos(angle);
    float x = (uv.x) * c - (uv.y) * s;
    float y = (uv.x) * s + (uv.y) * c;
    return float2(x, y) + 0.5;
}

#ifdef USE_DITHER

float4 CalcDitherPos(float4 pos)
{
    float4 screenPos = ComputeScreenPos(pos);
    return float4(screenPos.xy * _ScreenParams.xy / DITHER_SIZE, 0, screenPos.w);
}

void ClipDither(float4 ditherPos)
{
    float ditherColor = TEX2D_SAMPLE(_DitherTex, ditherPos.xy / ditherPos.w).r;
    if (ditherColor <= _DitherCutt) discard;
}

#endif

v2f vert(appdata_t v)
{
    v2f o = (v2f)0;
    VertexPositionInputs vpi = GallopGetVertexPositionInputs(v.vertex);
    o.pos = vpi.positionCS * _EyePupliScale;

#ifdef TOON_EYE
    float3 posWorld = vpi.positionWS;

    float3 normal = v.normal;

    // 顔用のライティング処理
    float3 vtxVector = posWorld - _FaceCenterPos.xyz;
    float3 rawCylinderNormal = posWorld - (_FaceCenterPos.xyz + (dot(_FaceUp, vtxVector) * _FaceUp));
    float3 cylinderNormal = normalize(rawCylinderNormal);
    normal = lerp(mul(GetObjectToWorldMatrix(), float4(normal, 0)).xyz, cylinderNormal, _CylinderBlend);

    // 顔ライティングの場合法線はすでにモデルマトリックスと計算済みなのでそのまま使う
    o.normalDir = normal;
    o.vnormal = mul(GetWorldToViewMatrix(), float4(normal, 0)).xyz;

    o.posWorld = posWorld;

#endif // TOON_EYE

    float2 uv2;
    float2 uvTemp = v.uv - 0.5;

#ifdef USE_EYE_REFLECTION
    //Yは左右の目によって基準が違うので調整が必要
    o.refl.x = v.uv.x;
#endif

    if (v.uv.y >= 0.5)
    {
#ifdef USE_EYE_REFLECTION
        o.refl.y = (v.uv.y - 0.5) * 2.0;
#endif

#if defined(MAYA_HLSL)
        // Maya用のコード
        uv2 = CalcUV(uvTemp + _MainParam0.xy, _MainParam0.z);
        o.uv = TRANSFORM_TEX(uv2, _MainTex);
        o.uv.x = o.uv.x * _RepeatUV + _RepeatUVAdd;

        uvTemp = v.uv2 - 0.5;
        //左
        uv2 = CalcUV(uvTemp + _HighParam10.xy, _HighParam10.z);
        uv2 += _Offset.xy;
        o.uv0 = TRANSFORM_TEX(uv2, _High0Tex);
        uv2 = CalcUV(uvTemp + _HighParam11.xy, _HighParam11.z);
        o.uv1 = TRANSFORM_TEX(uv2, _High0Tex);

        o.kiraParam.x = _HighParam10.w;
        o.kiraParam.y = _HighParam11.w;
#else
        // Unity用のコード
        uv2 = CalcUV(uvTemp + _MainParam[0].xy, _MainParam[0].z);
        o.uv = TRANSFORM_TEX(uv2, _MainTex);

        uvTemp = v.uv2 - 0.5;
        //左
        uv2 = CalcUV(uvTemp + _HighParam1[0].xy, _HighParam1[0].z);
        uv2 += _Offset.xy;
        o.uv0 = TRANSFORM_TEX(uv2, _High0Tex);
        uv2 = CalcUV(uvTemp + _HighParam1[1].xy, _HighParam1[1].z);
        o.uv1 = TRANSFORM_TEX(uv2, _High0Tex);

        o.kiraParam.x = _HighParam1[0].w;
        o.kiraParam.y = _HighParam1[1].w;
#endif
    }
    else
    {
#ifdef USE_EYE_REFLECTION
        o.refl.y = v.uv.y * 2.0;
#endif

#if defined(MAYA_HLSL)
        // Maya用のコード
        uv2 = CalcUV(uvTemp + _MainParam1.xy, _MainParam1.z);
        o.uv = TRANSFORM_TEX(uv2, _MainTex);
        o.uv.x = o.uv.x * _RepeatUV + _RepeatUVAdd;

        uvTemp = v.uv2 - 0.5;
        //右
        uv2 = CalcUV(uvTemp + _HighParam20.xy, _HighParam20.z);
        uv2 += _Offset.zw;
        o.uv0 = TRANSFORM_TEX(uv2, _High0Tex);
        uv2 = CalcUV(uvTemp + _HighParam21.xy, _HighParam21.z);
        o.uv1 = TRANSFORM_TEX(uv2, _High0Tex);

        o.kiraParam.x = _HighParam20.w;
        o.kiraParam.y = _HighParam21.w;
#else
        // Unity用のコード
        uv2 = CalcUV(uvTemp + _MainParam[1].xy, _MainParam[1].z);
        o.uv = TRANSFORM_TEX(uv2, _MainTex);

        uvTemp = v.uv2 - 0.5;
        //右
        uv2 = CalcUV(uvTemp + _HighParam2[0].xy, _HighParam2[0].z);
        uv2 += _Offset.zw;
        o.uv0 = TRANSFORM_TEX(uv2, _High0Tex);
        uv2 = CalcUV(uvTemp + _HighParam2[1].xy, _HighParam2[1].z);
        o.uv1 = TRANSFORM_TEX(uv2, _High0Tex);

        o.kiraParam.x = _HighParam2[0].w;
        o.kiraParam.y = _HighParam2[1].w;
#endif
    }

    //2番目のパラメータのみ共有されている
    uvTemp = v.uv3 - 0.5;

#if defined(MAYA_HLSL)
    // Maya用のコード
    uv2 = CalcUV(uvTemp + _HighParam12.xy, _HighParam12.z);
#else
    // Unity用のコード
    uv2 = CalcUV(uvTemp + _HighParam1[2].xy, _HighParam1[2].z);
#endif
    o.uv2 = TRANSFORM_TEX(uv2, _High0Tex);

#ifdef USE_FIXPROJECTION
    // Blend projection (Perspective)
    float2 pos = o.pos.xy * o.pos.w / _CameraLength;
    o.pos.xy = lerp(o.pos.xy, pos.xy, _FixProjection);
#endif

#ifdef USE_FOG
    o.fogParam = CalcFogParamOriginFromVertex(v.vertex);
#endif

#ifdef USE_DITHER
    o.ditherPos = CalcDitherPos(o.pos);
#endif

    return o;
}

fixed4 frag(v2f i) : COLOR
{
#ifdef USE_DITHER
    ClipDither(i.ditherPos);
#endif

    float2 uv = i.uv;
    fixed4 col = TEX2D_SAMPLE(_MainTex, uv);
    float kira0;
    float kira1;

#ifdef USE_MASK_COLOR
    half4 colorMask = TEX2D_SAMPLE(_MaskColorTex, i.uv);
    // 0.49～0にかけて_MaskColorR1を、0.51～1にかけて_MaskColorR2を使用する。
    // 0.49～0.51については色は触らない。
    half r1 = (0.49 - min(0.49, colorMask.r)) * (1 / 0.49);
    half r2 = (max(0.51, colorMask.r) - 0.51) * (1 / 0.49);
    half g1 = (0.49 - min(0.49, colorMask.g)) * (1 / 0.49);
    half g2 = (max(0.51, colorMask.g) - 0.51) * (1 / 0.49);
    half b1 = (0.49 - min(0.49, colorMask.b)) * (1 / 0.49);
    half b2 = (max(0.51, colorMask.b) - 0.51) * (1 / 0.49);

    col.rgb *= lerp(1, _MaskColorR1.rgb, r1).rgb;
    col.rgb *= lerp(1, _MaskColorR2.rgb, r2).rgb;
    col.rgb *= lerp(1, _MaskColorG1.rgb, g1).rgb;
    col.rgb *= lerp(1, _MaskColorG2.rgb, g2).rgb;
    col.rgb *= lerp(1, _MaskColorB1.rgb, b1).rgb;
    col.rgb *= lerp(1, _MaskColorB2.rgb, b2).rgb;
#endif // USE_MASK_COLOR

#ifdef USE_EYE_REFLECTION
    //RGでUV動かしてもいいがデフォルトテクスチャを(1,0.5,0.5)と外部設定前提になってしまうので、ずらすのは止めておく
    half4 refRate = TEX2D_SAMPLE(_ReflectionMask, i.refl);
    fixed4 refColor = TEX2D_SAMPLE(_ReflectionTex, _ReflectionOffsetScaleUV.xy + i.refl * _ReflectionOffsetScaleUV.zw);
    col = lerp(col, refColor, _ReflectionRate * refRate.r * refColor.a);
#endif

    kira0 = TEX2D_SAMPLE(_High0Tex, i.uv0).r * i.kiraParam.x;
    kira0 = kira0 - _Limit;
    kira1 = -kira0;
    //MemoPadにてsignが使用できない(0xFFFFFFが-1にならない)ので同じことを行う
    if (kira0 < 0.0)
    {
        kira0 = 0.0;
        kira1 = -1.0;
    }
    else if(kira0 > 0.0)
    {
        kira0 = 1.0;
        kira1 = 0.0;
    }
    col.rgb += max(0.0, kira0 + kira1);

    kira0 = TEX2D_SAMPLE(_High1Tex, i.uv1).r * i.kiraParam.y;
    kira0 = kira0 - _Limit;
    kira1 = -kira0;
    if (kira0 < 0.0)
    {
        kira0 = 0.0;
        kira1 = -1.0;
    }
    else if (kira0 > 0.0)
    {
        kira0 = 1.0;
        kira1 = 0.0;
    }
    col.rgb += max(0.0, kira0 + kira1);

#if defined(MAYA_HLSL)
    // Maya用のコード
    kira0 = TEX2D_SAMPLE(_High2Tex, i.uv2).r * _HighParam12.w;
#else
    // Unity用のコード
    kira0 = TEX2D_SAMPLE(_High2Tex, i.uv2).r * _HighParam1[2].w;
#endif
    kira0 = kira0 - _Limit;
    kira1 = -kira0;
    if (kira0 < 0.0)
    {
        kira0 = 0.0;
        kira1 = -1.0;
    }
    else if (kira0 > 0.0)
    {
        kira0 = 1.0;
        kira1 = 0.0;
    }
    col.rgb += max(0.0, kira0 + kira1);

#if defined(USE_LIGHT_COLOR) || defined(TOON_EYE)

#if defined(BUILDIN_PIPELINE)
    Light lightData;
    lightData.color = _LightColor0.rgb;
    lightData.direction = _WorldSpaceLightPos0.xyz;

#else
    Light lightData = GetMainLight();
#endif

#endif


#ifdef USE_LIGHT_COLOR
    col.rgb *= lightData.color;
#endif

#ifdef TOON_EYE

    fixed4 baseColor = col;

    half3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld);

    // DirectionalLightの位置（共通か固有か）
    // _UseOriginalDirectionalLightが1以上であれば固有DirectinalLightを使用する
#if defined(MAYA_HLSL)
    // Maya用のコード
    half3 lightDirection = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir), step(1, (float)_UseOriginalDirectionalLight));
#else
    // Unity用のコード
    half3 lightDirection = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir), step(1, _UseOriginalDirectionalLight));
#endif

    half halfLambert = 0.5 * dot(i.normalDir, lightDirection) + 0.5;
    half3 halfDirection = normalize(viewDirection + lightDirection);

    half shading = halfLambert;
    half shadingTemp = (_ToonStep - _ToonFeather);
    // _ToonFeatherが0以下だった場合はfinalShadowを0にする
    half finalShadow = lerp(saturate((1 + (shadingTemp - shading) / (_ToonFeather))), 0, step(_ToonFeather, 0));

    half3 toonColor = baseColor.rgb * _GlobalToonColor.rgb * 0.7;

    // Toonの明るい部分の色補正
    half mulStep = step(_ToonBrightColor.a, 0.5);
    half addStep = 1 - mulStep;
    baseColor.rgb = baseColor.rgb * lerp(half3(1, 1, 1), _ToonBrightColor.rgb, mulStep) + (_ToonBrightColor.rgb * addStep);

    // Toonの暗い部分の色補正
    mulStep = step(_ToonDarkColor.a, 0.5);
    addStep = 1 - mulStep;
    toonColor.rgb = toonColor.rgb * lerp(half3(1, 1, 1), _ToonDarkColor.rgb, mulStep) + (_ToonDarkColor.rgb * addStep);

    baseColor.rgb = lerp(baseColor.rgb, toonColor.rgb, finalShadow);

    col = baseColor;
#endif // TOON_EYE

    col.rgb *= _CharaColor.rgb * _LightProbeColor.rgb;

#ifdef USE_FOG
    //Fogの影響は最後に受ける
    col.rgb = ApplyFog(i.fogParam.x, i.fogParam.y, col).rgb;
#endif

#ifdef USE_ALPHA
    col.a = _CharaColor.a;
#endif

#ifdef USE_COLOR_FADE
    col.rgb = lerp(col.rgb, _FadeColor.rgb,_FadeColor.a);
    col.a *= _FadeRate;
#endif

    // 彩度
    col.rgb = ColorSaturation(col.rgb, _Saturation);

    return col;
}
