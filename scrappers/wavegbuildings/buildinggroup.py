class BuildingGroup:
    def __init__(self, bs_obj):
        self.buildings = []
        self.bs_obj = bs_obj

    @staticmethod
    def from_bs(bldg_group_bs):
        building_group = BuildingGroup(bldg_group_bs)
        building_group.parse()
        return building_group

    def parse(self):
        bldgs_bs = self.bs_obj.findAll("a", {"class": "bldg_title"})
        buildings = []
        for building in bldgs_bs:
            buildings.append(building.text)

        self.buildings = buildings

    def __str__(self):
        return str('\n'.join(self.buildings))
