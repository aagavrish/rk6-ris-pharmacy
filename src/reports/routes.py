from reports.utils import report_required, query_execution
from flask import (Blueprint, render_template, session,
                   current_app, request, flash)

from database.sql_provider import SQLProvider
from database.operations import call_proc

from decorators.routes import login_required, role_required


reports_app = Blueprint('reports_app', __name__, template_folder='templates')
sql_provider = SQLProvider('reports/sql')


@reports_app.route('/')
@login_required(session)
@role_required(session)
def reports_index():
    return render_template('reports_index.html',
                           reports=current_app.config['reports_list'])


@reports_app.route('/view-report', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
@report_required
def view_report(report):
    if request.method == 'POST':
        if report['sql_statement'] == "":
            flash('Возникла непредвиденная ошибка', 'error')
            return render_template('view_report.html',
                                   name=report['rep_name'],
                                   rep_id=report['rep_id'])

        check_flag, result = query_execution(
            'date', report['sql_statement'], sql_provider)
        if check_flag:
            cost = sum(item['amount'] * item['price'] for item in result)
            return render_template('view_report.html',
                                   name=report['rep_name'],
                                   rep_id=report['rep_id'],
                                   result=result,
                                   cost=cost)
        else:
            flash(result, 'error')
    return render_template('view_report.html',
                           name=report['rep_name'],
                           rep_id=report['rep_id'])


@reports_app.route('/create-report', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
@report_required
def create_report(report):
    if request.method == 'POST':
        procedure = report['procedure']
        date = request.form.get('date')

        if procedure == "":
            flash('Возникла непредвиденная ошибка', 'error')
            return render_template('create_report.html',
                                   name=report['rep_name'],
                                   rep_id=report['rep_id'])

        result = call_proc(
            current_app.config['MYSQL_DB_CONFIG'], procedure, f'{date}-01')

        if result:
            flash(result, 'error')
        else:
            flash('Отчет успешно создан', 'okay')
    return render_template('create_report.html',
                           name=report['rep_name'],
                           rep_id=report['rep_id'])
