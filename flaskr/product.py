import functools
import os

import pandas as pd

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)

from flaskr.db import get_db

bp = Blueprint('product', __name__, url_prefix='/product')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/view', methods=['GET'])
@login_required
def view():
    if request.method == 'GET':
        db = get_db()
        products = db.execute(
            'SELECT * FROM product'
        ).fetchall()
        return render_template('product/view.html', products=products)
    return redirect(url_for('index'))


@bp.route('/product_import', methods=['GET', 'POST'])
@login_required
def product_import():
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


@bp.route('/product_export', methods=['GET'])
@login_required
def product_export():
    if request.method == 'GET':
        filename = "registar_sifara.csv"
        db = get_db()
        query = 'SELECT * FROM product'
        df = pd.read_sql_query(query, db).drop(['id'], axis=1)
        df.to_csv(filename, index=False)
        return Response(
            open(filename, 'r'),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment;filename={filename}'}
        )
    return redirect(url_for('index'))
