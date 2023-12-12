# -*- coding: utf-8 -*-
import os
import subprocess
from sys import exec_prefix
import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya as om
import tool_log
import shr.model.rename_lod.command as cmd

# ------------------------------------------
# 定数
# ------------------------------------------
#fileInfo用
INFO_NAMES = {"path":"animation_export_path","name":"animation_export_name"} 
PROXY_MESH_GRP_NAME = "proxy_mesh_grp"
MESH_GRP_NAME = "mesh"
HUMAN_TYPE = ["ply","npc","mob"]
DEV = True

class exporter():
    def __init__(self,prec_type):
        self.prec_type = prec_type
        self.exportpath = ""
        self.export_target_grps = []

    # ------------------------------------------
    # Pathの取得
    # ------------------------------------------
    @staticmethod
    def get_current_scene_path():
        """
        現在開いているシーンのパスを取得
        """
        fullpath = cmds.file(q=True, sn=True)
        filepath = os.path.dirname(fullpath)
        filename = os.path.basename(fullpath).split(".",1)[0]
        rtn = {"path":filepath,"name":filename}    
        return rtn

    @staticmethod
    def get_current_saved_path():
        """
        現在fileinfoに保存している情報を取得
        """
        filepath = cmds.fileInfo( INFO_NAMES["path"],query=True )[0]
        filename = cmds.fileInfo( INFO_NAMES["name"],query=True )[0]
        rtn = {"path":filepath,"name":filename} 
        return rtn 

    @staticmethod
    def get_current_fbx_path():
        """
        相対的にfbxのパスを取得
        """
        filepath = exporter.get_current_scene_path()["path"].rsplit("/",2)[0] + "/mesh"
        return filepath

    # ------------------------------------------
    # preprocess
    # ------------------------------------------
    def __get_target_joints(self,selected):
        """
        選択以下の骨を取得
        prepで使用
        """
        target_joints = cmds.listRelatives(selected,ad=True,type="joint",pa=True) or []
        if cmds.objectType(selected) == "joint":
            target_joints.extend(selected)
        return target_joints
    
    def __get_group(self,selected,group_type):
        """
        選択以下のproxy meshのgroupを選択
        prepで使用
        """
        groups = cmds.listRelatives(selected,c=True,type="transform",f=True) or []
        
        #proxy_meshのgroupを検索
        if group_type == "proxy_mesh":
            
            for lp in groups:
                if PROXY_MESH_GRP_NAME in lp:
                    return lp

        elif group_type == "mesh":
            for lp in groups:
                if lp.endswith(MESH_GRP_NAME):
                    return lp

        #未使用
        elif group_type == "rig":
            return 0
        return 0

    def __delete_end_joints(self,target_joints):
        """
        選択以下の骨を取得
        prepで使用
        """
        for lp in target_joints:
            if lp.endswith("end"):
                cmds.delete(lp)
                print("delete endjoint >> %s" % lp)

    def __create_shader(self,name, node_type="lambert"):
        """
        shaderの作成
        proxymesh用に用意したものなので、基本はlambertのみで運用
        """
        mtl = cmds.shadingNode(node_type, name=name, asShader=True)  
        
        sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr("%s.outColor" % mtl, "%s.surfaceShader" % sg)

        src_mtl = name.rsplit("_",1)[0]
        color = cmds.getAttr(src_mtl + ".color")

        cmds.setAttr(mtl + ".color", *color[0], type="double3")
        return mtl, sg

    def __asign_shader(self,meshes,sg):
        """
        shaderのassign
        proxymesh用に用意したものなので、基本はlambertのみで運用
        """
        meshes = cmds.ls(meshes, dag=True, type="mesh", noIntermediate=True)
        cmds.sets(meshes, forceElement=sg)
        return

    def _model_prep(self):
        """
        skeletalmeshのエクスポート前に行うシーンのクリーンアップ
        """
        is_raise = False
        try:
            selected = cmds.ls(sl=True)
            target_joints = self.__get_target_joints(selected)
            
            proxy_mesh_grp = self.__get_group(selected,"proxy_mesh")
            
            mesh_grp = self.__get_group(selected,"mesh")
            lod_grps = cmds.listRelatives(mesh_grp,c=True,pa=True) or []
            #meshのgroupをlodグループに置き換え
            self.replace_transform_to_lodgroup(mesh_grp)
            
            #//選択状態を元に戻す、lodgroupの置き換えに入れる
            cmds.select(selected,r=True)
            
            #proxy_mesh_grpが存在していれば
            if proxy_mesh_grp != 0:
                #proxy_meshの整理
                proxy_meshes = cmds.listRelatives(proxy_mesh_grp,ad=True,f=True,type="transform")

                for lod_grp in lod_grps:
                    lod_proxy_mesh_grp = cmds.duplicate(proxy_mesh_grp)[0]
                    cmds.parent(lod_proxy_mesh_grp,lod_grp)
                    
                    #同一階層になっているハズという想定
                    for i,tgt_obj in  enumerate(cmds.listRelatives(lod_proxy_mesh_grp,ad=True,pa=True,type="transform")):
                        src_obj = proxy_meshes[i]
                        exporter.copy_skincluster(src_obj,tgt_obj)

                        #リネームとマテリアルのアサイン（lod0以外）
                        if lod_grp.endswith("lod0"):
                            continue
                        lod_sn = self.get_short_name(lod_grp)

                        tgt_shape = cmds.listRelatives(tgt_obj, shapes=True,f=True)
                        current_sg = cmds.listConnections(tgt_shape, s=False, d=True, t='shadingEngine')
                        current_mat = cmds.ls(cmds.listConnections(current_sg, s=True, d=False), mat=True)[0]
                        
                        mtl,sg = self.__create_shader(current_mat+"_"+lod_sn)
                        self.__asign_shader(tgt_obj,sg)

                        cmds.rename(tgt_obj,tgt_obj+"_"+lod_sn)
                    cmds.rename(lod_proxy_mesh_grp,PROXY_MESH_GRP_NAME)
                cmds.delete(proxy_mesh_grp)

            cmds.select(selected,r=True)
            cmd.rename_lods()
            self.__delete_end_joints(target_joints)
        
            root = exporter.get_hierarchy_root_joint(target_joints[0])
            #root骨をworldにparent
            cmds.parent(root,w=True)
            
            #書き出し用のオブジェクトを選択状態へ
            cmds.select(root,r=True)
            cmds.select(selected,add=True)

        except Exception as e:
            print("例外args:", e.args)
            is_raise = True

        return is_raise

    def _animation_prep(self):
        """
        animationのエクスポート前に行うシーンのクリーンアップ
        """

        is_raise = False
        try:
            selected = cmds.ls(sl=True)
            target_joints = self.__get_target_joints(selected)
            #アニメーションをベイク
            exporter.bake_animation(target_joints)
            
            #リファレンスを複製(namespaceの除去と編集可の状態へ)
            duplicated = cmds.duplicate(target_joints,ic = True,po=True)

            root = exporter.get_hierarchy_root_joint(duplicated[0])
            
            #root骨をworldにparent
            cmds.parent(root,w=True)
            
            #不要なjointの削除
            self.__delete_end_joints(cmds.listRelatives(root,ad=True,type="joint"))

            #書き出し用のオブジェクトを選択状態へ
            cmds.select(root,r=True)
        
        except Exception as e:
            print("例外args:", e.args)
            is_raise = True

        return is_raise


    def _organize_sotai_prep(self):
        selected = cmds.ls(sl=True)
        id = self.get_character_info()
        chr_type = id["character_type"]
        mesh_grp = self.__get_group(selected,"mesh")
        lod_grps = cmds.listRelatives(mesh_grp,c=True,pa=True) or []

        fc_root = None
        fc_mesh_grp = None
        hr_root = None
        hr_mesh_grp = None

        #idの一文字目がprefixになる
        for lp in HUMAN_TYPE:
            if chr_type == lp:
                prefix = lp[0]

        fc_root = cmds.group(em=True,w=True,name="{0}fc{1}".format(prefix,id["character_number"]))
        fc_mesh_grp = cmds.group(em=True,p=fc_root,name="mesh")

        hr_root = cmds.group(em=True,w=True,name="{0}hr{1}".format(prefix,id["character_number"]))
        hr_mesh_grp = cmds.group(em=True,p=hr_root,name="mesh")

        for lod_grp in lod_grps:
            mesh_parts = cmds.listRelatives(lod_grp,c=True,pa=True)
            for mesh_part in mesh_parts:
                if mesh_part.endswith("face"):
                    fc_lod_grp = cmds.group(em=True,p=fc_mesh_grp,name=self.get_short_name(lod_grp))
                    cmds.parent(mesh_part,fc_lod_grp)
                if mesh_part.endswith("hair"):
                    hr_lod_grp = cmds.group(em=True,p=hr_mesh_grp,name=self.get_short_name(lod_grp))
                    cmds.parent(mesh_part,hr_lod_grp)

        cmds.select(selected,r=True)
        self.export_target_grps.extend([fc_root,hr_root])

    def exec_prep(self):
        cmds.undoInfo(openChunk=True)
        if self.prec_type == "model":
            id_dict = self.get_character_info()
            if id_dict["detail_category"] == 0:
                self._organize_sotai_prep()
            
            self._model_prep()
        elif self.prec_type == "animation":
            self._animation_prep()
        cmds.undoInfo(closeChunk=True)

    def check_human_model(self):
        typ = self.get_character_info()["character_type"]
        for lp in HUMAN_TYPE:
            if typ == lp:
                return True
        else:
            return False

    def get_character_info(self):
        scene_name = exporter.get_current_scene_path()["name"]
        number = scene_name[3:]
        character_id = str(number)

        rtn_info = {}
        rtn_info["detail_category"] = int(character_id[0])
        rtn_info["type"] = int(character_id[0:3])
        rtn_info["variation"] = int(character_id[2])
        rtn_info["character_type"] = scene_name[:3]
        rtn_info["character_number"] = scene_name[3:]

        return rtn_info

    def warning_dialog(self):
        selected_btn = cmds.confirmDialog( title='Warning', 
                            message=u'エクスポートには作業データの保存が必要です\nファイルを保存します。よろしいですか?', 
                            button=[u'はい',u'いいえ'], 
                            defaultButton=u'はい', 
                            cancelButton=u'いいえ', 
                            dismissString=u'いいえ')
        if selected_btn == u'はい':
            cmds.file(s=True,de=True)
            return 1
        else:
            return 0

    def export_result_dialog(self,exported_paths):
        #末尾一文字切り取り

        message = "■export assets"
        export_path = ""
        asset_message = "\n\n  ●export_asset"
        export_message = "\n\n  ●export path"
        for lp in exported_paths:
            export_path,name = lp.rsplit("/",1)
            asset_message += "\n    "+name+".fbx"
        else:
            export_message = export_message+"\n    {}".format(export_path)

        message = message+export_message+asset_message
        selected_btn = cmds.confirmDialog( title='Result', 
                            message=message, 
                            button=[u'閉じる','エクスプローラーで開く'], 
                            defaultButton=u'閉じる', 
                            cancelButton=u'閉じる'
                            )
        if selected_btn == u"エクスプローラーで開く":
            export_path = export_path.replace("/","\\")
            subprocess.Popen(['explorer', export_path], shell=True)



    # ------------------------------------------
    # export
    # ------------------------------------------

    def export(self,path="",file_name=""):
        """
        ベースとなるエクスポート関数
        """
        #exportしようとしているfolderが無ければ作成
        os.makedirs(path, exist_ok=True)

        if not DEV:
            self.send_logger()

        if cmds.ls(sl = True) == []:
            cmds.warning(u"対象が選択されていません。rootとなるノードを選択して実行してください。")
            return 0
        
        is_saved= self.warning_dialog()
        if not is_saved:
            cmds.warning(u"ファイルが保存できませんでした。処理を終了します。")
            return 0
        
        exportpath = path+"/s_"+file_name
        self.set_fbx_settings()

        #整頓して選択状態を変更
        is_raise = self.exec_prep()

        if is_raise:
            cmds.file(cmds.file(q=True, sn=True),o=True,f=True)
            return 0

        selected_joint = cmds.ls(sl=True,type="joint")[0]
        exported_fbx_paths = []

        try:
            #書き出し
            om.MGlobal.executeCommand('FBXExport -f "{0}.fbx" -s'.format(exportpath) )
            print("exported >> %s.fbx" % exportpath.replace("/","\\"))
            exported_fbx_paths.append(exportpath)

            #
            count = 1
            if len(self.export_target_grps) != 0:
                for lp in self.export_target_grps:
                    target = [lp,selected_joint]
                    cmds.select(target,r=True)
                    exportpath = path+"/"+self.get_short_name(lp)
                    om.MGlobal.executeCommand('FBXExport -f "{0}.fbx" -s'.format(exportpath) )
                    print("exported >> %s.fbx" % exportpath.replace("/","\\"))
                    exported_fbx_paths.append(exportpath)
                    count += 1
        except RuntimeError:
            cmds.error(u"fbxの書き出しができませんでした。保存先が正しいかご確認ください。")

        #re_open
        # cmds.file(cmds.file(q=True, sn=True),o=True,f=True)
        self.export_result_dialog(exported_fbx_paths)
            
    def export_by_currently_fbx_path(self):
        """
        現在開いているSceneの階層にエクスポート
        """
        filepath = exporter.get_current_fbx_path()
        self.export(filepath,exporter.get_current_scene_path()["name"])

    def export_by_currently_scene_path(self,file_name):
        """
        現在開いているSceneの階層にエクスポート
        """
        filepath = exporter.get_current_scene_path()["path"]
        self.export(filepath,file_name)

    def export_by_currently_saved_path(self):
        """
        現在のinfo保存されている場所にエクスポート
        """
        if cmds.fileInfo( INFO_NAMES["path"],q=True ) == []:
            exporter.initialize_ui_info()
        paths = exporter.get_current_saved_path()
        self.export(paths["path"],paths["name"])



    # ------------------------------------------
    # コマンド
    # ------------------------------------------

    @staticmethod
    def delete_namespace(root):
        """
        namespaceの削除
        """    
        target_assets = cmds.listRelatives(root,ad=True) or []
        nss = []
        
        #削除する必要のあるnamespaceを検索
        for lp in target_assets:
            ns = lp.split(":")[0]
            #namespaceがついている and 既にリストに入っていない
            if ":" in lp and ns not in nss:
                nss.append(ns)
        
        rtn = 0
        for ns in nss:
            cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
            try:
                cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
                print('Namespace deleted:', ns)
                rtn = 1
            except:
                pass
        return rtn

    @staticmethod
    def bake_animation(joints):
        '''
        アニメーションをベイク
        '''
        # Get Character joints
        start = cmds.playbackOptions(q=True, minTime=True)
        end   = cmds.playbackOptions(q=True, maxTime=True)
        # Bake Animation
        cmds.bakeResults(	joints,
                        simulation=True,
                        t=(start,end),
                        sampleBy=1,
                        disableImplicitControl=True,
                        preserveOutsideKeys=False,
                        sparseAnimCurveBake=False,
                        removeBakedAttributeFromLayer=False,
                        bakeOnOverrideLayer=False,
                        minimizeRotation=False,
                        at=['tx','ty','tz','rx','ry','rz','sx','sy','sz'] )
        # Return Result
        return joints

    @staticmethod
    def get_hierarchy_root_joint(joint=""):
        """
        引数jointのrootに当たる骨の取得
        """
        rootJoint = joint

        #再帰処理
        while (True):
            parent = cmds.listRelatives( rootJoint,
                                        parent=True,
                                        type='joint' )
            if not parent:
                break
            rootJoint = parent[0]
        return rootJoint 

    def set_fbx_settings(self):
        """
        fbxの保存設定
        """
        preset_path = os.path.dirname(__file__).replace("\\","/")+"/presets"
        preset_name = "/" + self.prec_type + ".fbxexportpreset"
        preset = preset_path+preset_name
        mel.eval('FBXLoadExportPresetFile -f "{}"'.format(preset))

    def replace_group_to_transform(self,grp):
        """
        grp = transformに置き換えられるグループ
        grpにはlod groupが入る想定
        """
        mesh_grp = grp
        new_grp  = cmds.group(em=True,w=True,n="mesh")
        for lp in cmds.listRelatives(mesh_grp,c=True) or []:
            cmds.parent(lp,new_grp)

        parent = cmds.listRelatives(mesh_grp,p=True)[0]
        cmds.delete(mesh_grp)
        grp = cmds.parent(new_grp,parent)
        cmds.reorder(grp,front=True)

    def replace_transform_to_lodgroup(self,tf):
        """
        tf = lodグループに変換するtransform
        """
        # リネームするためのショートネームを取得 
        sn_mesh_grp = self.get_short_name(tf)
        # 最終的な親階層の取得
        parent_grp = cmds.listRelatives(tf,p=True)[0]
        
        lods = cmds.listRelatives(tf,c=True,pa=True)
        # worldにペアレント
        w_lods = cmds.parent(lods,w=True)
        
        #選択状態をクリア
        cmds.select(clear=True)
        cmds.LevelOfDetailGroup()
        lod_grp = cmds.ls(sl=True)[0]

        #不要なデータの削除
        cmds.delete(cmds.listRelatives(lod_grp,c=True))
        cmds.delete(tf)

        cmds.parent(w_lods,lod_grp)
        cmds.parent(lod_grp,parent_grp)
        cmds.reorder(lod_grp,front=True)
        cmds.rename(lod_grp,sn_mesh_grp)
        return 

    def get_short_name(self,longName):
        if "|" in longName:
            sn = longName.rsplit("|",1)[-1]
        else :
            sn = longName
        return sn

    def send_logger(self):
        logger_type = ""
        version = "v2022.09.02"

        if self.prec_type == "model":
            logger_type = "CharacterExporter"
        elif self.prec_type == "animation":
            logger_type = "AnimationExporter"

        logger = tool_log.get_logger(logger_type,version)
        logger.send_launch("")

    @staticmethod
    def copy_and_rebind(src_obj,parent_grp = ""):
        """
        src_objをコピーしてバインドする
        """
        skincluster_node = mel.eval('findRelatedSkinCluster "{}"'.format(src_obj))
        if len(skincluster_node) == 0:
            return 0
        max_inf = cmds.skinCluster(skincluster_node,q=True,mi=True)
        connection_joint = cmds.listConnections(skincluster_node+".matrix",type="joint")
        duplicate_buff = ""
        if parent_grp != "":
            duplicate_buff = cmds.duplicate(src_obj,rr=True,p=parent_grp)[0]
        else:
            duplicate_buff = cmds.duplicate(src_obj,rr=True)[0]
        cmds.skinCluster(connection_joint,duplicate_buff,removeUnusedInfluence = False,tsb = True,mi = max_inf)
        cmds.copySkinWeights(src_obj,duplicate_buff,nm = True,sa = "closestPoint",ia = ["oneToOne","name"])
        return duplicate_buff

    def copy_skincluster(src_obj,tgt_obj):
        """
        src_objをコピーしてバインドする
        """
        skincluster_node = mel.eval('findRelatedSkinCluster "{}"'.format(src_obj))
        if len(skincluster_node) == 0:
            return 0
        max_inf = cmds.skinCluster(skincluster_node,q=True,mi=True)
        connection_joint = cmds.listConnections(skincluster_node+".matrix",type="joint")
        cmds.skinCluster(connection_joint,tgt_obj,removeUnusedInfluence = False,tsb = True,mi = max_inf)
        cmds.copySkinWeights(src_obj,tgt_obj,nm = True,sa = "closestPoint",ia = ["oneToOne","name"])
        return 
        

    # ------------------------------------------
    # ui
    # ------------------------------------------
    @staticmethod
    def initialize_ui_info():
        """
        fileInfoの初期化(現在のシーンの場所と名前を入れる)
        初めてシーンを開いた際に使用
        アニメーション用
        """
        paths = exporter.get_current_scene_path()
        cmds.fileInfo( INFO_NAMES["path"],paths["path"] )
        cmds.fileInfo( INFO_NAMES["name"],paths["name"] )

def character_export():
    """
    個別実行用
    キャラクターエクスポートの関数
    """
    exp = exporter("model")
    exp.export_by_currently_fbx_path()

def animation_export():
    """
    個別実行用
    アニメーションエクスポートの関数
    """
    exp = exporter("animation")
    exp.export_by_currently_saved_path()
