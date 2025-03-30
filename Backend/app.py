from flask import Flask
from config import LocalDevelopmentConfig
from models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_cors import CORS

def createApp():
    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)


    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    app.security = Security(app, datastore=datastore, register_blueprint=False)
    CORS(app)
    app.app_context().push()

    return app

app = createApp()

import create_initial_data
import routes




if (__name__ == '__main__'):
    app.run()