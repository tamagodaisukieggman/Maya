# -*- coding: shift-jis -*-
import maya.cmds as cmds
import webbrowser
import json
import os
from collections import OrderedDict

    
JSON_PATH = os.getenv("HOMEDRIVE")+os.getenv("HOMEPATH")+'\Documents\maya\Scripting_Files\Reconnect_Joint.json'

grp_list = []
result_path = JSON_PATH





# ファイル書き出し
def exportJson(path_=r'', dict={}):
    
    if not os.path.isdir(os.path.dirname(path_)):
        os.makedirs(os.path.dirname(path_))
    f = open(path_, 'w')
    json.dump(dict, f, indent=4)
    f.close()




# ファイル読み込み
def importJson(path=r''):
    
    f = open(path, 'r')
    tmp = f.read()
    res = json.loads(tmp, object_pairs_hook=OrderedDict)
    f.close()
    return res




# idのチェック_pl
def id_check_pl(*args):     
 
          
    pl_jointlist = [u'null', u'_900', u'_000', u'_001', u'_002', u'_003', u'_004', u'_005', u'del_005', u'_00a', u'_00b', u'_00c', u'_00d' \
                , u'_200', u'_201', u'_202', u'del_202', u'_211', u'_212', u'_213', u'del_213', u'_221', u'_222', u'_223', u'del_223' \
                , u'_230', u'_231', u'_232', u'_233', u'del_233', u'_240', u'_241', u'_242', u'_243', u'del_243', u'_a0d', u'_a21' \
                , u'_a0c', u'_a38', u'_a37', u'_a30', u'_a0b', u'_006', u'_007', u'_008', u'_009', u'_100', u'_101', u'_102', u'del_102' \
                , u'_111', u'_112', u'_113', u'del_113', u'_121', u'_122', u'_123', u'del_123', u'_130', u'_131', u'_132', u'_133', u'del_133' \
                , u'_140', u'_141', u'_142', u'_143', u'del_143', u'_a09', u'_a31', u'_a08', u'_a28', u'_a27', u'_a20', u'_a07', u'_a0a', u'_a06' \
                , u'_a04', u'_012', u'_013', u'_014', u'_015', u'del_015', u'_a14', u'_a33', u'_a13', u'_a39', u'_a3a', u'_a32', u'_00e', u'_00f' \
                , u'_010', u'_011', u'del_011', u'_a10', u'_a23', u'_a0f', u'_a29', u'_a2a', u'_a22', u'_a12', u'_a34', u'_a35', u'_a36', u'_a0e', u'_a24', u'_a25', u'_a26']

    
    id_node = cmds.listRelatives('null', parent=True, path=True)
    id = id_node[0]
    joint_list = cmds.ls('null', dag=True, type='joint')
    print(id)


    # pl****
    if 'pl' in id:
        disconnect_joint(joint_list, pl_jointlist)

          
    else:
        cmds.confirmDialog(message=u'plのデータを使用してください。', icn='warning')




# idのチェック_np
def id_check_np(*args):     
                                         
    np_jointlist = [u'null', u'_900', u'_000', u'_001', u'_002', u'_003', u'_004', u'_005', u'_00a', u'_00b', u'_00c', u'_00d', u'_200', u'_201' \
                , u'_202', u'del_202', u'_211', u'_212', u'_213', u'del_213', u'_221', u'_222', u'_223', u'del_223', u'_241', u'_242', u'_243' \
                , u'del_243', u'_231', u'_232', u'_233', u'del_233', u'_a21', u'_a30', u'_a38', u'_006', u'_007', u'_008', u'_009', u'_100' \
                , u'_101', u'_102', u'del_102', u'_111', u'_112', u'_113', u'del_113', u'_121', u'_122', u'_123', u'del_123', u'_131', u'_132' \
                , u'_133', u'del_133', u'_141', u'_142', u'_143', u'del_143', u'_a31', u'_a20', u'_a28', u'_012', u'_013', u'_014', u'_015' \
                , u'del_015', u'_a33', u'_a32', u'_a39', u'_00e', u'_00f', u'_010', u'_011', u'del_011', u'_a23', u'_a22', u'_a29']

    
    id_node = cmds.listRelatives('null', parent=True, path=True)
    id = id_node[0]
    joint_list = cmds.ls('null', dag=True, type='joint')
    print(id)


    # np****
    if 'np' in id:
        disconnect_joint(joint_list, np_jointlist)

       
    else:
        cmds.confirmDialog(message=u'npのデータを使用してください。', icn='warning')




