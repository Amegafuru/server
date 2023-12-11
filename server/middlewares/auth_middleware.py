from flask import request, jsonify
from exceptions.api_error import ApiError
from service.token_service import tokenService

def authMiddleware(request, response, next):
    try:
        authorizationHeader = request.headers.get('Authorization')

        if not authorizationHeader:
            return ApiError().UnauthorizedError()  # Возвращаем ошибку "Unauthorized" в случае отсутствия заголовка авторизации

        accessToken = authorizationHeader.split()[1] if ' ' in authorizationHeader else None

        if not accessToken:
            return ApiError().UnauthorizedError()  # Возвращаем ошибку "Unauthorized" если отсутствует токен доступа

        userData = tokenService.validateAccessToken(accessToken)

        if not userData:
            return ApiError().UnauthorizedError()  # Возвращаем ошибку "Unauthorized" если токен недействителен или отсутствуют данные пользователя

        # Добавление данных пользователя в объект request для использования в последующих обработчиках
        request.user = userData
        next()

    except Exception as e:
        return ApiError().UnauthorizedError()  # Обработка других исключений с возвратом ошибки "Unauthorized"
