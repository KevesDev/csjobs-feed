import xml.etree.ElementTree as xml_tree
import requests
import re

RSS_SOURCE = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
OUTPUT_FILE = "jobsfeed.xml"

def strip_html(html):
    if not html:
        return ""
    return re.sub(r"<[^>]+>", "", html).strip()

# Fetch source RSS
source_feed = xml_tree.fromstring(requests.get(RSS_SOURCE).content)

# Create new RSS
rss_element = xml_tree.Element("rss", {"version": "2.0"})
channel = xml_tree.SubElement(rss_element, "channel")

xml_tree.SubElement(channel, "title").text = "CS Jobs Feed"
xml_tree.SubElement(channel, "link").text = "https://kevesdev.github.io/csjobs-feed/"
xml_tree.SubElement(channel, "description").text = "Remote computer science and programming jobs"
xml_tree.SubElement(channel, "language").text = "en-us"

# Copy items
for item in source_feed.findall("./channel/item"):
    new_item = xml_tree.SubElement(channel, "item")

    xml_tree.SubElement(new_item, "title").text = item.findtext("title")
    xml_tree.SubElement(new_item, "link").text = item.findtext("link")
    xml_tree.SubElement(
        new_item,
        "description"
    ).text = strip_html(item.findtext("description"))
    xml_tree.SubElement(new_item, "pubDate").text = item.findtext("pubDate")

# Write output
tree = xml_tree.ElementTree(rss_element)
tree.write(OUTPUT_FILE, encoding="UTF-8", xml_declaration=True)
