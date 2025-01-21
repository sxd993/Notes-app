from flask import Flask, render_template, request, redirect, url_for
from flask.views import MethodView

app = Flask(__name__)

class HomePage(MethodView):
    def get(self):
        return render_template('home.html')


class NotePages(MethodView):
    notes = []

    def get(self):
        return render_template('notes.html', notes=self.notes)
    
    def post(self):
        note = request.form.get('note')
        note_to_delete = request.form.get('note_to_delete')

        if note:
            self.notes.append(note)
        elif note_to_delete:
            if note_to_delete in self.notes:
                self.notes.remove(note_to_delete)
        
        return redirect(url_for('notes'))



app.add_url_rule('/ddd', view_func=HomePage.as_view('home'))    
app.add_url_rule('/', view_func=NotePages.as_view('notes'))



if __name__ == '__main__':
    app.run(debug=True)
