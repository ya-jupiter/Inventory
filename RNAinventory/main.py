import csv
import io
from flask import render_template, request, redirect, send_file, url_for
import pandas as pd
import sqlite3

from RNAinventory import app, utils


DATABASE = './RNAinventory/database.db'

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
            'excoef': row[4],
            'a260': row[5],
            'conc': row[6],
            'volume': row[7],
            'mol': row[8]
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
    note = request.form['note']
    
    try:
        a260 = float(request.form['a260'])
        volume = float(request.form['volume'])
    except ValueError:
        return 'A260 or volume value are not numeric', 400
        
    register_info = utils.RegistrationInfo(name, sequence, note, a260, volume)
    if register_info[0] == False:
        return register_info[1], 400
    
    id = (register_info[0], register_info[2])
    
    # register to SQL by INSERT command of SQL
    con = sqlite3.connect(DATABASE)
    
    # check data duplication
    ids = con.execute('SELECT name, note FROM seqs').fetchall()
    print(id)
    print(ids)
    
    if id in ids:
        return f'Trying to register Name and Note, those are already registered in Inventory', 400

    # ?,?,? will be the following list
    con.execute('INSERT INTO seqs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                register_info)
    con.commit()
    con.close()
    return redirect(url_for('index'))

# batch input page page
@app.route('/batch') # url
def batch():
    return render_template('batch.html')
    
# download for batch tempplate
@app.route('/download')
def download_template():
    return send_file('templates/template.csv', as_attachment=True)

# upload batch template
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    # error 
    if not file:
        return 'No file is selected', 400
    
    if file.filename.endswith('.csv'):
        file_path = '/work/RNAinventory/uploaded/temp.csv'
        df = pd.read_csv(file)
        data = []
        for r in df.itertuples():
            data.append(r)
        
        df.to_csv(file_path, index=False)
    
    # error if file is not csv   
    else:
        return 'Only CSV format is allowed', 400
    return render_template('upload.html', data=data)

# batch_register
@app.route('/batch_register', methods=['POST'])
def batch_register():
    file_path = '/work/RNAinventory/uploaded/temp.csv'
    df = pd.read_csv(file_path)
    
    # each row will be registered to SQL by for loop
    con = sqlite3.connect(DATABASE)
    
    for i, r in df.iterrows():
        name = r['Name']
        sequence = r['Sequence']
        note = r['Note']
        a260 = r['A260']
        volume = r['volume(uL)']
        
        register_info = utils.RegistrationInfo(name, sequence, note, a260, volume)
        if register_info[0] == False:
            return register_info[1], 400
    
        # ?,?,? will be the following list
        con.execute('INSERT INTO seqs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                    register_info)
        con.commit()
         
    con.close()
     
    return redirect(url_for('index'))