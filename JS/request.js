// Данные для отправки
const userData = {
    username: 'example_username',
    email: 'example@example.com',
    password: 'example_password'
};

// Опции запроса
const requestOptions = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
};

// URL вашего сервера Flask, где находится маршрут '/register'
const registerURL = 'http://127.0.0.1:5000/register'; // Замените на ваш URL

// Отправка запроса
fetch(registerURL, requestOptions)
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }
        return response.json();
    })
    .then(data => {
        console.log('Успешно зарегистрирован пользователь:', data);
        // Здесь вы можете обработать ответ от сервера
    })
    .catch(error => {
        console.error('Ошибка:', error);
        // Обработка ошибки при отправке запроса
    });