import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class MailService:
    def __init__(self):
        # Получение учетных данных SMTP из переменных среды
        self.smtp_host = os.getenv('SMTP_HOST')
        self.smtp_port = os.getenv('SMTP_PORT')
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')

        # Создание объекта SMTP и установка соединения
        self.transporter = smtplib.SMTP(self.smtp_host, self.smtp_port)
        self.transporter.starttls()
        self.transporter.login(self.smtp_user, self.smtp_password)

    def send_activation_mail(self, to_email, link):
        # Создание сообщения
        message = MIMEMultipart()
        message['From'] = self.smtp_user
        message['To'] = to_email
        message['Subject'] = 'Активация аккаунта на ' + os.getenv('API_URL')

        # HTML-тело письма
        body = f"""
        <div>
            <h1>Для активации перейдите по ссылке</h1>
            <a href="{link}">{link}</a>
        </div>
        """
        message.attach(MIMEText(body, 'html'))

        # Отправка сообщения
        self.transporter.send_message(message)
