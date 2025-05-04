import os
import xml.etree.ElementTree as ET
import json


OUTPUT_DIR = "out"
INPUT_FILE = "impulse_test_input.xml"


os.makedirs(OUTPUT_DIR, exist_ok=True)


def parse_xml(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    data = {}
    for elem in root:
        class_name = elem.tag
        attributes = {}
        for attr in elem:
            attributes[attr.tag] = attr.text
        data[class_name] = attributes

    return data


def generate_config_xml(data):
    root = ET.Element("Config")

    for class_name, attributes in data.items():
        class_elem = ET.SubElement(root, class_name)
        for attr_name, value in attributes.items():
            attr_elem = ET.SubElement(class_elem, attr_name)
            attr_elem.text = value

    tree = ET.ElementTree(root)
    tree.write(os.path.join(OUTPUT_DIR, "config.xml"), encoding="utf-8", xml_declaration=True)


def generate_meta_json(data):
    meta = {"classes": []}

    for class_name, attributes in data.items():
        class_meta = {
            "name": class_name,
            "attributes": [{"name": attr_name, "type": "string"} for attr_name in attributes.keys()]
        }
        meta["classes"].append(class_meta)

    with open(os.path.join(OUTPUT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=4)


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"File {INPUT_FILE} is missing")
        return

    data = parse_xml(INPUT_FILE)
    generate_config_xml(data)
    generate_meta_json(data)


if __name__ == "__main__":
    main()
