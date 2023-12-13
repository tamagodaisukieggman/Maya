import logging
import studiolibrary
from P4 import P4, P4Exception
from tatool.log import ToolLogging, Stage

POSE_LIB_DIR = "//mtk/main/tool_resources/studiolibrary/..."

tool_title = 'Studio Library'
ToolLogging = ToolLogging(projects='mutsunokami',
                          toolcategory='Maya',
                          target_stage=Stage.pr,
                          tool_version='2.9.6.b3')
logger = ToolLogging.getTemplateLogger(tool_title)

# マルチカウントインポートによる重複ハンドリングの増加に対応
logger.handlers = []
logger.addHandler(ToolLogging.get_streamhandler(tool_title, level=logging.DEBUG))
logger.addHandler(ToolLogging.get_fluent_send_handler(tool_title, level=logging.DEBUG))
logger.propagate = False
logger.setLevel(logging.INFO)


def sync_pose_data() -> None:
    try:
        logger.debug("Accessing P4 to sync pose library files.")
        p4 = P4()
        p4.connect()
        p4.run("sync", POSE_LIB_DIR)
        logger.info("Pose library files up to date.")
        p4.disconnect()
    except P4Exception:
        # logger.warning("Upading pose library is failed @ {}".format(POSE_LIB_DIR))
        for e in p4.errors: logger.error(e)
    
    
def main():
    logger.send_launch("Studio Library is launching...")
    sync_pose_data()
    studiolibrary.main()