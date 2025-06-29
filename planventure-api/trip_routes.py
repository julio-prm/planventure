from flask import Blueprint, request, jsonify
from app import db
from models.trip import Trip
from auth_middleware import token_required
from datetime import datetime, timedelta

trip_bp = Blueprint('trip', __name__, url_prefix='/trips')

@trip_bp.route('/', methods=['POST'])
@token_required
def create_trip():
    data = request.get_json()
    destination = data.get('destination')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    itinerary = data.get('itinerary')
    user_id = getattr(request, 'user', {}).get('user_id')

    if not destination or not start_date or not end_date:
        return jsonify({'error': 'destination, start_date, and end_date are required.'}), 400
    if not user_id:
        return jsonify({'error': 'User authentication failed.'}), 401

    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    except Exception:
        return jsonify({'error': 'start_date and end_date must be in YYYY-MM-DD format.'}), 400

    if not itinerary:
        itinerary = generate_default_itinerary(destination, start_date_obj, end_date_obj)

    trip = Trip(
        user_id=user_id,
        destination=destination,
        start_date=start_date_obj,
        end_date=end_date_obj,
        latitude=latitude,
        longitude=longitude,
        itinerary=itinerary
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify({'message': 'Trip created successfully.', 'trip': trip.to_dict()}), 201

@trip_bp.route('/', methods=['GET'])
@token_required
def get_trips():
    trips = Trip.query.all()
    return jsonify({'trips': [trip.to_dict() for trip in trips]}), 200

@trip_bp.route('/<int:trip_id>', methods=['GET'])
@token_required
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404
    return jsonify({'trip': trip.to_dict()}), 200

@trip_bp.route('/<int:trip_id>', methods=['PUT'])
@token_required
def update_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404
    data = request.get_json()
    trip.name = data.get('name', trip.name)
    trip.description = data.get('description', trip.description)
    db.session.commit()
    return jsonify({'message': 'Trip updated successfully.', 'trip': trip.to_dict()}), 200

@trip_bp.route('/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({'error': 'Trip not found.'}), 404
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'message': 'Trip deleted successfully.'}), 200

def generate_default_itinerary(destination, start_date, end_date):
    """
    Generate a default itinerary template for a trip.
    :param destination: The trip destination
    :param start_date: Start date as a date object
    :param end_date: End date as a date object
    :return: String itinerary template
    """
    days = (end_date - start_date).days + 1
    itinerary_lines = [f"Day {i+1}: [Add your plans for {destination} here]" for i in range(days)]
    return "\n".join(itinerary_lines)
