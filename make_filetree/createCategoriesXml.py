import xml.etree.ElementTree as ET
from collections import defaultdict, namedtuple
from pathlib import PureWindowsPath, Path
from shutil import copy2

janusdir = Path('C:\\Packard\\Janus\\')

#xmlns:xsi= xmlns:xsd
attr_qname = ET.QName("http://www.w3.org/2001/XMLSchema", "xsd")

nsmap = {'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

Protocol = namedtuple("Protocol", "new_folder category old_path protocol description")
protocols = defaultdict(list) # dict[category] = [Protocol, Protocol,....]
categories_order = ['Analytik',
                    'Analytik_NO_CSV',
                    'Mutationsanalytik',
                    'Pooling',
                    'Pooling Low Volume',
                    'Pooling Replacement',
                    'TeamGuM',
                    'Analytik_Backup',
                    'Pooling_Backup',
                    'TEST_NO SCAN WITH BACKUP AND EMPTY BC',
                    'TEST_ROTATED',
                    ]

with open("Categories_edited.csv") as f:
    header = f.readline()
    for line in f.readlines():
        new_folder, category, old_path, protocol, description, used = line.strip().split('\t')
        p = Protocol(Path(new_folder), category, Path(old_path), protocol, description)
        protocols[category].append(p)
        (janusdir / "Protocols_new" / Path(new_folder)).mkdir(exist_ok=True, parents=True)  # create Folder foreach Abteilung or Category

root = ET.Element('ArrayOfCategoryModel', {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "xmlns:xsd": "http://www.w3.org/2001/XMLSchema"})
for category in categories_order:
    categorymodel = ET.SubElement(root, 'CategoryModel', Name=category)
    treeview = ET.SubElement(categorymodel, "TreeView")
    treeview.text = "true"
    protocollist = ET.SubElement(categorymodel, "ProtocolList")
    for p in protocols[category]:
        #copy protocol to new folder
        destinationdir = janusdir / "Protocols_new" / p.new_folder
        file = list(janusdir.rglob(p.protocol))
        if len(file) > 1:
            print(f"Duplicates found for {p.protocol} => {[str(x) for x in list(file)]}")
        try:
            copy2(file[0], destinationdir)
            protocolmodel = ET.SubElement(protocollist,
                                          "ProtocolModel",
                                          ID='',
                                          FileName=str(destinationdir / p.protocol),
                                          Description=p.description,
                                          LastRunDate='0001-01-01T00:00:00')
        except IndexError:
            print(p.protocol, " not found")
showtreeview = ET.SubElement(root, "ShowTreeView")
showtreeview.text = "True"
tree = ET.ElementTree(root)
ET.indent(tree, space='\t', level=0)
tree.write('Categories_new.xml', xml_declaration=True, encoding="utf-8")
