def insert_motion_show_option():
    """option起動のエントリーポイント
    """
    from . import controller

    global insert_animation_controller

    try:
        insert_animation_controller.close_option()
    except Exception:
        pass
    insert_animation_controller = controller.InsertAnimationController()
    insert_animation_controller.show_option()

    return insert_animation_controller
