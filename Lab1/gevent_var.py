import xml.etree.ElementTree as ET
from urllib.request import urlopen
import time
import collections
import gevent

counter = collections.Counter()


def find_all_indexes(input_str, search_str):
    amount = 0
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return amount
        amount += 1
        index = i + 1
    return amount


def insert(source: str):
    if (not isinstance(source, type(None))):
        for key in counter:
            counter[key] += find_all_indexes(source.upper(), key)


def thread(rss):
    for item in rss.iterfind('channel/item'):
        title = item.findtext('title')
        description = item.findtext('description')
        fulltext = item.findtext('fulltext')
        insert(title)
        insert(description)
        insert(fulltext)


def create_xml(filename):
    root = ET.Element("info")
    places = ET.Element("places")
    root.append(places)
    for key in counter:
        if counter[key] == 0:
            continue
        place = ET.SubElement(places, "place")
        name = ET.SubElement(place, "name")
        name.text = key
        amount = ET.SubElement(place, "amount")
        amount.text = str(counter[key])

    tree_str = ET.tostring(root, 'utf-8')
    content = '' + tree_str.decode('utf-8')
    output = open(filename, 'w')
    output.write(content)


def main():
    mytree = ET.parse('res/source.xml')
    myroot = mytree.getroot()
    places_list = open('res/input.txt')
    for line in places_list:
        line = line.replace('\n', '')
        counter[line] = 0
    threads = []
    start_time = time.time()
    for url in list(myroot):
        var_url = urlopen(url.text)
        xml_doc = ET.parse(var_url)
        threads.append(gevent.spawn(thread, xml_doc))
    gevent.joinall(threads)
    end = time.time() - start_time
    print(end)
    create_xml("output/output.xml")


if __name__ == "__main__":
    main()
