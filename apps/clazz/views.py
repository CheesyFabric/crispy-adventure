#导入蓝图对象
from . import clazz

from flask import render_template, redirect, url_for, session, request
from flask.views import MethodView
from apps.models import Clazz,db

class ClazzManagement(MethodView):

    def get(self):
        clazzs = Clazz.query.all()
        return render_template("clazz_management.html",clazzs=clazzs)
    def post(self):
        clazzs = Clazz.query.all()
        cname=request.form.get("cname")
        #搜索匹配的班级 返回这个班级列表对象
        clazzs=search_clazzs(cname)
        return render_template("clazz_management.html",clazzs=clazzs)

clazz.add_url_rule("/clazz_management/",view_func=ClazzManagement.as_view("clazz_management"))

#搜索匹配的班级 返回这个班级对象
def search_clazzs(cname):
    clazzs=Clazz.query.filter_by(name=cname).all()
    return clazzs

# 提交修改后的班级数据
@clazz.route("/change_clazz_info/",methods=["POST","GET"])
def change_clazz_info():

    if request.method=="POST":

        # 判断是修改原来的班级数据 还是添加新的班级数据
        clazz_id = request.form.get('clazz_id')
        # 如果能取到这个值 说明是修改原有的班级数据
        if clazz_id:
            clazz_name=request.form.get('clazz_name')
            clazz_count=request.form.get('clazz_count')

            clazz=Clazz.query.filter_by(id=clazz_id).first()
            clazz.name=clazz_name
            clazz.count=clazz_count
            db.session.commit()
        # 如果不能取到这个值 说明是新增班级数据

    if request.method == "GET":

        clazz_name = request.args.get('clazz_name')
        clazz_count = request.args.get('clazz_count')

        clazz=Clazz()
        clazz.name = clazz_name
        clazz.count = clazz_count
        db.session.add(clazz)
        db.session.commit()

    return redirect(url_for("clazz.clazz_management"))









