from flask import Flask, render_template

app = Flask(__name__, template_folder="app/templates")

from app.routes import *

if __name__ == "__main__":
    app.run(debug=True)