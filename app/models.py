from .database import db
from datetime import datetime

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_time = db.Column(db.DateTime, nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    serviced = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Asset {self.name}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'service' or 'expiration'
    time = db.Column(db.DateTime, default=datetime.utcnow)

    asset = db.relationship('Asset', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification for Asset {self.asset_id}>'

class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'service' or 'expiration'
    time = db.Column(db.DateTime, default=datetime.utcnow)

    asset = db.relationship('Asset', backref=db.backref('violations', lazy=True))

    def __repr__(self):
        return f'<Violation for Asset {self.asset_id}>'
