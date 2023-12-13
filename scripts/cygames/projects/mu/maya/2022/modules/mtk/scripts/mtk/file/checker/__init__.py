# -*- coding: utf-8 -*-
u"""Checker"""
from .model.gui import CharaChecker
from .model.gui import EnvChecker
from .model.gui import RigChecker
# from .unknown import Unknown
from .model.validation import Validation
from .motion.validation import MotionValidation
from .model.modification import Modification
from .model.gui import Checker


# from mtku.maya.mtklog import MtkLog


__all__ = (
    'Validation', 'MotionValidation',
    'Modification',
    'Checker', 'CharaChecker', 'EnvChecker',
    'Unknown',
)


# logger = MtkLog(__name__)


def checker():
    win = Checker()
    win.show()


# ---------------------------------------
# 動作確認後、ここから下は消す
# ---------------------------------------
# def chara_checker():
#     u"""main"""
#     logger.debug(u'CharaChecker')
#     logger.usage()

#     win = CharaChecker()
#     win.show()


# def env_checker():
#     u"""EnvExporter"""
#     logger.debug(u'EnvChecker')
#     logger.usage()

#     win = EnvChecker()
#     win.show()


# def rig_checker():
#     u"""RigChecker"""
#     logger.debug(u'RigChecker')
#     logger.usage()

#     win = RigChecker()
#     win.show()
