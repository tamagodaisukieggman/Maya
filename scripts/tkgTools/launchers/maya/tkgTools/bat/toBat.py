# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import fnmatch
import os
import re
import subprocess
import sys

from maya import cmds, mel


def python2bat(maya_cmd="import bat.fromBat as fromBat;reload(fromBat);fromBat.create_primitive()",
               add_cmds=None,
               exe_bat=None,
               create_bat=True,
               create_exe_bat=None,
               execute_created_bat=None,
               maya_version=None,
               filter_path=None,
               output_log_path=None,
               mel_system=False):

    u"""
    maya_cmd: type: string: You must set 'r' front of command r"import mymodule as mmd;reload(mmd);mmd.myFunc()"
    add_cmds: type: list: supplement commands list
    exe_bat: type: string: You want to execute bat file path.
    create_bat: type: bool: When you want to create bat from maya_cmd.
    create_exe_bat: type: string: If create_bat=True, creating file path.
    execute_created_bat: type: bool: When you want to execute your created bat right now.
    maya_version: type: int: Reccomend > int(cmds.about(v=1))
    filter_path: type: list: Filtering MAYA_SCRIPT_PATH, PYTHONPATH, MAYA_MODULE_PATH from name list > ['thirdPrty', 'student']
    mel_system: type: bool: Editing

    バッチを作成し、そのバッチに複数のファイルをD&Dしたい場合は'%ARGS%'を関数の引数にいれる
    """

    if add_cmds:
        for adcm in add_cmds:
            maya_cmd += adcm

    if filter_path:
        script_path = convert_needed_path(path=search_exist_path(os.getenv('MAYA_SCRIPT_PATH')), needed=['tkgTools', 'cygames'])
        python_path = convert_needed_path(path=search_exist_path(os.getenv('PYTHONPATH')), needed=['tkgTools', 'cygames'])
        module_path = convert_needed_path(path=search_exist_path(os.getenv('MAYA_MODULE_PATH')), needed=['tkgTools', 'cygames'])
        plugin_path = convert_needed_path(path=search_exist_path(os.getenv('MAYA_PLUG_IN_PATH')), needed=['tkgTools', 'cygames'])

    else:
        script_path = search_exist_path(os.getenv('MAYA_SCRIPT_PATH'))
        python_path = search_exist_path(os.getenv('PYTHONPATH'))
        module_path = search_exist_path(os.getenv('MAYA_MODULE_PATH'))
        plugin_path = search_exist_path(os.getenv('MAYA_PLUG_IN_PATH'))

    # Mayaコマンドを渡すと長くなるので、別のファイルにコマンドを書いて、それを実行するかたちのほうがいいかも
    # maya_cmd = '''
    # from maya import cmds, mel;
    # mel.eval("""
    # CreatePolygonSphere;
    # CreatePolygonCube;
    # CreatePolygonCylinder;
    # file -rn "{}/bat_test.ma";
    # file -f -save  -options "v=0;";
    # """)
    # '''.format(os.path.dirname(exe_bat))

    args = [maya_version,
            script_path,
            python_path,
            module_path,
            plugin_path,
            output_log_path,
            maya_cmd]

    # Create bat
    bat_sentence = r'''
@echo off

setlocal

::::::::::::::::::::::::::::::::::
::For Iteration
::::::::::::::::::::::::::::::::::
set ARGS=%*
set ARGS=%ARGS:\=/%

::::::::::::::::::::::::::::::::::
::Maya Default
::::::::::::::::::::::::::::::::::
set MAYA_UI_LANGUAGE=en_US
set PYTHONDONTWRITEBYTECODE=1

::::::::::::::::::::::::::::::::::
::Maya Path
::::::::::::::::::::::::::::::::::
set MAYA_SCRIPT_PATH={1}

set PYTHONPATH={2}

set MAYA_MODULE_PATH={3}

set MAYA_PLUG_IN_PATH={4}

set MAYA_CMD_FILE_OUTPUT={5}

::::::::::::::::::::::::::::::::::
::mayabatch
::::::::::::::::::::::::::::::::::
set COMMAND={6}
call "C:\Program Files\Autodesk\Maya{0}\bin\mayabatch.exe" -command "python(\"%COMMAND%\")"

pause

    '''.format(maya_version,
               script_path,
               python_path,
               module_path,
               plugin_path,
               output_log_path,
               maya_cmd)


    if create_bat:
        with open(create_exe_bat, mode='w') as f:
            f.write(bat_sentence)

        if execute_created_bat:
            os.system(create_exe_bat)
            return
        else:
            return


    # Python3
    if sys.version_info.major == 3:
        subprocess.run([exe_bat, args])

    # Python2
    mel_systen_words = ''
    if sys.version_info.major == 2:
        for i, arg in enumerate(args):
            if mel_system:
                if i == 0:
                    mel_systen_words += '"{}"'.format(arg)
                else:
                    mel_systen_words += " " + ' "{}"'.format(arg)
            else:
                exe_bat += " " + '"{}"'.format(arg)

        if mel_system:
            mel.eval('system("start {}" + {});'.format(exe_bat, mel_systen_words))
        else:
            os.system(exe_bat)


