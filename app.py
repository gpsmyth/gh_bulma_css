from flask import Flask, render_template, request, redirect, url_for
import uuid
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # prod would be done differently
csrf = CSRFProtect(app)

todos = [
  {'id': str(uuid.uuid4()), 'task': 'Buy groceries', 'done': False},
  {'id': str(uuid.uuid4()), 'task': 'Walk the dog', 'done': True},
  {'id': str(uuid.uuid4()), 'task': 'Read a book', 'done': False},
  {'id': str(uuid.uuid4()), 'task': 'Go for a run', 'done': False},
]

@app.route('/')
def home():
  return render_template('index.html', todos=todos)

@app.route('/create-todo', methods=['POST'])
def create_todo():
  task = request.form.get('title')
  if task:
    new_todo = {'id': str(uuid.uuid4()), 'task': task, 'done': False}
    todos.append(new_todo)
  # return render_template('index.html', todos=todos)
  return redirect(url_for('home'))

@app.route('/update-todo/<todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
  for todo in todos:
    if todo['id'] == todo_id:
      todo['done'] = not todo['done']
      break
  # return render_template('index.html', todos=todos)
  # UX/bug: you currently return render_template(...) after POST requests. 
  # That can cause duplicate submissions if the user reloads the page. 
  # Use Post/Redirect/Get (redirect to the home route) after handling POSTs.
  return redirect(url_for('home'))

@app.route('/delete-todo/<todo_id>', methods=['GET', 'POST'])
def delete_todo(todo_id):
  global todos
  todos = [todo for todo in todos if todo['id'] != todo_id]
  # return render_template('index.html', todos=todos)
  return redirect(url_for('home'))

if __name__ == '__main__':
  app.run(debug=True, port=8000)