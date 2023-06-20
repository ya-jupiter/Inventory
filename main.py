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
            'note': row[2],
            'length': row[3],
            'excoef': row[4]
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
    sequence = request.form['sequence'].upper()
    sequence = sequence.replace(' ', '')
    # need to raise error if containing other letters
    note = request.form['note']
    length = len(sequence)
    excoef = CalcExCoef(sequence)
    print(f'ex coef: {excoef}')

    # register to SQL by INSERT command of SQL
    con = sqlite3.connect(DATABASE)

    # ?,?,? will be the following list
    con.execute('INSERT INTO seqs VALUES(?, ?, ?, ?, ?)', 
                [name, sequence, note, length, excoef])
    con.commit()
    con.close()
    return redirect(url_for('index'))

# Calculate extinction coefficiency
def CalcExCoef(sequence):
    length = len(sequence)
    ep1 = 0
    ep2 = 0

    ep1_dict = {
        "AA": 13.7, "AC": 10.5, "AG": 12.5, "AU": 12.0,
        "CA": 10.5, "CC": 7.1, "CG": 8.9, "CU": 8.1,
        "GA": 12.6, "GC": 8.7, "GG": 10.8, "GU": 10.6,
        "UA": 12.3, "UC": 8.6, "UG": 10.0, "UU": 9.8
    }

    ep2_dict = {
        "A": 15.4, "C": 7.2, "G": 11.5, "U": 9.9
    }

    for i in range(1, length):
        xy = sequence[i-1:i+1]
        y = sequence[i]

        ep1 += ep1_dict[xy]

        if i < length - 1:
            ep2 += ep2_dict[y]

    print(sequence)
    print(2 * ep1 - ep2)

    return 2 * ep1 - ep2
