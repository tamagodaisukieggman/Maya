# -*- coding: utf-8 -*-

from __future__ import absolute_import


ANIM_CURVE_T = ('animCurveTA', 'animCurveTL', 'animCurveTT', 'animCurveTU')
"""animCurveTのノードタイプ
"""

ANIM_CURVE_U = ('animCurveUA', 'animCurveUL', 'animCurveUT', 'animCurveUU')
"""animCurveUのノードタイプ
"""

ANIM_CURVE_TANGENT_TYPES = {
    1: 'Fixed', 2: 'Linear', 3: 'Flat', 5: 'Step', 6: 'Slow', 7: 'Fast',
    9: 'Spline', 10: 'Clamped', 16: 'Plateau', 17: 'StepNext', 18: 'Auto'
}
"""animCurveのタンジェントタイプ
"""

UNIT_CONVERSION = ('unitConversion', 'timeToUnitConversion', 'unitToTimeConversion')
"""unitConversionノードタイプ
"""

IDENTITY_MATRIX = (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)
"""単位行列 (float16)
"""

THUMBNAIL_WIDTH = 200
"""サムネイル幅
"""

THUMBNAIL_HEIGHT = 200
"""サムネイル高さ
"""

TRANSFORMATION_CHANNELS = (
    'translateX', 'translateY', 'translateZ',
    'rotateX', 'rotateY', 'rotateZ',
    'scaleX', 'scaleY', 'scaleZ',
)
"""トランスフォームチャンネル
"""

KEY_TANGENT_FLAGS = ('inAngle', 'outAngle', 'inWeight', 'outWeight', 'ix', 'ox', 'iy', 'oy')
"""keyTangentコマンドフラグ
"""
