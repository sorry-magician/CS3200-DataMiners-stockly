from flask import Flask
from dotenv import load_dotenv
import os
import logging
from backend.db_connection import init_app as init_db
from backend.products.products import products
from backend.inventory.inventory import inventory
from backend.analytics.analytics import analytics
from backend.admin.admin import admin

def create_app() -> Flask:
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret")
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER", "").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD", "").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST", "").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT", "3306").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME", "").strip()

    app.logger.info("create_app(): initializing database connection")
    init_db(app)

    app.logger.info("create_app(): registering blueprints")
    app.register_blueprint(products, url_prefix='/api')
    app.register_blueprint(inventory, url_prefix='/api')
    app.register_blueprint(analytics, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/api')

    return app
