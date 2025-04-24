import httpx
from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models.stepperMotor import StepperMotor
from app import os, db
from app.utils.common import is_ip_alive

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/device-id/<string:ip>', methods=['GET'])
@login_required
def get_device_id(ip):
    try:
        ip_address = ip

        if not ip_address:
            return jsonify({'error': 'ip_address required'}), 400

        if is_ip_alive(ip_address):
            return jsonify({"error": f"IP {ip_address} is not reachable"}), 404

        device_id = fetch_device_id_from_ip(ip_address)
        if not device_id:
            return jsonify({'error': 'Failed to retrieve device ID'}), 502

        update_motor_device_id(ip_address, device_id)

        return jsonify({'device_id': device_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)})

def fetch_device_id_from_ip(ip):
    try:
        url = f"http://{ip}/od/4041/00"
        response = httpx.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip('"')
    except httpx.RequestError:
        return ''

def update_motor_device_id(ip, device_id):
    motor = StepperMotor.query.filter_by(ip_address=ip).first()
    if motor:
        motor.device_id = device_id
        db.session.commit()