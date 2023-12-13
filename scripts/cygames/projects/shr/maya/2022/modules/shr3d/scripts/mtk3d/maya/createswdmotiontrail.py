# coding=utf-8
import maya.cmds as mc


def create_swd_motiontrail(*args):
    nmsp = "eqw00_999_rig:"
    st = nmsp + 'swordTip'

    sf = mc.playbackOptions(q=1, minTime=1)
    ef = mc.playbackOptions(q=1, maxTime=1)

    loc = mc.spaceLocator(n='swordTip_loc')
    pc = mc.parentConstraint(st, loc)

    mc.bakeResults(loc[0], t=(sf, ef), sb=1, simulation=1, at=["tx", "ty", "tz", "rx", "ry", "rz"])

    mc.delete(pc)

    mc.snapshot(loc[0], motionTrail=1, constructionHistory=1, startTime=sf,
                endTime=ef, increment=1, update=1, n=loc[0] + '_mt')
    mc.scriptJob(ro=0, attributeChange=['eqw00_999_rig:swordCtrl.matrix', warn], compressUndo=1)


def warn(*args):
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]
    tra_val = mc.xform('eqw00_999_rig:swordTip', t=1, q=1, ws=1)
    rot_val = mc.xform('eqw00_999_rig:swordTip', ro=1, q=1, ws=1)
    val = tra_val + rot_val

    n = len(attrs)

    ct = mc.currentTime(query=True)
    for i in range(0, n, 1):
        mc.selectKey('swordTip_loc.{}'.format(attrs[i]), time=(ct, ct), r=1, k=1)
        mc.keyframe(animation='keys', valueChange=val[i])


def main():
    create_swd_motiontrail()
