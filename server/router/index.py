from flask import Blueprint
from controllers.user_controller import registration, login, logout, activate, refresh, getUsers
from flask import request
from flask_validator import ValidateParams
from middlewares.authMiddleware import authMiddleware

# Создаем Blueprint для маршрутов
router = Blueprint('router', __name__)

# Проверка параметров с использованием flask_validator
validate = ValidateParams()

# Роуты
@router.route('/registration', methods=['POST'])
@validate.params('email', 'password')
def registration_route():
    return registration(request)

@router.route('/login', methods=['POST'])
def login_route():
    return login(request)

@router.route('/logout', methods=['POST'])
def logout_route():
    return logout(request)

@router.route('/activate/<link>', methods=['GET'])
def activate_route(link):
    return activate(link)

@router.route('/refresh', methods=['GET'])
def refresh_route():
    return refresh(request)

@router.route('/users', methods=['GET'])
@authMiddleware
def getUsers_route():
    return getUsers(request)

# Другие роуты...