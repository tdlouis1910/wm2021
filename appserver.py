# from __future__ import division, print_function
# # coding=utf-8
# import sys


from app.application import create_app
from app.common.utils import *

from env import BaseConfig

import os


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
session = tf.compat.v1.Session(config=config)

app = create_app(base_url=BaseConfig.BASE_URL)

weights_loaded="./checkpoint/yolov4"
labels_path = "./checkpoint/yolov4/labelmap.txt"

model_loaded = None

def load_model(model_path):
    print(("* Loading Tensor model and Flask starting server..."
            "please wait until server has fully started"))
    global model_loaded
    model_loaded = tf.saved_model.load(model_path, tags=[tag_constants.SERVING])


def predict(image_name):

        input_image = image_name
        input_size = image_size

        original_image = cv2.imread(input_image)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.

        images_data = []
        images_data.append(image_data)

        images_data = np.asarray(images_data).astype(np.float32)

        infer = model_loaded.signatures["serving_default"]

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

        pred_bbox = [scores.numpy(), classes.numpy(), valid_detections.numpy()]

        return utils.predicted_classes(pred_bbox)

        # cropped_image = utils.draw_bbox(original_image, pred_bbox)
        # image = Image.fromarray(cropped_image.astype(np.uint8))

        # image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        # detected_fname = output + 'Detected' + str(111) + '.jpg'
        # cv2.imwrite(detected_fname, image)

@app.route('/predict', methods=['POST'])
@authentication({'user'})
def index_predict(auth):
    res = getresponse("SUCCESS")

    if auth is None:
        res = getresponse("UNAUTHENTICATED")
        return jsonify(res), res['status']

    file = request.files['file']
    filename = secure_filename(file.filename)

    basepath = os.path.dirname(__file__)

    file_path = os.path.join(basepath, 'static/uploads', filename)

    file.save(file_path)

    get_detected_object = predict(file_path)

    result = [result['prediction'] for result in get_detected_object]

    res['result'] = result

    return jsonify(res), res['status']

if __name__ == '__main__':

    load_model(weights_loaded)

    print("Loaded tensor model.......")

    app.debug = True
    app.run(host = "0.0.0.0")


# import os
# import glob
# import re, glob, os,cv2
# import numpy as np
# import pandas as pd
# import detect_object
# from shutil import copyfile
# import shutil
# from distutils.dir_util import copy_tree

# # Flask utils
# from flask import Flask, redirect, url_for, request, render_template
# from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer

# # Define a flask app
# app = Flask(__name__)

# #for f in os.listdir("static\\similar_images\\"):
# #   os.remove("static\\similar_images\\"+f)

# print('Model loaded. Check http://127.0.0.1:5000/')


# @app.route('/', methods=['GET'])
# def index():
#     # Main page
#     return render_template('index.html')

# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       # create a secure filename
#       filename = secure_filename(f.filename)
#       print(filename)
#       # save file to /static/uploads
# #      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#       basepath = os.path.dirname(__file__)
      
#       file_path = os.path.join(basepath, './static/uploads', secure_filename(f.filename))
      
#       print(file_path)
#       f.save(file_path)
      
#       get_detected_object=detect_object.ts_detector(file_path)
      	
#       return render_template("uploaded.html", fname=filename, display_detection=get_detected_object[1])
        

# #@app.route('/predict', methods=['GET', 'POST'])
# #def upload():
# #    if request.method == 'POST':
# #        # Get the file from post request
# #        f = request.files['file']
# #
#         # Save the file to ./uploads
# #        basepath = os.path.dirname(__file__)
# #        file_path = os.path.join(
# #            basepath, 'uploads', secure_filename(f.filename))
# #        f.save(file_path)

#         # Make prediction
# #       get_detected_object=detect_object(file_path)
# #        return get_detected_object
# #    return None


# if __name__ == '__main__':
#     app.run(debug=True)


