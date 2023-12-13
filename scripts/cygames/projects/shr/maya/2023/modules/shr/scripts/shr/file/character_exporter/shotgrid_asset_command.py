import shotgun_api3 as shotgun

SCRIPT_NAME = "shr_shotgrid_tool"
API_KEY = r"mtgzpax5ha%icildaxgazNgjj"
HOSTNAME = "https://cygames.shotgunstudio.com"


class sg_asset_tools:
    def __init__(self):
        self.sg = shotgun.Shotgun(HOSTNAME, script_name=SCRIPT_NAME, api_key=API_KEY)
        project_name = "shenron"
        self.project = self.sg.find_one("Project", [["name", "is", project_name]])

    def get_asset(self, asset_type, fields):
        assets = self.sg.find(
            "Asset",
            [["project", "is", self.project], ["sg_asset_type", "is", asset_type]],
            fields,
        )
        return assets

    def find_asset_id_by_name(self, asset_name, asset_type=None, get_type="id"):
        filters = [
            ["project", "is", self.project],
            ["code", "is", asset_name],
        ]

        if asset_type != None:
            filters.append(["sg_asset_type", "is", asset_type])

        asset = self.sg.find_one(
            "Asset",
            filters,
            ["id", "code"],
        )
        if asset == None:
            return None

        if get_type == "id":
            return asset["id"]
        elif get_type == "asset":
            print(type(asset))
            return asset

    def update_parent_field(self, id, update_data):
        return self.sg.update("Asset", entity_id=id, data={"parents": update_data})

    def get_character_parent_assets(self, asset_name) -> list:
        parents = []
        for lp in self.get_asset("Character", ["id", "code", "parents"]):
            if lp["code"] == asset_name:
                try:
                    parents = lp["parents"]
                except KeyError:
                    continue
        return parents

    def get_skeleton_asset(self, asset_name):
        for lp in self.get_asset("Skeleton", ["id", "code"]):
            if lp["code"] == asset_name:
                return lp

    def get_character_skeleton_name(self, asset_name):
        parents = self.get_character_parent_assets(asset_name)
        for parent in parents:
            parent_asset_data = self.sg.find_one(
                "Asset",
                [
                    ["project", "is", self.project],
                    ["id", "is", parent["id"]],
                ],
                ["code", "sg_asset_type"],
            )
            if parent_asset_data["sg_asset_type"] == "Skeleton":
                return parent_asset_data["code"]
        return None

    def create_asset(self, asset_name, asset_type, description=""):
        if self.find_asset_id_by_name(asset_name, "Skeleton") != None:
            return 0
        # ShotgunにAssetを作成します
        data = {
            "code": asset_name,
            "sg_asset_type": asset_type,
            "description": description,
            "project": self.project,
        }
        return self.sg.create(entity_type="Asset", data=data)

    def list_asset_fields(self):
        return
