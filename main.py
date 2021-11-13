import xml.etree.ElementTree as ET
from pathlib import PureWindowsPath

tree = ET.parse('categories.xml')
root = tree.getroot()

paths = []
for category in root.findall("CategoryModel"):
    for element in category.iter("ProtocolModel"):
        protocolpath = element.get("FileName")
        paths.append(protocolpath)
purepaths = map(PureWindowsPath, paths)

#with open("JAA_ProtocolFilePaths.txt", "w") as out:
#    for i in sorted(purepaths):
#        out.write(f"{str(i.name)}\n")
for path in sorted(purepaths):
    print(path)



