# -*- coding: utf-8 -*-

import os
import re

import apiutils
from apiutils import uiutils
import cypyapiutils
from cypyapiutils import pyside as psutils

from pipelinetools import postproc_set_editor as pse

from pipelinetools.postproc_set_editor import ui_preset

from Qt import QtWidgets, QtGui, QtCore


import pymel.core as pm
from maya import cmds

from pipelinetools.postproc_set_editor import operator
from .operator import ParamType


class PostprocSetEditor(uiutils.OptionWindow):
    def filepath(self):
        return __file__

    def content(self, **args):
        self.sets = []
        fr_args = {'ebg':True, 'backgroundColor':(0.3, 0.3, 0.3), 'bv':False, 'marginWidth':5, 'marginHeight':15}
        self.cur = 0
        varfile = os.path.join(os.path.dirname(__file__), 'config_main.yaml')
        self.var = cypyapiutils.Variable(self.id, toolgroup='Maya', defaultfile=varfile)

        self.mc = args['column']
        pm.setParent(self.mc)
        #rl = pm.rowLayout(nc=3, ct3=['both']*3, co3=[10]*3, rowAttach=[(2, 'top', 0), (3, 'top', 0)])
        self.form = form = pm.formLayout()

        self.fr1 = fr1 = pm.frameLayout(l='Sets:', **fr_args)
        
        form1 = pm.formLayout()
        
        self.tsl = pse.textScrollList(ams=True, w=10)
        
        pm.textScrollList(self.tsl, e=True, sc=pm.Callback(self.select_item, self.tsl))

        rl = pm.rowLayout(nc=3, ct3=['left']*3, co3=[0, 2, 2])
        pm.button('Create', c=pm.Callback(self.add_item))
        pse.icon_button('Delete', 'trash.png', pm.Callback(self.delete_item, self.tsl))
        pse.icon_button('Preset', 'edit_preset.png', pm.Callback(self.save_preset))

        pm.setParent(form1)

        rl2 = pm.rowLayout(nc=2, ct2=['left']*2, co2=[0, 2])
        pse.icon_button('Run', 'play.png', pm.Callback(self.dryrun))
        pse.icon_button('Reload', 'reload.png', pm.Callback(self.reload_set), style='iconAndTextHorizontal')

        pm.formLayout(form1, e=True,
                ac=[
                    (rl, 'bottom', 10, rl2), 
                    (self.tsl, 'bottom', 10, rl),
                    ],
                af=[
                    (self.tsl, 'top', 0),
                    (self.tsl, 'right', 0), 
                    (self.tsl, 'left', 0), 
                    
                    (rl2, 'bottom', 0),
                    (rl2, 'left', 0),
                    ],)

        
        pm.setParent(form)
        

        self.fr2 = fr2 = pm.frameLayout(l='Linked objects:', **fr_args)
        form2 = pm.formLayout()
        
        self.linked_objs = pse.textScrollList(ams=True, w=10, sc=self.select_linked_objects)
        linked_objs_buttons = pm.rowLayout(nc=2,  ct2=['right']*2, co2=[3]*2)
        pm.button('Add Objects', c=pm.Callback(self.add_linked_objs))
        pse.icon_button('Remove', 'trash.png', pm.Callback(self.remove_linked_objs), style='iconOnly')
        pm.formLayout(form2, e=True, 
                ac=[
                    (self.linked_objs, 'bottom', 10, linked_objs_buttons),
                    ],
                af=[
                    (self.linked_objs, 'top', 0),
                    (self.linked_objs, 'right', 0), 
                    (self.linked_objs, 'left', 0), 
                    (linked_objs_buttons, 'bottom', 0),
                    ]
        )
        
        pm.setParent(form)
        self.fr3 = fr3 = pm.frameLayout(l='Operators:', **fr_args)
        self.form3 = form3 = pm.formLayout()
        
        self.op = pm.optionMenu( label='Name:', cc=pm.Callback(self.refresh_targets))

        for op in list(operator.operators.values()):
            pm.menuItem(label=op().label())
        op_btns = pm.rowLayout(nc=2, ct2=['right']*2, co2=[2]*2)
        pm.button(l='Add Operator', c=pm.Callback(self.add_operator))
        pse.icon_button('Delete', 'trash.png', pm.Callback(self.delete_operator), style='iconOnly')

        pm.setParent('..')
        self.tsl_op = pm.textScrollList(ams=True, w=250, sc=pm.Callback(self.op_selected))
        
        
        self.cl_opprm = pm.columnLayout(adj=True)

        pm.formLayout(form3, e=True, 
                af=[
                    (self.op, 'top', 0),
                    (self.tsl_op, 'left', 0), 
                    (self.tsl_op, 'right', 0), 
                    (self.cl_opprm, 'bottom', 0),
                ],
                ac=[
                    (op_btns, 'top', 10, self.op),
                    (self.tsl_op, 'top', 10, op_btns),
                    (self.tsl_op, 'bottom', 10, self.cl_opprm),
                ]

        )

        pm.setParent(form)
        self.fr4 = fr4 = pm.frameLayout(l='Targets:', **fr_args)
        form4 = pm.formLayout()
        self.tsl_target = pse.textScrollList(ams=True, w=250, sc=self.select_targets)
        
        tgt_btns = pm.rowLayout(nc=2, ct2=['right']*2, co2=[2]*2)
        pm.button('Add Targets', c=pm.Callback(self.add_targets))
        pse.icon_button('Remove', 'trash.png', pm.Callback(self.remove_targets), style='iconOnly')

        pm.formLayout(form4, e=True, 
                af=[
                    (self.tsl_target, 'top', 0),
                    (self.tsl_target, 'left', 0),
                    (self.tsl_target, 'right', 0),
                    (tgt_btns, 'bottom', 0),
                ],
                ac=[
                    (self.tsl_target, 'bottom', 10, tgt_btns),
                ]

        )

        #
        pm.formLayout(form, e=True, 
                                attachPosition=[
                                    (fr1, 'top', 0, 0),
                                    (fr1, 'bottom', 0, 100),
                                    (fr1, 'left', 0, 0),
                                    (fr1, 'right', 0, 25), 

                                    (fr2, 'top', 0, 0),
                                    (fr2, 'bottom', 0, 100),
                                    (fr2, 'left', 10, 25),
                                    (fr2, 'right', 0, 50),

                                    (fr3, 'top', 0, 0),
                                    (fr3, 'bottom', 0, 100),
                                    (fr3, 'left', 10, 50),
                                    #(fr3, 'right', 0, 75),

                                    (fr4, 'top', 0, 0),
                                    (fr4, 'bottom', 0, 100),
                                    #(fr4, 'left', 10, 75),
                                    (fr4, 'right', 0, 100),


                                ],
                                af=[
                                    (fr1, 'bottom', 0),
                                    (fr2, 'bottom', 0),
                                    (fr3, 'bottom', 0),
                                    (fr4, 'bottom', 0),
                                ],

                                ac=[
                                    (fr4, 'left', 10, fr3),
                                ]
                            )

        self.reload_set()
    

        try:
            pm.textScrollList(self.tsl, e=True, sii=1)
            self.select_item(self.tsl)
            self.refresh_linked_objs()
            self.refresh_operators()
            self.refresh_op_parameters()
            self.refresh_targets()
        except:
            pass

        return form
    

    def dryrun(self):
        from workfile_manager_maya.export.postproc.all import postproc_edit_set as ppes

        setobjs = self.get_current_setobjs()
        
        if setobjs is None:
            return

        for setobj in setobjs:
            spc = [setobj.get_setname()]
            pp = ppes.Plugin()
            pp.execute({'plugin_name':'postproc_edit_set', 'specified':spc, 'dryrun':True})

        self.refresh_set()
        self.refresh_linked_objs()
        self.refresh_operators()
        self.refresh_op_parameters()
        self.refresh_targets()

        cmds.dgdirty(a=True)

    def open_preset_window(self):
        w = ui_preset.PresetWindow(pse.PRESET_WINDOW_NAME, w=350, h=460)
        w.set_parent(self)
        w.show()


    def save_preset(self):
        self.open_preset_window()

    def remove_targets(self):
        setobj = self.get_current_setobj()
        if setobj is None:
            return

        try:
            op_setname = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        ms = pm.textScrollList(self.tsl_target, q=True, si=True)
        if ms is None:
            ms = []
        for _ in ms:
            pm.sets(pm.PyNode(op_setname), remove=[pm.PyNode(x) for x in ms])
        
        self.refresh_targets()

    def delete_tsl_item(self, tsl, delcmd):
        buf = pm.textScrollList(tsl, q=True, allItems=True)
        selected = pm.textScrollList(tsl, q=True, si=True)
        to_sel = None

        for opname in selected:
            if len(buf) > 1:
                try:
                    to_sel = buf[buf.index(opname)+1]
                except:
                    buf.remove(opname)
                    to_sel = buf[-1]

            #cmds.delete(opname)
            delcmd(opname)

        return to_sel

    def delete_operator(self):
        to_sel = self.delete_tsl_item(self.tsl_op, lambda x:cmds.delete(x))

        self.refresh_operators()

        if to_sel is not None:
            pm.textScrollList(self.tsl_op, e=True, da=True)
            pm.textScrollList(self.tsl_op, e=True, si=to_sel)

        self.refresh_op_parameters()
        self.refresh_targets()

    def add_operator(self, opname=None, op_setname=None):
        cmds.select(cmds.ls(sl=True, type='objectSet'), ne=True, d=True)

        setobj = self.get_current_setobj()
        if setobj is None:
            return
        if not pm.objExists(setobj.pm_set):
            return
        
        op_label = pm.optionMenu(self.op, q=True, value=True)

        i = 1
        while True:
            if op_setname is None or i > 1:
                op_setname = 'plset%02d_%s' % (i, op_label.lower() if opname is None else opname)

            if not cmds.objExists(op_setname):
                break
            i += 1

        op_set = pm.sets(name=op_setname)
        operator.validate_operator_set(op_set, opname, op_label)
        
        pm.sets(setobj.pm_set, add=op_set)

        self.refresh_operators()
        pm.textScrollList(self.tsl_op, e=True, da=True)
        pm.textScrollList(self.tsl_op, e=True, si=op_set.name())
        
        self.refresh_op_parameters()
        self.refresh_targets()

        return op_set

    def add_targets(self):
        sel = cmds.ls(sl=True)
        if len(sel) == 0:
            return

        setobj = self.get_current_setobj()
        if setobj is None:
            return
        if not pm.objExists(setobj.pm_set):
            return
        
        ms = cmds.sets(setobj.pm_set.name(), q=True)
        if ms is None:
            ms = []

        try:
            op_setname = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        pm.sets(pm.PyNode(op_setname), add=sel)
        
        self.refresh_targets()

    def select_targets(self):
        cmds.select(cl=True)
        ms = pm.textScrollList(self.tsl_target, q=True, si=True)
        if ms is None:
            ms = []
        for item in ms:
            cmds.select(item, add=True)

    def remove_linked_objs(self):
        setobj = self.get_current_setobj()
        if setobj is None:
            return

        ms = pm.textScrollList(self.linked_objs, q=True, si=True)
        if ms is None:
            ms = []

        for item in ms:
            if cmds.objExists(item):
                pm.sets(setobj.pm_link_set, remove=item)
                setobj.pm_nodes.remove(pm.PyNode(item))

        self.refresh_linked_objs()
        self.refresh_operators()
        self.refresh_op_parameters()
        self.refresh_targets()

    def select_linked_objects(self):
        cmds.select(cl=True)
        ms = pm.textScrollList(self.linked_objs, q=True, si=True)
        if ms is None:
            ms = []
        for item in ms:
            if cmds.objExists(item):
                cmds.select(item, add=True)

    def get_current_setobj(self):
        try:
            idx = pm.textScrollList(self.tsl, q=True, sii=True)[0]-1
        except:
            pm.textScrollList(self.tsl_target, e=True, ra=True)
            return None
        
        return self.sets[idx]

    def get_setobj_from_name(self, setname):
        buf = [x for x in self.sets if x.get_setname()==setname]
        if len(buf) == 0:
            return None
        return buf[0]


    def get_current_setobjs(self):
        try:
            ms = pm.textScrollList(self.tsl, q=True, sii=True)
        except:
            #pm.textScrollList(self.tsl_target, e=True, ra=True)
            return None

        return [self.sets[x-1] for x in ms]


    def add_linked_objs(self):
        setobj = self.get_current_setobj()
        
        if setobj is None:
            return
        if not pm.objExists(setobj.pm_set):
            return
        
        if not pm.objExists(setobj.pm_link_set):
            return
        
        pm.sets(setobj.pm_link_set, add=pm.ls(sl=True))

        setobj.pm_nodes = pm.sets(setobj.pm_link_set, q=True)

        self.refresh_linked_objs()
        self.refresh_operators()
        self.refresh_op_parameters()
        self.refresh_targets()

    def refresh_operators(self):
        pm.textScrollList(self.tsl_op, e=True, ra=True)
        setobj = self.get_current_setobj()
        if setobj is None:
            return

        ops = setobj.get_operators()

        for op in ops:
            pm.textScrollList(self.tsl_op, e=True, a=op)

        if len(ops) > 0:
            pm.textScrollList(self.tsl_op, e=True, sii=1)

        self.refresh_op_parameters()

    def op_selected(self):
        self.refresh_op_parameters()
        self.refresh_targets()

    def refresh_op_parameters(self):
        clds = pm.columnLayout(self.cl_opprm, q=True, ca=True)
        if clds is not None:
            for c in clds:
                cmds.deleteUI(c)

        si = pm.textScrollList(self.tsl_op, q=True, si=True)
        try:
            set_ = pm.ls(si, type='objectSet')[0]
        except:
            return
        
        try:
            opname = cmds.getAttr(set_.name()+'.postproc_edit_set__operator_name')
        except:
            return
        
        if opname not in operator.operators:
            return

        operator.validate_operator_set(set_, opname)

        params = operator.operators[opname]().params()
        if len(params) > 0:
            for pname_, ptype, label, dv in params:
                pname = operator.attrname_from_base(pname_)
                pm.setParent(self.cl_opprm)
                value = cmds.getAttr(set_.name()+'.'+pname)

                if ptype == operator.ParamType.String:
                    pm.rowLayout(nc=3, co3=(2, 2, 2), ct3=('left', 'left', 'left'))
                    pm.text(l=label+':')
                    tf = pm.textField(w=170, tx=value)
                    pm.textField(tf, e=True, cc=pm.Callback(self.string_param_changed, tf, pname))
                    
                    pse.icon_button('', 'help.png', pm.Callback(self.show_text_param_help), style='iconOnly')
                elif ptype == operator.ParamType.Boolean:
                    cb = pm.checkBoxGrp(ncb=1, l=label+':', v1=value, adj=2, cal=(1, 'left'))
                    pm.checkBoxGrp(cb, e=True, cc=pm.Callback(self.boolean_param_changed, cb, pname))

                elif ptype == operator.ParamType.Float:
                    ffg = pm.floatFieldGrp(pre=5, nf=1, l=label+':', v1=value, adj=2, cal=(1, 'left'))
                    pm.floatFieldGrp(ffg, e=True, cc=pm.Callback(self.float_param_changed, ffg, pname))

                elif ptype == operator.ParamType.Int:
                    ifg = pm.intFieldGrp(nf=1, l=label+':', v1=value, adj=2, cal=(1, 'left'))
                    pm.intFieldGrp(ifg, e=True, cc=pm.Callback(self.int_param_changed, ifg, pname))

                elif ptype == operator.ParamType.Enum:
                    om = pm.optionMenu(l=label+':')
                    for mi in dv:
                        pm.menuItem(l=mi)
                        
                    pm.optionMenu(om, e=True, sl=value+1, cc=pm.Callback(self.enum_param_changed, om, pname))
                    


    def show_text_param_help(self):
        m = '<1>, <2>, <3>, ..., <N>：      N番目のターゲット名\n' + \
            '<1;expr;rep_str>：                 <1>の値の正規表現exprでマッチする個所をrep_strで置換したもの'

        w = QtWidgets.QVBoxLayout()
        w.addWidget(QtWidgets.QLabel(m))
        w.addWidget(QtWidgets.QWidget(), 1)

        d = psutils.PromptDialog2('Info', btns=['OK'])
        d.setStyleSheet('QLabel {font-size:18px}')
        d.show(aw=w, m=u'【使用可能な書式】\n')

    def string_param_changed(self, tf, pname):
        try:
            op_set = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        value = cmds.textField(tf, q=True, tx=True)
        cmds.setAttr(op_set+'.'+pname, value, type='string')
        
    def boolean_param_changed(self, cb, pname):
        try:
            op_set = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        value = cmds.checkBoxGrp(cb, q=True, v1=True)
        cmds.setAttr(op_set+'.'+pname, value)

    def float_param_changed(self, ffg, pname):
        try:
            op_set = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        value = cmds.floatFieldGrp(ffg, q=True, v1=True)
        cmds.setAttr(op_set+'.'+pname, value)

    def int_param_changed(self, ifg, pname):
        try:
            op_set = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        value = cmds.intFieldGrp(ifg, q=True, v1=True)
        cmds.setAttr(op_set+'.'+pname, value)

    def enum_param_changed(self, om, pname):
        try:
            op_set = cmds.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return
        value = cmds.optionMenu(om, q=True, sl=True)
        cmds.setAttr(op_set+'.'+pname, value-1)
        

    def refresh_targets(self):
        pm.textScrollList(self.tsl_target, e=True, ra=True)

        setobj = self.get_current_setobj()
        if setobj is None:
            return

        try:
            op_setname = pm.textScrollList(self.tsl_op, q=True, si=True)[0]
        except:
            return

        tgs = setobj.get_targets(op_setname)
        
        for tg in tgs:
            pm.textScrollList(self.tsl_target, e=True, a=tg)
        
    def delete_item(self, tsl):
        for item in pm.textScrollList(tsl, q=True, si=True):
            set_ = self.get_setobj_from_name(item)
            pse.clear_set(set_.pm_set.name())
        self.reload_set()

    def get_setobj(self, setname):
        try:
            buf = [cmds.getAttr(x.pm_set+'.'+pse.SETNAME_ATTR) for x in self.sets]
            
            i = buf.index(setname)
            set_ = self.sets[i]
            return set_
        except:
            return None

    def select_item(self, tsl):
        cmds.select(cl=True)

        try:
            setname = pm.textScrollList(tsl, q=True, si=True)[0]
        except:
            setname = None

        setobj = self.get_setobj(setname)
        if setobj is not None:
            pm.select([x for x in setobj.pm_nodes if pm.objExists(x)])

        self.refresh_linked_objs()
        self.refresh_operators()
        self.refresh_op_parameters()
        self.refresh_targets()
        
        

    def refresh_linked_objs(self):
        pm.textScrollList(self.linked_objs, e=True, ra=True)
        try:
            item = pm.textScrollList(self.tsl, q=True, si=True)[0]
        except:
            return

        setobj = self.get_setobj(item)

        if setobj is None:
            return

        for x in [x.name() for x in setobj.pm_nodes]:
            pm.textScrollList(self.linked_objs, e=True, a=x)

    def add_item(self):
        d = pse.InputSetName(pse.INPUT_NAME_WINDOW)
        
        d._prostproc_set_editor_mwin = self
        d.show()
        pm.window(d.win, e=True, w=600)

    def _add_item(self, base_set_name):
        if not pse.is_unique(base_set_name):
            return
        self._add_item2(base_set_name)

    def _add_item2(self, base_set_name):
        sel = pm.ls(sl=True)
        set_ = pse.Set(sel, set_name=base_set_name, new=True)
        self.sets.append(set_)
        self.refresh_set()
        pm.textScrollList(self.tsl, e=True, da=True)
        pm.textScrollList(self.tsl, e=True, si=set_.get_setname())
        self.refresh_linked_objs()
        self.refresh_operators()
        self.refresh_op_parameters()
        self.refresh_targets()

        return set_
        

    def reload_set(self):
        cmds.dgdirty(a=True)

        self.sets = []
        for set_ in [x for x in cmds.ls(type='objectSet') if cmds.attributeQuery('postproc_edit_set', n=x, ex=True)]:
            try:
                ms = cmds.sets(set_, q=True)
                if ms is None:
                    ms = []
                tgset = [x for x in ms if cmds.objectType(x) == 'objectSet' and re.search(r'^plset\d{2}_target', x)][0]

            except:
                tgset = None

            if pse.is_root_set(set_):
                set_obj = pse.Set(set_name=set_)
                try:
                    ms = pm.sets(tgset, q=True)
                except:
                    ms = None

                if ms is None:
                    ms = []
                set_obj.pm_nodes = ms
                self.sets.append(set_obj)
        
        self.refresh_set()


    def refresh_set(self):
        cmds.textScrollList(self.tsl, e=True, removeAll=True)

        self.sets = [x for x in self.sets if x.get_setname() is not None]
        for n in self.sets:
            cmds.textScrollList(self.tsl, e=True, a=n.get_setname())

        if len(self.sets) > 0:
            cmds.textScrollList(self.tsl, e=True, sii=1)

        self.refresh_linked_objs()
        self.refresh_operators()
        self.refresh_op_parameters()
        self.refresh_targets()
        
    
    def execute(self):
        return

    def apply_button_label(self):
        return 'Apply'

    def reset_optvar(self):
        #toolopt = apiutils.ToolOpt(self.id)
        pass
        
    def is_editmenu_enabled(self):
        return False

def show():
    w = PostprocSetEditor('Post-process Set Editor', w=700, h=580)
    w.show()