import xml.etree.ElementTree as ET
from pathlib import PureWindowsPath, Path
from shutil import copyfile

tree = ET.parse('../protocols/Categories_new.xml')
root = tree.getroot()

paths = []
for category in root.findall("CategoryModel"):
    destination = category.get("Name") 
    Path(destination).mkdir(exist_ok=True)
    for element in category.iter("ProtocolModel"):
        protocolpath = element.get("FileName")
        copyfile(protocolpath, destination)
        # paths.append(protocolpath)
purepaths = map(PureWindowsPath, paths)

#with open("JAA_ProtocolFilePaths.txt", "w") as out:
#    for i in sorted(purepaths):
#        out.write(f"{str(i.name)}\n")
# for path in sorted(purepaths):
#     print(path)



