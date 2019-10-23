from flask import session,redirect,url_for

# 登录验证
def login_validate(func):
    def inner(*args,**kwargs):
        if  session.get("uname"):  # None == Flase
            return func(*args,**kwargs)
        else:
            return redirect(url_for("stu.login"))

    return inner