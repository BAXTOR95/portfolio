from app import app, db
from models import User

with app.app_context():
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    user = User(username=username, email=email, is_admin=True)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print(f"Admin user {username} created successfully.")
