from flask import Blueprint, request, jsonify
from .models import Asset
from .database import db
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "Asset Reminder API is running!"})

# ✅ Create a new asset
@bp.route('/assets', methods=['POST'])
def create_asset():
    data = request.get_json()
    print("Received data:", data)  # 👈 Add this line

    try:
        name = data['name']
        service_time = datetime.fromisoformat(data['service_time'])
        expiration_time = datetime.fromisoformat(data['expiration_time'])

        asset = Asset(
            name=name,
            service_time=service_time,
            expiration_time=expiration_time
        )
        db.session.add(asset)
        db.session.commit()

        return jsonify({"message": "Asset created", "id": asset.id}), 201

    except Exception as e:
        print("Error:", e)  # 👈 Print error in terminal
        return jsonify({"error": str(e)}), 400

# ✅ Get all assets
@bp.route('/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    print("assets",assets)
    result = []
    for asset in assets:
        result.append({
            "id": asset.id,
            "name": asset.name,
            "service_time": asset.service_time.isoformat(),
            "expiration_time": asset.expiration_time.isoformat(),
            "serviced": asset.serviced
        })
    return jsonify(result)

# ✅ Mark an asset as serviced
@bp.route('/assets/<int:id>', methods=['PUT'])
def mark_serviced(id):
    asset = Asset.query.get(id)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    asset.serviced = True
    db.session.commit()
    return jsonify({"message": "Asset marked as serviced"})

# (Optional) Get a single asset
@bp.route('/assets/<int:id>', methods=['GET'])
def get_asset(id):
    asset = Asset.query.get(id)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    return jsonify({
        "id": asset.id,
        "name": asset.name,
        "service_time": asset.service_time.isoformat(),
        "expiration_time": asset.expiration_time.isoformat(),
        "serviced": asset.serviced
    })

from .models import Notification, Violation
from datetime import datetime, timedelta

@bp.route('/run-checks', methods=['GET', 'POST'])
def run_checks():
    now = datetime.utcnow()
    in_15_minutes = now + timedelta(minutes=15)

    assets = Asset.query.all()
    notifications_created = 0
    violations_created = 0

    for asset in assets:
        # 🚨 Notification: Upcoming service
        if now <= asset.service_time <= in_15_minutes:
            already_notified = Notification.query.filter_by(asset_id=asset.id, type='service').first()
            if not already_notified:
                n = Notification(asset_id=asset.id, type='service')
                db.session.add(n)
                notifications_created += 1

        # 🚨 Notification: Upcoming expiration
        if now <= asset.expiration_time <= in_15_minutes:
            already_notified = Notification.query.filter_by(asset_id=asset.id, type='expiration').first()
            if not already_notified:
                n = Notification(asset_id=asset.id, type='expiration')
                db.session.add(n)
                notifications_created += 1

        # ❌ Violation: Missed service
        if now > asset.service_time and not asset.serviced:
            already_violated = Violation.query.filter_by(asset_id=asset.id, type='service').first()
            if not already_violated:
                v = Violation(asset_id=asset.id, type='service')
                db.session.add(v)
                violations_created += 1

        # ❌ Violation: Asset expired
        if now > asset.expiration_time:
            already_violated = Violation.query.filter_by(asset_id=asset.id, type='expiration').first()
            if not already_violated:
                v = Violation(asset_id=asset.id, type='expiration')
                db.session.add(v)
                violations_created += 1

    db.session.commit()

    return jsonify({
        "message": "Checks complete",
        "notifications_created": notifications_created,
        "violations_created": violations_created
    })

# ✅ Get all Notifications
@bp.route('/notifications', methods=['GET'])
def get_notifications():
    from .models import Notification

    notifications = Notification.query.all()
    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "asset_id": n.asset_id,
            "type": n.type,
            "time": n.time.isoformat()
        })
    return jsonify(result)


# ✅ Get all Violations
@bp.route('/violations', methods=['GET'])
def get_violations():
    from .models import Violation

    violations = Violation.query.all()
    result = []
    for v in violations:
        result.append({
            "id": v.id,
            "asset_id": v.asset_id,
            "type": v.type,
            "time": v.time.isoformat()
        })
    return jsonify(result)
