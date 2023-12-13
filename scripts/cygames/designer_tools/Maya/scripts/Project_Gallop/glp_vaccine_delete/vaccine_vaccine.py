import os
import maya.cmds as cmds


# ===============================================
def get_patient_list(root_path):
    """search target file
    """

    vaccine_virus_str_list = ['vaccine.py', 'sysytenasdasdfsadfsdaf_dsfsdfaasd']
    ma_path_list = []
    patient_list = []

    for curDir, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".ma"):
                ma_path_list.append(os.path.join(curDir, file))

    for ma_path in ma_path_list:
        try:
            with open(ma_path) as f:
                string = f.read()
                for vaccine_virus_str in vaccine_virus_str_list:
                    if string.find(vaccine_virus_str) >= 0:
                        patient_list.append(ma_path)
                        break
        except Exception:
            pass

    return patient_list


# ===============================================
def kill_vaccine():
    """delete target script nodes
    """

    target_script_nodes = ['vaccine_gene', 'breed_gene', 'script']
    script_nodes = cmds.ls(typ='script')

    print(script_nodes)

    flg = False
    for script_node in script_nodes:
        for target_script_node in target_script_nodes:
            if script_node.startswith(target_script_node):
                cmds.delete(script_node)
                flg = True
                break

    return flg


# ===============================================
def treat_patient(path):
    """do cleaning
    """

    root_path = path
    patient_list = get_patient_list(root_path)
    treated_list = []

    for patient in patient_list:
        cmds.file(patient, open=True, executeScriptNodes=False, f=True)
        result = kill_vaccine()
        cmds.file(s=True, f=True)

        if result:
            treated_list.append(patient)

    return treated_list
