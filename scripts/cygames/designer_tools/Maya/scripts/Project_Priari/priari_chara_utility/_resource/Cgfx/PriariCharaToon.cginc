//UNITY_SHADER_NO_UPGRADE

#include "PriariCharaToonProps.cginc"
#include "../../Common/ShaderCommon.cginc"
#include "../../Common/FogCommon.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float3 normal : NORMAL;
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                float4 vcolor : COLOR;
#endif
            };

#if defined(MAYA_CGFX)
            // Maya用のコード.Mayaだと TEXCOORD0～7までらしい。Fog使わないので消して代用する。
            struct v2f
            {
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 editNormalDir : TEXCOORD7;
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                float4 vcolor : TEXCOORD5;
                float3 normalDir : TEXCOORD1;
                float4 posWorld : TEXCOORD2;
                float3 vnormal : TEXCOORD3;
                float4 param : TEXCOORD4;
#endif
#ifdef USE_DITHER
                float4 ditherPos : TEXCOORD6;
#endif
            };
#else
            // Unity用のコード
            struct v2f
            {
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 editNormalDir : TEXCOORD7;
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                float4 vcolor : TEXCOORD8;
                float3 normalDir : TEXCOORD1;
                float4 posWorld : TEXCOORD2;
                float3 vnormal : TEXCOORD3;
                float4 param : TEXCOORD4;
#endif

#if defined(USE_FOG)
                float fogParam : TEXCOORD5;
#endif

#ifdef USE_DITHER
                float4 ditherPos : TEXCOORD6;
#endif

#ifdef TOON_FACE_SHADOW
                float4 posHeadLocal : TEXCOORD9;
#endif

#ifdef USE_HIGHT_LIGHT
                float4 hightColor : TEXCOORD10;
#endif
            };
#endif

            // OptionMaskMapの初期値
            static const half4 OptionMaskMapDefault = half4(0.0, 0.0, 0.5, 0.0);

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

            v2f vert (appdata v)
            {
                v2f o;
                UNITY_INITIALIZE_OUTPUT(v2f, o);
#if defined(MAYA_CGFX)
                o.pos = mul(UNITY_MATRIX_MVP,v.vertex);
#else
                o.pos = PriariObjectToClipPos(v.vertex);
#endif
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(USE_FOG) || defined(USE_HIGHT_LIGHT)
                float4 posWorld = mul(unity_ObjectToWorld, v.vertex);
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                o.vcolor = v.vcolor;
#endif
                float3 normal = v.normal;

                // 顔用のライティング処理
#ifdef TOON_FACE
                float3 vtxVector = posWorld.xyz - _FaceCenterPos.xyz;
                float3 rawCylinderNormal = posWorld.xyz - (_FaceCenterPos.xyz + (dot(_FaceUp, vtxVector) * _FaceUp));
                float3 cylinderNormal = normalize(rawCylinderNormal);
                normal = lerp(cylinderNormal, mul((float3x3)UNITY_MATRIX_M, normal), v.vcolor.b * (1 - _CylinderBlend));
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)

                // 顔用のライティング処理
#ifdef TOON_FACE
                // 顔ライティングの場合法線はすでにモデルマトリックスと計算済みなのでそのまま使う
                o.normalDir = normal;
                o.vnormal = mul((float3x3)UNITY_MATRIX_V, normal);

#elif defined(TOON_HAIR)
                // 通常時
                // 髪等は通常の法線を使うことになると思われる
                // 髪を球状法線とブレンド

                float3 centerNormal = normalize(posWorld.xyz - _FaceCenterPos); // こっちは球状法線
                o.normalDir = mul((float3x3)UNITY_MATRIX_M, normal); // こっちはモデル法線（モデルマトリクスとかけて球状法線と同じ土俵に持ってくる）

                // 面が逆を向いていたら球状法線を反転させて使う
                half revStep = step(0.0, dot(o.normalDir, centerNormal)) * 2 - 1;
                centerNormal = centerNormal * revStep;

                // 球状法線と元法線のブレンド率計算
                // 球状法線と元法線が直行しているときは元を採択する
                float blendRate = abs(dot(o.normalDir, centerNormal)) * lerp(1, v.vcolor.b, _HairNormalBlend);

                centerNormal = lerp(o.normalDir, centerNormal, blendRate);

                o.editNormalDir = centerNormal;
                
                o.vnormal = mul((float3x3)UNITY_MATRIX_MV, normal);
