import os
import sys
import inspect
from pathlib import Path

from maya import cmds
from mtk import logger


def ocport(open_port=True) -> None:
    
    mel_port_state = cmds.commandPort(':7001', query=True)
    python_port_state = cmds.commandPort(':7002', query=True)
    
    # Mel port control
    if open_port and not mel_port_state:
        logger.info('Open Port: "7001" for Mel')
        cmds.commandPort(name=':7001', sourceType='mel', echoOutput=True)
    elif open_port and mel_port_state:
        logger.info('Port for Mel is already open: "7001"')
        pass
    else:
        logger.info('Close Port: "7001" for Mel')
        cmds.commandPort(name=':7001', sourceType='mel', echoOutput=True, close=True)
    
        
    # Python port control
    if open_port and not python_port_state:
        cmds.commandPort(name=':7002', sourceType='python', echoOutput=True)
    elif open_port and mel_port_state:
        logger.info('Port for Python is already open: "7002"')
        pass
    else:
        cmds.commandPort(name=':7002', sourceType='python', echoOutput=True, close=True)


def reset_session_for_script(user_path=None):
    if user_path is None:
        user_path = Path(os.path.dirname(__file__)).parent.parent
        
    to_delete = list()
    for key, module in list(sys.modules.items()):
        try:
            module_file_path = inspect.getfile(module).lower()
            if module_file_path == __file__.lower():
                continue
            
            if module_file_path.startswith(str(user_path)):
                logger.debug("Removing {}".format(key))
                to_delete.append(key)
        except:
            pass
        
    for module in to_delete:
        del sys.modules[module]