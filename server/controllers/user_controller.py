from flask import request, jsonify, redirect, make_response
from exceptions.api_error import ApiError
from service.user_service import UserService
from wtforms import Form, StringField, PasswordField, validators
import os

# Создаем экземпляр сервиса пользователя
userService = UserService()

# Создаем форму для регистрации пользователя
class RegistrationForm(Form):
    email = StringField('Email', [validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])

class UserController:
    def registration(self):
        try:
            # Валидация данных из запроса
            form = RegistrationForm(request.form)
            if form.validate():
                email = form.email.data
                password = form.password.data
                
                # Вызываем метод регистрации из сервиса пользователя
                userData = userService.registration(email, password)
                
                # Формируем ответ с данными пользователя и устанавливаем куку refreshToken
                response = make_response(jsonify(userData), 200)
                response.set_cookie('refreshToken', userData['refreshToken'], max_age=30 * 24 * 60 * 60, httponly=True)
                return response
            else:
                raise ApiError.BadRequest('Ошибка при валидации', form.errors)
        except Exception as e:
            raise ApiError(e)

    # Метод для входа пользователя
    def login(self):
        try:
            # Получаем email и password из запроса
            email = request.json.get('email')
            password = request.json.get('password')
            
            # Вызываем метод логина из сервиса пользователя
            userData = userService.login(email, password)
            
            # Формируем ответ с данными пользователя и устанавливаем куку refreshToken
            response = make_response(jsonify(userData), 200)
            response.set_cookie('refreshToken', userData['refreshToken'], max_age=30 * 24 * 60 * 60, httponly=True)
            return response
        except Exception as e:
            raise ApiError(e)

    # Метод для выхода пользователя
    def logout(self):
        try:
            # Получаем refreshToken из куки запроса
            refreshToken = request.cookies.get('refreshToken')
            
            # Вызываем метод логаута из сервиса пользователя
            token = userService.logout(refreshToken)
            
            # Формируем ответ и удаляем куку refreshToken
            response = make_response(jsonify(token), 200)
            response.delete_cookie('refreshToken')
            return response
        except Exception as e:
            raise ApiError(e)

    # Метод для активации аккаунта
    def activate(self, link):
        try:
            # Получаем activationLink из запроса и активируем аккаунт
            userService.activate(link)
            
            # Редиректим на клиентскую страницу
            return redirect(os.getenv.CLIENT_URL)
        except Exception as e:
            raise ApiError(e)

    # Метод для обновления токена
    def refresh(self):
        try:
            # Получаем refreshToken из куки запроса
            refreshToken = request.cookies.get('refreshToken')
            
            # Вызываем метод обновления токена из сервиса пользователя
            userData = userService.refresh(refreshToken)
            
            # Формируем ответ с обновленными данными пользователя и устанавливаем куку refreshToken
            response = make_response(jsonify(userData), 200)
            response.set_cookie('refreshToken', userData['refreshToken'], max_age=30 * 24 * 60 * 60, httponly=True)
            return response
        except Exception as e:
            raise ApiError(e)

    # Метод для получения всех пользователей
    def get_users(self):
        try:
            # Вызываем метод получения всех пользователей из сервиса пользователя
            users = userService.get_all_users()
            
            # Возвращаем JSON со всеми пользователями
            return jsonify(users)
        except Exception as e:
            raise ApiError(e)
