# coding: utf-8
import logging
import math
import os
import maya.cmds as cmds

from mtku.maya.menus.file.exporter import MotionSettings
from mtku.maya.menus.animation.cameramotion.settings import MtkCameraExportSettings
from mtku.maya.utils.bat import MtkBat
from mtku.maya.utils.perforce import MtkP4


logger = logging.getLogger(__name__)

ANIM_CURVE_T = ('animCurveTA', 'animCurveTL', 'animCurveTT', 'animCurveTU')
FPS_MAP = {'game': 15, 'film': 24, 'pal': 25, 'ntsc': 30, 'show': 48, 'palf': 50, 'ntscf': 60}


def to_fps_num(value):
    try:
        return int(value)
    except:
        pass

    try:
        return float(value)
    except:
        pass

    return value


def list_animcurve(exclude_clip=True, exclude_reference=True):
    """シーン内のアニメーションカーブを取得

    param bool exclude_clip: clipに接続されているカーブを除外
    param bool exclude_reference: リファレンスされているカーブを」除外
    return: animCurveノードのリスト
    rtype: list
    """

    crvs = cmds.ls(type=ANIM_CURVE_T)
    if not crvs:
        return []

    ret = []
    for crv in crvs:
        if exclude_reference and cmds.referenceQuery(crv, isNodeReferenced=True):
            continue

        crv_dst = cmds.listConnections('{}.o'.format(crv), s=False, d=True)
        if not crv_dst:
            continue

        if exclude_clip and cmds.objectType(crv_dst[0], i='clipLibrary'):
            continue

        ret += [crv]

    return ret


