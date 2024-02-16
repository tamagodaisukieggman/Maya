import maya.cmds as cmds
# scaleZのIN開始フレームには1, LOOP開始フレームには2, OUT開始フレームには3が入っている
g_valid_split_values = {1.0, 2.0, 3.0}

def get_first_split_frame():
    """timing_boxに最初に打ってある最初の有効なキーのフレームと値のtupleを返す
    Note: timing_boxは必ずしもIN, LOOP, OUT揃っているとは限らない
    必ずしもIN, LOOP, OUTの順とは限らない
    """
    timing_box = cmds.ls('timing_box', recursive=True)
    if not timing_box:
        return
    timing_box = timing_box[0]
    keyframes = cmds.keyframe(timing_box + '.scaleZ', q=True, time=())
    if not keyframes:
        return
    for frame in keyframes:
        try:
            values = cmds.keyframe(timing_box + '.scaleZ', q=True, time=(frame, frame), eval=True)
        except Exception:
            return
        if values:
            value = values[0]
            # 有効な値は1, 2, 3
            if value in g_valid_split_values:
                return (frame, value)


def get_last_split_frame():
    """timing_boxに最初に打ってある最後の有効なキーのフレームと値のtupleを返す
    """
    timing_box = cmds.ls('timing_box', recursive=True)
    if not timing_box:
        return
    timing_box = timing_box[0]
    keyframes = cmds.keyframe(timing_box + '.scaleZ', q=True, time=())
    if not keyframes:
        return
    keyframes.reverse()
    for frame in keyframes:
        try:
            values = cmds.keyframe(timing_box + '.scaleZ', q=True, time=(frame, frame), eval=True)
        except Exception:
            return
        if values:
            value = values[0]
            # 有効な値は1, 2, 3
            if value in g_valid_split_values:
                return (frame, value)


def get_next_split_frame(cur_frame_value):
    """timing_boxに最初に打ってあるcur_frame_valueの次の有効なキーのフレームと値のtupleを返す
    間違ってtiming_boxがベイクされていたりする場合に備え、同じモーションの連続キーはスキップする
    最後だけ同じモーションタイプが2個続いても返す
    Note: timing_boxは必ずしもIN, LOOP, OUT揃っているとは限らない
    必ずしもIN, LOOP, OUTの順とは限らない
    """
    if not cur_frame_value:
        return
    end_split_frame_value = get_last_split_frame()
    end_frame = end_split_frame_value[0]
    cur_frame = cur_frame_value[0]
    cur_value = cur_frame_value[1]
    timing_box = cmds.ls('timing_box', recursive=True)
    if not timing_box:
        return
    timing_box = timing_box[0]
    keyframes = cmds.keyframe(timing_box + '.scaleZ', q=True, time=(cur_frame, end_frame))
    if not keyframes:
        return
    for frame in keyframes:
        if frame <= cur_frame:
            continue
        values = cmds.keyframe(timing_box + '.scaleZ', q=True, time=(frame, frame), eval=True)
        if values:
            value = values[0]
            # 有効な値は1, 2, 3
            if value in g_valid_split_values:
                # 現在のキーと同じモーションタイプでない、もしくは最後のキーフレームなら返す
                if cur_value != value:
                    return (frame, value)
                elif frame == end_frame:
                    return (frame, value)


def has_loop_split_frame():
    """timing_boxにLOOPのキーが打ってある場合はTrueを返す
    """
    timing_box = cmds.ls('timing_box', recursive=True)
    if not timing_box:
        return False
    timing_box = timing_box[0]
    keyframes = cmds.keyframe(timing_box + '.scaleZ', q=True, time=())
    if not keyframes:
        return False
    for frame in keyframes:
        try:
            values = cmds.keyframe(timing_box + '.scaleZ', q=True, time=(frame, frame), eval=True)
        except Exception:
            return False
        if values:
            value = values[0]
            # LOOPは2
            if value == 2:
                return True
    return False
