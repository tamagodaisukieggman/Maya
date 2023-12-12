import json
import pathlib

import pytest
from maya import cmds
from mtk.cutscene.sequencer.sequencer_data.client import \
    SequencerJsonDataClient

TEST_FOLDER = pathlib.Path(__file__).parent / "test_data"

TEST_SCENE_FOLDER = TEST_FOLDER / "scene"
TEST_EXPORTRESOURCES_FOLDER = TEST_SCENE_FOLDER / "exportresources"

test_maya_scene = TEST_SCENE_FOLDER / "test_load_data.mb"
seq_file_path = TEST_SCENE_FOLDER / "test_load_data.seq"


@pytest.mark.skip
class TestSequencerJsonDataClient(object):
    def test_load(self):
        cmds.file(test_maya_scene, open=True, force=True)

        assert SequencerJsonDataClient.load(seq_file_path)

    def test_save(self, tmp_path: pathlib.Path):
        """tempにMayaシーンを保存してseqをセーブしてみて同じ内容になるか
        """
        print("tmp_path", tmp_path)
        temp_scene_path = tmp_path / "scene"
        temp_scene_path.mkdir()
        temp_maya_scene_path = temp_scene_path / "temp.mb"
        temp_seq_path = temp_scene_path / "temp.seq"

        cmds.file(test_maya_scene, open=True, force=True)
        cmds.file(rename=str(temp_maya_scene_path))
        cmds.file(save=True, force=True)

        SequencerJsonDataClient.save(str(temp_seq_path))

        with open(str(seq_file_path), "r") as f:
            base_data = json.loads(f.read())

        with open(str(temp_seq_path), "r") as f:
            temp_data = json.loads(f.read())

        assert base_data == temp_data

    def test_create_default_sequencer_path(self):
        """
        """
        cmds.file(test_maya_scene, open=True, force=True)

        path = SequencerJsonDataClient.create_default_sequencer_path()
        assert str(seq_file_path) == path
