@echo off

:: Excel ファイルのマクロを実行するvbs
set vbsFile="%~dp0\runExcelMacro.vbs"

:: バッチでは直接ネットワークパスは使えないのでドライブ名を割り当て
net use x: "\\CGS-STR-PRI01-M\mutsunokami_storage\30_design\environment\outsorce\order_form_template"

:: テンプレートのExcel ファイル
set templeteExcelFile="x:\order_form_template_macro.xlsm"

:: コマンドライン引数を環境変数に格納

:: Excel を開くか
set varLaunchExcel=%1

:: アセット名
set varAssetName=%2

:: トライアングル数
set varTriangles=%3

:: テクスチャ解像度
set varResolution=%4

:: 素材
set varPhysicalMaterial=%5

:: コリジョン
set varCollision=%6

:: LOD
set varLod=%7

:: 親マテリアル
set varParentMaterial=%8

:: シェーダ
set varShader=%9

:: ノーマルマップタイプ
shift
set varNormalMapType=%9

:: 作業シーンのパス
shift
set varScenePath=%9

:: 発注者名
shift
set varOrderer=%9

:: キャプチャ画像を貼り付けるか
shift
set varPasteCaptureImage=%9

:: Excel 書き出しフォルダ
shift
set varExportFolderPath=%9

:: エクセルファイルのマクロを実行
%vbsFile% %varLaunchExcel% %templeteExcelFile% createOrderForm

:: ネットワークドライブ名を削除
net use x: /delete

@REM pause
