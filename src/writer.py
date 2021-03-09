import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import os


def write(data, format):
    """
    Writes the given data into a file in the directory from which this call was made.
    Where data must be a dictionary; and format must be either "json", or "xml".

    Returns the response which has been writen to the file.
    """
    assert format == "json" or format == "xml"
    parent_dir = os.path.dirname(__file__)
    if format == "json":
        response_json = json.dumps(data, separators=(',', ': '), indent=4)
        with open(os.path.join(parent_dir, "output", "invoice.json"), "wt") as json_file:
            json_file.write(response_json)
        return response_json
    else:
        raw_xml = dicttoxml(data, custom_root="invoice", attr_type=False)
        response_xml = parseString(raw_xml).toprettyxml()
        with open(os.path.join(parent_dir, "output", "invoice.xml"), "wt") as xml_file:
            xml_file.write(response_xml)
        return response_xml