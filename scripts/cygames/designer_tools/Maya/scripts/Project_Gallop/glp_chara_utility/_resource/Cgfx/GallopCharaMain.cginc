// Character shader

#include "GallopCharaMainProps.cginc"

struct appdata_t
{
    float4 vertex : POSITION;
    float3 normal : NORMAL;
    float2 texcoord : TEXCOORD0;
};

struct v2f
{
    float4 pos      : SV_POSITION;
    float2 uv       : TEXCOORD0;
};

#if defined(MINI_EYE)
uniform float4 _UVOffset;
#endif

v2f vert(appdata_t v )
{
    v2f o;
    o.pos = GallopObjectToClipPos(v.vertex);
    o.uv.xy = TRANSFORM_TEX(v.texcoord.xy, _MainTex);

#ifdef MINI_EYE
    //左右目の境界がx=0.125単位となっている
    float eye = step(v.texcoord.x, 0.125);  //左目だったら1が返るはず
    o.uv.xy += (_UVOffset.xy * eye) + (_UVOffset.zw * (1.0 - eye));
#endif

#ifdef USE_FIXPROJECTION
    // Blend projection (Perspective)
    float2 pos = o.pos.xy * o.pos.w / _CameraLength;
    o.pos.xy = lerp(o.pos.xy, pos.xy, _FixProjection);
#endif
    return o;
}

fixed4 frag( v2f i ) : COLOR
{
    fixed4 diffSamplerColor = tex2D( _MainTex, i.uv.xy );

#ifdef USE_EMISSIVE
    //発光
    diffSamplerColor.rgb += tex2D(_EmissiveTex, i.uv).rgb * _EmissiveColor.rgb;
#endif

#if defined(BLEND_MULTIPLY) || defined(MIRROR_STAGE_BLEND)
    // 乗算合成時は_CharaColorの色を乗算しない
#else
    diffSamplerColor.rgb *= _CharaColor.rgb;
#endif

    return diffSamplerColor;
}

