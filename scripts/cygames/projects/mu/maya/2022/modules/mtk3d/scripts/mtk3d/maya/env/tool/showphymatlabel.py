# -*- coding: cp932 -*-
#===============================================
#
# �t�F�[�X�ɕ����}�e���A�����x����\��
#
# Fujita Yukihiro
#
#===============================================

# import maya.cmds as cmds
from maya import cmds

def show_phy_material_labels() -> None:
    """ �t�F�[�X�ɕ����}�e���A�����x����\�� """

    # �A�m�e�[�V�����m�[�h�O���[�v��
    LABELS_NODE_NAME = "_physics_mat_labels"

    # ���łɑ��݂���΍폜
    if cmds.objExists(LABELS_NODE_NAME):
        cmds.delete(LABELS_NODE_NAME)

    # �I�����擾
    sel = cmds.ls(selection=True)

    # �I���m�[�h�̂��ׂĂ̎q���̂����Amesh ���擾
    all_mesh_nodes: list[str] = cmds.listRelatives(sel, fullPath=True, allDescendents=True, type="mesh", noIntermediate=True)

    if all_mesh_nodes is None:
        all_mesh_nodes = []

    # �I�����Ă��郁�b�V���m�[�h���擾
    sel_meshes: list[str] = cmds.ls(selection=True, long=True, type="mesh")

    # �S�Ẵ��b�V���m�[�h���X�g�ɑI�����b�V���m�[�h��ǉ�
    all_mesh_nodes.extend(sel_meshes)

    # ���X�g����d�����폜
    all_mesh_nodes = list(set(all_mesh_nodes))

    # �S�Ẵ^�[�Q�b�g���b�V���m�[�h
    target_mesh_nodes = []

    for mesh_node in all_mesh_nodes:

        # collision �m�[�h�ȉ��ɂ��郁�b�V���m�[�h�Ȃ�
        if "|collision|" in mesh_node:

            # �^�[�Q�b�g���b�V���m�[�h���X�g�ɒǉ�
            target_mesh_nodes.append(mesh_node)

    # �^�[�Q�b�g���b�V���̂��ׂẴt�F�[�X���擾
    target_faces: list[str] = cmds.polyListComponentConversion(target_mesh_nodes, toFace=True)

    if len(target_faces) != 0:
        target_faces = cmds.filterExpand(target_faces, selectionMask=34)

    # �I�����Ă���t�F�[�X���擾
    sel_faces = cmds.filterExpand(selectionMask=34)

    # �I�����Ă���t�F�[�X������ꍇ
    if sel_faces is not None:

        for face in sel_faces:

            # �t�F�[�X���烁�b�V���m�[�h���擾
            mesh_node = cmds.listRelatives(face, parent=True, fullPath=True)

            # collision �m�[�h�ȉ��ɂ��郁�b�V���m�[�h�Ȃ�
            if "|collision|" in mesh_node[0]:

                # �^�[�Q�b�g���b�V���m�[�h���X�g�ɒǉ�
                target_mesh_nodes.append(mesh_node[0])

                # �^�[�Q�b�g�t�F�[�X���X�g�ɒǉ�
                target_faces.append(face)

    # ���X�g����d�����폜
    target_mesh_nodes = list(set(target_mesh_nodes))

    # �Ώۃ��b�V���m�[�h���Ȃ���ΏI��
    if len(target_mesh_nodes) == 0:
        return

    # �n�C���C�g����Ă���m�[�h���擾
    hl_nodes = cmds.ls(hilite=True)

    # �A�T�C������Ă���}�e���A����I��
    cmds.hyperShade(shaderNetworksSelectMaterialNodes=True)

    # �I���}�e���A�����擾
    sel_materials = cmds.ls(selection=True, materials=True)

    # �쐬�����A�m�e�[�V�����m�[�h
    ann_nodes = []

    for mat in sel_materials:

        # �����}�e���A�����A�T�C������Ă����
        if cmds.attributeQuery("phyMaterialName", node=mat, exists=True):

            # �}�e���A�����A�T�C������Ă��镨��I��
            cmds.hyperShade(objects=mat)

            # �I�����Ă��郁�b�V���m�[�h���擾
            assigned_meshes = cmds.ls(selection=True, long=True, type="mesh")

            # �^�[�Q�b�g���b�V���m�[�h�ƃA�T�C������Ă��郁�b�V���m�[�h�̐ϏW��
            meshes = set(target_mesh_nodes) & set(assigned_meshes)

            if meshes is None:
                meshes = []

            else:
                meshes = list(meshes)

            # �I�����Ă���t�F�[�X���擾
            assigned_faces = cmds.filterExpand(selectionMask=34)

            if assigned_faces is None:
                assigned_faces = []

            # �ϏW���̌��ʂ̃��b�V���m�[�h���t�F�[�X�ɕϊ�
            assigned_meshes_faces = cmds.polyListComponentConversion(meshes, toFace=True)

            assigned_faces.extend(assigned_meshes_faces)

            # ���X�g���t���b�g��
            assigned_faces = cmds.ls(assigned_faces, flatten=True)

            # �d�����폜
            assigned_faces = list(set(assigned_faces))

            # �^�[�Q�b�g���b�V���m�[�h�ƃA�T�C������Ă��郁�b�V���m�[�h�̐ϏW��
            faces = set(target_faces) & set(assigned_faces)


            if faces is None:
                faces = []

            else:
                faces = list(faces)

            # �t�F�[�X�𒸓_���X�g�ɕϊ�
            vertex = cmds.polyListComponentConversion(faces, toVertex=True)

            # ���_���X�g���t���b�g��
            vertex = cmds.filterExpand(vertex, selectionMask=31)

            # �쐬����A�m�e�[�V�����m�[�h�̈ʒu
            ann_pos = [0, 0, 0]

            for v in vertex:

                # ���_�ʒu���擾
                pos: list = cmds.pointPosition(v, world=True)

                # �t�F�[�X���\�����钸�_�ʒu���W�����v
                ann_pos[0] += pos[0]
                ann_pos[1] += pos[1]
                ann_pos[2] += pos[2]

            # �t�F�[�X���\�����钸�_��
            vertex_count = len(vertex)

            # �t�F�[�X�̒��S�ʒu���擾
            ann_pos[0] = ann_pos[0] / vertex_count
            ann_pos[1] = ann_pos[1] / vertex_count
            ann_pos[2] = ann_pos[2] / vertex_count

            # �A�m�e�[�V�����m�[�h�̃J���[��ݒ�i���邯��ΈÂ��A�Â���Ζ��邭�j
            col = cmds.getAttr(mat + ".color")
            col = list(col[0])

            if (col[0] + col[1] + col[2]) / 3 >= 0.5:
                col[0] = col[0] * 0.2
                col[1] = col[1] * 0.2
                col[2] = col[2] * 0.2

            else:
                col[0] = 1 - (1 - col[0]) * 0.8
                col[1] = 1 - (1 - col[1]) * 0.8
                col[2] = 1 - (1 - col[2]) * 0.8

            # �A�m�e�[�V�����m�[�h�̃e�L�X�g��ݒ�
            ann_text = cmds.getAttr(mat + ".phyMaterialName")

            # �A�m�e�[�V�����m�[�h���쐬
            ann_node = cmds.annotate(faces[0], text=ann_text, point=ann_pos)

            # �A�m�e�[�V�����m�[�h�̖����I�t
            cmds.setAttr(ann_node + ".displayArrow", False)

            # �I�[�o�[���C�h�J���[��ݒ�
            cmds.setAttr(ann_node + ".overrideEnabled", True)
            cmds.setAttr(ann_node + ".overrideRGBColors", True)
            cmds.setAttr(ann_node + ".overrideColorRGB", col[0], col[1], col[2], type="double3", clamp=True)

            # �A�m�e�[�V�����m�[�h���X�g�ɒǉ�
            ann_nodes.append(cmds.listRelatives(ann_node, parent=True)[0])

    if len(ann_nodes) != 0:

        # �O���[�v�m�[�h�쐬
        cmds.group(empty=True, name=LABELS_NODE_NAME)

        # �A�E�g���C�i�Ŕ�\����
        cmds.setAttr(LABELS_NODE_NAME + ".hiddenInOutliner", True)

        # �쐬�����A�m�e�[�V�����m�[�h���O���[�v�m�[�h�̎q��
        cmds.parent(ann_nodes, LABELS_NODE_NAME)

    # �I���𕜌�
    cmds.hilite(hl_nodes, replace=True)
    cmds.select(sel, replace=True)
