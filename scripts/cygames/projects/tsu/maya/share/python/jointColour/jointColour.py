from maya import cmds
from functools import partial


#############################################################################
# getExtraJoints
def getExtraJoints(*args):
    a_joints = cmds.ls("_a*", shortNames=True, type="joint")
    c_joints = cmds.ls("_c*", shortNames=True, type="joint")
    d_joints = cmds.ls("_d*", shortNames=True, type="joint")
    e_joints = cmds.ls("_e*", shortNames=True, type="joint")
    f_joints = cmds.ls("_f*", shortNames=True, type="joint")

    return a_joints, c_joints, d_joints, e_joints, f_joints
##################################edit
# Select joints
def selectJoints(*args):
    extraJoints = getExtraJoints()
    checked_cb_list = []
    cblist = ["checkbox_a_joints", "checkbox_c_joints", "checkbox_d_joints", "checkbox_e_joints", "checkbox_f_joints"]
    for i in range(len(cblist)):
        if cmds.checkBox(cblist[i], q=True, value=args[0]):
            checked_cb_list.append(extraJoints[i])
    checked_cb_list = sum(checked_cb_list, [])
    print(checked_cb_list)
    cmds.select(checked_cb_list)


# Deselect joints
def deselectJoints(*args):
    extraJoints = getExtraJoints()
    checked_cb_list = []
    cblist = ["checkbox_a_joints", "checkbox_c_joints", "checkbox_d_joints", "checkbox_e_joints", "checkbox_f_joints"]
    for i in range(len(cblist)):
        if cmds.checkBox(cblist[i], q=True, value=False):
            checked_cb_list.append(extraJoints[i])
    checked_cb_list = sum(checked_cb_list, [])
    print(checked_cb_list)
    cmds.select(checked_cb_list)


# All
def joint_colours(*args):
    a_joints, c_joints, d_joints, e_joints, f_joints = getExtraJoints()
    for a_joint in a_joints:
        cmds.setAttr(a_joint + ".overrideEnabled", 1)
        cmds.color(a_joint, rgb=(1, 0, 0))

    for c_joint in c_joints:
        cmds.setAttr(c_joint + ".overrideEnabled", 1)
        cmds.color(c_joint, rgb=(1, 0, 1))

    for d_joint in d_joints:
        cmds.setAttr(d_joint + ".overrideEnabled", 1)
        cmds.color(d_joint, rgb=(0, 1, 1))

    for e_joint in e_joints:
        cmds.setAttr(e_joint + ".overrideEnabled", 1)
        cmds.color(e_joint, rgb=(1, 0, 1))

    for f_joint in f_joints:
        cmds.setAttr(f_joint + ".overrideEnabled", 1)
        cmds.color(f_joint, rgb=(0, 1, 1))


# All Outliner
def autoOutliner(*args):
    a_joints, c_joints, d_joints, e_joints, f_joints = getExtraJoints()

    for a_joint in a_joints:
        cmds.setAttr(a_joint + ".useOutlinerColor", 1)
        cmds.setAttr(a_joint + ".outlinerColor", 1, 0, 0)

    for c_joint in c_joints:
        cmds.setAttr(c_joint + ".useOutlinerColor", 1)
        cmds.setAttr(c_joint + ".outlinerColor", 1, 0, 1)

    for d_joint in d_joints:
        cmds.setAttr(d_joint + ".useOutlinerColor", 1)
        cmds.setAttr(d_joint + ".outlinerColor", 0, 1, 1)

    for e_joint in e_joints:
        cmds.setAttr(e_joint + ".useOutlinerColor", 1)
        cmds.setAttr(e_joint + ".outlinerColor", 1, 0, 1)

    for f_joint in f_joints:
        cmds.setAttr(f_joint + ".useOutlinerColor", 1)
        cmds.setAttr(f_joint + ".outlinerColor", 0, 1, 1)

    cmds.select(a_joints)
    cmds.select(d=True)


