import pandas as pd
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, Response
)
from flaskr.auth import login_required
from flaskr.db import get_db

ERROR_INVOICE_NOT_NUM = "Obe vrednosti moraju biti broj"
ERROR_INVOICE_REQUIRED = "Oba polja su obavezna"
ERROR_INVOICE_CODE_NOT_EXISTS = "Sifra proizvoda nije u bazi"

bp = Blueprint('invoice', __name__)


def is_num(num):
    if num.isnumeric():
        return True
    try:
        float(num)
        return True
    except ValueError:
        return False


@bp.route('/')
@login_required
def index():
    db = get_db()
    invoices = db.execute(
        'SELECT p.code, p.name, p.price, i.quantity'
        ' FROM product p JOIN invoice i ON p.code=i.product_code'
    ).fetchall()
    return render_template('invoice/index.html', invoices=invoices)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'GET':
        return render_template('invoice/create.html')
    elif request.method == 'POST':
        error = None
        product_code = request.form['product_code']
        quantity = request.form['quantity']

        if not (product_code and quantity):
            error = ERROR_INVOICE_REQUIRED

        if not (is_num(product_code) and is_num(quantity)):
            error = ERROR_INVOICE_NOT_NUM

        if not error:
            db = get_db()
            codes = db.execute(
                'SELECT code FROM product'
                ' WHERE code = ?', (product_code,)
            ).fetchone()
            if codes:
                db.execute(
                    'INSERT INTO invoice (product_code, quantity)'
                    ' VALUES (?, ?)',
                    (product_code, quantity)
                )
                db.commit()
            else:
                error = f"Sifra proizvoda {product_code} ne postoji"
        if error is not None:
            flash(error)
            return render_template('invoice/create.html')
        else:
            return redirect(url_for('invoice.index'))


@bp.route('/invoice_import', methods=['GET', 'POST'])
@login_required
def invoice_import():
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


@bp.route('/invoice_export', methods=['GET'])
@login_required
def invoice_export():
    if request.method == 'GET':
        filename = "transakcije.csv"
        db = get_db()
        query = '''SELECT p.code, p.name, p.price, i.quantity'
                ' FROM product p JOIN invoice i ON p.code=i.product_code'''
        df = pd.read_sql_query(query, db)
        df.to_csv(filename, index=False)
        return Response(
            open(filename, 'r'),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment;filename={filename}'}
        )
    return redirect(url_for('index'))
