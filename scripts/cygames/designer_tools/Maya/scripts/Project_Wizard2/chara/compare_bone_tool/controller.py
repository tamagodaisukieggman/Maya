import webbrowser
import typing as tp

import maya.cmds as cmds

from ..chara_utility import utility as chr_utils
from .view import View
from .app import BoneCompare
from .detail_controller import DetailController
from .data import BoneCheckedData, CheckState


class CompareBoneToolController:
    def __init__(self):
        self.ui = View()

        self.target_objects: tp.List[str] = None

        self.setup_ui()

    def setup_ui(self):
        self.ui.change_all_error_status_color("gray", "white")
        self.ui.on_clicked_detail_button.connect(self.clicked_detail_btn)
        self.ui.gui.compare_btn.clicked.connect(self.clicked_compare_btn)
        self.ui.gui.compare_table.itemSelectionChanged.connect(
            self.on_selection_changed
        )

        self.ui.gui.get_source_joint_btn.clicked.connect(
            self.clicked_get_source_joint_btn
        )
        self.ui.gui.get_target_joint_btn.clicked.connect(
            self.clicked_get_target_joint_btn
        )
        self.ui.gui.actiondocument.triggered.connect(self.show_manual)

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            webbrowser.open(
                "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=780851467"
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")

    def clicked_compare_btn(self):
        if (
            self.ui.gui.target_joint_name_txt.text() == ""
            or self.ui.gui.target_joint_name_txt.text() == ""
        ):
            result = cmds.confirmDialog(
                title="警告",
                message="それぞれのrootのジョイントが設定されていません。現在の選択から取得して実行しますか？",
                button=["Yes", "No"],
                defaultButton="Yes",
                cancelButton="No",
                dismissString="No",
            )
            if result:
                set_result = self.set_root_bones_by_selected()
            else:
                cmds.warinig("rootが設定されていないため実行できません。基準or対象のrootジョイントを設定してください。")
                return

        self.ui.reset_item_table()
        """比較ボタンを押した時の処理"""

        # 対象の骨の取得
        source = self.ui.gui.source_joint_name_txt.text()
        target = self.ui.gui.target_joint_name_txt.text()

        if not cmds.objExists(source) or not cmds.objExists(target):
            cmds.warning("")
            return

        source_joints = self.get_descendant_joints(source)
        target_joints = self.get_descendant_joints(target)
        self.check_datas = []

        self.compare_bone_structure_and_update_list(source_joints, target_joints)

        self.ui.reset_window_size()

        self.set_all_error_status()

    def set_all_error_status(self):
        """全てのエラーチェック確認用ステータスの更新"""
        error_count_data = self.get_all_check_error_status()
        if error_count_data["error_count"]:
            self.ui.gui.all_error_status_txt.setText(
                f"Error >> {error_count_data['error_count']}"
            )
            self.ui.change_all_error_status_color("red", "white")

        elif error_count_data["exist_error_count"]:
            self.ui.gui.all_error_status_txt.setText(
                f"Not Exist >> {error_count_data['exist_error_count']}"
            )
            self.ui.change_all_error_status_color("orange", "white")

        else:
            self.ui.gui.all_error_status_txt.setText(f"No Error")
            self.ui.change_all_error_status_color("lightgreen", "black")

    def compare_bone_structure_and_update_list(
        self, source_joints: tp.List[str], target_joints: tp.List[str]
    ):
        """比較結果をリストに反映する

        Args:
            source_joints (tp.List[str]): 比較のsource側の骨群
            target_joints (tp.List[str]): 比較のtarget側の骨群
        """
        source_joint_shortnames = self.get_short_name_list(source_joints)
        target_joint_shortnames = self.get_short_name_list(target_joints)

        diff_data = self.find_diff(source_joint_shortnames, target_joint_shortnames)

        progress_window, progress_bar = self.create_progress_bar(len(diff_data["A"])+1)

        if diff_data["A"]:
            item_data = {}
            ns = self.get_namespace(source_joints[0])
            for short_name in diff_data["A"]:
                item_data["source_joint_name"] = f"{ns}:{short_name}"
                item_data["target_joint_name"] = "<Nothing>"
                item_data[
                    "simple_error_message"
                ] = f"{item_data['source_joint_name']}は対象のジョイントに存在しません"
                self.add_missing_item_data(item_data)
                cmds.progressBar(progress_bar, edit=True, step=1)

        cmds.deleteUI(progress_window)

        progress_window, progress_bar = self.create_progress_bar(len(diff_data["B"])+1)

        if diff_data["B"]:
            item_data = {}
            ns = self.get_namespace(target_joints[0])
            for short_name in diff_data["B"]:
                item_data["source_joint_name"] = "<Nothing>"
                item_data["target_joint_name"] = f"{ns}:{short_name}"
                item_data[
                    "simple_error_message"
                ] = f"{item_data['target_joint_name']}は基準のジョイントに存在しません"
                self.add_missing_item_data(item_data)
                cmds.progressBar(progress_bar, edit=True, step=1)

        cmds.deleteUI(progress_window)


        progress_window, progress_bar = self.create_progress_bar(len(source_joints)+1)
        for source_joint in source_joints:
            source_short_name = chr_utils.get_short_name(source_joint)
            item_data = {}
            for target_joint in target_joints:
                if target_joint.endswith(source_short_name):
                    source_joint_name = cmds.ls(source_joint)[0]
                    target_joint_name = cmds.ls(target_joint)[0]
                    item_data["source_joint_name"] = source_joint_name
                    item_data["target_joint_name"] = target_joint_name
                    compare = BoneCompare(source_joint, target_joint)
                    compare.exec_compare()

                    item_data["check_data"] = compare.checked_data

                    if compare.checked_data.check_state == CheckState.HAS_ERROR:
                        item_data["simple_error_message"] = "値の異なるアトリビュートが存在します"
                    elif compare.checked_data.check_state == CheckState.NO_ERROR:
                        item_data["simple_error_message"] = "正しい値です。"

                    # error onlyのフィルタがかかっていたらNoErrorははじく
                    if self.ui.gui.error_only_cbox.isChecked():
                        if compare.checked_data.check_state == CheckState.NO_ERROR:
                            break

                    compare.checked_data.joint_name = source_short_name
                    self.check_datas.append(compare.checked_data)
                    self.ui.add_item_table(item_data)
                    break
            cmds.progressBar(progress_bar, edit=True, step=1)
        cmds.deleteUI(progress_window)

    def set_root_bones_by_selected(self):
        joints = cmds.ls(sl=True, type="joint")
        if not joints:
            cmds.warning("ジョイントが選択されていません")
            return False

        self.ui.gui.source_joint_name_txt.setText(joints[0])
        self.ui.gui.target_joint_name_txt.setText(joints[1])
        return True

    def add_missing_item_data(self, item_data: dict):
        """見つからない骨をnot existのエラーとして登録

        Args:
            item_data (dict): 参照渡しで値を設定するdictの変数
        """
        exist_error_check_data = BoneCheckedData()
        exist_error_check_data.check_state = CheckState.EXIST_ERROR
        item_data["check_data"] = exist_error_check_data
        self.ui.add_item_table(item_data)
        # Notingの場合は空の値を入れておく
        self.check_datas.append(exist_error_check_data)

    def clicked_detail_btn(self, row: int):
        check_data = self.check_datas[row]
        detail_controller = DetailController(check_data)
        detail_controller.show_ui()

    def clicked_get_source_joint_btn(self):
        selected_joints = cmds.ls(sl=True, type="joint")
        if selected_joints:
            self.ui.gui.source_joint_name_txt.setText(selected_joints[0])
        else:
            cmds.warning("基準のジョイントを選択して実行してください")

    def clicked_get_target_joint_btn(self):
        target_joints = cmds.ls(sl=True, type="joint")
        if target_joints:
            self.ui.gui.target_joint_name_txt.setText(target_joints[0])
        else:
            cmds.warning("基準のジョイントを選択して実行してください")

    def get_all_check_error_status(self) -> dict:
        """全てのチェック情報からエラーの数を返す

        Returns:
            dict: errorの数を保持する辞書
        """
        error_count = 0
        exist_error_count = 0
        for check_data in self.check_datas:
            if check_data.check_state == None:
                continue

            if check_data.check_state == CheckState.HAS_ERROR:
                error_count += 1

            elif check_data.check_state == CheckState.EXIST_ERROR:
                exist_error_count += 1
        return {"error_count": error_count, "exist_error_count": exist_error_count}

    def on_selection_changed(self):
        cmds.select(clear=True)
        selected_items = self.ui.gui.compare_table.selectedItems()
        for item in selected_items:
            if cmds.objExists(item.text()):
                cmds.select(item.text(), add=True)

    def get_descendant_joints(self, joint: str) -> tp.List[str]:
        """rootの骨を取得

        Args:
            joint (str): 取得する基準となる骨名

        Returns:
            tp.List[str]: 子孫の全てのジョイント
        """
        root = chr_utils.get_root_node(joint)
        descendant_joints = [root]
        descendant_joints.extend(
            cmds.listRelatives(root, ad=True, type="joint", fullPath=True) or []
        )
        return descendant_joints

    @staticmethod
    def get_namespace(node_name: str):
        """
        指定されたノード名からネームスペースを取得します。
        Args:
            node_name (str): ネームスペースを取得したいノード名（ネームスペースが含まれている場合、フルパスでも可）
        Returns:
            str: ノードのネームスペース、ノードがネームスペースに属していない場合は空の文字列
        """
        node_name = node_name.split("|")[-1]

        namespace = ""
        if ":" in node_name:
            namespace = node_name.rsplit(":", 1)[0]
        return namespace

    @staticmethod
    def find_diff(A, B):
        diff_A = list(set(A) - set(B))
        diff_B = list(set(B) - set(A))
        return {"A": diff_A, "B": diff_B}

    @staticmethod
    def get_short_name_list(node_list):
        rtn_list = []
        for node in node_list:
            rtn_list.append(chr_utils.get_short_name(node))
        return rtn_list
    
    @staticmethod
    def create_progress_bar(max_count: int) -> any:
        """プログレスバーを作成

        Args:
            max_count (int): プログレスバーのmax step

        Returns:
            any: プログレスバー
        """
        # プログレスバーの作成
        progress_window = cmds.window(title="Progress", widthHeight=(300, 50))
        cmds.columnLayout(adjustableColumn=True)
        progress_bar = cmds.progressBar(maxValue=max_count, width=300)
        cmds.showWindow(progress_window)
        return progress_window, progress_bar

    def show_ui(self):
        self.ui.show()

    def close_ui(self):
        self.ui.close()
