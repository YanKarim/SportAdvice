from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
app.config["SECRET_KEY"] = SECRET_KEY


@app.route('/')
def main():
    return ""


if '__main__' == __name__:
    app.run(port=8080, host='127.0.0.1')