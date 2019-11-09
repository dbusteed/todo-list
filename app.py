from flask import Flask, render_template, g, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'some-sneaky-stuff'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():

    c = get_db().cursor()
    
    rows = c.execute('SELECT * FROM Todo')

    return render_template('index.html', rows=rows)


@app.route('/add', methods=['POST'])
def add():
    
    todo = request.form['todo']
    date = request.form['date']

    if len(todo) > 0 and len(date) > 0:
        c = get_db().cursor()
        c.execute(f"INSERT INTO Todo(Text, Due_date) VALUES('{todo}', '{date}');")
        c.execute('COMMIT')

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    c = get_db().cursor()
    c.execute(f"DELETE FROM Todo WHERE ID={id}")
    c.execute('COMMIT')

    return redirect('/')


if __name__ == '__main__':
    app.run()