def convert_needed_path(path=None, needed=None):
    new_path = []
    for ne in needed:
        filtered = list(set(fnmatch.filter(path.split(';'), '*' + ne + '*')))
        for fil in filtered:
            new_path.append(fil)

    new_path = list(set(new_path))
    new_path.sort()

    return ';'.join(new_path)

def search_exist_path(path):
    return ';'.join([p for p in path.split(';') if os.path.isdir(p)])

def create_fromPython_execute_bat_check_nodes():
    # maya_cmd="from maya import cmds, mel;from imp import reload;import bat.fromBat as fromBat;reload(fromBat);fromBat.create_primitive();"
    maya_cmd="from maya import cmds, mel;from imp import reload;"

    add_cmds=[
    "import bat.fromBat as fromBat;",
    "reload(fromBat);",
    "batFunc = fromBat.BatFunc();",
    "batFunc.check_samename=True;",
    "batFunc.check_object_values=True;",
    "batFunc.run_files('%ARGS%');"
    ]

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/check_nodes.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=add_cmds,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

def create_fromPython_execute_bat_detach_joints():
    # maya_cmd="from maya import cmds, mel;from imp import reload;import bat.fromBat as fromBat;reload(fromBat);fromBat.create_primitive();"
    maya_cmd="from maya import cmds, mel;from imp import reload;"

    add_cmds=[
    "import bat.fromBat as fromBat;",
    "reload(fromBat);",
    "batFunc = fromBat.BatFunc();",
    "batFunc.detach_joints=True;",
    "batFunc.run_files('%ARGS%');"
    ]

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/detach_joints.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=add_cmds,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

def create_fromPython_execute_bat_detach_meshes():
    # maya_cmd="from maya import cmds, mel;from imp import reload;import bat.fromBat as fromBat;reload(fromBat);fromBat.create_primitive();"
    maya_cmd="from maya import cmds, mel;from imp import reload;"

    add_cmds=[
    "import bat.fromBat as fromBat;",
    "reload(fromBat);",
    "batFunc = fromBat.BatFunc();",
    "batFunc.detach_meshes=True;",
    "batFunc.run_files('%ARGS%');"
    ]

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/detach_meshes.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=add_cmds,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

def create_fromPython_execute_bat_save_values():
    # maya_cmd="from maya import cmds, mel;from imp import reload;import bat.fromBat as fromBat;reload(fromBat);fromBat.create_primitive();"
    maya_cmd="from maya import cmds, mel;from imp import reload;"

    add_cmds=[
    "import bat.fromBat as fromBat;",
    "reload(fromBat);",
    "batFunc = fromBat.BatFunc();",
    "batFunc.save_values=True;",
    "batFunc.run_files('%ARGS%');"
    ]

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/save_values.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=add_cmds,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

def create_fromPython_execute_bat_export_skinweights():
    # maya_cmd="from maya import cmds, mel;from imp import reload;import bat.fromBat as fromBat;reload(fromBat);fromBat.create_primitive();"
    maya_cmd="from maya import cmds, mel;from imp import reload;"

    add_cmds=[
    "import bat.fromBat as fromBat;",
    "reload(fromBat);",
    "batFunc = fromBat.BatFunc();",
    "batFunc.export_skinweights=True;",
    "batFunc.run_files('%ARGS%');"
    ]

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/export_skinweights.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=add_cmds,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

def create_fromPython_execute_bat_export_mb_file():
    maya_cmd="""
from maya import cmds, mel
from imp import reload
import bat.fromBat as fromBat
reload(fromBat)
batFunc = fromBat.BatFunc()
batFunc.export_mb_file=True
batFunc.run_files('%ARGS%')
    """

    maya_cmd = maya_cmd.replace('\n', ';').lstrip(';')

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/export_mb_file.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=None,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

def create_fromPython_execute_bat_all():
    maya_cmd="""
from maya import cmds, mel
from imp import reload
import bat.fromBat as fromBat
reload(fromBat)
batFunc = fromBat.BatFunc()
batFunc.check_samename=True
batFunc.check_object_values=True
batFunc.save_values=True
batFunc.export_skinweights=True
batFunc.export_mb_file=True
batFunc.detach_joints=True
batFunc.detach_meshes=True
batFunc.run_files('%ARGS%')
    """

    maya_cmd = maya_cmd.replace('\n', ';').lstrip(';')

    # exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/fromPython.bat'.format(os.getenv('USER'))
    create_exe_bat = r'C:/Users/{}/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/bat/execute_all.bat'.format(os.getenv('USER'))

    output_log_path = '{}/maya.log'.format(os.path.dirname(create_exe_bat))

    maya_version = int(cmds.about(v=1))

    python2bat(maya_cmd=maya_cmd,
               add_cmds=None,
                exe_bat=False,
                create_bat=True,
                create_exe_bat=create_exe_bat,
                execute_created_bat=False,
                maya_version=maya_version,
                filter_path=None,
                output_log_path=output_log_path,
                mel_system=False)

if __name__ == '__main__':
    create_fromPython_execute_bat_check_nodes()
    create_fromPython_execute_bat_detach_joints()
    create_fromPython_execute_bat_detach_meshes()
    create_fromPython_execute_bat_save_values()
    create_fromPython_execute_bat_export_skinweights()
    create_fromPython_execute_bat_export_mb_file()
    create_fromPython_execute_bat_all()
