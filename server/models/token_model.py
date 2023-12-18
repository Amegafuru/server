from mongoengine import Document, StringField, ReferenceField

class TokenModel(Document):
    user = ReferenceField('user')  # Поле для ссылки на другой документ (User)
    refreshToken = StringField(required=True)  # Строковое поле refreshToken, обязательное для заполнения
