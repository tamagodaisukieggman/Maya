# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
import csv
from datetime import datetime
from imp import reload
import json
import logging
import math
import os
import subprocess
import sys
import timeit
import time
import traceback
import warnings
import xml.etree.ElementTree as ET

import maya.cmds as cmds
import maya.mel as mel
try:
    import pymel.core as pm
except:
    print(traceback.format_exc())
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.OpenMayaUI as omui

sys.dont_write_bytecode = True

maya_version = cmds.about(v=1)

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')
typFolder = '{}/types/'.format(dir_path)

# logFolder = '{}/log/'.format(dir_path)
# logFile = '{0}build_log.log'.format(logFolder)

# logging settings
formatter = "%(asctime)s: %(levelname)s - %(message)s"

logger = logging.getLogger()
logger.handlers = [] # This is the key thing for the question!

# Start defining and assigning your handlers here
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# logging.basicConfig(
#     filename=logFile,
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

# warnings.filterwarnings('ignore')

class Build(object):
    def __init__(self, buildPath=None, excactDir=None, logFolder=None, plus_image=None):
        """Build Commands
        from tkgTools.tkgRig.scripts.build import rigbuild
        reload(rigbuild)
        rb=rigbuild.Build(types='biped')
        rb.main()
        """

        self.logFolder = logFolder.replace('\\', '/')
        if not os.path.isdir(self.logFolder):
            os.makedirs(self.logFolder)

        self.logFile = '{0}/build_log.log'.format(self.logFolder)
        if '//' in self.logFile:
            self.logFile = self.logFile.replace('//', '/')

        fh = logging.FileHandler(self.logFile)
        logger.addHandler(fh)

        # list_types=None
        #
        # if types:
        #     if ',' in types:
        #         list_types=types.split(',')
        #     elif not ',' in types:
        #         list_types=[types]
        #
        # self.types=list_types
        if excactDir == '=/':
            excactDir=None
        self.excactDir=excactDir
        self.error_results=[]
        self.save_file_path_list=[]
        self.dataPath = buildPath.replace('\\', '/')
        self.buildPath = buildPath.replace('\\', '/')

        self.plus_image = plus_image

    def main(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt = u'{0}/error_{1}{2:4d}'.format(self.logFolder, now, datetime.now().microsecond) # 時間は%H%M%S

        logging.info('\n{}\n'.format('|'*100))
        logging.info('Build Date:{}'.format(perse_date(now)))
        logging.info('\n{}\n'.format('|'*100))

        # # scriptEditorInfoの情報の取得
        # flags = ["se", "si", "sr", "sw", "ssw"]
        # state = {}
        # for x in flags:
        #     kwargs = {"q" : True, x : True}
        #     val = cmds.scriptEditorInfo(**kwargs)
        #     state[x] = val

        # リグのビルド
        self.build_rigs()

        # # warningの停止
        # cmds.scriptEditorInfo(e=True, sw=True)
        #
        # # scriptEditorInfoの元の情報を設定
        # for x, val in state.iteritems():
        #     kwargs = {"e" : True, x : val}
        #     cmds.scriptEditorInfo(**kwargs)

        # xmlファイルを表示
        logging.info('\n{}\n'.format('='*20))
        logging.info('\n'.join(self.save_file_path_list))
        logging.info('\n{}\n'.format('='*20))

        if self.error_results: # error_resultがあれば、
            # txt = 'D:/error.csv'
            # txt = u'{0}/error_{1}{2:4d}.csv'.format(logFolder, datetime.now().strftime("%Y%m%d_%H%M%S"), datetime.now().microsecond) # 時間は%H%M%S
            save_csv = txt+'.csv'
            with open(save_csv, 'w') as csv_file:
                fieldnames = ['ID', 'FILE', 'LINE', 'ERROR']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for result in self.error_results:
                    writer.writerow({'ID':result[0], 'FILE':result[1], 'LINE':result[2], 'ERROR':result[3]})

        # cmds.quit(force=True)

    def build_rigs(self):
        build_file_list=[]

        logging.info('{}\nBuild Path:{}\n{}'.format('>'*10, self.buildPath, '>'*10))

        for root, dirs, files in os.walk(self.buildPath):
            for fname in files:
                file_path = os.path.join(root, fname)
                search_file = file_path.replace('\\', '/')
                if search_file.endswith('.xml'):
                    if self.excactDir:
                        # logging.info('Excact Dir:{0}'.format(self.excactDir))
                        if self.excactDir in search_file:
                            build_file_list.append(search_file)
                    else:
                        build_file_list.append(search_file)
                    # logging.info(self.build_file)

        list_build_file_list=list(set(build_file_list))

        builded_characters = []
        builded_error_characters = []

        logging.info('\n{}'.format('-'*10))
        logging.info('Build File List\n{}'.format(list_build_file_list))
        logging.info('\n{}'.format('-'*10))

        for build_file in list_build_file_list:
            self.build_file=build_file
            setup_settings = self.parseFile(self.dataPath)
            try:
                for setup_dir, setup_characters in setup_settings.items():
                    if not os.path.isdir(setup_dir):
                        logging.info('\n{} Skip Setup Directory {}\n{}\n'.format('^'*10, '^'*10, setup_dir))
                        continue

                    rig_setup_ids = setup_characters['rigSetupID']
                    chara_paths = setup_characters['charaPath']
                    save_file_paths = setup_characters['savefilepath']

                    logging.info('#'*10)
                    logging.info('Setup Characters:{}'.format(rig_setup_ids))
                    logging.info('Characters Path:{}'.format(chara_paths))
                    logging.info('Save File Paths:{}'.format(save_file_paths))
                    logging.info('#'*10)

                    for i, (rig_setup_id, chara_path, save_file_path) in enumerate(zip(rig_setup_ids, chara_paths, save_file_paths)):
                        try:
                            self.setup_rig(rig_setup_id=rig_setup_id, chara_path=chara_path, save_file_path=save_file_path)
                            builded_characters.append((rig_setup_id))
                        except Exception as e:
                            logging.info(traceback.format_exc())
                            builded_error_characters.append(rig_setup_id)

            except Exception as e:
                # logging.info(traceback.format_exc())
                # logger.error(e, exc_info=e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                # logging.info(exc_type, fname, exc_tb.tb_lineno)
                tbs = traceback.format_tb(exc_tb)[1]
                logging.info('\n{} ERROR {} \n File:{} \n Line:{} \n Message:{} \n \n'.format(
                    '#'*10,
                    '#'*10,
                    self.build_file,
                    tbs,
                    e))
                self.error_results.append((self.build_file, tbs, e))

        logging.info('Build Rigs: {}'.format(builded_characters))
        logging.info('Build Error: {}'.format(self.error_results))

    def setup_rig(self, rig_setup_id=None, chara_path=None, save_file_path=None):
        # --
        # setup info
        # --

        setup_path='/'.join(self.build_file.split('/')[:-1])

        # new file
        if chara_path:
            # if os.path.isfile(chara_path):
            #     cmds.file(new=1, f=1)
            #     cmds.file(chara_path, i=1, f=1)
            #     logging.info('Import File:{}'.format(chara_path))
            # else:
            #     if not os.path.isdir(chara_path):
            #         logging.info('Error Read File:{}'.format(chara_path))
            #     # raise ValueError('{0} is not exists!'.format(chara_path))

            fbxspl = chara_path.split('/')
            fname = fbxspl[-1].split('.')[0]

        if rig_setup_id:
            format_rig_setup_id = str(rig_setup_id)
            fname = str(rig_setup_id)

        logging.info('Rig Setup:{}'.format(format_rig_setup_id))
        logging.info('#'*10)

        setup_folders = [
            '{0}/010_primary'.format(setup_path),
            '{0}/020_secondary'.format(setup_path),
            '{0}/030_extra'.format(setup_path),
            '{0}/040_init'.format(setup_path),
            '{0}/050_lock'.format(setup_path),
            '{0}/060_user'.format(setup_path)
        ]

        # primary
        for setup_file_path in setup_folders:
            setup_folder_spl = setup_file_path.split('/')[-1]
            if self.check_files_in_folder(setup_file_path):
                logging.info('\n'+'#'*10+' {}:{} Start'.format(format_rig_setup_id, setup_folder_spl)+'#'*10+'\n')
                self.run_files(setup_file_path=setup_file_path, rig_setup_id=format_rig_setup_id, chara_path=chara_path)
                logging.info('\n'+'#'*10+' {}:{} End '.format(format_rig_setup_id, setup_folder_spl)+'#'*10+'\n')

        day = u'{0}'.format(datetime.now().strftime("%Y%m%d"))
        date = u'{0}{1:4d}'.format(datetime.now().strftime("%Y%m%d_%H%M%S"), datetime.now().microsecond) # 時間は%H%M%S
        if not save_file_path:
            save_file_path='{}/rig/{}/{}_rig_{}_{}.ma'.format('{}/000_data'.format(setup_path), day, fname, date, maya_version)

        self.makedirs('/'.join(save_file_path.split('.')[:-1][0].split('/')[:-1]))
        cmds.file(rn=save_file_path)

        if save_file_path.endswith('.ma'):
            file_type = "mayaAscii"
        elif save_file_path.endswith('.mb'):
            file_type = "mayaBinary"

        cmds.file(f=1, save=1, options='v=0', type=file_type)
        if self.plus_image:
            save_with_playblast(snapshot=True)

        self.save_file_path_list.append(save_file_path)
        logging.info('\n'+'+'*10+' Save File '+'+'*10+'\n')
        logging.info('Saved:{0}'.format(save_file_path))

        cmds.file(new=True, f=True)

    def run_files(self, setup_file_path=None, rig_setup_id=None, chara_path=None):
        for root, dirs, files in os.walk(setup_file_path):
            if root.endswith('old'):
                continue

            for fname in files:
                file_path = os.path.join(root, fname)
                build_file = file_path.replace('\\', '/')
                logging.info('{}Build:{}:{}'.format('-'*10, rig_setup_id, build_file))
                try:
                    if build_file.endswith('.py'):
                        if 2022 <= float(maya_version):
                            build_format = "rig_setup_id = '{}';chara_path = '{}';build_file = '{}';".format(rig_setup_id,
                                                                                                             chara_path,
                                                                                                             str(build_file))
                            exec(build_format + open(str(build_file), encoding="utf-8").read(), globals())
                        else:
                            # exec(codecs.open(str(build_file), encoding="utf-8").read())
                            execfile(build_file)

                    elif build_file.endswith('.mel'):
                        mel.eval('source "{0}"'.format(str(build_file)))

                except Exception as e:
                    # logging.info(traceback.format_exc())
                    # logger.error(e, exc_info=e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # logging.info(exc_type, fname, exc_tb.tb_lineno)
                    tbs = traceback.format_tb(exc_tb)[1]
                    logging.info('\n{} {}:ERROR Start {} \n File:{} \n Line:{} \n Message:{} \n \n'.format(
                        '!'*10,
                        rig_setup_id,
                        '!'*10,
                        build_file,
                        tbs,
                        e))
                    self.error_results.append((rig_setup_id, build_file, tbs, e))
                    logging.info('{} {}:ERROR End {}\n'.format('!'*10, rig_setup_id, '!'*10))

                    logging.info('{} {}:RESUME Process {}\n\n'.format('>'*10, rig_setup_id, '>'*10))

    def parseFile(self, dataPath=None):
        setup_character_dict = {}
        tree = ET.parse(self.build_file)
        root = tree.getroot()
        for char_path_value in root.iter('characters'):
            rig_setup_ids = []
            chara_paths=[]
            savefile_pathes=[]

            # char_path=char_path_value.attrib['dir']
            # char_path_slash = char_path.replace('\\', '/')

            setup_character_dict[dataPath] = {}

            for value in char_path_value.iter('character'):
                rig_setup_id=value.attrib['rigSetupID']
                rig_setup_id_slash = rig_setup_id.replace('\\', '/')
                rig_setup_ids.append(rig_setup_id_slash)

                # chara_path=char_path+value.attrib['charaPath']
                chara_path=value.attrib['charaPath']
                chara_path_slash = chara_path.replace('\\', '/')
                chara_paths.append(chara_path_slash)

                savefile_path=value.attrib['savefilepath']
                savefile_path = savefile_path.replace('\\', '/')
                if savefile_path == '':
                    savefile_path = None
                savefile_pathes.append(savefile_path)

            setup_character_dict[dataPath]['rigSetupID'] = rig_setup_ids
            setup_character_dict[dataPath]['charaPath'] = chara_paths
            setup_character_dict[dataPath]['savefilepath'] = savefile_pathes

        return setup_character_dict

    def check_files_in_folder(self, folder_path):
        # 指定されたフォルダ内のファイルとディレクトリを取得
        files_and_folders = os.listdir(folder_path)
        files_and_folders = [folder for folder in files_and_folders if not 'old' in folder]

        # ファイルのみを取得
        files = [f for f in files_and_folders if os.path.isfile(os.path.join(folder_path, f))]

        # .py または .mel ファイルが存在するかを確認
        for file in files:
            if file.endswith('.py') or file.endswith('.mel'):
                return True

        return False

    def makedirs(self, path=None):
        if not os.path.isdir(path):
            os.makedirs(path)

def perse_date(now):
    day_, time_ = now.split('_')
    year_str = ''.join(list(day_)[0:4])
    month_str = ''.join(list(day_)[4:6])
    day_str = ''.join(list(day_)[6:8])

    hour_str = ''.join(list(time_)[0:2])
    minu_str = ''.join(list(time_)[2:4])
    sec_str = ''.join(list(time_)[4:6])

    week = datetime(int(year_str), int(month_str), int(day_str))
    weekday_dict = {
        0:'MON',
        1:'TUE',
        2:'WED',
        3:'THU',
        4:'FRI',
        5:'SAT',
        6:'SUN'

    }
    dow = weekday_dict[week.weekday()]

    return '{}/{}/{}({}) {}:{}:{}'.format(year_str, month_str, day_str, dow, hour_str, minu_str, sec_str)

# def grabViewport(filePath):
#     viewport = omui.M3dView.active3dView()
#     viewport.refresh()
#     img = om.MImage()
#     img.create(1920, 1080)
#     viewport.readColorBuffer(img, True)
#     ext = filePath.split('.')[1]
#     img.writeToFile(filePath, ext)

def save_with_playblast(snapshot=None):
    cur_time=cmds.currentTime(q=1)
    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = 1
    else:
        autoKeyState = 0

    cmds.autoKeyframe(st=0)

    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)

    cur_path = cmds.file(q=1, sn=1)
    # cur_dir = os.path.split(cur_path)
    #
    # mayaSwatches_path = cur_dir[0] + '/.mayaSwatches/'
    # try:
    #     os.makedirs(mayaSwatches_path)
    # except FileExistsError:
    #     pass

    base_name, file_ext = os.path.splitext(cur_path)
    img_path = cur_path.replace(base_name + file_ext, base_name + '.jpg')

    if snapshot:
        playmin = cur_time
        playmax = playmin

    # grabViewport(mayaSwatches_path + '.jpg')

    cmds.playblast(st=playmin,
                   et=playmax,
                   format='image',
                   completeFilename=img_path,
                   percent=100,
                   viewer=False,
                   forceOverwrite=True,
                   fp=4,
                   showOrnaments=False,
                   quality=70,
                   clearCache=1)

    cmds.currentTime(cur_time)
    cmds.autoKeyframe(st=autoKeyState)


# if __name__ == "__main__":
#     rb=rigbuild.Build(type='biped')
#     rb.main()
