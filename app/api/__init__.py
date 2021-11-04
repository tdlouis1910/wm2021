
from app.api import users, customers, water_meter, detect_object

routes = [
    users,
    customers,
    water_meter,
    detect_object
]

def init_app(app, base_url):

    for route in routes:
        app.register_blueprint(route.bp, url_prefix=base_url + route.path)