from flask import (Blueprint, render_template, request,
                   current_app, flash, session, redirect, url_for)
from database.sql_provider import SQLProvider
from database.operations import select_from_db, insert_into_db

from decorators.routes import login_required, role_required

from datetime import date

basket_app = Blueprint('basket_app', __name__, template_folder='templates')
sql_provider = SQLProvider('basket/sql')


@basket_app.route('/', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def basket_index():
    if not session.get('basket'):
        session['basket'] = []

    sql_statement = sql_provider.get('select_all_med.sql', {})
    result = select_from_db(
        current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if request.method == 'POST':
        med_id = request.form['med_ID']
        cost = request.form['cost']
        quantity = int(request.form['quantity'])

        stock_amount = next((item['amount']
                            for item in result if item['med_ID'] == med_id), 0)

        for item in session['basket']:
            if item['med_ID'] == med_id and item['cost'] == cost:
                if item['quantity'] + quantity > stock_amount:
                    flash(
                        'Количество товара в корзине \
                            превысит доступное количество на складе',
                        'error')
                    break
                item['quantity'] += quantity
                flash('Добавлено в корзину', 'okay')
                break
        else:
            session['basket'].append(
                {'med_name': request.form['med_name'],
                    'quantity': quantity,
                    'med_company': request.form['med_company'],
                    'cost': cost,
                    'med_ID': med_id})
            flash('Добавлено в корзину', 'okay')
        session.modified = True

    return render_template('basket_index.html',
                           count=len(session['basket']),
                           result=result)


@basket_app.route('/show', methods=['GET'])
@login_required(session)
@role_required(session)
def show_basket_handler():
    basket = session.get('basket')
    if len(basket) == 0:
        flash('Корзина пуста', 'error')
        return redirect(url_for('basket_app.basket_index'))
    else:
        cost = 0
        for item in basket:
            cost += int(item['cost']) * int(item['quantity'])
        return render_template('show_basket.html', basket=basket, cost=cost)


@basket_app.route('/delete-all', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def delete_all_handler():
    session['basket'] = []
    session.modified = True
    flash('Корзина очищена', 'okay')
    return redirect(url_for('basket_app.basket_index'))


@basket_app.route('/delete-current', methods=['POST'])
@login_required(session)
@role_required(session)
def delete_current_handler():
    basket = session.get('basket', [])
    session['basket'] = [product for product in basket if product['med_ID']
                         != request.form.get('med_ID')]
    session.modified = True

    return redirect(url_for('basket_app.show_basket_handler'))


@basket_app.route('/create-order', methods=['POST'])
@login_required(session)
@role_required(session)
def create_order_handler():
    username = session.get('user')
    basket = session.get('basket', [])
    date_now = date.today()

    for item in basket:
        sql_statement = sql_provider.get('create_order.sql', {
                                         'username': username,
                                         'med_ID': item['med_ID'],
                                         'quantity': item['quantity'],
                                         'price': item['cost'],
                                         'date': date_now})
        insert_into_db(current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    session['basket'] = []
    session.modified = True
    flash('Заказ успешно создан', 'okay')
    return redirect(url_for('basket_app.basket_index'))
