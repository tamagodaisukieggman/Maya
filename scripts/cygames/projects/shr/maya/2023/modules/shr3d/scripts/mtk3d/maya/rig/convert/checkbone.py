# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from collections import OrderedDict
import os
import codecs
import sys
import pdb
import traceback

# pdb.set_trace()
from datetime import datetime

if cmds.pluginInfo('mayaHIK', q=True, l=True) == False:
    cmds.loadPlugin("mayaHIK")
if cmds.pluginInfo('mayaCharacterization', q=True, l=True) == False:
    cmds.loadPlugin("mayaCharacterization")
if cmds.pluginInfo('OneClick', q=True, l=True) == False:
    cmds.loadPlugin("OneClick")
if cmds.pluginInfo('fbxmaya', q=True, l=True) == False:
    cmds.loadPlugin("fbxmaya")
if cmds.pluginInfo('rotationDriver', q=True, l=True) == False:
    cmds.loadPlugin("rotationDriver")
    print('rotationDriver is loaded')

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

logFolder = '{}/log/'.format(dir_path)

class RunBones(object):
    def __init__(self, round_value=None):
        self.src_joints=OrderedDict()
        self.round_value=round_value
        self.results=[]
        self.len_get_joints_list=[]
        self.file_paths=[]
        self.jointValues_buf=[]

        # ply00_999
        self.ply00_999_special=None
        self.ply00_999_ref_imp=[]

    def get_src_joint_values(self, file_path=None, ):
        # 元の骨
        self.src_joints[file_path]=OrderedDict()
        self.get_joints, self.len_get_joints = self.get_current_joints()
        self.joint_values=self.get_current_joint_values(self.get_joints)
        self.src_joints[file_path][self.len_get_joints]=self.joint_values
        self.len_get_joints_list.append(self.len_get_joints)

    def file_open(self, file_path):
        cmds.file(f=1, new=1)
        cmds.file(file_path, f=1, o=1)

    def ply00_999_special_open(self, file_path):
        cmds.file(file_path, buildLoadSettings=True, open=True)
        nsettings = range(cmds.selLoadSettings(ns=1, q=1))
        ids = [str(i) for i in nsettings if i]
        references = cmds.selLoadSettings(ids, fn=1, q=1)
        for i, (ref, ref_id) in enumerate(zip(references, ids)):
            if 'ply00_999' in ref:
                cmds.selLoadSettings(ref_id, e=1, deferReference=0)
                self.ply00_999_ref_imp.append(ref)
            else:
                cmds.selLoadSettings(ref_id, e=1, deferReference=1)

        cmds.file(file_path, o=True, f=1, loadSettings='implicitLoadSettings')

    def get_current_joints(self):
        get_joints = cmds.ls(type='joint')
        get_joints.sort()
        len_get_joints = len(get_joints)

        return get_joints, len_get_joints

    def get_current_joint_values(self, joints):
        joint_values=OrderedDict()
        for obj in joints:
            trans=cmds.xform(obj, q=1, t=1, os=1)
            round_trans=list(map(round, trans, [self.round_value]*len(trans)))
            joint_values[obj]=round_trans

        return joint_values

    def reload_reference(self, refNode='ply00_999_rigRN'):
        if cmds.objExists(refNode):
            cmds.file(loadReferenceDepth="asPrefs", loadReference=refNode)
        else:
            return False

    def run_files(self, fbx_path, save_path, root_jnt, checkjoints, export_fbx, ply00_999_special):
        self.save_path=save_path
        self.ply00_999_special=ply00_999_special
        if not os.path.isdir(logFolder):
            os.makedirs(logFolder)

        error_results=[]

        print(fbx_path)
        print(type(fbx_path))

        listFiles=[]
        folder_or_files = fbx_path.split(' ')
        if folder_or_files == []:
            print('D&D error')
        for fbx_path in folder_or_files:
            if '' == fbx_path:
                print('empty:')
            else:
                if fbx_path.endswith('.ma') or fbx_path.endswith('.mb'):
                    listFiles.append(fbx_path)
                else:
                    for root, dirs, files in os.walk(fbx_path):
                        for fname in files:
                            self.result=[]
                            file_path = os.path.join(root, fname)
                            listFiles.append(file_path)

        print('Files:')
        print('\n'.join(listFiles))
        print('\n')

        for file_path in listFiles:
            self.check_file = file_path.replace('\\', '/')
            if self.check_file.endswith('.ma') or self.check_file.endswith('.mb'):
                # file open
                if self.ply00_999_special == 'True':
                    try:
                        self.ply00_999_special_open(self.check_file)
                    except Exception as e:
                        error_results.append((self.check_file, traceback.print_exc()))
                        self.file_open(self.check_file)
                else:
                    self.file_open(self.check_file)

            elif self.check_file.endswith('.fbx'):
                # file open
                self.file_open(self.check_file)

                self.file_paths.append(self.check_file)

            print('Current scene:{0}'.format(self.check_file))

            try:
                if checkjoints == 'True':
                    self.checkjoints()

                if export_fbx == 'True':
                    print('Start FBX Export')
                    self.func_export_fbx(root_jnt)

            except Exception as e:
                print(traceback.print_exc())
                error_results.append((self.check_file, traceback.print_exc()))

        if error_results: # error_resultがあれば、
            # txt = 'D:/error.csv'
            txt = u'{}/error_{}{:4d}.csv'.format(logFolder, datetime.now().strftime("%Y%m%d_%H%M%S"), datetime.now().microsecond) # 時間は%H%M%S
            # csvで書き出し
            with codecs.open(txt, 'w', 'utf-8') as f:
                for result in error_results:
                    f.write(u'{}, {}\n'.format(result[0], result[1]))

    def checkjoints(self):
        self.get_src_joint_values(file_path=self.check_file)

        values = ['{0},{1},{2},{3}'.format(jnt, value[0], value[1], value[2]) for jnt, value in self.joint_values.items()]
        jointValues = ['{0},{1},{2}'.format(value[0], value[1], value[2]) for jnt, value in self.joint_values.items()]

        self.result.append(('{0}'.format(self.len_get_joints),
                       '{0}\n'.format('\n'.join(values)),
                       '{0}'.format('\n'),
                       '{0}'.format('\n'.join(jointValues))))


        # txt = 'D:/error.csv'
        txt = u'{}checkbone.csv'.format(logFolder)
        # csvで書き出し
        # with open(txt, mode='w') as f:
        jointsTypeFolder='{0}/joints_{1}'.format(txt.split('.')[0], result[0][0])
        if not os.path.isdir(jointsTypeFolder):
            os.makedirs(jointsTypeFolder)

        txt_joints='{0}/{1}.csv'.format(jointsTypeFolder, '{0}'.format(self.check_file.split('/')[-1]))
        with open(txt_joints, mode='w') as f:
            f.write('{0}\n'.format(self.check_file))
            f.write('{0}\n'.format(result[0][1]))
            f.write('{0}\n'.format(result[0][2]))

        if jointValues in self.jointValues_buf:
            txt_joints='{0}/joints_{1}_same_{2}.csv'.format(txt.split('.')[0], result[0][0], self.jointValues_buf.index(jointValues))
            with open(txt_joints, mode='w') as f:
                f.write('{0}\n'.format(self.check_file))
                f.write('{0}\n'.format(result[0][1]))
                f.write('{0}\n'.format(result[0][3]))

        self.jointValues_buf.append(jointValues)


    def importAllReferences(self):
        print("Importing all references...")
        done = False
        while (done == False and (len(pm.listReferences()) != 0)):
            refs = pm.listReferences()
            print("Importing " + str(len(refs)) + " references.")
            for ref in refs:
                if ref.isLoaded():
                    done = False
                    ref.importContents()
                else:
                    done = True
        print("Done importing references...")
        return True

    def remove_all_namespace(self):
        cmds.namespace(setNamespace=':')
        for ns in reversed(cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)):
            if ns != 'UI' and ns != 'shared':
                cmds.namespace(moveNamespace=(ns, ':'), force=True)
                cmds.namespace(removeNamespace=ns)

    def ply00_999_special_import(self):
        for ref in self.ply00_999_ref_imp:
            cmds.file(ref, ir=1)

        cmds.namespace(setNamespace=':')
        for ns in reversed(cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)):
            if ns != 'UI' and ns != 'shared':
                if 'ply00_999' in ns:
                    cmds.namespace(moveNamespace=(ns, ':'), force=True)
                    cmds.namespace(removeNamespace=ns)

        self.ply00_999_ref_imp=[]

    def func_export_fbx(self, root_jnt):
        if self.ply00_999_special == 'True':
            self.ply00_999_special_import()
        else:
            self.importAllReferences()
            self.remove_all_namespace()

        # self.importAllReferences()
        # self.remove_all_namespace()

        try:
            cmds.parent(root_jnt, w=1)
        except:
            pass
        cmds.select(root_jnt)
        cmds.bakeResults([root_jnt],
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         hierarchy='below',
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         controlPoints=False)

        # 保存するときの処理
        fbxspl = self.check_file.split('/')
        fname = fbxspl[-1].split('.')[0]

        mel.eval('FBXExport -f "{0}/{1}.fbx" -s;'.format(self.save_path, fname))

        print('Saved:{0}'.format(self.save_path, fname))
