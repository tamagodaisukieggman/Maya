# -*- coding: utf-8 -*-
from maya import cmds

ALLSET_NAME = "AllSet"
CTRLSET_NAME = "CtrlSet"
ANIMJTSET_NAME = "AnimJtSet"


def get_set_members(_set):
    _sets = []
    if cmds.nodeType(_set) == "objectSet":
        _members = cmds.sets(_set, q=True)
        for _member in _members:
            res = get_set_members(_member)
            _sets.extend(res)
    else:
        _sets.append(_set)
    return _sets


def set_name_check(ANIMJTSET_NAME, set_node):
    types = []
    texts = []
    error_nodes = []

    _flag = False
    if ANIMJTSET_NAME.lower() in set_node.lower():
        _flag = True
        if ANIMJTSET_NAME != set_node:
            types.append("{}".format(ANIMJTSET_NAME))
            texts.append(u"[ {} ] の名前が違う".format(ANIMJTSET_NAME))
            error_nodes.append(set_node)
    
    if not _flag:
        types.append("{}".format(ANIMJTSET_NAME))
        texts.append(u"[ {} ] がない".format(ANIMJTSET_NAME))
        error_nodes.append("")
    
    return types, texts, error_nodes



def main(scene_path):
    
    types = []
    texts = []
    error_nodes = []

    all_set_flag = False
    ctrl_set_flag = False
    anim_jnt_set_flag = False

    _sets = cmds.ls(type="objectSet")

    _all_set = None
    _ctrl_set = None
    _anim_jnt_set = None
    
    if not _sets:
        types.append("{}".format("objectSet"))
        texts.append(u"[ objectSet ] がない")
        error_nodes.append("")
    
    else:
        for _set in _sets:
            if ALLSET_NAME.lower() in _set.lower():
                all_set_flag = True
                if ALLSET_NAME != _set:
                    types.append("{} {}".format(ALLSET_NAME, "name"))
                    texts.append(u"[ {} ] の名前が違う".format(ALLSET_NAME))
                    error_nodes.append(_set)
                else:
                    _all_set = _set
                if _all_set:
                    break
        
        if _all_set:
            _set_members = cmds.sets(_all_set, q=True)

            if not _set_members:
                types.append("{} {}".format(ALLSET_NAME, "empty"))
                texts.append(u"[ {} ] に何もない".format(ALLSET_NAME))
                error_nodes.append("")
            
            else:
                for _set_member in _set_members:

                    if _set_member.lower() in CTRLSET_NAME.lower():
                        ctrl_set_flag = True
                        if _set_member != CTRLSET_NAME:
                            types.append("{} {}".format(CTRLSET_NAME, "name"))
                            texts.append(u"[ {} ] の名前が違う".format(CTRLSET_NAME))
                            error_nodes.append(_set_member)
            
                    if _set_member.lower() in ANIMJTSET_NAME.lower():
                        anim_jnt_set_flag = True
                        if _set_member != ANIMJTSET_NAME:
                            types.append("{} {}".format(ANIMJTSET_NAME, "name"))
                            texts.append(u"[ {} ] の名前が違う".format(ANIMJTSET_NAME))
                            error_nodes.append(_set_member)
    
    if not all_set_flag:
        types.append("{}".format(ALLSET_NAME))
        texts.append(u"[ {} ] がない".format(ALLSET_NAME))
        error_nodes.append("None")

        if not ctrl_set_flag:
            types.append("{}".format(CTRLSET_NAME))
            texts.append(u"[ {} ] がない".format(CTRLSET_NAME))
            error_nodes.append("None")
        
        if not anim_jnt_set_flag:
            types.append("{}".format(ANIMJTSET_NAME))
            texts.append(u"[ {} ] がない".format(ANIMJTSET_NAME))
            error_nodes.append("None")

    else:
        if not ctrl_set_flag:
            types.append("{}".format(CTRLSET_NAME))
            texts.append(u"[ {} ] が [ {} ] にない".format(CTRLSET_NAME, ALLSET_NAME))
            error_nodes.append(CTRLSET_NAME)
        
        if not anim_jnt_set_flag:
            types.append("{}".format(ANIMJTSET_NAME))
            texts.append(u"[ {} ] が [ {} ] にない".format(ANIMJTSET_NAME, ALLSET_NAME))
            error_nodes.append(ANIMJTSET_NAME)

    # print(" ----------------------check_all_set")
    return zip(texts, types, error_nodes)