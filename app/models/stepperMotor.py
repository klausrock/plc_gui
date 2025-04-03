from datetime import datetime

from app import db

class StepperMotor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    engine_number = db.Column(db.String(120), nullable=True)
    mac_address = db.Column(db.String(20), nullable=False, unique=True, index=True)
    ip_address = db.Column(db.String(45), nullable=False)
    model_number = db.Column(db.String(120), nullable=True)
    connected = db.Column(db.Boolean, nullable=True, default=False)
    tested = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
