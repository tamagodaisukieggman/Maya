# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


def add_namespace_to_ln(long_name, namespace):
    """
    渡されたlongnameにnamespaceを付与して返す
    """

    renewal_path = ''
    for name_parts in long_name.split('|'):
        if not namespace == '':
            renewal_path += '|{0}:{1}'.format(namespace, name_parts)
        else:
            renewal_path += '|{0}'.format(name_parts)

    return renewal_path
