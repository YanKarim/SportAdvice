from flask_restful import reqparse, Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from . import db_session
from .users import User
from .tables import Table


class RegisterResources(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()  # создаем парсер для принятия аргументов
        self.parser.add_argument('name', type=str, required=True, help='Имя обязательно')
        self.parser.add_argument('email', type=str, required=True, help='Email обязателен')
        self.parser.add_argument('age', type=int, required=True, help='Возраст обязателен')
        self.parser.add_argument('password', type=str, required=True, help='Пароль обязателен')
        self.parser.add_argument('password_again', type=str, required=True, help='Подтверждение пароля обязательно')

    def post(self):
        if request.is_json:  # чтобы можно было через json
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

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        try:
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return {"status": "SUCCESS!", "access_token": access_token, "refresh_token": refresh_token,
                    "user": {"id": user.id, "name": user.name}}, 201

        except Exception as e:
            db_sess.rollback()  # откат
            db_sess.close()
            return {"ERROR": str(e)}, 500


class LoginResources(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()  # создаем парсер для принятия аргументов
        self.parser.add_argument('email', type=str, required=True, help='Email обязателен')
        self.parser.add_argument('password', type=str, required=True, help='Пароль обязателен')
        self.parser.add_argument('remember_me', type=bool, required=False, default=False)

    def post(self):
        if request.is_json:  # чтобы можно было через json
            args = self.parser.parse_args()
        else:
            args = {
                'email': request.form.get('email'),
                'password': request.form.get('password'),
                'remember_me': request.form.get('remember_me') == 'on'
            }

        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).filter(User.email == args["email"]).first()

            if user and user.check_password(args["password"]):
                access_token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                db_sess.close()
                return {"status": "SUCCESS", "access_token": access_token, "refresh_token": refresh_token,
                        "user": {"id": user.id, "name": user.name}}, 200

            else:
                db_sess.close()
                return {"ERROR": "неверный пароль или почта", }, 401

        except Exception as e:
            db_sess.rollback()  # откат
            db_sess.close()
            return {"ERROR": str(e)}, 500


class ProfileResources(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).get(int(user_id))

            if not user:
                return {"ERROR": "Пользователь не найден"}, 404
                db_sess.close()

            db_sess.close()
            return {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "age": user.age
                }
            }, 200
        except Exception as e:
            db_sess.close()
            return {"ERROR": str(e)}, 500

    @jwt_required()
    def put(self):
        # Обновление профиля (пример)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True)  # позже добавлю
        args = self.parser.parse_args()
        user_id = get_jwt_identity()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id)
        user.name = args['name']
        return {"status": "Profile updated"}, 200


class RefreshResources(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=user_id)
        return {"access_token": new_access_token}, 200


class TableResources(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=False)
        self.parser.add_argument('trainings', type=dict, required=False, location="json")
        self.parser.add_argument('food', type=dict, required=False, location="json")

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        db_sess = db_session.create_session()
        table = db_sess.query(Table).filter(Table.user_id == user_id).first()
        if not table:
            table = Table(
                name=f"Таблица №{user_id}",
                trainings={"Понедельник": "", "Вторник": "", "Среда": "", "Четверг": "", "Пятница": "", "Суббота": "",
                           "Воскресенье": ""},
                food={"Понедельник": "", "Вторник": "", "Среда": "", "Четверг": "", "Пятница": "", "Суббота": "",
                      "Воскресенье": ""},
                user_id=user_id
            )

            db_sess.add(table)
            db_sess.commit()

        return {"name": table.name, "trainings": table.trainings, "food": table.food}, 200

    @jwt_required()
    def post(self):
        pass  # там нечего создавать, при отсутствии создается при 1 запросе get

    @jwt_required()
    def delete(self):
        pass  # там нечего удалять, не нужно

    @jwt_required()
    def put(self):
        args = self.parser.parse_args()
        user_id = get_jwt_identity()
        name = args["name"]
        trainings = args["trainings"]
        food = args["food"]
        db_sess = db_session.create_session()
        table = db_sess.query(Table).filter(Table.user_id == user_id).first()
        if name:
            table.name = name if name is not None else table.name

        table.trainings = trainings if trainings is not None else table.trainings
        table.food = food if food is not None else table.food
        try:
            db_sess.commit()
            db_sess.close()
            return {"status": "SUCCESS"}, 200
        except Exception as e:
            db_sess.rollback()
            db_sess.close()
            return {"ERROR": f"{e}"}, 403