############Checkbox funcs#################################################################
# Select all cmd
def checkAll(*args):
    cmds.checkBox("checkbox_a_joints", e=True, value=True)
    cmds.checkBox("checkbox_c_joints", e=True, value=True)
    cmds.checkBox("checkbox_d_joints", e=True, value=True)
    cmds.checkBox("checkbox_e_joints", e=True, value=True)
    cmds.checkBox("checkbox_f_joints", e=True, value=True)
    return selectJoints(True)


# Deselect all cmd
def deselectAll(*args):
    cmds.checkBox("checkbox_a_joints", e=True, value=False)
    cmds.checkBox("checkbox_c_joints", e=True, value=False)
    cmds.checkBox("checkbox_d_joints", e=True, value=False)
    cmds.checkBox("checkbox_e_joints", e=True, value=False)
    cmds.checkBox("checkbox_f_joints", e=True, value=False)
    cmds.select(deselect=True)


#####################################################################################################
# Set Colour &  Outliner
def setColour(col, mode,*args):
    extraJoints = getExtraJoints()
    checked_cb_list = []
    cblist = ["checkbox_a_joints", "checkbox_c_joints", "checkbox_d_joints", "checkbox_e_joints", "checkbox_f_joints"]
    # for cb, ex_j in zip(cblist, extraJoints):
    for i in range(len(cblist)):
        if cmds.checkBox(cblist[i], q=True, value=True):
            checked_cb_list.append(extraJoints[i])
    checked_cb_list = sum(checked_cb_list, [])

    for checked_cb in checked_cb_list:
        if mode == 1:
            cmds.setAttr(checked_cb + ".overrideEnabled", 1)
            cmds.color(checked_cb, rgb=col)

        if mode == 2:
            cmds.setAttr(checked_cb + ".useOutlinerColor", 1)
            cmds.setAttr(checked_cb + ".outlinerColor", col[0], col[1], col[2])
            cmds.select(extraJoints[0])
            cmds.select(d=True)


###########################################################################################
# outliner reset all
def resetOutlinerColour(*args):
    extraJoints = getExtraJoints()
    listA = []
    for i in range(len(extraJoints)):
        listA.append(extraJoints[i])
    listA = sum(listA, [])
    for i in listA:
        cmds.setAttr(i + ".useOutlinerColor", 0)
        cmds.select(extraJoints[0])
        cmds.select(d=True)


# outliner reset selected
def outlinerResetSelected(*args):
    extraJoints = getExtraJoints()
    checked_cb_list = []
    cblist = ["checkbox_a_joints", "checkbox_c_joints", "checkbox_d_joints", "checkbox_e_joints", "checkbox_f_joints"]
    for i in range(len(cblist)):
        if cmds.checkBox(cblist[i], q=True, value=True):
            checked_cb_list.append(extraJoints[i])
    checked_cb_list = sum(checked_cb_list, [])

    for checked_cb in checked_cb_list:
        cmds.setAttr(checked_cb + ".useOutlinerColor", 0)
        cmds.select(extraJoints[0])
        cmds.select(d=True)


# Joint reset all

def jointReset(*args):
    extraJoints = getExtraJoints()
    listA = []
    for i in range(len(extraJoints)):
        listA.append(extraJoints[i])
    listA = sum(listA, [])
    for i in listA:
        cmds.color(listA)


# Joint reset selected
def jointResetSelected(*args):
    extraJoints = getExtraJoints()
    checked_cb_list = []
    cblist = ["checkbox_a_joints", "checkbox_c_joints", "checkbox_d_joints", "checkbox_e_joints", "checkbox_f_joints"]
    for i in range(len(cblist)):
        if cmds.checkBox(cblist[i], q=True, value=True):
            checked_cb_list.append(extraJoints[i])
    checked_cb_list = sum(checked_cb_list, [])

    for checked_cb in checked_cb_list:
        cmds.setAttr(checked_cb + ".overrideEnabled", 1)
        cmds.color(checked_cb)


