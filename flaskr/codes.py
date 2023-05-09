import functools
import pandas as pd

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db

bp = Blueprint('codes', __name__, url_prefix='/codes')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/codes_import', methods=['GET', 'POST'])
@login_required
def codes_import():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        db = get_db()
        for index, row in df.iterrows():
            db.execute('INSERT INTO product (code, name, price)'
                       ' VALUES (?, ?, ?)'
                       'ON CONFLICT(code) DO UPDATE SET'
                       ' name=excluded.name,'
                       ' price=excluded.price',
                       (row['sifra'], row['naziv'], row['cena'])

                       )
            db.commit()
        flash("Sifre uspesno ucitane")
    elif request.method == 'GET':
        return render_template('data/import_data.html')
    return redirect(url_for('index'))


@bp.route('/codes_export', methods=['GET'])
@login_required
def codes_export():
    if request.method == 'GET':
        flash("hejjj export")
    return redirect(url_for('index'))
