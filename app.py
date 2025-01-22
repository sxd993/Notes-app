from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'notes.db'

# Функция для работы с базой данных
def execute_query(query, params=(), fetch=False):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        conn.commit()

# Главная страница заметок
@app.route('/', methods=['GET', 'POST'])
def notes_page():
    if request.method == 'POST':
        note = request.form.get('note')
        note_to_delete = request.form.get('note_to_delete')

        if note:
            execute_query('INSERT INTO notes (content) VALUES (?)', (note,))
        elif note_to_delete:
            execute_query('DELETE FROM notes WHERE id = ?', (note_to_delete,))

        return redirect(url_for('notes_page'))

    notes = execute_query('SELECT id, content FROM notes', fetch=True)
    return render_template('notes.html', notes=notes)

# Инициализация базы перед запуском приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
