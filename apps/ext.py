from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


# 初始化第三方插件
def init_ext(app):
    init_db(app)
    pass


# 初始化数据库
def init_db(app):
    # 数据库连接的路径
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@127.0.0.1:3306/flask_orm2?charset=utf8'
    #  打印sql语句
    app.config['SQLALCHEMY_ECHO'] = True
    # 自动提交事务  将整个视图函数作为一个事务
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    #  提示信息\

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 连接池最大连接数  默认5
    app.config['SQLALCHEMY_POOL_SIZE']=20
    db.init_app(app)
    migrate.init_app(app=app, db=db)
