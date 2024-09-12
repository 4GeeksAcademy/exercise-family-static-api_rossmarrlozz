"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    jackson_family.add_member(new_member)
    return jsonify({"done": True}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    eliminar_familiar = jackson_family.delete_member(member_id)
    if not eliminar_familiar:
        return jsonify({"mensaje": "Familiar no encontrado"}),400
    return jsonify({"done": True}), 200

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    updated_member = request.json
    result = jackson_family.update_member(member_id, updated_member)
    if not result:
        return jsonify({"mensaje":"No se encontro al miembro"}), 400
    return jsonify({"done": True}), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    miembro_econtrado = jackson_family.get_member(member_id)
    if not miembro_econtrado:
        return jsonify({"mensaje": "No se encontro al miembro"}), 400
    return jsonify(miembro_econtrado),200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
