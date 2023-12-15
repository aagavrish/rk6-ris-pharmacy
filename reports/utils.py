from flask import request, current_app, flash, redirect
from functools import wraps

from database.operations import select_from_db


def get_report():
    if request.method == 'GET':
        rep_id = request.args.get('rep_id')
    elif request.method == 'POST':
        rep_id = request.form.get('rep_id')

    try:
        report = next(
            report for report in current_app.config['reports_list']
            if report['rep_id'] == rep_id)
    except StopIteration:
        flash('Отчет не найден', 'error')
        return None

    return report


def report_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        report = get_report()
        if report is None:
            flash('Отчет не найден', 'error')
            return redirect('/reports')
        return f(report, *args, **kwargs)
    return decorated_function


def query_execution(key, sql_statement_name, sql_provider):
    data = request.form.get(key)

    if not data:
        return False, "Данные не введены"

    sql_statement = sql_provider.get(sql_statement_name, {key: data})
    result = select_from_db(
        current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if not result:
        return False, "Отчет не найден"

    return True, result
