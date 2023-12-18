from mongoengine import Document, StringField, BooleanField

class UserModel(Document):
    # Определение структуры данных пользователя
    email = StringField(unique=True, required=True)  # Поле для электронной почты, уникальное и обязательное для заполнения
    password = StringField(required=True)  # Поле для пароля, обязательное для заполнения
    isActivated = BooleanField(default=False)  # Поле, указывающее активирован ли пользователь, по умолчанию False
    activationLink = StringField()  # Поле для ссылки активации

    meta = {'collection': 'users'}  # Имя коллекции в базе данных MongoDB
