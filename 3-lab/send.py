# А, А, Г, А, Б

# 1) Вариант A: Gmail (через SMTP/IMAP с App Password)
# 2) Вариант А: Простое текстовое письмо
# 3) Вариант Г: Генерация случайных тестовых данных
# 4) Вариант A: Поиск писем с определенной темой
# 5) Вариант Б: Отправить автоматический ответ


import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



def generate_random_message():
    subjects = [
        'Привет!',
        'Случайное письмо',
        'Новости дня',
        'Ваш одноразовый код',
        'Проверка связи',
        'Важно!'
    ]
    bodies = [
        'Это тестовое случайное сообщение. Хорошего дня!',
        'Мы просто проверяем отправку писем через SMTP.',
        'Ваш код подтверждения: {code}',
        'Если вы получили это письмо, значит всё работает.',
        'Случайный факт: число сегодня — {code}.',
    ]
    code = random.randint(100000, 999999)
    subject = random.choice(subjects)
    body_template = random.choice(bodies)
    body = body_template.format(code=code)
    return subject, body


def send_email(to_email, subject, body):
    smtp_username = EMAIL_ADDRESS
    smtp_password = EMAIL_PASSWORD
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [to_email], msg.as_string())

if __name__ == '__main__':
    to = EMAIL_ADDRESS
    subj, body = generate_random_message()
    send_email(to, subj, body)
    print(f'Письмо отправлено на {to} с темой: {subj}')