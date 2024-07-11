# -*- coding=utf-8 -*-
# https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=50413795

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import json
import os.path
# import cerberus

if __name__ == "__main__":
    pass
"""
# config.json
[
  {"name": "none", "label": u"なし", "color": [0.05, 0.05, 0.05]},
]
"""
CONFIG_PATH = os.path.join(os.path.split(__file__)[0], 'config.json')


def read():
    print(CONFIG_PATH)

    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        try:
            data_sets = json.load(config_file)

        except ValueError as jsn_err:
            print(jsn_err)
            return None

        else:

            # Validation of dictionary keys
            for index, data in enumerate(data_sets):

                if data.keys() != {'name', 'label', 'color', 'enable'}:
                    data_sets.pop(index)

            return data_sets