#else
                // 通常時
                o.normalDir = mul((float3x3)UNITY_MATRIX_M, normal);
                o.vnormal = mul((float3x3)UNITY_MATRIX_MV, normal);
#endif
                o.posWorld = posWorld;
                o.param.x = exp2(lerp(11, 1, _SpecularPower));//これ何とかしたい
#endif
#ifdef USE_FIXPROJECTION
                // Blend projection (Perspective)
                float2 pos = o.pos.xy * o.pos.w / _CameraLength;
                o.pos.xy = lerp(o.pos.xy, pos.xy, _FixProjection);
#endif

#ifdef USE_FOG
                float3 viewPos = UnityObjectToViewPos(v.vertex);
                o.fogParam = FastCalcFogParam(posWorld.y, -viewPos.z);
#endif

#ifdef USE_DITHER
                o.ditherPos = CalcDitherPos(o.pos);
#endif

#ifdef TOON_FACE_SHADOW
                o.posHeadLocal = mul(_faceShadowHeadMat, posWorld);
#endif

#ifdef USE_HIGHT_LIGHT
                o.hightColor = _HightLightColor * (1.0 - saturate((posWorld.y - _HightLightParam.x) / _HightLightParam.y));
#endif
                return o;
            }

#ifdef ZEKKEN_TEX
            // ゼッケン表示位置。(UVCenter.xy - (UVSize / 2).xy, UVSize.xy)
            static const float4 ZekkenNumberFrontOffset = float4(0.51445, 0.66505, 0.2957, 0.2399);
            static const float4 ZekkenNumberBackOffset = float4(0.52545, 0.1911, 0.2697, 0.2410);
            static const float4 ZekkenNameFrontOffset = float4(0.4173, 0.5361, 0.4588, 0.0626);
            static const float4 ZekkenNameBackOffset = float4(0.4212, 0.0676, 0.4568, 0.0676);

            fixed4 CompositeZekken(fixed4 baseColor, float4 frontOffset, float4 backOffset, sampler2D compTex, float4 color, half2 baseUV)
            {
                float2 offsetF = frontOffset.xy;
                float2 aspectF = frontOffset.zw;

                float2 offsetB = backOffset.xy;
                float2 aspectB = backOffset.zw;

                float2 compUVF = float2(baseUV.xy / aspectF - offsetF / aspectF);
                float2 compUVB = float2(baseUV.xy / aspectB - offsetB / aspectB);
                fixed4 compF = tex2D(compTex, compUVF) * color;
                fixed4 compB = tex2D(compTex, compUVB) * color;
                float maskF = compF.w * compF.w * compF.w;
                float maskB = compB.w * compB.w * compB.w;
                fixed4 colorF = lerp(0, compF, maskF);
                fixed4 colorB = lerp(0, compB, maskB);
                baseColor = lerp(baseColor, 0, min(colorF.a + colorB.a, 1));    // colorFかcolorBのα値が存在していたら、baseColorを0にする
                return baseColor + colorF + colorB;
            }
