# -*- coding: utf-8 -*-
u"""ply00のボディ側のリグ関節をロケーターでコンストして、WorldOffset/LocalOffsetを独立して編集できるようにする

"""

import maya.cmds as cmds

from mtku.maya.log import MtkDBLog
from mtku.maya.menus.animation.bakemovectrl.command import bake_move_ctrl

from .base import BaseConst
from .ply import CtrlPly00 as Ctrl
from .ply import LocatorPly00 as Loc


logger = MtkDBLog(__name__)


class TurnTableFree(BaseConst):

    root_locator = 'TurnTableFree'
    locators = (
        # 下半身
        Loc.leg_r, Loc.leg_l,
        Loc.hip,
        # 胴・胸・両手首・アップベクター
        Loc.wrist_r, Loc.wrist_l,
        Loc.spine_a, Loc.spine_b,
        Loc.arm_pv_r, Loc.arm_pv_l,
        Loc.leg_pv_r, Loc.leg_pv_l,
        # ターンテーブル位置決め用
        Loc.turntable, Loc.foots,
    )
    root_children = root_locator, locators

    constrain_infos = (
        # 下半身
        {'src': Ctrl.leg_r, 'dst': Loc.leg_r, 'types': ('orient', 'point')},
        {'src': Ctrl.leg_l, 'dst': Loc.leg_l, 'types': ('orient', 'point')},
        {'src': Ctrl.hip, 'dst': Loc.hip, 'types': ('orient', 'point')},
        # 手首
        {'src': Ctrl.wrist_r, 'dst': Loc.wrist_r, 'types': ('orient', )},
        {'src': Ctrl.hand_r, 'dst': Loc.wrist_r, 'types': ('point', )},
        {'src': Ctrl.wrist_l, 'dst': Loc.wrist_l, 'types': ('orient',)},
        {'src': Ctrl.hand_l, 'dst': Loc.wrist_l, 'types': ('point',)},
        # 胴体
        {'src': Ctrl.spine_a, 'dst': Loc.spine_a, 'types': ('orient', 'point')},
        {'src': Ctrl.spine_b, 'dst': Loc.spine_b, 'types': ('orient', 'point')},
        # UpVector
        {'src': Ctrl.arm_pv_r, 'dst': Loc.arm_pv_r, 'types': ('orient', 'point')},
        {'src': Ctrl.arm_pv_l, 'dst': Loc.arm_pv_l, 'types': ('orient', 'point')},
        {'src': Ctrl.leg_pv_r, 'dst': Loc.leg_pv_r, 'types': ('orient', 'point')},
        {'src': Ctrl.leg_pv_l, 'dst': Loc.leg_pv_l, 'types': ('orient', 'point')},
        # ターンテーブル
        {'src': Ctrl.hip, 'dst': Loc.turntable, 'types': ('point', )},
        {'src': Ctrl.leg_r, 'dst': Loc.foots, 'types': ('point', )},
    )
    reverse_constrain_infos = (
        # 下半身
        {'src': Loc.leg_r, 'dst': Ctrl.leg_r, 'types': ('orient', 'point')},
        {'src': Loc.leg_l, 'dst': Ctrl.leg_l, 'types': ('orient', 'point')},
        {'src': Loc.hip, 'dst': Ctrl.hip, 'types': ('orient', 'point')},
        # 手首
        {'src': Loc.wrist_r, 'dst': Ctrl.wrist_r, 'types': ('orient',)},
        {'src': Loc.wrist_r, 'dst': Ctrl.hand_r, 'types': ('point',)},
        {'src': Loc.wrist_l, 'dst': Ctrl.wrist_l, 'types': ('orient',)},
        {'src': Loc.wrist_l, 'dst': Ctrl.hand_l, 'types': ('point',)},
        # 胴体
        {'src': Loc.spine_a, 'dst': Ctrl.spine_a, 'types': ('orient', )},
        {'src': Loc.spine_b, 'dst': Ctrl.spine_b, 'types': ('orient', )},
        # UpVector
        {'src': Loc.arm_pv_r, 'dst': Ctrl.arm_pv_r, 'types': ('point', )},
        {'src': Loc.arm_pv_l, 'dst': Ctrl.arm_pv_l, 'types': ('point', )},
        {'src': Loc.leg_pv_r, 'dst': Ctrl.leg_pv_r, 'types': ('point', )},
        {'src': Loc.leg_pv_l, 'dst': Ctrl.leg_pv_l, 'types': ('point', )},
    )

    move_ctrl = 'moveCtrl'
    local_offset = 'localOffset'

    @classmethod
    def _copy_move_ctrl_keys_to_local_offset(cls, namespace):
        cmds.copyKey('{}:{}'.format(namespace, cls.move_ctrl), hi='none')
        cmds.pasteKey('{}:{}'.format(namespace, cls.local_offset), o='replace')

    @classmethod
    def main(cls):
        u"""main関数"""
        logger.debug(cls.root_locator)
        # locatorチェック
        namespace = cls.get_namespace_from_selection()
        logger.debug('namespace: {}'.format(namespace))

        if cmds.ls(u'{}:{}'.format(namespace, cls.root_locator)):
            logger.warning(u'制御用Locatorが既に存在するので処理を停止しました')
            return

        if not namespace:
            # logger.warning(u'コントローラーセットからネームスペースを取得できませんでした')
            # controllerをbake
            ctrls = cmds.ls(sl=True, typ='objectSet')
            cls.bake(ctrls)

        # locator 生成
        cls.create_locator(cls.root_locator, namespace)
        [cls.create_locator(l, namespace) for l in cls.locators]

        # parent
        cls.parent(cls.root_locator, cls.locators, namespace)

        # コンストレイン
        for info in cls.constrain_infos:
            cls.constraint(info['src'], info['dst'], info['types'], namespace)

        # bake
        cls.bake(cls.locators, namespace)

        # コンストレイン (反転)
        for info in cls.reverse_constrain_infos:
            cls.constraint(info['src'], info['dst'], info['types'], namespace)

        # # 後で書き直す部分
        cmds.pointConstraint(
            '{}:{}'.format(namespace, Loc.foots),
            '{}:{}'.format(namespace, Loc.turntable),
            skip=('x', 'z'),
        )

        # ルートジョイントの値をmoveCtrlにキーとして打つ
        bake_move_ctrl(namespace='{}:'.format(namespace), btx=True, bty=False, btz=True, bry=False)

        # moveCtrlのキーをlocalOffsetにコピー
        cls._copy_move_ctrl_keys_to_local_offset(namespace)
