from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


TITLE = "Hair Tool Supporter"
NAME = "{}".format("_".join(TITLE.lower().split()))

PROJECT = "shenron"

TOOL_NAME = "{} {}".format(PROJECT, TITLE)

CLASS_NAME = "".join(TITLE.split())

TOOL_CATEGORY = "Maya"

TOOL_VERSION = 'v2022.09.15'

BUTTONS = {
            'colorButtonA': [85, 170, 255],
            'colorButtonB': [255, 85, 127],
            'colorButtonC': [255, 170, 127],
            'colorButtonD': [85, 85, 255],
            'colorButtonE': [170, 170, 255],
            'colorButtonF': [170, 255, 127],
            'colorButtonG': [255, 255, 127],
            'colorButtonH': [255, 170, 0],
            'colorButtonI': [214, 65, 3],
            'colorButtonJ': [144, 221, 72],
            }

FILE_NODE_NAME = 'file_node'
FILE_PATH_NAME = 'file_path'
IMAGE_FILE_TYPES = ["tga",
                    "png",
                    "jpg",
                    "jpeg",
                    "tif",
                    "tiff",
                    ]
TEXTURE_FILE_TYPES = {"depth": "depthTexture",
                        "alpha": "alphaTexture",
                    }