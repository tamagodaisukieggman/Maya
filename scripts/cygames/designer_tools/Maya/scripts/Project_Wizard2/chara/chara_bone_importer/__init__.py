from .app import BoneImporter


def exec_import_only():
    """特定のパスの骨をインポート"""
    bone_importer = BoneImporter()
    bone_importer.execute(is_import_only=True)

def exec_recreate_bone():
    """特定のパスの骨をインポート"""
    bone_importer = BoneImporter()
    bone_importer.execute(is_import_only=False)