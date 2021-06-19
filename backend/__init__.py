from flask import Flask, render_template
from flask_cors import CORS
import config

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret
    CORS(app)

    with app.app_context():
        from .frontend import frontend
        from .api import bulwark
        from .api import api

        app.register_blueprint(frontend)
        app.register_blueprint(bulwark)
        app.register_blueprint(api)

        @app.errorhandler(404)
        def page_not_found(e):
            return render_template(
                "pages/404.html", message="Page not found"
            ), 404

        return app
