import os
import sys
from random import shuffle


def get_category_file_dict(csv_path):
    category_file = {}
    with open(csv_path) as f:
        header = f.readline().strip()
        for line in f.readlines():
            line = line.strip()
            fname, width, height, category, xmin, ymin, xmax, ymax = line.split(",")
            file_id = os.path.basename(fname)
            if category in ignore:
                continue
            if category in category_file:
                if file_id in category_file[category]:
                    category_file[category][file_id].append(line)
                else:
                    category_file[category][file_id] = [line]
            else:
                category_file[category] = {file_id:[line]}
    return category_file, header

if __name__ == "__main__":
    category_file, header = get_category_file_dict(sys.argv[1])

    images_per_category = sorted([(len(category_file[category]), category) for category in category_file.keys()], reverse=True)
    min_images = images_per_category[-1][0]

    for _, category in images_per_category:
        if len(category_file[category]) > min_images:
            fnames = list(category_file[category].keys())
            shuffle(fnames)
            for i in range(len(fnames) - min_images):
                for category in category_file.keys():
                    if fnames[i] in category_file[category]:
                        del category_file[category][fnames[i]]

    annotations = []
    for category in category_file.keys():
        num_annotations = 0
        for file_id in category_file[category]:
            for annotation in category_file[category][file_id]:
                num_annotations += 1
                annotations.append(annotation)
        print(category, len(category_file[category]), num_annotations)

    annotations.insert(0, header)
    
    with open(sys.argv[2], "w+") as f:
        for annotation in annotations:
            f.write(annotation + "\n")
