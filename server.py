import pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Подключение к MongoDB по вашей строке подключения
# Замените '<PASSWORD>' на ваш реальный пароль
client = pymongo.MongoClient("mongodb+srv://root:Rubchenko5@cluster0.qk1yqon.mongodb.net/?retryWrites=true&w=majority")

db = client.mydatabase  # Выбор базы данных
users_collection = db["users"]  # Создание коллекции для пользователей

# Секретный ключ для подписи токена (можете изменить на свой секретный ключ)
SECRET_KEY = "your_secret_key"

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

# Маршрут для входа пользователя и получения токена
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Получение данных из запроса

    # Проверка наличия обязательных полей
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Необходимо указать email и password'}), 400

    # Проверка существования пользователя с данным email и password
    user = users_collection.find_one({'email': data['email'], 'password': data['password']})
    if user:
        # Генерация токена с данными пользователя
        token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Неверные email или password'}), 401

# Маршрут, требующий авторизации
@app.route('/protected', methods=['GET'])
def protected():
    # Получение токена из заголовка Authorization
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Требуется токен для доступа'}), 401

    try:
        # Проверка и декодирование токена
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['user_id']

        # Здесь можно добавить логику для работы с защищенным ресурсом

        return jsonify({'message': 'Доступ разрешен'})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Истек срок действия токена'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Неверный токен'}), 401

if __name__ == '__main__':
    app.run(debug=True)