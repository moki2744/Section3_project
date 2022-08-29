from flask import Flask
import pandas as pd


def create_app():
    app = Flask(__name__)

    from project_app.views.main_views import main_bp
    from project_app.views.ML_views import predict_bp
    from project_app.views.map_views import map_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(map_bp)
    return app

if __name__ == "__main__":
  app = create_app()
  app.run()