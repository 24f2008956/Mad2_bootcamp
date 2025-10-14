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

    
    

api.add_resource(Parking_lot_API, '/api/parking_lots')

