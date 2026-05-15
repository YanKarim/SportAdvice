from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager
from data import db_session
from forms.user import RegisterForm, LoginForm
from data.user_resources import RegisterResources, LoginResources, ProfileResources, RefreshResources, TableResources
from flask_restful import Api
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()


app = Flask(__name__)
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
app.config["SECRET_KEY"] = SECRET_KEY
app.config['JSON_AS_ASCII'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
api = Api(app)
jwt = JWTManager(app)
api.add_resource(RegisterResources, "/api/register")
api.add_resource(LoginResources, "/api/login")
api.add_resource(ProfileResources, "/api/profile")
api.add_resource(RefreshResources, "/api/refresh")
api.add_resource(TableResources, "/api/table")


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return {"ERROR": "Missing or invalid token"}, 401

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return {"ERROR": "Token has expired"}, 401

@jwt.invalid_token_loader
def invalid_token_response(error):
    return {"ERROR": "Invalid token"}, 401


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    return render_template("profile.html")

@app.route('/')
@app.route('/mainpage', methods=['GET', 'PUT'])
def mainpage():
    return render_template("mainpage.html")

@app.route('/sport')
def sport():
    return render_template("/training/training.html", title="Спорт")

@app.route('/sport/massa_nabor')
def massa_nabor():
    return render_template("/training/massa_nabor.html", title="Массанабор")

@app.route('/sport/dieta')
def diet():
    return render_template("/training/diet.html", title="Диета")

@app.route('/sport/training')
def training():
    return render_template("/training/exercise.html", title="Тренировки")

@app.route('/food')
def food():
    return render_template("/healthy food/food.html", title="Питание")


if '__main__' == __name__:
    main()