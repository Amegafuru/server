from flask import Blueprint
from controllers.user_controller import UserController
from flask import request
from flask_validator import ValidateEmail
from middlewares.auth_middleware import authMiddleware

# Создаем Blueprint для маршрутов
router = Blueprint('router', __name__)

# Создаем экземпляр UserController
user_controller = UserController()

# Проверка параметров с использованием flask_validator для email
#validate_email = ValidateEmail(field='email')

# Роуты
@router.route('/registration', methods=['POST'])
#@validate_email.params('email', 'password')
def registration_route():
    return user_controller.registration(request)

@router.route('/login', methods=['POST'])
def login_route():
    return user_controller.login(request)

@router.route('/logout', methods=['POST'])
def logout_route():
    return user_controller.logout(request)

@router.route('/activate/<link>', methods=['GET'])
def activate_route(link):
    return user_controller.activate(link)

@router.route('/refresh', methods=['GET'])
def refresh_route():
    return user_controller.refresh(request)

@router.route('/users', methods=['GET'])
@authMiddleware
def getUsers_route():
    return user_controller.getUsers(request)

# Другие роуты...