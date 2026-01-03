import yaml
import xml.etree.ElementTree as xml_tree
import requests

with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

rss_element = xml_tree.Element('rss', {'version': '2.0'})
channel_element = xml_tree.SubElement(rss_element, 'channel')

xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'link').text = yaml_data['link']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']

# Pull CS jobs from RSS feed
feed = xml_tree.fromstring(
    requests.get('https://weworkremotely.com/categories/remote-programming-jobs.rss').content
)

for item in feed.findall('./channel/item'):
    item_element = xml_tree.SubElement(channel_element, 'item')

    xml_tree.SubElement(item_element, 'title').text = item.find('title').text
    xml_tree.SubElement(item_element, 'link').text = item.find('link').text
    xml_tree.SubElement(item_element, 'description').text = item.find('description').text
    xml_tree.SubElement(item_element, 'pubDate').text = item.find('pubDate').text

output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('jobsfeed.xml', encoding='UTF-8', xml_declaration=True)
