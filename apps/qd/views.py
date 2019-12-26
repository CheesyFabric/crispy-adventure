# 导入qd蓝图对象
from . import qd
from flask import render_template, redirect, url_for, flash, session,jsonify,request
import time
from apps.decorator import login_validate
from flask.views import MethodView
from apps.qd.forms import QdForm
from apps.models import Qd, db, User, Clazz


# 显示今日时间
def create_time():
    create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return create_time


# 登录验证
# @qd.route("/qdhome/",endpoint="qd_home")
# @login_validate
# def qd_home():
#     return render_template("qd/qd_home.html",create_time=create_time())

class QdView(MethodView):
    decorators = [login_validate]

    def get(self):
        if session['role'] == 0:
            return render_template("qd/manager_qd_home.html")
        else:
            # 查找并显示签到表里的签到历史数据
            qds = Qd.query.filter_by(uid=session.get("uid")).order_by(Qd.create_time.desc()).all()
            today_qd = None
            # 先看是否有签到历史数据 如果有
            if len(qds) > 0:
                # 如果签到历史的第一条数据是今天的（如果已经签过到）
                if qds[0].create_time == create_time():
                    today_qd = qds[0]
                # 如果今天还没签到
                else:
                    today_qd = None
            else:
                today_qd = None
            return render_template("qd/qd_home.html", create_time=create_time(), qds=qds, today_qd=today_qd)

    def post(self):
        form = QdForm()
        # 如果验证通过 提交签到数据
        if form.validate_on_submit():
            uid = session.get("uid")
            qd = Qd(uid=uid, stage=form.data.get("stage"), progress=form.data.get("progress"),
                    code_num=form.data.get("code_num"), bug_num=form.data.get("bug_num"),
                    create_time=form.data.get("create_time"), remark=form.data.get("remark"))
            db.session.add(qd)
            db.session.commit()
            return redirect(url_for("qd.qd"))
        else:
            flash("请将签到信息填写完整！")
            return redirect(url_for("qd.qd"))

qd.add_url_rule('/qd/', view_func=QdView.as_view('qd'))

@qd.route("/search_qd/", methods=["POST"])
def search_qd():
    cname=request.form.get("cname")
    nick_name=request.form.get("nick_name")
    create_time=request.form.get("create_time")
    # 查讯所有的签到数据
    qd = Qd.query.join(User).join(User.clazzs)
    if cname:
        cname=cname.strip()
        qd=qd.filter(Clazz.name==cname)
    if nick_name:
        nick_name=nick_name.strip()
        qd=qd.filter(User.nick_name==nick_name)
    if create_time:
        create_time=create_time.strip()
        qd=qd.filter(Qd.create_time==create_time)

    qd=qd.all()
    qds = []
    for q in qd:
        # 班级名
        cname=q.user.clazzs[0].name if len(q.user.clazzs)>0 else "None"
        #班级id
        cid=q.user.clazzs[0].id
        #昵称
        uname=q.user.nick_name
        uid=q.uid
        qds.append({
            "id":q.id,
            "uid":uid,
            "uname":uname,
            "cid":cid,
            "cname":cname,
            "stage":q.stage,
            "progress":q.progress,
            "code_num":q.code_num,
            "bug_num":q.bug_num,
            "create_time":q.create_time,
            "remark":q.remark
        })
    return jsonify({"qd":qds})

class DataAnalysis(MethodView):
    decorators = [login_validate]

    def get(self):
        if session['role'] == 0:
            return render_template('data_analysis/manager_data_analysis.html')
        if session['role'] == 1:
            return render_template('data_analysis/user_data_analysis.html')
    def post(self):
        # 学生 姓名 列表
        us=[]
        # 对应 代码数 列表
        all_code=[]
        # 获取所有的学生
        users=User.query.filter_by(role=1).all()
        sql = """

                    SELECT 
                    IFNULL(q2.code_num,0) as code_num FROM
                    (SELECT create_time FROM t_qd GROUP BY create_time ORDER BY create_time)AS q1
                    LEFT JOIN 
                    (SELECT * FROM t_qd WHERE uid={})AS q2 
                    ON q1.create_time=q2.create_time   

                """

        for u in users:
            us.append(u.nick_name)
        #     通过学生对象找签到数据 列表
            qds=Qd.query.filter_by(uid=u.id)

            # code_num.append([qd.code_num for qd in qds])
            #所有的签到日期
            data=[d[0] for d in db.session.execute('SELECT create_time FROM t_qd GROUP BY create_time ORDER BY create_time').cursor._rows]



            code_nums = [c[0] if c[0] else 0 for c in db.session.execute(sql.format(u.id)).cursor._rows]
            all_code.append(code_nums)

        return jsonify({
            "user":us,
            "data":data,
            "code_num":all_code
        })


qd.add_url_rule('/data_analysis/', view_func=DataAnalysis.as_view('data_analysis'))