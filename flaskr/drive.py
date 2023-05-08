import functools
import pandas as pd

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('drive', __name__, url_prefix='/drive')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/codes', methods=['GET', 'POST'])
def codes():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        db = get_db()
        for index, row in df.iterrows():
            db.execute('INSERT INTO product (code, name, price)'
                       ' VALUES (?, ?, ?)',
                       (row['sifra'], row['naziv'], row['cena'])
                       )
            db.commit()
        flash("Sifre uspesno ucitane")
    elif request.method == 'GET':
        return render_template('data/import_data.html')
    return redirect(url_for('index'))


@bp.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        db = get_db()
        for index, row in df.iterrows():
            db.execute('INSERT INTO invoice (product_code, quantity)'
                       ' VALUES (?, ?)',
                       (row['sifra'], row['kolicina'])
                       )
            db.commit()
        flash("Podaci o transakcijama uspesno ucitani")
    elif request.method == 'GET':
        return render_template('data/import_data.html')
    return redirect(url_for('index'))
