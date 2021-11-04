import pandas as pd

from distutils.dir_util import copy_tree
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from shutil import copyfile
import shutil
import os, glob
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


framework="tf"  #tf, tflite, trt
model="yolov4"  #yolov3 or yolov4
tiny=False      #yolo or yolo-tiny
iou=0.45        #iou threshold
score=0.25      #score threshold
output='./static/detections/'  #path to output folder
num_classes=11	

image_size=416
config = ConfigProto()
config.gpu_options.allow_growth = True



class Model(object):

    def __init__(self, model_path):
        tf.saved_model.load(model_path, tags=[tag_constants.SERVING])


    def predict(self, image_name):

        print(image_name)

        input_image = image_name
        input_size = image_size

        original_image = cv2.imread(input_image)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        print(original_image)

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.

        images_data = []
        images_data.append(image_data)

        images_data = np.asarray(images_data).astype(np.float32)


        infer = model.signatures['serving_default']

        batch_data = tf.constant(images_data)

        pred_bbox = infer(batch_data)

        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]


        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=iou,
            score_threshold=score
        )


        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

        cropped_image = utils.draw_bbox(original_image, pred_bbox)
        image = Image.fromarray(cropped_image.astype(np.uint8))

        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        detected_fname = output + 'Detected' + str(111) + '.jpg'
        cv2.imwrite(detected_fname, image)


        return [image, detected_fname]
