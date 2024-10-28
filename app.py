from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from models import MonitorLog, ErrorLog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/log', methods=['POST'])
def add_log():
    data = request.get_json()

    if data['status'] == 'success':
        new_log = MonitorLog(
            status=data['status'],
            cpu=data['cpu_usage'],
            gpu=data['gpu_usage'],
            cpu_memory=data['memory_usage'],
            gpu_memory=data['gpu_memory_usage'],
            server=data['server']
        )
    elif data['status'] == 'failed':
        new_log = MonitorLog(
            status=data['status'],
            cpu=None,
            gpu=None,
            cpu_memory=None,
            gpu_memory=None,
            server=data['server']
        )
        error_log = ErrorLog(
            monitor_log=new_log,
            msg=data['error']
        )
        db.session.add(error_log)

    db.session.add(new_log)
    db.session.commit()

    return jsonify({'message': 'Log added successfully'}), 201

@app.route('/log', methods=['GET'])
def get_logs():
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    logs = MonitorLog.query.filter(MonitorLog.timestamp >= one_day_ago).all()
    result = []

    for log in logs:
        if log.status == 'success':
            result.append({
                'cpu_usage': log.cpu,
                'gpu_usage': log.gpu,
                'gpu_memory_usage': log.gpu_memory,
                'memory_usage': log.cpu_memory,
                'status': log.status,
                'server': log.server
            })
        elif log.status == 'failed':
            error_log = ErrorLog.query.filter(ErrorLog.monitor_log_id == log.id).first()
            result.append({
                'server': log.server,
                'status': log.status,
                'error': error_log.msg if error_log else None
            })

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
