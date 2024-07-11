#ifndef _DESIGNER_CHARATOON_HLSLINC_
#define _DESIGNER_CHARATOON_HLSLINC_

#ifdef MAYA_HLSL
#include "GallopCharaToonProps.fx"
#else
#include "GallopCharaToonProps.hlsl"
#endif

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float3 normal : NORMAL;
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                float4 vcolor : COLOR;
#endif
            };

#if defined(MAYA_HLSL)
            // Maya用のコード.Mayaだと TEXCOORD0～7までらしい。Fog使わないので消して代用する。
            struct v2f
            {
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3 editNormalDir : TEXCOORD7;
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                float4 vcolor : TEXCOORD5;
                float3 normalDir : TEXCOORD1;
                float3 posWorld : TEXCOORD2;
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
                float3 posWorld : TEXCOORD2;
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

            v2f vert (appdata v)
            {
                v2f o = (v2f)0;
                VertexPositionInputs vpi = GallopGetVertexPositionInputs(v.vertex.xyz);
                o.pos = vpi.positionCS;
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(USE_FOG) || defined(USE_HIGHT_LIGHT)
                float3 posWorld = vpi.positionWS;
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT)
                o.vcolor = v.vcolor;
#endif
                float3 normal = v.normal;

                // 顔用のライティング処理
#ifdef TOON_FACE
                float3 vtxVector = posWorld - _FaceCenterPos.xyz;
                float3 rawTkglinderNormal = posWorld - (_FaceCenterPos.xyz + (dot(_FaceUp, vtxVector) * _FaceUp));
                float3 cylinderNormal = normalize(rawTkglinderNormal);
                normal = lerp(cylinderNormal, mul((float3x3)UNITY_MATRIX_M, normal), v.vcolor.b * (1 - _TkglinderBlend));
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

                float3 centerNormal = normalize(posWorld - _FaceCenterPos); // こっちは球状法線
                o.normalDir = mul((float3x3)GetObjectToWorldMatrix(), normal); // こっちはモデル法線（モデルマトリクスとかけて球状法線と同じ土俵に持ってくる）

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
                o.normalDir = mul((float3x3)GetObjectToWorldMatrix(), normal);
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
                float3 viewPos = vpi.positionVS;
                o.fogParam = FastCalcFogParam(posWorld.y, -viewPos.z);
#endif

#ifdef USE_DITHER
                o.ditherPos = CalcDitherPos(o.pos);
#endif

#ifdef TOON_FACE_SHADOW
                o.posHeadLocal = mul(_faceShadowHeadMat, float4(posWorld,1));
#endif

#ifdef USE_HIGHT_LIGHT
                o.hightColor = _HightLightColor * (1.0 - saturate((posWorld.y - _HightLightParam.x) / _HightLightParam.y));
#endif
                return o;
            }

