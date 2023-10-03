from flask import Flask
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config.from_mapping(SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'db.sqlite'))

    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return 'passed'
    
    return app