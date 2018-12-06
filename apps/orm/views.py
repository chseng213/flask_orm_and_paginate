from flask import Blueprint, render_template
from sqlalchemy import and_, or_

from apps.ext import db
from apps.orm.models import Category
from apps.user.models import User

orm = Blueprint('orm', __name__)


@orm.route('/')
def find():
    '''
    select * from table
    select column,... from table
    select colum ,..  from table  where ()
    select colum,... from  where ()  order by  colum [ASC | DESC]
    where  ()
    group by colum,..  having ()
    order by colum ,..   [ASC | DESC]

     多表
     外连接:   全外连接(mysql不支持)  左外连接   右外连接
     where table alas left outer join table alas
     same columname
     using(alas.colum=alas.colum)  |
     different columname
     on(colum=cloum)
    :return:
    '''
    #  关系运算符  != >  <  >=   <=   ==
    Category.query.filter(Category.name == '')
    #  in like between and    and or
    #  select * from categroy where cate_id in (1,2,3)
    query = Category.query.filter(Category.cate_id.in_([1, 2]))
    cate_list = query.all()

    #  select * from cate where name like '%亚%'
    #  filter(条件一,条件二)  等同于 and_(条件一,条件二)
    query = Category.query.filter(Category.name.like('%亚%'))
    cate_list = query.all()
    #  sql语句中的and
    # query = Category.query.filter(and_(Category.cate_idcate_id.in_([1,2]),Category.name.like('%亚%')))
    # cate_list = query.all()
    #  sql查询中的or
    query = Category.query.filter(or_(Category.cate_id.in_([1, 2]), Category.name.like('%日%')))
    cate_list = query.all()

    # sql语句中的between and
    query = Category.query.filter(Category.cate_id.between(1, 100))
    cate_list = query.all()

    # 过滤列
    # <class 'list'>: [(1, '亚韩'), (3, '日本'), (2, '欧美')]
    cate_list = Category.query.with_entities(Category.cate_id, Category.name).all()
    data = []
    for cate in cate_list:
        data.append({'cate_id': cate[0], 'name': cate[1]})
    # Category.query.filter_by()
    return render_template('cate.html', cate_list=data)

@orm.route('/update/')
def update():
    user = User.query.get(7)
    user.username = '未知y用户'
    db.session.add(user)
    # 设置了自动提交配置了
    # db.session.commit()






@orm.route('/list/<int:page>/<int:size>/')
def pagination_view(page, size):
    pagination = Category.query.paginate(page=page, per_page=size, error_out=False)
    # 获取页码数
    print(pagination.pages)
    # 当前数据
    print(pagination.items)
    # 总条数
    print(pagination.total)
    # 当前页码
    print(pagination.page)
    #  是否有上一页
    print(pagination.has_prev)
    # 是否有下一页
    print(pagination.has_next)
    # 下一页页码数
    print(pagination.prev_num)
    # 上一页页码数
    print(pagination.next_num)
    # pagination.iter_pages(left_edge=2, left_current=2,
    #                       right_current=5, right_edge=2)
    '''
    left_edge=2,  导航左边最少显示两条数据(1,2)
    left_current=2, 当前左边显示两条数据(不包含自己)
    right_current=5, 当前右边最少显示五条记录(包含自己)
    right_edge=2  导航右边最少显示两条数据(最后两页)
    '''
    right_current = 5
    left_current = 5
    if page < 6:
        right_current = 11 - page
    elif pagination.pages - page < 5:
        left_current = 9 - (pagination.pages - page)
    return render_template('pagination.html', pagination=pagination, right_current=right_current,
                           left_current=left_current)


@orm.route('/cate/')
def cate():
    cates = Category.query.all()

    return render_template('cate.html', cates=cates)
