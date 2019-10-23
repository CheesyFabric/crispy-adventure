from flask_wtf import Form
from wtforms import StringField, IntegerField, validators
from wtforms.validators import DataRequired


class QdForm(Form):
    stage = StringField('阶段', validators=[DataRequired()])
    progress = StringField("进度", validators=[DataRequired()])
    code_num = IntegerField('代码数', validators=[DataRequired()])
    bug_num = IntegerField("bug数", validators=[DataRequired()])
    create_time = StringField("时间", validators=[DataRequired()])
    remark = StringField("备注")
