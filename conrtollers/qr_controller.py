from fileinput import filename
import json
import time
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


class Order:

    def get_order(id: int) -> Dict:
        order = None
        try:
            req = request.Request('https://www.botobot.ru/api/v1/orders', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer v1.57678.wIP9pATCDWrtbAuMnkigLxgnN8QSn-LGn_TRq6niSjSjaGuUitFkStxedsDb7nMf' } )
            resp = request.urlopen(req)
            resp_str = resp.read().decode('utf-8')
            order_list = json.loads(resp_str)
        except:
            return order
        for _order in order_list:
            if _order['id'] == id:
                order = _order
        return order

    def __init__(self, id: int) -> None:
        self._data = Order.get_order(id)
    
    @property
    def id(self):
        return self._data['id']
    
    @property
    def mobile(self):
        return self._data['mobile']
    
    @property
    def email(self):
        return self._data['email']

    @property
    def paid(self):
        return self._data['paid']

    @property
    def goods(self):
        return self._data['goods']

    def update_order(self):
        try:
            _updated_order = Order.get_order(self.id)
            if _updated_order != None:
                self._data['paid'] = _updated_order['paid']
        except:
            return


def create_tickets(order: Order) -> bool: 
    
    for t in order.goods:
        type = t['title']
        for i in range(0, t['count']):

    
            seed = uuid.uuid4()    
            
            ticket = Ticket(seed=str(seed), order_id=order.id, email=order.email, phone=order.mobile, ticket_type=type)
            ticket.create()
            """
            ------------------------------
            ?????? ?????????? ????????????
            ?? ???????? str(seed), email, phone
            ------------------------------
            """

            src = generate_qr(str(seed))
            
            email = EmailSender(
                host="smtp.yandex.ru",
                port=465,
                use_starttls=False,
                cls_smtp=SMTP_SSL,
                username = 'noreply@stepiveter.ru',
                password = 'l0lk@k12'
            )   

            email.send(
                subject='???????????? ?????????? ???? ???????? (?????? ????????????????) :(!',
                sender="noreply@stepiveter.ru",
                receivers=[order.email],
                html="""
                <h1>?????????????? ??????????????</h1>
                <p>QR ?????? ?????? ?????????????????? ?????? ???????????????? ?????????? ?? ??????????</p>
                {{ myimg }}
                """,
                body_images={"myimg": src}
            )
            os.remove(src)


def proceed_order(id: int):
    if Ticket.read(id):
        return 
    order = Order(id)
    while True:
        order.update_order()
        if order.paid:
            print(f"Order {id} successeful proceeded")
            create_tickets(order)
            break
        else:
            print(f'Waiting for payment for order {id}') 
            time.sleep(10)



if __name__ == '__main__':
    # set_order_status(334832, 20)
    proceed_order(334884)
