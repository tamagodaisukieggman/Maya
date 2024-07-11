//UNITY_SHADER_NO_UPGRADE

#if defined(MAYA_HLSL)
// // Maya用コード

#define TOON_EYE
#include "GallopCharaToonProps.fx"

#else // MAYA_HLSL

//Eyeは必須でTOON_EYEを定義しておく
#define TOON_EYE
#include "GallopCharaToonProps.hlsl"

#endif // MAYA_HLSL

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
    float3 rawTkglinderNormal = posWorld - (_FaceCenterPos.xyz + (dot(_FaceUp, vtxVector) * _FaceUp));
    float3 cylinderNormal = normalize(rawTkglinderNormal);
    normal = lerp(mul(GetObjectToWorldMatrix(),float4(normal,0)).xyz, cylinderNormal, _TkglinderBlend);

    // 顔ライティングの場合法線はすでにモデルマトリックスと計算済みなのでそのまま使う
    o.normalDir = normal;
    o.vnormal = mul(GetWorldToViewMatrix(), float4(normal,0)).xyz;

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

        uv2 = CalcUV(uvTemp + _MainParam0.xy, _MainParam0.z);
        o.uv = TRANSFORM_TEX(uv2, _MainTex);
#if defined(MAYA_HLSL)
        // Maya用のコード
        o.uv.x = o.uv.x * _RepeatUV + _RepeatUVAdd;
#endif

        uvTemp = v.uv2 - 0.5;
        //左
        uv2 = CalcUV(uvTemp + _HighParam10.xy, _HighParam10.z);
        uv2 += _Offset.xy;
        o.uv0 = TRANSFORM_TEX(uv2, _High0Tex);
        uv2 = CalcUV(uvTemp + _HighParam11.xy, _HighParam11.z);
        o.uv1 = TRANSFORM_TEX(uv2, _High0Tex);

        o.kiraParam.x = _HighParam10.w;
        o.kiraParam.y = _HighParam11.w;
    }
    else
    {
#ifdef USE_EYE_REFLECTION
        o.refl.y = v.uv.y * 2.0;
#endif

        uv2 = CalcUV(uvTemp + _MainParam1.xy, _MainParam1.z);
        o.uv = TRANSFORM_TEX(uv2, _MainTex);
#if defined(MAYA_HLSL)
        // Maya用のコード
        o.uv.x = o.uv.x * _RepeatUV + _RepeatUVAdd;
#endif

        uvTemp = v.uv2 - 0.5;
        //右
        uv2 = CalcUV(uvTemp + _HighParam20.xy, _HighParam20.z);
        uv2 += _Offset.zw;
        o.uv0 = TRANSFORM_TEX(uv2, _High0Tex);
        uv2 = CalcUV(uvTemp + _HighParam21.xy, _HighParam21.z);
        o.uv1 = TRANSFORM_TEX(uv2, _High0Tex);

        o.kiraParam.x = _HighParam20.w;
        o.kiraParam.y = _HighParam21.w;
    }

    //2番目のパラメータのみ共有されている
    uvTemp = v.uv3 - 0.5;

    uv2 = CalcUV(uvTemp + _HighParam12.xy, _HighParam12.z);
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
    fixed4 refColor = TEX2D_SAMPLE(_ReflectionTex, i.refl);
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

    kira0 = TEX2D_SAMPLE(_High2Tex, i.uv2).r * _HighParam12.w;
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

    Light lightData = GetMainLight();

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
    half3 lightDirection1 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir1), step(1, (float)_UseOriginalDirectionalLight));
    half3 lightDirection2 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir2), step(1, (float)_UseOriginalDirectionalLight));
#else
    // Unity用のコード
    half3 lightDirection1 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir1), step(1, _UseOriginalDirectionalLight));
    half3 lightDirection2 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir2), step(1, _UseOriginalDirectionalLight));
#endif

    half halfLambert = min(1, (0.5 * dot(i.normalDir, lightDirection1) + 0.5) + (0.5 * dot(i.normalDir, lightDirection2) + 0.5));
    half3 halfDirection = normalize(viewDirection + lightDirection1);

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

#ifdef USE_BLOOM_MASK
    return _BloomMask;
#endif

    return col;
}
