# Source: https://github.com/datitran/raccoon_dataset.git

import os
import shutil
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from random import shuffle

VALID_PROP = 0.1

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    path = sys.argv[1]
    image_paths = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('xml')]
    shuffle(image_paths)
    split = int(len(image_paths) * VALID_PROP)
    image_sets = {'train': image_paths[split:], 'valid': image_paths[:split]}

    for directory in ('train', 'valid'):
        set_path = os.path.join(path, directory)
        if not os.path.exists(set_path):
            os.mkdir(set_path)
        for image_path in image_sets[directory]:
            fname = os.path.basename(image_path).split('.')[0]
            shutil.copyfile(image_path, os.path.join(set_path, fname+'.xml'))
            shutil.copyfile(image_path.replace('.xml', '.JPEG'), os.path.join(set_path, fname+'.JPEG'))
        xml_df = xml_to_csv(set_path)
        xml_df.to_csv('{}/{}.csv'.format(set_path, directory), index=None)
    print('Successfully converted xml to csv.')

main()
