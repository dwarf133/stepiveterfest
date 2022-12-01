#!/var/www/stepiveterfest/venv/bin/python3
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
from models.time_intervals import TimeIntervals, Guests

guests = Guests.query.filter_by().all()
intervals = [TimeIntervals.select_interval_by_id(guest.interval_id) for guest in guests]
selected = []
for i in range(0, len(guests)):
    if intervals[i].type == 'tattoes':
        selected.append({
            'guest': guests[i],
            'interval': intervals[i]
        })


print(f'Отправить уведомлений: {len(selected)}')

emailsender = EmailSender(
        host="smtp.yandex.ru",
        port=465,
        use_starttls=False,
        cls_smtp=SMTP_SSL,
        username = 'noreply@stepiveter.ru',
        password = 'l0lk@k12'
    )

alias = {
    'tattoes': 'Татуеровки',
    'walk': 'Экскурсия по историческому центру Оренбурга',
    'lambik': 'Шеринг ламбиков',
    'peppers': 'Соревнования по поеданию острых перцев'
} 

t = 0
for temp in selected:

    emailsender.send(
        subject='Напоминание об обязательной покраске тела',
        sender="noreply@stepiveter.ru",
        receivers=[temp['guest'].email],
        html=f"""
        <h1>Степная История</h1>
        <p>Ты записан на {temp['interval'].time} на памятные портачки\n Адресс: Кирова, 5. Угловое здание. З этаж. Вход с угла где магазин Магнит</p>
        """
    )

    t+=1
    print(f"Отправленно {t} из {len(selected)}")