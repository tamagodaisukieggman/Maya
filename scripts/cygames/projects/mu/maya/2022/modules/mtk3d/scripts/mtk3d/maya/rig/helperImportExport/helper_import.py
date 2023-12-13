"""
import helper joints attributes and values in json format
"""
import json

import maya.cmds as mc
import maya.mel as mm


def main(filePath, fileName):
    # import json file
    print filePath + fileName
    with open(filePath + fileName + ".json") as f:
        jsn = json.load(f)

    # --------------------------------------------------------------------------------------------------------------#
    # hierarchy sort
    num = len(jsn)
    for i in range(num):
        jsn.sort(key=lambda x: x['hierarchyLevel'])

    # --------------------------------------------------------------------------------------------------------------#
    # make joint

    for i in range(num):
        name = jsn[i]["helperJoint"]
        source_joint = jsn[i]["sourceJoint"]

        # attr and value
        attr = jsn[i]["attributes"]

        if not mc.objExists(name):
            helper_bone = mc.joint(n=name)
            parent_space = jsn[i]["parentSpace"]
            mc.parent(helper_bone, parent_space)

            mc.setAttr(helper_bone + ".overrideEnabled", True)
            mc.setAttr(helper_bone + ".overrideColorRGB", *[0.0, 0.14, 0.35])
            mc.setAttr(helper_bone + ".overrideRGBColors", 1)

            # ---------------------------------------------------------------------------------------------------------#
            # make and connect helper node
            makeHelperJoint(helper_bone, source_joint)

        # set value

        attrs = jsn[i]["attributes"]
        attrNums = len(jsn[i]["attributes"])

        for attr, vals in attrs.items():
            if type(vals) == list:
                try:
                    mc.setAttr(name + "." + attr, *vals[0])
                except:
                    pass
            elif type(vals) == unicode:
                try:
                    mc.setAttr(name + "." + attr, vals, type="string")
                except:
                    pass
            else:
                try:
                    mc.setAttr(name + "." + attr, vals)
                    print attr
                except:
                    pass


def makeHelperJoint(helper_bone, source_joint):
    mm.eval("setHelperBoneNode {} {}".format(helper_bone, source_joint))


if __name__ == '__main__':
    main()
