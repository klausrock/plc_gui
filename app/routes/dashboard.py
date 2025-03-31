import re
import subprocess
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.models.stepperMotor import StepperMotor
from app import os

bp = Blueprint('dashboard', __name__, url_prefix='')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('views/dashboard/index.html')

@bp.route('system-settings')
@login_required
def system_settings():
    motors = StepperMotor.query.all()
    motors_list = [
        {
            'engine_number': motor.engine_number,
            'mac_address': motor.mac_address,
            'ip_address': motor.ip_address,
            'model_number': motor.model_number,
            'connected': motor.connected,
            'tested': motor.tested,
            'created_at': motor.created_at
        } for motor in motors
    ]
    return render_template('views/dashboard/system_settings.html', motors=motors_list)

@bp.route('ping_mac', methods=['POST'])
@login_required
def ping_mac():
    data = request.get_json()
    mac_address = data.get('mac')

    if not mac_address:
        return jsonify({'error': 'MAC address is required'}), 400

    # Assuming you have DNS configured to resolve MAC.fritz.box to an IP
    # ping_command = f"ping -n 1 {mac_address}.fritz.box" if os.name == 'nt' else f"ping -c 1 {mac_address}.fritz.box"

    # Ensure MAC is uppercase and clean
    mac_hostname = f"MAC-{mac_address}.fritz.box"
    # mac_hostname = f"MAC-{raw_mac}"
    ping_command = f"ping -n 1 {mac_hostname}" if os.name == 'nt' else f"ping -c 1 {mac_hostname}"

    try:
        result = subprocess.run(ping_command, shell=True, capture_output=True, text=True)

        # Extract IP Address from the response
        match = re.search(r'\[(.*?)\]' if os.name == 'nt' else r'\((.*?)\)', result.stdout)
        ip_address = match.group(1) if match else None

        if ip_address:
            return jsonify({'ip': ip_address})
        else:
            return jsonify({'error': 'ping failed.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@bp.route('/save_data', methods=['POST'])
@login_required
def save_data():
    data = request.get_json()
    return data