from flask import Flask

from apps.ext import init_ext
from apps.orm.views import orm


# 程序入口
from apps.user.views import user


def create_app():
    app = Flask(__name__)
    # 上线是删除 或者改为Flase
    app.debug = True
    # 自定义选择器需要在蓝图之前注册
    register_blueprint(app)
    init_ext(app)

    return app


def register_blueprint(app):
    app.register_blueprint(orm)
    app.register_blueprint(user,url_prefix='/user')
