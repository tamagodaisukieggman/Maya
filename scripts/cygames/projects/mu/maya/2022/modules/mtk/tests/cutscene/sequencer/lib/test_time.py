from pathlib import Path

from mtk.cutscene.sequencer.lib import time


def test_fetch_file_updated_time():
    script_dir = Path(__file__).parent
    test_data_dir = script_dir / "test_data"
    test_file = test_data_dir / "test_fetch_file_updated_time.txt"
    result = time.fetch_file_updated_time(test_file)

    assert "2022/01/27 10:48:58" == result


def test_fetch_now_time():
    # 実行テストのみ
    time.fetch_now_time()
    assert True
