from getpass import getpass
import sys

from webapp import create_app
from webapp.user.models import db, User

app = create_app()

with app.app_context():
    username = input("Введите имя пользователя: ")

    if User.query.filter(User.user_name == username).count():
        print('Пользователь с таким именем уже существует')
        sys.exit(0)

    password = getpass("Введите пароль: ")
    password2 = getpass("Введите пароль повторно: ")

    if password != password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(
        user_name=username,
        role='admin'
    )

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print(f"Создан ползователь с id {new_user.id}!")