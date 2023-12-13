import maya.cmds as cmds
import pytest

def test_chr_all_check_success():
    test_filepath = 'D:/tech-designer/maya_legacy/scripts/Project_Wizard2/tests/chara_checker_test/test_data/p2_c_yuwan01.mb'
    cmds.file(test_filepath,open = True,f=True)

    from Project_Wizard2.chara.character_checker import app as testapp
    from Project_Wizard2.common.maya_checker.data import ErrorType

    checker = testapp.get_character_checker(["p2"])
    checker.exec_all_check()
    has_error = False
    for task_name in checker.debug_datas:
        # 
        if task_name not in ["ExistsUnknownNode","ExistsUnknownPlugin","Wiz2TextureLocation"]:
            debug_data = checker.get_debug_data(task_name)
            if debug_data.error_type != ErrorType.NOCHECKED and debug_data.error_type != ErrorType.NOERROR:
                has_error = True
                print(f"{task_name}に問題あり")
    assert not has_error

def test_chr_all_check_error():
    test_filepath = 'D:/tech-designer/maya_legacy/scripts/Project_Wizard2/tests/chara_checker_test/test_data/p2_b_hotpants01_error.ma'
    cmds.file(test_filepath,open = True,f=True)

    from Project_Wizard2.chara.character_checker import app as testapp
    from Project_Wizard2.common.maya_checker.data import ErrorType

    checker = testapp.get_character_checker(["|p2_b_hotpants01"])
    checker.exec_all_check()
    has_error = False
    for task_name in checker.debug_datas:
        if task_name not in ["ExistsUnknownNode","ExistsUnknownPlugin","Wiz2TextureLocation"]:
            debug_data = checker.get_debug_data(task_name)
            if debug_data.error_type != ErrorType.NOCHECKED and debug_data.error_type != ErrorType.NOERROR:
                has_error = True
                print(f"{task_name}に問題あり")
    assert has_error

@pytest.mark.parametrize("task_name", ["Wiz2FileName", "Wiz2JointStructure"])
def test_chr_single_check_success(task_name):
    test_filepath = 'D:/tech-designer/maya_legacy/scripts/Project_Wizard2/tests/chara_checker_test/test_data/p2_b_hotpants01.ma'
    cmds.file(test_filepath,open = True,f=True)

    from Project_Wizard2.chara.character_checker import app as testapp
    from Project_Wizard2.common.maya_checker.data import ErrorType

    checker = testapp.get_character_checker(["p2"])
    checker.exec_task_by_taskname(task_name)
    debug_data = checker.get_debug_data(task_name)
    has_error = False
    if debug_data.error_type != ErrorType.NOCHECKED and debug_data.error_type != ErrorType.NOERROR:
        has_error = True
        print(f"{task_name}に問題あり")
    assert not has_error

@pytest.mark.parametrize("task_name", ["Wiz2FileName", "Wiz2JointStructure"])
def test_chr_single_check_error(task_name):
    test_filepath = 'D:/tech-designer/maya_legacy/scripts/Project_Wizard2/tests/chara_checker_test/test_data/p2_b_hotpants01_error.ma'
    cmds.file(test_filepath,open = True,f=True)

    from Project_Wizard2.chara.character_checker import app as testapp
    from Project_Wizard2.common.maya_checker.data import ErrorType

    checker = testapp.get_character_checker(["|p2_b_hotpants01"])
    checker.exec_task_by_taskname(task_name)
    debug_data = checker.get_debug_data(task_name)
    has_error = False
    if debug_data.error_type != ErrorType.NOCHECKED and debug_data.error_type != ErrorType.NOERROR:
        has_error = True
        print(f"{task_name}に問題あり")
    assert has_error