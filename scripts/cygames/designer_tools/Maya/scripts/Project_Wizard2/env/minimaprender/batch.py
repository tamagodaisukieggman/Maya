# -*- coding: utf-8 -*-
from distutils.util import strtobool
import json
import os
import traceback
import re
# from wzdx.log import get_logger
import maya.cmds as cmds
# from wzdx.maya.utils.perforce import Perforce
from .command import MiniMapRender

log_root = '{}/.tkgpublic/wzdx'.format(os.environ['TEMP'])
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_file = '{}/wx_minimap_render_bat.csv'.format(log_root)
log_file = re.sub(r'\\', '/', log_file)
# logger = get_logger(__name__, fh_config={'log_file': log_file})
from logging import getLogger
logger = logger = getLogger(__name__)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')


class MiniMapRenderBatch(object):

    @classmethod
    def _read_config_file(cls, key):
        with open(CONFIG_PATH, 'r') as config_file:
            try:
                data_set = json.load(config_file)
                return data_set[0][key]
            except Exception as e:
                logger.error(e)

    @classmethod
    def _is_maya_file(cls, file_path):
        u"""Mayaファイルか

        :param file_path: ファイルパス
        :return: bool
        """
        if file_path.endswith('.ma') or file_path.endswith('.mb'):
            return True
        else:
            return False

    @classmethod
    def _open_file(cls, maya_file_path):
        u"""Mayaシーンを開く

        :param maya_file_path: Mayaシーンのパス
        """
        try:
            if maya_file_path and os.path.exists(maya_file_path):
                sw = cmds.scriptEditorInfo(q=True, sw=True)
                cmds.scriptEditorInfo(sw=True)
                cmds.file(maya_file_path, o=True, f=True, rer=False, pmt=False)
                cmds.scriptEditorInfo(sw=sw)
                return True
            else:
                return False
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error(u'ファイルオープン失敗: {}'.format(maya_file_path))

            return False

    @classmethod
    def _get_maya_file_path(cls, root_path):
        u"""ファイルの取得"""
        for dirpath, dirnames, filenames in os.walk(root_path):
            for filename in filenames:
                if cls._is_maya_file(filename):
                    yield re.sub(r'\\', r'/', os.path.join(dirpath, filename))

    @classmethod
    def _get_maya_file_path_from_argument(cls, argument):
        u"""指定した引数からmayaファイルのパスを取得

        :param argument: 引数
        :return: mayaファイルのパス
        """
        if isinstance(argument, unicode) or isinstance(argument, str):  # noqa
            arguments = argument.split(' ')
            for argument in arguments:
                if os.path.isdir(argument):
                    for maya_file_path in cls._get_maya_file_path(argument):
                        yield maya_file_path

                elif cls._is_maya_file(argument):
                    yield re.sub(r'\\', r'/', argument)
                else:
                    continue

        elif isinstance(argument, list) or isinstance(argument, tuple):
            for arg_ in argument:
                for maya_file_path in cls._get_maya_file_path_from_argument(arg_):
                    yield maya_file_path
        else:
            return

    @classmethod
    def _create_output_path(cls, maya_file_path):
        u"""出力ファイルパス作成

        :return:
        """
        maya_scenes_directory = os.path.dirname(maya_file_path)
        root_directory = os.path.dirname(maya_scenes_directory)
        images_directory = '{}/images'.format(root_directory)
        file_name, _ = os.path.splitext(os.path.basename(maya_file_path))

        output_file_path = '{}/{}_tmp'.format(images_directory, file_name)

        return output_file_path

    @classmethod
    def _set_resolution_orthographic_width(cls, collision_camera, width, height, orthographic_width_multiply):
        u"""解像度に任意の値を乗算して正投影幅を設定

        :param collision_mesh:
        :param collision_camera:
        :return:
        """
        # XZは原点にする
        cmds.setAttr('{}.translateX'.format(collision_camera), 0)
        cmds.setAttr('{}.translateZ'.format(collision_camera), 0)

        # 解像度最大値に合わせて任意の値を乗算
        resolution = max(width, height) * orthographic_width_multiply
        cmds.camera(collision_camera, e=True, ow=resolution)
        logger.info(u'正投影幅: {}'.format(cmds.camera(collision_camera, q=True, ow=True)))

    @classmethod
    def _set_collision_orthographic_width(cls, meshes, collision_camera):
        u"""コリジョンメッシュのバウンディングボックス最大値に正投影幅を設定

        :return:
        """
        bounding_box_max = MiniMapRender._get_bounding_box(meshes)
        cmds.camera(collision_camera, e=True, ow=bounding_box_max)
        logger.info(u'正投影幅: {}'.format(cmds.camera(collision_camera, q=True, ow=True)))

    @classmethod
    def _rename_file(cls, file_path, *args):
        u"""レンダリグしたファイル名末尾の _tmp を除外してリネームする"""
        pass
        # image_dir = os.path.dirname(file_path)
        # filename, ext = os.path.splitext(os.path.basename(file_path))
        # filename = filename[:filename.find('_tmp')]
        # filename = filename.replace('mdl_', 'utx_minimap_map_')
        # output_saved_file = '{}/{}{}'.format(image_dir, filename, ext)
        # Perforce.edit(output_saved_file)
        # cmds.sysFile(file_path, rename=output_saved_file)
        # Perforce.add(output_saved_file)

        # return output_saved_file

    @classmethod
    def exec_(cls, maya_file_root_path):
        u"""Batch """

        logger.info(u'\n{:-^100}'.format(u'ミニマップレンダーバッチ処理開始'))

        open_errors = []
        open_files = 0
        minimap_node_errors = []
        output_files = []
        errors = []

        for maya_file_path in cls._get_maya_file_path_from_argument(maya_file_root_path):

            logger.info('\n{:-^100}'.format(os.path.basename(maya_file_path)))
            logger.info('{}: {}'.format(u'処理対象ファイル'.encode('cp932'), maya_file_path))

            if not cls._open_file(maya_file_path):
                open_errors.append(maya_file_path)
                continue

            minimap_mesh = MiniMapRender._get_minimap_mesh()

            if not minimap_mesh:
                logger.info('{}: {}'.format(u'minimap ノードが見つかりません'.encode('cp932'), maya_file_path))
                minimap_node_errors.append(maya_file_path)
                continue

            # 出力ファイルパス作成
            output_file_path = cls._create_output_path(maya_file_path)

            # config.json 読み込み
            resolution_width = int(cls._read_config_file('resolution_width'))
            resolution_height = int(cls._read_config_file('resolution_height'))
            image_format = str(cls._read_config_file('image_format'))
            lighting_mode = str(cls._read_config_file('lighting_mode'))
            orthographic_width_multiply = int(cls._read_config_file('orthographic_width_multiply'))
            orthographic = strtobool(str(cls._read_config_file('orthographic')))

            # レンダリング設定
            temp_collision_mesh = cmds.ls(MiniMapRender._post_minimap_render(minimap_mesh), assemblies=True)
            logger.debug('{}: {}'.format(u'コリジョンメッシュ複製'.encode('cp932'), temp_collision_mesh))

            image_format_value = MiniMapRender._get_image_format_value(image_format)
            logger.debug('{}: {}'.format(u'イメージフォーマット'.encode('cp932'), image_format_value))

            lighting_mode_value = MiniMapRender._get_lighting_mode_value(lighting_mode)
            logger.debug('{}: {}'.format(u'ライティングモード'.encode('cp932'), lighting_mode_value))

            MiniMapRender._set_render_settings(image_format_value, lighting_mode_value)
            logger.debug('{}'.format(u'レンダリング設定変更'.encode('cp932')))

            # レンダリング出力用ファイル名生成
            MiniMapRender._set_image_file_prefix(output_file_path)

            collision_camera, _ = MiniMapRender._create_render_camera()
            logger.info('{}: {}'.format(u'コリジョンレンダリングカメラ作成'.encode('cp932'), collision_camera))

            if orthographic:
                # 解像度に任意の値を乗算して正投影幅を設定
                logger.info('Orthographic Multiply On')
                cls._set_resolution_orthographic_width(collision_camera, resolution_width, resolution_height, orthographic_width_multiply)

            else:
                # コリジョンメッシュのバウンディングボックス最大値に正投影幅を設定
                logger.info('Orthographic Multiply Off')
                cls._set_collision_orthographic_width(minimap_mesh, collision_camera)

            # レンダリング実行
            result_output = u'{}.{}'.format(output_file_path, image_format)
            cmds.ogsRender(cam=collision_camera, w=resolution_width, h=resolution_height, cv=True, f=1.0)

            # リネームファイル
            saved_file = cls._rename_file(result_output)
            logger.info('{}: {}'.format(u'ファイルを保存'.encode('cp932'), saved_file))
            output_files.append(saved_file)
            logger.info('\n{:-^100}'.format(''))

            open_files += 1

        if output_files:
            logger.info(u'{:-<79}'.format(''))
            logger.info(u'出力したファイル'.encode('cp932'))
            for output_file in output_files:
                logger.info(output_file)
            logger.info(u'{:-<79}'.format(''))

        if errors:
            logger.info(u'エラーがあったファイル'.encode('cp932'))
            logger.info(u'{:-<79}'.format(''))
            for error in errors:
                logger.error(error)
            logger.info(u'{:-<79}'.format(''))

        if minimap_node_errors:
            logger.info(u'{:-<79}'.format(''))
            logger.info(u'minimap ノードがないファイル'.encode('cp932'))
            for error in minimap_node_errors:
                logger.error(error)
            logger.info(u'{:-<79}'.format(''))

        logger.info('{}'.format(u'処理を終了しました'.encode('cp932')))
        logger.info('{}: {}'.format(u'処理したファイル'.encode('cp932'), open_files))
        logger.info('{}: {}'.format(u'エラーファイル数'.encode('cp932'), len(errors)))
        logger.info('{}: {}'.format(u'ファイルオープンエラー数'.encode('cp932'), len(open_errors)))
        logger.info('{}: {}'.format(u'ログの出力先'.encode('cp932'), log_file))
        logger.info(u'\n{:-^100}'.format('END'))