#endif

            fixed4 frag (v2f i) : SV_Target
            {
#ifdef USE_DITHER
                ClipDither(i.ditherPos);
#endif

                fixed4 baseColor = tex2D(_MainTex, i.uv);
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

                baseColor.rgb *= lerp(half3(1, 1, 1), _MaskColorR1, r1);
                baseColor.rgb *= lerp(half3(1, 1, 1), _MaskColorR2, r2);
                baseColor.rgb *= lerp(half3(1, 1, 1), _MaskColorG1, g1);
                baseColor.rgb *= lerp(half3(1, 1, 1), _MaskColorG2, g2);
                baseColor.rgb *= lerp(half3(1, 1, 1), _MaskColorB1, b1);
                baseColor.rgb *= lerp(half3(1, 1, 1), _MaskColorB2, b2);
#endif // USE_MASK_COLOR
#ifdef ZEKKEN_TEX
                baseColor = CompositeZekken(baseColor, ZekkenNumberFrontOffset, ZekkenNumberBackOffset, _ZekkenNumberTex, _ZekkenFontColor, i.uv.xy);
                baseColor = CompositeZekken(baseColor, ZekkenNameFrontOffset, ZekkenNameBackOffset, _ZekkenNameTex, _ZekkenFontColor, i.uv.xy);
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(TOON_CUTOUT) || defined(TOON_FACE_SHADOW)
                half4 tripleMask = tex2D(_TripleMaskMap, i.uv);
#endif

#ifdef TOON_CUTOUT
                // カットオフマスク
                half cutoffMask = tripleMask.b;
                if (cutoffMask < _Cutoff) discard;
#ifdef ALPHA_TOON
                baseColor.a *= (cutoffMask - _Cutoff) / (1 - _Cutoff);
#endif
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(USE_LIGHT_COLOR)
                half3 lightColor = _LightColor0.rgb;//この値が取得できない場合、Tagに記述されたLightModeがForwardBaseになっていない
                baseColor.rgb *= lightColor;
                fixed4 originalColor = baseColor;
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(TOON_FACE_SHADOW)
                half4 optionMask = lerp(OptionMaskMapDefault, tex2D(_OptionMaskMap, i.uv), _UseOptionMaskMap);

                // 影マスク
                half shadowMask = tripleMask.r;
#ifdef TOON_FACE
                // 頬・鼻の外連味マスク
                half faceCheatMask = tripleMask.g;
                // スペキュラマスク
                half specularMask = optionMask.r;
#else
                // スペキュラマスク
                half specularMask = tripleMask.g;
#endif
                // 環境マスク
                half envMask = optionMask.g;
                // リムマスク
                half rimMask = optionMask.b;

#if defined(MAYA_CGFX)
                //Mayaだと_WorldSpaceCameraPosが取れない
                half3 viewDirection = normalize(half3(ViewInvXf[0].w,ViewInvXf[1].w,ViewInvXf[2].w) - i.posWorld.xyz);
#else
                half3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld.xyz);
#endif
                // DirectionalLightの位置（共通か固有か）
                half3 lightDirection;

                // _UseOriginalDirectionalLightが1以上であれば固有DirectinalLightを使用する
#if defined(MAYA_CGFX)
                //Mayaだとstep(int, int)は受け付けないらしい。
                lightDirection = lerp(normalize(_WorldSpaceLightPos0.xyz), normalize(_OriginalDirectionalLightDir), step(1, (float)_UseOriginalDirectionalLight));
#else
                lightDirection = lerp(normalize(_WorldSpaceLightPos0.xyz), normalize(_OriginalDirectionalLightDir), step(1, _UseOriginalDirectionalLight));
#endif
//#endif
                half halfLambert;
#ifdef TOON_HAIR
                // 髪用のライティング処理
                // 共通のライトの向き
                // 髪の毛などはこっちになると思われる
                halfLambert = 0.5 * dot(i.editNormalDir, lightDirection) + 0.5;
#else
                // 共通のライトの向き
                halfLambert = 0.5 * dot(i.normalDir, lightDirection) + 0.5;
#endif
                half3 halfDirection = normalize(viewDirection + lightDirection);
#endif

#ifdef TOON_SHADING
                half shading = shadowMask * halfLambert;
                half shadingTemp = (_ToonStep - _ToonFeather);
                // _ToonFeatherが0以下だった場合はfinalShadowを0にする
                half finalShadow = lerp(saturate((1 + (shadingTemp - shading) / (_ToonFeather))), 0, step(_ToonFeather, 0));

                half4 toonMap = tex2D(_ToonMap, i.uv);
