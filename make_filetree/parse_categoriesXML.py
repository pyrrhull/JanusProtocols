import xml.etree.ElementTree as ET
from pathlib import PureWindowsPath, Path
from shutil import copy2

tree = ET.parse('../protocols/Categories.xml')
root = tree.getroot()

with open("Categories.csv", "w") as f:
    for cat in root.findall("CategoryModel"):
        category = cat.get("Name")
        for element in cat.iter("ProtocolModel"):
            description = element.get("Description")
            fullpath = PureWindowsPath(element.get("FileName"))
            f.write(f'{category}\t{str(fullpath)}\t{fullpath.name}\t{description}\r')

#with open("JAA_ProtocolFilePaths.txt", "w") as out:
#    for i in sorted(purepaths):
#        out.write(f"{str(i.name)}\n")
# for path in sorted(purepaths):
#     print(path)



