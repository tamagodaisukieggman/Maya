const FACIAL_TARGET_SUFFIX = '_facial_target_tmp';
const FACIAL_FINAL_SUFFIX = '_facial_target';
const FACIAL_SAVE_DIR_PATH = 'W:/gallop/svn/svn_gallop/80_3D/01_character/02_faical_list/facial'

const EAR_TARGET_SUFFIX = '_ear_target_tmp';
const EAR_FINAL_SUFFIX = '_ear_target';
const EAR_SAVE_DIR_PATH = 'W:/gallop/svn/svn_gallop/80_3D/01_character/02_faical_list/ear'

const FACE_TYPE_TARGET_SUFFIX = '_face_type_target_tmp';
const FACE_TYPE_FINAL_SUFFIX = '_face_type_target';
const FACE_TYPE_SAVE_DIR_PATH = 'W:/gallop/svn/svn_gallop/80_3D/01_character/02_faical_list/face_type'

utility = {

    //==================================================
    /**
     * 
     */
    getFixPath: function (targetPath) {
        return targetPath.replace(/\\/g, '/');
    },

    //==================================================
    /**
     * 
     */
    getDirPath: function (targetPath) {

        targetPath = utility.getFixPath(targetPath);

        if (targetPath.indexOf('/') < 0) {
            return targetPath;
        }

        splitList = targetPath.split('/');

        dirPath = '';

        for (var p = 0; p < splitList.length - 1; p++) {

            dirPath += splitList[p];

            if (p < splitList.length - 2) {
                dirPath += '/';
            }
        }

        return dirPath;
    },

    //==================================================
    /**
     * 
     */
    getFileName: function (targetPath) {

        targetPath = utility.getFixPath(targetPath);

        if (targetPath.indexOf('/') < 0) {
            return targetPath;
        }

        splitList = targetPath.split('/');

        return splitList[splitList.length - 1];
    },

    //==================================================
    /**
     * 
     */
    getFileNameNoExt: function (targetPath) {

        fileName = utility.getFileName(targetPath);

        if (fileName.indexOf('.') < 0) {
            return fileName;
        }

        splitList = fileName.split('.');

        return splitList[0];
    },

    //==================================================
    /**
     * 
     */
    getFileExtension: function (targetPath) {

        fileName = utility.getFileName(targetPath);

        if (fileName.indexOf('.') < 0) {
            return '';
        }

        splitList = fileName.split('.');

        return splitList[splitList.length - 1];
    },

    //==================================================
    /**
     * 
     */
    getFixLayerName: function (targetString) {

        if (targetString.indexOf(' ') < 0) {
            return targetString;
        }

        splitList = targetString.split(' ');

        return splitList[0];
    },

    //==================================================
    /**
     * 
     */
    clippingToUnderLayer: function () {

        if (!app.activeDocument.activeLayer) {
            return
        }

        var ref = new ActionReference();
        ref.putEnumerated( charIDToTypeID( 'Lyr ' ), charIDToTypeID( 'Ordn' ), charIDToTypeID( 'Trgt' ) );

        var desc = new ActionDescriptor();
        desc.putReference( charIDToTypeID( 'null' ), ref );

        executeAction( charIDToTypeID( 'GrpL' ), desc, DialogModes.NO );

    }
}

