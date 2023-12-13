# -*- coding: utf-8 -*-
u"""Shotgridの処理をラップしたクラス
将来的に分離してgallopバッチから読み込める形式に変更する
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

try:
    import shotgun_api3
except Exception as e:
    pass

try:
    # Maya2022-
    from builtins import object
except Exception:
    pass


class Shotgrid(object):

    def __init__(self, sg_url='', user='', password=''):

        self._sg_url = sg_url
        self.user = user
        self.password = password

        self.sg_instance = None

    def __create_instance(self):
        u"""インスタンス生成
        """

        if not self._sg_url or not self.user or not self.password:
            return None

        return shotgun_api3.Shotgun(
            base_url=self._sg_url,
            login=self.user,
            password=self.password)

    def __check_connection(self, instance_obj):
        u"""Shotgridにログインできているかをチェックする
        """

        try:
            instance_obj.get_session_token()
            return True

        except shotgun_api3.shotgun.AuthenticationFault:
            return False

    def check_loaded_shotgun_api_module(self):
        u"""shotgun_api3モジュールが呼び出せているかを確認する
        """

        if 'shotgun_api3' not in sys.modules:
            return False

        return True

    def set_shotgrid_instance(self):
        u"""shotgridインスタンスを設定する
        shotgun_api3モジュールが呼び出せていない、またはShotgridにログインできない場合は
        インスタンス設定は行われない
        """

        if not self.check_loaded_shotgun_api_module():
            return False

        instance_obj = self.__create_instance()
        if not instance_obj:
            return False

        if not self.__check_connection(instance_obj):
            return False

        self.sg_instance = instance_obj
        return True

    def check_exec_sg_instance_decorator(func):
        u"""session_tokenが取得出来ていてsgにログインできている状態かチェックするデコレータ
        """

        def check_exec_sg_instance(self, *args, **kwargs):

            if not self.sg_instance:
                # sgとの接続を試みる
                if not self.set_shotgrid_instance():
                    return None

            return func(self, *args, **kwargs)

        return check_exec_sg_instance

    @check_exec_sg_instance_decorator
    def get_projects(self, project_name):
        u"""project_nameから該当するProjectを取得する

        Args:
            project_name ([type]): 検索したいProject名

        Returns:
            [type]: {
                'id': Projectのid(int),
                'name': Project名
            }
            or None
        """

        filters = [["name", "is", project_name]]
        fields = ["name", "sg_description"]

        return self.sg_instance.find(entity_type="Project", filters=filters, fields=fields)

    @check_exec_sg_instance_decorator
    def get_entity(self, code_name, project_info=None, add_filters=None, add_field=None, entity_type='Asset', set_all_field=False, get_one=False):
        u"""code(Assetエンティティでいうアセット名)に一致しエンティティタイプが合致するオブジェクトを全て取得する

        Args:
            code_name ([type]): code名(Assetエンティティでいうアセット名)
            project_info ([type], optional): 検索するproject. Defaults to None.
            add_filters ([type], optional): 検索対象のフィルター.追加するとより絞り込める. Defaults to None.
                                            記法が特殊なので、追加する時は注意が必要
                                            ex) [['sg_glp_section', 'is', '3DCGキャラ班'], [...]]
            add_field ([type], optional): 取得するオブジェクトに含みたいフィールド. Defaults to None.
                                          設定しない場合、取得したオブジェクトに含まれるのはcodeとdescriptionのみ(nameは自動的に入る)
                                          ex) ['sg_glp_section', 'sg_glp_division']
            entity_type (str, optional): . Defaults to 'Asset'.
            set_all_field (bool, optional): [description]. Defaults to False.
            get_one (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """

        filters = [["code", "is", code_name]]

        if project_info:
            filters.append(['project', 'is', {'id': project_info.get('id'), 'type': project_info.get('type')}])

        if add_filters:
            filters.extend(add_filters)

        fields = ['code', 'description']
        if add_field:
            fields.extend(add_field)

        if set_all_field:
            fields = [key for key in list(self.sg_instance.schema_field_read('Asset').keys())]

        if get_one:
            return self.sg_instance.find_one(entity_type=entity_type, filters=filters, fields=fields)
        else:
            return self.sg_instance.find(entity_type=entity_type, filters=filters, fields=fields)

    @check_exec_sg_instance_decorator
    def create_asset(self, asset_name, project_info, add_data=None, entity_type='Asset'):
        """
        """

        data = {
            'code': asset_name,
            'project': {'id': project_info.get('id'), 'type': project_info.get('type')}
        }

        if add_data:
            data.update(add_data)

        return self.sg_instance.create(entity_type=entity_type, data=data)

    @check_exec_sg_instance_decorator
    def update_asset(self, asset_info, entity_data):
        """
        """

        return self.sg_instance.update(
            entity_type=asset_info.get("type"), entity_id=asset_info.get("id"), data=entity_data)

    @check_exec_sg_instance_decorator
    def get_field_info(self, field_code, entity_type='Asset'):
        """
        """

        return self.sg_instance.schema_field_read(entity_type, field_code)

    @check_exec_sg_instance_decorator
    def upload_file(self, asset_info, file_path, field_name='sg_uploaded_movie'):
        """
        """

        return self.sg_instance.upload(
            entity_type=asset_info.get('type'),
            entity_id=asset_info.get('id'),
            path=file_path,
            field_name=field_name
        )
