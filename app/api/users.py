from flask import Blueprint, abort
from sqlalchemy import func, and_, or_

from app.common.utils import *
from models import *


path = "/users"
bp = Blueprint('users', __name__)

@bp.route('/join', methods=['POST'])
def join():

    fields = {'email', 'password', 'profile_img', 'name', 'phone_number', 'introduce'}

    user_data = {}

    data = getparams()
    res = formvalidation(data, fields)

    for item in fields:
        user_data[item] = data.get(item, None)

    
    user = User(
        email = user_data['email'],
        pw = user_data['password'],
        name = user_data['name'],
        profile_img = 1,
        phone_number = user_data['phone_number'],
        introduce = user_data['introduce'],
    )
    
    if User.query.filter(User.email == user_data['email']).count() > 0:
        res = getresponse("SERVER_ERROR", "Email was registered")
        return jsonify(res), res['status']
    else:
        db.session.add(user)
        db.session.commit()

        user_info = User.query.filter(User.email == user_data['email']).first()

        token = generate_token({        
            'type': 'user',
            'idx': user.idx
        }),
        user_info.token = token
        db.session.commit()

    return jsonify(res), res['status']



@bp.route('/login', methods=['POST'])
def login():

    data = getparams()
    res = formvalidation(data, {'email', 'password'})

    email = data.get("email", None)
    password = data.get("password", None)

    user = User.authenticate(email, password)

    if user is None:
        res = getresponse('VALIDATION_ERROR')
        return jsonify(res), res['status']
    else:
        res['logged_in'] = user.dict_login()
        return jsonify(res), res['status']


@bp.route('/profile', methods=['POST'])
@authentication({'user'})
def profile(auth):

    data = getparams()
    res = getresponse("SUCCESS")

    user = auth['member']

    res['user'] = user.dict_profile()

    return jsonify(res), res['status']

        


   
    

