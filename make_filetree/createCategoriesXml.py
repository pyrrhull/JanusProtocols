import xml.etree.ElementTree as ET
from collections import defaultdict, namedtuple
from pathlib import PureWindowsPath, Path
from shutil import copy2

janusdir = Path('C:\\Packard\\Janus\\')

#xmlns:xsi= xmlns:xsd
attr_qname = ET.QName("http://www.w3.org/2001/XMLSchema", "xsd")

nsmap = {'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

Protocol = namedtuple("Protocol", "new_folder category old_path protocol")
protocols = defaultdict(list)


with open("../Liste_protokolle_test.csv") as f:
    header = f.readline()
    for line in f.readlines():
        new_folder,category, old_path, protocol = line.strip().split(',')
        p = Protocol(Path(new_folder), category, Path(old_path), protocol)
        protocols[category].append(p)
        (janusdir / "Protocols_new" / Path(category)).mkdir(exist_ok=True, parents=True)  # create Folder foreach Abteilung or Category

root = ET.Element('ArrayOfCategoryModel', {"xlmns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "xlmns:xsd": "http://www.w3.org/2001/XMLSchema"})
for category in protocols.keys():
    destinationdir = janusdir / "Protocols_new" / category
    categorymodel = ET.SubElement(root, 'CategoryModel', Name=category)
    treeview = ET.SubElement(categorymodel, "TreeView")
    treeview.text = "true"
    protocollist = ET.SubElement(categorymodel, "ProtocolList")
    for p in protocols[category]:
        #copy protocol to new folder
        file = list(janusdir.rglob(p.protocol))
        if len(file) > 1:
            print(f"Duplicates found for, {p}, {list(file)}")
        try:
            copy2(file[0], destinationdir)
            protocolmodel = ET.SubElement(protocollist,
                                          "ProtocolModel",
                                          ID='',
                                          FileName=str(destinationdir / p.protocol),
                                          Description="",
                                          LastRunDate='')
        except IndexError:
            print(p.protocol, " not found")

tree = ET.ElementTree(root)
ET.indent(tree, space='\t', level=0)
tree.write('newCategories.xml', xml_declaration=True, encoding="utf-8")
