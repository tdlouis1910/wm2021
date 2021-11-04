from flask import Blueprint, abort
from sqlalchemy import func, and_, or_

from app.common.utils import *
from models import *


path = "/water-meter"
bp = Blueprint('water-meter', __name__)

@bp.route('/<int:idx>/get', methods=['POST'])
def get_index(idx):

    data = getparams()
    res = getresponse("SUCCESS")
    
    water_meter = WaterMeter.query.get(idx)

    previous_record_index = RecordIndex.query.get(water_meter.previous_record_idx)
    record_index = RecordIndex.query.get(water_meter.record_idx)

    res['water_meter'] = water_meter.dict()

    res['prev_record'] = previous_record_index.dict()

    res['moment_record'] =  record_index.dict()

    return jsonify(res), res['status']


@bp.route('/<int:idx>/checking', methods=['POST'])
def get_latest_record(idx):

    data = getparams()
    res = getresponse("SUCCESS")
    
    water_meter = WaterMeter.query.get(idx)

    record_index = RecordIndex.query.get(water_meter.record_idx)

    res['latest_record'] =  record_index.dict()

    return jsonify(res), res['status']

@bp.route('/<int:idx>/record/update', methods=['POST'])
def update_record(idx):

    data = getparams()
    res = getresponse("SUCCESS")
    
    water_meter = WaterMeter.query.get(idx)

    record_index = RecordIndex.query.get(water_meter.record_idx)

    water_meter.previous_record_idx = record_index.idx

    #122 idx is the default exception value
    water_meter.record_idx = 122

    db.session.commit()

    res['water_meter'] = water_meter.dict()


    return jsonify(res), res['status']