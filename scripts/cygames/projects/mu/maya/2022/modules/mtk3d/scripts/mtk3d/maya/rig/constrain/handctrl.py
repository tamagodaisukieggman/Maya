# -*- coding: utf-8 -*-
u"""手のひらの位置にグローバルでロケーターを作成してアニメーションコンストして制御できるようにする

"""
import maya.cmds as cmds

from mtku.maya.log import MtkDBLog
from .base import BaseConst
from .ply import CtrlPly00 as Ctrl
from .ply import LocatorPly00 as Loc


logger = MtkDBLog(__name__)


class HandCtrl(BaseConst):

    root_locator = 'HandCtrls'
    locators = (
        Loc.arm_pv_r, Loc.arm_pv_l,
        Loc.hand_r, Loc.hand_l,
    )
    hand_locators = (Loc.hand_r, Loc.hand_l)
    palm_locators = (Loc.palm_r, Loc.palm_l)
    # -----------------------------
    #  mode: 0
    dummy_locators = (
        Loc.dmy_hand_r, Loc.dmy_hand_l,
        Loc.dmy_palm_r, Loc.dmy_palm_l,
    )
    delete_locators = (Loc.dmy_hand_r, Loc.dmy_hand_l)
    # mode: 1

    # -----------------------------
    # mode:0
    palm_parent_children = (
        (Loc.dmy_hand_r, (Loc.dmy_palm_r,)),
        (Loc.dmy_hand_l, (Loc.dmy_palm_l,)),
        (Loc.palm_r, (Loc.hand_r,)),
        (Loc.palm_l, (Loc.hand_l,)),
        (root_locator, (Loc.palm_r, Loc.palm_l, Loc.arm_pv_r, Loc.arm_pv_l)),
    )

    # mode:1
    wrist_parent_children = (
        (root_locator, (Loc.hand_r, Loc.hand_l, Loc.arm_pv_r, Loc.arm_pv_l)),
    )

    # -----------------------------
    #  mode: 0
    palm_constrain_infos = (
        {'src': Ctrl.wrist_r, 'dst': Loc.dmy_hand_r, 'types': ('orient',)},
        {'src': Ctrl.hand_r, 'dst': Loc.dmy_hand_r, 'types': ('point',)},
        {'src': Ctrl.wrist_l, 'dst': Loc.dmy_hand_l, 'types': ('orient',)},
        {'src': Ctrl.hand_l, 'dst': Loc.dmy_hand_l, 'types': ('point',)},
        {'src': Loc.dmy_hand_r, 'dst': Loc.hand_r, 'types': ('orient', 'point')},
        {'src': Loc.dmy_palm_r, 'dst': Loc.palm_r, 'types': ('orient', 'point')},
        {'src': Loc.dmy_hand_l, 'dst': Loc.hand_l, 'types': ('orient', 'point')},
        {'src': Loc.dmy_palm_l, 'dst': Loc.palm_l, 'types': ('orient', 'point')},
        {'src': Ctrl.arm_pv_r, 'dst': Loc.arm_pv_r, 'types': ('point',)},
        {'src': Ctrl.arm_pv_l, 'dst': Loc.arm_pv_l, 'types': ('point',)},
    )

    reverse_palm_constrain_infos = (
        {'src': Loc.hand_r, 'dst': Ctrl.wrist_r, 'types': ('orient', )},
        {'src': Loc.hand_r, 'dst': Ctrl.hand_r, 'types': ('point', )},
        {'src': Loc.hand_l, 'dst': Ctrl.wrist_l, 'types': ('orient',)},
        {'src': Loc.hand_l, 'dst': Ctrl.hand_l, 'types': ('point',)},
        {'src': Loc.arm_pv_r, 'dst': Ctrl.arm_pv_r, 'types': ('point',)},
        {'src': Loc.arm_pv_l, 'dst': Ctrl.arm_pv_l, 'types': ('point',)},
    )
    #  mode: 1
    wrist_constrain_infos = (
        {'src': Ctrl.wrist_r, 'dst': Loc.hand_r, 'types': ('orient',)},
        {'src': Ctrl.hand_r, 'dst': Loc.hand_r, 'types': ('point',)},
        {'src': Ctrl.wrist_l, 'dst': Loc.hand_l, 'types': ('orient',)},
        {'src': Ctrl.hand_l, 'dst': Loc.hand_l, 'types': ('point',)},
        {'src': Ctrl.arm_pv_r, 'dst': Loc.arm_pv_r, 'types': ('point',)},
        {'src': Ctrl.arm_pv_l, 'dst': Loc.arm_pv_l, 'types': ('point',)},
        {'src': Ctrl.spine_b, 'dst': root_locator, 'types': ('orient', 'point')},
    )

    @classmethod
    def main(cls, mode):
        u"""main関数

        :param mode: 0: palm 1: wrist
        """
        logger.debug('{}: {}'.format(cls.root_locator, mode))

        # locatorチェック
        namespace = cls.get_namespace_from_selection()
        # if not namespace:
        #     logger.warning(u'コントローラーセットからネームスペースを取得できませんでした')
        #     return
        if cmds.ls(u'{}:{}'.format(namespace, cls.root_locator)):
            logger.warning(u'制御用Locatorが既に存在するので処理を停止しました')
            return

        # controllerをbake
        ctrls = cmds.ls(sl=True, typ='objectSet')
        cls.bake(ctrls)

        # locator 生成
        cls.create_locator(cls.root_locator, namespace)
        [cls.create_locator(l, namespace) for l in cls.locators]

        # 後で見直す部分
        cmds.setAttr(u'{}:{}.scale'.format(namespace, cls.locators[0]), 20, 20, 20)
        cmds.setAttr(u'{}:{}.scale'.format(namespace, cls.locators[1]), 20, 20, 20)
        cmds.setAttr(u'{}:{}.scale'.format(namespace, cls.locators[2]), 30, 30, 20)
        cmds.setAttr(u'{}:{}.scale'.format(namespace, cls.locators[3]), 20, 20, 20)

        if mode == 0:  # Palm
            # locator 生成
            [cls.create_locator(l, namespace) for l in cls.dummy_locators]
            [cls.create_locator(l, namespace) for l in cls.palm_locators]

            # locator サイズ調整
            # 後で見直す部分
            cmds.setAttr(u'{}:{}.t'.format(namespace, Loc.dmy_palm_r), -6, 0, -2)
            cmds.setAttr(u'{}:{}.t'.format(namespace, Loc.dmy_palm_l), 6, 0, -2)
            for l in cls.palm_locators:
                cmds.setAttr(u'{}:{}.scale'.format(namespace, l), 30, 30, 30)

            # parent
            [cls.parent(p, c, namespace) for p, c in cls.palm_parent_children]

            # コンストレイン
            for info in cls.palm_constrain_infos:
                cls.constraint(info['src'], info['dst'], info['types'], namespace)

            # bake
            cls.bake(list(cls.locators) + list(cls.palm_locators), namespace)

            # コンストレイン (反転)
            for info in cls.reverse_palm_constrain_infos:
                cls.constraint(info['src'], info['dst'], info['types'], namespace)

            # locator削除
            [cmds.delete(u'{}:{}'.format(namespace, l)) for l in cls.delete_locators]
            # locator非表示
            [cls.hide(l, namespace) for l in cls.hand_locators]

        else:  # Wrist
            # コンストレイン
            for info in cls.wrist_constrain_infos:
                cls.constraint(info['src'], info['dst'], info['types'], namespace)

            # parent
            [cls.parent(p, c, namespace) for p, c in cls.wrist_parent_children]

            # bake
            cls.bake(cls.locators, namespace)

            # コンストレイン (反転)
            for info in cls.reverse_palm_constrain_infos:
                cls.constraint(info['src'], info['dst'], info['types'], namespace)
