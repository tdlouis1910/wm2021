from flask import Blueprint, abort
from sqlalchemy import func, and_, or_

from app.common.utils import *
from models import *


path = "/customers"
bp = Blueprint('customers', __name__)

@bp.route('', methods=['POST'])
@authentication({'user'})
def customers_list(auth):
    data = getparams()
    res = getresponse("SUCCESS")

    page = data.get("page", None)
    page_size = data.get("page_size", None)
    
    user = auth['member']

    if user is None:
        res = getresponse("UNAUTHENTICATED")
        return jsonify(res), res['status']
 
    area = data.get("area", None)
    district = data.get("district", None)
    province = data.get("province", None)

    customers = Customer.query.filter_by(deleted_at = None)

    if area is not None and district is not None and province is not None:
        customers = Customer.query.filter_by(area = area, district = district, province = province, deleted_at = None)


    if page is None:
        customers.all()
    elif page > 0 and page_size is not None:
        customers = customers[(page - 1) * page_size:page*page_size]

    # _listCustomers = []

    # for customer in customers:

    #     print(customer.idx)
    #     print(WaterMeter.query.get(customer.idx).dict())

    #     water_meter = WaterMeter.query.get(customer.idx)
    #     previous_record_index = RecordIndex.query.get(water_meter.previous_record_idx)
    #     record_index = RecordIndex.query.get(water_meter.record_idx)

    #     dic = dict(
    #         customer = customer.dict(),
    #         record_details = dict(
    #             water_meter = water_meter.dict(),
    #             previous_record_index = previous_record_index.dict(),
    #             record_index = record_index.dict()
    #         ),
    #     )

    #     _listCustomers.append(dic)
       

    # res['list'] = _listCustomers

    res['list'] = [customer.dict() for customer in customers]


    return jsonify(res), res['status']