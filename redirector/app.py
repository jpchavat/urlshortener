import os

from dotenv import load_dotenv
from flask import Flask

from common.error_handlers import configure_error_handlers
from common.json_provider import CustomJSONProvider

load_dotenv(str(os.path.join(os.path.dirname(__file__), ".env")))


def load_all_views(app):
    from redirector.views import api

    app.register_blueprint(api)


def create_app(configs=None, load_views=True, load_redis=True, load_db=True):
    app = Flask(__name__)
    app.json = CustomJSONProvider(app)

    from redirector.config import Config

    app.config.from_object(Config)
    if configs:
        # Override the default configurations, if provided
        app.config.update(configs)

    if load_db:
        from common.dynamodb import db

        db.init_app(app)

    if load_redis:
        from common.redis import redis_cli

        redis_cli.init_app(app)

    if load_views:
        load_all_views(app)
    configure_error_handlers(app)

    return app


if __name__ == "__main__":
    app = create_app({"ENV": "development", "DEBUG": True, "LOG_LEVEL": "DEBUG"})
    app.run(host="0.0.0.0", port=5000)
