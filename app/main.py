from flask import Flask, render_template, jsonify
from data import db_session
from data.users import User
from forms.user import RegisterForm
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
app.config["SECRET_KEY"] = SECRET_KEY


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password.data:
            return render_template("register.html", form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()
        items = db_sess.query(User).filter(User.email == form.email.data).all()
        if items:
            return render_template("register.html", form=form, message="К этой почте уже привязан аккаунт")

        try:
            int(form.age.data)
        except ValueError:
            return render_template("register.html", form=form, message="Неверно введен возраст")

        user = User(
            name=form.name.data,
            email=form.email.data,
            age=int(form.age.data)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return jsonify({"status": "SUCCESS!"})

    return render_template("register.html", form=form)


if '__main__' == __name__:
    main()