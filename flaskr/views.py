# -*- coding: utf-8 -*-


import os
import re
import functools
import datetime

from flaskr import app, socketio

from flask import render_template, request, flash, url_for, redirect, jsonify, g, session
from werkzeug.utils import secure_filename
from flask_socketio import emit

from service.JiraService import JiraService
from service.WorkBookService import WorkBookService
from Utils import log_conf

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

jira_service = JiraService()
module_logger = log_conf()
ALLOWED_EXTENSIONS = set(['xlsx'])
project_name = ''
cases = []


def allowed_file(filename):
    # 检查文件格式是否正确
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def secure_filename(filename):
    # 确保文件不包含 / -
    filename = re.sub('[""\/\--]+', '-', filename)
    filename = re.sub(r':-', ':', filename)
    filename = re.sub(r'^-|-$', '', filename)
    return filename


def login_required(view):
    # 视图装饰器，未登录的用户重定向到登录页
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view


@app.before_request
def load_logged_in_user():
    user = session.get('user')
    if user is None:
        g.user = None
    else:
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        jira_service.user = request.form.get('username')
        jira_service.password = request.form.get('pass')
        if request.form.get('host')[-1] == '/':
            jira_service.host = request.form.get('host')[:-2]

        status_code = jira_service.is_login()
        if status_code == 401 or status_code == 403:
            flash("Invalid user")
        else:
            session.clear()
            session['user'] = jira_service.user
        return redirect(url_for('import_case'))
    return render_template("index.html")


@app.route('/rest/api/projects', methods=['GET'])
@login_required
def get_projects():
    return jsonify(jira_service.get_projects())


@app.route('/import', methods=['GET', 'POST'])
@login_required
def import_case():
    # 获取项目名称和要导入的用例文件
    global project_name, cases
    if request.method == 'POST':
        project_name = request.form['project']
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('import_case'))
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            last_index = file_name.rfind('.')
            name = file_name[:last_index]
            ext = file_name[last_index+1:]
            saved_file = g.user + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_' + name + '.' + ext
            file.save(os.path.join(PATH('../TestCase'), saved_file))

            wb = WorkBookService(os.path.join(PATH('../TestCase'), saved_file))
            cases = wb.get_test_cases()

            return jsonify(cases)
    return render_template("case.html")


@app.route('/rest/api/logs', methods=['GET'])
@login_required
def get_logs():
    # ajax api for displaying real time logs
    with open(os.path.join(PATH('../Log'), '2019-08-30.log'), 'r') as logs:
        return jsonify({'logs': logs.read()})


@socketio.on('my_event', namespace='/cases')
def send_cases(message):
    uploaded = False
    while not uploaded:
        project_id = jira_service.get_project_id(project_name)
        if len(cases) == 0:
            module_logger.warning("case file is empty!")
            return
        else:
            for i in range(len(cases)):
                module_logger.info("case: {0}".format(cases[i]))
                case = jira_service.generate_issue_payload(cases[i]["title"], project_id=project_id)
                emit('my_response', cases[i]['title'])
                # issue_id = jira_service.create_issue(case)
                for j in range(len(cases[i]["steps"])):
                    step = cases[i]["steps"][j]
                    # jira_service.add_test_step(issue_id, step)
                    emit('my_response', cases[i]["steps"][j])

        uploaded = True
    emit('disconnect', 'disconnect')