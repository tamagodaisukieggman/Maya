// UNITY_SHADER_NO_UPGRADE

#include "GallopCharaRichProps.cginc"

v2f vert(appdata v)
{
    v2f o;
    o.vertex = mul(UNITY_MATRIX_MVP, v.vertex);
    o.uv = TRANSFORM_TEX(v.uv, _MainTex);

#if UNITY_VERSION >= 540
    float4 wnormal = mul(unity_ObjectToWorld, v.normal);
#else
    float4 wnormal = mul(_Object2World, v.normal);
#endif
    o.normal = wnormal.xyz;
#if defined(MAYA_CGFX)
    o.vnormal = mul(UNITY_MATRIX_MV, float4(v.normal.xyz,0)).xyz;
#else
    o.vnormal = mul((float3x3)UNITY_MATRIX_MV, v.normal.xyz).xyz;
#endif
    return o;
}

fixed4 frag(v2f i) : SV_Target
{
    float3 _LightDir = normalize(_GlobalLightDir.xyz);
    float4 ctrl = tex2D(_ControlMap, i.uv);
    fixed4 baseColor = tex2D(_MainTex, i.uv);
    fixed4 col = baseColor;

    //頂点の法線情報を使う
    float3 normalVec = i.normal;

    float3 eyeDir = UNITY_MATRIX_V[2].xyz;//視線方向
    half rim = 1.0 - saturate(dot(eyeDir, normalVec));
    rim = pow(rim, _RimPower + 1) * _RimRate * ctrl.b;
#if 1
    //法線調整機能
    normalVec += eyeDir * _RimNormalAdjust;//横方法を弱くする
    normalVec = normalize(normalVec);
#endif

#if 1
    //環境マップ
    half2 euv =  (i.vnormal.xy + 1) * 0.5;
    half3 envPower = tex2D(_GlobalEnvTex, euv).rgb * _GlobalEnvColor.rgb;
    fixed3 env = baseColor.rgb * envPower.rgb * _EnvBias;
    col.rgb = lerp(col.rgb, env.rgb, ctrl.g * _EnvRate * _GlobalEnvRate);
#endif

#if 1
    //スペキュラマップ補完
    float  spec = max(0, dot(_LightDir, normalVec));
    spec = pow(spec, _SpecPower) * _SpecRate * ctrl.r;
    spec *= _GlobalSpecRate;
    fixed4 specTex = tex2D(_SpecTex, i.uv);
    col.rgb = lerp(col.rgb, specTex.rgb*_SpecColor, spec);
#endif

    float diffuse = max(0, dot(_LightDir, normalVec));
    //if (diffuse > 0.5)diffuse = 1;//りみったー
#if 0
    //トゥーン処理（オミット）
    float toon = diffuse;
    toon = 1 - saturate(toon + (1 - _ToonRate*_GlobalToonRate));
    toon *=  ctrl.g;//ctrl.gはトゥーンのマスク
    fixed4 shadow = tex2D(_ShadowTex,i.uv) * _ShadowColor;
    col.rgb = lerp(col.rgb,shadow.rgb,toon);
#endif

    //リム
    fixed4 rimTemp = lerp(specTex, _RimColor, _RimSpecRate);
    float4 rimRate = rimTemp * rim * (diffuse + _RimShadow + _GlobalRimShadowRate);//スペキュラカラーをリムにも使う
    rimRate *= _GlobalRimRate;
    col.rgb += rimRate.rgb;

#if 0
    //従来型スペキュラ
    float  spec = max(0, dot(_LightDir, normalVec));
    spec = pow(spec, _SpecPower) * _SpecRate * ctrl.r;
    col.rgb += _SpecColor * spec;
#endif

    col.rgb = col.rgb * _CharaColor.rgb;
    //col.rgb = diffuse;
    //col.rgb = toon;
    //col.rgb = ctrl.g;
    //col.rgb = env.rgb;
    return col;
}