import unittest

from bs4 import BeautifulSoup

from scrappers.wavegbuildings import BuildingGroup


class BuildingGroupTest(unittest.TestCase):
    def test_parse(self):
        soup = BeautifulSoup(open("waveg-buildings.html"), "lxml")
        self.assertEquals(len(BuildingGroup.parse(soup)), 384)


if __name__ == "__main__":
    unittest.main()
