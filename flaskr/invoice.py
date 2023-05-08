from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('invoice', __name__)


@bp.route('/')
def index():
    db = get_db()
    invoices = db.execute(
        'SELECT p.code, p.name, p.price, i.quantity'
        ' FROM product p JOIN invoice i ON p.code=i.product_code'
    ).fetchall()
    print(invoices)
    return render_template('invoice/index.html', invoices=invoices)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        product_code = request.form['product_code']
        quantity = request.form['quantity']
        error = None

        if not product_code:
            error = 'product_code is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO invoice (product_code, quantity)'
                ' VALUES (?, ?)',
                (product_code, quantity)
            )
            db.commit()
            return redirect(url_for('invoice.index'))

    return render_template('invoice/create.html')

