import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_httpauth import HTTPTokenAuth


db = SQLAlchemy()
_api = Api(prefix='/api')
auth = HTTPTokenAuth()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
        os.path.join(app.instance_path, 'data.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    
    '''db.app = app
    db.drop_all()
    db.create_all() # '''
    
    from flaskr.root import root
    app.register_blueprint(root)

    from flaskr.api import ItemAPI
    _api.add_resource(ItemAPI,'/items',endpoint='items')

    # 用户api
    from flaskr.api import UserRegister, UserLogin, UserUpdate, UserCancel, UserSearch, UserLogout
    _api.add_resource(UserRegister,'/users/register')
    _api.add_resource(UserLogin,'/users/login')
    _api.add_resource(UserUpdate,'/users/update')
    _api.add_resource(UserCancel,'/users/cancel')
    _api.add_resource(UserSearch,'/users/search')
    _api.add_resource(UserLogout,'/users/logout')

    # 管理员api
    from flaskr.api import AdminSearchOneById, AdminDeleteOneById, AdminUpdateOne, AdminSearchAll, AdminDeleteAll
    _api.add_resource(AdminSearchOneById,'/admin/search/one')
    _api.add_resource(AdminDeleteOneById,'/admin/delete/one')
    _api.add_resource(AdminUpdateOne,'/admin/update/one')
    _api.add_resource(AdminSearchAll,'/admin/search/all')
    _api.add_resource(AdminDeleteAll,'/admin/delete/all')

    _api.init_app(app)

    return app