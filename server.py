import pymongo
from flask import Flask, request, jsonify

app = Flask(__name__)

# Подключение к MongoDB по вашей строке подключения
# Замените '<PASSWORD>' на ваш реальный пароль
client = pymongo.MongoClient("mongodb+srv://root:Rubchenko5@cluster0.qk1yqon.mongodb.net/?retryWrites=true&w=majority")

db = client.mydatabase  # Выбор базы данных
users_collection = db["users"]  # Создание коллекции для пользователей

# Проверка подключения к базе данных MongoDB
def check_db_connection():
    try:
        client.server_info()  # Проверка, доступен ли сервер MongoDB
        return True
    except pymongo.errors.ServerSelectionTimeoutError:
        return False

# Маршрут для проверки подключения к базе данных
@app.route('/check_connection')
def check_connection():
    if check_db_connection():
        return jsonify({'message': 'Подключение к базе данных установлено'}), 200
    else:
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 500

# Маршрут для регистрации нового пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Получение данных из запроса

    # Проверка наличия обязательных полей
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Необходимо указать username, email и password'}), 400

    # Создание объекта пользователя
    new_user = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password']  # В реальном приложении пароль нужно хэшировать
    }

    # Проверка, существует ли пользователь с таким email
    existing_user = users_collection.find_one({'email': data['email']})
    if existing_user:
        return jsonify({'error': 'Пользователь с этим email уже зарегистрирован'}), 400

    # Вставка нового пользователя в коллекцию MongoDB
    result = users_collection.insert_one(new_user)

    return jsonify({'message': 'Пользователь успешно зарегистрирован', 'user_id': str(result.inserted_id)}), 200

if __name__ == '__main__':
    app.run(debug=True)