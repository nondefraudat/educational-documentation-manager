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
    from . import admforms
    app.register_blueprint(admforms.bp)

    from .auth import login_required
    from flask import redirect, url_for

    @app.route('/')
    @login_required
    def index():
        return redirect(url_for('admforms.teachers'))
    
    def index():
        return redirect(url_for('admforms.departments'))
    
    def index():
        return redirect(url_for('admforms.facultys'))
    
    def index():
        return redirect(url_for('admforms.ranks'))
    
    def index():
        return redirect(url_for('admforms.positions'))
    
    def index():
        return redirect(url_for('admforms.degrees'))

    return app