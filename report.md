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
    - Difficult to use
- #### FasterRCNN
  - Pros
    - Understands what the object is supposed to look like
    - Robust to changes in orientation
    - Robust to partial occlusion
  - Cons
    - Difficult to use
    - Not robust to occlusion
    - Requires training data for each object
    - Slow performance
    - Does not take advantage of temporal information
    
Since FasterRCNN was robust to partial occlusion and changes in orientation, it was found to be the optimal method out of all of the ones that were tried. 

# Approach
This project took advantage of the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection).

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
Once the dataset was created, I fine-tuned the faster_rcnn_resnet50 model available from the Object Detection API's [model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md).
