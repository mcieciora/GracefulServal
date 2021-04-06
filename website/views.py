from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from .models import Url
from . import db, create_app
from sqlalchemy import desc
import json
from requests import get, exceptions

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_name = request.form.get('url_name')
        url_route = request.form.get('url')

        name = Url.query.filter_by(name=url_name).first()
        url = Url.query.filter_by(url=url_route).first()

        if name or url:
            flash('URL name already exists.', category='error')
        else:
            try:
                if get(url_route).status_code == 200:
                    new_url = Url(name=url_name, url=url_route)
                    db.session.add(new_url)
                    db.session.commit()
                    flash('URL added!', category='success')
            except exceptions.MissingSchema:
                flash('URL is not correct!', category='error')

    with create_app().app_context():
        data = Url.query.order_by(desc(Url.id)).all()

    return render_template("home.html", user=current_user, data=data)


@views.route('/delete-url', methods=['POST'])
def delete_url():
    url = json.loads(request.data)
    url_id = url['urlId']
    url = Url.query.get(url_id)
    if url:
        db.session.delete(url)
        db.session.commit()
    flash('URL was removed successfully!', category='success')
    return jsonify({})
