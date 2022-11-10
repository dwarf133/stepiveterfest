#!/var/www/stepiveter/venv/bin/python3
#-*- coding: utf-8 -*-
from models.ticket import Ticket
from redmail import EmailSender
from smtplib import SMTP_SSL


resp = Ticket.count_tickets()

email = EmailSender(
        host="smtp.yandex.ru",
        port=465,
        use_starttls=False,
        cls_smtp=SMTP_SSL,
        username = 'noreply@stepiveter.ru',
        password = 'l0lk@k12'
    )   

email.send(
    subject='Сводка купленных билетов',
    sender="noreply@stepiveter.ru",
    receivers=['map@stepiveter.ru', 'danila@stepiveter.ru'],
    html=f"""
    <p>
    Flex: {resp['Flex']}</br>
    Supporter: {resp['Supporter']}</br>
    Rampage: {resp['Rampage']}</br>
    </p>
    """
)