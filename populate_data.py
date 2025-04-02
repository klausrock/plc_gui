from app import create_app, db
from app.models.user import User
from app.models.stepperMotor import StepperMotor

app = create_app()

def add_users(users):
    db.session.bulk_save_objects(users)

def add_motors(motors):
    db.session.bulk_save_objects(motors)

with app.app_context():

    # Adding users
    test_users = [
        User(name="John Doe", license_number="123456")
    ]

    # Adding motors
    test_motors = [
        StepperMotor(engine_number=1, mac_address='AA-BB-CC-DD-EE-01', ip_address='192.168.1.101',
                     model_number='PD4-E601L42-E-65-3A', connected=True, tested=True),
        StepperMotor(engine_number=2, mac_address='AA-BB-CC-DD-EE-02', ip_address='192.168.1.102',
                     model_number='PD4-E601L42-E-65-3A', connected=True, tested=False),
        StepperMotor(engine_number=3, mac_address='AA-BB-CC-DD-EE-03', ip_address=None, model_number=None,
                     connected=False, tested=False),
        StepperMotor(engine_number=4, mac_address='AA-BB-CC-DD-EE-04', ip_address='192.168.1.104',
                     model_number='PD4-E601L42-E-65-3A', connected=True, tested=True),
    ]

    add_users(test_users)
    add_motors(test_motors)

    db.session.commit()

    print("Data added successfully!")