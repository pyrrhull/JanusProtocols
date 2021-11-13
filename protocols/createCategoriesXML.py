import xml.etree.ElementTree as ET
from pathlib import PureWindowsPath

tree = ET.parse('Categories_new.xml')

root = tree.getroot()

with open('filelist.csv', 'w') as file:
    for model in root.iter('CategoryModel'):
        m = model.attrib['Name']
        for lst in model.iter('ProtocolModel'):
            filepath = lst.attrib['FileName']
            filename = PureWindowsPath(filepath).name
            file.writelines(f'{m},{filename}\n')


