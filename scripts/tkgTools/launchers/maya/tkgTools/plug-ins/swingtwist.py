# -*- coding: utf-8 -*-
"""SwingTwist is a dependency graph node that decomposes the local rotation of a transform to drive the rotation of
another transform allowing the user to scale the swing and twist components of the local rotation.

To create the node, select the driver, then the driven and run cmds.swingTwist(name='swingTwistNodeName')

node = cmds.swingTwist(driver, driven, name='nodeName')
"""

# import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as om2
import maya.api.OpenMayaUI as omui2
import maya.cmds as cmds

import math

def maya_useNewAPI():
    pass

def slerp(qa, qb, t):
    """Calculates the quaternion slerp between two quaternions.

    From: http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/slerp/index.htm

    :param qa: Start MQuaternion.
    :param qb: End MQuaternion.
    :param t: Parameter between 0.0 and 1.0
    :return: An MQuaternion interpolated between qa and qb.
    """
    qm = om2.MQuaternion()

    # Calculate angle between them.
    cos_half_theta = qa.w * qb.w + qa.x * qb.x + qa.y * qb.y + qa.z * qb.z
    # if qa == qb or qa == -qb then theta = 0 and we can return qa
    if abs(cos_half_theta) >= 1.0:
        qm.w = qa.w
        qm.x = qa.x
        qm.y = qa.y
        qm.z = qa.z
        return qa

    # Calculate temporary values
    half_theta = math.acos(cos_half_theta)
    sin_half_theta = math.sqrt(1.0 - cos_half_theta * cos_half_theta)
    # if theta = 180 degrees then result is not fully defined
    # we could rotate around any axis normal to qa or qb
    if math.fabs(sin_half_theta) < 0.001:
        qm.w = (qa.w * 0.5 + qb.w * 0.5)
        qm.x = (qa.x * 0.5 + qb.x * 0.5)
        qm.y = (qa.y * 0.5 + qb.y * 0.5)
        qm.z = (qa.z * 0.5 + qb.z * 0.5)
        return qm

    ratio_a = math.sin((1 - t) * half_theta) / sin_half_theta
    ratio_b = math.sin(t * half_theta) / sin_half_theta
    # Calculate quaternion
    qm.w = (qa.w * ratio_a + qb.w * ratio_b)
    qm.x = (qa.x * ratio_a + qb.x * ratio_b)
    qm.y = (qa.y * ratio_a + qb.y * ratio_b)
    qm.z = (qa.z * ratio_a + qb.z * ratio_b)
    return qm

def create_matrix(mat):
    new_mat = []
    item = []
    for i, row in enumerate(mat):
        item.append(row)
        if i in [3, 7, 11, 15]:
            new_mat.append(item)
            item = []
    return new_mat


