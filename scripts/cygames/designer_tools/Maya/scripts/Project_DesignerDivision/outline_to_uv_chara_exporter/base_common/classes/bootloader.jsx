// ===============================================
// 初期値等の書き込み
// ===============================================
function setup(){

    jsxBridgeSetting.myScriptPath = (new File($.fileName)).parent;
    jsxBridgeSetting.xmlPath = jsxBridgeSetting.myScriptPath + "/xml_setting.xml";
    jsxBridgeSetting.exportPath = jsxBridgeSetting.myScriptPath + "/jsx_bridge_result.xml";
    jsxBridgeSetting.lockFilePath = jsxBridgeSetting.myScriptPath + "/jsx_bridge.lock";

    jsxBridgeParam.targetJsx = undefined;
    
    jsxBridgeResult.status = "";
    jsxBridgeResult.additionalInfo = new Array();

    // ロックファイルの作成
    lockFileObj = new File(jsxBridgeSetting.lockFilePath);
    if(lockFileObj){
        lockFileObj.open("w");
        lockFileObj.write("");
        lockFileObj.close();
    }

}

// ===============================================
// 引数を復元する
// ===============================================
function restoreArgs(){

    var xmlFileObj = new File(jsxBridgeSetting.xmlPath);

    // XMLファイルの読み込み
    if(xmlFileObj){

        var flg = xmlFileObj.open("r");
        if(flg === true){

            // 読み込んだテキストからXMLオブジェクトの作成
            var xmlText = xmlFileObj.read();
            var xmlObj = new XML(xmlText);

            // 必須部のデータを取得
            jsxBridgeParam.targetJsx = xmlObj.target_info.path.child(0);
            jsxBridgeSetting.sessionId = xmlObj.target_info.session_id.child(0);

            // 実データ取り込み
            var elementsCount = xmlObj.args.elements().length();
            for(var i = 0;i<elementsCount;i++){

                var category = xmlObj.args.child(i).localName();

                // 取り込もうとしているアイテムがarrayの場合
                if(category == "array"){

                    var itemName = xmlObj.args.child(i).@name;
                    var tempArray = new Array();
                    var childElementsCount = xmlObj.args.child(i).elements().length();

                    for(var j = 0;j<childElementsCount;j++){
                        var grandChild = xmlObj.args.child(i).child(j);
                        var value = getValue(grandChild);
                        tempArray.push(value);
                    }
                    var cmd = "jsxBridgeParam." + itemName + " = tempArray";
                    eval(cmd);

                // array以外の場合
                }else{

                    var itemName = xmlObj.args.child(i).@name;
                    var value = getValue(xmlObj.args.child(i));

                    var cmd = "jsxBridgeParam." + itemName + "= value;";
                    eval(cmd);

                }
            }
            // 使い終わったら閉じて削除
            flg = xmlFileObj.close();
            if(flg){
                xmlFileObj.remove();
            }
            return true;
        }

    }else{
        alert("XMLファイルの取り込みに失敗しました。");
        return false;
    }
}

// ===============================================
// XMLから実際の値を適した形で復元する
// ===============================================
function getValue(childXML){

    var itemType = childXML.@type;
    var value = childXML.child(0);

    if(itemType == "str" || itemType == "unicode"){
        return value.toString();

    }else if(itemType == "int"){
        return parseInt(value);

    }else if(itemType == "float"){
        return parseFloat(value);

    }else if(itemType == "bool"){
        if(value == "True"){
            return true;
        }else{
            return false;
        }

    }else if(itemType == "array"){
        var arrayName = value.toString().replace("@array/", "")
        var cmd = "jsxBridgeParam." + arrayName;
        return eval(cmd);
    }

}

// ===============================================
// 結果XMLのInfoにアイテムを追加する
// Args:
//      info: itemとして追加するものを渡す。string, number, booleanを想定
// ===============================================
function addResultInfo(info){

    // 辞書型などが持ち込まれた際にははじく
    if((typeof(info) !== "string") && (typeof(info) !== "number") && (typeof(info) !== "boolean")){
        return;
    }

    jsxBridgeResult.additionalInfo.push(info);
}

// ===============================================
// 結果を出力する
// ===============================================
function exportResult(){

    // 共通部分
    var xmlRoot = new XML("<Result><session_id>" + jsxBridgeSetting.sessionId + "</session_id><status>" + jsxBridgeResult.status + "</status></Result>");

    if(jsxBridgeResult.additionalInfo.length != 0){
        var xmlInfo = new XML("<info></info>");
        xmlRoot.insertChildBefore(null, xmlInfo);
    }

    // 追加情報あれば追加
    for(var i = 0;i < jsxBridgeResult.additionalInfo.length;i++){
        escapedVal = escape(jsxBridgeResult.additionalInfo[i]);
        var infoXML = new XML("<item>" + escapedVal + "</item>");
        xmlRoot.info.insertChildBefore(null, infoXML);
    }

    // 書き込み
    var xmlFile = new File(jsxBridgeSetting.exportPath);
    if(xmlFile){
        xmlFile.open("w");
        xmlFile.write(xmlRoot.toString());
        xmlFile.close();
    }
}

// ===============================================
// ロック開放
// ===============================================
function releaseLock(){

    // ロックファイルの削除
    lockFileObj = new File(jsxBridgeSetting.lockFilePath);
    if(lockFileObj){
        lockFileObj.remove();
    }

}

// ===============================================
// メイン関数
// ===============================================
function Main(){

    // 設定
    setup();

    // 引数復元
    var loadResult = restoreArgs();

    if(loadResult === true){

        try{
            var ret = $.evalFile(jsxBridgeParam.targetJsx);
            jsxBridgeResult.status = ret;
        }catch(e){
            jsxBridgeResult.status = 1;
            addResultInfo(e.toString());
        }

    }else{
        jsxBridgeResult.status = 1
        addResultInfo("XML LOAD FAILED");
    }

    // 結果を出力
    exportResult();

    // ロック開放
    releaseLock();
}

// ===============================================
// Global 変数
// ===============================================
var jsxBridgeSetting = Object();
var jsxBridgeParam = Object();
var jsxBridgeResult = Object();

Main();