#####################################################################################
# UI
def ui():
    if cmds.window('JointColour_Window', ex=True):
        cmds.deleteUI('JointColour_Window')

    cmds.window('JointColour_Window', title="JointColour", sizeable=True)
    cmds.columnLayout(adjustableColumn=False, parent='JointColour_Window', rs=5, co=("left", 2))
    cmds.text(label="Auto Colour", font="boldLabelFont", align="left")
    cmds.rowLayout(numberOfColumns=5, parent='JointColour_Window', columnAlign=(1, "left"))
    cmds.button(label="Joint", command=partial(joint_colours))
    cmds.button(label="Outliner", command=partial(autoOutliner))

    cmds.columnLayout(adjustableColumn=True, parent='JointColour_Window')
    cmds.text(label="Select Joints", font="boldLabelFont", align="left")

    button_layout4 = cmds.rowLayout(numberOfColumns=6, parent='JointColour_Window', columnAlign=(1, "left"))
    cmds.checkBox("checkbox_a_joints", label="_a joints", onc=partial(selectJoints, True), ofc=partial(selectJoints, False))
    cmds.checkBox("checkbox_c_joints", label="_c joints", onc=partial(selectJoints, True), ofc=partial(selectJoints, False))
    cmds.checkBox("checkbox_d_joints", label="_d joints", onc=partial(selectJoints, True), ofc=partial(selectJoints, False))
    cmds.checkBox("checkbox_e_joints", label="_e joints", onc=partial(selectJoints, True), ofc=partial(selectJoints, False))
    cmds.checkBox("checkbox_f_joints", label="_f joints", onc=partial(selectJoints, True), ofc=partial(selectJoints, False))

    cmds.columnLayout(adjustableColumn=False, parent='JointColour_Window')

    cmds.rowLayout(numberOfColumns=4, parent='JointColour_Window', columnAlign=(1, "left"))

    cmds.button(label="Select All", command=partial(checkAll))
    cmds.button(label="Deselect All", command=partial(deselectAll))

    cmds.columnLayout(adjustableColumn=False, parent='JointColour_Window')
    cmds.text(label="Set Joint Colour", font="boldLabelFont")
    cmds.rowLayout(numberOfColumns=8, parent='JointColour_Window', columnAlign=(1, "left"))
    cmds.separator()
    cmds.button(label="", command=partial(setColour, (1,0,0), 1), backgroundColor=(1, 0, 0))
    cmds.button(label="", command=partial(setColour, (1,0,1), 1), backgroundColor=(1, 0, 1))
    cmds.button(label="", command=partial(setColour, (0,1,1), 1), backgroundColor=(0, 1, 1))
    cmds.button(label="", command=partial(setColour, (0,1,0), 1), backgroundColor=(0, 1, 0))
    cmds.button(label="", command=partial(setColour, (1,1,0), 1), backgroundColor=(1, 1, 0))

    cmds.columnLayout(adjustableColumn=False, parent='JointColour_Window', rs=5)
    cmds.rowLayout(numberOfColumns=3, parent='JointColour_Window', columnAlign=(1, "left"))
    cmds.button(label="Reset All", command=partial(jointReset))
    cmds.button(label="Reset Selected", command=partial(jointResetSelected))

    cmds.columnLayout(adjustableColumn=False, parent='JointColour_Window', rs=5)
    cmds.text(label="Set Outliner Colour", font="boldLabelFont")
    cmds.rowLayout(numberOfColumns=8, parent='JointColour_Window', columnAlign=(1, "left"))

    cmds.button(label="", command=partial(setColour, (1,0,0), 2), backgroundColor=(1, 0, 0))
    cmds.button(label="", command=partial(setColour, (1,0,1), 2), backgroundColor=(1, 0, 1))
    cmds.button(label="", command=partial(setColour, (0,1,1), 2), backgroundColor=(0, 1, 1))
    cmds.button(label="", command=partial(setColour, (0,1,0), 2), backgroundColor=(0, 1, 0))
    cmds.button(label="", command=partial(setColour, (1,1,0), 2), backgroundColor=(1, 1, 0))
    cmds.columnLayout(adjustableColumn=False, parent='JointColour_Window')
    cmds.rowLayout(numberOfColumns=3, parent='JointColour_Window', columnAlign=(1, "left"))
    cmds.button(label="Reset All", command=partial(resetOutlinerColour))
    cmds.button(label="Reset Selected", command=partial(outlinerResetSelected))
    cmds.showWindow()


ui()