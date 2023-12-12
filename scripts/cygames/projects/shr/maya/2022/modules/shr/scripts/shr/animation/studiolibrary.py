import logging
import studiolibrary

# from P4 import P4, P4Exception
import tool_log

POSE_LIB_DIR = "C:/cygames/shrdev/shr_art/tool_resources/studiolibrary/...."
logger = tool_log.get_logger("ta_studiolibrary", "v2022.10.25")


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
        for e in p4.errors:
            logger.error(e)


def main():
    # ログ送信
    logger.send_launch("")

    # sync_pose_data()
    studiolibrary.main(name="shr_studiolibrary", path=POSE_LIB_DIR)
