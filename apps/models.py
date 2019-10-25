from flask_sqlalchemy import SQLAlchemy
from apps import app
from werkzeug.security import generate_password_hash, check_password_hash

# 连接数据库
db = SQLAlchemy(app)

# 中间表
user_clazz = db.Table(
    "user_clazz",
    db.Model.metadata,
    db.Column("uid", db.INTEGER, db.ForeignKey("t_user.id"), primary_key=True),
    db.Column("cid", db.INTEGER, db.ForeignKey("t_clazz.id"), primary_key=True)
)


# 创建ORM模型
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(50), nullable=False)
    nick_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    _password = db.Column(db.String(500), nullable=False)
    phone=db.Column(db.String(11))

    clazzs = db.relationship("Clazz", backref="users", secondary=user_clazz)

    def __init__(self, uname, nick_name, role, gender, password, confirm_password):
        self.uname = uname
        self.nick_name = nick_name
        self.role = role
        self.gender = gender
        self.passwd = password
        self.confirm_password = confirm_password

    @property
    def passwd(self):
        return self.passwd

    # 给数据库里的密码加密
    @passwd.setter
    def passwd(self, rowpasswd):
        self._password = generate_password_hash(rowpasswd)

    #     验证密码
    '''
    第一个参数传入我们需要对比的密码，第二个参数传入我们的明文密码。
    这样这个函数就帮我们完成了先加密再对比的操作。如果相等，那么将返回True，否则返回False
    '''

    def check_passwd(self, password):
        return check_password_hash(self._password, password)


class Clazz(db.Model):
    __tablename__ = "t_clazz"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    count = db.Column(db.INTEGER)


class Qd(db.Model):
    __tablename__ = "t_qd"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    uid=db.Column(db.INTEGER,db.ForeignKey("t_user.id"))
    user=db.relationship("User")
    # 阶段
    stage = db.Column(db.String(32))
    # 进度
    progress = db.Column(db.String(32))
    # 代码数
    code_num = db.Column(db.INTEGER)
    # bug数
    bug_num = db.Column(db.INTEGER)
    create_time = db.Column(db.String(32))
    remark=db.Column(db.String(100))
    def __init__(self,uid,stage,progress,code_num,bug_num,create_time,remark=None):
        self.uid=uid
        self.stage=stage
        self.progress=progress
        self.code_num=code_num
        self.bug_num=bug_num
        self.create_time=create_time
        self.remark=remark
