from flask import render_template, request, redirect, url_for
import sqlite3

from RNAinventory import app

DATABASE = 'database.db'

# top画面の設定
@app.route('/') # web appのtopにきたらindex関数を呼び出すという設定
def index():
    con = sqlite3.connect(DATABASE) # conncection instance
    db_seqs = con.execute('SELECT * FROM seqs').fetchall() # make list from SQL
    con.close()
    # at this point, db data is in tuples in list
    # need to convert to dicts in list

    seqs = []
    # convert tuple to dict
    for row in db_seqs:
        seqs.append({
            'name': row[0],
            'sequence': row[1],
            'note': row[2]
            })
        
    # up index.html
    return render_template(
        'index.html',           # index.htmlを起動するように設定
        seqs=seqs               # 引数に辞書を指定する
        ) 

# resigter page
@app.route('/form') # url
def form():
    return render_template(
        'form.html'
    )

# register function
@app.route('/register', methods=['POST'])
def register():
    # get data from form with flask.request method
    name = request.form['name']
    sequence = request.form['sequence']
    note = request.form['note']

    # register to SQL by INSERT command of SQL
    con = sqlite3.connect(DATABASE)

    # ?,?,? will be the following list
    con.execute('INSERT INTO seqs VALUES(?, ?, ?)', 
                [name, sequence, note])
    con.commit()
    con.close()
    return redirect(url_for('index'))
