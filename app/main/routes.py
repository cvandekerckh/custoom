from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import OrderForm
from app.translate import translate
from app.main import bp
from app.models import Story
from app.models import Buyer
from utils.google_sheet import db_to_sheet


SHEET_REFERENCE = "11RJsiBKrRY1bTjwm0qg-KvZZJHR18pcMN3GoLPbHoe0"
BUYER_TAB_NAME = "clients"
STORY_TAB_NAME = "albums"


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    print(form)
    if request.method == 'POST':
        buyer = Buyer(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            address_1 = form.address_1.data,
            address_2 = form.address_2.data,
            city = form.city.data,
            country = form.country.data,
            postal_code = form.postal_code.data,
            state = form.state.data,
        )
        db.session.add(buyer)
        db.session.commit()
        story = Story(
            nickname = form.nickname.data,
            nickname_gender = form.nickname_gender.data,
            location = form.location.data,
            dog = form.dog.data,
            friend = form.friend.data,
            friend_gender = form.friend_gender.data,
            cake = form.cake.data,
            cake_gender = form.cake_gender.data,
            body = form.body.data,
            author = Buyer.query.filter_by(email=form.email.data).first_or_404()
        )
        story.link_album()
        db.session.add(story)
        db.session.commit()
        db_to_sheet(
            "buyer",
            'sqlite:///app.db', #current_app.config["SQLALCHEMY_DATABASE_URI"],
            SHEET_REFERENCE,
            BUYER_TAB_NAME,
        )
        db_to_sheet(
            "story",
            'sqlite:///app.db', #current_app.config["SQLALCHEMY_DATABASE_URI"],
            SHEET_REFERENCE,
            STORY_TAB_NAME,
        )
        flash(_('Votre commande a bien été enregistrée'))
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form)


@bp.route('/translate', methods=['POST'])
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