#ifdef USE_MASK_COLOR
                toonMap.rgb *= lerp(half3(1, 1, 1), _MaskToonColorR1, r1);
                toonMap.rgb *= lerp(half3(1, 1, 1), _MaskToonColorR2, r2);
                toonMap.rgb *= lerp(half3(1, 1, 1), _MaskToonColorG1, g1);
                toonMap.rgb *= lerp(half3(1, 1, 1), _MaskToonColorG2, g2);
                toonMap.rgb *= lerp(half3(1, 1, 1), _MaskToonColorB1, b1);
                toonMap.rgb *= lerp(half3(1, 1, 1), _MaskToonColorB2, b2);
#endif // USE_MASK_COLOR
#if defined(USE_TOONCOLOR)
                //ToonColorの場合はテクスチャを参照せず、BaseColorの輝度値を調整したものをトゥーン色とする
                half3 toonColor = baseColor.rgb * _ToonColor.rgb * lightColor *_GlobalToonColor.rgb;
#else
                half3 toonColor = toonMap.rgb * lightColor *_GlobalToonColor.rgb;
#endif
                // 頂点カラーのアルファで補正のかかり具合を調整
                half shadowBias = (1 - ((1 - i.vcolor.a) * _VertexColorToonPower) * (0.5 - abs(min(0, halfLambert - 0.5))) * 2);

                // Toonの明るい部分の色補正
                half mulStep = step( _ToonBrightColor.a, 0.5 );
                half addStep = 1 - mulStep;
                baseColor.rgb = baseColor.rgb * lerp( half3( 1, 1, 1 ), _ToonBrightColor.rgb, mulStep * shadowBias) + ( _ToonBrightColor.rgb * addStep * shadowBias);

                // Toonの暗い部分の色補正
                mulStep = step( _ToonDarkColor.a, 0.5 );
                addStep = 1 - mulStep;
                toonColor.rgb = toonColor.rgb * lerp( half3( 1, 1, 1 ), _ToonDarkColor.rgb, mulStep * shadowBias) + ( _ToonDarkColor.rgb * addStep * shadowBias);

                // 明るい部分のオリジナルカラーを取っておく
                fixed4 brightOriginalColor = baseColor;

                baseColor.rgb = lerp(baseColor.rgb, toonColor.rgb, finalShadow);
#endif

// 眉は独自のかかり方(常にToonの暗い部分の補正がかかる)
#ifdef TOON_MAYU
                // Toonの暗い部分の色補正
                half mulStep = step( _ToonDarkColor.a, 0.5 );
                half addStep = 1 - mulStep;
                baseColor.rgb = baseColor.rgb * lerp( half3( 1, 1, 1 ), _ToonDarkColor.rgb, mulStep) + ( _ToonDarkColor.rgb * addStep);
#endif

#ifdef USE_DIRT
                fixed4 dirtRate = tex2D(_DirtTex, i.uv) * _DirtScale;

#if defined(MAYA_CGFX)
                half dirt_a = (dirtRate.r * _DirtRate1) + (dirtRate.g * _DirtRate2) + (dirtRate.b * _DirtRate3);
#else
                half dirt_a = (dirtRate.r * _DirtRate[0]) + (dirtRate.g * _DirtRate[1]) + (dirtRate.b * _DirtRate[2]);
#endif

#endif

#ifdef USE_WET
                baseColor.rgb = (baseColor.rgb * (_WetRate));
#endif

#if defined(TOON_SPECULAR)||defined(TOON_RIM)

