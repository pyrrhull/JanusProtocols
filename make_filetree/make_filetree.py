import xml.etree.ElementTree as ET
from pathlib import PureWindowsPath, Path
from shutil import copy2

sourcedir = 'C:\\Packard\\Janus\\'

tree = ET.parse('')
root = tree.getroot()

paths = []
for category in root.findall("CategoryModel"):
    destination = category.get("Name") 
    Path(destination).mkdir(exist_ok=True)
    for element in category.iter("ProtocolModel"):
        fullpath = element.get("FileName")
        try:
            copy2(fullpath, destination)
        except FileNotFoundError:
            print('{} not found'.format(fullpath))
        # paths.append(protocolpath)
purepaths = map(PureWindowsPath, paths)

#with open("JAA_ProtocolFilePaths.txt", "w") as out:
#    for i in sorted(purepaths):
#        out.write(f"{str(i.name)}\n")
# for path in sorted(purepaths):
#     print(path)



