# -*- coding: utf-8 -*-

import enum
import re
from maya import cmds
import pymel.core as pm
from cypyapiutils import pyside as psutils


class ParamType(enum.Enum):
    Boolean = 1,
    Int = 2,
    Float = 3,
    String = 4,
    Enum = 5,


def attrname_from_label(label):
    return 'postproc_edit_set__operator_params__' + re.sub(r'\W', '_', label)

def attrname_from_base(base):
    return 'postproc_edit_set__operator_params__' + base

def get_operator_from_set(op_setname):
    attrname = 'postproc_edit_set__operator_name'
    if not cmds.attributeQuery(attrname, ex=True, n=op_setname):
        return None
    opname = cmds.getAttr(op_setname+'.'+attrname)
    try:
        idx = [x().name() for x in list(operators.values())].index(opname)
    except:
        return None
    op = list(operators.values())[idx]()
    return op


def validate_operator_set(op_set, opname=None, op_label=None):
    if opname is None:
        if op_label is None:
            raise Exception('Both opname and op_label are None.')
        idx = [x().label() for x in list(operators.values())].index(op_label)
    else:
        idx = [x().name() for x in list(operators.values())].index(opname)

    op = list(operators.values())[idx]()
    attrname = 'postproc_edit_set__operator_name'
    if not pm.attributeQuery(attrname, ex=True, n=op_set):
        pm.addAttr(op_set, ln=attrname, dt='string')
        pm.setAttr(op_set+'.'+attrname, op.name())
        pm.setAttr(op_set+'.'+attrname, l=True)

    for pname_, type_, _, dv in op.params():
        pname = attrname_from_base(pname_)
        if pm.attributeQuery(pname, ex=True, n=op_set):
            continue
        
        if type_ == ParamType.String:
            cmds.addAttr(op_set.name(), ln=pname, dt='string')
            cmds.setAttr(op_set.name()+'.'+pname, dv, type='string')
        elif type_ == ParamType.Boolean:
            cmds.addAttr(op_set.name(), ln=pname, at='bool')
            cmds.setAttr(op_set.name()+'.'+pname, dv)
        elif type_ == ParamType.Float:
            cmds.addAttr(op_set.name(), ln=pname, at='double')
            cmds.setAttr(op_set.name()+'.'+pname, dv)
        elif type_ == ParamType.Enum:
            cmds.addAttr(op_set.name(), ln=pname, at='enum', en=':'.join(dv))
            cmds.setAttr(op_set.name()+'.'+pname, e=True, keyable=True)
        elif type_ == ParamType.Int:
            cmds.addAttr(op_set.name(), ln=pname, at='long')
            cmds.setAttr(op_set.name()+'.'+pname, dv)
            

        cmds.setAttr(op_set.name() + '.'+pname, e=True, keyable=True)


class Operator():
    def __init__(self, setname=None):
        self.setname = setname

        try:
            ms = cmds.sets(setname, q=True)
        except:
            ms = None

        if ms is None:
            ms = []
            
        #targets = [x for x in ms if cmds.objectType(x) != 'objectSet']
        targets = self.expand_set(ms)

        self.pmobjs = [pm.PyNode(x) for x in targets]

    def expand_set(self, x):
        res = []
        if type(x) is list:
            for n in x:
                res += self.expand_set(n)
        else:
            if cmds.objectType(x) == 'objectSet':
                if cmds.attributeQuery('postproc_edit_set__operator_name', ex=True, n=x):
                    buf = cmds.sets(x, q=True)
                    if buf is not None:
                        for n in buf:
                            res += self.expand_set(n)
                else:
                    res.append(x)
            else:
                res.append(x)

        return res

    def name(self):
        raise Exception('Override name() in derived class.')

    def label(self):
        raise Exception('Override label() in derived class.')

    def params(self):
        return [] 

    def execute(self, args):
        raise Exception('Override execute() in derived class.')

    def get_param_value(self, index, get_attr_args={}):
        try:
            _pname, ptype, _, dv = self.params()[index]
            pname = attrname_from_base(_pname)

            if not cmds.attributeQuery(pname, n=self.setname, ex=True):
                print('attribute doesnt exist: ', pname)
                if ptype == ParamType.Enum:
                    res = dv[0]
                else:
                    res = dv
                
                return res

            v = cmds.getAttr(self.setname+'.'+pname, **get_attr_args)
            if ptype == ParamType.String:
                v = self.solve_string_param_value(v)
            
            return v
                    
        except Exception as e:
            print(e)
            return None

    def solve_string_param_value(self, value):
        expr1 = re.compile('<([^<>]*)>')
        m = expr1.search(value)
        if not m:
            return value
        
        v1 = m.group(1)

        m = re.search('([^;]*);([^;]*);([^;]*)', v1)

        if m:
            org = m.group(1)
            expr = m.group(2)
            rep = m.group(3)
        else:
            org = v1
            expr = None

        solved1 = org
        if re.match(r'\d+', org):
            try:
                idx = int(org)-1
                solved1 = self.pmobjs[idx].nodeName()
            except:
                pass

        if expr is None:
            value = expr1.sub(solved1, value, 1)
            return self.solve_string_param_value(value)

        else:
            solved2 = re.sub(expr, rep, solved1)
            value = expr1.sub(solved2, value, 1)
            return self.solve_string_param_value(value)

    def order(self):
        return 1

