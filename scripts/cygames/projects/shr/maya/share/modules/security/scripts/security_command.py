# -*- coding: utf-8 -*-
import maya.cmds as cmds

# ====================================
# load plugins
# ====================================

#プラグインを強制的にロード
def force_load_plugins():
    plugins = ["MayaScanner.py","MayaScannerCB.py"]
    #load all plugins
    for check_plugin in plugins:
        if not cmds.pluginInfo(check_plugin, query=True, loaded=True):
            cmds.loadPlugin(check_plugin)
            cmds.pluginInfo(check_plugin, edit=True, autoload=True)
            print("loaded plugin >> {}".format(check_plugin))
    
# ====================================
# remove callbacks
# ====================================

#エディターから不要なコールバックを除去
def remove_corrupted_callbacks(exec_batch = False):
    #必要に応じてtypを配列に変更の必要あり
    target_callbacks = ["CgAbBlastPanelOptChangeCallback"]
    is_fixed = False
    for model_panel in cmds.getPanel(typ="modelPanel"):
        callback = cmds.modelEditor(model_panel, query=True, editorChanged=True)
        for target_callback in target_callbacks:
            if callback == target_callback:
                # Remove the callbacks from the editor
                cmds.modelEditor(model_panel, edit=True, editorChanged="")
                remove_callback_script(target_callbacks)
                print("callback removed >> {}".format(callback) )
                is_fixed = True

    #修正が発生した場合、保存を促すダイアログを表示
    if exec_batch == False:
        if is_fixed:
            confirm = cmds.confirmDialog( 
                            title=u'shenron security tool', 
                            message=u'破損したScriptNodeがシーンに含まれています。修正しましたが、そのまま保存してよろしいでしょうか？', 
                            button=['Yes','No'], 
                            defaultButton='Yes', 
                            cancelButton='No', 
                            dismissString='No' 
                            )
            if confirm == 'Yes':
                cmds.file(save=True)

#uiConfigurationScriptNodeから不要なCallback文を除去
def remove_callback_script(callbacks):
    uiConfigurationScriptNode = cmds.ls("uiConfigurationScriptNode")[0]
    for target_callback in callbacks:        
        before = cmds.getAttr("{}.before".format(uiConfigurationScriptNode))
        settext = before.replace('-editorChanged \\"{0}\\" \\n'.format(target_callback),"")
        settext = settext.replace('-editorChanged "{0}"'.format(target_callback),"")
        cmds.setAttr("{}.before".format(uiConfigurationScriptNode),settext,type="string")
