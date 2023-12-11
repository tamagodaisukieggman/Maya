const DIRT_FOLDER_NAME = "dirt";

function Main(){

    var self = this;
    var doc = app.activeDocument;

    if (!doc){
        return;
    }

    // psdとbmpのパスを取得
    var docPath = doc.fullName.fsName;
    var psdPath = docPath.replace('.bmp', '.psd');

    // psdとbmpのファイルオブジェクト作成
    var psdFileObj = new File(psdPath);
    var bmpFileObj = new File(docPath);

    if (!psdFileObj.exists){
        return;
    }

    // 元々のpsdを削除
    doc.close(SaveOptions.DONOTSAVECHANGES);
    psdFileObj.remove()

    // bmpを開く
    open(bmpFileObj);
    doc = app.activeDocument;

    // dirtレイヤーセットに入れる
    var layerList = doc.layers;
    var bgLayer = layerList[0];
    bgLayer.opacity = 100;

    var dirtLayerSet = activeDocument.layerSets.add();
    dirtLayerSet.name = DIRT_FOLDER_NAME;
    bgLayer.move(dirtLayerSet, ElementPlacement.INSIDE);

    // psd保存
    var psdSaveOpt = new PhotoshopSaveOptions();
    psdSaveOpt.alphaChannels = true;
    psdSaveOpt.embedColorProfile = false;
    psdSaveOpt.layers = true;
    psdSaveOpt.spotColors = false;
    app.activeDocument.saveAs(psdFileObj, psdSaveOpt, true, Extension.LOWERCASE);

    // bmpを削除
    doc.close(SaveOptions.DONOTSAVECHANGES);
    bmpFileObj.remove();

    // psdを開く
    if (psdFileObj.exists){
        open(psdFileObj);
    }
}

Main();