#ifdef ZEKKEN_TEX
            fixed4 CompositeZekken(fixed4 baseColor, float4 frontOffset, float4 backOffset, TEXTURE2D(compTex), SAMPLER(compSampler), float4 color, half2 baseUV)
            {
                float2 offsetF = frontOffset.xy;
                float2 aspectF = frontOffset.zw;

                float2 offsetB = backOffset.xy;
                float2 aspectB = backOffset.zw;

                float2 compUVF = float2(baseUV.xy / aspectF - offsetF / aspectF);
                float2 compUVB = float2(baseUV.xy / aspectB - offsetB / aspectB);
                fixed4 compF = SAMPLE_TEXTURE2D(compTex, compSampler, compUVF) * color;
                fixed4 compB = SAMPLE_TEXTURE2D(compTex, compSampler, compUVB) * color;
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

                fixed4 baseColor = TEX2D_SAMPLE(_MainTex, i.uv);

#ifdef USE_UV_EMISSIVE
                //Maskによって一部カラー反映を無効にする箇所があるため先頭で取得する
                //_UVEmissivePowerが1以上指定される事があるので注意する事
                half emissiveMask = TEX2D_SAMPLE(_UVEmissiveMaskTex, i.uv).r * _UVEmissivePower;
                //_UVEmissivePower = 0の場合影補正は有効にしたい
                half invEmissiveMask = 1.0 - saturate(emissiveMask);
#endif

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

                baseColor.rgb *= lerp(1, _MaskColorR1, r1).rgb;
                baseColor.rgb *= lerp(1, _MaskColorR2, r2).rgb;
                baseColor.rgb *= lerp(1, _MaskColorG1, g1).rgb;
                baseColor.rgb *= lerp(1, _MaskColorG2, g2).rgb;
                baseColor.rgb *= lerp(1, _MaskColorB1, b1).rgb;
                baseColor.rgb *= lerp(1, _MaskColorB2, b2).rgb;

#endif // USE_MASK_COLOR
#ifdef ZEKKEN_TEX
                baseColor = CompositeZekken(baseColor, ZekkenNumberFrontOffset, ZekkenNumberBackOffset, _ZekkenNumberTex, sampler_ZekkenNumberTex,_ZekkenFontColor, i.uv.xy);
                baseColor = CompositeZekken(baseColor, ZekkenNameFrontOffset, ZekkenNameBackOffset, _ZekkenNameTex, sampler_ZekkenNameTex,_ZekkenFontColor, i.uv.xy);
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(TOON_CUTOUT) || defined(TOON_FACE_SHADOW)
                half4 tripleMask = TEX2D_SAMPLE(_TripleMaskMap, i.uv);
#endif

#ifdef TOON_CUTOUT
                // カットオフマスク
                half cutoffMask = tripleMask.b;
                if (cutoffMask < _Cutoff) discard;
#ifdef ALPHA_TOON
                baseColor.a *= (cutoffMask - _Cutoff) / (1 - _Cutoff);
#endif
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(USE_LIGHT_COLOR) || defined(TOON_FACE_SHADOW)
                Light lightData = GetMainLight();
#endif

                //TOON_FACE_SHADOW以外は反映する
#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(USE_LIGHT_COLOR)
                baseColor.rgb *= lightData.color;
#endif

#if defined(TOON_SHADING) || defined(TOON_SPECULAR) || defined(TOON_RIM) || defined(TOON_ENVIRONMENT) || defined(TOON_FACE_SHADOW)
                half4 optionMask = lerp(OptionMaskMapDefault, TEX2D_SAMPLE(_OptionMaskMap, i.uv), _UseOptionMaskMap);

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

#if defined(MAYA_HLSL)
                //Mayaだと_WorldSpaceCameraPosが取れない
                half3 viewDirection = normalize(half3(ViewInvXf[0].w,ViewInvXf[1].w,ViewInvXf[2].w) - i.posWorld);
#else
                half3 viewDirection = normalize(_WorldSpaceCameraPos.xyz - i.posWorld);
#endif
                // DirectionalLightの位置（共通か固有か）
                half3 lightDirection1, lightDirection2;

                // _UseOriginalDirectionalLightが1以上であれば固有DirectinalLightを使用する
#if defined(MAYA_HLSL)
                //Mayaだとstep(int, int)は受け付けないらしい。
                lightDirection1 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir1), step(1, (float)_UseOriginalDirectionalLight));
                lightDirection2 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir2), step(1, (float)_UseOriginalDirectionalLight));
#else
                lightDirection1 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir1), step(1, _UseOriginalDirectionalLight));
                lightDirection2 = lerp(normalize(lightData.direction), normalize(_OriginalDirectionalLightDir2), step(1, _UseOriginalDirectionalLight));
#endif
//#endif
                half halfLambert;
#ifdef TOON_HAIR
                // 髪用のライティング処理
                // 共通のライトの向き
                // 髪の毛などはこっちになると思われる
                halfLambert = 0.5 * dot(i.editNormalDir, lightDirection1) + 0.5;
#else
                // 共通のライトの向き
                halfLambert = (0.5 * dot(i.normalDir, lightDirection1) + 0.5) + (0.5 * dot(i.normalDir, lightDirection2) + 0.5);
                halfLambert = min(1, halfLambert);
#endif
                half3 halfDirection = normalize(viewDirection + lightDirection1);
#endif

#ifdef TOON_SHADING
                half shading = shadowMask * halfLambert;
                half shadingTemp = (_ToonStep - _ToonFeather);
                // _ToonFeatherが0以下だった場合はfinalShadowを0にする
                half finalShadow = lerp(saturate((1 + (shadingTemp - shading) / (_ToonFeather))), 0, step(_ToonFeather, 0));

                half4 toonMap = TEX2D_SAMPLE(_ToonMap, i.uv);
#ifdef USE_MASK_COLOR
                toonMap.rgb *= lerp(1, _MaskToonColorR1, r1).rgb;
                toonMap.rgb *= lerp(1, _MaskToonColorR2, r2).rgb;
                toonMap.rgb *= lerp(1, _MaskToonColorG1, g1).rgb;
                toonMap.rgb *= lerp(1, _MaskToonColorG2, g2).rgb;
                toonMap.rgb *= lerp(1, _MaskToonColorB1, b1).rgb;
                toonMap.rgb *= lerp(1, _MaskToonColorB2, b2).rgb;
#endif // USE_MASK_COLOR
#if defined(USE_TOONCOLOR)
                //ToonColorの場合はテクスチャを参照せず、BaseColorの輝度値を調整したものをトゥーン色とする
                half3 toonColor = baseColor.rgb * _ToonColor.rgb * lightData.color *_GlobalToonColor.rgb;
