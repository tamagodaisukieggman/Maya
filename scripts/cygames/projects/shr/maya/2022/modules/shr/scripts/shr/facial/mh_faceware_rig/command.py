import typing as tp

import pymel.core as pm
import pymel.core.nodetypes as nt
import maya.OpenMayaUI as OpenMayaUI
import shr.animation.bakesimulation as bs

RIG_GUI_NAME = "GRP_faceGUI"


class RigUtilCommands:
    @classmethod
    def get_corresponding_rig(
        cls, rigs  #: tp.List(nt.Transform)
    ):  # -> tp.List(nt.Transform):
        """rigsの対となる

        Args:
            rigs (tp.List(nt.Transform)): sub or mainのリグ

        Returns:
            tp.List(nt.Transform): rigsの対となるリグ
        """
        rtn_rigs = []
        if "_SUB" in str(pm.ls(sl=True)[0]):
            for lp in rigs:
                main_rig = cls.get_mainrig_from_selected_subrig(lp)
                rtn_rigs.append(main_rig)
        else:
            for lp in rigs:
                sub_rig = cls.get_subrig_from_selected_mainrig(lp)
                rtn_rigs.append(sub_rig)
        return rtn_rigs

    @classmethod
    def get_mainrig_from_selected_subrig(cls, sub_rig: nt.Transform) -> nt.Transform:
        """入力のsub rigに対応するmain rigを返す

        Args:
            sub_rig (pm.Transform): sub rig

        Raises:
            ValueError: sub rigのノード以外を渡すとエラー

        Returns:
            pm.Transform: main rig
        """
        # "CTRL_"と"_SUB"が含まれていればリグオブジェクトと判定
        if "CTRL_" not in sub_rig.name() and "_SUB" not in sub_rig.name():
            raise ValueError("No sub_rig node selected")
        main_rig = pm.PyNode(sub_rig.name().replace("_SUB", ""))
        return main_rig

    @classmethod
    def get_subrig_from_selected_mainrig(cls, main_rig: nt.Transform) -> nt.Transform:
        """入力のmain_rigに対応するsub rigを返す

        Args:
            main_rig (pm.Transform): main_rig

        Raises:
            ValueError: sub rigのノード以外を渡すとエラー

        Returns:
            pm.Transform: sub rig
        """
        # "CTRL_"が含まれていればリグオブジェクトと判定
        if "CTRL_" not in main_rig.name():
            raise ValueError("No main_rig node selected")
        sub_rig = pm.PyNode(main_rig.name() + "_SUB")
        return sub_rig

    @classmethod
    def initialize_mh_rig(cls):
        """sub_rigと計算用に作成したノードの削除"""
        RigGUICommands.delete_sub_rig_gui()
        RigGUICommands.delete_math_nodes()

    @classmethod
    def bake_mainrig_animation(cls):
        bs.main()

    @classmethod
    def select_mainrig(cls):  # -> tp.List[nt.Transform]:
        """main rigを全て選択

        Returns:
            tp.List[nt.Transform]: _description_
        """
        children = pm.listRelatives("FRM_faceGUI", ad=True, type="transform")
        rtn_rigs = []
        for lp in children:
            if "CTRL_" in lp.name():
                rtn_rigs.append(lp)
        pm.select(rtn_rigs)
        return rtn_rigs


