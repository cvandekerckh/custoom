from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import OrderForm
from app.models import User
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = OrderForm(request.form)
    print(request.form)
    if request.method == 'POST':
    #if form.validate_on_submit():
        print("coco")
        print(form.email.data)
        print(form.phone.data)
        print(form.message.data)
        flash(_('Votre commande a bien été enregistrée'))
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form)


@bp.route('/translate', methods=['POST'])
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})

