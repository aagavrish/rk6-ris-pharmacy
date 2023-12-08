from flask import Flask, render_template, session, redirect, url_for

from access.routes import access_app
from queries.routes import queries_app
from reports.routes import reports_app
from basket.routes import basket_app

import json

app = Flask(__name__)
app.secret_key = 'e58b116b7a9c7fab192e1e0c68d713aa24c64382636fc22'
app.config['MYSQL_DB_CONFIG'] = json.load(open('configs/db_config.json'))

app.register_blueprint(access_app, url_prefix='/auth')
app.register_blueprint(queries_app, url_prefix='/queries')
app.register_blueprint(reports_app, url_prefix='/reports')
app.register_blueprint(basket_app, url_prefix='/basket')

with open('configs/reports.json', 'r', encoding='UTF-8') as file:
    reports = json.load(file)
    app.config['reports_list'] = [
        {
            'rep_name': report['rep_name'],
            'rep_id': report['rep_id'],
            'procedure': report['procedure'],
            'sql_statement': report['sql_statement']
        }
        for report in reports
    ]


@app.route('/', methods=['GET'])
@app.route('/main-page', methods=['GET'])
@app.route('/main-page/', methods=['GET'])
def index_handler():
    if 'is_auth' not in session:
        return redirect(url_for('access_app.access_index'))
    return render_template('index.html')


if __name__ == '__main__':
    settings = {'host': '127.0.0.1', 'port': 5000}
    app.run(host=settings['host'], port=settings['port'], debug=True)
