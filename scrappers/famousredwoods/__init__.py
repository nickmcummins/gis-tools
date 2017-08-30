import glob
from lxml import etree

from gpxpy.gpx import GPX

from scrappers.famousredwoods.redwoodhtmlpage import RedwoodHTMLPage

if __name__ == '__main__':
    redwood_html_pages = []
    redwood_html_pages += glob.glob("/misc/website-dl/famousredwoods.com/*.html")
    redwood_html_pages += glob.glob("/misc/website-dl/famousredwoods.com/*/index.html")

    gpx = GPX()

    for html_file in redwood_html_pages:
        try:
            redwood_html_page = RedwoodHTMLPage(html_file)
            gpx.waypoints.append(redwood_html_page.to_gpx_trackpoint())
        except (IndexError, AttributeError):
            print("Skipping " + html_file)

    gpx_string = etree.tostring(
        etree.fromstring(gpx.to_xml().encode('utf-8'), parser=etree.XMLParser(encoding='utf-8')),
        pretty_print=True).decode('utf-8')

    gpx_file = open('famousredwood-trees-with-descriptions.gpx', 'w')
    gpx_file.write(gpx_string)
