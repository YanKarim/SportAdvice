from flask_restful import reqparse, Resource
from flask import jsonify, request
from . import db_session
from .users import User


class RegisterResources(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser() # создаем парсер для принятия аргументов
        self.parser.add_argument('name', type=str, required=True, help='Имя обязательно')
        self.parser.add_argument('email', type=str, required=True, help='Email обязателен')
        self.parser.add_argument('age', type=int, required=True, help='Возраст обязателен')
        self.parser.add_argument('password', type=str, required=True, help='Пароль обязателен')
        self.parser.add_argument('password_again', type=str, required=True, help='Подтверждение пароля обязательно')

    def post(self):
        if request.is_json: # чтобы можно было через json
            args = self.parser.parse_args()
        else:
            args = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'age': request.form.get('age'),
                'password': request.form.get('password'),
                'password_again': request.form.get('password_again')
            }

        if args["password"] != args["password_again"]:
            return {"ERROR": "Пароли не совпадают"}, 400

        db_sess = db_session.create_session()
        item = db_sess.query(User).filter(User.email == args["email"]).first()
        if item:
            db_sess.close()
            return {"ERROR": "На почту уже зарегистрирован аккаунт"}, 409

        user = User(
            name=args["name"],
            email=args["email"],
            age=args["age"]
        )
        user.set_password(args["password"])
        try:
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return {"status": "SUCCESS!"}, 201

        except Exception as e:
            db_sess.rollback() # откат
            db_sess.close()
            return {"ERROR": str(e)}, 500
