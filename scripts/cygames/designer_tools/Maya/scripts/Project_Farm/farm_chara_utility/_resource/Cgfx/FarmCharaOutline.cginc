//UNITY_SHADER_NO_UPGRADE
// defined(MAYA_CGFX)の部分をMayaのCgfx用に修正している

#if defined(MAYA_CGFX)  // Maya専用のプロパティ定義。多くはProps.cgincから持ってくる

#include "FarmCharaToonProps.cginc"

float _OutlineWidth;
float4 _OutlineColor;

uniform float _GlobalOutlineOffset;
uniform float _GlobalOutlineWidth;
float _GlobalCameraFov;

#define PLATFORM_SCALE( x )     (x)
#define OUTLINE_DISTANCE_SCALE  PLATFORM_SCALE(0.0028*_GlobalOutlineWidth)
#define OUTLINE_Z_OFFSET        PLATFORM_SCALE(0.0015 * 0.125 * 100)
#define OUTLINE_OFFSET          (0.75)    // アウトラインサイズのオフセット

#else // Unity用

#include "../../../Common/ShaderCommon.cginc"
#include "../../../Common/FogCommon.cginc"

uniform fixed4 _CharaColor;
uniform fixed4 _LightProbeColor;

uniform sampler2D _MainTex;
uniform float4 _MainTex_ST;

uniform sampler2D _OutlineTex;
uniform float4 _OutlineParam;

#ifdef TOON_CUTOUT
uniform sampler2D _TripleMaskMap;
uniform half _Cutoff;
#endif

uniform float  _FixProjection;// 正射影率.
uniform float  _CameraLength;

uniform half _OutlineWidth;
uniform fixed4 _OutlineColor;

uniform float _GlobalOutlineOffset;
uniform half _GlobalOutlineWidth;
uniform float _GlobalOutlineColorOffsetScale;

uniform float _StencilComp;
uniform float _StencilOp;

float _GlobalCameraFov;
uniform float4 _GlobalOutlineDepthOffset;

#ifdef USE_DITHER
#define DITHER_SIZE (4)
uniform float _DitherCutt;
uniform sampler2D _DitherTex;
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

struct appdata_t {
    // Mayaは法線の扱いや、スクリプトでアトリビュートに代入する順序が異なるので別に書く
#if defined(MAYA_CGFX)
    float4 vertex : POSITION;
    float2 texcoord : TEXCOORD0;
    float3 normal : NORMAL;
    float4 color : COLOR;
#else
    float4 vertex : POSITION;
    float3 normal : TANGENT;
    fixed4 color : COLOR;
    float2 texcoord : TEXCOORD0;
#endif

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
    float ditherColor = tex2D(_DitherTex, ditherPos.xy / ditherPos.w).r;
    if (ditherColor <= _DitherCutt) discard;
}

#endif

v2f vert(appdata_t v)
{
    v2f o;
    //    太さとオフセットの調整機能を入れた処理
    o.pos = FarmObjectToClipPos(v.vertex);

    //    FOVの値を反映する
    float fov_offset = _GlobalCameraFov;
    float transform_offset = OUTLINE_OFFSET + (fov_offset / 2.0);

#if defined(MAYA_CGFX)  // Mayaは法線方向をそのまま使う。offsetは係数をかけてUnityと数値を合わせる
    float adjust_unity_coefficient = 10.0;
    float4 norm = mul(UNITY_MATRIX_MVP, float4(normalize(v.normal), 0.0));
    float2 offset = norm.xy * transform_offset * adjust_unity_coefficient;
#else
    float4 norm = mul(UNITY_MATRIX_IT_MV, float4(v.normal, 0.0));
    float2 offset = TransformViewToProjection(norm.xy) * transform_offset;
#endif

    //    手前が太くなりすぎず、奥が細くなりすぎないように調整
    o.pos.xy += offset * (v.color.r * OUTLINE_DISTANCE_SCALE * _OutlineWidth);

    float z_offset = OUTLINE_Z_OFFSET * (1.0 - v.color.g) * fov_offset * _GlobalOutlineOffset;

#if defined(UNITY_REVERSED_Z)
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
    half4 tripleMask = tex2D(_TripleMaskMap, i.uv);
    if (tripleMask.b < _Cutoff) discard;
#endif

#ifdef USE_OUTLINE_MAINTEX
    half4 mainMapColor = tex2D(_MainTex, i.uv);
#else
    half4 mainMapColor = tex2D(_OutlineTex, i.uv);
#endif

    // OutlineColorのアルファ値で計算式が変化する。
    // 0.0 <= a <  0.5 : mainMapColor.rgb = lerp(_OutlineColor.rgb, mainMapColor.rgb, _OutlineColor.a * 2)
    // 0.5 <= a <= 1.0 : mainMapColor.rgb =* lerp((1,1,1), _OutlineColor.rgb, (_OutlineColor.a - 0.5) * 2)
    mainMapColor.rgb = lerp(lerp(_OutlineColor.rgb, mainMapColor.rgb, _OutlineColor.a * 2),
                            mainMapColor.rgb * lerp(WhiteColorRGB, _OutlineColor.rgb, (_OutlineColor.a - 0.5) * 2),
                            step(0.5, _OutlineColor.a));

#ifdef USE_MASK_COLOR
    half4 colorMask = tex2D(_MaskColorTex, i.uv);
    // 0.49～0にかけて_MaskColorR1を、0.51～1にかけて_MaskColorR2を使用する。
    // 0.49～0.51については色は触らない。
    half r1 = (0.49 - min(0.49, colorMask.r)) * (1 / 0.49);
    half r2 = (max(0.51, colorMask.r) - 0.51) * (1 / 0.49);
    half g1 = (0.49 - min(0.49, colorMask.g)) * (1 / 0.49);
    half g2 = (max(0.51, colorMask.g) - 0.51) * (1 / 0.49);
    half b1 = (0.49 - min(0.49, colorMask.b)) * (1 / 0.49);
    half b2 = (max(0.51, colorMask.b) - 0.51) * (1 / 0.49);
    mainMapColor.rgb *= lerp(half3(1, 1, 1), _MaskColorR1, r1);
    mainMapColor.rgb *= lerp(half3(1, 1, 1), _MaskColorR2, r2);
    mainMapColor.rgb *= lerp(half3(1, 1, 1), _MaskColorG1, g1);
    mainMapColor.rgb *= lerp(half3(1, 1, 1), _MaskColorG2, g2);
    mainMapColor.rgb *= lerp(half3(1, 1, 1), _MaskColorB1, b1);
    mainMapColor.rgb *= lerp(half3(1, 1, 1), _MaskColorB2, b2);
#endif // USE_MASK_COLOR

    mainMapColor.rgb *= _CharaColor.rgb * _LightProbeColor.rgb;

#ifdef USE_FOG
    //Fogの影響は最後に受ける
    mainMapColor.rgb = ApplyFog(i.fogParam.x, i.fogParam.y, mainMapColor).rgb;
#endif

#ifdef USE_ALPHA
    mainMapColor.a = _CharaColor.a;
#endif

    return mainMapColor;
}
