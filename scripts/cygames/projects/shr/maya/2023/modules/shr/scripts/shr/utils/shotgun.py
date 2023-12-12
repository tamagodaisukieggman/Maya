# -*- coding: utf-8 -*-
u"""shotgun

..
    END__CYGAMES_DESCRIPTION

"""

import os
import maya.cmds as cmds
from functools import wraps
import shotgun_api3 as sgapi
from shotgun_api3 import ShotgunError

import logging
logger = logging.getLogger('shotgun_for_mtk_explorer')
logger.setLevel(logging.ERROR)
logger.disabled = True

# shotgun config settings
sgconfig = {
    'url': r'https://cygames.shotgunstudio.com',
    'project': 'Mutsunokami',
    'api_key': 'ciqrkvzatb-vxcdlpcjdnoqX6',
    'script_name': 'mtk_shotgun_for_maya',
    'user_name': '',
    'user_pw': '',
    'login_type': 'script',  # 'script' (api_key, script_name) or 'user' (user_name, user_pw).
}

sg = None
_enable_sg = True

def dict_to_unicode(d):
    return '{%s}' % ',\n'.join("'%s': '%s'" % pair for pair in list(d.items()))

# shotgun wrapper function
# description:
#   1. open shotgun connection
#   2. execute calling function
#   3. keep shotgun connection
def sgwrapper(func):
    u"""sgコマンドのdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        u"""wrapper

        :param args: args[0] function, args[1] ファイルパスまたはファイルパスのリスト
        :param kwargs:
        :return:
        """
        global sg
        global _enable_sg

        result = None

        if not _enable_sg:
            return result

        try:
            if not sg:
                logger.debug("SG Wrapper: Connecting to Shotgun...")

                if sgconfig['login_type'] is 'script':
                    sg = sgapi.Shotgun(base_url=sgconfig['url'],
                                       script_name=sgconfig['script_name'],
                                       api_key=sgconfig['api_key'])

                # or, login with user name and password
                else:
                    sg = sgapi.Shotgun(base_url=sgconfig['url'],
                                       login=sgconfig['user_name'],
                                       password=sgconfig['user_pw'])

                if sg:
                    logger.debug("SG Wrapper: Connection OK!")

            result = func(*args, **kwargs)

        except ShotgunError as sg_error:
            logger.debug("Shotgun Error:")
            logger.error(sg_error)
        finally:
            #if sg:
            #    sg.close()
            #    logger.debug("SG Wrapper: Closing Shotgun Connection...")
            if not sg:
                logger.error("SG Wrapper: Connection Failed !")

        return result
    return wrapper


class MtkSG(object):
    # get shotgun instance
    @classmethod
    @sgwrapper
    def open_session(cls):
        # why does this return None ?
        if sg:
            return sg
        return None

    @classmethod
    @sgwrapper
    def close_session(cls):
        if sg:
            sg.close()

    # SG PROJECT METHODS
    @classmethod
    @sgwrapper
    def project(cls):
        sg_project = None
        if sg:
            project_name = sgconfig['project']
            sg_entity = "Project"
            sg_filters = [['name', 'is', project_name]]
            sg_fields = ['id', 'name', 'type']
            sg_project = sg.find_one(sg_entity, sg_filters, sg_fields)
        return sg_project

    # SG ASSET METHODS
    @classmethod
    @sgwrapper
    def all_sg_asset_types(cls):
        sg_asset_type_list = []
        if sg:
            sg_project = MtkSG.project()
            sg_entity = "Asset"
            sg_field = 'sg_asset_type'
            asset_fields = sg.schema_field_read(sg_entity, field_name=sg_field, project_entity=sg_project)
            if asset_fields is not None:
                sg_asset_type_list = asset_fields["sg_asset_type"]["properties"]["valid_values"]["value"]
        return sg_asset_type_list

    @classmethod
    @sgwrapper
    def asset(cls, asset_name):
        sg_asset = None
        if sg:
            # aquire the sg project entity
            sg_project = MtkSG.project()
            project_id = sg_project['id']

            # search for the specified sg asset entity
            sg_entity = "Asset"
            sg_filters = [['project', 'is', {'type': 'Project', 'id': project_id}], ['code', 'is', asset_name]]
            sg_fields = ['code', 'type', 'description', 'tags', 'id', 'sg_asset_type', 'levels', 'name']
            sg_asset = sg.find_one(sg_entity, sg_filters, sg_fields)
        return sg_asset

    @classmethod
    @sgwrapper
    def asset_batch(cls, asset_name_list):
        sg_asset_list = []
        if sg:
            # aquire the sg project entity
            sg_project = MtkSG.project()
            project_id = sg_project['id']

            for asset_name in asset_name_list:
                # search for the specified sg asset entity
                sg_entity = "Asset"
                sg_filters = [['project', 'is', {'type': 'Project', 'id': project_id}], ['code', 'is', asset_name]]
                sg_fields = ['code', 'type', 'description', 'tags', 'id', 'sg_asset_type', 'levels', 'name']
                sg_asset = sg.find_one(sg_entity, sg_filters, sg_fields)
                sg_asset_list.append(sg_asset)
        return sg_asset_list

    @classmethod
    @sgwrapper
    def all_assets(cls, asset_type_filter=None):
        sg_assets = []
        if sg:
            sg_project = MtkSG.project()
            project_id = sg_project['id']
            sg_entity = "Asset"

            sg_filters = [
                ['project', 'is', {'type': 'Project', 'id': project_id}],
            ]

            # currently, only works with 1 filter. can't do multi-filter (Character + FX + Prop)
            if asset_type_filter is not None:
                asset_filter = ['sg_asset_type', 'is', asset_type_filter]
                sg_filters.append(asset_filter)

            # 'code' is the asset's name. 'name' doesnt return anything.
            sg_fields = ['code', 'type', 'description', 'tags', 'id', 'sg_asset_type', 'levels']

            sg_assets = sg.find(sg_entity, sg_filters, sg_fields)

        if sg_assets is None:
            sg_assets = []

        return sg_assets

    @classmethod
    @sgwrapper
    def asset_thumbnail_url(cls, sg_asset):
        # this function fetches an asset thumbnail usrl
        thumb_url = None
        if sg:
            sg_entity = "Asset"
            sg_filters = [['id', 'is', sg_asset['id']]]
            sg_fields = ['id', 'code', 'image']

            asset_fields = sg.find_one(sg_entity, sg_filters, sg_fields)
            thumb_url = asset_fields.get('image')  # this url can be accessed.
            #asset_thumb_url_info = urlparse.urlparse(response_image)
            #asset_thumb_path = self._get_path(asset_thumb_url_info)
            #asset_thumb_url_short = asset_thumb_url_info.scheme + '://' + asset_thumb_url_info.netloc + asset_thumb_path

            #print(r"Asset Thumbnal URL: {}".format(thumb_url))
            #print(r"Asset Thumb URL Info: {}".format(asset_thumb_url_info))
            #print(r"Asset Thumb Path: {}".format(asset_thumb_path))
            #print(r"Asset Thumb URL Short: {}".format(asset_thumb_url_short))
        return thumb_url

    # SG TASK METHODS
    @classmethod
    @sgwrapper
    def task_template(cls, task_template_name):
        # this function fetches an sg task template
        # ex: task_template_name = r'mtk Animation Asset'
        sg_template = None
        if sg:
            sg_entity = 'TaskTemplate'
            sg_filters = [['code', 'is', task_template_name]]
            sg_fields = [u'type', u'id', u'code', 'entity', 'content', 'project', 'tasks', 'TaskTemplate.tasks', 'TaskTemplate.Tasks']  # task_template, template_task
            sg_template = sg.find_one(sg_entity, sg_filters, sg_fields)

            template_id = sg_template['id']

        return sg_template

    @classmethod
    @sgwrapper
    def task_template_data(cls, task_template_name):
        # this function fetches the task data from an sg task template
        # source ref:
        # https://github.com/shotgunsoftware/shotgunEvents/blob/master/src/examplePlugins/update_task_template_entities.py
        task_template_data = []
        if sg:
            task_schema = sg.schema_field_read("Task")
            sg_anim_template = MtkSG.task_template(task_template_name=task_template_name)

            if task_schema and sg_anim_template:
                # Remove any Task fields from the schema that we aren't allowed to edit.
                task_schema_copy = task_schema.copy()

                for field, value in list(task_schema.items()):
                    if value["editable"]["value"] is False:
                        del task_schema_copy[field]
                task_schema = task_schema_copy

                task_template_data = sg.find(
                    "Task",
                    [["task_template", "is", sg_anim_template]],
                    task_schema.keys()
                )

        return task_template_data

    @classmethod
    @sgwrapper
    def asset_task_batch(cls, sg_asset_name_list):
        sg_task_dict = {}
        if sg:
            sg_project = MtkSG.project()
            project_type = sg_project['type']
            project_id = sg_project['id']

            # query for tasks
            sg_entity = "Task"

            # the tasks are Asset tasks, from the specified project
            sg_filters = [
                ['project', 'is', {'type': project_type, 'id': project_id}],
                ['entity', 'type_is', 'Asset'],
            ]

            # the assets are specified below
            code_filter_list = []

            for asset_name in sg_asset_name_list:
                code_filter = ['entity.Asset.code', 'is', asset_name]
                code_filter_list.append(code_filter)

            code_filter_dict = {
                "filter_operator": "any",
                "filters": code_filter_list
            }

            sg_filters.append(code_filter_dict)

            # the task and asset data fields we want
            sg_fields = ['type', 'id', 'content', 'sg_status_list', 'step', 'entity', 'entity.Asset.sg_status_list']

            logger.info("querying shotgun asset tasks...")

            all_sg_tasks = sg.find(sg_entity, sg_filters, sg_fields)

            logger.info("number of assets: {}".format(len(sg_asset_name_list)))

            logger.info("found {} tasks".format(len(all_sg_tasks)))

            if all_sg_tasks:
                filtered_tasks = all_sg_tasks
                for sg_asset_name in sg_asset_name_list:
                    sg_tasks = [y for y in filtered_tasks if y['entity']['name'] == sg_asset_name]
                    logger.debug("asset: {}".format(sg_asset_name))
                    logger.debug("tasks: {}".format(sg_tasks))
                    sg_task_dict[sg_asset_name] = sg_tasks
            else:
                logger.info("failed to get shotgun asset tasks.")

        return sg_task_dict

    @classmethod
    @sgwrapper
    def set_asset_task_status(cls, sg_task_id, sg_status):
        result = False

        if sg:
            sg_entity = "Task"

            sg_data = {
                'sg_status_list': sg_status
            }

            result = sg.update(sg_entity, sg_task_id, sg_data)

        return result