function Main(){

    var self = this;
    var rootPath = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model\\head';

    //==================================================
    /**
     * headフォルダ配下で_facial_target_tmpなど一時的にしかできていないはずの名前のpsdを検索しリストする。
     * Pythonツールから一連の流れでPhotoshopで処理をする時「Photoshop.exe path_to_jsx」で処理を実行しているため
     * パラメータが渡せないのでこの方法を取っていると思われる。
     * gallopではvirtual_drive_setting.exeなどを使いsubstで仮想ドライブWを割り当てる運用。
     */
    self.getTargetPsd = function () {

        var folderObj = Folder(rootPath);

        var resultList = []
        SearchPsd(folderObj);

        function SearchPsd(folderObj){

            var contentsList = folderObj.getFiles();

            for (var i in contentsList){

                if (contentsList[i]instanceof Folder){
                    SearchPsd(contentsList[i]);
                }

                if (contentsList[i]instanceof File){

                    var fileName = contentsList[i].name;

                    if (fileName.match(FACIAL_TARGET_SUFFIX) || fileName.match(EAR_TARGET_SUFFIX) || fileName.match(FACE_TYPE_TARGET_SUFFIX)) {
                        resultList.push(contentsList[i])
                    }
                }
            }
        }

        return resultList;
    }

    self.targetPsdList = self.getTargetPsd();

    if(self.targetPsdList.length == 0){
        alert("処理対象のpsdが見つかりませんでした");
        return;
    }

    var openErrorFiles = [];

    for (var i=0; i<self.targetPsdList.length; i++) {
        try{
            open(self.targetPsdList[i]);
        }
        catch(ex){
            openErrorFiles.push("ファイルオープンエラー:" + self.targetPsdList[i])
            continue;
        }

        var thisDoc = app.activeDocument;

        var listCreator = new CreateFacialList();
        listCreator.execute();

        thisDoc.close(SaveOptions.DONOTSAVECHANGES);

        var targetSuffix = '';
        var finalSuffix = '';

        if (self.targetPsdList[i].name.match(FACIAL_TARGET_SUFFIX)) {
            targetSuffix =  FACIAL_TARGET_SUFFIX;
            finalSuffix = FACIAL_FINAL_SUFFIX;
        }
        else if (self.targetPsdList[i].name.match(EAR_TARGET_SUFFIX)) {
            targetSuffix =  EAR_TARGET_SUFFIX;
            finalSuffix = EAR_FINAL_SUFFIX;
        }
        else if (self.targetPsdList[i].name.match(FACE_TYPE_TARGET_SUFFIX)) {
            targetSuffix =  FACE_TYPE_TARGET_SUFFIX;
            finalSuffix = FACE_TYPE_FINAL_SUFFIX;
        }

        var dstFileObj = new File(self.targetPsdList[i].fullName.replace(targetSuffix, finalSuffix));

        if (dstFileObj.exists) {
            dstFileObj.remove();
        }

        self.targetPsdList[i].rename(self.targetPsdList[i].fullName.replace(targetSuffix, finalSuffix));
    } 

    // ファイルオープンエラーになったpsdがあったらログで報告
    if(openErrorFiles && openErrorFiles.length > 0){
        var confirmWindow;
        var logFileName = "ErrorLog.txt";
        var saveFile = new File(Folder.desktop + "/" + logFileName);
        if (saveFile.exists) {
            // 上書き、もしくはファイル名を指定できるポップアップ
            var res =
            "dialog { \
                properties:{ resizeable: true, closeButton: true }, \
                info: Panel { \
                    orientation: 'column', \
                    text: '「ErrorLog.txt」はデスクトップに既にあります', \
                    name: Group { \
                        orientation: 'row', \
                        s: StaticText { text:'エラーログのファイル名:' }, \
                        e: EditText { characters: 30, text: '" + logFileName + "'} \
                    }, \
                }, \
                buttons: Group { \
                    orientation: 'row', \
                    saveBtn: Button { text:'この名前で保存', properties:{name:'save'} }, \
                    cancelBtn: Button { text:'Cancel', properties:{name:'cancel'} } \
                } \
            }";

            confirmWindow = new Window (res);
            confirmWindow.buttons.saveBtn.onClick = function () {
                // winオブジェクトは残るのでファイル名はそこから取る
                confirmWindow.close();
            }
            confirmWindow.center();
            // isCancelled: save=0, cancel=2, closeButton=2
            var isCancelled = confirmWindow.show();
            if(isCancelled==0){
                logFileName = confirmWindow.info.name.e.text.replace(/^s+|s+$/g,'');
                if(logFileName == ""){
                    // 万が一ユーザーがファイル名を削除した上で「この名前で保存」するようならデフォルトで上書きする
                    logFileName = "ErrorLog.txt"
                }
            }
        }
        saveFile = new File(Folder.desktop + "/" + logFileName);
        saveFile.open("wa");
        saveFile.write(openErrorFiles.join("\n"));
        saveFile.close();
        alert("""ファイルオープンエラーになったpsdがありました。\n
              デスクトップに書き出しましたのでご確認ください\n""" + logFileName);
    }else{
        alert('出力完了');
    }
}

