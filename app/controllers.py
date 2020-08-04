"""Controllers."""

from app.models import Driver, Client, Order
from app import session
from datetime import datetime
import json
from flask import Response


def create_driver(name: str, car: str) -> (bool, dict):
    """Driver creator."""
    driver = session.query(Driver).filter_by(name=name).first()
    if not driver:
        driver = Driver(name, car)
        session.add(driver)
        session.commit()
        response_dict = {
            'id': driver.id,
            'name': driver.name,
            'car': driver.car
        }
        session.close()
        return response_dict
    return False


def find_driver(driver_id: int) -> (bool, dict):
    """Driver finder."""
    driver = session.query(Driver).filter_by(id=driver_id).first()
    if driver:
        response_dict = {
            'id': driver.id,
            'name': driver.name,
            'car': driver.car
        }
        session.close()
        return response_dict
    else:
        session.close()
        return False


def delete_driver(driver_id: int) -> (bool, dict):
    """Driver deleter."""
    driver = session.query(Driver).filter_by(id=driver_id).first()
    if driver:
        response_dict = {
            'id': driver.id,
            'name': driver.name,
            'car': driver.car
        }
        session.delete(driver)
        session.commit()
        session.close()
        return response_dict
    else:
        session.close()
        return False


def create_client(name: str, is_vip: str) -> (bool, dict):
    """Client creator."""
    client = session.query(Client).filter_by(name=name).first()
    if not client:
        client = Client(name, is_vip)
        session.add(client)
        session.commit()
        response_dict = {
            'id': client.id,
            'name': client.name,
            'is_vip': client.is_vip
        }
        session.close()
        return response_dict
    return False


def find_client(client_id: int) -> (bool, dict):
    """Client finder."""
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        response_dict = {
            'id': client.id,
            'name': client.name,
            'is_vip': client.is_vip
        }
        session.close()
        return response_dict
    else:
        session.close()
        return False


def delete_client(client_id: int) -> (bool, dict):
    """Client deleter."""
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        response_dict = {
            'id': client.id,
            'name': client.name,
            'is_vip': client.is_vip
        }
        session.delete(client)
        session.commit()
        session.close()
        return response_dict
    else:
        session.close()
        return False


def create_order(client_id: int, driver_id: int, date_created: datetime, status: str,
                 address_from: str,
                 address_to: str) -> dict:
    """Order creator."""
    date_created = datetime.strptime(date_created, '%Y-%m-%dT%H:%M:%S.%fZ')
    order = Order(client_id=client_id, driver_id=driver_id, address_from=address_from,
                  address_to=address_to, date_created=date_created,
                  status=status)
    session.add(order)
    session.commit()
    response_dict = {
        'id': order.id,
        'client_id': order.client_id,
        'driver_id': order.driver_id,
        'date_created': datetime.strftime(order.date_created, '%Y-%m-%dT%H:%M:%S.%fZ'),
        'status': order.status,
        'address_from': order.address_from,
        'address_to': order.address_to
    }
    session.close()
    return response_dict


def find_order(order_id: int) -> (bool, dict):
    """Order finder."""
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        response_dict = {
            'id': order.id,
            'client_id': order.client_id,
            'driver_id': order.driver_id,
            'date_created': datetime.strftime(order.date_created,
                                              '%Y-%m-%dT%H:%M:%S.%fZ'),
            'status': order.status,
            'address_from': order.address_from,
            'address_to': order.address_to
        }
        session.close()
        return response_dict
    else:
        session.close()
        return False


def edit_order(order_id: int, client_id: int, driver_id: int, date_created: datetime,
               status: str,
               address_from: str,
               address_to: str) -> Response:
    """Order editor."""
    order = session.query(Order).filter_by(id=order_id).first()

    if order:
        date_created = datetime.strptime(date_created, '%Y-%m-%dT%H:%M:%S.%fZ')
        dict_to_bd = {
            'id': order_id,
            'client_id': client_id,
            'driver_id': driver_id,
            'date_created': date_created,
            'status': status,
            'address_from': address_from,
            'address_to': address_to
        }

        if order.status == 'not_accepted' or (
                order.driver_id == driver_id and order.client_id == client_id):
            if (order.status == status) or (order.status == 'not_accepted' and (
                    status == 'in_progress' or status == 'cancelled')) or (
                    order.status == 'in_progress' and (
                    status == 'done' or status == 'cancelled')):
                order.driver_id = driver_id
                order.client_id = client_id
                order.status = status

                session.query(Order).filter_by(id=order_id).update(dict_to_bd)
                session.commit()

                response_dict = {
                    'id': order.id,
                    'client_id': order.client_id,
                    'driver_id': order.driver_id,
                    'date_created': datetime.strftime(order.date_created,
                                                      '%Y-%m-%dT%H:%M:%S.%fZ'),
                    'status': order.status,
                    'address_from': order.address_from,
                    'address_to': order.address_to
                }

                json_response = json.dumps(response_dict, ensure_ascii=False)
                session.close()
                return Response(status='200 Edited', response=json_response)
            else:
                return Response(status='405 Not allowed')
        else:
            session.close()
            return Response(status='405 Not allowed')
    else:
        session.close()
        return Response(status='404 Not found')
