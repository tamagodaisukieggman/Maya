# coding=utf-8

import logging
import os
import maya.cmds as cmds
import maya.mel as mel
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MiniMapRender(object):

    @classmethod
    def _set_output_transform_enabled(cls, output_transform_enabled):
        u"""Render Settings > Common > Color Management > Apply Output Transform to Render

        :return:
        """
        cmds.colorManagementPrefs(e=True, ote=output_transform_enabled)

    @classmethod
    def _set_output_transform_color_conversion(cls, output_transform_color_conversion):
        u"""Render Settings > Common > Color Management > Transform Type

        :param output_transform_color_conversion:
        :return:
        """
        cmds.colorManagementPrefs(e=True, otc=output_transform_color_conversion)

    @classmethod
    def _set_output_transform_name(cls, output_transform_name):
        u"""Color Management > Output Transform

        :param output_transform_name:
        :return:
        """
        try:
            cmds.colorManagementPrefs(e=True, otn=output_transform_name)
        except Exception as ex:
            cmds.warning(ex)

    @classmethod
    def _set_multi_sample_enable(cls, multi_sample_enable):
        u"""Render Settings > Maya Hardware 2.0 > Anti-aliasing > Multisample Anti-aliasing Enable

        :return:
        """
        hard_ware_render_globals = 'hardwareRenderingGlobals'
        cmds.setAttr('{}.multiSampleEnable'.format(hard_ware_render_globals), multi_sample_enable)

    @classmethod
    def _set_enable_default_light(cls, enable_default_light):
        u"""Render Settings > Common > Render Options > Enable Default Light

        :return:
        """
        default_render_globals = 'defaultRenderGlobals'
        cmds.setAttr('{}.enableDefaultLight'.format(default_render_globals), enable_default_light)

    @classmethod
    def _set_lighting_mode(cls, lighting_mode):
        u"""Hardware 2.0 > Render Options > Lighting Mode

        :param light_mode:
        :return:
        """
        hard_ware_render_globals = 'hardwareRenderingGlobals'
        cmds.setAttr('{}.lightingMode'.format(hard_ware_render_globals), lighting_mode)

    @classmethod
    def _set_image_format(cls, image_format):
        u"""Image format

        :param image_format: .jpg, .png, .tgaなど
        """
        default_render_globals = 'defaultRenderGlobals'
        cmds.setAttr('{}.imageFormat'.format(default_render_globals), image_format)

    @classmethod
    def _set_image_file_prefix(cls, image_file_prefix):
        u"""File Output > File Name Prefix

        :param image_file_prefix:
        :return:
        """
        default_render_globals = 'defaultRenderGlobals'
        if not image_file_prefix:
            cmds.setAttr('{}.imageFilePrefix'.format(default_render_globals), '', type='string')
        else:
            cmds.setAttr('{}.imageFilePrefix'.format(default_render_globals), image_file_prefix, type='string')

    @classmethod
    def _set_number_of_samples(cls, samples):
        u""" RenderSettings > Maya Hardware > Quality > Number Of Samples

        :param samples:
        :return:
        """
        hard_ware_render_globals = 'hardwareRenderGlobals'
        cmds.setAttr('{}.numberOfSamples'.format(hard_ware_render_globals), samples)

    @classmethod
    def _create_image_file(cls, directory, camera_name, frame):
        u"""カメラ名とフレームレートを出力ファイルに追加

        :param directory:
        :param camera_name:
        :param frame:
        :return:
        """
        # ネームスペース修正
        if ':' in camera_name:
            camera_name = camera_name.split(':')[1]
        scene_file_name = os.path.splitext(os.path.basename(cmds.file(q=True, sn=True)))[0]
        image_file_name = '{}_{}_{}'.format(scene_file_name, camera_name, frame)
        image_file = '{}/{}'.format(directory, image_file_name)

        return image_file

    @classmethod
    def _get_camera_frame(cls, camera_):
        u"""レンダリング用カメラのキーフレーム取得

        :return:
        """
        camera_look_at = cmds.listRelatives(camera_, p=True)

        if camera_look_at:
            key_frames = cmds.keyframe(camera_look_at, q=True, at='translateX')
            return key_frames
        else:
            key_frames = cmds.keyframe(camera_, q=True, at='translateX')
            return key_frames

    @classmethod
    def _get_render_settings(cls):
        u"""ツール実行前のレンダー情報取得

        :return:
        """

        default_render_globals = 'defaultRenderGlobals'
        hard_ware_render_globals = 'hardwareRenderingGlobals'

        output_transform_enabled = cmds.colorManagementPrefs(q=True, ote=True)
        output_transform_color_conversion = cmds.colorManagementPrefs(q=True, otc=True)
        output_transform_name = cmds.colorManagementPrefs(q=True, otn=True)
        multi_sample_enable = cmds.getAttr('{}.multiSampleEnable'.format(hard_ware_render_globals))
        enable_default_light = cmds.getAttr('{}.enableDefaultLight'.format(default_render_globals))
        lighting_mode = cmds.getAttr('{}.lightingMode'.format(hard_ware_render_globals))
        image_format = cmds.getAttr('{}.imageFormat'.format(default_render_globals))
        image_file_prefix = cmds.getAttr('{}.imageFilePrefix'.format(default_render_globals))
        number_of_samples = cmds.getAttr('hardwareRenderGlobals.numberOfSamples')

        render_settings = {
            'output_transform_enabled': output_transform_enabled,
            'output_transform_color_conversion': output_transform_color_conversion,
            'output_transform_name': output_transform_name,
            'enable_default_light': enable_default_light,
            'multi_sample_enable': multi_sample_enable,
            'lighting_mode': lighting_mode,
            'image_format': image_format,
            'image_file_prefix': image_file_prefix,
            'number_of_samples': number_of_samples,
        }

        return render_settings

    @classmethod
    def _set_before_render_settings(cls, befor_render_settings):
        u"""ツール実行前の状態に戻す

        :param befor_render_settings:
        :return:
        """

        output_transform_enabled = befor_render_settings['output_transform_enabled']
        output_transform_color_conversion = befor_render_settings['output_transform_color_conversion']
        output_transform_name = befor_render_settings['output_transform_name']
        multi_sample_enable = befor_render_settings['multi_sample_enable']
        enable_default_light = befor_render_settings['enable_default_light']
        lighting_mode = befor_render_settings['lighting_mode']
        image_format = befor_render_settings['image_format']
        image_file_prefix = befor_render_settings['image_file_prefix']
        number_of_samples = befor_render_settings['number_of_samples']

        cls._set_output_transform_enabled(output_transform_enabled)
        cls._set_output_transform_color_conversion(output_transform_color_conversion)
        cls._set_output_transform_name(output_transform_name)
        cls._set_multi_sample_enable(multi_sample_enable)
        cls._set_enable_default_light(enable_default_light)
        cls._set_lighting_mode(lighting_mode)
        cls._set_image_format(image_format)
        cls._set_image_file_prefix(image_file_prefix)
        cls._set_number_of_samples(number_of_samples)

    @classmethod
    def _set_render_settings(cls, image_format_value, lighting_mode_value):

        cls._set_output_transform_enabled(True)
        cls._set_output_transform_color_conversion(False)
        cls._set_output_transform_name('ACES 1.0 SDR-video (sRGB)')
        cls._set_multi_sample_enable(False)
        cls._set_enable_default_light(False)
        cls._set_lighting_mode(lighting_mode_value)  # 4: Full Ambient
        cls._set_image_format(image_format_value)  # 32: png
        cls._set_number_of_samples(1)

    @classmethod
    def _get_image_format_value(cls, image_format):

        index = {
            'tif': 3,
            'tif': 3,
            'jpg': 8,
            'tga': 19,
            'psd': 31,
            'png': 32,
        }

        return index[image_format]

    @classmethod
    def _get_lighting_mode_value(cls, lighting_mode):

        index = {
            'Default': 0,
            'All': 1,
            'None': 2,
            'Active': 3,
            'Full Ambient': 4,
        }

        return index[lighting_mode]

    # コリジョンメッシュ
    @classmethod
    def _get_minimap_mesh(cls):
        u"""コリジョンメッシュ取得
        既存のminimapグループがある場合はグループの子ノード
        :return:
        """
        minimap_mesh = []
        minimap_group = 'minimap'
        if cmds.ls(minimap_group):
            minimap_mesh = cmds.listRelatives(minimap_group, children=True, fullPath=True)
            return minimap_mesh
        all_mesh_transforms = []
        roots = cls._list_mesh_roots()
        for root in roots:
            if root.endswith('_col'):
                cmds.select(root, hierarchy=True)
                all_mesh_transforms = [cmds.listRelatives(i, p=True, fullPath=True)[0] for i in cmds.ls(sl=True, long=True, type='mesh')]
        for mesh_transform in all_mesh_transforms:
            if mesh_transform.find('_ground') > -1:
                if mesh_transform not in minimap_mesh:
                    minimap_mesh.append(mesh_transform)
        if not minimap_mesh:
            return False
        return minimap_mesh

    @classmethod
    def _list_mesh_roots(cls):
        all_top_nodes = cmds.ls(assemblies=True)
        all_cameras = cmds.listCameras()
        non_camera_roots = [x for x in all_top_nodes if x not in all_cameras]
        cmds.select(non_camera_roots, hi=True)
        meshes = cmds.ls(sl=True, long=True, type='mesh')
        mesh_roots = []
        for mesh in meshes:
            root = cls._get_root_node(mesh)
            if root not in mesh_roots:
                mesh_roots.append(root)
        return mesh_roots

    @classmethod
    def _get_root_node(cls, node):
        if not node:
            return
        parents = cmds.listRelatives(node, parent=True, fullPath=True)
        if not parents:
            return node
        else:
            for p in parents:
                return cls._get_root_node(p)

    @classmethod
    def _post_minimap_render(cls, collision_mesh):
        u"""複製して表示、それ以外非表示
        collision_meshをグループ化、minimapグループとして複製、
        元のcollision_meshのグループ化解除、minimapグループをWorld配下へ
        :param collision_mesh: _colグループ内のgroundのついたメッシュの配列
        :return: minimapグループ
        """
        cmds.hide(all=True)
        if not collision_mesh:
            return
        minimap_group = 'minimap'
        # 既存でminimapグループがある場合はそれをレンダリング
        if cmds.ls(minimap_group):
            if cmds.listRelatives(minimap_group, parent=True):
                cmds.parent(minimap_group, world=True)
            if not cmds.getAttr('{0}.visibility'.format(minimap_group)):
                cmds.showHidden(minimap_group, a=True)
            children = cmds.listRelatives(minimap_group, children=True)
            for child in children:
                # 子ノードの表示が非表示なら念のため聞く
                is_child_visible = cmds.getAttr('{0}.visibility'.format(child))
                if type(is_child_visible) is list:
                    is_child_visible = is_child_visible[-1]
                if not is_child_visible:
                    user_choice = cmds.confirmDialog(title='Confirm',
                                                     message='minimapグループ内に非表示の子がありますが表示しますか?',
                                                     button=['Yes','No'], defaultButton='Yes',
                                                     cancelButton='No', dismissString='No' )
                    if user_choice == 'Yes':
                        cmds.showHidden(minimap_group, a=True, b=True)
            return minimap_group
        # 既存でminimapグループがなければコリジョンメッシュから作成
        try:
            tmp_group = cmds.group(collision_mesh, n='tmp_col_orig_meshes')
            minimap_group = cmds.duplicate(tmp_group, renameChildren=False, name='minimap')[0]
            cmds.ungroup(tmp_group, world=False)
            cmds.parent(minimap_group, world=True)
            cmds.showHidden(minimap_group, a=True, b=True)
            return minimap_group
        except Exception as e:
            logger.info(u'複製に失敗しました')
            logger.error('{}'.format(e))
            return

    @classmethod
    def set_rotate_y(cls, node, **kwargs):
        u""" Y軸180度回転させる

        :param node:
        :param kwargs:
        :return:
        """
        cmds.setAttr(node + '.rotateY', 180)
        cmds.makeIdentity(node, a=True, n=False, pn=True)

    @classmethod
    def _output_file_name(cls):
        u"""出力ファイル名

        :param directory:
        :param file_name:
        :return:
        """
        base_name = os.path.basename(cmds.file(q=True, sn=True))
        scene_file_name, _ = os.path.splitext(base_name)
        return scene_file_name

    @classmethod
    def _get_collision_size(cls, collision_mesh):
        u"""コリジョン縦横の最大値を取得

        :return:
        """
        bounding_box = cmds.exactWorldBoundingBox(collision_mesh, ce=True, ii=False)
        bounding_box_width_height = [bounding_box[3] - bounding_box[0], bounding_box[5] - bounding_box[2]]
        bounding_box_max = max(bounding_box_width_height)
        return bounding_box_max

    @classmethod
    def _create_render_camera(cls):
        u"""レンダリング用カメラ生成

        :return:
        """
        if cmds.ls('minimap_capture_cameraShape', type='camera'):
            return cmds.listRelatives('minimap_capture_cameraShape', parent=True)[0]
        collision_cameras = cmds.camera(o=True)
        cam_name = 'minimap_capture_camera'
        cam_name = cmds.rename(collision_cameras[0], cam_name)
        cmds.setAttr('{}.rotateX'.format(cam_name), -90)
        cmds.setAttr('{}.translateY'.format(cam_name), 10000)
        cmds.setAttr('{}.farClipPlane'.format(cam_name), 100000)
        translate_y = cmds.getAttr('{}.translateY'.format(cam_name))
        far_clip_plane = cmds.getAttr('{}.farClipPlane'.format(cam_name))
        messages = [u'カメラY座標'.encode('cp932'), 'Far Clip Plane']
        logger.info('{}: {}, {}: {}'.format(messages[0], translate_y, messages[1], far_clip_plane))
        return cam_name

    @classmethod
    def _get_bounding_box(cls, collision_mesh):
        u"""コリジョンメッシュバウンディングボックスの長さ最大値取得

        :return:
        """
        bounding_box = cmds.exactWorldBoundingBox(collision_mesh, ce=True, ii=False)
        bounding_box_width_height = [bounding_box[3] - bounding_box[0], bounding_box[5] - bounding_box[2]]
        bounding_box_max = max(bounding_box_width_height)

        return bounding_box_max

    @classmethod
    def minimap_render_exec_(cls, output, width, height, image_format, lighting_mode, fill_percent, minimap_mesh, fill_checked, batch=False):
        u"""レンダリング実行(コリジョンメッシュレンダリング 背景データ用)

        :param output:
        :param width:
        :param height:
        :param image_format:
        :param lighting_mode:
        :param fill_percent:
        :param collision_mesh:
        :param fill_checked:
        :return:
        """
        if not minimap_mesh:
            if batch:
                cmds.warning('ミニマップのノードが見つかりませんでした')
            else:
                cmds.confirmDialog(title='Confirm',
                                   message='ミニマップのノードが見つかりませんでした',
                                   button=['OK'])
            return
        if not output:
            if batch:
                cmds.warning('出力ファイル名を指定してください')
            else:
                cmds.confirmDialog(title='Confirm',
                                   message='出力ファイル名を指定してください',
                                   button=['OK'])
            return
        if fill_checked:
            if fill_percent <= 0 or fill_percent > 100:
                if batch:
                    cmds.warning('Fill %は1~100で指定してください')
                else:
                    cmds.confirmDialog(title='Confirm',
                                   message='Fill %は1~100で指定してください',
                                   button=['OK'])
                return
        cls._post_minimap_render(minimap_mesh)

        temp_collision_mesh = cmds.ls(minimap_mesh, assemblies=True)
        # cls.set_rotate_y(temp_collision_mesh[0])

        # 元のレンダリング設定保存
        before_render_settings = cls._get_render_settings()

        image_format_value = cls._get_image_format_value(image_format)
        lighting_mode_value = cls._get_lighting_mode_value(lighting_mode)
        cls._set_render_settings(image_format_value, lighting_mode_value)

        # 出力用ファイル名生成
        cls._set_image_file_prefix(output)

        # 現在のビュー保存
        viewports = cmds.getPanel(type='modelPanel')
        visible = cmds.getPanel(vis=True)
        active_panel=''
        for panel in viewports:
            if panel in visible:
                active_panel = panel
                break
        current_camera = cmds.modelEditor(active_panel, q=True, cam=True)
        # コリジョンレンダリングカメラ作成
        collision_camera = cls._create_render_camera()
        cmds.modelEditor(active_panel, e=True, cam=collision_camera)
        cmds.select(minimap_mesh)
        if fill_checked:
            logger.info('Fill {}%'.format(fill_percent))
            # カメラフィット
            cmds.viewFit(fitFactor=(fill_percent*0.01))
        else:
            logger.info('Fill 100%')
            # カメラフィット
            cmds.viewFit()
        logger.info(u'正投影幅: {}'.format(cmds.camera(collision_camera, q=True, ow=True)))

        # レンダリング実行
        cmds.ogsRender(cam=collision_camera, w=width, h=height, cf=True, cv=True, ems=False)

        # 保存したファイルパス
        saved_file = u'{}_tmp.{}'.format(output, image_format)
        logger.info(u'ファイル保存: {}'.format(saved_file))

        # ビュー元に戻す
        mel.eval('lookThroughModelPanel {} {}'.format(current_camera, active_panel))

        # レンダー設定を元に戻す
        cls._set_before_render_settings(before_render_settings)
        return {'saved_file': saved_file, 'minimap_mesh': temp_collision_mesh, 'minimap_cameras': collision_camera}
