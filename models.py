from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class MonitorLog(Base):
    __tablename__ = 'monitor_logs'

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    cpu = Column(Integer, nullable=True)
    gpu = Column(Integer, nullable=True)
    cpu_memory = Column(Integer, nullable=True)
    gpu_memory = Column(Integer, nullable=True)
    server = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    error_logs = relationship('ErrorLog', back_populates='monitor_log')

class ErrorLog(Base):
    __tablename__ = 'error_logs'

    id = Column(Integer, primary_key=True)
    monitor_log_id = Column(Integer, ForeignKey('monitor_logs.id'))
    msg = Column(String, nullable=False)

    monitor_log = relationship('MonitorLog', back_populates='error_logs')
