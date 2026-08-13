from flask import jsonify


def success_response(data=None, message=None, status=200):
    payload = {'success': True}
    if message:
        payload['message'] = message
    if data is not None:
        payload['data'] = data
    return jsonify(payload), status


def error_response(message, status=400, errors=None):
    payload = {'success': False, 'error': message}
    if errors:
        payload['errors'] = errors
    return jsonify(payload), status
