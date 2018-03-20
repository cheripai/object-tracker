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
            if category in category_file:
                if file_id in category_file[category]:
                    category_file[category][file_id].append(line)
                else:
                    category_file[category][file_id] = [line]
            else:
                category_file[category] = {file_id: [line]}
    return category_file, header


def get_num_annotations(category_dict):
    return sum([1 for file_id in category_dict for annotation in category_dict[file_id]])


if __name__ == "__main__":
    category_file, header = get_category_file_dict(sys.argv[1])

    num_annotations_category = [(get_num_annotations(category_file[category]), category)
                                for category in category_file.keys()]
    num_annotations_category = sorted(num_annotations_category, reverse=True)
    min_annotations = num_annotations_category[-1][0]

    for _, cur_category in num_annotations_category:
        num_annotations = get_num_annotations(category_file[cur_category])
        fnames = list(category_file[cur_category].keys())
        shuffle(fnames)
        i = 0
        while num_annotations > min_annotations:
            num_annotations = get_num_annotations(category_file[cur_category])
            for c in category_file.keys():
                min_annotations = min(get_num_annotations(category_file[c]), min_annotations)
                if fnames[i] in category_file[c]:
                    del category_file[c][fnames[i]]
            i += 1

    annotations = []
    for category in category_file.keys():
        num_annotations = 0
        for file_id in category_file[category]:
            for annotation in category_file[category][file_id]:
                num_annotations += 1
                annotations.append(annotation)
        print(category, len(category_file[category]), num_annotations)

    shuffle(annotations)
    annotations.insert(0, header)

    with open(sys.argv[2], "w+") as f:
        for annotation in annotations:
            f.write(annotation + "\n")
