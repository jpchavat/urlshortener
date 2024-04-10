import os

from dotenv import load_dotenv
from flask import Flask

from common.error_handlers import configure_error_handlers
from common.json_provider import CustomJSONProvider

load_dotenv(str(os.path.join(os.path.dirname(__file__), ".env")))


def create_app(configs=None):
    app = Flask(__name__)
    app.json = CustomJSONProvider(app)

    from admin.config import Config

    app.config.from_object(Config)
    if configs:
        # Override the default configurations, if provided
        app.config.update(configs)

    from common.dynamodb import db
    from common.redis import redis_cli

    db.init_app(app)
    redis_cli.init_app(app)

    from admin.views import api

    app.register_blueprint(api)

    configure_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