#if defined(TOON_RIM_CONTROLL)
                // カメラのライト、アップのベクトルをとる
                half3 camRightVector = UNITY_MATRIX_V[0].xyz;
                half3 camUpVector = UNITY_MATRIX_V[1].xyz;

                half3 horizonOffsetVector = camRightVector * (step(0.0, _RimHorizonOffset * -1) * 2 - 1);
                half3 verticalOffsetVector = camUpVector * (step(0.0, _RimVerticalOffset * -1) * 2 - 1);

                half3 rimViewDirection = lerp(viewDirection, horizonOffsetVector, abs(_RimHorizonOffset));
                rimViewDirection = lerp(rimViewDirection, verticalOffsetVector, abs(_RimVerticalOffset));

                half rimShading = dot(rimViewDirection, i.normalDir);
                half rimTemp = (_RimStep - _RimFeather);
                half rim = saturate((1 + (rimTemp - rimShading) / (_RimFeather)));
                rim = rim * rim * rim * rim;
                rim = rim * _RimColor.a * rimMask;//shadowがrimを兼ねる

                // 以下rim2の処理
                half3 horizonOffsetVector2 = camRightVector * (step(0.0, _RimHorizonOffset2 * -1) * 2 - 1);
                half3 verticalOffsetVector2 = camUpVector * (step(0.0, _RimVerticalOffset2 * -1) * 2 - 1);

                half3 rimViewDirection2 = lerp(viewDirection, horizonOffsetVector2, abs(_RimHorizonOffset2));
                rimViewDirection2 = lerp(rimViewDirection2, verticalOffsetVector2, abs(_RimVerticalOffset2));

                half rimShading2 = dot(rimViewDirection2, i.normalDir);
                half rimTemp2 = (_RimStep2 - _RimFeather2);
                half rim2 = saturate((1 + (rimTemp2 - rimShading2) / (_RimFeather2)));
                rim2 = rim2 * rim2 * rim2 * rim2;
                rim2 = rim2 * _RimColor.a * rimMask;//shadowがrimを兼ねる
                
#else
                half rimShading = dot(viewDirection, i.normalDir);
                half rimTemp = (_RimStep - _RimFeather);
                half rim = saturate((1 + (rimTemp - rimShading) / (_RimFeather)));
                half rim2 = rim * rim;//rimは４乗で固定化する
                half rim4 = rim2 * rim2;
                rim = rim4 * _RimColor.a * rimMask;//shadowがrimを兼ねる
                
#endif // TOON_RIM_CONTROLL

#endif

#ifdef TOON_SPECULAR
#if 0
                //本来のspecular
                half specular = 0.5 * dot(halfDirection, i.normalDir) + 0.5;
                half specularTemp = specularMask * pow(specular, i.param.x);
#else
                //fake specular
                half specularTemp = specularMask * saturate(pow(rimShading, 1 + _SpecularPower * 10));
#endif
                //return specularTemp;

                //half3 specularColor = (specularMap.rgb * lightColor) * specularTemp;
                half3 specularColor = (_SpecularColor.rgb * lightColor) * specularTemp;

                // ios:iphone6(A9系)＆ios10以降の不具合対応
                // specularColorがマイナスになるときが一部端末である。
                // saturate関数では回避できず、max関数を使用して、一度0始まりにする。
#if defined(MAYA_CGFX)
                // Maya用のコード
                half3 fixedSpecularColor = max(half3(0, 0, 0), specularColor);
#else
                // Unity用のコード
                half3 fixedSpecularColor = max(0, specularColor);
#endif

                // 明暗部に加算した際にsaturateによってスペキュラー計算が入る部分が暗くなってしまうのでsaturateを削除
                // baseColor.rgb = saturate(baseColor.rgb + fixedSpecularColor.rgb);
                baseColor.rgb = baseColor.rgb + fixedSpecularColor.rgb;

#ifdef USE_DIRT
                half3 dirtColor = _GlobalDirtColor.rgb;

#ifdef TOON_SHADING
                //陰色を入れる
                dirtColor.rgb = lerp(dirtColor.rgb, _GlobalDirtToonColor.rgb, finalShadow);
#endif
                //dirtのスペキュラを無効にする
                baseColor.rgb = lerp(baseColor.rgb, dirtColor.rgb, dirt_a);
