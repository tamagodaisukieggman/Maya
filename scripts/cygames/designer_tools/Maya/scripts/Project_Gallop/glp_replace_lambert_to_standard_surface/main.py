# -*- coding: utf-8 -*-

from . import model
from importlib import reload

reload(model)


class Main(object):

    def __init__(self):
        pass

    def replace_lambert_to_standard_surface(self):
        """lambertシェーダーをStandardSurfaceシェーダーに置き換える
        """

        model.replace_lambert_to_standard_surface()


if __name__ == '__main__':

    main = Main()
    main.replace_lambert_to_standard_surface()
