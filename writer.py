import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


def write(data, format):
    assert format == "json" or format == "xml"
    if format == "json":
        receipt_json = json.dumps(data, separators=(',', ': '), indent=4)
        with open("invoice.json", "wt") as json_file:
            json_file.write(receipt_json)
        return receipt_json
    else:
        raw_xml = dicttoxml(data, custom_root="invoice", attr_type=False)
        receipt_xml = parseString(raw_xml).toprettyxml()
        with open("invoice.xml", "wt") as xml_file:
            xml_file.write(receipt_xml)
        return receipt_xml