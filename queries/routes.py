from flask import Blueprint, render_template, request, current_app, flash, session
from database.sql_provider import SQLProvider
from database.operations import select_from_db, insert_into_db

from decorators.routes import login_required, role_required

queries_app = Blueprint('queries_app', __name__, template_folder='templates')
sql_provider = SQLProvider('queries/sql')


def query_execution(key, sql_statement_name):
    data = request.form.get(key)

    if not data:
        return False, "Данные не введены"

    sql_statement = sql_provider.get(sql_statement_name, {key: data})
    result = select_from_db(
        current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if not result:
        return False, "Нет результатов"

    return True, result


@queries_app.route('/', methods=['GET'])
@login_required(session)
def queries_index():
    return render_template('queries_index.html')


# ================= PHARMACIST =================

@queries_app.route('/search-med-by-name', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def search_med_by_name():
    if request.method == 'GET':
        return render_template('search_med_by_name.html')
    elif request.method == 'POST':
        check_flag, result = query_execution(
            'med_name', 'search_med_by_name.sql')

        if check_flag:
            return render_template('search_med_by_name.html', result=result)
        else:
            flash(result, 'error')
            return render_template('search_med_by_name.html')


@queries_app.route('/search-med-by-country', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def search_med_by_country():
    if request.method == 'GET':
        return render_template('search_med_by_country.html')
    elif request.method == 'POST':
        check_flag, result = query_execution(
            'med_country', 'search_med_by_country.sql')

        if check_flag:
            return render_template('search_med_by_country.html', result=result)
        else:
            flash(result, 'error')
            return render_template('search_med_by_country.html')


@queries_app.route('/search-med-by-group', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def search_med_by_group():
    if request.method == 'GET':
        return render_template('search_med_by_group.html')
    elif request.method == 'POST':
        check_flag, result = query_execution(
            'med_group', 'search_med_by_group.sql')

        if check_flag:
            return render_template('search_med_by_group.html', result=result)
        else:
            flash(result, 'error')
            return render_template('search_med_by_group.html')

# ==============================================


# ================ MERCHANDISER ================

@queries_app.route('/search-supplier-by-city', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def search_supplier_by_city():
    if request.method == 'GET':
        return render_template('search_supplier_by_city.html')
    elif request.method == 'POST':
        check_flag, result = query_execution(
            'city', 'search_supplier_by_city.sql')

        if check_flag:
            return render_template('search_supplier_by_city.html', result=result)
        else:
            flash(result, 'error')
            return render_template('search_supplier_by_city.html')


@queries_app.route('/show-order-by-date', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_order_by_date():
    if request.method == 'GET':
        return render_template('show_ord_by_date.html')
    elif request.method == 'POST':
        check_flag, result = query_execution(
            'conclusion_date', 'show_ord_by_date.sql')

        if check_flag:
            return render_template('show_ord_by_date.html', result=result)
        else:
            flash(result, 'error')
            return render_template('show_ord_by_date.html')


@queries_app.route('/show-med-balance-by-group', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_med_balance_by_group():
    if request.method == 'GET':
        return render_template('show_balance_by_group.html')
    elif request.method == 'POST':
        check_flag, result = query_execution(
            'med_group', 'show_balance_by_group.sql')

        if check_flag:
            return render_template('show_balance_by_group.html', result=result)
        else:
            flash(result, 'error')
            return render_template('show_balance_by_group.html')

# ==============================================


# =================== MANAGER ==================

@queries_app.route('/add-new-internal-user', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def add_new_internal_user():
    if request.method == 'GET':
        return render_template('add_new_internal_user.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        sql_statement = sql_provider.get(
            'check_user_doesnt_exist.sql', {'username': username})
        result = select_from_db(
            current_app.config['MYSQL_DB_CONFIG'], sql_statement)

        if result:
            flash('Пользователь уже существует', 'error')
            return render_template('add_new_internal_user.html')
        else:
            insert_into_db(current_app.config['MYSQL_DB_CONFIG'], sql_provider.get(
                'insert_new_internal_user.sql', {'username': username, 'password': password, 'role': role}))
            flash('Пользователь успешно добавлен', 'okay')
            return render_template('add_new_internal_user.html')


@queries_app.route('/show-rating-by-orders-count', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_rating_by_orders_count():
    if request.method == 'GET':
        return render_template('show_rating_ord_by_month.html')
    elif request.method == 'POST':
        date = request.form.get('date')
        limit = request.form.get('limit')

        sql_statement = sql_provider.get(
            'show_rating_ord_by_month.sql', {'date': date, 'limit': limit})
        result = select_from_db(
            current_app.config['MYSQL_DB_CONFIG'], sql_statement)

        if result:
            return render_template('show_rating_ord_by_month.html', result=result)
        else:
            flash('Нет результатов', 'error')
            return render_template('show_rating_ord_by_month.html')

# ==============================================
