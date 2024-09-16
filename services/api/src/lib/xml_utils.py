import re
import xml.dom.minidom


def trim_xml(xml_string):
    return re.sub(r">\s+<", "><", xml_string.strip())


def format_xml(xml_string):
    # Remove any whitespace between tags
    xml_string = trim_xml(xml_string)

    # Parse the XML string to dom object
    dom = xml.dom.minidom.parseString(xml_string)

    # Pretty-print the XML
    pretty_xml_as_string = dom.toprettyxml(indent="    ", newl="\n")

    # Remove the XML declaration
    pretty_xml_as_string = "\n".join(pretty_xml_as_string.split("\n")[1:])

    return pretty_xml_as_string


if __name__ == "__main__":
    # Example usage
    xml_string = """ <root>
    <child> <data>value is this</data> </child>




    </root> """

    print("raw:", xml_string)
    trimmed_xml = trim_xml(xml_string)
    print("trimmed:", trimmed_xml)
    formatted_xml = format_xml(xml_string)
    print("formatted:", formatted_xml)
