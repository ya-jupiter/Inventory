from flask import Flask

app = Flask(__name__)

import RNAinventory.main

# SQL database
from RNAinventory import db
db.create_RNA_table()


# terminalからflask directoryが置いてある階層まで移動
# $ cd work/
# $ export FLASK_APP=RNAinventory
# $ export FALSK_ENV=develoment # debuk mode
# $ flask run