class SwingTwistNode(om2.MPxNode):
    TYPE_NAME = 'swingTwist'
    # TYPE_ID = om2.MTypeId(0x00115817)
    TYPE_ID = om2.MTypeId(0x00935728)

    output_rotation = om2.MObject()
    output_rotation_x = om2.MObject()
    output_rotation_y = om2.MObject()
    output_rotation_z = om2.MObject()
    matrix = om2.MObject()
    twist_weight = om2.MObject()
    swing_weight = om2.MObject()
    twist_axis = om2.MObject()
    rotate_axis = om2.MObject()
    rotate_axis_x = om2.MObject()
    rotate_axis_y = om2.MObject()
    rotate_axis_z = om2.MObject()
    joint_orient = om2.MObject()
    joint_orient_x = om2.MObject()
    joint_orient_y = om2.MObject()
    joint_orient_z = om2.MObject()
    rotate_order = om2.MObject()

    swing_axis_list = {
        0:om2.MVector.kXaxisVector,
        1:om2.MVector.kYaxisVector,
        2:om2.MVector.kZaxisVector,
    }


    twist_axis_list = {
        0:om2.MVector.kYaxisVector,
        1:om2.MVector.kZaxisVector,
        2:om2.MVector.kXaxisVector,
    }

    rotation_order = {
        0:om2.MEulerRotation.kXYZ,
        1:om2.MEulerRotation.kYZX,
        2:om2.MEulerRotation.kZXY,
        3:om2.MEulerRotation.kXZY,
        4:om2.MEulerRotation.kYXZ,
        5:om2.MEulerRotation.kZYX,
    }

    @classmethod
    def creator(cls):
        return SwingTwistNode()

    @classmethod
    def initialize(cls):
        e_attr = om2.MFnEnumAttribute()
        m_attr = om2.MFnMatrixAttribute()
        n_attr = om2.MFnNumericAttribute()
        u_attr = om2.MFnUnitAttribute()

        cls.output_rotation_x = u_attr.create('outRotateX', 'outRotateX', om2.MFnUnitAttribute.kAngle)
        u_attr.writable = False
        u_attr.storable = False

        cls.output_rotation_y = u_attr.create('outRotateY', 'outRotateY', om2.MFnUnitAttribute.kAngle)
        u_attr.writable = False
        u_attr.storable = False

        cls.output_rotation_z = u_attr.create('outRotateZ', 'outRotateZ', om2.MFnUnitAttribute.kAngle)
        u_attr.writable = False
        u_attr.storable = False

        cls.output_rotation = n_attr.create('outRotate', 'outRotate',
                                            cls.output_rotation_x, cls.output_rotation_y, cls.output_rotation_z)
        n_attr.writable = False
        n_attr.storable = False
        cls.addAttribute(cls.output_rotation)

        cls.twist_weight = n_attr.create('twist', 'twist', om2.MFnNumericData.kFloat, 1.0)
        n_attr.keyable = True
        n_attr.setMin(-1.0)
        n_attr.setMax(1.0)
        cls.addAttribute(cls.twist_weight)
        cls.attribute_affects(cls.twist_weight)

        cls.swing_weight = n_attr.create('swing', 'swing', om2.MFnNumericData.kFloat, 1.0)
        n_attr.keyable = True
        n_attr.setMin(-1.0)
        n_attr.setMax(1.0)
        cls.addAttribute(cls.swing_weight)
        cls.attribute_affects(cls.swing_weight)

        cls.twist_axis = e_attr.create('twistAxis', 'twistAxis')
        e_attr.keyable = True
        e_attr.addField('X Axis', 0)
        e_attr.addField('Y Axis', 1)
        e_attr.addField('Z Axis', 2)
        cls.addAttribute(cls.twist_axis)
        cls.attribute_affects(cls.twist_axis)

        cls.matrix = m_attr.create('matrix', 'matrix')
        cls.addAttribute(cls.matrix)
        cls.attribute_affects(cls.matrix)

        cls.joint_orient_x = u_attr.create('jointOrientX', 'jointOrientX', om2.MFnUnitAttribute.kAngle)
        cls.joint_orient_y = u_attr.create('jointOrientY', 'jointOrientY', om2.MFnUnitAttribute.kAngle)
        cls.joint_orient_z = u_attr.create('jointOrientZ', 'jointOrientZ', om2.MFnUnitAttribute.kAngle)
        cls.joint_orient = n_attr.create('jointOrient', 'jointOrient',
                                         cls.joint_orient_x, cls.joint_orient_y, cls.joint_orient_z)
        cls.addAttribute(cls.joint_orient)
        cls.attribute_affects(cls.joint_orient)

        cls.rotate_axis_x = u_attr.create('rotateAxisX', 'rotateAxisX', om2.MFnUnitAttribute.kAngle)
        cls.rotate_axis_y = u_attr.create('rotateAxisY', 'rotateAxisY', om2.MFnUnitAttribute.kAngle)
        cls.rotate_axis_z = u_attr.create('rotateAxisZ', 'rotateAxisZ', om2.MFnUnitAttribute.kAngle)
        cls.rotate_axis = n_attr.create('rotateAxis', 'rotateAxis',
                                        cls.rotate_axis_x, cls.rotate_axis_y, cls.rotate_axis_z)
        cls.addAttribute(cls.rotate_axis)
        cls.attribute_affects(cls.rotate_axis)

        cls.rotate_order = e_attr.create('rotateOrder', 'rotateOrder')
        e_attr.addField('XYZ', 0)
        e_attr.addField('YZX', 1)
        e_attr.addField('ZXY', 2)
        e_attr.addField('XZY', 3)
        e_attr.addField('YXZ', 4)
        e_attr.addField('ZYX', 5)
        cls.addAttribute(cls.rotate_order)
        cls.attribute_affects(cls.rotate_order)

    @classmethod
    def attribute_affects(cls, attribute):
        cls.attributeAffects(attribute, cls.output_rotation_x)
        cls.attributeAffects(attribute, cls.output_rotation_y)
        cls.attributeAffects(attribute, cls.output_rotation_z)
        cls.attributeAffects(attribute, cls.output_rotation)

    def __init__(self):
        om2.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug != self.output_rotation and plug.parent() != self.output_rotation:
            return om2.kUnknownParameter

        # Get the input data
        matrix = data.inputValue(self.matrix).asMatrix()
        twist_weight = data.inputValue(self.twist_weight).asFloat()
        swing_weight = data.inputValue(self.swing_weight).asFloat()
        twist_axis = data.inputValue(self.twist_axis).asShort()
        rotate_order = data.inputValue(self.rotate_order).asShort()
        h_joint_orient = data.inputValue(self.joint_orient)
        h_rotate_axis = data.inputValue(self.rotate_axis)
        joint_orient = [h_joint_orient.child(x).asAngle().asDegrees() for x in [self.joint_orient_x, self.joint_orient_y, self.joint_orient_z]]
        rotate_axis = [h_rotate_axis.child(x).asAngle().asDegrees() for x in [self.rotate_axis_x, self.rotate_axis_y, self.rotate_axis_z]]

        ##########################################################
        # CallBack用
        # matrix = om2.MMatrix(cmds.getAttr(source_obj + '.matrix'))
        # twist_weight = cmds.getAttr(source_obj + '.twistWeight')
        # swing_weight = cmds.getAttr(source_obj + '.swingWeight')
        # twist_axis = cmds.getAttr(source_obj + '.twistAxis')
        # rotate_order = cmds.getAttr(source_obj + '.ro')
        # joint_orient = cmds.getAttr(source_obj + '.jo')[0]
        # rotate_axis = cmds.getAttr(source_obj + '.ra')[0]
        ##########################################################

        # Get the input rotation quaternion
        rotation = om2.MTransformationMatrix(matrix).rotation().asQuaternion()

        # Take out the joint orient and rotate axis from the rotation quaternion
        # joint_orient = [math.radians(x) for x in joint_orient]
        # joint_orient = om2.MEulerRotation([math.radians(x) for x in joint_orient])
        joint_orient = om2.MEulerRotation([math.radians(x) for x in joint_orient]).asQuaternion()

        # rotate_axis = [math.radians(x) for x in rotate_axis]
        # rotate_axis = om2.MEulerRotation([math.radians(x) for x in rotate_axis])
        rotate_axis = om2.MEulerRotation([math.radians(x) for x in rotate_axis]).asQuaternion()

        rotation = rotate_axis.inverse() * rotation * joint_orient.inverse()
        rotation_matrix = create_matrix(rotation.asMatrix())

        # Calculate swing
        target_vector = [om2.MVector(rotation_matrix[x][0], rotation_matrix[x][1], rotation_matrix[x][2]) for x in range(3)][twist_axis]
        reference_vector = self.swing_axis_list[twist_axis]
        swing = reference_vector.rotateTo(target_vector)

        twist = rotation * swing.inverse()
        twist_matrix = create_matrix(twist.asMatrix())
        # Calculate twist
        target_vector = [om2.MVector(twist_matrix[x][0], twist_matrix[x][1], twist_matrix[x][2]) for x in [1, 2, 0]][twist_axis]
        reference_vector = self.twist_axis_list[twist_axis]
        twist = reference_vector.rotateTo(target_vector)

        # Scale by the input weights
        rest = om2.MQuaternion()
        swing = slerp(rest, swing, abs(swing_weight))
        twist = slerp(rest, twist, abs(twist_weight))

        # Process any inversion
        if twist_weight < 0.0:
            twist.invertIt()
        if swing_weight < 0.0:
            swing.invertIt()

        out_rotation = twist * swing
        # Convert the rotation to euler
        euler = out_rotation.asEulerRotation()
        euler.reorderIt(self.rotation_order[rotate_order])
        # rx = math.degrees(euler.x)
        # ry = math.degrees(euler.y)
        # rz = math.degrees(euler.z)

        rx, ry, rz = math.degrees(euler.x), math.degrees(euler.y), math.degrees(euler.z)

        # CallBack用
        # cmds.setAttr(drv_obj + '.r', *[rx, ry, rz])

        # Set the output
        h_out = data.outputValue(self.output_rotation)
        for rot, attr in zip([rx, ry, rz], [self.output_rotation_x, self.output_rotation_y, self.output_rotation_z]):
            angle = om2.MAngle(rot, om2.MAngle.kDegrees)
            handle = h_out.child(attr)
            handle.setMAngle(angle)
            handle.setClean()

        h_out.setClean()
        data.setClean(plug)