def convert_fps(scale_pivot_frame=0, offset_frame=0, to_fps='59.94', scale_fps=None):
    """シーンフレームレートの変換処理

    animCurve以外は考慮していないので注意。
    """

    if scale_pivot_frame is None:
        scale_pivot_frame = cmds.playbackOptions(q=True, min=True)

    scale_fps = scale_fps or to_fps

    scale_fps = to_fps_num(scale_fps)
    to_fps = to_fps_num(to_fps)

    current_time_unit = cmds.currentUnit(q=True, time=True).replace('fps', '').replace('df', '')
    current_fps = to_fps_num(FPS_MAP.get(current_time_unit, current_time_unit))

    if to_fps == current_fps:
        cmds.warning('現在のフレームレートが変換フレームレートと同じです。')
        return False

    playback_ast = cmds.playbackOptions(q=True, ast=True)
    playback_min = cmds.playbackOptions(q=True, min=True)
    playback_max = cmds.playbackOptions(q=True, max=True)
    playback_aet = cmds.playbackOptions(q=True, aet=True)

    logger.info('Current fps : {}'.format(current_fps))
    logger.info('Convert fps : {}'.format(to_fps))
    logger.info('Current Playback Range : [ {} ] - [ {} ]'.format(playback_min, playback_max))

    autokey_stat = cmds.autoKeyframe(q=True, st=True)
    cmds.autoKeyframe(st=False)
    cmds.refresh(suspend=True)
    # cmds.undoInfo(swf=False)
    cmds.undoInfo(ock=True)

    try:
        modify_crvs = list_animcurve()
        apply_crv_modify = bool(modify_crvs)

        if apply_crv_modify:
            # Euler Filter
            if cmds.objExists('*:CTRL_SETS'):
                ctrls = cmds.sets('*:CTRL_SETS', q=True)
                if ctrls:
                    logger.info('Apply Euler Filter.')
                    cmds.filterCurve(ctrls)

            # logger.info('Apply Euler Filter.')
            # cmds.filterCurve(modify_crvs)

        # if apply_crv_modify:
        #     logger.info('Pre Bake')
        #     crv_start_frame = cmds.findKeyframe(modify_crvs, which='first')
        #     crv_end_frame = cmds.findKeyframe(modify_crvs, which='last')
        #     cmds.bakeResults(modify_crvs,
        #         simulation=True,
        #         time=(crv_start_frame, crv_end_frame),
        #         sampleBy=1.0,
        #         disableImplicitControl=False,
        #         preserveOutsideKeys=False,
        #         sparseAnimCurveBake=False,
        #         removeBakedAttributeFromLayer=False,
        #         removeBakedAnimFromLayer=False,
        #         bakeOnOverrideLayer=False,
        #         minimizeRotation=False,
        #         controlPoints=False,
        #         shape=False
        #     )

        if scale_fps == 23.976:
            scale_fps = 24.0 * 1000.0 / 1001.0

        elif scale_fps == 29.97:
            scale_fps = 30.0 * 1000.0 / 1001.0

        elif scale_fps == 47.952:
            scale_fps = 48.0 * 1000.0 / 1001.0

        elif scale_fps == 59.94:
            scale_fps =  60.0 * 1000.0 / 1001.0

        time_scale = float(scale_fps) / float(current_fps)
        new_ast = scale_pivot_frame - (scale_pivot_frame - playback_ast) * time_scale
        new_min = scale_pivot_frame - (scale_pivot_frame - playback_min) * time_scale
        new_max = scale_pivot_frame + (playback_max - scale_pivot_frame) * time_scale
        new_aet = scale_pivot_frame + (playback_aet - scale_pivot_frame) * time_scale
        int_ast = math.floor(new_ast)
        int_min = math.floor(new_min)
        int_max = math.ceil(new_max)
        int_aet = math.ceil(new_aet)

        # fps変更
        logger.info('Change Fps : {} to {}'.format(current_fps, to_fps))
        cmds.currentUnit(time='{}fps'.format(to_fps), updateAnimation=False)

        # タイムスケール
        if apply_crv_modify:
            logger.info('Time Scale : pivot = {}, scale = {}'.format(scale_pivot_frame, time_scale))
            modify_crvs = list_animcurve()
            cmds.scaleKey(modify_crvs, timeScale=time_scale, timePivot=scale_pivot_frame)

            # エンドフレームのキーを移動
            logger.info('Move End Key to Integer Frame.')
            cmds.keyframe(modify_crvs, e=True, r=True, o='over', t=(new_max - 0.01, int_max + 0.01), tc=int_max - new_max)

            modify_crvs = list_animcurve()
            crv_start_frame = cmds.findKeyframe(modify_crvs, which='first')
            crv_end_frame = cmds.findKeyframe(modify_crvs, which='last')
            bake_start = int(round(crv_start_frame))
            bake_end = int(round(crv_end_frame))
            logger.info('Bake Animation : [ {} ] - [ {} ]'.format(bake_start, bake_end))
            cmds.bakeResults(modify_crvs,
                simulation=True,
                time=(bake_start, bake_end),
                sampleBy=1.0,
                disableImplicitControl=False,
                preserveOutsideKeys=False,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                removeBakedAnimFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=False,
                controlPoints=False,
                shape=False
            )

        # フレームオフセット
        if offset_frame != 0.0:
            logger.info('Frame Offset.')
            modify_crvs = list_animcurve()
            cmds.keyframe(modify_crvs, e=True, r=True, o='over', tc=offset_frame)

            logger.info('Update Playback Range : [ {} ] - [ {} ]'.format(int_min + offset_frame, int_max + offset_frame))
            cmds.playbackOptions(
                ast=int_ast + offset_frame, 
                min=int_min + offset_frame, 
                max=int_max + offset_frame, 
                aet=int_aet + offset_frame
            )
        else:
            # タイムレンジ更新
            logger.info('Update Playback Range : [ {} ] - [ {} ]'.format(int_min, int_max))
            cmds.playbackOptions(ast=int_ast, min=int_min, max=int_max, aet=int_aet)

        # シーン内のエクスポート設定を更新
        logger.info('Update Export Settings.')
        fix_start = cmds.playbackOptions(q=True, min=True)
        fix_end = cmds.playbackOptions(q=True, max=True)

        # Export Settings
        export_settings = MotionSettings.get_export_sets(MotionSettings.root_export_set)
        if export_settings:
            for setting in export_settings:
                start = cmds.getAttr('{}.start'.format(setting))
                end = cmds.getAttr('{}.end'.format(setting))
                cmds.setAttr('{}.start'.format(setting), fix_start)
                cmds.setAttr('{}.end'.format(setting), fix_end)

        # Camera Export Settings
        camera_settings = MtkCameraExportSettings.get_all_setting_nodes()
        if camera_settings:
            for setting in camera_settings:
                start = cmds.getAttr('{}.start'.format(setting))
                end = cmds.getAttr('{}.end'.format(setting))
                cmds.setAttr('{}.start'.format(setting), fix_start)
                cmds.setAttr('{}.end'.format(setting), fix_end)

    except Exception as e:
        print(str(e))

    finally:
        cmds.undoInfo(cck=True)
        # cmds.undoInfo(swf=True)
        cmds.refresh(suspend=False)
        cmds.autoKeyframe(st=autokey_stat)

    return True


