def create_unique_name(base_name, string_list):
    """固有のオブジェクト名を作成する

    :param base_name: 生成する名前のベース名
    :type base_name: str
    :param search_type: 検索するノード名
    :type base_name: str
    :return: 存在しなければ、base_name, 存在していれば、[base_name]_[1, 2 ,3etc]
    :rtype: str
    """
    hit_names = [_ for _ in string_list if base_name in _]
    if hit_names != []:
        unique_name = "{}_{}".format(base_name, len(hit_names))
        return unique_name
    else:
        return base_name
