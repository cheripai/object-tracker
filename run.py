import sys
import os
import numpy as np
from PIL import Image
import src.siamese as siam
from src.tracker import tracker
from src.parse_arguments import parse_arguments
from src.region_to_bbox import region_to_bbox


def main():
    # avoid printing TF debugging information
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    # TODO: allow parameters from command line or leave everything in json files?
    hp, evaluation, run, env, design = parse_arguments()
    # Set size for use with tf.image.resize_images with align_corners=True.
    # For example,
    #   [1 4 7] =>   [1 2 3 4 5 6 7]    (length 3*(3-1)+1)
    # instead of
    # [1 4 7] => [1 1 2 3 4 5 6 7 7]  (length 3*3)
    final_score_sz = hp.response_up * (design.score_sz - 1) + 1
    # build TF graph once for all
    filename, image, templates_z, scores = siam.build_tracking_graph(final_score_sz, design, env)

    initial_bboxes, frame_name_list, _ = _init_video(env, evaluation, evaluation.video)
    start_frame, pos_x, pos_y, target_w, target_h = initial_bboxes[0]
    bboxes, speed = tracker(hp, run, design, frame_name_list, pos_x, pos_y, target_w, target_h, final_score_sz,
                            filename, image, templates_z, scores, start_frame)
    start_frame, pos_x, pos_y, target_w, target_h = initial_bboxes[1]
    bboxes, speed = tracker(hp, run, design, frame_name_list, pos_x, pos_y, target_w, target_h, final_score_sz,
                            filename, image, templates_z, scores, start_frame)


def _init_video(env, evaluation, video):
    video_folder = os.path.join(env.root_dataset, video)
    frame_name_list = [f for f in os.listdir(video_folder) if f.endswith(".jpg")]
    frame_name_list = [os.path.join(env.root_dataset, video, '') + s for s in frame_name_list]
    frame_name_list.sort()
    with Image.open(frame_name_list[0]) as img:
        frame_sz = np.asarray(img.size)
        frame_sz[1], frame_sz[0] = frame_sz[0], frame_sz[1]

    # read the initialization from ground truth
    init_file = os.path.join(video_folder, 'init.txt')
    initial_bboxes = np.genfromtxt(init_file, delimiter=',')

    if len(initial_bboxes.shape) == 1:
        initial_bboxes = np.expand_dims(initial_bboxes, axis=0)
    return initial_bboxes, frame_name_list, frame_sz


if __name__ == '__main__':
    sys.exit(main())
