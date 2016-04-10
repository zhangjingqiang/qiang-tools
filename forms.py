from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from models import User

class LoginForm(Form):
    username = StringField('Username',
                           validators=[Required(), Length(1, 32)])
    password = PasswordField('Password', validators=[Required(),
                                                     Length(1, 32)])

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None and not user.verify_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        return True

class ToolForm(Form):
    name = StringField('Tool name', validators=[Required(),
                                                Length(1, 60)])
