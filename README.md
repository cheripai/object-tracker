# Approaches Attempted
- #### KCF (All OpenCV trackers)
  - Pros
    - Fast performance
    - Ease of use
  - Cons
    - Not robust to occlusion
    - Not robust to changes in orientation
- #### SiamFC
  - Pros
    - Good tracking
  - Cons
    - Not robust to occlusion
    - Not robust to changes in orientation
- #### FasterRCNN
  - Pros
    - Understands what the object is supposed to look like
    - Robust to changes in orientation
  - Cons
    - Not robust to occlusion
    - Requires training data for each object
    - Slower performance
    - Does not take advantage of temporal information
    
# Tracking Approach
KCF was found to be sufficient for test2 when given initial bounding boxes. KCF was preferred over detection as it was more stable (didn't lose track of objects throughout frames) and much faster.

# Detection Approach
This approach took advantage of the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection).

With just the pre-trained model, we see reasonable results on detecting the objects in the image.
![pre-trained model result](https://raw.githubusercontent.com/cheripai/object-tracker/master/doc/stock_detector_api.png)
The model was trained on [COCO](https://cocodataset.org), which is a dataset of 90 classes that include many of the objects that appear in the test videos.
We see that the model also detects objects that we do not desire and does not detect all of the objects that we desire.
As such, I downloaded the relevant object class images from COCO and also some from [OID](https://github.com/openimages/dataset) to perform fine-tuning on only the relevant object classes. Unfortunately, not all of the desired objects were found within the detection datasets and I did not have the time to scrape and hand-label the images for the remaining classes, so they were simply omitted. 

The classes in the dataset are as follows:
- backpack
- bottle
- bowl
- handbag
- orange
- shoes
- suitcase
- tomato

Balancing was performed so that each object class had roughly the same number of images (~500).
Once the dataset was created, I fine-tuned the faster_rcnn_resnet50 model available from the Object Detection API's [model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). Multiple models were tried, but faster_rcnn_resnet50 was chosen due to a good balance between speed and detection performance. With the approriate hardware, faster_rcnn_resnet50 can run at approximately 11 frames per second. Since my hardware is not as powerful, I ran detection on every 4th frame.

# Next Steps
- Adding images of the classes that were not present in the dataset
- Occlusion handling: Since the algorithm is able to detect what objects are present in the image, logic can be added so that certain objects can be inserted into another. For example, we know that a suitcase or a backpack are "carrier" objects. As such, if an object's bounding box intersects with a carrier object's bounding box, we can assume that it is being carried.
- A hybrid method between tracking and detection. For example, the detection algorithm can be run every N frames to spawn the initial bounding boxes for the tracking algorithm. 

# Requirements
- numpy
- opencv-contrib-python
- opencv-python
- Pillow
- scipy

# Install
- Follow object detection [installation guide](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
 ```bash 
# From tensorflow/models/research/
python setup.py sdist
cd slim && python setup.py sdist
```
- Download [weights](https://drive.google.com/file/d/17_avhejr77uZOcxPkohk09YNKZ1yX45m/view?usp=sharing) and place in ```weights/``` directory

# Running
- ```python simple_tracker.py /path/to/test2.mp4```
- ```python detector.py /path/to/images/of/test.mp4 /path/to/output/directory```
