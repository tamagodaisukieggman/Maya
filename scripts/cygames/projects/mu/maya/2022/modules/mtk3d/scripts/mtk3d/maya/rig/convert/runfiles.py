# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

from collections import OrderedDict
import codecs
from datetime import datetime
import os
import pdb
import sys
import traceback

# fktoikmatch
from mtk3d.maya.rig.ikfk.ikfkmatch import common as ikfk_common
reload(ikfk_common)

# deleteAnimNode
from mtk3d.maya.rig.convert import animnode
reload(animnode)

# mvn_convert_to_ply00_m_000
from mtk3d.maya.rig.convert import mvn_convert_to_ply00_m_000
reload(mvn_convert_to_ply00_m_000)

# mvn_convert_to_mob00_m_000
from mtk3d.maya.rig.convert import mvn_convert_to_mob00_m_000
reload(mvn_convert_to_mob00_m_000)

if cmds.pluginInfo('mayaHIK', q=True, l=True) == False:
    cmds.loadPlugin("mayaHIK")
if cmds.pluginInfo('mayaCharacterization', q=True, l=True) == False:
    cmds.loadPlugin("mayaCharacterization")
if cmds.pluginInfo('OneClick', q=True, l=True) == False:
    cmds.loadPlugin("OneClick")
if cmds.pluginInfo('fbxmaya', q=True, l=True) == False:
    cmds.loadPlugin("fbxmaya")

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

logFolder = '{}/log/'.format(dir_path)

class RunFiles(object):
    def __init__(self, fktoikmatch=None, deleteAnimNode=None, mvnToPly=None, mvnToMob=None, open_import='open'):
        # initialize
        self.open_import = open_import

        # functions
        # fktoikmatch
        self.fktoikmatch=fktoikmatch
        self.fktoikmatch_set_switch=None

        self.deleteAnimNode = deleteAnimNode

        self.mvnToPly = mvnToPly
        self.mvnToMob = mvnToMob

    def main(self, drop_path, save_path):
        self.drop_path=drop_path
        self.save_path=save_path
        try:
            self.run_files()
        except Exception as e:
            print(e)

    def file_open(self, file_path):
        cmds.file(f=1, new=1)
        cmds.file(file_path, f=1, o=1)

    def file_import(self, file_path):
        if file_path.endswith('.ma'):
            scene_type = 'mayaAscii'
            scene_options = 'v=0;p=17;f=0'
        elif file_path.endswith('.mb'):
            scene_type = 'mayaBinary'
            scene_options = 'v=0;'
        elif file_path.endswith('.fbx'):
            scene_type = 'FBX'
            scene_options = 'fbx'

        cmds.file(file_path,
                  pr=1,
                  ignoreVersion=1,
                  i=1,
                  type=scene_type,
                  importFrameRate=True,
                  importTimeRange="override",
                  mergeNamespacesOnClash=False,
                  options=scene_options)


    def run_files(self):
        if not os.path.isdir(logFolder):
            os.makedirs(logFolder)

        error_results=[]

        listFiles=[]
        folder_or_files = self.drop_path.split(' ')
        if folder_or_files == []:
            print('D&D error')
        for self.drop_path in folder_or_files:
            if '' == self.drop_path:
                print('empty:')
            else:
                if (
                    self.drop_path.endswith('.ma')
                    or self.drop_path.endswith('.mb')
                    or self.drop_path.endswith('.fbx')
                    ):
                    listFiles.append(self.drop_path)
                else:
                    for root, dirs, files in os.walk(self.drop_path):
                        for fname in files:
                            self.result=[]
                            file_path = os.path.join(root, fname)
                            if (
                                file_path.endswith('.ma')
                                or file_path.endswith('.mb')
                                or file_path.endswith('.fbx')
                                ):
                                listFiles.append(file_path)

        print('Files:')
        print('\n'.join(listFiles))
        print('\n')

        for file_path in listFiles:
            self.check_file = file_path.replace('\\', '/')
            if (
                self.check_file.endswith('.ma')
                or self.check_file.endswith('.mb')
                or self.check_file.endswith('.fbx')
                ):
                if self.open_import == 'open':
                    self.file_open(self.check_file)

                elif self.open_import == 'import':
                    try:
                        # functions
                        if self.mvnToPly:
                            mvn_to_ply = mvn_convert_to_ply00_m_000.MVNConvertToPly()
                            print(u'Start --{0}--'.format(self.save_path))
                            mvn_to_ply.main(current_scene=self.check_file, save_path=self.save_path)
                            print(u'End --------------------------------')

                        if self.mvnToMob:
                            mvn_to_mob = mvn_convert_to_mob00_m_000.MVNConvertToPly()
                            print(u'Start --{0}--'.format(self.save_path))
                            mvn_to_mob.main(current_scene=self.check_file, save_path=self.save_path)
                            print(u'End --------------------------------')

                    except Exception as e:
                        print(traceback.print_exc())
                        error_results.append((self.check_file, traceback.print_exc()))

            print('Current scene:{0}'.format(self.check_file))

            try:
                # functions
                if self.fktoikmatch:
                    ik2fk_fk2ik=ikfk_common.IKFKMatchMan()
                    print(u'Start --{0}--'.format(str(self.fktoikmatch)))
                    ik2fk_fk2ik.main(current_scene=cmds.file(q=1, sn=1), save_path=self.save_path, bat_mode=True, set_switch=self.fktoikmatch_set_switch)
                    print(u'End --{0}--'.format(str(self.fktoikmatch)))

                if self.deleteAnimNode:
                    deleteAnimNode = animnode.DeleteAnimNode()
                    print(u'Start --{0}--'.format(self.save_path))
                    deleteAnimNode.main(current_scene=cmds.file(q=1, sn=1), save_path=self.save_path)
                    print(u'End --{0}--'.format(deleteAnimNode.attribute_list))

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
