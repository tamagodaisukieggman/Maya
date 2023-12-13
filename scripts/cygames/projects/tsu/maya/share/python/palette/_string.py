# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re


def _convertCtoS(text=''):
    return re.sub("([A-Z])",lambda x:"_" + x.group(1).lower(), text)


def _convertStoC(text=''):
    return re.sub("_(.)",lambda x:x.group(1).upper(), text)


def _convertCtoL(text=''):
    tmp = re.sub("([A-Z])",lambda x:" " + x.group(1), text)
    return '{0}{1}'.format(tmp[0].upper(), tmp[1:])







