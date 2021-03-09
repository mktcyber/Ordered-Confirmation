import json
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


def write(data, format):
    """
    Writes the given data into a file in the directory from which this call was made.
    Where data must be a dictionary; and format must be either "json", or "xml".

    Returns the response which has been writen to the file.
    """
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