function CreateFacialList() {

    var self = this;

    self.baseDocument = activeDocument;
    self.exportType = "";

    self.targetSuffix = null;
    self.finalSuffix = null;

    self.saveDirPath = null;

    self.baseFilePath = null;
    self.baseDirPath = null;
    self.baseFileName = null;
    self.baseFileNameNoExt = null;
    self.baseFileExtension = null;

    self.targetFileObjList = null;
    self.titleFileObj = null;

    self.baseTitleLayer = null;

    self.templateLayerSet = null;
    self.templateAnchorLayer = null;
    self.templateSizeLayer = null;

    self.positionLayerSetItemList = null;

    //==================================================
    /**
     * 現在のドキュメント(xxx_ear_target_tmp.psd)の中に表情のpng画像を配置して
     * 80_3D/01_character/02_faical_list/ear フォルダの中にjpgを書き出す。
     */
    self.execute = function () {
        // 例: chr1001_00_ear_target_tmp.psd
        self.baseDocument = activeDocument;

        if (self.baseDocument == null) {
            return;
        }

        self.baseFilePath = utility.getFixPath(self.baseDocument.fullName.fsName);
        self.baseDirPath = utility.getDirPath(self.baseFilePath);
        self.baseFileName = utility.getFileName(self.baseFilePath);
        self.baseFileNameNoExt = utility.getFileNameNoExt(self.baseFileName);
        self.baseFileExtension = utility.getFileExtension(self.baseFileName);

        self.checkFile(); // self.targetFileObjListにtarget_xxx.pngを格納

        self.checkDocument();
        self.setTitle();
        self.checkTemplateLayerSet();
        self.duplicateTemplateLayerSet();
        self.saveDocument(); // psdドキュメントを保存するとともに、ここでjpgも書き出している
        // self.openExplorer();
    }

    //==================================================
    /**
     * psdと同じフォルダ内のpngをリストし
     * ターゲット一覧のpng(title_xxx.png)だったらself.titleFileObjにセット
     * それ以外のpngはself.targetFileObjListに格納
     * title__【 耳のターゲット一覧 chr1001_00 】.png
     */
    self.checkFile = function () {

        self.targetFileObjList = [];
        self.titleFileObj = null;

        var baseDirObj = new Folder(self.baseDirPath);

        tempFileObjList = baseDirObj.getFiles('*.png');

        for (var p = 0; p < tempFileObjList.length; p++) {

            var thisFileObj = tempFileObjList[p];

            var thisFileName = thisFileObj.name;

            if (thisFileName.indexOf('title') >= 0) {
                self.titleFileObj = thisFileObj;
            }
            else {
                self.targetFileObjList.push(thisFileObj);
            }
        }

        self.targetFileObjList.sort();
    }

    //==================================================
    /**
     * 
     */
    self.checkDocument = function () {

        self.positionLayerSetItemList = []
        var layerList = self.baseDocument.layers;

        self.targetSuffix = '';
        self.finalSuffix = '';

        if (self.baseDocument.name.match(FACIAL_TARGET_SUFFIX)) {
            self.exportType = "facial_target";
            self.targetSuffix = FACIAL_TARGET_SUFFIX;
            self.finalSuffix = FACIAL_FINAL_SUFFIX;
            self.saveDirPath = FACIAL_SAVE_DIR_PATH;
        }
        else if (self.baseDocument.name.match(EAR_TARGET_SUFFIX)) {
            self.exportType = "ear_target";
            self.targetSuffix = EAR_TARGET_SUFFIX;
            self.finalSuffix = EAR_FINAL_SUFFIX;
            self.saveDirPath = EAR_SAVE_DIR_PATH;
        }
        else if (self.baseDocument.name.match(FACE_TYPE_TARGET_SUFFIX)) {
            self.exportType = "face_type";
            self.targetSuffix = FACE_TYPE_TARGET_SUFFIX;
            self.finalSuffix = FACE_TYPE_FINAL_SUFFIX;
            self.saveDirPath = FACE_TYPE_SAVE_DIR_PATH;
        }

        for (var p = 0; p < layerList.length; p++) {

            var thisLayer = layerList[p];

            if (thisLayer.name == 'title') {
                self.baseTitleLayer = thisLayer;
            }
            else if (thisLayer.name == 'ItemTemplate') {
                self.templateLayerSet = thisLayer;
            }
            else if (thisLayer.name == 'ItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('Ear', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
            else if (thisLayer.name == 'BrowItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('Brow', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
            else if (thisLayer.name == 'EyeItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('Eye', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
            else if (thisLayer.name == 'MouthItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('Mouth', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
            else if (thisLayer.name == 'Type0ItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('セット表情', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
            else if (thisLayer.name == 'Type1ItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('目のみの表情', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
            else if (thisLayer.name == 'Type2ItemPosition') {

                var thisItem = new PositionLayerSetItem();
                thisItem.createItem('口のみの表情', thisLayer);
                self.positionLayerSetItemList.push(thisItem);

            }
        }
    }

    //==================================================
    /**
     * 「title」という名前のテキストレイヤーにタイトルテキストを設定する
     */
    self.setTitle = function () {

        if (self.baseTitleLayer == null) {
            return;
        }

        if (self.titleFileObj == null) {
            return;
        }

        var thisFileNameNoExt = utility.getFileNameNoExt(self.titleFileObj.fullName);
        // 例：title__【 耳のターゲット一覧 chr1001_00 】だったら【 耳のターゲット一覧 chr1001_00 】
        var splitList = thisFileNameNoExt.split('__');
        var title = splitList[1];
        // 「title」テキストレイヤーのテキストを設定。
        self.baseTitleLayer.textItem.contents = title;
    }

    //==================================================
    /**
     * 「ItemTemplate」レイヤーセットの中の各レイヤーの表示状態を設定
     */
    self.checkTemplateLayerSet = function () {

        if (self.templateLayerSet == null) {
            alert("「ItemTemplate」レイヤーセットがなかったので処理できません")
            return;
        }

        var layerList = self.templateLayerSet.layers;
        if (layerList == null) {
            alert("「ItemTemplate」レイヤーセットの中にレイヤーがありませんでした")
            return;
        }

        for (var p = 0; p < layerList.length; p++) {

            var thisLayer = layerList[p];

            if (thisLayer.name == 'anchor') {
                self.templateAnchorLayer = thisLayer;
                thisLayer.visible = false;
            }
            else if (thisLayer.name == 'info0') {
                thisLayer.visible = true;
            }
            else if (thisLayer.name == 'info1') {
                thisLayer.visible = true;
            }
            else if (thisLayer.name == 'info2') {
                thisLayer.visible = true;
            }
            else if (thisLayer.name == 'size') {
                self.templateSizeLayer = thisLayer;
                thisLayer.visible = true;
            }
            else if (thisLayer.name == 'waku0') {
                thisLayer.visible = false;
            }
            else if (thisLayer.name == 'waku1') {
                thisLayer.visible = false;
            }
        }
    }

    //==================================================
    /**
     * 
     */
    self.duplicateTemplateLayerSet = function () {

        if (!self.positionLayerSetItemList) {
            return;
        }

        if (self.targetFileObjList == null) {
            return;
        }

        if (self.targetFileObjList.length == 0) {
            return;
        }

        var tempAnchorBounds = self.templateAnchorLayer.bounds;

        var tempAnchorCenter = [tempAnchorBounds[0] + tempAnchorBounds[2], tempAnchorBounds[1] + tempAnchorBounds[3]];
        tempAnchorCenter[0] *= 0.5;
        tempAnchorCenter[1] *= 0.5;

        var tempSizeBounds = self.templateSizeLayer.bounds;

        var tempSizeCenter = [tempSizeBounds[0] + tempSizeBounds[2], tempSizeBounds[1] + tempSizeBounds[3]];
        tempSizeCenter[0] *= 0.5;
        tempSizeCenter[1] *= 0.5;

        var tempSizeSize = [tempSizeBounds[2] - tempSizeBounds[0], tempSizeBounds[3] - tempSizeBounds[1]];

        for (var p = 0; p < self.targetFileObjList.length; p++) {

            var thisFileObj = self.targetFileObjList[p];
            var thisFilePath = self.targetFileObjList[p].fullName;
            var thisFileNameNoExt = utility.getFileNameNoExt(thisFilePath);
            //----------------------

            var splitList = thisFileNameNoExt.split('__');
            var index = null;
            var info0 = null;
            var info1 = null;
            var info2 = null;
            var info3 = null;
            var wakuType = null;

            if (self.exportType == "facial_target" || self.exportType == "ear_target"){
                index = splitList[0];
                info0 = splitList[1];
                info1 = splitList[2];
                info2 = splitList[3];
                info3 = splitList[4];
                wakuType = splitList[5];
            }
            else if (self.exportType == "face_type"){
                index = splitList[1];
                info0 = splitList[2];
                info1 = splitList[1];
                info3 = splitList[0];
            }

            //----------------------

            var targetPosLayer = null;
            var targetPosLayerList = null;
            var targetLabel = null;

            if (info3 == 'Eyebrow_L') {
                targetLabel = 'Brow';
            }
            else if (info3 == 'Eye_L') {
                targetLabel = 'Eye';
            }
            else if (info3 == 'Mouth') {
                targetLabel = 'Mouth';
            }
            else if (info3 == 'Ear') {
                targetLabel = 'Ear';
            }
            else if (info3 == '0') {
                targetLabel = 'セット表情';
            }
            else if (info3 == '1') {
                targetLabel = '目のみの表情';
            }
            else if (info3 == '2') {
                targetLabel = '口のみの表情';
            }

            for (var q = 0; q < self.positionLayerSetItemList.length; q++) {
                if (self.positionLayerSetItemList[q].label == targetLabel) {
                    targetPosLayerList = self.positionLayerSetItemList[q].positionLayerList;
                }
            }

            if (!targetPosLayerList) {
                continue;
            }

            for (var q = 0; q < targetPosLayerList.length; q++) {

                var thisLayer = targetPosLayerList[q];

                if (thisLayer.name == info1) {
                    targetPosLayer = thisLayer;
                    break;
                }
            }

            if (targetPosLayer == null) {
                continue;
            }

            //----------------------

            var dupLayer = self.templateLayerSet.duplicate(self.baseDocument, ElementPlacement.PLACEATBEGINNING);
            dupLayer.name = info0;

            //----------------------

            app.open(thisFileObj);

            var imageDoc = app.activeDocument;

            var imageSize = [0, 0]

            if (info3 == 'Mouth') {
                imageSize[0] = tempSizeSize[0] * 1.5;
                imageSize[1] = tempSizeSize[0] * 1.5;
            }
            else if (info3 == 'Ear') {
                imageSize[0] = tempSizeSize[0];
                imageSize[1] = tempSizeSize[1];
            }
            else {
                imageSize[0] = tempSizeSize[0];
                imageSize[1] = tempSizeSize[0];
            }

            imageDoc.resizeImage(imageSize[0], imageSize[1]);

            imageDoc.layers[0].duplicate(self.baseDocument);

            app.activeDocument = imageDoc;
            imageDoc.close(SaveOptions.DONOTSAVECHANGES);

            app.activeDocument = self.baseDocument;

            var imageLayer = self.baseDocument.activeLayer;

            thisImageOffset = [0, 0];

            thisImageOffset[0] = tempSizeCenter[0] - imageSize[0] * 0.5;

            if (info3 == 'Eye_L') { // 中央合わせ
                thisImageOffset[1] = tempSizeCenter[1] - imageSize[1] * 0.35;
            }
            else if (info3 == 'Mouth') { // 下端合わせ
                thisImageOffset[1] = tempSizeCenter[1] - (imageSize[1] * 1.0 - tempSizeSize[1] * 0.5);
            }
            else { // 上端合わせ
                thisImageOffset[1] = tempSizeCenter[1] - tempSizeSize[1] * 0.5;
            }

            imageLayer.translate(thisImageOffset[0], thisImageOffset[1]);

            imageLayer.move(dupLayer, ElementPlacement.INSIDE);

            //----------------------

            var dupLayerList = dupLayer.layers;
            for (var q = 0; q < dupLayerList.length; q++) {

                var thisLayer = dupLayerList[q];
                var thisLayerFixName = utility.getFixLayerName(thisLayer.name)

                if (thisLayerFixName == 'info0') {

                    thisLayer.textItem.contents = info0;

                    if (info0 == '') {
                        thisLayer.visible = false;
                    }
                }
                else if (thisLayerFixName == 'info1') {

                    thisLayer.textItem.contents = info1;

                    if (info1 == '') {
                        thisLayer.visible = false;
                    }
                }
                else if (thisLayerFixName == 'info2' && info2 != '') {

                    thisLayer.textItem.contents = info2;

                    if (info2 == '') {
                        thisLayer.visible = false;
                    }
                }
                else if (thisLayerFixName == 'size') {

                    imageLayer.move(thisLayer, ElementPlacement.PLACEBEFORE);
                    app.activeDocument.activeLayer = imageLayer;

                    utility.clippingToUnderLayer();
                }
                else if (thisLayerFixName == 'anchor') {
                }
                else if (thisLayerFixName == 'waku0' && wakuType == '1') {
                    thisLayer.visible = true;
                }
                else if (thisLayerFixName == 'waku1' && wakuType == '2') {
                    thisLayer.visible = true;
                }
            }

            //----------------------

            var thisPosBounds = targetPosLayer.bounds;

            var thisPosCenter = [thisPosBounds[0] + thisPosBounds[2], thisPosBounds[1] + thisPosBounds[3]];
            thisPosCenter[0] *= 0.5;
            thisPosCenter[1] *= 0.5;

            thisPosOffset = [0, 0];
            thisPosOffset[0] = thisPosCenter[0] - tempAnchorCenter[0];
            thisPosOffset[1] = thisPosCenter[1] - tempAnchorCenter[1];

            var mergedLayer = dupLayer.merge();

            mergedLayer.translate(thisPosOffset[0], thisPosOffset[1]);
            
        }

        //self.baseDocument.activeLayer = self.templateLayerSet;
        self.templateLayerSet.remove();

        for (var p = 0; p < self.positionLayerSetItemList.length; p++) {

            if (self.positionLayerSetItemList[p].titleLayer) {

                self.positionLayerSetItemList[p].setTitle(self.positionLayerSetItemList[p].label);
                self.positionLayerSetItemList[p].titleLayer.move(self.positionLayerSetItemList[p].positionLayerSet, ElementPlacement.PLACEBEFORE);

            }

            self.positionLayerSetItemList[p].positionLayerSet.remove();
        }
    }

    //==================================================
    /**
     * 
     */
    self.saveDocument = function () {

        //----------------------

        self.baseDocument.save();

        //----------------------

        saveDirPath = ''

        if (Folder(self.saveDirPath).exists) {
            saveDirPath = self.saveDirPath;
        }
        else {
            saveDirPath = self.baseDirPath;
        }

        var jpgFilePath = saveDirPath + '/' + self.baseFileNameNoExt.replace(self.targetSuffix, self.finalSuffix) + '.jpg'

        var jpgSaveOptions = new JPEGSaveOptions();
        jpgSaveOptions.quality = 12;

        self.baseDocument.saveAs(new File(jpgFilePath), jpgSaveOptions, true);
    }

    //==================================================
    /**
     * 
     */
    self.openExplorer = function () {

        var folderObj = new Folder(self.baseDirPath);

        folderObj.execute()
    }

}

function PositionLayerSetItem() {

    var self = this;
    const TITLE_LAYER_NAME = 'PartTitle'

    self.label = null;
    self.positionLayerSet = null;
    self.titleLayer = null;
    self.positionLayerList = null;

    //==================================================
    /**
     * 
     */
    self.createItem = function (label, positionLayerSet) {

        self.label = label;
        self.positionLayerSet = positionLayerSet;

        self.positionLayerList = [];

        var positionLayerList = self.positionLayerSet.layers;

        for (var p = 0; p < positionLayerList.length; p++) {

            var thisLayer = positionLayerList[p];

            if (thisLayer.name == TITLE_LAYER_NAME) {
                self.titleLayer = thisLayer;
                continue;
            }

            self.positionLayerList.push(thisLayer);
        }
    }

    //==================================================
    /**
     * 
     */
    self.setTitle = function (title) {

        if (!self.titleLayer) {
            return;
        }

        self.titleLayer.textItem.contents = title;
    }
    
}


Main();
