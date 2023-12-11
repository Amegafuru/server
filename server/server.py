from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
from pymongo import MongoClient
from modules.mongo_config import get_mongo_connection_string
from middlewares.error_middleware import error_middleware
from router.index import router
from dotenv import load_dotenv
import os

client_url = os.environ.get('CLIENT_URL')

# Создание экземпляра Flask
app = Flask(__name__)

# Настройка CORS
CORS(app, supports_credentials=True, origins=client_url)

# Загрузка переменных среды из файла .env
port = os.getenv("PORT")
host = os.getenv("API_URL")

# Получение строки подключения и имени базы данных из модуля mongo_config
ATLAS_CONNECTION_URL, ATLAS_DB_NAME, ATLAS_COLLECTION_NAME = get_mongo_connection_string()

# Подключение к серверу MongoDB Atlas
try:
    client = MongoClient(ATLAS_CONNECTION_URL)
    db = client[ATLAS_DB_NAME]  # Выбор базы данных
    print("Подключение к MongoDB Atlas успешно.")
except Exception as e:
    print(f"Ошибка подключения к MongoDB Atlas: {e}")

# Применение маршрутов
app.register_blueprint(router, url_prefix='/api')

# Подключение обработчика ошибок
app.register_error_handler(Exception, error_middleware)

# Роут для обработки API
@app.route('/api/some_endpoint', methods=['GET'])
def get_data():
    collection = db[f"{ATLAS_COLLECTION_NAME}"]  # Укажите имя вашей коллекции в MongoDB

    # Здесь можно выполнять операции с вашей базой данных
    # Например, получить данные из коллекции
    data = list(collection.find())  # Получить все документы из коллекции

    return jsonify(data)
if __name__ == '__main__':
    app.run(host=host, port=port)  # Запуск сервера на порте 5000


# import pymongo
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import jwt
# from datetime import datetime, timedelta

# app = Flask(__name__)
# CORS(app)

# # Подключение к MongoDB по вашей строке подключения
# # Замените '<PASSWORD>' на ваш реальный пароль
# client = pymongo.MongoClient("mongodb+srv://root:Rubchenko5@cluster0.qk1yqon.mongodb.net/?retryWrites=true&w=majority")

# db = client.mydatabase  # Выбор базы данных
# users_collection = db["users"]  # Создание коллекции для пользователей

# # Секретный ключ для подписи токена (можете изменить на свой секретный ключ)
# SECRET_KEY = "your_secret_key"

# # Проверка подключения к базе данных MongoDB
# def check_db_connection():
#     try:
#         client.server_info()  # Проверка, доступен ли сервер MongoDB
#         return True
#     except pymongo.errors.ServerSelectionTimeoutError:
#         return False

# # Маршрут для проверки подключения к базе данных
# @app.route('/check_connection')
# def check_connection():
#     if check_db_connection():
#         return jsonify({'message': 'Подключение к базе данных установлено'}), 200
#     else:
#         return jsonify({'error': 'Ошибка подключения к базе данных'}), 500

# # Маршрут для регистрации нового пользователя
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json  # Получение данных из запроса

#     # Проверка наличия обязательных полей
#     if 'username' not in data or 'email' not in data or 'password' not in data:
#         return jsonify({'error': 'Необходимо указать username, email и password'}), 400

#     # Создание объекта пользователя
#     new_user = {
#         'username': data['username'],
#         'email': data['email'],
#         'password': data['password']  # В реальном приложении пароль нужно хэшировать
#     }

#     # Проверка, существует ли пользователь с таким email
#     existing_user = users_collection.find_one({'email': data['email']})
#     if existing_user:
#         return jsonify({'error': 'Пользователь с этим email уже зарегистрирован'}), 400

#     # Вставка нового пользователя в коллекцию MongoDB
#     result = users_collection.insert_one(new_user)

#     return jsonify({'message': 'Пользователь успешно зарегистрирован', 'user_id': str(result.inserted_id)}), 200

# # Маршрут для входа пользователя и получения токена
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json  # Получение данных из запроса

#     # Проверка наличия обязательных полей
#     if 'email' not in data or 'password' not in data:
#         return jsonify({'error': 'Необходимо указать email и password'}), 400

#     # Проверка существования пользователя с данным email и password
#     user = users_collection.find_one({'email': data['email'], 'password': data['password']})
#     if user:
#         # Генерация токена с данными пользователя
#         token = jwt.encode({'user_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(days=1)}, SECRET_KEY, algorithm='HS256')
#         return jsonify({'token': token})
#     else:
#         return jsonify({'error': 'Неверные email или password'}), 401

# # Маршрут, требующий авторизации
# @app.route('/protected', methods=['GET'])
# def protected():
#     # Получение токена из заголовка Authorization
#     token = request.headers.get('Authorization')

#     if not token:
#         return jsonify({'error': 'Требуется токен для доступа'}), 401

#     try:
#         # Проверка и декодирование токена
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         user_id = decoded['user_id']

#         # Здесь можно добавить логику для работы с защищенным ресурсом

#         return jsonify({'message': 'Доступ разрешен'})
#     except jwt.ExpiredSignatureError:
#         return jsonify({'error': 'Истек срок действия токена'}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({'error': 'Неверный токен'}), 401

# if __name__ == '__main__':
#     app.run(debug=True)