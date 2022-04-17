from flask_wtf import FlaskForm
from wtforms import SubmitField, ValidationError, PasswordField, EmailField
from wtforms.validators import Length, DataRequired, EqualTo

from app.models import User


class RegisterForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(max=256)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password",
        [DataRequired(), EqualTo("confirm_password", message="Passwords must match")],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Repeat Password", render_kw={"placeholder": "Repeat Password"}
    )
    submit = SubmitField("Create Account")

    def validate_email(form, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email has already in use by another user")
