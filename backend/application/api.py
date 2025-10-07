from flask_restful import Resource, Api
api = Api()
from .models import Parking_lot,db
from flask_security import auth_required,roles_required


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

    

api.add_resource(Parking_lot_API, '/api/parking-lots')
