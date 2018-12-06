from flask import Blueprint, render_template, request, redirect, url_for

from apps.ext import db
from apps.user.models import User, Address

user = Blueprint('user', __name__, template_folder='templates')


# @user.route('/add/')
# def add_user():
#     user_list = [User(username=f"用户{i}") for i in range(30)]
#     配置重设置了app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True，会自动调用db.session.commit()方法去提交
#     db.session.add_all(user_list)
#
#     return render_template('user_index.html')


@user.route('/index/<int:page>/<int:size>/')
def index(page, size):
    pagination = User.query.paginate(page=page, per_page=size, error_out=False)
    right_current = 5
    left_current = 5
    if page < 6:
        right_current = 11 - page
    elif pagination.pages - page < 5:
        left_current = 9 - (pagination.pages - page)
    return render_template('user_index.html', pagination=pagination, right_current=right_current,
                           left_current=left_current)


@user.route('/', methods=['get', 'post'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        province = request.form.get('province')
        city = request.form.get('city')
        detail = request.form.get('detail')
        is_continue = request.form.get('continue')
        if username:
            user_ = User(username=username)
            db.session.add(user_)
            if None not in (phone, province, city, detail):
                db.session.add(Address(uid=user_.uid, phone=phone, province=province, city=city, detail=detail))
                if is_continue:
                    return render_template('add_user.html')
                else:
                    return redirect(url_for('.index', page=1, size=3))
            else:
                return render_template('add_user.html', msg='所有选线为必填项,请补全!')
        else:
            return render_template('add_user.html', msg='昵称不能为空!')


@user.route('/detail/<int:uid>/')
def detail(uid):
    user_ = User.query.filter(User.uid == uid).first()
    if user:
        return render_template('user_detail.html', user_=user_)
    else:
        return '未查询到该用户'


@user.route('/delete/<int:uid>/')
def delete_(uid):
    addr = Address.query.filter(Address.uid == uid).first()
    if addr:
        db.session.delete(addr)
        return redirect(url_for('.detail', uid=uid))
    else:
        return '未查询到该用户'


@user.route('/update/<int:uid>/', methods=['get', 'post'])
def update_(uid):
    if request.method == 'GET':
        user_ = User.query.filter_by(uid=uid).first()
        return render_template('user_update.html', user_=user_)
    elif request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        province = request.form.get('province')
        city = request.form.get('city')
        detail = request.form.get('detail')
        if None not in (phone, province, city, detail, username):
            user_ = User.query.filter(User.uid == uid, User.username == username).first()
            if user_:
                user_.username = username
                user_.addrs[0].phone = phone
                user_.addrs[0].province = province
                user_.addrs[0].city = city
                user_.addrs[0].detail = detail
                return redirect(url_for('.index', page=1, size=3))
            else:
                return render_template('user_update.html', msg='所有选线为必填项,请补全!',
                                       user_=User.query.filter(User.uid == uid).first())
        else:
            return render_template('user_update.html', msg='所有选线为必填项,请补全!',
                                   user_=User.query.filter(User.uid == uid).first())


# @user.route('/pag/<int:page>/<int:size>/')
# def test_macro(page, size):
#     pagination = User.query.paginate(page=page, per_page=size, error_out=False)
#     return render_template('limit.html', pagination=pagination, size=size)


@user.route('/pag2/')
def test2_macro():
    page = request.values.get('page')
    size = request.values.get('size')
    if page and size:
        try:
            page = int(page)
            size = int(size)
            pagination = User.query.paginate(page=page, per_page=size, error_out=False)
            return render_template('limit.html', pagination=pagination, size=size)
        except Exception as e:
            pass
    else:
        pass
