# -*- coding: utf-8 -*-
from maya import cmds
from maya.app.general import mayaMixin

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QPushButton,
    QMessageBox,
    QErrorMessage,
    QProgressDialog
)

class BakeSimulatedBone(mayaMixin.MayaQWidgetBaseMixin, QDialog):
    def __init__(self):
        super(BakeSimulatedBone, self).__init__()

        self.setWindowTitle('Bake Simulation')

        button = QPushButton('Bake')
        button.setMinimumSize(200, 70)
        button.clicked.connect(self.execute)
        layout = QVBoxLayout()
        layout.addWidget(button)
        self.setLayout(layout)

        self.resize(300, 70)

    def execute(self):

        sel = cmds.ls(sl=True)
        if len(sel) == 0:
            dialog = QErrorMessage(self)
            dialog.showMessage(u"なんも選択されとらん！")
            return
        elif len(sel) > 1:
            dialog = QMessageBox(self)
            dialog.warning(self, "Error", u"複数選択されとるばってん、最初んとしか判断せんけど、よかと？")
        pieces = cmds.listRelatives(sel[0])
        cmds.select(clear=True)

        progress = QProgressDialog(u"焼き付けよっけん待ちんしゃい", "Cancel", 0, len(pieces), self)
        progress.setWindowTitle('Bake Simulations...')
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)

        root_joint_name = 'jnt_0000_skl_root'
        root_joint = cmds.joint(name=root_joint_name)
        cmds.select(clear=True)
        parent_joints = []
        for i, piece in enumerate(pieces):
            progress.setValue(i+1)
            if progress.wasCanceled():
                break

            joint_name = 'jnt_{}_skl_joint{}'.format(str(i+1).zfill(4), str(i+1))
            parent_joint = cmds.joint(name=joint_name)
            parent_joints.append(parent_joint)
            constrain = cmds.parentConstraint(piece, parent_joint)
            cmds.bakeResults(
                simulation=True,
                time=(
                    cmds.playbackOptions(query=True, minTime=True),
                    cmds.playbackOptions(query=True, maxTime=True)),
                sampleBy=1,
                oversamplingRate=1,
                disableImplicitControl=True,
                preserveOutsideKeys=True,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                removeBakedAnimFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                controlPoints=False,
                shape=True,
            )
            cmds.delete(constrain)

            # Remove animated key for each piece
            cmds.cutKey(piece, clear=True, attribute="tx")
            cmds.cutKey(piece, clear=True, attribute="ty")
            cmds.cutKey(piece, clear=True, attribute="tz")
            cmds.cutKey(piece, clear=True, attribute="rx")
            cmds.cutKey(piece, clear=True, attribute="ry")
            cmds.cutKey(piece, clear=True, attribute="rz")
            cmds.cutKey(piece, clear=True, attribute="sx")
            cmds.cutKey(piece, clear=True, attribute="sy")
            cmds.cutKey(piece, clear=True, attribute="sz")

            # Bake Skin
            cmds.skinCluster(parent_joint, piece)
            cmds.select(clear=True)
        else:
            cmds.parent(parent_joints, root_joint)

            dialog = QMessageBox(self)
            dialog.setText(u"終わったばい")
            dialog.show()


def main():
    dialog = BakeSimulatedBone()
    dialog.show()


if __name__ == '__main__':
    main()
