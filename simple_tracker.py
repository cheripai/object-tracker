import numpy as np
import cv2
import sys
from scipy.misc import imsave

TOMATO_INIT = (636, 392, 66, 66)
BOWL_INIT = (424, 340, 104, 84)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Input video name is missing')
        exit()

    cv2.namedWindow("tracking")
    camera = cv2.VideoCapture(sys.argv[1])
    tracker = cv2.MultiTracker_create()
    init_once = False

    ok, image = camera.read()
    if not ok:
        print('Failed to read video')
        exit()

    i = 1
    while camera.isOpened():
        ok, image = camera.read()
        if not ok:
            print('no image to read')
            break

        # Start timer
        timer = cv2.getTickCount()

        if not init_once:
            ok = tracker.add(cv2.TrackerKCF_create(), image, TOMATO_INIT)
            ok = tracker.add(cv2.TrackerKCF_create(), image, BOWL_INIT)
            init_once = True

        ok, boxes = tracker.update(image)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        for newbox in boxes:
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(image, p1, p2, (200, 0, 0))

        # Display FPS on frame
        cv2.putText(image, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.imshow('tracking', image)
        i += 1

        k = cv2.waitKey(1)
        if k == 27: break  # esc pressed
