from exceptions.api_error import ApiError
from flask import jsonify

def error_middleware(err, req, res, next):
    print(err)
    if isinstance(err, ApiError):
        return jsonify({'message': err.message, 'errors': err.errors}), err.status
    return jsonify({'message': 'Непредвиденная ошибка'}), 500