class OperatorDelete(Operator):
    def name(self):
        return 'delete'

    def label(self):
        return 'Delete'

    def params(self):
        return [
            ('skip_in_test', ParamType.Boolean, 'Skip in test', True),
        ]

    def execute(self, args):
        if 'dryrun' in args and args['dryrun']:
            if self.get_param_value(0):
                return

        for pmobj in self.pmobjs:
            pm.delete(pmobj)

    def order(self):
        return 10

class OperatorUngroup(Operator):
    def name(self):
        return 'ungroup'

    def label(self):
        return 'Ungroup'

    def execute(self, args):
        for pmobj in self.pmobjs:
            pm.ungroup(pmobj)
            
    def order(self):
        return 9

class OperatorCombine(Operator):
    def name(self):
        return 'combine_mesh'

    def label(self):
        return 'Combine Mesh'

    def params(self):
        return [
            ('combined_mesh_name', ParamType.String, 'Mesh Name', '<1>'),
            ('Unparent', ParamType.Boolean, 'Unparent', True),
            ('history_in_test', ParamType.Boolean, 'Keep history in test', True),
            ('pivot_position', ParamType.Enum, 'Pivot position', ['Center', 'Last object', 'World origin']),
        ]

    def execute(self, args):
        if len(self.pmobjs) == 0:
            return

        cname = self.get_param_value(0)
        for n in self.pmobjs:
            if n.nodeName() == cname:
                i = 1
                while True:
                    _name = n.nodeName() + '%d' % i
                    if cmds.objExists(_name):
                        i += 1
                    else:
                        break
                cmds.rename(n.name(), _name)

        buf = pm.listRelatives(self.pmobjs[0], p=True, pa=True)
        if buf is not None and len(buf) > 0:
            pr = buf[0]
        else:
            pr = None

        ch = True if 'dryrun' in args and args['dryrun'] and self.get_param_value(2) else False
        
        args = {}
        pivot = self.get_param_value(3)
        if pivot == 0:
            args['centerPivot'] = True
        elif pivot == 1:
            args['objectPivot'] = True

        res = pm.polyUnite(self.pmobjs, ch=ch, mergeUVSets=1, name=cname, **args)
        
        if len(res) > 0:
            cmds.sets(res, e=True, forceElement=self.setname)



        if not self.get_param_value(1):
            if pr is not None:
                pm.parent(res, pr)

        return res

class OperatorMergeVertex(Operator):
    def name(self):
        return 'merge_vertex'

    def label(self):
        return 'Merge Vertex'

    def execute(self, args):
        am = self.get_param_value(0)
        th = self.get_param_value(1)
        
        print('th: ', th)
        print('am: ', am)
        cmds.polyMergeVertex(self.pmobjs, d=th, am=am, ch=False)

    def params(self):
        return [
            ('always_merge', ParamType.Boolean, 'Always Merge', True),
            ('threshold', ParamType.Float, 'Threshold', 0.01),
        ]

    def order(self):
        return 9

