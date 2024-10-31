from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jst = pytz.timezone('Asia/Tokyo')

class MonitorLog(db.Model):
    __tablename__ = 'monitor_logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String, nullable=False)
    cpu = db.Column(db.Integer, nullable=True)
    gpu = db.Column(db.Integer, nullable=True)
    cpu_memory = db.Column(db.Integer, nullable=True)
    gpu_memory = db.Column(db.Integer, nullable=True)
    gpu_name = db.Column(db.String, nullable=True)

    server = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(jst))

    error_logs = db.relationship('ErrorLog', back_populates='monitor_log')

class ErrorLog(db.Model):
    __tablename__ = 'error_logs'

    id = db.Column(db.Integer, primary_key=True)
    monitor_log_id = db.Column(db.Integer, db.ForeignKey('monitor_logs.id'))
    msg = db.Column(db.String, nullable=False)

    monitor_log = db.relationship('MonitorLog', back_populates='error_logs')




@app.route('/')
def index():
    return render_template('index.html')

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
            server=data['server'],
            gpu_name=data['gpu_name'],
            timestamp=datetime.now(jst)
        )
        db.session.add(new_log)
    elif data['status'] == 'failed':
        new_log = MonitorLog(
            status=data['status'],
            cpu=None,
            gpu=None,
            cpu_memory=None,
            gpu_memory=None,
            gpu_name=None,
            server=data['server'],
            timestamp=datetime.now(jst)
        )

        db.session.add(new_log)
        db.session.flush()

        error_log = ErrorLog(
            monitor_log=new_log,
            msg=data['error']
        )
        db.session.add(error_log)

    
    db.session.commit()

    return jsonify({'message': 'Log added successfully'}), 201

@app.route('/log', methods=['GET'])
def get_logs():
    one_hour_ago = datetime.now(jst) - timedelta(hours=1)
    #dbのserverのユニークな値を取得
    servers = db.session.query(MonitorLog.server).distinct().all()
    #logsに各サーバーの最新のログを格納
    logs = []
    for server in servers:
        log = MonitorLog.query.filter(MonitorLog.server == server[0]).filter(MonitorLog.timestamp >= one_hour_ago).order_by(MonitorLog.timestamp.desc()).first()
        if log:
            logs.append(log)

    result = {}

    for log in logs:


        if log.status == 'success':
            result[log.server] = {
                'cpu_usage': str(log.cpu),
                'gpu_usage': str(log.gpu),
                'gpu_memory_usage': str(log.gpu_memory),
                'memory_usage': str(log.cpu_memory),
                'status': log.status,
                'gpu_name': log.gpu_name,
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        elif log.status == 'failed':
            error_log = ErrorLog.query.filter(ErrorLog.monitor_log_id == log.id).first()
            print(error_log.msg)
            result[log.server]={
                'status': log.status,
                'gpu_name': log.gpu_name,
                'error': error_log.msg if error_log else None,
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }



    response = app.response_class(
        response=json.dumps(result, ensure_ascii=False),
        mimetype='application/json'
    )

    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
    # with app.app_context():
    #     db.create_all()