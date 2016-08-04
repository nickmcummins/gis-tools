from gpxpy.gpx import GPX
from lxml import etree

from scrappers.wavegbuildings.building import Building


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
        buildings_tag = self.bs_obj.findAll("div", {"class": "bldg_cel"})
        buildings = []
        for building_tag in buildings_tag:
            buildings.append(Building.from_tag(building_tag))

        self.buildings = buildings

    def __str__(self):
        return '\n'.join(list(map(str, self.buildings)))

    def to_gpx(self):
        gpx = GPX()
        for building in self.buildings:
            gpx.waypoints.append(building.to_gpx_trackpoint())

        gpx_xml = gpx.to_xml()
        return etree.tostring(etree.fromstring(gpx_xml.encode('utf-8'),
                              parser=etree.XMLParser(encoding='utf-8')),
                              pretty_print=True).decode('utf-8')


