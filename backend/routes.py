from . import app
import os
import json
from flask import jsonify, Blueprint, request, make_response, abort, url_for  # noqa; F401

api = Blueprint('api', __name__, url_prefix='/api')
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return jsonify(picture), 200
    # If no match found
    return jsonify({'message': 'Picture not found'}), 404  

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    # Check for duplicates
    for picture in data:
        if picture['id'] == new_picture['id']:
            return jsonify({'Message': f"picture with id {new_picture['id']} already present"}), 302
    # Add to list and return success
    data.append(new_picture) 
    return jsonify(new_picture), 201  # 201 CREATED

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Find the picture
    for i, picture in enumerate(data):  # Using enumerate for index
        if picture['id'] == id:
            data[i] = request.get_json()  # Update
            return jsonify(data[i]), 200 # Success
    # Picture not found
    return jsonify({'message': 'Picture not found'}), 404 

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i, picture in enumerate(data):
        if picture['id'] == id:
            del data[i]  # Remove from the list
            return '', 204  # 204 No Content
    # Picture not found
    return jsonify({'message': 'Picture not found'}), 404