#endif


#endif

#ifdef TOON_ENVIRONMENT 
                //環境マップ
                fixed2 euv = (i.vnormal.xy + 1) * 0.5;
                half3 envPower = tex2D(_EnvMap, euv).rgb;// *_GlobalEnvColor.rgb;
                half3 env = baseColor.rgb * envPower.rgb * _EnvBias;
                baseColor.rgb = lerp(baseColor.rgb, env.rgb, envMask * _EnvRate);
#endif

#ifdef TOON_RIM
                //リム
                //half4 rimColor = lerp(specularMap, _RimColor, _RimSpecRate);
                half4 rimColor = lerp(_SpecularColor, _RimColor, _RimSpecRate);;
                half diffuse = max(0, dot(lightDirection, i.normalDir));
                half4 rimRate = rimColor * rim * (diffuse + _RimShadow + _RimShadowRate) * _GlobalRimColor;//スペキュラカラーをリムにも使う

                //rimRate *= _GlobalRimRate;
                baseColor.rgb += rimRate.rgb;

#if defined(TOON_RIM_CONTROLL)
                // リム2
                //half4 rimColor2 = lerp(specularMap, _RimColor2, _RimSpecRate2);
                half4 rimColor2 = lerp(_SpecularColor, _RimColor2, _RimSpecRate2);
                half4 rimRate2 = rimColor2 * rim2 * (diffuse + _RimShadowRate2) * _GlobalRimColor;
                baseColor.rgb += rimRate2.rgb;
#endif

#ifdef USE_DIRT
                //rimRateが0でスペキュラーが出ないのであれば、dirtColorをそれ以外であれば_DirtRimSpecularColorを使用するマスクを作成する
                float dirtMaskRim = rimRate.r + rimRate.g + rimRate.b;
                float3 dirtColorRim;
                if (dirtMaskRim <= 0.00001)
                {
                    dirtColorRim = _GlobalDirtColor;
                }
                else
                {
                    dirtColorRim = _GlobalDirtRimSpecularColor;
                }
                baseColor.rgb = lerp(baseColor.rgb, dirtColorRim, dirt_a);
#endif

