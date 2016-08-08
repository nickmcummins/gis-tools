from urllib.request import urlopen

from bs4 import BeautifulSoup

from scrappers.wavegbuildings.buildinggroup import BuildingGroup

if __name__ == '__main__':
    print("Hello!")
    html = urlopen("http://www.nickmcummins.com/waveg-buildings.html")
    bsObj = BeautifulSoup(html, "lxml")
    bldg_group = bsObj.find("h2", {"id": "wa_seattle"}).findNext()
    buildings = BuildingGroup(bldg_group)

    file = open("/home/nick/GPS/waveg-buildings.gpx", "w")
    file.write(buildings.to_gpx())
    file.close()
