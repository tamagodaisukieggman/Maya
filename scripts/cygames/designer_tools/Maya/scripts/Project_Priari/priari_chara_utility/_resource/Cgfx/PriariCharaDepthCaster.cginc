//UNITY_SHADER_NO_UPGRADE

#include "../../../Common/ShaderCommon.cginc"

uniform float  _FixProjection;// 正射影率.
uniform float  _CameraLength;

uniform half _OutlineWidth;
uniform half _OutlineBrightness;

float _GlobalOutlineOffset;
half _GlobalOutlineWidth;

float _GlobalCameraFov;

#ifdef USE_DITHER
#define DITHER_SIZE (4)
uniform float _DitherCutt;
uniform sampler2D _DitherTex;
#endif

#ifdef TOON_CUTOUT
uniform half _Cutoff;

uniform sampler2D _MainTex;
uniform float4 _MainTex_ST;
uniform sampler2D _TripleMaskMap;
#endif


struct appdata_chara
 {
    float4 vertex : POSITION;
    float3 normal : TANGENT;
    fixed4 vcolor  : COLOR;

#ifdef TOON_CUTOUT
    float2 uv : TEXCOORD0;
#endif
};

struct v2f
{
    float4 pos : SV_POSITION;
#ifdef TOON_CUTOUT
    float2 uv : TEXCOORD0;
#endif
    float2 depth : TEXCOORD1;

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

v2f vert (appdata_chara v)
{
    v2f o;
    o.depth = 0;
    UNITY_TRANSFER_DEPTH(o.depth);

    //    太さとオフセットの調整機能を入れた処理
    o.pos = UnityObjectToClipPos(v.vertex);
#ifdef TOON_CUTOUT
    o.uv = TRANSFORM_TEX(v.uv, _MainTex);
#endif

    float z = saturate(o.pos.z);
    float4 z_w = o.pos / o.pos.w;

    //    FOVの値を反映する
    float fov_offset = _GlobalCameraFov;
    float transform_offset = OUTLINE_OFFSET + (fov_offset / 2.0f);
    float color_offset = fov_offset;
    float z_offset = OUTLINE_Z_OFFSET;

    float4 norm = mul(UNITY_MATRIX_IT_MV, float4(v.normal, 0.0));
    float2 offset = TransformViewToProjection(norm.xy) * transform_offset;

    //    手前が太くなりすぎず、奥が細くなりすぎないように調整
    o.pos.xy += offset * (v.vcolor.r * OUTLINE_DISTANCE_SCALE * _OutlineWidth);

    //    奥に押し出して余計なアウトラインが表示されないように調整
    //Out.HPos.z += OUTLINE_Z_OFFSET * lerp( z_w, Out.HPos.z, (1.0-z) ) * (1.0f-In.ColorSet.g);
    //    FOVの値によって一部端末でアウトラインが浮き出てしまう対応
    //Out.HPos.z += z_offset * lerp( Out.HPos.z, z_w.z, z ) * (1.0f-(In.ColorSet.g * color_offset));
#if defined(UNITY_REVERSED_Z)    
    o.pos.z -= z_offset * (1.0f - v.vcolor.g) * color_offset * _GlobalOutlineOffset;
#else
    o.pos.z += z_offset * (1.0f - v.vcolor.g) * color_offset * _GlobalOutlineOffset;
#endif

#ifdef USE_FIXPROJECTION
    float2 pos = o.pos.xy * o.pos.w / _CameraLength;
    o.pos.xy = lerp(o.pos.xy, pos.xy, _FixProjection);
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

#ifdef TOON_CUTOUT
    half4 tripleMask = tex2D(_TripleMaskMap, i.uv);
    if (tripleMask.b < _Cutoff)discard;
#endif


    UNITY_OUTPUT_DEPTH(i.depth);
}
