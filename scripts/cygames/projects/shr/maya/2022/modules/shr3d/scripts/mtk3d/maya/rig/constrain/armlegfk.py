# -*- coding: utf-8 -*-
u"""手足の関節位置にグローバルでロケーターを作成してアニメーションコンストレイントして擬似FK状態を作る

"""

import maya.cmds as cmds

from mtku.maya.log import MtkDBLog
from .base import BaseConst
from .ply import CtrlPly00 as Ctrl
from .ply import McProxyJtPly00 as ProxyJt
from .ply import LocatorPly00 as Loc


logger = MtkDBLog(__name__)


class ArmLegFK(BaseConst):

    # Locator
    root_locator = 'ArmLegFK'
    waist_children_locators = (
        Loc.leg_r, Loc.leg_l,
        Loc.knee_r, Loc.knee_l,
        Loc.foot_r, Loc.foot_l,
        Loc.leg_pv_l, Loc.leg_pv_r,
    )
    chest_children_locators = (
        Loc.shoulder_r, Loc.shoulder_l,
        Loc.arm_r, Loc.arm_l,
        Loc.forearm_r, Loc.forearm_l,
        Loc.hand_r, Loc.hand_l,
        Loc.arm_pv_r, Loc.arm_pv_l,
    )

    # parent, children
    parent_children = (
        # Waist
        (Loc.waist, (Loc.leg_r, Loc.leg_l)),
        (Loc.leg_r, (Loc.leg_pv_r, Loc.knee_r)),
        (Loc.leg_l, (Loc.leg_pv_l, Loc.knee_l)),
        (Loc.knee_r, (Loc.foot_r, )),
        (Loc.knee_l, (Loc.foot_l, )),
        # Chest
        (Loc.chest, (Loc.shoulder_r, Loc.shoulder_l, )),
        (Loc.shoulder_r, (Loc.arm_r, )),
        (Loc.shoulder_l, (Loc.arm_l, )),
        (Loc.arm_r, (Loc.arm_pv_r, Loc.forearm_r)),
        (Loc.arm_l, (Loc.arm_pv_l, Loc.forearm_l)),
        (Loc.forearm_r, (Loc.hand_r, )),
        (Loc.forearm_l, (Loc.hand_l,)),
    )

    # constrain
    constrain_infos = (
        # 右脚
        {'src': Ctrl.leg_r, 'dst': Loc.foot_r, 'types': ('orient', 'point')},
        {'src': ProxyJt.leg_r, 'dst': Loc.knee_r, 'types': ('orient', 'point')},
        {'src': ProxyJt.upleg_r, 'dst': Loc.leg_r, 'types': ('orient', 'point')},
        # 左脚
        {'src': Ctrl.leg_l, 'dst': Loc.foot_l, 'types': ('orient', 'point')},
        {'src': ProxyJt.leg_l, 'dst': Loc.knee_l, 'types': ('orient', 'point')},
        {'src': ProxyJt.upleg_r, 'dst': Loc.leg_l, 'types': ('orient', 'point')},
        # 脚 (アップベクター)
        {'src': Ctrl.leg_pv_r, 'dst': Loc.leg_pv_r, 'types': ('point', )},
        {'src': Ctrl.leg_pv_l, 'dst': Loc.leg_pv_l, 'types': ('point', )},
        # 右腕
        {'src': Ctrl.wrist_r, 'dst': Loc.hand_r, 'types': ('orient', )},
        {'src': Ctrl.hand_r, 'dst': Loc.hand_r, 'types': ('point',)},
        {'src': ProxyJt.forearm_r, 'dst': Loc.forearm_r, 'types': ('orient', 'point')},
        {'src': ProxyJt.arm_r, 'dst': Loc.arm_r, 'types': ('orient', 'point')},
        {'src': ProxyJt.shoulder_r, 'dst': Loc.shoulder_r, 'types': ('orient', 'point')},
        # 左腕
        {'src': Ctrl.wrist_l, 'dst': Loc.hand_l, 'types': ('orient',)},
        {'src': Ctrl.hand_l, 'dst': Loc.hand_l, 'types': ('point',)},
        {'src': ProxyJt.forearm_l, 'dst': Loc.forearm_l, 'types': ('orient', 'point')},
        {'src': ProxyJt.arm_l, 'dst': Loc.arm_l, 'types': ('orient', 'point')},
        {'src': ProxyJt.shoulder_l, 'dst': Loc.shoulder_l, 'types': ('orient', 'point')},
        # 腕 (アップベクター)
        {'src': Ctrl.arm_pv_r, 'dst': Loc.arm_pv_r, 'types': ('point',)},
        {'src': Ctrl.arm_pv_l, 'dst': Loc.arm_pv_l, 'types': ('point',)},
        # 腰
        {'src': Ctrl.hip, 'dst': Loc.waist, 'types': ('orient', 'point')},
        # 胴体
        {'src': Ctrl.spine_b, 'dst': Loc.chest, 'types': ('orient', 'point')},
    )
    reverse_constrain_infos = (
        # 右脚
        {'src': Loc.foot_r, 'dst': Ctrl.leg_r, 'types': ('orient', 'point')},
        # 左脚
        {'src': Loc.foot_l, 'dst': Ctrl.leg_l, 'types': ('orient', 'point')},
        # 脚 (アップベクター)
        {'src': Loc.leg_pv_r, 'dst': Ctrl.leg_pv_r, 'types': ('point',)},
        {'src': Loc.leg_pv_l, 'dst': Ctrl.leg_pv_l, 'types': ('point',)},
        # 右腕
        {'src': Loc.hand_r, 'dst': Ctrl.wrist_r, 'types': ('orient',)},
        {'src': Loc.hand_r, 'dst': Ctrl.hand_r, 'types': ('point',)},
        {'src': Loc.shoulder_r, 'dst': Ctrl.shoulder_r, 'types': ('orient',)},
        # 左腕
        {'src': Loc.hand_l, 'dst': Ctrl.wrist_l, 'types': ('orient',)},
        {'src': Loc.hand_l, 'dst': Ctrl.hand_l, 'types': ('point',)},
        {'src': Loc.shoulder_l, 'dst': Ctrl.shoulder_l, 'types': ('orient',)},
        # 腕 (アップベクター)
        {'src': Loc.arm_pv_r, 'dst': Ctrl.arm_pv_r, 'types': ('point',)},
        {'src': Loc.arm_pv_l, 'dst': Ctrl.arm_pv_l, 'types': ('point',)},
        # 腰
        {'src': Ctrl.hip, 'dst': Loc.waist, 'types': ('orient', 'point')},
        # 胴体
        {'src': Ctrl.spine_b, 'dst': Loc.chest, 'types': ('orient', 'point')},
    )

    @classmethod
    def main(cls):
        u"""main関数"""
        logger.debug(cls.root_locator)

        # locatorチェック
        namespace = cls.get_namespace_from_selection()
        logger.debug('namespace: {}'.format(namespace))
        # if not namespace:
        #     logger.warning(u'コントローラーセットからネームスペースを取得できませんでした')
        #     return
        if cmds.ls(u'{}:{}'.format(namespace, cls.root_locator)):
            logger.warning(u'制御用Locatorが既に存在するので処理を停止しました')
            return

        if not namespace:
            # logger.warning(u'コントローラーセットからネームスペースを取得できませんでした')
            # controllerをbake
            ctrls = cmds.ls(sl=True, typ='objectSet')
            cls.bake(ctrls)

        # controllerをbake
        # ctrls = cmds.ls(sl=True, typ='objectSet')
        # cls.bake(ctrls)

        # locator 生成
        cls.create_locator(cls.root_locator, namespace)
        cls.create_locator(Loc.waist, namespace)
        [cls.create_locator(l, namespace) for l in cls.waist_children_locators]
        cls.create_locator(Loc.chest, namespace)
        [cls.create_locator(l, namespace) for l in cls.chest_children_locators]

        # parent
        [cls.parent(p, c, namespace) for p, c in cls.parent_children]
        cls.parent(cls.root_locator, (Loc.waist, Loc.chest), namespace)

        # locatorサイズ調整
        scale = (15, 15, 15)
        for root_node in (Loc.waist, Loc.chest):
            cmds.setAttr(u'{}:{}.scale'.format(namespace, root_node), *scale)

        # コンストレイン
        for info in cls.constrain_infos:
            cls.constraint(info['src'], info['dst'], info['types'], namespace)

        # bake
        cls.bake((Loc.waist, Loc.chest), namespace)

        # コンストレイン (反転)
        for info in cls.reverse_constrain_infos:
            cls.constraint(info['src'], info['dst'], info['types'], namespace)

        # locator非表示
        [cls.hide(l, namespace) for l in (Loc.leg_pv_r, Loc.leg_pv_l, Loc.arm_pv_r, Loc.arm_pv_l)]
