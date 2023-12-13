import yaml

# シェーダ名・シェーダ説明リスト
shader_list = []

# シェーダ説明リスト
shader_description_list = []

# シェーダ設定yaml を読み込む
with open("Z:/mtk/config/model_editor/change_shader/shader_prefs.yaml", "rb") as file:
    shader_prefs = yaml.load(file)

# シェーダ情報
shader_info = shader_prefs["shader_info"]

for shader, info in shader_info.items():

    # シェーダのタグ情報に「Env」が含まれる場合（デカール以外）
    if "Env" in info["tags"] and "Decal" not in info["tags"]:
        shader_list.append(shader)
        shader_list.append(info["description"])

for shader in shader_list:
    print(shader)