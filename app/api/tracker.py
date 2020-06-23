from flask import Blueprint, request
from flask_restx import Api, Resource

from app.api.models import Package

tracker_blueprint = Blueprint("tracker", __name__)
api = Api(tracker_blueprint)


class Tracker(Resource):
    def post(self):
        post_data = request.get_json()
        tracking_code = post_data.get("tracking_code")
        package = Package.query.filter_by(tracking_code=tracking_code).first()
        response_object = {}
        response_object = {"status": package.status}
        return response_object, 200


api.add_resource(Tracker, "/track")
