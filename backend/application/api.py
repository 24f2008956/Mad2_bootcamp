from flask_restful import Resource, Api
api = Api()
from .models import Parking_lot,db
from flask_security import auth_required,roles_required
from flask import request
import datetime


class Parking_lot_API(Resource):
    @auth_required('token')
    def get(self):
        lots = Parking_lot.query.all()
        response = []
        
        for lot in lots:
            response.append({
                "id": lot.id,
                "name": lot.name,
                "address": lot.address,
                "pincode": lot.pincode,
                "price_per_hour": lot.price_per_hour,
                "max_no_spots": lot.max_no_spots,
                "created_at": lot.created_at.isoformat()
            })

        return response, 200
    
    
 
    @auth_required('token')
    def post(self):
        data = request.get_json()

        required_fields = ['name', 'address', 'pincode', 'price_per_hour', 'max_no_spots']
        if not all(field in data for field in required_fields):
            return {"message": "Missing fields in request"}, 400

        existing_lot = Parking_lot.query.filter_by(name=data['name']).first()
        if existing_lot:
            return {"message": "Parking lot with this name already exists"}, 409

        try:
            new_lot = Parking_lot(
                name=data['name'],
                address=data['address'],
                pincode=data['pincode'],
                price_per_hour=data['price_per_hour'],
                max_no_spots=data['max_no_spots'],
                created_at=datetime.datetime.utcnow()
            )

            db.session.add(new_lot)
            db.session.commit()
            return {"message": "Parking lot created successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error occurred: {str(e)}"}, 500


    @auth_required('token')
    def put(self):
        data = request.get_json()

        # ID is required to identify which parking lot to update
        lot_id = request.args.get('id')
        if not lot_id:
            return {"message": "Missing parking lot ID in query parameters"}, 400

        lot = Parking_lot.query.get(lot_id)
        if not lot:
            return {"message": "Parking lot not found"}, 404

        try:
            # Update fields if provided
            if 'name' in data:
                # Check for duplicate name if changing
                existing_lot = Parking_lot.query.filter_by(name=data['name']).first()
                if existing_lot and existing_lot.id != lot.id:
                    return {"message": "Another parking lot with this name already exists"}, 409
                lot.name = data['name']

            if 'address' in data:
                lot.address = data['address']
            if 'pincode' in data:
                lot.pincode = data['pincode']
            if 'price_per_hour' in data:
                lot.price_per_hour = data['price_per_hour']
            if 'max_no_spots' in data:
                lot.max_no_spots = data['max_no_spots']

            db.session.commit()
            return {"message": "Parking lot updated successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"message": f"Error occurred: {str(e)}"}, 500

    @auth_required('token')
    def delete(self):
        lot_id = request.args.get('id')

        if not lot_id:
            return {"message": "Missing parking lot ID"}, 400

        lot = Parking_lot.query.get(lot_id)
        if not lot:
            return {"message": "Parking lot not found"}, 404

        try:
            db.session.delete(lot)
            db.session.commit()
            return {"message": "Parking lot deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error occurred: {str(e)}"}, 500
from flask_restful import Resource, reqparse
from flask import request
from flask_security import auth_required
from models import Parking_spot, Parking_lot, db

class Parking_Spot_API(Resource):
    
    @auth_required('token')
    def get(self):
        lot_id = request.args.get('lot_id')
        if not lot_id:
            return {"message": "Missing 'lot_id' parameter"}, 400
        
        spots = Parking_spot.query.filter_by(lot_id=lot_id).all()
        response = []

        for spot in spots:
            response.append({
                "id": spot.id,
                "lot_id": spot.lot_id,
                "number": spot.number,
                "is_available": spot.is_available
            })

        return response, 200

    @auth_required('token')
    def post(self):
        data = request.get_json()
        required_fields = ['lot_id', 'number']
        
        if not all(field in data for field in required_fields):
            return {"message": "Missing fields"}, 400

        # Check if lot exists
        lot = Parking_lot.query.get(data['lot_id'])
        if not lot:
            return {"message": "Parking lot not found"}, 404

        # Check for duplicate spot number in the same lot
        existing = Parking_spot.query.filter_by(lot_id=data['lot_id'], number=data['number']).first()
        if existing:
            return {"message": "Spot number already exists in this lot"}, 409

        new_spot = Parking_spot(
            lot_id=data['lot_id'],
            number=data['number'],
            is_available=data.get('is_available', True)
        )

        try:
            db.session.add(new_spot)
            db.session.commit()
            return {"message": "Parking spot created successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error occurred: {str(e)}"}, 500

    @auth_required('token')
    def put(self):
        spot_id = request.args.get('id')
        if not spot_id:
            return {"message": "Missing 'id' parameter"}, 400

        spot = Parking_spot.query.get(spot_id)
        if not spot:
            return {"message": "Parking spot not found"}, 404

        data = request.get_json()

        if 'number' in data:
            # Check for duplicate number
            duplicate = Parking_spot.query.filter_by(lot_id=spot.lot_id, number=data['number']).first()
            if duplicate and duplicate.id != spot.id:
                return {"message": "Duplicate spot number in the same lot"}, 409
            spot.number = data['number']

        if 'is_available' in data:
            spot.is_available = data['is_available']

        try:
            db.session.commit()
            return {"message": "Parking spot updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error occurred: {str(e)}"}, 500

    @auth_required('token')
    def delete(self):
        spot_id = request.args.get('id')
        if not spot_id:
            return {"message": "Missing 'id' parameter"}, 400

        spot = Parking_spot.query.get(spot_id)
        if not spot:
            return {"message": "Parking spot not found"}, 404

        try:
            db.session.delete(spot)
            db.session.commit()
            return {"message": "Parking spot deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error occurred: {str(e)}"}, 500
        


class Bookings_API(Resource):

    @auth_required('token')
    def get(self):
        if current_user.has_role('admin'):
            bookings = Booking.query.all()
        else:
            bookings = Booking.query.filter_by(user_id=current_user.id).all()

        response = []
        for b in bookings:
            response.append({
                "id": b.id,
                "user_id": b.user_id,
                "vehicle_number": b.vehicle_number,
                "parking_lot_id": b.parking_lot_id,
                "parking_spot_id": b.parking_spot_id,
                "spot_number": b.parking_spot.spot_number if b.parking_spot else None,
                "in_time": b.in_time.isoformat(),
                "out_time": b.out_time.isoformat() if b.out_time else None,
                "cost": b.cost
            })
        return response, 200

    @auth_required('token')
    def post(self):
        data = request.get_json()
        required = ['parking_lot_id', 'parking_spot_id', 'vehicle_number']
        if not all(field in data for field in required):
            return {"message": "Missing required fields"}, 400

        spot = Parking_spot.query.get(data['parking_spot_id'])

        # Validate spot
        if not spot:
            return {"message": "Parking spot not found"}, 404
        if spot.status == 'O':
            return {"message": "Spot is already occupied"}, 409
        if spot.parking_lot_id != data['parking_lot_id']:
            return {"message": "Spot does not belong to the selected lot"}, 400

        # Create booking
        booking = Booking(
            user_id=current_user.id,
            parking_lot_id=data['parking_lot_id'],
            parking_spot_id=data['parking_spot_id'],
            vehicle_number=data['vehicle_number'],
            in_time=datetime.now(pytz.timezone('Asia/Kolkata'))
        )

        # Mark spot as occupied
        spot.status = 'O'
        spot.user_id = current_user.id

        try:
            db.session.add(booking)
            db.session.commit()
            return {"message": "Booking created successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error: {str(e)}"}, 500

    @auth_required('token')
    def put(self):
        booking_id = request.args.get('id')
        if not booking_id:
            return {"message": "Missing booking ID"}, 400

        booking = Booking.query.get(booking_id)
        if not booking:
            return {"message": "Booking not found"}, 404

        if booking.out_time:
            return {"message": "Booking already completed"}, 409

        try:
            booking.out_time = datetime.now(pytz.timezone('Asia/Kolkata'))

            duration_hours = (booking.out_time - booking.in_time).total_seconds() / 3600
            price_per_hour = booking.parking_lot.price_per_hour if booking.parking_lot else 0
            booking.cost = round(duration_hours * price_per_hour, 2)

            # Free the spot
            spot = Parking_spot.query.get(booking.parking_spot_id)
            if spot:
                spot.status = 'A'
                spot.user_id = None

            db.session.commit()
            return {"message": "Booking completed", "cost": booking.cost}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating booking: {str(e)}"}, 500

    @auth_required('token')
    def delete(self):
        booking_id = request.args.get('id')
        if not booking_id:
            return {"message": "Missing booking ID"}, 400

        booking = Booking.query.get(booking_id)
        if not booking:
            return {"message": "Booking not found"}, 404

        try:
            # Optionally free the spot
            spot = Parking_spot.query.get(booking.parking_spot_id)
            if spot and spot.status == 'O':
                spot.status = 'A'
                spot.user_id = None

            db.session.delete(booking)
            db.session.commit()
            return {"message": "Booking deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error deleting booking: {str(e)}"}, 500

    
    

api.add_resource(Parking_lot_API, '/api/Parking_lots')
api.add_resource(Parking_Spot_API, '/api/parking_spots')
api.add_resource(Bookings_API, '/api/bookings')

