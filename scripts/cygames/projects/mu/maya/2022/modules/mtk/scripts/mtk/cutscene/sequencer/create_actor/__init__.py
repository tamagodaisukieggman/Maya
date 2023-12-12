from . import controller
from .app import ActorCreator


def show_actor_option(sequencer):
    """option起動のエントリーポイント
    """
    global create_actor_controller

    try:
        create_actor_controller.close_option()
    except Exception:
        pass
    create_actor_controller = controller.CreateActorController(sequencer)
    create_actor_controller.show_option()

    return create_actor_controller
