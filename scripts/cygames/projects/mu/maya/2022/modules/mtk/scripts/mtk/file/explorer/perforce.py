import os

from PySide2.QtGui import QIcon
from pathlib import Path

try:
    import maya.cmds as cmds
    if hasattr(cmds, 'about'):
        MODE = 'MAYA'
    else:
        MODE = 'STANDALONE'
except ImportError:
    MODE = 'STANDALONE'

import logging
logger = logging.getLogger(__name__)

class MtkExplorerPerforceStatusIconProvider(object):
    base_path = Path(os.path.dirname(__file__))

    # icon
    icon_none = QIcon(str(base_path.joinpath('images/perforce/status/none.png')))
    icon_add = QIcon(str(base_path.joinpath('images/perforce/status/add.png')))
    icon_checkout = QIcon(str(base_path.joinpath('images/perforce/status/checkout.png')))
    icon_other = QIcon(str(base_path.joinpath('images/perforce/status/other.png')))
    icon_latest = QIcon(str(base_path.joinpath('images/perforce/status/latest.png')))
    icon_stale = QIcon(str(base_path.joinpath('images/perforce/status/stale.png')))

    p4_action_icons = {
        'add': icon_add,
        'other': icon_other,
        'checkout': icon_checkout,
        'stale': icon_stale,
        'latest': icon_latest,
        'none': icon_none,
    }

    @classmethod
    def status_icon(cls, p4_action_status):
        icon = cls.p4_action_icons['none']
        if p4_action_status in cls.p4_action_icons:
            icon = cls.p4_action_icons[p4_action_status]
        return icon