#else
                half3 toonColor = toonMap.rgb * lightData.color *_GlobalToonColor.rgb;
#endif
                // 頂点カラーのアルファで補正のかかり具合を調整
                half shadowBias = (1 - ((1 - i.vcolor.a) * _VertexColorToonPower) * (0.5 - abs(min(0, halfLambert - 0.5))) * 2);

#ifdef USE_UV_EMISSIVE
                //Emissiveマスクが設定されている箇所は、陰を無効にする
                shadowBias = shadowBias * invEmissiveMask;
#endif
                // Toonの明るい部分の色補正
                half mulStep = step(_ToonBrightColor.a , 0.5);
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

#ifdef USE_UV_EMISSIVE
                //Emissiveマスクが設定されている箇所は、陰を無効にする
                mulStep = mulStep * invEmissiveMask;
                addStep = addStep * invEmissiveMask;
#endif
                baseColor.rgb = baseColor.rgb * lerp( half3( 1, 1, 1 ), _ToonDarkColor.rgb, mulStep) + ( _ToonDarkColor.rgb * addStep);
#endif

#ifdef USE_DIRT
                fixed4 dirtRate = TEX2D_SAMPLE(_DirtTex, i.uv) * _DirtScale;

#if defined(MAYA_HLSL)
                half dirt_a = (dirtRate.r * _DirtRate1) + (dirtRate.g * _DirtRate2) + (dirtRate.b * _DirtRate3);
#else
                half dirt_a = (dirtRate.r * _DirtRate.x) + (dirtRate.g * _DirtRate.y) + (dirtRate.b * _DirtRate.z);
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
                half specularTemp = specularMask * saturate(pow(max(0,rimShading), max(0,1 + _SpecularPower * 10)));
#endif
                //return specularTemp;

                //half3 specularColor = (specularMap.rgb * lightColor) * specularTemp;
                half3 specularColor = (_SpecularColor.rgb * lightData.color) * specularTemp;

                // ios:iphone6(A9系)＆ios10以降の不具合対応
                // specularColorがマイナスになるときが一部端末である。
                // saturate関数では回避できず、max関数を使用して、一度0始まりにする。
#if defined(MAYA_HLSL)
                // Maya用のコード
                half3 fixedSpecularColor = max(half3(0, 0, 0), specularColor);
#else
                // Unity用のコード
                half3 fixedSpecularColor = max(0, specularColor);
#endif

                // 明暗部に加算した際にsaturateによってスペキュラー計算が入る部分が暗くなってしまうのでsaturateを削除
                // baseColor.rgb = saturate(baseColor.rgb + fixedSpecularColor.rgb);

                baseColor.rgb = baseColor.rgb + fixedSpecularColor.rgb;

                //UV Emissiveは汚れより先
#ifdef USE_UV_EMISSIVE
                half2 uvEmissiveUV = _UVEmissiveRange.xy + (((i.uv - _UVEmissiveRange.xy) + _UVEmissiveScroll.xy) % _UVEmissiveRange.zw);
                half4 uvEmissiveColor = TEX2D_SAMPLE(_UVEmissiveTex, uvEmissiveUV);
                float3 emifinalColor = baseColor.rgb + (uvEmissiveColor.rgb * _EmissiveColor.rgb) * emissiveMask;
                baseColor.rgb = saturate(emifinalColor);
#endif

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
                half3 envPower = TEX2D_SAMPLE(_EnvMap, euv).rgb;// *_GlobalEnvColor.rgb;
                half3 env = baseColor.rgb * envPower.rgb * _EnvBias;
                baseColor.rgb = lerp(baseColor.rgb, env, envMask * _EnvRate);
#endif

#ifdef TOON_RIM
                //リム
                //half4 rimColor = lerp(specularMap, _RimColor, _RimSpecRate);
                half4 rimColor = lerp(_SpecularColor, _RimColor, _RimSpecRate);;
                half diffuse = max(0, dot(lightDirection1, i.normalDir));
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
                    dirtColorRim = _GlobalDirtColor.rgb;
                }
                else
                {
                    dirtColorRim = _GlobalDirtRimSpecularColor.rgb;
                }
                baseColor.rgb = lerp(baseColor.rgb, dirtColorRim.rgb, dirt_a);
#endif