def convert_scene(src_file, dst_file, scale_pivot_frame=0, to_fps='59.94'):
    if not os.path.isfile(src_file):
        return False

    # New Scene
    cmds.file(new=True, f=True)

    # Scene Open
    cmds.file(src_file, f=True, options='v=0', ignoreVersion=True, typ='mayaAscii', o=True)

    # fps convert
    try:
        ret = convert_fps(scale_pivot_frame=scale_pivot_frame, to_fps=to_fps)
        if not ret:
            return False

    except Exception as e:
        print(str(e))
        return False

    dst_dir = os.path.dirname(dst_file)
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    # Scene Rename
    cmds.file(rename=dst_file)

    # Save
    cmds.file(f=True, options='v=0', save=True)

    # New Scene
    cmds.file(new=True, f=True)

    return True


def convert_scenes(export_dir, target_files, scale_pivot_frame=0, to_fps='59.94', checkout=False):
    if not os.path.isdir(export_dir):
        logger.warning('# 出力ディレクトリが見つかりません。')
        return

    target_files = list(MtkBat.get_maya_file_path_from_argument(target_files))
    num_targets = len(target_files)

    logger.info('#' * 50)
    logger.info('Convert target : {} files'.format(num_targets))
    logger.info('#' * 50)

    success_files = []
    failed_files = []

    for cnt, convert_target in enumerate(target_files, 1):
        convert_target = convert_target.replace(os.sep, '/')
        base_name = os.path.basename(convert_target)
        dst_file = os.path.join(export_dir, base_name).replace(os.sep, '/')
        print('\n')
        logger.info('#' * 50)
        logger.info('# [ {} / {} ] Convert Start: {}'.format(cnt, num_targets, base_name))
        logger.info('#' * 50)

        if os.path.exists(dst_file):
            if checkout:
                MtkP4.edit(dst_file)

        ret = convert_scene(convert_target, dst_file, scale_pivot_frame=scale_pivot_frame, to_fps=to_fps)

        logger.info('#' * 50)
        if ret:
            success_files.append(convert_target)
            logger.info('# [ {} / {} ] Convert Success: {}'.format(cnt, num_targets, base_name))
        else:
            failed_files.append(convert_target)
            logger.warning('# [ {} / {} ] Convert Failed: {}'.format(cnt, num_targets, base_name))
        logger.info('#' * 50)
        print('\n')

    logger.info('#' * 50)
    logger.info('Convert Finished : All {}, Success {}, Failed {}'.format(num_targets, len(success_files), len(failed_files)))
    if failed_files:
        for failed_file in failed_files:
            logger.warning('failed : {}'.format(failed_file))
    logger.info('#' * 50)
