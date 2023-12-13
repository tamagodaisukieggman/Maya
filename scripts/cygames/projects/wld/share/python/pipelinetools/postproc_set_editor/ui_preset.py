# -*- coding: utf-8 -*-

import os
import re
import yaml
import copy

import apiutils
from apiutils import uiutils
import cypyapiutils
from cypyapiutils import pyside as psutils

import pipelinetools.postproc_set_editor as pse

from Qt import QtWidgets, QtGui, QtCore


import pymel.core as pm
from maya import cmds

from pipelinetools.postproc_set_editor import operator
from .operator import ParamType
    

RECENT_PRESET_KEY = 'RecentLoadedPresetFile'

class PresetWindowBase(uiutils.OptionWindow):
    def filepath(self):
        return __file__

    def content(self, **args):
        self.sets = []

        self.cur = 0
        varfile = os.path.join(os.path.dirname(__file__), 'config_preset.yaml')
        self.var = cypyapiutils.Variable(self.id, toolgroup='Maya', defaultfile=varfile)

        self.mc = args['column']
        pm.setParent(self.mc)

        c1 = pm.formLayout()
        
        l1 = pm.text('Presets:')
        self.tsl = pse.textScrollList(sc=pm.Callback(self.select_item), ams=True)
        self.tfg = pm.textFieldGrp(l='New preset name: ', cw2=(120, 200))

        r1 = pm.rowLayout(nc=2, ct2=['left', 'left'], co2=[2, 2])
        pse.icon_button('Save Preset', 'save.png', pm.Callback(self.save_preset))
        pse.icon_button('Delete', 'trash.png', pm.Callback(self.delete_item), style='iconOnly')

        pm.formLayout(c1, e=True, af=[
                (l1, 'top', 0),
                (r1, 'bottom', 0),
                (self.tsl, 'left', 0),
                (self.tsl, 'right', 0),
            ],
            ac=[
                (self.tsl, 'top', 0, l1),
                (self.tsl, 'bottom', 10, self.tfg),
                (self.tfg, 'bottom', 20, r1),
            ],
        )

        pm.menuItem(divider=True, parent=self.edit_menu)
        pm.menuItem(l='Load Presets...', c=pm.Callback(self.load_presets), parent=self.edit_menu)
        self.recent_presets = pm.menuItem(l='Load Recent Presets', pmc=pm.Callback(self.refresh_recent_presets), parent=self.edit_menu, subMenu=True)
        self.recent_presets.children = []
        pm.menuItem(divider=True, parent=self.edit_menu)
        pm.menuItem(l='Save to Preset File...', c=pm.Callback(self.save_presets), parent=self.edit_menu)


        self.refresh_list()

        try:
            pm.textScrollList(self.tsl, e=True, sii=1)
            self.select_item()
        except:
            pass


        return c1

    def _first_recent_preset(self):
        dir_ = None
        try:
            dir_ = self.var.var[RECENT_PRESET_KEY][0]
        except:
            pass
        return dir_

    def save_presets(self):
        preset_file, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save Presets', self._first_recent_preset(), '*.yaml', None)
        if preset_file == '':
            return
        with open(preset_file, mode='w') as hdl:
            output = {'presets':self.var.var['presets']}
            hdl.write(yaml.safe_dump(output, encoding='utf-8', allow_unicode=True, default_flow_style=False))

    def refresh_recent_presets(self):
        for c in self.recent_presets.children:
            cmds.deleteUI(c)

        if RECENT_PRESET_KEY not in self.var.var:
            return

        presets = self.var.var[RECENT_PRESET_KEY]

        self.recent_presets.children = []

        for p in presets:
            item = pm.menuItem(l=p, parent=self.recent_presets, c=pm.Callback(self.load_presets, p))
            self.recent_presets.children.append(item)

    def load_presets(self, presets_file=None):
        
        if presets_file is None:
            presets_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Load Presets', self._first_recent_preset(), '*.yaml', None)
        
        if not os.path.exists(presets_file):
            return

        if pm.textScrollList(self.tsl, q=True, ni=True) > 0:
            d = psutils.PromptDialog2('Confirmation')
            d.setStyleSheet('QWidget {font-size:16px}')
            res = d.show(m=u'プリセットファイルをロードしますか？\n\n※リスト内のプリセットは全て失われます。\n')
            if res != 1:
                return
        
        with open(presets_file, 'r') as fhd:
            try:
                self.var.var['presets'] = copy.deepcopy(yaml.load(fhd)['presets'])
            except:
                fhd.close()
                return
            else:
                if RECENT_PRESET_KEY not in self.var.var:
                    self.var.var[RECENT_PRESET_KEY] = []
                if presets_file in self.var.var[RECENT_PRESET_KEY]:
                    self.var.var[RECENT_PRESET_KEY].remove(presets_file)
                self.var.var[RECENT_PRESET_KEY].insert(0, presets_file)
                self.var.save()

                self.refresh_list()
        

        

    def delete_item(self):
        try:
            ms = pm.textScrollList(self.tsl, q=True, si=True)
        except:
            ms = None
        if ms is None:
            ms = []

        if ms == []:
            return

        d = psutils.PromptDialog2('Confirmation')
        d.setStyleSheet('QWidget {font-size:16px}')
        res = d.show(u'下のプリセットを削除してよろしいですか？\n\n%s' % '\n'.join(ms))
        if res != 1:
            return

        for item in ms:
            pm.textScrollList(self.tsl, e=True, ri=item)
            self.var.var['presets'].pop(item)

        self.select_item()
        self.var.save()

    def select_item(self):
        try:
            item = pm.textScrollList(self.tsl, q=True, si=True)[0]
        except:
            item = None

        if hasattr(self, 'tfg'):
            if item is not None:
                pm.textFieldGrp(self.tfg, e=True, text=item)

    def refresh_list(self):
        pm.textScrollList(self.tsl, e=True, ra=True)
        try:
            presets =self.var.get('presets') 
            if presets is None:
                return
        except:
            return

        for k in sorted(self.var.get('presets').keys()):
            pm.textScrollList(self.tsl, e=True, a=k)

    def execute(self):
        pass

    def is_desc_enabled(self):
        return False

    def is_editmenu_enabled(self):
        return False