def initializePlugin(plugin):
    vendor = "Shunsuke Takagi"
    version = "0.0.1"

    plugin_fn = om2.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(SwingTwistNode.TYPE_NAME,
                               SwingTwistNode.TYPE_ID,
                               SwingTwistNode.creator,
                               SwingTwistNode.initialize,
                               om2.MPxNode.kDependNode)
    except Exception as e:
        print(e)
        om2.MGlobal.displayError("Failed to register node: {0}".format(SwingTwistNode.TYPE_NAME))
        raise

    # cmds.setNodeTypeFlag('tkgmultiattrblendnode', threadSafe=True)

def uninitializePlugin(plugin):
    plugin_fn = om2.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(SwingTwistNode.TYPE_ID)
    except:
        om2.MGlobal.displayError("Failed to deregister node: {0}".format(SwingTwistNode.TYPE_NAME))
        raise





# def initializePlugin(obj):
#     mplugin = OpenMaya.MFnPlugin(obj)
#
#     try:
#         mplugin.registerNode('swingTwist', SwingTwistNode.id, SwingTwistNode.creator,
#                              SwingTwistNode.initialize, OpenMaya.MPxNode.kDependNode)
#     except:
#         sys.stderr.write('Faled to register node: %s' % 'swingTwist')
#         raise
#
# # プラグインを終了する際にMayaから呼ばれる関数
# def uninitializePlugin(mobject):
#     mplugin = OpenMaya.MFnPlugin(mobject)
#     try:
#         mplugin.deregisterNode(SwingTwistNode.id)
#     except:
#         sys.stderr.write('Faled to uninitialize node: %s' % 'swingTwist')
#         raise





# if __name__ == "__main__":
#     cmds.file(new=1, f=1)
#     plugin_name = "swingtwist.py"
#     cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
#     cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))


# path = 'C:/Users/kesun/Desktop'
#
# pluginPath=os.environ.get('MAYA_PLUG_IN_PATH')
# if not path in pluginPath:
#     os.environ['MAYA_PLUG_IN_PATH']+='%s%s' % (os.pathsep,path)
#
# plugin_name = '{0}/swingtwist.py'.format(path)
# cmds.loadPlugin("{0}".format(plugin_name), qt=1)
