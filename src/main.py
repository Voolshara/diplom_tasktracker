from src.db import check_task, new_task, get_all_running_tasks, get_now_phone, set_data, change_status, get_all_close_tasks

from phonenumbers import parse as phone_parse
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# tasks = []
# completed_tasks = []

@app.route('/')
def index():
    args = request.args.to_dict()
    tasks = get_all_running_tasks()
    if "is_task_exist" in args:
        return render_template('index.html', tasks=tasks, is_task_exist=True)
    return render_template('index.html', tasks=tasks)

@app.route('/new', methods=['POST'])
def add_task():
    task = request.form['task']
    if check_task(task):
        new_task(task)
        return redirect(url_for('index'))
    return redirect(url_for('index', is_task_exist=True))
    
@app.route('/add_info', methods=['POST'])
def add_task_info():
    # ImmutableMultiDict([('phone', ''), ('email', 'sdf'), ('Nickname', ''), ('name', ''), ('addinfo', ''), ('task', 'dfs')])
    task_data = request.form.to_dict()
    old_phone, old_phone_text = get_now_phone(int(task_data['task']))
    if old_phone == task_data['phone']:
        task_data['phone_text'] = old_phone_text
    else:
        try:
            phone_info = str(phone_parse(task_data['phone']))
        except:
            phone_info = ""
        task_data['phone_text'] = phone_info
    set_data(task_data)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    change_status(int(task_id))
    return redirect(url_for('index'))

@app.route('/archive')
def archive():
    completed_tasks = get_all_close_tasks()
    return render_template('archive.html', completed_tasks=completed_tasks)

def run():
    app.run("0.0.0.0", port="5000", debug=False)
