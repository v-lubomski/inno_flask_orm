"""Views."""

from flask import request, Response
import json
import app.controllers as ctrl
from app import app
from app.utilities import json_validate
from app.schemes import DRIVERS_SCHEMA, ORDERS_SCHEMA, CLIENTS_SCHEMA


@app.route('/drivers/<int:driver_id>', methods=['GET', 'DELETE'])
@app.route('/drivers', methods=['POST'])
def drivers(driver_id: int = None) -> Response:
    """Driver handler."""
    if request.method == "POST":
        req = request.get_json()
        if json_validate(json=req, schema=DRIVERS_SCHEMA):
            result = ctrl.create_driver(name=req['name'], car=req['car'])
            if result:
                json_result = json.dumps(result, ensure_ascii=False)
                return Response(status='201 Created', response=json_result)
            else:
                return Response(status='200', response="Driver already exists")
        else:
            return Response(status='400 Wrong request')

    if request.method == "GET":
        result = ctrl.find_driver(driver_id)
        if result:
            json_result = json.dumps(result, ensure_ascii=False)
            return Response(status='200 Successful operation', response=json_result)
        else:
            return Response(status='404 Object was not found in the database')

    if request.method == "DELETE":
        result = ctrl.delete_driver(driver_id)
        if result:
            json_result = json.dumps(result, ensure_ascii=False)
            return Response(status='200 Deleted', response=json_result)
        else:
            return Response(status='404 Object was not found in the database')


@app.route('/clients/<int:client_id>', methods=['GET', 'DELETE'])
@app.route('/clients', methods=['POST'])
def clients(client_id: id = None) -> Response:
    """Client handler."""
    if request.method == "POST":
        req = request.get_json()
        if json_validate(json=req, schema=CLIENTS_SCHEMA):
            result = ctrl.create_client(name=req['name'], is_vip=req['is_vip'])
            if result:
                json_result = json.dumps(result, ensure_ascii=False)
                return Response(status='201 Created', response=json_result)
            else:
                return Response(status='200 Client already exists')
        else:
            return Response(status='400 Wrong request')

    if request.method == "GET":
        result = ctrl.find_client(client_id)
        if result:
            json_result = json.dumps(result, ensure_ascii=False)
            return Response(status='200 Successful operation', response=json_result)
        else:
            return Response(status='404 Object was not found in the database')

    if request.method == "DELETE":
        result = ctrl.delete_client(client_id)
        if result:
            json_result = json.dumps(result, ensure_ascii=False)
            return Response(status='204', response=json_result)
        else:
            return Response(status='404 Object was not found in the database')


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT'])
@app.route('/orders', methods=['POST'])
def orders(order_id: int = None) -> Response:
    """Order handler."""
    if request.method == "POST":
        req = request.get_json()
        if json_validate(json=req, schema=ORDERS_SCHEMA):
            result = ctrl.create_order(client_id=req['client_id'],
                                       driver_id=req['driver_id'],
                                       date_created=req['date_created'],
                                       status=req['status'],
                                       address_from=req['address_from'],
                                       address_to=req['address_to'])
            json_result = json.dumps(result, ensure_ascii=False)
            return Response(status='201 Created', response=json_result)
        else:
            return Response(status='400 Wrong request')

    if request.method == "GET":
        result = ctrl.find_order(order_id)
        if result:
            json_result = json.dumps(result, ensure_ascii=False)
            return Response(status='200 Successful operation', response=json_result)
        else:
            return Response(status='404 Object was not found in the database')

    if request.method == "PUT":
        req = request.get_json()
        if json_validate(json=req, schema=ORDERS_SCHEMA):
            result = ctrl.edit_order(order_id=order_id, client_id=req['client_id'],
                                     driver_id=req['driver_id'],
                                     date_created=req['date_created'],
                                     status=req['status'],
                                     address_from=req['address_from'],
                                     address_to=req['address_to'])
            return result
        else:
            return Response(status='400 Wrong request')
