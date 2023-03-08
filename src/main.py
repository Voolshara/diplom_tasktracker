from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

tasks = []
completed_tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append(task)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    completed_task = tasks.pop(task_id)
    completed_tasks.append(completed_task)
    return redirect(url_for('index'))

@app.route('/archive')
def archive():
    return render_template('archive.html', completed_tasks=completed_tasks)

def run():
    app.run(debug=False)