# ファイルパスの選択
def file_set(*args):
    
    global result_path
    
    basicFilter = "*.json"
    result_file = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fileMode=0, caption='Select File')
    result_path = str(result_file[0])
    cmds.textField('file_path', e=True, text=result_path.replace('u',''))




# 接続の解除（pl, np）
def disconnect_joint(joint_list, id_jointlist):  
    
    r_jointlist = []     
    child_list = []
    parent_list = []
    
    
    # 解除するジョイントの親のみピックアップ         
    for j in joint_list:
        if j in id_jointlist:
            pass
        else:
            r_jointlist.append(j)
    
    p_jointlist = cmds.listRelatives(r_jointlist, parent=True, path=True)
     
    for pj,j in zip(p_jointlist, r_jointlist):    
        if pj in id_jointlist:
            child_list.append(j)
            parent_list.append(pj)
            
        else:
            pass
    
    print(child_list)
    print(parent_list)
   
    
    set_grp(child_list, parent_list)
          


    
def disconnect_joint_exe(child_list, parent_list, grp_list):
    
    global result_path
    print(result_path)
    
       
    # 接続の解除
    setting_dict = {'child_list':child_list, 'parent_list':parent_list }
    exportJson(result_path, setting_dict)
    
    for j in child_list:
        cmds.parent(j, w=True)
        
        
    # グループを解除したジョイントとペアレント
    for j,g in zip(child_list, grp_list):
        cmds.parent(j, g)
    
    
    # 解除したジョイントをグループ化
    cmds.group(grp_list, n='grp_sec_joint')





# 接続の解除（pl, np以外）
def disconnect_joint_other(*args):
    
    global result_path
    print(result_path)
    
    # 解除したいジョイントを選択
    child_list = cmds.ls(sl=True)
    
    
    if not child_list:
        # 解除したいジョイントを選択していない場合はエラー
        cmds.confirmDialog(message=u'ペアレント解除したいジョイントを選択してください。', icn='warning')
    
    else:
        parent_list = cmds.listRelatives(child_list, parent=True, path=True)
        setting_dict = {'child_list':child_list, 'parent_list':parent_list}
        print(setting_dict)
        
        exportJson(result_path, setting_dict)
        
        set_grp(child_list, parent_list)
    



def disconnect_joint_other_exe(child_list, parent_list,grp_list): 
    
    for j in child_list:
        cmds.parent(j, w=True)


    # グループを解除したジョイントとペアレント
    for j,g in zip(child_list, grp_list):
        cmds.parent(j, g)
    
    
    # 解除したジョイントをグループ化
    cmds.group(grp_list, n='grp_sec_joint')




def set_grp(child_list, parent_list):
    
    # 親ジョイントの代わりのグループを作成
    pj_tr = []
    pj_ro = []
    pj_sc = []
    
    global grp_list
    grp_list = []
    
    for j in child_list:
        grp_list.append(cmds.group(em=True, n='g'+j))
    
    
    # グループにグローバル値をコピー
    for j in parent_list:            
        pj_tr.append(cmds.xform(j, q=True, t=True, ws=True))
        pj_ro.append(cmds.xform(j, q=True, ro=True, ws=True))
        pj_sc.append(cmds.xform(j, q=True, s=True, ws=True))
    
             
    for g, i in zip(grp_list, pj_tr):
        cmds.xform(g, t=i, ws=True)
        
    for g, i in zip(grp_list, pj_ro):
        cmds.xform(g, ro=i, ws=True) 
        
    for g, i in zip(grp_list, pj_sc):
        cmds.xform(g, s=i, ws=True) 

    
    id_node = cmds.listRelatives('null', parent=True, path=True)
    id = id_node[0]
    
    
    if 'pl' in id or 'np' in id :
        disconnect_joint_exe(child_list, parent_list, grp_list)
    
    else:
        disconnect_joint_other_exe(child_list, parent_list, grp_list)





# 再接続
def connect_joint(*args):
    
    global grp_list
    global result_path
    print(result_path)
        
    setting_dict = importJson(result_path)
    
    child_list = setting_dict["child_list"]
    parent_list = setting_dict["parent_list"]
    
    
    # グループとのペアレントを解除
    for j in child_list:
        cmds.parent(j, w=True)
        
    for g in grp_list:
        cmds.delete(g)
    
    cmds.delete('grp_sec_joint')
    
    for cj, pj in zip(child_list, parent_list):    
        cmds.parent(cj, pj)
        




#　Help
def show_toolHelp(*args):
    toolHelp_url = r'https://wisdom.cygames.jp/x/aE4BGw'
    webbrowser.open_new_tab(toolHelp_url)   



