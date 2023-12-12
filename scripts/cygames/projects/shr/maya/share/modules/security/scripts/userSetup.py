# -*- coding: utf-8 -*-
import maya.cmds as cmds
import security_command

#pluginのロード
cmds.evalDeferred('security_command.force_load_plugins()')

#uiConfigurationScriptNodeの不要なコールバックの除去
cmds.evalDeferred('cmds.scriptJob(event=("SceneOpened", "security_command.remove_corrupted_callbacks()"))')