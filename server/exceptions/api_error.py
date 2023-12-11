class ApiError(Exception):
    def __init__(self, status, message, errors=None):
        super().__init__(message)
        self.status = status
        self.errors = errors if errors is not None else []

    @staticmethod
    def unauthorized_error():
        return ApiError(401, 'Пользователь не авторизован')

    @staticmethod
    def bad_request(message, errors=None):
        return ApiError(400, message if message else 'Неверный запрос', errors if errors is not None else [])
