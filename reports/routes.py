from flask import Blueprint, render_template, session, current_app, request, redirect, flash, url_for

from database.sql_provider import SQLProvider
from database.operations import select_from_db, call_proc

from decorators.routes import login_required, role_required

reports_app = Blueprint('reports_app', __name__, template_folder='templates')
sql_provider = SQLProvider('reports/sql')


def query_execution(key, sql_statement_name):
    data = request.form.get(key)

    if not data:
        return False, "Данные не введены"

    sql_statement = sql_provider.get(sql_statement_name, {key: data})
    result = select_from_db(
        current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if not result:
        return False, "Отчет не найден"

    return True, result


@reports_app.route('/')
@login_required(session)
@role_required(session)
def reports_index():
    return render_template('reports_index.html', reports=current_app.config['reports_list'])


def get_report():
    if request.method == 'GET':
        rep_id = request.args.get('rep_id')
    elif request.method == 'POST':
        rep_id = request.form.get('rep_id')

    try:
        report = next(
            report for report in current_app.config['reports_list'] if report['rep_id'] == rep_id)
    except StopIteration:
        flash('Отчет не найден', 'error')
        return None

    return report


@reports_app.route('/view-report', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def view_report():
    report = get_report()
    if report is None:
        return redirect('/reports')

    if request.method == 'GET':
        return render_template('view_report.html', name=report['rep_name'], rep_id=report['rep_id'])
    elif request.method == 'POST':
        check_flag, result = query_execution('date', report['sql_statement'])
        if check_flag:
            cost = sum(item['amount'] * item['price'] for item in result)
            return render_template('view_report.html', name=report['rep_name'], rep_id=report['rep_id'], result=result, cost=cost)
        else:
            flash(result, 'error')
            return redirect(url_for('reports_app.view_report', rep_id=report['rep_id']))


@reports_app.route('/create-report', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def create_report():
    report = get_report()
    if report is None:
        return redirect('/reports')

    if request.method == 'GET':
        return render_template('create_report.html', name=report['rep_name'], rep_id=report['rep_id'])
    elif request.method == 'POST':
        procedure = report['procedure']
        date = request.form.get('date')

        result = call_proc(
            current_app.config['MYSQL_DB_CONFIG'], procedure, f'{date}-01')

        if result:
            flash(result, 'error')
        else:
            flash('Отчет успешно создан', 'okay')
        return redirect(url_for('reports_app.create_report', rep_id=report['rep_id']))
