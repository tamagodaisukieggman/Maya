from .controller import PropertyEditor


def main(controller, track_data):
    base = PropertyEditor(controller, track_data)
    base.execute()
    return base