class PresetWindow(PresetWindowBase):
    def apply_button_label(self):
        return 'Create'

    def save_preset(self):
        try:
            presets = self.var.get('presets')
            if presets is None:
                presets = {}
        except:
            presets = {}
         

        tx = cmds.textFieldGrp(self.tfg, q=True, text=True)
        if tx == '':
            return
        
        if tx in presets:
            d = psutils.PromptDialog2('Confirmation')
            d.setStyleSheet('QWidget {font-size:16px}')
            res = d.show(m=u'%s はすでに存在します。上書きしますか？' % tx)
            if res != 1:
                return
        #self.var.replace(tx, {'arg1': 1})
        #self.var.save()
        print('filename: ', self.var.filename())

        setobj = self.parent_window.get_current_setobj()
        if setobj is None:
            return

        dic = {}

        linkedobjs = [x.name() for x in setobj.pm_nodes]
        #self.var.replace(tx, {'linked_objs':linkedobjs})
        dic['linked_objs'] = linkedobjs

        dic_op = []

        for op_setname in cmds.sets(setobj.pm_set.name(), q=True):
            if cmds.objectType(op_setname) != 'objectSet' or \
                not cmds.attributeQuery('postproc_edit_set__operator_name', n=op_setname, ex=True):
                continue

            op_name = cmds.getAttr(op_setname+'.postproc_edit_set__operator_name')

            try:
                idx = [x().name() for x in list(operator.operators.values())].index(op_name)
                op_obj = list(operator.operators.values())[idx]()
            except:
                print('Error: Invalid operator: ', op_name)
                continue

            op = {}
            op['name'] = op_setname
            op['type'] = op_name
            op['targets'] = cmds.sets(op_setname, q=True)
            params = {}
            for pname, ptype, _, _ in op_obj.params():
                attrname = operator.attrname_from_base(pname)
                value = cmds.getAttr(op_setname+'.'+attrname)
                params[pname] = {
                    'type': str(ptype),
                    'value': value
                }

            op['params'] = params

            dic_op.append(op)

        dic['operator'] = dic_op
        presets[tx] = dic

        self.var.replace('presets', presets)

        self.var.save()

        self.refresh_list()

    def set_parent(self, parent):
        self.parent_window = parent

    def select_mult(self, n):
        try:
            if not cmds.objExists(n):
                n = re.sub('.*[|]', '', n)
            
            cmds.select(cmds.ls(n), ne=True, add=True)
        
        except Exception as e:
            print(e)

    def solve_dependency(self, dic_ops):
        def is_targets_in_rest(targets, buf):
            for t in targets:
                if t in buf:
                    return True
            return False

        for _ in range(len(dic_ops)):
            targets = dic_ops[0]['targets']
            i = 0
            while True:
                if (i+1) >= len(dic_ops):
                    break
                if not is_targets_in_rest(targets, [x['name'] for x in dic_ops[i+1:]]):
                    break
                dic_ops[i], dic_ops[i+1] = dic_ops[i+1], dic_ops[i]
                i += 1


    def execute_item(self, preset_name):
        presets = self.var.get('presets')
        linked_objs = presets[preset_name]['linked_objs']
        print('linked_objs: ', linked_objs)
        pm.select(cl=True)

        base_set_name = preset_name

        i = 1
        while True:
            if pse.is_unique(base_set_name, silent=True):
                break
            else:
                base_set_name = re.sub('_\d+$', '', base_set_name) + '_%d' % i
                i += 1
            

        self.parent_window._add_item2(base_set_name)
        
        for n in linked_objs:
            self.select_mult(n)
        self.parent_window.add_linked_objs()
        
        dic_ops = presets[preset_name]['operator']
        try:
            self.solve_dependency(dic_ops)
        except:
            import traceback
            print(traceback.format_exc())

        for _, dic_op in enumerate(dic_ops):
            #opname = dic_op['name']
            optype = dic_op['type']
            
            targets = dic_op['targets']
            cmds.select(cl=True)
            op_set = self.parent_window.add_operator(opname=optype)
            
            idx = [x().name() for x in list(operator.operators.values())].index(optype)
            op = list(operator.operators.values())[idx]()
            for pname, ptype, _, _ in op.params():
                attrname = operator.attrname_from_base(pname)
                try:
                    value = dic_op['params'][pname]['value']
                except:
                    continue
                if ptype == operator.ParamType.Boolean:
                    cmds.setAttr(op_set+'.'+attrname, value)
                elif ptype == operator.ParamType.Int:
                    cmds.setAttr(op_set+'.'+attrname, value)
                elif ptype == operator.ParamType.Float:
                    cmds.setAttr(op_set+'.'+attrname, value)
                elif ptype == operator.ParamType.String:
                    cmds.setAttr(op_set+'.'+attrname, value, type='string')
                elif ptype == operator.ParamType.Enum:
                    cmds.setAttr(op_set+'.'+attrname, value)


            cmds.select(cl=True)
            for t in targets:
                self.select_mult(t)
            
            self.parent_window.add_targets()

        
    def execute(self):
        sel = pm.ls(sl=True)
        try:
            ms = pm.textScrollList(self.tsl, q=True, si=True)
            if ms is None:
                ms = []
            for preset_name in ms:
                self.execute_item(preset_name)
            
        except Exception as e:
            print(e)

        finally:
            if len(sel)>0:
                pm.select(sel)
            else:
                pm.select(cl=True)

        self.parent_window.refresh_op_parameters()

    def is_editmenu_enabled(self):
        return True

    def reset_optvar(self):
        d = psutils.PromptDialog2('Confirmation', btns=['Reset', 'Cancel'])
        res = d.show(m='Reset presets to default?', modal=True)
        if res == 1:
            self.var.load_default()
            self.refresh_list()



