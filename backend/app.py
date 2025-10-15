from flask import Flask
from application.models import db, User, Role, UserRoles
from flask_security import Security, SQLAlchemyUserDatastore
from application.config import LocalDevelopmentConfig
from flask_cors import CORS

from application.celery_init import celery_init_app
from celery.schedules import crontab
from application.task import csv_down_ad
from application.api import api


def create_app():
    app = Flask(__name__)
    print(app.static_folder)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore = datastore , register_blueprint=False )
    @app.security.unauthn_handler
    def unautn_handler(reason,headers):
        print(reason)
        return {"message" : f"please provide {reason[0]}"} ,401
    
    @app.security.unauthz_handler
    def unautz_handler(func_name,params):
        print(func_name)
        print(params)
        return {"message" : f"you don't have access to use {params[0]} resource"} ,403
    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

from application.initial_data import *
from application.routes import *


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month='13', hour=6, minute=40),  
        csv_down_ad.s() ,
        name="generating admin csv"
    )


if __name__ == "__main__":
    app.run(debug=True)