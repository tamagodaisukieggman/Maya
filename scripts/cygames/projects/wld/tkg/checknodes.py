import codecs
import json
import math
import os
from collections import OrderedDict

from maya import cmds, mel


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


def json_transfer(fileName=None, operation=None, export_values=None):
    if operation == 'export':
        with codecs.open(fileName, 'w', encoding='utf-8') as f:
            json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        with codecs.open(fileName, 'r', encoding='utf-8') as f:
            return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)


# export dag_nodes
check_node_types = ['displayLayer', 'transform', 'objectSet']
export_exists_nodes = cmds.ls(type=check_node_types)
export_exists_nodes = list(set(export_exists_nodes))
export_exists_nodes.sort()
dag_nodes = []
for obj in export_exists_nodes:
    if not obj in dag_nodes:
        dag_nodes.append(obj)

check_nodes_dict = OrderedDict()
check_nodes_dict['checknodes'] = dag_nodes


# check precision
round_digit = 3
check_round_attrs = OrderedDict()
not_round_attrs = []
fix_attr = True
exempt_nodes = ['persp', 'top', 'front', 'side']
for obj in dag_nodes:
    if obj in exempt_nodes:
        continue

    listAttrs = cmds.listAttr(obj, k=1) or None
    if not listAttrs:
        continue

    for at in listAttrs:
        obj_at = '{}.{}'.format(obj, at)
        try:
            get_at = cmds.getAttr(obj_at)
        except Exception as e:
            continue

        if type(get_at) == float:
            round_get_at = truncate(round(get_at, round_digit), round_digit)
            if get_at != round_get_at:
                not_round_attrs.append([obj_at, get_at, round_get_at])

check_round_attrs['attrs'] = not_round_attrs

if fix_attr:
    for nra in check_round_attrs['attrs']:
        cmds.setAttr(nra[0], nra[2])



file_path = 'C:/Users/{}/Documents/maya/scripts/tkgTools/tkgRig/data/projects/www/scripts/checknodes.json'.format(os.getenv('USER'))

json_transfer(fileName=file_path, operation='export', export_values=check_nodes_dict)

# import
not_exist_nodes = [obj for obj in dag_nodes if not cmds.objExists(obj)]
print(not_exist_nodes)
