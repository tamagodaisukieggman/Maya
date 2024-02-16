# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

import sys

g_all_log_list = None
g_is_print = False
g_encode_type = None
g_indent = 0


# ===============================================
def reset():

    global g_all_log_list
    global g_is_print
    global g_encode_type
    global g_indent

    g_all_log_list = None
    g_is_print = True
    g_encode_type = None
    g_indent = 0


# ===============================================
def write(log=None):

    global g_all_log_list

    if not g_all_log_list:
        g_all_log_list = []

    fix_log = '  ' * g_indent

    if log:
        fix_log += log

    g_all_log_list.append(fix_log)

    if g_is_print:

        if not g_encode_type:
            print(fix_log)
            return

        print(fix_log.encode(g_encode_type))


# ===============================================
def write_warning(log):

    write('WARNING : {0}'.format(log))


# ===============================================
def write_error(log):

    write('ERROR : {0}'.format(log))


# ===============================================
def write_line(type=-1):

    line_char = '#'
    line_length = 4

    if type == 0:

        line_char = '#'
        line_length = 6

    elif type == 1:

        line_char = '*'
        line_length = 5

    elif type == 2:

        line_char = '+'
        line_length = 4

    elif type == 3:

        line_char = '='
        line_length = 3

    elif type == 4:

        line_char = '-'
        line_length = 2

    else:

        line_char = '-'
        line_length = 2

    write(line_char * line_length * 10)


# ===============================================
def get_log():

    result = ''

    if g_all_log_list:

        for p in range(0, len(g_all_log_list)):

            result += g_all_log_list[p]

            if p != len(g_all_log_list) - 1:
                if sys.version_info.major == 3:
                    result += '\n'
                else:
                    result += u'\r\n'

    if not g_encode_type:
        return result

    return result.encode(g_encode_type)


# ===============================================
def output_log(output_file_path):

    this_log = get_log()

    output_file = open(output_file_path, 'w')

    output_file.write(this_log)

    output_file.close()


# ===============================================
def clear_log():

    global g_all_log_list

    g_all_log_list = None


# ===============================================
def is_print(is_print):

    global g_is_print

    g_is_print = is_print


# ===============================================
def set_encode_type(encode_type):

    global g_encode_type

    g_encode_type = encode_type


# ===============================================
def set_indent(indent):

    global g_indent

    g_indent = indent
