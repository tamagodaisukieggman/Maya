# -*- coding=utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re
import os.path
from importlib import reload

import maya.cmds as cmds

# http://help.autodesk.com/cloudhelp/2018/JPN/Maya-Tech-Docs/PyMel/
try:
    import pymel.core as pmc
except Exception:
    cmds.confirmDialog( title='Confirm', message='PyMelをインストールしてください', button=['OK'])

from . import utility
reload(utility)


class PhysicalMaterial(object):

    def __init__(self):
        super(PhysicalMaterial, self).__init__()
        self._config = None
        self._shading_node_type = 'lambert'
        self._col_mesh_regex = '^(ms)_(w\d{2})_([asd]{1}\d{3})_(ground)(\d{2})_([a-zA-Z0-9]{3})_([a-zA-Z0-9]{2})'

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config_object=None):
        if config_object is not None:
            self._config = config_object

    @property
    def shading_node(self):
        return self._shading_node_type

    @shading_node.setter
    def shading_node(self, type_string='lambert'):
        self._shading_node_type = type_string

    @staticmethod
    def liner_to_srgb(liner):
        return [pow(*data) for data in zip(liner, [1 / 2.2] * 3)]

    @staticmethod
    def srgb_to_liner(srgb):
        return [pow(*data) for data in zip(srgb, [2.2] * 3)]

    def _find_config(self, name):

        for config in self._config:
            if name == config['name']:
                print('Find configuration: {} = {}'.format(name, config))
                return config

        return None

    def _create(self, name=''):
        # マテリアルを作ると選択状態が変わるので、事前に選択状態を得ておく。
        selected = cmds.ls(sl=True)
        shading_node = None
        shading_engine = None
        if name and cmds.ls(name):
            return name
        else:
            shading_node = cmds.shadingNode('lambert', name=name, asShader=True)
            shading_engine = cmds.sets(name='%sSG' % shading_node, empty=True, renderable=True, noSurfaceShader=True)
            cmds.connectAttr('%s.outColor' % shading_node, '%s.surfaceShader' % shading_engine)
        # 選択状態を戻す。
        cmds.select(selected, replace=True)
        print('Create: {}'.format(shading_node))
        return shading_node

    def _connection(self, shading_pynode, shadingengine_pynode):
        """_shading_node_typeがsurfaceShaderの時に利用
        Args:
            shading_pynode (pymel Object): surfaceShader
            shadingengine_pynode (pymel Object): shadingEngine
        """
        if self._shading_node_type == 'surfaceShader':
            # pmc.connectAttr('{}.outColor'.format(shading_pynode.name()), '{}.surfaceShader'.format(shadingengine_pynode.name()), force=True)
            shading_pynode.attr('outColor').connect(shadingengine_pynode.attr('surfaceShader'))

    def _find_shading_pair(self, name):
        shading_node = None
        shading_engine = None

        config = self._find_config(name)

        nodes = pmc.ls(config['name'], type=self._shading_node_type)
        if len(nodes) == 1:
            shading_node = nodes[0]

        if not shading_node:
            cmds.confirmDialog( title='Confirm', message='設定がありません\nTAにご連絡ください', button=['OK'])

        nodes = shading_node.attr('outColor').outputs(type='shadingEngine')
        if len(nodes) == 1:
            shading_engine = nodes[0]

        return shading_node, shading_engine
    
    def _list_col_mesh_by_type(self, type):
        mesh_by_type = []
        minimap_mesh = self._get_minimap_mesh()
        for full_path in minimap_mesh:
            mesh = full_path.split('|')[-1]
            match_obj = re.match(self._col_mesh_regex, mesh)
            if match_obj:
                if match_obj.group(7) == type:
                    mesh_by_type.append(full_path)
        return mesh_by_type

    # コリジョンメッシュ
    def _get_minimap_mesh(self):
        u"""コリジョンメッシュ取得
        :return:
        """
        minimap_mesh = []
        all_mesh_transforms = []
        roots = self._list_mesh_roots()
        for root in roots:
            if root.endswith('_col'):
                cmds.select(root, hierarchy=True)
                all_mesh_transforms = [cmds.listRelatives(i, p=True, fullPath=True)[0] for i in cmds.ls(sl=True, long=True, type='mesh')]
        if not all_mesh_transforms:
            all_mesh_transforms = [cmds.listRelatives(i, p=True, fullPath=True)[0] for i in cmds.ls(long=True, type='mesh')]
        for mesh_transform in all_mesh_transforms:
            if mesh_transform.find('_ground') > -1:
                if mesh_transform not in minimap_mesh:
                    minimap_mesh.append(mesh_transform)
        if not minimap_mesh:
            return False
        return minimap_mesh
    
    def _get_root_node(self, node):
        if not node:
            return
        parents = cmds.listRelatives(node, parent=True, fullPath=True)
        if not parents:
            return node
        else:
            for p in parents:
                return self._get_root_node(p)

    def _list_mesh_roots(self):
        all_top_nodes = cmds.ls(assemblies=True)
        all_cameras = cmds.listCameras()
        non_camera_roots = [x for x in all_top_nodes if x not in all_cameras]
        cmds.select(non_camera_roots, hi=True)
        meshes = cmds.ls(sl=True, long=True, type='mesh')
        mesh_roots = []
        for mesh in meshes:
            root = self._get_root_node(mesh)
            if root not in mesh_roots:
                mesh_roots.append(root)
        return mesh_roots

    def _unlock(self, shading_node=None):
        targets = [shading_node]
        targets.extend(shading_node.attr('outColor').outputs(type='shadingEngine'))

        for target in targets:
            if target.isLocked():
                target.unlock()

    def _set_color(self, shading_node, name):
        """マテリアルの色をコンフィグ（config.json）に指定した色にする
        Args:
            shading_node (str): マテリアル名
            name (str): config.jsonのname.
        """
        if not shading_node:
            cmds.warning('色変え失敗: shading_nodeがありません')
            return
        if not name:
            cmds.warning('色変え失敗: config.jsonのnameが指定されていません')
            return
        config = self._find_config(name)
        if not config:
            cmds.warning('色変え失敗: config.jsonにname「{}」が指定されていません'.format(name))
            return
        try:
            cmds.objectType(shading_node)
        except Exception as ex:
            print(ex)
        if self._shading_node_type == 'surfaceShader':
            shading_node.attr('outColor').set(config['color'])
            print('Change material color: {}.outColor = {}'.format(shading_node, config['color']))
        elif self._shading_node_type == 'lambert':
            cmds.setAttr('{}.color'.format(shading_node), config['color'][0], config['color'][1], config['color'][2])
            print('Change material color: {}.color = {}'.format(shading_node, config['color']))
        else:
            print('{}はサポートしていません'.format(str(self._shading_node_type)))

    @utility.undo_chunk
    def members(self, name='None'):
        print('Members: {}'.format(name))

        _, shading_engine = self._find_shading_pair(name)

        targets = []
        if shading_engine is not None:
            targets = shading_engine.elements()
            targets = pmc.ls(targets, flatten=True)
            targets = [tg for tg in targets if 'shaderBallGeomShape' not in tg.name()]

        return targets

    @utility.undo_chunk
    def select(self, name='None'):
        print('Select: {}'.format(name))
        type = name.split('_')[-1]
        mesh_by_type = self._list_col_mesh_by_type(type)
        if mesh_by_type:
            cmds.select(mesh_by_type)

    @utility.undo_chunk
    def assign(self, name='None'):
        print('Assign: {}'.format(name))
        targets = []
        selection = cmds.ls(sl=True, long=True)
        if len(selection) == 0:
            return
        for mesh_long_name in selection:
            mesh_short_name = mesh_long_name.split('|')[-1]
            match_obj = re.match(self._col_mesh_regex, mesh_short_name)
            if not match_obj:
                user_choice = cmds.confirmDialog(title='Warning', message='コリジョンの命名規則と違いますが続行しますか?',
                                                 button=['続行', 'Cancel'],
                                                 defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel')
                if user_choice == 'Cancel':
                    return
            targets.append(mesh_long_name)
        for mesh_long_name in targets:
            shapes = cmds.listRelatives(mesh_long_name, shapes=True, path=True)
            if shapes:
                mats = self._get_assigned_materials(shapes[0])
                mesh_short_name = mesh_long_name.split('|')[-1]
                target_material = ''
                if mats:
                    if mesh_short_name.startswith('ms_'):
                        expected_mat_name = 'mt_{}'.format(mesh_short_name[len('ms_'):])
                        for mat in mats:
                            if mat == expected_mat_name:
                                target_material = mat
                    else:
                        expected_mat_name = 'mt_{}'.format(mesh_short_name)
                else:
                    return
                if not target_material:
                    target_material= self._create(name=expected_mat_name)
                self._set_color(shading_node=target_material, name=name)
                shading_engine = cmds.listConnections(target_material, type='shadingEngine')
                if shading_engine:
                    shading_engine = shading_engine[0]
                cmds.sets(mesh_long_name, forceElement=shading_engine)
            else:
                cmds.warning('No shape found')

    def _get_assigned_materials(self, shape):
        """オブジェクトにアサインされているマテリアルを取得する関数
        Args:
            obj (str): オブジェクト名(shape)
        Returns:
            tp.Optional[str]: マテリアル名 (マテリアルが見つからない場合はNone)
        """

        materials = set()
        shading_groups = cmds.listConnections(shape, type="shadingEngine")
        if not shading_groups:
            cmds.warning('No shadingEngine')
            return []

        for sg in shading_groups:
            connected_materials = cmds.ls(cmds.listConnections(sg), materials=True)
            if connected_materials:
                materials.update(connected_materials)

        # フェースにアサインされているマテリアルを取得
        num_faces = cmds.polyEvaluate(shape, face=True)
        for i in range(num_faces):
            face = "{}.f[{}]".format(shape, i)
            shading_group = cmds.listConnections(face, type="shadingEngine")
            if shading_group:
                connected_material = cmds.ls(
                    cmds.listConnections(shading_group), materials=True
                )
                if connected_material:
                    materials.update(connected_material)

        return list(materials)

    @utility.undo_chunk
    def check(self):
        """

        """
        materials = {}

        for config in self._config:
            nodes = pmc.ls(config['name'], type=self._shading_node_type)

            # 定義に従ったマテリアルが見つからなかったら
            if len(nodes) == 0:

                if config['enable']:
                    mtl, sg = self._create(name=config['name'])
                    self._connection(mtl, sg)

                    nodes = [mtl, sg]

                else:
                    continue

            # 定義に従ったマテリアルが見つかったら
            elif len(nodes) == 1:

                # 定義で無効化を指示されていたら
                if not config['enable']:
                    # アサインを退避した後に削除する？
                    self._unlock(shading_node=nodes[0])

                    continue

                else:
                    pass

            else:
                pass

            self._set_color(shading_node=nodes[0], name=config['name'])
            materials.update({config['name']: nodes[0]})

        return materials
