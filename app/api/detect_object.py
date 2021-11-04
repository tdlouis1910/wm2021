from flask import Blueprint, abort, redirect, url_for, request, render_template
from flask_sqlalchemy import model
from sqlalchemy import func, and_, or_

from app.common.utils import *
from models import *

from werkzeug.utils import secure_filename
import os, glob


path = "/predict"
bp = Blueprint('predict', __name__)


def predict_image(image_name):
    
    # appserver.model_loaded.predict(image_name)


    return True


@bp.route('/image', methods=['POST'])
@authentication({'user'})
def customers_list(auth):

    data = getparams()
    res = getresponse("SUCCESS")

    if auth is None:
        res = getresponse("UNAUTHENTICATED")
        return jsonify(res), res['status']



    file = request.files['file']

    filename = secure_filename(file.filename)

    print(filename)

    basepath = os.path.dirname(__file__)

    file_path = os.path.join(basepath, './static/uploads', secure_filename(file.filename))
    file.save(file_path)

    get_detected_object = predict_image(file_path)
# 
    res['result'] = get_detected_object[1]


    return jsonify(res), res['status']