#ifdef TOON_FACE
                // shad_cのアルファで頬と鼻の外連味を出す

                // shad_cのアルファが0.51以上なら頬、0.49未満なら鼻
                half cheekThreshold = 0.51;
                half noseThreshold = 0.49;

                // モデルとライトの左右判定。1なら右、-1なら左
                half3 centerDir = i.posWorld.xyz - _FaceCenterPos;
                half modelSide = step(0.0, dot(cross(_FaceForward, centerDir), _FaceUp)) * 2 - 1;
                half lightSide = step(0.0, dot(cross(_FaceForward, lightDirection), _FaceUp)) * 2 - 1;

                // 1ならライト側、-1ならライトと逆側
                half lightSameSide = modelSide * lightSide;
                // 頬の処理（頬はライトと反対側にオリジナルの色を出す
                // 真後ろから真横の範囲をcheekAnglePowerOffsetずらした値を使用
                half cheekAnglePowerOffset = 0.1;
                half cheekAnglePowerTemp = max(0, dot(_FaceForward, lightDirection * -1) + cheekAnglePowerOffset);
                half cheekAnglePower = 1 - (abs(0.5 - cheekAnglePowerTemp) * 2);

                // ライトが下方向に回った時に頬抜きが減衰するように補正
                half vrtPower = min(dot(_FaceUp, lightDirection), 0) + 1;
                vrtPower = vrtPower * vrtPower;
                cheekAnglePower = max(cheekAnglePower, 0) * vrtPower;
                
                // toon陰の際で頬抜きを減衰させて、陰の際と合体しないようにする
                // toonFeather=0.05と同じ減衰をかける
                half cheekPretenseTemp = (_ToonStep - 0.05);
                half finalCheekPretense = saturate((1 + (cheekPretenseTemp - shading) / (0.05)));

                // shad_cのアルファの 0.5~1 を 0~1 として扱う
                half cheekPretensePower = max(0, faceCheatMask - cheekThreshold) * 2;
                cheekPretensePower = cheekPretensePower * finalCheekPretense * cheekAnglePower;

                // ライトの反対側ではdiffの色を使う
                half3 cheekColor = lerp(brightOriginalColor.rgb, toonColor, (lightSameSide + 1) * 0.5);

                //TODO:oi_shinya:ios:
                // 謎な不具合：step関数結果をfixedに入れる＞＞その結果を2つ用意してlerp関数に使用するとアセバンビルドでエラーになる
                // なので片方をfloatにして回避している。
                float isCheek = step(cheekThreshold, faceCheatMask);
                fixed cheekPretenseStep = step((1.0 - _CheekPretenseThreshold), cheekPretensePower);
                baseColor.rgb = lerp(baseColor.rgb, cheekColor.rgb, cheekPretenseStep * isCheek);
                
                // 鼻の処理(鼻はライト側にオリジナル、逆側に陰)
                half noseAnglePower = saturate((1 - abs(dot(_FaceForward, lightDirection))) * 2);

                // shad_cのアルファの 0.5~0 を 0~1 として扱う
                half nosePower = min(noseThreshold, faceCheatMask) * -2 + 1;
                nosePower = nosePower * noseAnglePower;
                
                // ライト側ではdiff、反対側ではshadの色を使う
                half3 noseColor = lerp(toonColor, brightOriginalColor.rgb, (lightSameSide + 1) * 0.5);

                //TODO:oi_shinya:ios:
                // 謎な不具合：step関数結果をfixedに入れる＞＞その結果を2つ用意してlerp関数に使用するとアセバンビルドでエラーになる
                // なので片方をfloatにして回避している。
                float isNose = step(faceCheatMask, noseThreshold);
                fixed noseStep = step((1.0 - _NosePretenseThreshold), nosePower);
                baseColor.rgb = lerp(baseColor.rgb, noseColor.rgb, noseStep * isNose * _NoseVisibility); // _NoseVisibilityをnoseStepに掛けるとアセバンビルドでエラーになる
#endif  

#endif

                baseColor.rgb *= _CharaColor.rgb * _LightProbeColor.rgb;

#ifdef TOON_MAYU
                //眉はエミッシヴの影響を受けない
#else
                //発光
                //上記の演算より後に発光を計算しないと一部演出に支障がでる
                //(ライブで暗所用のフィルターかける時にemissiveは光るようにしたい)
                half final_emi = 1;
#ifdef USE_DIRT
                //発光部分にも汚れの効果をのせる
                final_emi = 1 - dirt_a;
#endif
                baseColor.rgb += tex2D(_EmissiveTex, i.uv).rgb * _EmissiveColor.rgb * final_emi;
#endif

#ifdef TOON_FACE_SHADOW
                //顔影
                float shadowColorRate = saturate((i.posHeadLocal.y - _faceShadowEndY) / _faceShadowLength) * _faceShadowAlpha;
                baseColor.rgb = (1 - tripleMask.b) * baseColor.rgb + tripleMask.b * (1 - shadowColorRate) * baseColor.rgb + tripleMask.b * shadowColorRate * baseColor.rgb * _faceShadowColor.rgb;
#endif

#ifdef USE_HIGHT_LIGHT
                //キャラカラーより高さライトの影響の方が強い
                baseColor.rgb = baseColor.rgb + i.hightColor;
#endif

#ifdef USE_FOG
                //Fogの影響は最後に受ける
                //GalaxyS9+Android9にて関数だとハングアップするので、直接計算するように変更
                baseColor.rgb = lerp(_Global_FogColor.rgb, baseColor.rgb, i.fogParam);
#endif

#ifdef USE_ALPHA
                baseColor.a *= _CharaColor.a;
#endif

                return baseColor;
            }
