import xml.etree.ElementTree as ET
from collections import defaultdict, namedtuple
from pathlib import PureWindowsPath, Path
from shutil import copy2

janusdir = Path('C:\\Packard\\Janus\\')

#xmlns:xsi= xmlns:xsd
attr_qname = ET.QName("http://www.w3.org/2001/XMLSchema", "xsd")

nsmap = {'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

Protocol = namedtuple("Protocol", "name path")
protocols = defaultdict(list)

with open("categoriesxml2csv.csv") as f:
    for line in f.readlines():
        abteilung, fullpath, name = line.strip().split(',')
        p = Protocol(Path(name), Path(fullpath))
        protocols[abteilung].append(p.name)
        (janusdir / "Protocols" / Path(abteilung)).mkdir(exist_ok=True)  # create Folder foreach Abteilung or Category

root = ET.Element('ArrayOfCategoryModel', {"xlmns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "xlmns:xsd": "http://www.w3.org/2001/XMLSchema"})
for cat in protocols.keys():
    destinationdir = janusdir / "Protocols_new" / cat
    category = ET.SubElement(root, 'CategoryModel', Name=cat)
    treeview = ET.SubElement(category, "TreeView")
    treeview.text = "true"
    protocollist = ET.SubElement(category, "ProtocolList")
    for p in protocols[cat]:
        #copy protocol to new folder
        file = list(janusdir.rglob(p.name))
        if len(file) > 1:
            print(f"Duplicates found for, {p}, {list(file)}")
        copy2(file[0], destinationdir)
        protocolmodel = ET.SubElement(protocollist,
                                      "ProtocolModel",
                                      ID='',
                                      FileName=str(destinationdir / p.name),
                                      Description="",
                                      LastRunDate='')


tree = ET.ElementTree(root)
ET.indent(tree, space='\t', level=0)
tree.write('newCategories.xml', xml_declaration=True, encoding="utf-8")
