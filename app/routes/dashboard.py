import re
import subprocess
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from app.models.stepperMotor import StepperMotor
from app import os, db

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
            'id': motor.id,
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

    # Ensure MAC is uppercase and clean
    mac_hostname = f"MAC-{mac_address}.fritz.box"
    ping_command = f"ping -n 1 {mac_hostname}" if os.name == 'nt' else f"ping -c 1 {mac_hostname}"

    try:
        result = subprocess.run(ping_command, shell=True, capture_output=True, text=True)

        # Extract IP Address from the response
        match = re.search(r'\[(.*?)\]' if os.name == 'nt' else r'\((.*?)\)', result.stdout)
        ip_address = match.group(1) if match else None

        if ip_address:
            motor = StepperMotor.query.filter_by(mac_address=mac_address).first()
            if motor:
                motor.ip_address = ip_address
                motor.connected = True
            else:
                motor = StepperMotor(
                    mac_address=mac_address,
                    ip_address=ip_address,
                    connected=True
                )
                db.session.add(motor)
            db.session.commit()
            return jsonify({'ip': ip_address})
        else:
            return jsonify({'error': 'ping failed.'})
    except Exception as e:
        return jsonify({'error': str(e)})

@bp.route('/edit/<int:motor_id>')
@login_required
def edit_motor(motor_id):
    motor = StepperMotor.query.get_or_404(motor_id)
    return render_template('views/dashboard/edit_motor.html', motor=motor)

@bp.route('/update/<int:motor_id>', methods=['POST'])
@login_required
def update_motor(motor_id):
    motor = StepperMotor.query.get_or_404(motor_id)
    motor.engine_number = request.form.get('engine_number')
    motor.model_number = request.form.get('model_number')
    db.session.commit()
    flash('Stepper motor updated.', 'success')
    return redirect(url_for('dashboard.system_settings'))

@bp.route('/save_data', methods=['POST'])
@login_required
def save_data():
    data = request.get_json()
    return data