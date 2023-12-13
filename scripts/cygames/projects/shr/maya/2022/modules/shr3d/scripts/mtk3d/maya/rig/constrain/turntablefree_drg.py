# -*- coding: utf-8 -*-
u"""drg00のボディ側のリグ関節をロケーターでコンストして、WorldOffset/LocalOffsetを独立して編集できるようにする

"""

import maya.cmds as cmds

from mtku.maya.log import MtkDBLog
from .base import BaseConst
from .drg import CtrlDrg00 as Ctrl
from .drg import LocatorDrg00 as Loc


logger = MtkDBLog(__name__)


class TurnTableFreeDrg(BaseConst):

    root_locator = 'TurnTableFreeDrg'
    locators = (
        # 四肢
        Loc.footF_l, Loc.footF_r,
        Loc.foot_r, Loc.foot_l,
        # 胴体
        Loc.cog,
        # pv
        Loc.footF_pv_r, Loc.footF_pv_l,
        Loc.foot_pv_r, Loc.foot_pv_l,
        # ターンテーブル位置決め用
        Loc.turntable, Loc.foots,
    )
    root_children = root_locator, locators

    constrain_infos = (
        # 四肢
        {'src': Ctrl.foot_r, 'dst': Loc.foot_r, 'types': ('orient', 'point')},
        {'src': Ctrl.foot_l, 'dst': Loc.foot_l, 'types': ('orient', 'point')},
        {'src': Ctrl.footF_r, 'dst': Loc.footF_r, 'types': ('orient', 'point')},
        {'src': Ctrl.footF_l, 'dst': Loc.footF_l, 'types': ('orient', 'point')},

        # 胴体
        {'src': Ctrl.cog, 'dst': Loc.cog, 'types': ('orient', 'point')},

        # UpVector
        {'src': Ctrl.footF_pv_r, 'dst': Loc.footF_pv_r, 'types': ('orient', 'point')},
        {'src': Ctrl.footF_pv_l, 'dst': Loc.footF_pv_l, 'types': ('orient', 'point')},
        {'src': Ctrl.foot_pv_r, 'dst': Loc.foot_pv_r, 'types': ('orient', 'point')},
        {'src': Ctrl.foot_pv_l, 'dst': Loc.foot_pv_l, 'types': ('orient', 'point')},
        # ターンテーブル
        {'src': Ctrl.cog, 'dst': Loc.turntable, 'types': ('point', )},
    )
    reverse_constrain_infos = (
        # 四肢
        {'src': Loc.foot_r, 'dst': Ctrl.foot_r, 'types': ('orient', 'point')},
        {'src': Loc.foot_l, 'dst': Ctrl.foot_l, 'types': ('orient', 'point')},
        {'src': Loc.footF_r, 'dst': Ctrl.footF_r, 'types': ('orient', 'point')},
        {'src': Loc.footF_l, 'dst': Ctrl.footF_l, 'types': ('orient', 'point')},

        # 胴体
        {'src': Loc.cog, 'dst': Ctrl.cog, 'types': ('orient', 'point')},

        # UpVector
        {'src': Loc.footF_pv_r, 'dst': Ctrl.footF_pv_r, 'types': ('point', )},
        {'src': Loc.footF_pv_l, 'dst': Ctrl.footF_pv_l, 'types': ('point', )},
        {'src': Loc.foot_pv_r, 'dst': Ctrl.foot_pv_r, 'types': ('point', )},
        {'src': Loc.foot_pv_l, 'dst': Ctrl.foot_pv_l, 'types': ('point', )},
    )

    @classmethod
    def main(cls):
        u"""main関数"""
        logger.debug(cls.root_locator)

        # locatorチェック
        namespace = cls.get_namespace_from_selection()
        if not namespace:
            logger.warning(u'コントローラーセットからネームスペースを取得できませんでした')
            return
        if cmds.ls(u'{}:{}'.format(namespace, cls.root_locator)):
            logger.warning(u'制御用Locatorが既に存在するので処理を停止しました')
            return

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

        # 後で書き直す部分
        cmds.pointConstraint(
            '{}:{}'.format(namespace, Loc.foots),
            '{}:{}'.format(namespace, Loc.turntable),
            skip=('x', 'z'),
        )
