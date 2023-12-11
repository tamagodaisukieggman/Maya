# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass

class KDTree(object):

    def __init__(self, data_list, position_getter, k, depth=0):

        self.position_getter = position_getter

        self.axis = depth % k

        self.data = None
        self.left = None
        self.right = None

        if data_list:
            copy_data_list = data_list[:]
            copy_data_list.sort(key=lambda x: self.position_getter(x)[self.axis])
            index = len(copy_data_list) // 2

            self.data = copy_data_list[index]
            self.left = KDTree(copy_data_list[:index], self.position_getter, k, depth + 1)
            self.right = KDTree(copy_data_list[index + 1:], self.position_getter, k, depth + 1)

    def search_point(self, point):
        """近傍探索

        Args:
            point (MPoint): 探索する位置

        Returns:
            object: 最近傍点に位置するオブジェクト
        """

        if self.data is None:
            return None

        pos = self.position_getter(self.data)

        best = (self.data, pos.distanceTo(point))

        first, second = (self.left, self.right) if pos[self.axis] > point[self.axis] else (self.right, self.left)

        first_best = first.search_point(point)

        if first_best and first_best[1] < best[1]:
            best = first_best

        if best[1] > abs(point[self.axis] - pos[self.axis]):
            second_best = second.search_point(point)

            if second_best and second_best[1] < best[1]:
                best = second_best

        return best

    def search_radius(self, point, radius):
        """半径探索

        Args:
            point (MPoint): 探索する位置
            radius (float): 探索する頂点からの範囲

        Returns:
            list[object]: 半径内に位置するオブジェクト
        """

        result = []

        if self.data is None:
            return result

        pos = self.position_getter(self.data)

        if pos.distanceTo(point) <= radius:
            result.append(self.data)

        first, second = (self.left, self.right) if pos[self.axis] > point[self.axis] else (self.right, self.left)

        result.extend(first.search_radius(point, radius))

        if radius >= abs(point[self.axis] - pos[self.axis]):
            result.extend(second.search_radius(point, radius))

        return result
