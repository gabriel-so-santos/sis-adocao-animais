from flask import Flask, render_template
from database import init_db, Session

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

from app.routes import *

init_db()
session = Session()

if __name__ == "__main__":
    app.run(debug=True)