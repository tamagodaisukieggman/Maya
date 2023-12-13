//UNITY_SHADER_NO_UPGRADE

#if defined(MAYA_HLSL)
#include "GallopCharaToonProps.fx"
#else
#include "GallopCharaToonProps.hlsl"
#endif // MAYA_HLSL

struct appdata_t
{
#if defined(MAYA_HLSL)
    float4 vertex : POSITION;
    float3 normal : NORMAL;
    float2 texcoord : TEXCOORD0;
    float4 color : COLOR;
#else
    float3 vertex : POSITION;
    float3 normal : TANGENT;
    float2 texcoord : TEXCOORD0;
    fixed4 color : COLOR;
#endif // MAYA_HLSL
};

struct v2f
{
    float4 pos : SV_POSITION;
    float2 uv  : TEXCOORD0;

#if defined(USE_FOG)
    float2 fogParam : TEXCOORD1;
#endif
#ifdef USE_DITHER
    float4 ditherPos : TEXCOORD2;
#endif

};

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
    //    太さとオフセットの調整機能を入れた処理
    o.pos = GallopObjectToClipPos(v.vertex);

    //    FOVの値を反映する
    float fov_offset = _GlobalCameraFov;
    float transform_offset = OUTLINE_OFFSET + (fov_offset / 2.0);

#if defined(MAYA_HLSL)  
    // Mayaは法線方向をそのまま使う。offsetは係数をかけてUnityと数値を合わせる
    float adjust_unity_coefficient = 10.0;
    float4 norm = mul(UNITY_MATRIX_MVP, float4(v.normal, 0.0));
    float2 offset = norm.xy * transform_offset * adjust_unity_coefficient;
#else
    float4 norm = mul(UNITY_MATRIX_IT_MV, float4(v.normal, 0.0));
    float2 offset = TransformWViewToHClip(norm.xyz).xy * transform_offset;
#endif
    
    //    手前が太くなりすぎず、奥が細くなりすぎないように調整
    o.pos.xy += offset.xy * (v.color.r * OUTLINE_DISTANCE_SCALE * _OutlineWidth);

    float z_offset = OUTLINE_Z_OFFSET * (1.0 - v.color.g) * fov_offset * _GlobalOutlineOffset;

#if (UNITY_REVERSED_Z)
    o.pos.z -= z_offset;
#else
    o.pos.z += z_offset;
#endif

#ifdef USE_FIXPROJECTION
    // Blend projection (Perspective)
    float2 pos = o.pos.xy * o.pos.w / _CameraLength;
    o.pos.xy = lerp(o.pos.xy, pos.xy, _FixProjection);
#endif

    o.uv = v.texcoord.xy;
#if defined(MAYA_HLSL)
    o.uv = TRANSFORM_TEX(v.texcoord.xy, 0);
#endif

#ifdef USE_FOG
    o.fogParam = CalcFogParamOriginFromVertex(v.vertex);
#endif

#ifdef USE_DITHER 
    o.ditherPos = CalcDitherPos(o.pos);
#endif

    return o;
}

static const fixed3 WhiteColorRGB = fixed3(1, 1, 1);

half4 frag(v2f i) : COLOR
{
#ifdef USE_DITHER
    ClipDither(i.ditherPos);
#endif

#ifdef TOON_CUTOUT
    half4 tripleMask = TEX2D_SAMPLE(_TripleMaskMap, i.uv);
    if (tripleMask.b < _Cutoff) discard;
#endif

#ifdef USE_OUTLINE_MAINTEX
    half4 mainMapColor = TEX2D_SAMPLE(_MainTex, i.uv);
#else
    half4 mainMapColor = TEX2D_SAMPLE(_OutlineTex, i.uv);
#endif

    // OutlineColorのアルファ値で計算式が変化する。
    // 0.0 <= a <  0.5 : mainMapColor.rgb = lerp(_OutlineColor.rgb, mainMapColor.rgb, _OutlineColor.a * 2)
    // 0.5 <= a <= 1.0 : mainMapColor.rgb =* lerp((1,1,1), _OutlineColor.rgb, (_OutlineColor.a - 0.5) * 2)
    mainMapColor.rgb = lerp(lerp(_OutlineColor.rgb, mainMapColor.rgb, _OutlineColor.a * 2),
                            mainMapColor.rgb * lerp(WhiteColorRGB, _OutlineColor.rgb, (_OutlineColor.a - 0.5) * 2),
                            step(0.5, _OutlineColor.a));

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
    mainMapColor.rgb *= lerp(float3(1, 1, 1), _MaskColorR1.rgb, r1);
    mainMapColor.rgb *= lerp(float3(1, 1, 1), _MaskColorR2.rgb, r2);
    mainMapColor.rgb *= lerp(float3(1, 1, 1), _MaskColorG1.rgb, g1);
    mainMapColor.rgb *= lerp(float3(1, 1, 1), _MaskColorG2.rgb, g2);
    mainMapColor.rgb *= lerp(float3(1, 1, 1), _MaskColorB1.rgb, b1);
    mainMapColor.rgb *= lerp(float3(1, 1, 1), _MaskColorB2.rgb, b2);
#endif // USE_MASK_COLOR

    mainMapColor.rgb *= _CharaColor.rgb * _LightProbeColor.rgb;

#ifdef USE_FOG
    //Fogの影響は最後に受ける
    mainMapColor.rgb = ApplyFog(i.fogParam.x, i.fogParam.y, mainMapColor).rgb;
#endif

#ifdef USE_ALPHA
    mainMapColor.a = _CharaColor.a;
#endif

    // 彩度
    mainMapColor.rgb = ColorSaturation(mainMapColor.rgb, _Saturation);

    return mainMapColor;
}
