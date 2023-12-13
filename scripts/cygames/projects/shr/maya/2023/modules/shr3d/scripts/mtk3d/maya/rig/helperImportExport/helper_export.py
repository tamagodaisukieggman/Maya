"""
export helper joints attributes and values in json format
"""

import json

import maya.cmds as mc


def main(filePath, fileName):
    # dict base
    poses = []

    # get export joints
    sel = mc.ls(sl=True, l=True)

    # get userDefinedAttribute and values
    for i in sel:
        # get helper bone name
        jt = i.split('|')[-1]

        # get helper bone parent
        pars = i.split('|')[1:]

        # get helper node
        hlp_node = getSourceNode(node=jt, attr="EditData")

        # get source joint
        src_jnt = mc.listConnections(hlp_node + ".BaseMatrix", s=True, d=False, c=False)

        # get helper bone attributes and value
        attr = mc.listAttr(i, ud=True)
        attr_and_val = {}
        num = len(attr)
        for j in range(num):
            val = mc.getAttr(i + '.' + attr[j])
            otherdict = {attr[j]: val}
            attr_and_val.update(otherdict)

        # get helper bone worldMatrix
        mat = mc.getAttr(i + '.worldMatrix')

        # add attributes to dict
        d = {}
        d.update(helperJoint=jt)
        d.update(attributes=attr_and_val)
        d.update(hierarchyLevel=len(pars))
        d.update(worldMatrix=mat)
        d.update(parentSpace=pars[-2])
        d.update(type=mc.nodeType(sel[0]))
        d.update(sourceJoint=src_jnt[0])

        poses.append(d)

    # ------------------------------------------------------------------------------------------------------------------
    print filePath + fileName
    saveFile(filePath, fileName, poses)


# list attr
def getSourceNode(node, attr):
    global src_node
    node_list = mc.listConnections(node, s=True, p=True)
    src_num = len(node_list)

    for i in range(src_num):
        nd = node_list[i].split(".")
        if nd[1] == attr:
            src_node = nd[0]
        else:
            pass
    return src_node


# export json
def saveFile(filePath, fileName, d):
    f = filePath + fileName + '.json'
    fp = open(f, 'w')
    json.dump(d, fp, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
