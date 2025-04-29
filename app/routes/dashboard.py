import re
import httpx
# import traceback
import subprocess
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from app.models.stepperMotor import StepperMotor
from app import os, db
from app.utils.common import is_ip_alive, format_mac

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
            'device_id': motor.device_id,
            'software_version': motor.software_version,
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
            # Step 1: Try to fetch the model name
            try:
                if is_ip_alive(ip_address):
                    model_url = f"http://{ip_address}/od/1008/00"
                    model_response = httpx.get(model_url)
                    model_number = model_response.text.strip('\"') if model_response.text else ''
                else:
                    print(f"IP {ip_address} is not reachable.")
                    model_number = 'ip not reachable'
            except Exception as e:
                print(f"Model number fetch failed: {e}")
                # error_details = traceback.format_exc()
                # print(f"Model fetch failed: {e}\n{error_details}")
                model_number = 'api no response'

            # Step 2: Create or update motor entry
            formated_mac_address = format_mac(mac_address)
            motor = StepperMotor.query.filter_by(mac_address=formated_mac_address).first()
            if motor:
                motor.ip_address = ip_address
                motor.connected = True
                if model_number:
                    motor.model_number = model_number
            else:
                last_motor = StepperMotor.query.order_by(StepperMotor.engine_number.desc()).first()
                next_engine_number = (int(last_motor.engine_number) + 1) if last_motor else 1
                motor = StepperMotor(
                    engine_number=next_engine_number,
                    mac_address=formated_mac_address,
                    ip_address=ip_address,
                    connected=True,
                    model_number=model_number,
                )
                db.session.add(motor)
            db.session.commit()
            return jsonify({'ip': ip_address})
        else:
            return jsonify({'error': 'ping failed.'})
    except Exception as e:
        return jsonify({'error': str(e)})
        # error_details = traceback.format_exc()
        # return jsonify({'error': str(e), 'details': error_details})

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

@bp.route('/delete/<int:motor_id>', methods=['POST'])
def delete_motor(motor_id):
    motor = StepperMotor.query.get_or_404(motor_id)

    db.session.delete(motor)
    db.session.commit()

    flash(f"Stepper Motor {motor.mac_address} deleted successfully!", 'success')
    return redirect(url_for('dashboard.system_settings'))