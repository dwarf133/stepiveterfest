#!/var/www/stepiveter/venv/bin/python3
#-*- coding: utf-8 -*-
from typing import Dict
from urllib import request
from jinja2 import Template
import pyqrcode
import uuid
import png
from redmail import EmailSender
from smtplib import SMTP_SSL
import os
from models.ticket import Ticket


def generate_qr(seed: str) -> str:
    image = pyqrcode.create(
        f'https://fest.stepiveter.ru/check?seed={str(seed)}'
        )
    image.png(f'tmp_img/{seed}.png', scale=5)
    return f'tmp_img/{seed}.png'

EMAILS = ['Orenjane@mail.ru', 'dm3try@gmail.com', 'covereser@gmail.com', 'yungisaev22@mail.ru',\
        'evgenuy.st1994@mail.ru', 'nik-antonenko1998@mail.ru', 'kolras@izh.com', ' a3.kzn@mail.ru.']

emailsender = EmailSender(
        host="smtp.yandex.ru",
        port=465,
        use_starttls=False,
        cls_smtp=SMTP_SSL,
        username = 'noreply@stepiveter.ru',
        password = 'l0lk@k12'
    ) 

for email in EMAILS:
    seed = uuid.uuid4()    

    src = generate_qr(str(seed))  

    emailsender.send(
        subject='Просто билет на фест (без пасхалок) :(!',
        sender="noreply@stepiveter.ru",
        receivers=[email],
        html="""
        <h1>Степная История</h1>
        <p>QR код для посещения дня рождения Степь и Ветер</p>
        {{ myimg }}
        """,
        body_images={"myimg": src}
    )
    os.remove(src)

    ticket = Ticket(seed=str(seed), order_id=666, email=email, phone=666, ticket_type="Flex")
    ticket.create()