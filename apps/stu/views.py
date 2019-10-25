# 导入stu蓝图对象
from . import stu

from flask import render_template, request, redirect, url_for, views, session

from apps.models import User, db, Clazz

from apps.decorator import login_validate


# stu蓝图对象
@stu.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("user/login.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        password = request.form["password"]

        user = User.query.filter_by(uname=uname).first()
        # 如果用户名能匹配到
        if user:
            # 如果密码正确
            if user.check_passwd(password):
                # print(request.form.get("uname"))
                # 把数据放到session里
                session["uid"]=user.id
                session["uname"] = uname
                session["clazz"] = user.clazzs[0].name
                session["gender"] = user.gender
                session['role']=user.role
                # 如果密码正确
                return redirect(url_for("home"), code=301)
            # 如果密码不正确
            else:
                return render_template("user/login.html", msg="密码错误")

        # 如果用户名不能匹配到
        else:
            return render_template("user/login.html", msg="用户名错误")


class Regsiter(views.MethodView):
    def get(self):
        # 从数据库获取班级信息 得到一个列表 里面是很多个clazzs对象
        clazzs = Clazz.query.all()
        return render_template("user/regsiter.html", clazzs=clazzs)

    def post(self):
        uname = request.form.get("uname")
        nick_name = request.form.get("nick_name")
        role = request.form.get("role")
        gender = request.form["gender"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        # print("{},{},{},{},{},{}".format(uname,nick_name,role,gender,password,confirm_password))

        cid = request.form["cid"]
        # 把数据存到数据库里
        user = User(uname, nick_name, role, gender, password, confirm_password)
        user.clazzs = Clazz.query.filter_by(id=cid).all()

        db.session.add(user)
        db.session.commit()

        # return render_template("login.html")
        return redirect(url_for("stu.login"), code=301)


# 注册类视图 设置类视图的url地址
stu.add_url_rule("/regsiter/", endpoint="R", view_func=Regsiter.as_view("regsiter"))


@stu.route("/home/")
@login_validate
def home():
    return render_template("home.html")



# 注销
@stu.route("/signout/")
def signout():
    session.clear()
    return redirect(url_for("stu.login"))

@stu.route("/info/",endpoint="info", methods=["GET", "POST"])
@login_validate
def info():
    user = User.query.filter_by(id=session["uid"]).first()
    if request.method=="GET":

        return render_template("info/info.html",user=user)
    if request.method=="POST":

        # 修改个人信息 提交数据库
        user.nick_name=request.form.get("nick_name")
        user.phone=request.form.get("phone")
        # user.gender=user
        user.clazzs[0].name=request.form.get("clazz")

        db.session.commit()