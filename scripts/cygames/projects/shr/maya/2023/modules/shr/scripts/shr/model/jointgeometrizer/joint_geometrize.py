import math

from maya import cmds
import maya.api.OpenMaya as om2


NOT_EXISTS_JOINTS = ["jnt_0000_skl_root", "jnt_mtp", "jnt_cnp", "jnt_move_root"]


class Geometrize(object):
    def __init__(self):
        super(Geometrize, self).__init__()

        self.cylinders = []
        self.spheres = []


    def clean(self):
        if cmds.ls("JointGeometry"):
            cmds.delete("JointGeometry")

        if not self.cylinders or not self.spheres:
            return False

        for cylinder in self.cylinders:
            result = cmds.ls(cylinder[0])
            if not result:
                continue

            cmds.delete(result)

        for sphere in self.spheres:
            result = cmds.ls(sphere[0])
            if not result:
                continue

            cmds.delete(result)


    def geometrize(self, joint, cradius=1, sradius=1):
    
        joint_children = cmds.listRelatives(joint, children=True, path=True)
        if not joint_children:
            return

        _pos1 = om2.MVector(cmds.xform(joint, q=True, t=True, ws=True))

        for joint_child in joint_children:
            _pos2 = om2.MVector(cmds.xform(joint_child, q=True, t=True, ws=True))
            _vec = _pos2 - _pos1
            _axis = om2.MVector([0, 1, 0])
            _pivot = om2.MVector([0, -0.5, 0])

            poly_cylinder_name = "{}_cyl".format(joint_child)
            poly_sphere_name = "{}_sph".format(joint_child)

            poly_cylinder = cmds.polyCylinder(n=poly_cylinder_name, ax=_axis, h=1, r=cradius)
            self.cylinders.append(poly_cylinder)
            poly_sphere = cmds.polySphere(n=poly_sphere_name, r=sradius)
            self.spheres.append(poly_sphere)

            cmds.setAttr("{}.rotatePivot".format(poly_cylinder[0]), *_pivot)
            cmds.setAttr("{}.scalePivot".format(poly_cylinder[0]), *_pivot)
            
            cmds.setAttr("{}.t".format(poly_cylinder[0]), *(_pos1 - _pivot))
            cmds.setAttr("{}.t".format(poly_sphere[0]), *_pos2)

            cmds.setAttr("{}.rx".format(poly_cylinder[0]), math.degrees(_axis.rotateTo(_vec).asEulerRotation().x))
            cmds.setAttr("{}.ry".format(poly_cylinder[0]), math.degrees(_axis.rotateTo(_vec).asEulerRotation().y))
            cmds.setAttr("{}.rz".format(poly_cylinder[0]), math.degrees(_axis.rotateTo(_vec).asEulerRotation().z))

            cmds.setAttr("{}.sy".format(poly_cylinder[0]), _vec.length())
