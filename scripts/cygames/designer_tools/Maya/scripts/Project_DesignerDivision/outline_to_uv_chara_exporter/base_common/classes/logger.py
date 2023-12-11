# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import sys


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Logger(object):

    # ===============================================
    def __init__(self):

        self.__all_log_list = None

        self.print_log = False
        self.encode_type = None

        self.clear_log()

    # ===============================================
    def clear_log(self):

        self.__all_log_list = []

    # ===============================================
    def get_log(self):

        result = ''

        if self.__all_log_list:
            for cnt in range(0, len(self.__all_log_list)):

                result += self.__all_log_list[cnt]

                if cnt != len(self.__all_log_list) - 1:
                    result += u'\r\n'

        if self.encode_type is None:
            return result

        if sys.version_info.major == 2:
            return result.encode(self.encode_type)
        else:
            # Python3だとエンコーディングは自動
            # encodeしてbytesを返すとfile.write()でエラーになる
            return result

    # ===============================================
    def output_log(self, target_file_path):

        this_log = self.get_log()

        output_file = open(target_file_path, 'w')

        output_file.write(this_log)

        output_file.close()

    # ===============================================
    def write_log(self, log=''):

        self.__all_log_list.append(log)

        if self.print_log:

            if self.encode_type is None:
                print(log)
                return

            print(log.encode(self.encode_type))

    # ===============================================
    def write_warning(self, log):

        self.write_log('WARNING : {0}'.format(log))

    # ===============================================
    def write_error(self, log):

        self.write_log('ERROR : {0}'.format(log))
