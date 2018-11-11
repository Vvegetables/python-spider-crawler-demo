from flask import Flask
from routes.data import main as data_routes
from routes.spider import main as spider_routes
from routes.index import main as index_routes
from settings import SECRETKTY


def configured_app():
    app = Flask(__name__)
    register_routes(app)
    return app
    

def register_routes(app):
    app.secret_key = SECRETKTY
    app.register_blueprint(spider_routes)
    app.register_blueprint(index_routes)
    app.register_blueprint(data_routes, url_prefix='/data')


if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=2000,
        debug=True,
        threaded=True,
    )
    app = configured_app()
    app.run(**config)
