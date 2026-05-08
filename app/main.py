from flask import Flask, render_template, jsonify
from data import db_session
from data.users import User
from forms.user import RegisterForm
from data.user_resources import RegisterResources
from flask_restful import Api
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
app.config["SECRET_KEY"] = SECRET_KEY
app.config['JSON_AS_ASCII'] = False
api = Api(app)
api.add_resource(RegisterResources, "/register")


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Если нужна CSRF защита
    return render_template("register.html", form=form)


if '__main__' == __name__:
    main()