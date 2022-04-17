from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, PasswordField, EmailField
from wtforms.validators import Length, DataRequired

from app.models import User


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(max=256)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password",
        [DataRequired()],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Sign In")

    def validate_email(form, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("User does not exists!")
