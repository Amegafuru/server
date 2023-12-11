import bcrypt
import uuid
from models.user_model import UserModel
from service.mail_service import mail_service
from service.token_service import token_service
from dtos.user_dto import UserDto
from exceptions.api_error import ApiError

class UserService:
    async def registration(self, email, password):
        # Предположим, что UserModel.find_one, UserModel.create и mail_service.send_activation_mail определены соответствующим образом
        candidate = UserModel.find_one({"email": email})
        if candidate:
            raise ApiError.BadRequest(f"Пользователь c почтовым адресом {email} уже существует")

        hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(3)).decode()
        activation_link = str(uuid.uuid4())

        user = UserModel.create(email=email, password=hash_password, activation_link=activation_link)
        await mail_service.send_activation_mail(email, f"{process.env.API_URL}/api/activate/{activation_link}")

        user_dto = UserDto(user)  # id, email, isActivated
        tokens = token_service.generate_tokens(user_dto.__dict__)
        await token_service.save_token(user_dto.id, tokens['refreshToken'])

        return {**tokens, "user": user_dto.__dict__}

    async def activate(self, activation_link):
        # Предположим, что UserModel.find_one и UserModel.save определены соответствующим образом
        user = UserModel.find_one({"activation_link": activation_link})
        if not user:
            raise ApiError.BadRequest("Некорректная ссылка активации")

        user.is_activated = True
        await user.save()

    # Остальные методы UserService могут быть реализованы аналогичным образом

# Это примерный код, и вам нужно будет адаптировать его под специфику вашего приложения и использованных библиотек
