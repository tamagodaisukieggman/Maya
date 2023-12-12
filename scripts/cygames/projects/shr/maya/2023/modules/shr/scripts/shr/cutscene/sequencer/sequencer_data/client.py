"""SequencerデータのSave機能
"""
from __future__ import annotations

import os
import pathlib

from maya import cmds

from ..api import *
from .data import SequencerSaveData

VERSION = "0.0.1"


class SequencerJsonDataClient(object):
    @classmethod
    def load(cls, file_path):
        save_data = SequencerSaveData()
        return save_data.load(file_path)

    @classmethod
    def save(cls, file_path):
        save_data = SequencerSaveData()
        save_data.update_maya_data()
        save_data.save(file_path)

    @classmethod
    def create_default_sequencer_path(cls) -> str:
        scene_path = cmds.file(query=True, sceneName=True)
        scene_dir = os.path.dirname(scene_path)

        scene_name = os.path.basename(scene_path)
        scene_name_no_ext = os.path.splitext(scene_name)[0]

        sequencer_file_name = f"{scene_name_no_ext}.seq"
        sequencer_file_path = os.path.join(scene_dir, sequencer_file_name)

        return str(pathlib.Path(sequencer_file_path))
