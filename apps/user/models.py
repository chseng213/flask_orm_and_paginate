from apps.ext import db


class User(db.Model):
    uid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    addrs = db.relationship('Address',lazy='dynamic',backref='user',uselist=True,)

class Address(db.Model):
    aid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    uid = db.Column(db.Integer,db.ForeignKey(User.uid,ondelete='CASCADE'))
    province = db.Column(db.String(100),nullable=False)
    city = db.Column(db.String(100),nullable=False)
    detail = db.Column(db.TEXT,nullable=False)
    phone = db.Column(db.String(20))