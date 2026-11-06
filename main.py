import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory database for simplicity
todos = [
    {"id": 1, "title": "Learn Python Flask", "completed": True},
    {"id": 2, "title": "Build a clean To-Do app", "completed": False},
    {"id": 3, "title": "Deploy to production", "completed": False}
]
next_id = 4

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimalist To-Do</title>
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --danger: #ef4444;
            --border: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 480px;
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        h1 {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.025em;
        }
        .todo-form {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }
        input[type="text"] {
            flex: 1;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--text);
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus {
            border-color: var(--primary);
        }
        button {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem 1.25rem;
            border-radius: 0.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: var(--primary-hover);
        }
        .todo-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 350px;
            overflow-y: auto;
        }
        .todo-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            background: var(--bg);
            border-radius: 0.5rem;
            border: 1px solid var(--border);
            transition: transform 0.1s;
        }
        .todo-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            cursor: pointer;
        }
        .todo-title {
            font-size: 0.95rem;
            word-break: break-all;
        }
        .completed .todo-title {
            text-decoration: line-through;
            color: var(--text-muted);
        }
        input[type="checkbox"] {
            accent-color: var(--primary);
            width: 1.1rem;
            height: 1.1rem;
            cursor: pointer;
        }
        .delete-btn {
            background: transparent;
            color: var(--danger);
            padding: 0.25rem 0.5rem;
            font-size: 0.85rem;
        }
        .delete-btn:hover {
            background: rgba(239, 68, 68, 0.1);
        }
        .empty-state {
            text-align: center;
            color: var(--text-muted);
            padding: 2rem 0;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tasks</h1>
        <form class="todo-form" action="/add" method="POST">
            <input type="text" name="title" placeholder="What needs to be done?" required autocomplete="off">
            <button type="submit">Add</button>
        </form>
        
        <ul class="todo-list">
            {% if todos %}
                {% for todo in todos %}
                <li class="todo-item {% if todo.completed %}completed{% endif %}">
                    <div class="todo-left" onclick="toggleTodo({{ todo.id }})">
                        <input type="checkbox" {% if todo.completed %}checked{% endif %}>
                        <span class="todo-title">{{ todo.title }}</span>
                    </div>
                    <form action="/delete/{{ todo.id }}" method="POST" style="display:inline;">
                        <button type="submit" class="delete-btn">Delete</button>
                    </form>
                </li>
                {% endfor %}
            {% else %}
                <div class="empty-state">No tasks yet. Enjoy your free time!</div>
            {% endif %}
        </ul>
    </div>

    <script>
        function toggleTodo(id) {
            fetch(`/toggle/${id}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    }
                });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    title = request.form.get('title', '').strip()
    if title:
        todos.append({"id": next_id, "title": title, "completed": False})
        next_id += 1
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            return jsonify({"success": True, "completed": todo['completed']})
    return jsonify({"success": False}), 404

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
