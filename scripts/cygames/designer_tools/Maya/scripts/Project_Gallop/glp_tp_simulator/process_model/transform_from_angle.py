# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from . import base_model
from .. import utils

reload(base_model)


class TransformFlomAngleModel(base_model.BaseModel):

    def __init__(self, *args, **kwargs):
        super(TransformFlomAngleModel, self).__init__(*args, **kwargs)

        # 回転順調整用に作成されるノード群
        self.__m2u_rot_compose_node = None
        self.__m2u_rot_decompose_node = None
        self.__u2m_rot_compose_node = None
        self.__u2m_rot_decompose_node = None

        # Unity再現で実行前に子階層のセグメントスケールオフにする必要があるため、復元できるように初期値を保持するためのdict
        self.__init_segment_scale_dict = {}

    def create_param_data_template(self):
        """モデルのパラメーターテンプレート

        Returns:
            dict: パラメーターテンプレート
        """

        param_data_template = {
            'reference': {
                'type': 'string',
                'value': '',
            },
            'referenceAxis': {
                'type': 'string',
                'value': '',
            },
            'refMin': {
                'type': 'long',
                'value': 0,
            },
            'refMax': {
                'type': 'long',
                'value': 0,
            },
            'transformType': {
                'type': 'string',
                'value': 'position',
            },
            'valueX': {
                'type': 'long',
                'value': 0,
            },
            'valueY': {
                'type': 'long',
                'value': 0,
            },
            'valueZ': {
                'type': 'long',
                'value': 0,
            },
        }

        return param_data_template

    def validate_param_data(self):
        """パラメーターのチェック

        Returns:
            bool: パラメーターが適切かどうか
        """

        result, msg = super(TransformFlomAngleModel, self).validate_param_data()

        param_data = self.param_data()

        min_val = 0
        max_val = 0
        if 'refMin' in param_data:
            min_val = param_data['refMin'].get('value')
        if 'refMax' in param_data:
            max_val = param_data['refMax'].get('value')
        if min_val == max_val:
            result = False
            msg = 'refMinとrefMaxが同じ値です'

        return result, msg

    def create_process(self):
        """プロセスを実行するノードを作成

        Returns:
            bool: 実行結果
            list: 作成されたノードリスト
        """

        target = self.target()

        if not target:
            return False, []

        expression_name = self.__class__.__name__ + target.split('|')[-1]
        expression_body = self.__create_body()
        process_nodes = []

        if self.__m2u_rot_compose_node and cmds.objExists(self.__m2u_rot_compose_node):
            process_nodes.append(self.__m2u_rot_compose_node)
        if self.__m2u_rot_decompose_node and cmds.objExists(self.__m2u_rot_decompose_node):
            process_nodes.append(self.__m2u_rot_decompose_node)
        if self.__u2m_rot_compose_node and cmds.objExists(self.__u2m_rot_compose_node):
            process_nodes.append(self.__u2m_rot_compose_node)
        if self.__u2m_rot_decompose_node and cmds.objExists(self.__u2m_rot_decompose_node):
            process_nodes.append(self.__u2m_rot_decompose_node)

        try:
            process_node = cmds.expression(n=expression_name, s=expression_body)
            process_nodes.append(process_node)
            return True, process_nodes
        except Exception as e:
            print(e)
            return False, process_nodes

    def pre_start_process(self):
        """プロセスの前処理
        """

        self.__create_input_rotation_order_conversion_nodes()

        # transformTypeがrotateならUnityのzxy回転をMayaのxyz回転に直すノードを作成
        param_data = self.param_data()
        if 'transformType' in param_data:
            trans_type = param_data['transformType'].get('value')
            if trans_type == 'rotate':
                self.__create_output_rotation_order_conversion_nodes()

        # セグメントスケールの初期値を記録した後、オフにする
        self.__init_segment_scale_dict = self.__get_init_segment_scale_dict(self.target())
        for key, val in self.__init_segment_scale_dict.items():
            if val:
                cmds.setAttr(key + '.segmentScaleCompensate', False)

    def __create_input_rotation_order_conversion_nodes(self):
        """リファレンスからの入力rotateをzxy回転順に変換するノードを作成
        """

        reference = ''
        param_data = self.param_data()
        for key, val in param_data.items():
            if key == 'reference':
                reference = val.get('value', '')

        if not reference or not cmds.objExists(reference):
            return

        cmp_mtx, dcmp_mtx = utils.create_rotate_order_conversion_nodes(
            'xyz',
            'zxy',
            reference + '_M2U_ROT_ORDER'
        )

        cmds.connectAttr(reference + '.rotate', cmp_mtx + '.inputRotate', f=True)

        # 後処理のために登録
        self.__m2u_rot_compose_node = cmp_mtx
        self.__m2u_rot_decompose_node = dcmp_mtx

    def __create_output_rotation_order_conversion_nodes(self):
        """Tpへの出力rotateをxyz回転順に変換するノードを作成
        """

        target = self.target()

        cmp_mtx, dcmp_mtx = utils.create_rotate_order_conversion_nodes(
            'zxy',
            'xyz',
            target + '_M2U_ROT_ORDER'
        )
        cmds.connectAttr(dcmp_mtx + '.outputRotate', target + '.rotate', f=True)

        # 後処理のために登録
        self.__u2m_rot_compose_node = cmp_mtx
        self.__u2m_rot_decompose_node = dcmp_mtx

    def __get_init_segment_scale_dict(self, target):
        """子階層のセグメントスケール初期値を記録

        Args:
            target (str): 対象のジョイント

        Returns:
            {str: bool}: 子階層のジョイント名とセグメントスケール有効/無効のdict
        """

        segment_scale_dict = {}
        if not cmds.objExists(target):
            return segment_scale_dict

        descendents = cmds.listRelatives(target, ad=True, type='joint', pa=True)
        for joint in descendents:
            segment_scale_dict[joint] = cmds.getAttr(joint + '.segmentScaleCompensate')

        return segment_scale_dict

    def __create_body(self):
        """エクスプレッションのmelを作成
        """

        target = self.target()
        param_data = self.param_data()

        ref = self.__m2u_rot_decompose_node
        ref_axis = ''
        ref_min = 0
        ref_max = 0
        trans_type = ''
        val_x = 0
        val_y = 0
        val_z = 0

        for key, val in param_data.items():

            if key == 'referenceAxis':
                ref_axis = val.get('value', '')

            elif key == 'refMin':
                ref_min = val.get('value', 0)

            elif key == 'refMax':
                ref_max = val.get('value', 0)

            elif key == 'transformType':
                trans_type = val.get('value', '')

            elif key == 'valueX':
                val_x = val.get('value', 0)

            elif key == 'valueY':
                val_y = val.get('value', 0)

            elif key == 'valueZ':
                val_z = val.get('value', 0)

        # Unityコンポーネントに合わせたラベル名からアトリビュート名に変換
        attr = ''
        if trans_type == 'Position':
            attr = 'translate'
        elif trans_type == 'Rotate':
            attr = 'rotate'
        elif trans_type == 'Scale':
            attr = 'scale'
        target_attr_x = '{}.{}X'.format(target, attr)
        target_attr_y = '{}.{}Y'.format(target, attr)
        target_attr_z = '{}.{}Z'.format(target, attr)

        if attr == 'rotate' and self.__u2m_rot_compose_node:
            target_attr_x = '{}.inputRotateX'.format(self.__u2m_rot_compose_node)
            target_attr_y = '{}.inputRotateY'.format(self.__u2m_rot_compose_node)
            target_attr_z = '{}.inputRotateZ'.format(self.__u2m_rot_compose_node)

        init_val_x = cmds.getAttr(target_attr_x)
        init_val_y = cmds.getAttr(target_attr_y)
        init_val_z = cmds.getAttr(target_attr_z)

        ref_attr = ''
        if ref_axis == 'x':
            ref_attr = 'outputRotateX'
        elif ref_axis == 'y':
            ref_attr = 'outputRotateY'
        elif ref_axis == 'z':
            ref_attr = 'outputRotateZ'

        ref_attr = '{}.{}'.format(ref, ref_attr)

        body = '''
int $uiFactor = 10000;
int $unityTransFactor = 100;
int $refMin = {0};
int $refMax = {1};
float $initValX = {2};
float $initValY = {3};
float $initValZ = {4};
float $valX = {5};
float $valY = {6};
float $valZ = {7};
string $transType = "{8}";

float $weight = 0.0;

float $refRotVal = {9};

// unity軸に合わせる
if (`gmatch "{9}" "*outputRotateY"`) {{
    $refRotVal = $refRotVal * -1;
}}
else if (`gmatch "{9}" "*outputRotateZ"`) {{
    $refRotVal = $refRotVal * -1;
}}

// Refの回転値を-180～180の値にする
$refRotVal = $refRotVal % 360.0;
if ($refRotVal >= 180.0) {{
    $refRotVal = $refRotVal - 360.0;
}}
else if ($refRotVal <= -180.0) {{
    $refRotVal = $refRotVal + 360.0;
}}

// weightの計算(Unityの式に合わせる)
if ($refMin > $refMax) {{
    if ($refMin >= $refRotVal * $uiFactor) {{
        $weight = ($refMin - ($refRotVal * $uiFactor)) / ($refMin - $refMax);
    }}
}}
else if ($refMax > $refMin) {{
    if ($refMin <= $refRotVal * $uiFactor) {{
        $weight = (($refRotVal * $uiFactor) - $refMin) / ($refMax - $refMin);
    }}
}}

if ($weight < 0) {{
    $weight = 0;
}}
else if ($weight > 1) {{
    $weight = 1;
}}

// 出力値の計算
if ($transType == "rotate") {{

    // 回転はUnity軸との変換
    $valY = $valY * -1;
    $valZ = $valZ * -1;
}}
else if ($transType == "translate") {{

    // 移動値はUnity単位との変換
    $valX = $valX * $unityTransFactor * -1;
    $valY = $valY * $unityTransFactor;
    $valZ = $valZ * $unityTransFactor;
}}

float $fixValX = ($valX / $uiFactor) * $weight + $initValX;
float $fixValY = ($valY / $uiFactor) * $weight + $initValY;
float $fixValZ = ($valZ / $uiFactor) * $weight + $initValZ;

// ターゲットアトリビュートにセット
{10} = $fixValX;
{11} = $fixValY;
{12} = $fixValZ;
'''.format(
    ref_min,
    ref_max,
    init_val_x,
    init_val_y,
    init_val_z,
    val_x,
    val_y,
    val_z,
    attr,
    ref_attr,
    target_attr_x,
    target_attr_y,
    target_attr_z,
)
        return body

    def post_stop_process(self):
        """プロセス終了時の処理
        """
        self.__restore_init_segment_scale()

    def __restore_init_segment_scale(self):
        """子階層のセグメントスケールの初期値を復元
        """

        if self.__init_segment_scale_dict:
            for key, val in self.__init_segment_scale_dict.items():
                cmds.setAttr(key + '.segmentScaleCompensate', val)
