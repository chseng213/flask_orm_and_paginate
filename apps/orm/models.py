from datetime import datetime

from apps.ext import db


class Category(db.Model):
    cate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), unique=True, index=True, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Boolean, default=1)
    # uselist  如果设置为False  表示一对一
    # 默认为 True
    '''
    lazy 参数部分可选值
    'select'   表示一次性将所有的数据加载进所有的内存
    'dynamic'   延迟加载 先加载主表的数据,当我们使用子表相关数据才去执行查询操作
    
    
    '''
    subs = db.relationship('SubCategory', uselist=True, lazy='dynamic',backref='category')


# 二级菜单
class SubCategory(db.Model):
    sub_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 创建外键字段
    cate_id = db.Column(db.Integer, db.ForeignKey(Category.cate_id, ondelete='CASCADE'))
    # 表名(如果设置__tablename__则使用修改后的名称)  +.   +字段(如果设置name则使用修改后的名称)
    # cate_id = db.Column(db.Integer,db.ForeignKey('category.cate_id'))
    name = db.Column(db.String(60), unique=True, index=True, nullable=False)
    status = db.Column(db.Boolean, default=1)
    sort = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=0)
    #  uselist = True(默认)   一对多,   uselist = Fasle  一对一
    types = db.relationship('CategoryType', uselist=True, lazy='dynamic', backref='sub')


# 三级菜单
class CategoryType(db.Model):
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub_id = db.Column(db.Integer, db.ForeignKey(SubCategory.sub_id))
    name = db.Column(db.String(60), unique=True, index=True, nullable=False)
    status = db.Column(db.Boolean, default=1)
    sort = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=0)
