import imaplib
import ssl
import email
from email.header import decode_header
from datetime import datetime, timedelta
from send import send_email, generate_random_message
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



def _decode_header(value):
    if not value:
        return ''
    decoded_parts = decode_header(value)
    fragments = []
    for text, enc in decoded_parts:
        if isinstance(text, bytes):
            try:
                fragments.append(text.decode(enc or 'utf-8', errors='replace'))
            except Exception:
                fragments.append(text.decode('utf-8', errors='replace'))
        else:
            fragments.append(text)
    return ''.join(fragments)


def search_emails_by_subject_last_month(target_subject_substring: str, limit: int = 50):
    target_norm = target_subject_substring.casefold().strip()
    if not target_norm:
        print("Пустая строка поиска.")
        return

    since_date = datetime.now() - timedelta(days=30)
    since_str = since_date.strftime("%d-%b-%Y")

    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL('imap.gmail.com', 993, ssl_context=context) as mail:
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('INBOX')

        status, data = mail.search(None, f'SINCE {since_str}')
        if status != 'OK':
            print("Ошибка при поиске писем.")
            return

        ids = data[0].split()
        if not ids:
            print(f"Нет писем с {since_str}.")
            return

        ids = ids[-limit:] if limit and len(ids) > limit else ids

        found = False
        for num in reversed(ids):
            status, msg_data = mail.fetch(num, '(RFC822.HEADER)')
            if status != 'OK' or not msg_data or not msg_data[0]:
                continue

            headers_bytes = msg_data[0][1]
            message = email.message_from_bytes(headers_bytes)

            subject = _decode_header(message.get('Subject', ''))
            from_header = _decode_header(message.get('From', ''))
            date = _decode_header(message.get('Date', ''))

            if target_norm in subject.casefold():
                found = True
                print("-" * 50)
                print(f"Тема: {subject}")
                print(f"От:   {from_header}")
                print(f"Дата: {date}")
                print()

        to = EMAIL_ADDRESS
        subj, body = generate_random_message()
        send_email(to, "REPLY: " + subj, body)
        print(f'Письмо отправлено на {to} с темой: {subj}')

        if not found:
            print(f"Писем с темой, содержащей '{target_subject_substring}', за последний месяц не найдено.")


if __name__ == '__main__':
    search_term = input("Введите подстроку для поиска в теме письма: ").strip()
    search_emails_by_subject_last_month(search_term, limit=50)