#ifdef TOON_FACE
                // shad_cのアルファで頬と鼻の外連味を出す

                // shad_cのアルファが0.51以上なら頬、0.49未満なら鼻
                half cheekThreshold = 0.51;
                half noseThreshold = 0.49;

                // モデルとライトの左右判定。1なら右、-1なら左
                half3 centerDir = i.posWorld.xyz - _FaceCenterPos;
                half modelSide = step(0.0, dot(cross(_FaceForward, centerDir), _FaceUp)) * 2 - 1;
                half lightSide = step(0.0, dot(cross(_FaceForward, lightDirection1), _FaceUp)) * 2 - 1;

                // 1ならライト側、-1ならライトと逆側
                half lightSameSide = modelSide * lightSide;
                // 頬の処理（頬はライトと反対側にオリジナルの色を出す
                // 真後ろから真横の範囲をcheekAnglePowerOffsetずらした値を使用
                half cheekAnglePowerOffset = 0.1;
                half cheekAnglePowerTemp = max(0, dot(_FaceForward, lightDirection1 * -1) + cheekAnglePowerOffset);
                half cheekAnglePower = 1 - (abs(0.5 - cheekAnglePowerTemp) * 2);

                // ライトが下方向に回った時に頬抜きが減衰するように補正
                half vrtPower = min(dot(_FaceUp, lightDirection1), 0) + 1;
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

                //oi_shinya:ios:
                // 謎な不具合：step関数結果をfixedに入れる＞＞その結果を2つ用意してlerp関数に使用するとアセバンビルドでエラーになる
                // なので片方をfloatにして回避している。
                float isCheek = step(cheekThreshold, faceCheatMask);
                fixed cheekPretenseStep = step((1.0 - _CheekPretenseThreshold), cheekPretensePower);
                baseColor.rgb = lerp(baseColor.rgb, cheekColor.rgb, cheekPretenseStep * isCheek);
                
                // 鼻の処理(鼻はライト側にオリジナル、逆側に陰)
                half noseAnglePower = saturate((1 - abs(dot(_FaceForward, lightDirection1))) * 2);

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

                //エミッシブによってキャラカラーが無効にする箇所がある
                float4 charaColor = _CharaColor;

#ifdef USE_UV_EMISSIVE
                //Mask=0だったら、本来の色を乗算する
                charaColor = lerp(float4(1, 1, 1, 1), charaColor, invEmissiveMask);
#endif

                baseColor.rgb *= charaColor.rgb * _LightProbeColor.rgb;

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
                baseColor.rgb += TEX2D_SAMPLE(_EmissiveTex, i.uv).rgb * _EmissiveColor.rgb * final_emi;
#endif

#ifdef TOON_FACE_SHADOW
                //顔影
                float shadowColorRate = saturate((i.posHeadLocal.y - _faceShadowEndY) / _faceShadowLength) * _faceShadowAlpha;
                baseColor.rgb = (1 - tripleMask.b) * baseColor.rgb + tripleMask.b * (1 - shadowColorRate) * baseColor.rgb + tripleMask.b * shadowColorRate * baseColor.rgb * _faceShadowColor.rgb;
#endif

#ifdef USE_HIGHT_LIGHT
                //キャラカラーより高さライトの影響の方が強い
                baseColor.rgb = baseColor.rgb + i.hightColor.rgb;
#endif

#ifdef USE_FOG
                //Fogの影響は最後に受ける
                //GalaxyS9+Android9にて関数だとハングアップするので、直接計算するように変更
                baseColor.rgb = lerp(_Global_FogColor.rgb, baseColor.rgb, i.fogParam);
#endif

#ifdef USE_ALPHA
                baseColor.a *= charaColor.a;
#endif

#ifdef USE_COLOR_FADE
                //残影フェード
                baseColor.rgb = lerp(baseColor.rgb, _FadeColor.rgb, _FadeColor.a);
                baseColor.a *= _FadeRate;
#endif

#ifdef USE_BLOOM_MASK
                return _BloomMask;
#endif

                return baseColor;
            }

#if defined(USE_COLOR_FADE) || defined(USE_DEPTH_ONLY)
            struct appdataDepth
            {
                float3 vertex : POSITION;
            };

            //Depthだけを書き込む処理
            struct v2fDepth
            {
                float4 pos : SV_POSITION;
            };

            v2fDepth vertDepth(appdataDepth v)
            {
                v2fDepth o = (v2fDepth)0;
                o.pos = GallopObjectToClipPos(v.vertex);
#ifdef USE_FIXPROJECTION
                // Blend projection (Perspective)
                float2 pos = o.pos.xy * o.pos.w / _CameraLength;
                o.pos.xy = lerp(o.pos.xy, pos.xy, _FixProjection);
#endif
                return o;
            }

            fixed4 fragDepth(v2fDepth v) : SV_Target
            {
                return fixed4(0, 0, 0, 1);
            }
#endif

#endif  //_DESIGNER_CHARA_TOON_HLSLINC_
