# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import argparse
import sys

from ..base_common import classes as base_class

from . import constants
from . import commands
from . import chara_exporter
from . import gui

try:
    # maya 2022-
    from builtins import str
    from importlib import reload
except Exception:
    pass

reload(base_class)
reload(constants)
reload(commands)
reload(chara_exporter)
reload(gui)


def show_ui():

    this_main = gui.MainWindow()
    this_main.create_ui()


def export(
        target_files=[],
        target_objects=[],
        show_in_exprorer=False,
        keep_temp_file=False,
        output_log=False,
        is_ascii=False,
        is_icon_model=False,
        export_base_setting=False,
        export_bodydiff_ids=[],
        body_shape_check_enabled=False):

    # ログ準備
    logger = base_class.logger.Logger()
    logger.clear_log()
    logger.print_log = True
    logger.encode_type = 'shift_jis'

    logger.write_log('######')
    logger.write_log(u'{0} バージョン {1}'.format(constants.TOOL_NAME, constants.TOOL_VERSION))
    logger.write_log('######')
    logger.write_log()

    try:
        for target_file in target_files:

            exporter = chara_exporter.CharaExporter(target_file)

            exporter.logger = logger
            exporter.export_target_list = target_objects
            exporter.is_ascii = is_ascii
            exporter.is_icon_model = is_icon_model
            exporter.keep_temp_file = keep_temp_file
            exporter.show_in_explorer = show_in_exprorer
            exporter.export_base_setting = export_base_setting
            exporter.export_bodydiff_id_list = export_bodydiff_ids
            exporter.body_shape_check_enabled = body_shape_check_enabled

            exporter.export()

        # ログ表示
        if output_log:
            commands.output_log_file(logger)

    except Exception:
        logger.write_log(str(sys.exc_info()))
        # ログ表示
        commands.output_log_file(logger)
        raise


if __name__ == '__main__':
    from maya import standalone
    standalone.initialize()

    parser = argparse.ArgumentParser()
    parser.add_argument('--target_files', required=True, nargs='*', default=[])
    parser.add_argument('--target_objects', nargs='*', default=[])
    parser.add_argument('--show_in_exprorer', action='store_true')
    parser.add_argument('--keep_temp_file', action='store_true')
    parser.add_argument('--output_log', action='store_true')
    parser.add_argument('--is_ascii', action='store_true')
    parser.add_argument('--is_icon_model', action='store_true')
    parser.add_argument('--export_base_setting', action='store_true')
    parser.add_argument('--export_bodydiff_ids', nargs='*', default=[])
    parser.add_argument('--body_shape_check_enabled', action='store_true')

    export(**vars(parser.parse_args()))