class RigGUICommands:
    @classmethod
    def create_sub_rig(cls):
        # グループ作成時に不要な階層移動を防ぐ
        pm.select(clear=True)

        """metahumanrig拡張のsub_rigの作成"""
        if pm.objExists("mh_sub_rigs_grps"):
            cls.delete_sub_rig_gui()

        root = pm.group(n="mh_sub_rigs_grps", w=True)
        sub_rig_root = pm.duplicate(
            pm.ls(cls.get_facegui_grp_name()), n=cls.get_facegui_grp_name() + "_SUB"
        )

        pm.parent(sub_rig_root, root)

        fleeze_targets = []
        target_mainrigs = []
        for lp in pm.listRelatives(sub_rig_root, ad=True, type="transform"):
            sub_rig = pm.rename(lp, lp.name() + "_SUB")
            main_rig = RigUtilCommands.get_mainrig_from_selected_subrig(sub_rig)

            # rigのノードのみ
            if sub_rig.name().startswith("CTRL_"):

                # 一定の規則に収まらない処理の必要のないリグをスキップ
                skip_list = ["CTRL_faceTweakersGUI_SUB", "CTRL_faceGUI_SUB"]
                if sub_rig.name() in skip_list:
                    continue

                # アトリビュートの設定
                for axis in ["X", "Y", "Z"]:
                    # 後で接続し直す必要のあるblendweight(ドリブンキー用)のノードを取得
                    blendweight = cls._get_blendweight_node(main_rig, axis)

                    # 一旦全てのtranslateをアンロック
                    pm.setAttr(
                        sub_rig.name() + ".translate{}".format(axis.upper()), lock=0
                    )
                    pm.setAttr(
                        main_rig.name() + ".translate{}".format(axis.upper()), lock=0
                    )

                    pm.transformLimits(sub_rig, ty=[-0.5, 0.5], ety=[1, 1])

                    math_node_base = main_rig.name()

                    # connectionの作成
                    add_math, mult_math = cls._create_math_node(math_node_base, axis)

                    cls._create_connection(
                        add_math,
                        mult_math,
                        main_rig,
                        sub_rig,
                        blendweight,
                        axis,
                    )

                # フリーズするノードのリスト
                fleeze_targets.append(sub_rig)

                # transformのチェック用
                target_mainrigs.append(main_rig)

                cls._set_center_trans(sub_rig)

                # TODO:文字の作成

        pm.makeIdentity(fleeze_targets, apply=True, t=1, r=0, s=0, n=0, pn=1)

        # mainrigのlock、subrigのアンロック
        cls.set_main_rig_enable(True)

        cls.check_invalid_value_rig(target_mainrigs)

    @classmethod
    def get_facegui_grp_name(cls) -> str:
        return cls.get_ref_assetname(RIG_GUI_NAME)

    @classmethod
    def get_ref_assetname(cls, name: str) -> str:
        if pm.objExists(name):
            return name
        elif pm.objExists("*:{}".format(name)):
            rtn_name = pm.ls("*:{}".format(name))[0].name()
            return rtn_name
        else:
            return None

    @classmethod
    def check_invalid_value_rig(cls, target_rigs: list):
        """不正な値を持っているリグを探して警告を出す

        Args:
            target_rigs (tp.List(nt.Transform)): 対象となるリグ
        """
        warning_target_rigs = []
        for main_rig in target_rigs:
            translate = pm.xform(main_rig, r=True, q=True, t=True)
            for value in translate:
                if cls._check_zero_value(value):
                    continue
                else:
                    warning_target_rigs.append(main_rig)

        cls.show_warning_zero_translate_driven_rig(warning_target_rigs)

    @classmethod
    def _check_zero_value(cls, value):
        if value == 0:
            return True
        # 近似も許容とする
        if value > -0.00001 and value < 0.0001:
            return True
        return False

    @classmethod
    def _create_math_node(
        cls, math_node_base: nt.Transform, axis: str
    ):  # -> tp.List[nt.Transform]:
        """math ノードの作成

        Args:
            math_node_base (nt.Transform): _description_
            axis (str): _description_

        Returns:
            tp.List[nt.Transform]: 作成したmathノードを二つ返す
        """
        add_math = pm.createNode("floatMath", n=math_node_base + "_add_" + axis)
        pm.setAttr(add_math.name() + ".floatB", 0)

        mult_math = pm.createNode("floatMath", n=math_node_base + "_multiply_" + axis)
        pm.setAttr(mult_math.name() + ".floatB", 2)
        pm.setAttr(mult_math.name() + ".operation", 2)

        return add_math, mult_math

    @classmethod
    def _create_connection(
        cls,
        add_math: nt.Transform,
        mult_math: nt.Transform,
        main_rig: nt.Transform,
        sub_rig: nt.Transform,
        blend: nt.Transform,
        axis: str,
    ):
        """connectionの作成

        Args:
            add_math (nt.Transform): + mathノード blendと計算用
            mult_math (nt.Transform): * mathノード 入力調整用
            main_rig (nt.Transform): mainのリグ
            sub_rig (nt.Transform): subのリグ
            blend (nt.Transform): blend weight (ドリブンキー用)
            axis (str): axis. X or Y or Z
        """
        if blend != None:
            # blendweightのlistconnectionを調べる
            pm.listConnections(blend, c=True, p=True)
            for lp in pm.listConnections(blend, c=True, p=True):
                if "output" in str(lp[0]) and "translate{}".format(axis) in str(lp[1]):
                    blend_attr = str(lp[0])

                    pm.connectAttr(
                        blend_attr,
                        "{}.floatB".format(add_math),
                    )

        # sub_rigとadd用のmathに接続
        pm.connectAttr(
            "{0}.translate{1}".format(sub_rig, axis),
            "{}.floatA".format(mult_math),
        )

        pm.connectAttr(
            "{}.outFloat".format(mult_math),
            "{}.floatA".format(add_math),
            f=True,
        )

        pm.connectAttr(
            "{}.outFloat".format(add_math),
            "{0}.translate{1}".format(main_rig, axis),
            f=True,
        )

    @classmethod
    def set_main_rig_enable(cls, value: bool):
        """main rigのenable設定

        Args:
            value (bool): main rigを有効/無効
        """
        if value == True:
            cls._set_lock_settings_rig_gui(True, False)
        else:
            cls._set_lock_settings_rig_gui(False, True)

    @classmethod
    def _set_lock_settings_rig_gui(cls, main_rig_enable: bool, sub_rig_enable: bool):
        """rig guiをbool値に合わせてロック 色設定

        Args:
            main_rig_enable (bool): _description_
            sub_rig_enable (bool): _description_
        """
        pm.setAttr(cls.get_facegui_grp_name() + ".template", main_rig_enable)
        pm.setAttr(cls.get_facegui_grp_name() + "_SUB" + ".template", sub_rig_enable)

        mat_name = cls.get_ref_assetname("GUI2D_yellow_shader")

        if main_rig_enable:
            pm.setAttr("{}.color".format(mat_name), [0, 1, 0.65385], type="double3")
        else:
            pm.setAttr("{}.color".format(mat_name), [1, 0.697, 0], type="double3")

    @classmethod
    def delete_sub_rig_gui(cls):
        """sub rigの削除"""
        # material等の設定を一旦mainを有効扱いに変更
        cls.set_main_rig_enable(True)

        # math関係のノード削除　再接続
        cls.delete_math_nodes()
        if cls.get_ref_assetname("mh_sub_rigs_grps"):
            cls.set_main_rig_enable(False)
            pm.delete(cls.get_ref_assetname("mh_sub_rigs_grps"))
        else:
            pm.warning("subrig_gui does not exist.")

    @classmethod
    def delete_math_nodes(cls):
        """全ての計算用ノードを削除、blendのコネクションをmain rigに再接続"""
        math_nodes = pm.ls("CTRL_*add_*", type="floatMath")
        # blend weightのつなげ直し
        for add_math in math_nodes:
            for lp in pm.listConnections(add_math, c=True, p=True):
                if ".floatB" in str(lp[0]):
                    bef_attr_name = str(lp[0]).split(".")[0]
                    attr_name, _, axis = bef_attr_name.rsplit("_", 2)
                    tra = "{0}.translate{1}".format(attr_name, axis)
                    blend = lp[1]
                    pm.connectAttr(blend, tra, f=True)

        math_nodes = []
        math_nodes.extend(pm.ls("CTRL_*multiply_*", type="floatMath"))
        math_nodes.extend(pm.ls("CTRL_*add_*", type="floatMath"))
        pm.delete(math_nodes)

    @classmethod
    def _get_blendweight_node(cls, main_rig: nt.Transform, axis: str) -> nt.Transform:
        """main_rigに接続されているblendweightの取得(ドリブンキーを使用している前提)

        Args:
            main_rig (pm.nodetypes.Transform): _description_

        Returns:
            nt.Transform: blendweight node
        """
        for node in pm.listConnections(main_rig, c=True, p=True):
            if (
                ".output" in node[1].name()
                and "translate{}".format(axis) in node[0].name()
            ):
                return node[1]
        return None

    @classmethod
    def _set_center_trans(cls, rig: nt.Transform):
        """リグを中心位置に移動
        中心は近似（リグの親オブジェクトがスライダーのビジュアルを表していたので、親の中心を取っている）

        Args:
            rig (_type_): _description_
        """
        parent = pm.listRelatives(rig, p=True)
        center = pm.objectCenter(parent, gl=True)
        pm.xform(rig, ws=True, t=center)

    @classmethod
    def show_warning_zero_translate_driven_rig(cls, target_rigs):
        message_text = "以下のリグに不正な値がTranslateに含まれています\n"
        for rig in target_rigs:
            message_text = message_text + "\n" + rig.name()

        pm.confirmDialog(
            title="警告",
            message="{}".format(message_text),
            button=["OK"],
            defaultButton="Yes",
            cancelButton="No",
            dismissString="No",
        )


