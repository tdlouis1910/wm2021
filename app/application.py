from flask import Flask
from flask.json import jsonify
from app.common.utils import getresponse
from flask_cors import CORS

from app import api

from app.common.extensions import db

def create_app(app_name='ESSAY', base_url=''):
    app = Flask(app_name)
    app.config.from_object('env.BaseConfig')

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)

    api.init_app(app, base_url)

    @app.errorhandler(404)
    def handle_notfound(e):
        res = getresponse('NOT_FOUND')
        return jsonify(res), res['status']
    
    @app.errorhandler(500)
    def internal_error(e):
        res = getresponse('SERVER_ERROR')
        return jsonify(res), res['status']


    # @app.errorhandler(InternalServerError)
    # def (error):
    #     res = getresponse('SERVER_ERROR')
    #     return jsonify(res), res['status']

    

    return app



# @bp.errorhandler(404)
# def not_found(e):

#     print(e)
#     res = getresponse('NOT_FOUND')

#     return jsonify(res), res['status']