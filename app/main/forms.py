from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l



class OrderForm(FlaskForm):
    nickname = StringField(_l('Nickname'), validators=[DataRequired()])
    nickname_gender = StringField(_l('Nickname gender'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    dog = StringField(_l('Dog'), validators=[DataRequired()])
    friend = StringField(_l('Friend'), validators=[DataRequired()])
    friend_gender = StringField(_l('Friend Gender'), validators=[DataRequired()])
    cake = StringField(_l('Cake'), validators=[DataRequired()])
    cake_gender = StringField(_l('Cake Gender'), validators=[DataRequired()])
    body = TextAreaField(_l('Body'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))


    first_name = StringField(_l('Prénom'), validators=[DataRequired()])
    last_name = StringField(_l('Nom de famille'), validators=[DataRequired()])
    email = StringField(_l('Adresse email'), validators=[DataRequired()])
    address_1 = StringField(_l('Adresse postale'), validators=[DataRequired()])
    address_2 = StringField(_l("Complement d'adresse"))
    city = StringField(_l('Ville'), validators=[DataRequired()])
    country = StringField(_l('Pays'), validators=[DataRequired()])
    postal_code = StringField(_l('Code postal'), validators=[DataRequired()])
    state = StringField(_l('Etat/province'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

