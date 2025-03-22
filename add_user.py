from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():

    new_user = User(name="John Doe",license_number="123456")
    db.session.add(new_user)
    db.session.commit()

    print(f"User {new_user.name} with license number {new_user.license_number} has been created")