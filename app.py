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



# Cтраница авторизации
@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password') #Передает через форму данные


    return render_template('home.html')



# Главная страница заметок
@app.route('/notes', methods=['GET', 'POST'])
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


# Страница редактирования заметок
@app.route('/edit_note', methods=['GET', 'POST'])
def edit_note_page():
    note_id = request.args.get('note_id')  # Получаем ID заметки из URL
    if not note_id:
        return "Заметка не найдена", 404

    # Подключаемся к базе данных и получаем заметку
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()

        # Получаем заметку по ID
        cur.execute("SELECT content FROM notes WHERE id = ?", (note_id,))
        note_data = cur.fetchone()

        if not note_data:  # Если заметка не найдена
            return "Заметка не найдена", 404

        note = note_data[0]  # Текст заметки

        if request.method == 'POST':
            # Получаем обновлённое содержимое заметки из формы
            updated_note = request.form.get('updated_note')

            # Обновляем заметку в базе данных
            cur.execute("UPDATE notes SET content = ? WHERE id = ?",
                        (updated_note, note_id))
            conn.commit()

            # Перенаправляем на страницу со списком заметок
            return redirect(url_for('notes_page'))

    # Отображаем страницу редактирования
    return render_template('note_edit.html', note=note)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
