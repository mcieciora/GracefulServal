from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Url
from . import db, create_app
from sqlalchemy import desc
import json
from requests import get

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_name = request.form.get('url_name')
        url = request.form.get('url')

        if get(url).status_code != 200:
            flash('URL is not correct!', category='error')
        else:
            new_url = Url(name=url_name, url=url)
            db.session.add(new_url)
            db.session.commit()
            flash('URL added!', category='success')

    with create_app().app_context():
        data = Url.query.order_by(desc(Url.id)).all()

    return render_template("home.html", user=current_user, data=data)


@views.route('/delete-url', methods=['POST'])
def delete_url():
    url = json.loads(request.data)
    urlId = url['urlId']
    url = Url.query.get(urlId)
    if url:
        db.session.delete(url)
        db.session.commit()

    return jsonify({})
