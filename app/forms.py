from flask.ext.wtf import Form
from wtforms.validators import DataRequired, Optional, EqualTo
from wtforms.fields import TextField, SelectField, IntegerField, PasswordField


class LoginForm(Form):
    user = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ChangePasswordForm(Form):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('retype_password')])
    retype_password = PasswordField('Retype Password', validators=[DataRequired()])


class RuleForm(Form):
    id = IntegerField(validators=[Optional()])
    name = TextField('Rule name', validators=[DataRequired()])
    rule = TextField('Rule', validators=[DataRequired()])


class DeviceForm(Form):
    id = IntegerField(validators=[Optional()])
    name = TextField('Device name', validators=[DataRequired()])
    mac_address = TextField('MAC Address', validators=[DataRequired()])
    group = SelectField('Group', coerce=str)


class GroupForm(Form):
    id = IntegerField(validators=[Optional()])
    name = TextField('Group name', validators=[DataRequired()])
