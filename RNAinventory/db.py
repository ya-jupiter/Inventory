import sqlite3

DATABASE = './RNAinventory/database.db'

def create_RNA_table():
    con = sqlite3.connect(DATABASE)
    con.execute("""CREATE TABLE IF NOT EXISTS seqs (
        name,
        sequence,
        note,
        length,
        excoef,
        a260,
        conc,
        volume,
        mol
        )""")
    con.close()