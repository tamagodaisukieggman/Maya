import typing as tp
from .checker import Checker


class CheckerFactory:
    @classmethod
    def create(cls, root_nodes: tp.List[str], checker_info: dict):
        """Checkerクラスのインスタンスを返すファクトリー

        Args:
            checker_info (dict): _description_
        """
        tool_title = cls.create_tool_title(checker_info)
        task_names = cls.create_task_names(checker_info)
        extra_datas = cls.create_extra_datas(checker_info)
        post_process_settings = cls.create_postprocess_settings(checker_info)

        checker = Checker(
            tool_title,
            task_names,
            extra_datas,
            root_nodes,
            post_process_settings,
        )

        return checker

    @classmethod
    def create_postprocess_settings(cls, checker_info):
        post_process_settings = []
        if "post_process_settings" in checker_info:
            post_process_settings = checker_info["post_process_settings"]
        return post_process_settings

    @classmethod
    def create_tool_title(cls, checker_info):
        checker_name = checker_info["checker_name"]
        checker_version = checker_info["checker_ui_version"]

        tool_title = f"{checker_name}_{checker_version}"
        return tool_title

    @classmethod
    def create_task_names(cls, current_task_datas):
        task_names = []
        for task_data in current_task_datas["tasks"]:
            if task_data["type"] != "task":
                continue

            task_name = task_data["name"]

            task_names.append(task_name)
        return task_names

    @classmethod
    def create_extra_datas(
        cls,
        current_task_datas: dict,
    ):
        """extra dataの作成

        Args:
            current_task_datas (dict): yamからtaskの引っ張ってきたdict
            current_task_names (tp.List[str]): taskの名前の配列
            extra_datas (dict): 参照で変更するextra_data
        """
        extra_datas = {}
        for task_data in current_task_datas["tasks"]:
            if task_data["type"] != "task":
                continue

            task_name = task_data["name"]

            if "extra_data" in task_data and task_data["extra_data"]:
                extra_datas.update({task_name: task_data["extra_data"]})
        return extra_datas