class DrivenGUICommands:
    @classmethod
    def create_driven_rig(cls, rig_name: str):
        """リグの作成

        Args:
            rig_name (str): 作成するリグの名前を入力
        """
        control_rig = cls.create_driven_rig_object(rig_name)
        cls.create_driven_key(control_rig)

    @classmethod
    def create_driven_rig_object(cls, rig_name: str):
        """リグの作成

        Args:
            rig_name (str): 作成するリグの名前を入力
        """
        rig = pm.polyCylinder(
            r=0.5,
            h=0.3,
            sx=20,
            sy=1,
            sz=1,
            ax=[0, 0, 1],
            rcp=0,
            cuv=3,
            ch=1,
            n=rig_name,
        )[0]

        base = pm.polyCube(
            w=10,
            h=0.1,
            d=0.1,
            sx=1,
            sy=1,
            sz=1,
            ax=[0, 1, 0],
            cuv=4,
            ch=1,
            n=rig_name + "_base",
        )[0]

        pm.select(clear=True)
        root = pm.group(n=rig_name + "_grp", w=True)
        vec = pm.datatypes.Vector(-5, 0, 0)
        rig.translateBy(vec, space="world")
        # pm.move(["{}.scalePivot".format(base.name()),"{}.rotatePivot".format(base.name())],[-5,0,0], rpr=True)
        pm.makeIdentity(rig, apply=True, t=1, r=0, s=0, n=0, pn=1)
        pm.transformLimits(rig, tx=[0, 10], etx=[1, 1])
        pm.setAttr("{}.ty".format(rig.name()), lock=True)
        pm.setAttr("{}.tz".format(rig.name()), lock=True)

        pm.parent([base, rig], root)
        return rig

    def create_driven_key(cls, driver, target_rigs):
        # 有効な値を引っ張ってきて、drivenkeyでつなげる
        # pm.setDrivenKeyframe("ball.scaleX",driverValue=0,value=0,currentDriver="ball.translateX" )
        # setDriverKeyframe -driverValue 5 -value 1 ball.scaleX;
        ...
