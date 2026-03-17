from flask import Flask, jsonify, request
from flask_cors import CORS
from APIDatabase import *

appFlask = Flask(__name__)
CORS(appFlask)


@appFlask.errorhandler(400)
def handle_400(error):
    return jsonify({"error": "Bad Request"}), 400


"""
GET
"""


@appFlask.route("/clients", methods=["GET"])
def get_clients_flask_api():
    id_param = request.args.get("id", type=int)
    name_param = request.args.get("name", type=str)

    if id_param is not None:
        return jsonify(get_client_id(id_param))
    if name_param is not None:
        return jsonify(get_client_name(name_param))
    return jsonify(get_clients())


"""
POST
"""


@appFlask.route("/clients", methods=["POST"])
def post_clients_flask_api():
    client_data = request.json
    insert_client(client_data)
    return jsonify({"message" : "Client created"})


"""
PUT
"""


@appFlask.route("/clients", methods=["PUT"])
def put_clients_flask_api():
    client_data = request.json
    id_param = request.args.get("id", type=int)

    if id_param is not None:
        update_client(id_param, client_data)
        return jsonify({"message" : "Client updated"})
    insert_client(client_data)
    return jsonify({"message" : "Client added"})


"""
DELETE
"""


@appFlask.route("/clients", methods=["DELETE"])
def delete_clients_flask_api():
    id_param = request.args.get("id", type=int)
    if id_param is None:
        return jsonify({"message" : "Client ID not found"}), 400
    delete_client(id_param)
    return jsonify({"message" : "Client deleted"})


if __name__ == "__main__":
    appFlask.run(debug=True, port=8002)
