# -*- coding: utf-8 -*-
"""ランダム位置生成
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import maya.api.OpenMaya as om
import random
import math
import maya.cmds as cmds


class PlacementObjs(object):

    def __init__(self):
        """コンストラクタ
        """

        pass

    def placement_objs_at_random_based_on_mesh(self, placement_value_info, target_obj_info_list):
        """オブジェクトをメッシュ状にランダムに配置する

        Args:
            placement_value_info: 配置情報がまとまったクラス
            target_obj_info_list: ランダムに配置されるオブジェクトの情報が入ったクラス
        """

        self.placement_value_info = placement_value_info
        self.target_obj_info_list = target_obj_info_list

        division_num = len(self.placement_value_info.base_mesh_list)

        rand_choice_target_obj_list = []
        for target_obj_info in self.target_obj_info_list:
            rand_choice_target_obj_list.extend([target_obj_info.target_obj] * target_obj_info.get_value())

        random.shuffle(rand_choice_target_obj_list)

        # obj_countをランダムに割り振る
        # メッシュ数分順番にランダムに振っていく方式の為
        # メッシュが増えれば増えるほど先に指定したメッシュに大きい値が振られがちになる
        rand_obj_count_list = []
        remaining_num = len(rand_choice_target_obj_list)
        for i in range(division_num):
            # 最後の値は残った数値をそのまま入れる
            if i == (division_num - 1):
                rand_obj_count_list.append(remaining_num)
            else:
                rand_obj_count = random.randint(0, remaining_num)
                rand_obj_count_list.append(rand_obj_count)
                remaining_num -= rand_obj_count

        if len(rand_choice_target_obj_list) != sum(rand_obj_count_list):
            cmds.warning('対象オブジェクト数が合致しません')
            return

        random_point_info_list = []
        for i in range(division_num):

            base_mesh = self.placement_value_info.base_mesh_list[i]
            if not cmds.objExists(base_mesh):
                cmds.warning('設定されたメッシュが存在しませんでした。')
                break
            rand_obj_count = rand_obj_count_list[i]

            points = self.generate_random_transform_based_on_mesh(
                base_mesh,
                self.placement_value_info.obj_distance,
                rand_obj_count,
                self.placement_value_info.avoidance_obj_list,
                self.placement_value_info.avoidance_distance_list
            )

            if len(points) != rand_obj_count:
                cmds.warning('オブジェクト数分のランダム配置が出来ませんでした。')
                break

            random_point_info_list.append(
                {
                    'base_mesh': base_mesh,
                    'points': points
                }
            )

        if len(random_point_info_list) != division_num:
            return

        cmds.undoInfo(openChunk=True)

        for rand_point_info in random_point_info_list:

            base_mesh = rand_point_info.get('base_mesh')
            points = rand_point_info.get('points')

            random_placement_obj_group_name = '{}_group'.format(
                base_mesh.split('|')[-1]
            )

            # 同じベースメッシュ名のグループを削除
            if cmds.objExists(random_placement_obj_group_name):
                cmds.delete(random_placement_obj_group_name)

            if not points:
                continue

            duplicate_obj_list = []
            for point in points:

                target_obj = rand_choice_target_obj_list.pop(0)

                # 高さ
                rand_height = self.generate_random_value(
                    self.placement_value_info.rand_min_height, self.placement_value_info.rand_max_height
                )

                # 回転。オイラーは軸ごとに回転させる場合もあるのでリストにしておく。
                quat = om.MQuaternion()
                rand_quat = om.MQuaternion()
                euler_list = []

                is_euler_rotation = False
                if self.placement_value_info.obj_placement_method == 'set_rotate':
                    is_euler_rotation = True
                elif self.placement_value_info.obj_placement_method == 'look_at_target':
                    is_euler_rotation = True

                if is_euler_rotation:
                    rand_euler = [
                        self.generate_random_value(
                            self.placement_value_info.rand_min_rotate_x,
                            self.placement_value_info.rand_max_rotate_x
                        ),
                        self.generate_random_value(
                            self.placement_value_info.rand_min_rotate_y,
                            self.placement_value_info.rand_max_rotate_y
                        ),
                        self.generate_random_value(
                            self.placement_value_info.rand_min_rotate_z,
                            self.placement_value_info.rand_max_rotate_z
                        ),
                    ]
                    euler_list = [rand_euler]
                else:
                    rand_quat = self.generate_random_rotate_quatanion(
                        [
                            self.placement_value_info.rand_min_rotate_x,
                            self.placement_value_info.rand_min_rotate_y,
                            self.placement_value_info.rand_min_rotate_z
                        ],
                        [
                            self.placement_value_info.rand_max_rotate_x,
                            self.placement_value_info.rand_max_rotate_y,
                            self.placement_value_info.rand_max_rotate_z
                        ],
                    )

                if self.placement_value_info.obj_placement_method == 'face_normal':

                    face_normal = self.get_closest_face_normal_vector(base_mesh, point)
                    face_normal_quat = self.convert_normal_vector_to_quaternion(face_normal)
                    quat = face_normal_quat * rand_quat

                    point = self.get_multiplied_translation_by_closest_face_normal(
                        point, rand_height, face_normal
                    )

                elif self.placement_value_info.obj_placement_method == 'set_rotate':

                    euler = [
                        self.placement_value_info.rotate_option_x,
                        self.placement_value_info.rotate_option_y,
                        self.placement_value_info.rotate_option_z,
                    ]

                    euler_list.insert(0, euler)

                    point = point
                    point[1] += rand_height

                elif self.placement_value_info.obj_placement_method == 'look_at_target':
                    # YupでZ方向をターゲットに向ける
                    quat = rand_quat
                    point = point
                    point[1] += rand_height

                    target_point = cmds.xform(
                        self.placement_value_info.look_at_target, q=True, ws=True, t=True
                    )

                    # 配置点から見たターゲットの位置ベクトル
                    look_vector = [
                        target_point[0] - point[0],
                        target_point[1] - point[1],
                        target_point[2] - point[2],
                    ]
                    # XZ平面での位置ベクトル
                    dir_vector = [
                        target_point[0] - point[0],
                        0,
                        target_point[2] - point[2],
                    ]
                    forward_vector = [0, 0, 1]

                    # 水平方向の向きを合わせた後、上下方向の向きを合わせる
                    if dir_vector != [0, 0, 0]:
                        om_look_vector = om.MVector(look_vector)
                        om_look_vector = om_look_vector.normalize()
                        om_forward_vector = om.MVector(forward_vector)
                        om_dir_vector = om.MVector(dir_vector)
                        om_dir_vector = om_dir_vector.normalize()

                        # XZ平面に投影して水平方向の向きを合わせる
                        dot_xz = self.get_dot_value([om_forward_vector[0], om_forward_vector[2]], [om_dir_vector[0], om_dir_vector[2]])
                        # 浮動小数点誤差を抑えるためクランプする
                        dot_xz = self.clamp_value(dot_xz, -1, 1)

                        euler_y = math.degrees(math.acos(dot_xz))
                        if self.get_cross_vector(om_forward_vector, om_dir_vector)[1] < 0:
                            # 外積ベクトルのY成分がマイナスなら逆回転
                            euler_y = euler_y * -1
                        rotate1 = [0, euler_y, 0]

                        # 上下方向の向きを合わせる
                        dot = self.get_dot_value(om_dir_vector, om_look_vector)
                        # 浮動小数点誤差を抑えるためクランプする
                        dot = self.clamp_value(dot, -1, 1)

                        euler_x = math.degrees(math.acos(dot))
                        if om_look_vector[1] > 0:
                            # Y成分がプラスなら見上げるので逆回転
                            euler_x = euler_x * -1
                        rotate2 = [euler_x, 0, 0]

                        # yzの順でまわす
                        euler_list.insert(0, rotate1)
                        euler_list.insert(1, rotate2)
                    else:
                        # ターゲットが真上or真下にいる場合
                        rotate = [90, 0, 0]
                        if look_vector[1] > 0:
                            rotate = [-90, 0, 0]
                        euler_list.insert(0, rotate)
                else:

                    quat = rand_quat
                    point = point
                    point[1] += rand_height

                dup_obj = cmds.duplicate(target_obj)

                if is_euler_rotation:
                    for euler in euler_list:
                        cmds.xform(dup_obj[0], ro=euler, os=True, r=True, eu=True)
                else:
                    self.set_rotate_by_quaternion(dup_obj[0], quat)

                cmds.setAttr(dup_obj[0] + ".translate", point[0], point[1], point[2])
                duplicate_obj_list.append(dup_obj[0])

            if duplicate_obj_list:
                cmds.group(duplicate_obj_list, n=random_placement_obj_group_name)

        cmds.undoInfo(closeChunk=True)

    def __get_fn_transform(self, target):
        """target名からopenMayaのMFnTransformノードを取得する

        Args:
            target: 取得するオブジェクトの名前

        Returns:
            MFnTransform
        """

        selection = om.MSelectionList()
        selection.add(target)
        depend_node = selection.getDependNode(0)
        fn_transform = om.MFnTransform(depend_node)

        return fn_transform

    def __get_fn_mesh(self, target):
        """targer名からopenMayaのMFnMeshノードを取得する

        Args:
            target: 取得するオブジェクトの名前

        Returns:
            MFnMesh
        """

        selection = om.MSelectionList()
        selection.add(target)
        dag_path = selection.getDagPath(0)
        fn_mesh = om.MFnMesh(dag_path)

        return fn_mesh

    def set_rotate_by_quaternion(self, target, quat):
        """対象のオブジェクトにQuaternionで回転を設定

        Args:
            target (object): 回転を設定するオブジェクト名
            quat (MQuaternion): 設定するQuaternion値
        """

        fn_transform = self.__get_fn_transform(target)
        fn_transform.rotateBy(quat, om.MSpace.kTransform)

    def get_closest_face_normal_vector(self, target, point):
        """対象のオブジェクトの、特定のポイントの最近似フェースの法線を取得

        Args:
            target: フェース法線を取得するオブジェクト
            point: 最近似フェースを取得するための特定の三次元座標
        """

        fn_mesh = self.__get_fn_mesh(target)

        # 第一変数 -> 最近似座標(利用せず)
        # 第二変数 -> 最近似フェースID
        _, closest_face_id = fn_mesh.getClosestPoint(point, om.MSpace.kWorld)
        # 最近似フェース法線 MVectorが戻り値
        face_normal = fn_mesh.getPolygonNormal(closest_face_id, om.MSpace.kWorld)

        return face_normal

    def convert_normal_vector_to_quaternion(self, normal):
        """法線ベクトルをクオータニオン値に変換

        Args:
            normal(MVector): 法線値

        Returns:
            MQuaternion 法線ベクトルを変換したクオータニオン値
        """

        return self.get_rotate_quaternion(om.MVector([0, 1, 0]), normal)

    def get_rotate_quaternion(self, origin, target):
        """回転に用いるクオータニオン値を取得

        Args:
            origin(MVector): 元々の方向ベクトル
            target(MVector): 向く先の方向ベクトル

        Returns:
            MQuaternion 法線ベクトルを変換したクオータニオン値
        """

        return om.MQuaternion(origin, target)

    def get_multiplied_translation_by_closest_face_normal(self, point, power, face_normal):
        """
        """

        multiplied_normal = face_normal * power
        return om.MPoint(point.x + multiplied_normal.x, point.y + multiplied_normal.y, point.z + multiplied_normal.z)

    def generate_random_value(self, min_value, max_value):
        """2つの値からランダムな値を生成

        Args:
            min_value(float): 最小値
            max_value(float): 最大値

        Returns:
            float 生成したランダム値
        """

        return random.uniform(min_value, max_value)

    def generate_random_rotate_quatanion(self, rotate_min, rotate_max):
        """ランダムなクオータニオン値を生成

        Args:
            rotate_min([x, y, z]): Angleの最小値
            rotate_max([x, y, z]): Angleの最大値

        Returns:
            MQuaternion ランダムなクオータニオン値
        """

        rand_x = random.uniform(rotate_min[0], rotate_max[0])
        rand_y = random.uniform(rotate_min[1], rotate_max[1])
        rand_z = random.uniform(rotate_min[2], rotate_max[2])

        rand_rotate_quat = om.MEulerRotation(
            math.radians(rand_x), math.radians(rand_y), math.radians(rand_z), om.MEulerRotation.kXYZ).asQuaternion()

        return rand_rotate_quat

    def get_dot_value(self, src_vector, dst_vector):
        """ベクトルの内積を求める

        Args:
            src_vector (vector): ベクトル1
            dst_vector (vector): ベクトル2
        """

        dot = 0

        for src_elm, dst_elm in zip(src_vector, dst_vector):
            dot += src_elm * dst_elm

        return dot

    def get_cross_vector(self, src_vector, dst_vector):
        """3次元ベクトルの外積ベクトルを求める

        Args:
            src_vector (vector3): ベクトル1
            dst_vector (vector3): ベクトル2
        """

        cross_vector = [0] * 3

        cross_vector[0] = \
            src_vector[1] * dst_vector[2] - \
            src_vector[2] * dst_vector[1]

        cross_vector[1] = \
            src_vector[2] * dst_vector[0] - \
            src_vector[0] * dst_vector[2]

        cross_vector[2] = \
            src_vector[0] * dst_vector[1] - \
            src_vector[1] * dst_vector[0]

        cross_length = \
            cross_vector[0] * cross_vector[0] + \
            cross_vector[1] * cross_vector[1] + \
            cross_vector[2] * cross_vector[2]

        cross_vector[0] /= cross_length
        cross_vector[1] /= cross_length
        cross_vector[2] /= cross_length

        return cross_vector

    def clamp_value(self, value, min, max):
        """値を範囲内にクランプする

        Args:
            value (float): クランプする値
            min (float): 最低範囲
            max (float): 最高範囲
        """

        if value < min:
            return min
        elif value > max:
            return max
        else:
            return value

    def generate_random_transform_based_on_mesh(self, target, distance, obj_num, avoidance_obj_list=[], avoidance_distance_list=[]):
        """メッシュの範囲にランダムな配置位置情報を生成する

        Args:
            target: 対象のオブジェクト
            distance (float): オブジェクト間の距離
            obj_num (int): 生成する位置情報の数
            avoidance_obj_list: オブジェクトを配置したくない中心のオブジェクトのリスト
            avoidance_distance_list (float): 配置したくない範囲のリスト(オブジェクト数と同数)
        """

        fn_translation_vector = None

        avoidance_transform_info_list = []
        if avoidance_obj_list:
            for i in range(len(avoidance_obj_list)):
                avoidance_obj = avoidance_obj_list[i]
                avoidance_distance = avoidance_distance_list[i]
                fn_transform = self.__get_fn_transform(avoidance_obj)
                fn_translation_vector = fn_transform.translation(om.MSpace.kTransform)
                avoidance_transform_info_list.append(
                    {
                        'fn_translation_vector': fn_translation_vector,
                        'avoidance_distance': avoidance_distance
                    })

        mesh_fn = self.__get_fn_mesh(target)

        distance = distance  # mに変換
        # 境界ボックスの最小角と最大角に適用するオフセットを計算
        half_voxel_dist = 0.5 * distance

        bounding_box = self.__get_bounding_box(mesh_fn)

        # バウンディングボックスの最小値を取得
        min_point = bounding_box.min
        min_point.x -= half_voxel_dist
        min_point.z -= half_voxel_dist

        # バウンディングボックスの最大値を取得
        max_point = bounding_box.max
        max_point.x += half_voxel_dist
        max_point.z += half_voxel_dist

        # 計算後のポジション情報を宣言
        voxels = []
        count = 0
        while len(voxels) < obj_num:

            rand_x = random.uniform(min_point.x, max_point.x)
            rand_z = random.uniform(min_point.z, max_point.z)

            base_point = om.MFloatPoint(rand_x, min_point.y, rand_z)

            max_param = 99999.0
            tolerance = 0.001
            ray_direction = om.MFloatVector(0, 1, 0)

            # 交差判定
            ret = mesh_fn.allIntersections(
                base_point,             # raySource ---------- レイスタートポイント
                ray_direction,          # rayDirection ------- レイの方向
                om.MSpace.kWorld,       # coordinate space --- ヒットポイントが指定されている座標空間
                max_param,              # maxParam ----------- ヒットを考慮する最大半径
                True,                   # testBothDirections - 負のrayDirectionのヒットも考慮する必要があるかどうか
                tolerance=tolerance,    # tolerance ---------- 交差操作の数値許容差
            )

            if (ret and len(ret[0]) % 2 == 1):

                point = om.MPoint(
                    om.MDistance(ret[0][0][0]).asUnits(om.MDistance.uiUnit()),
                    om.MDistance(ret[0][0][1]).asUnits(om.MDistance.uiUnit()),
                    om.MDistance(ret[0][0][2]).asUnits(om.MDistance.uiUnit())
                )

                is_overrapping = False
                # 基準オブジェクトからの重複禁止距離のヒットチェック
                if avoidance_transform_info_list:
                    for avoidance_transform_info in avoidance_transform_info_list:
                        fn_translation_vector = avoidance_transform_info.get('fn_translation_vector')
                        avoidance_distance = avoidance_transform_info.get('avoidance_distance')

                        distance_between_points = math.sqrt(
                            pow(fn_translation_vector.x - point[0], 2) + pow(fn_translation_vector.y - point[1], 2) + pow(fn_translation_vector.z - point[2], 2)
                        )

                        if distance_between_points < avoidance_distance:
                            is_overrapping = True
                            break

                # オブジェクト間の重複禁止距離のヒットチェック
                if not is_overrapping:
                    for voxel in voxels:
                        # 2点間の距離
                        distance_between_points = math.sqrt(
                            pow(voxel[0] - point[0], 2) + pow(voxel[1] - point[1], 2) + pow(voxel[2] - point[2], 2)
                        )
                        # print("distance_between_points : {}".format(distance_between_points))
                        if distance_between_points < distance:
                            break
                    else:
                        voxels.append(point)

            count += 1
            if count > pow(obj_num, 2) * 10:
                break

        return voxels

    def __float_iterator(self, start, stop, step):
        """分割用のイテレーター
        Args:
            start (flat): スタート値
            stop (flat)): ストップ値
            step (flaot): 分割の間隔
        Yields:
            float: 分割ポイント
        """
        r = start
        while r < stop:
            yield r
            r += step

    def __get_bounding_box(self, target):
        """選択したオブジェクトのバウンディング情報を取得
        """

        bounding_box = om.MBoundingBox()
        point_array = om.MPointArray()

        # ポイントの位置情報を取得
        point_array = target.getPoints(om.MSpace.kWorld)

        for points in range(len(point_array)):
            point = point_array[points]
            bounding_box.expand(point)

        return bounding_box