class OperatorPublishSplitMotion(Operator):
    def name(self):
        return 'publish_split_motion'

    def label(self):
        return 'Publish Split Motion'

    def execute(self, args):
        #if 'dryrun' in args and args['dryrun']:
        #    return

        from workfile_manager import cmds as wcmds
        from workfile_manager import postproc_utils
        from cylibassetdbutils import assetdbutils
        from workfile_manager_maya import assetutils_maya
        from workfile_manager import p4utils
        db = assetdbutils.DB.get_instance()
        p4u = p4utils.P4Utils.get_instance()

        #dccutils = args['dccutils']
        dccutils = assetutils_maya.MayaUtils.get_instance()

        share_asset_dict = None

        if 'source_file_info' in args:
            #filename = args['source_file']
            print('source_file_info: ', args['source_file_info'])
            workfile = args['source_file_info']['local_master_path']
            work_version = args['source_file_info']['version']

            share_asset_dict = args['assetdict']
            tags = args['tags']

        else:
            workfile = dccutils.current_scenefilename()
            refs = dccutils.getrefs()
            files = [workfile] + refs
            wfile = p4u.get_workfile_as_source(files)
            if len(wfile) == 0:
                d = psutils.PromptDialog2('Error', btns=['OK'])
                d.setStyleSheet('QLabel {font-size:14px}')
                d.show(m=u'ワークファイルが特定出来ません。\n\n一度ワークファイルを保存して再度試してください。')
                return
            workfile = wfile[0]['local_master_path']
            work_version = wfile[0]['version']


        if share_asset_dict is None:
            buf = db.get_workasset_versions(filename=workfile, version=work_version, ignore_path_template=True)
            if len(buf) == 0:
                d = psutils.PromptDialog2('Error', btns=['OK'])
                d.setStyleSheet('QLabel {font-size:18px}')
                d.show(m=u'対応するアセットが見つかりません。')
                return

            print('get_workasset_versions: ', buf)
            buf = sorted(buf, key=lambda x:x['update_date'])

            asset_dict = buf[-1]
            asset = dccutils.create_work_asset({})
            for k in asset.get_dict():
                if k in asset_dict:
                    setattr(asset, k, asset_dict[k])
                

            print('asset: ', asset.get_dict())
            tags_org = db.get_assigned_tags(asset)
            tags = [(x['tag_type'], x['name']) for x in tags_org]
            print('tags: ', tags)
            share_asset_dict = asset.get_dict()


        #
        share_asset = dccutils.create_share_anim_asset({})
        for k in share_asset.get_dict():
            if k in share_asset_dict:
                if k == 'path_template':
                    continue
                if k == 'version':
                    continue
                setattr(share_asset, k, share_asset_dict[k])
        variant = self.get_param_value(3, get_attr_args={'asString':True})            
        share_asset.variant = variant
        leafname = self.get_param_value(4)
        leafname = re.sub('\W', '-', leafname)
        
        if leafname.strip() != '':
            share_asset.leafname = leafname
        
            
        #
        split_name = self.get_param_value(0, get_attr_args={'asString':True})
        tag_types = [x[0] for x in tags]
        if 'anim-split' in tag_types:
            idx = tag_types.index('anim-split')
            tags[idx] = (tags[idx][0], split_name)
        else:
            tags.append(('anim-split', split_name))
        
        print('post_tags: ', tags)


        share_asset.set_path_template(tags=tags)
        print('path_template: ', share_asset.path_template)
        
        workfile_dict = {'local_master_path':workfile, 'version':work_version}

        
        
        cmds.select(self.pmobjs, ne=True)

        # preproc
        #wcmds.preproc(args, silent=True)

        #
        cmds.select(cmds.ls(dag=True), add=True)

        if 'postproc' not in args:
            
            from workfile_manager_maya import ui_maya
            from workfile_manager.plugin_utils import PluginType
            mwin = ui_maya.MainWindow(toolgroup='Default', toolname='workfile_manager')
            args['postproc'] = postproc_utils.get_postprocs(share_asset, mwin, only_enabled=True,
                                plugin_type=PluginType.PublishPostProcess, includes=['postproc_publish_parts'])
            #commitprocs = postproc_utils.get_postprocs(share_asset, mwin, only_enabled=True,
            #                    plugin_type=PluginType.CommitProcess)
        else:
            print('operator >>>>>>>>>>>>>>>>>>>>>>>>> ', args['postproc'])


        _args = {
            'export_all': False, 
            'export_only': False,
            'submit_server': True,
            'postproc': args['postproc'],
            'preproc': [],
            'user': p4u.p4.user,
            'keep_intermediate': args['keep_intermediate'] if 'keep_intermediate' in args else False,
            'textures': share_asset._get_textures(),
            'selection': [x.name() for x in self.pmobjs], 
            'frame_range': (self.get_param_value(1), self.get_param_value(2)),
            'frame_rate': share_asset.get_framerate(),
            'comment': args['comment'] if 'comment' in args else 'Published with SplitMotion',
        }

        if 'thumbnail_source' in args:
            _args['thumbnail_source'] = args['thumbnail_source']

        print('operator pmobjs: ', self.pmobjs)
        print('operator selection: ', _args['selection'])


        if 'procs' in args and ('commit_to_engine' not in args or args['commit_to_engine']):
            _args['commit_to_engine'] = True
            _args['procs'] = args['procs']
        else:
            _args['commit_to_engine'] = False


        task = wcmds.PublishTask(share_asset, tags, workfile_dict, _args['comment'], _args)

        res = task.execute(silent=True)
        print('res: ', res)

    def params(self):
        return [
            ('split_tag', ParamType.Enum, 'Split Tag', ['p00', 'p01','p02','p03','p04','p05','p06','p07','p08','p09']),
            ('start_frame', ParamType.Int, 'Start Frame', 1),
            ('end_frame', ParamType.Int, 'End Frame', 60),
            ('variant', ParamType.Enum, 'Variant', ['default', 'rig']),
            ('leafname', ParamType.String, 'Leaf Name', ''),
           
        ]

    def order(self):
        return 9        

def register_operators():
    from collections import OrderedDict

    buf = []
    buf.append(OperatorDelete)
    buf.append(OperatorUngroup)
    buf.append(OperatorCombine)
    buf.append(OperatorMergeVertex)
    buf.append(OperatorPublishSplitMotion)

    res = OrderedDict()
    for n in buf:
        res[n().name()] = n

    return res

operators = register_operators()

