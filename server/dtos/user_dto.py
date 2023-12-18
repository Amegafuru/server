class UserDto:
    def __init__(self, model):
        # Инициализация свойств объекта UserDto на основе модели пользователя

        # Присваиваем свойству email значение поля email из модели пользователя
        self.email = model.email

        # Преобразуем значение _id (предполагая, что это ObjectId) в строку и присваиваем свойству id
        self.id = str(model.id)

        # Присваиваем свойству isActivated значение поля isActivated из модели пользователя
        self.isActivated = model.isActivated
