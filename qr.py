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

from sqlalchemy import false




def create_ticket(email: str, phone: str) -> bool: 
    seed = uuid.uuid4()    
    
    """
    ------------------------------
    тут нужно класть
    в базу str(seed), email, phone
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
        subject='Это билет на фест, долбоклюй!',
        sender="noreply@stepiveter.ru",
        receivers=['map@stepiveter.ru'],
        html="""
        <h1>Hi,</h1>
        <p>have you seen this?</p>
        {{ myimg }}
        """,
        body_images={"myimg": src}
    )
    os.remove(src)


def generate_qr(seed: str) -> str:
    image = pyqrcode.create(
        f'https://fest.stepiveter.ru/check?seed={str(seed)}'
        )
    image.png(f'tmp_img/{seed}.png', scale=5)
    return f'tmp_img/{seed}.png'


def is_order_paid(order: Dict) -> bool:
    if order != None:
        #debug
        # print('ok', order['paid'])
        if order['paid'] == True:
            return True
        else:
            return False
    else:
        return False

# не рабоатет пока
def set_order_status(id: int, status: int):
    # try:
    req = request.Request(f'https://www.botobot.ru/api/v1/updateOrderStatus', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer v1.57678.wIP9pATCDWrtbAuMnkigLxgnN8QSn-LGn_TRq6niSjSjaGuUitFkStxedsDb7nMf' } )
    req.data = json.dumps({'id' : id, 'status' : status}).encode('utf-8')
    resp = request.urlopen(req)
    resp_str = resp.status
    # order_list = json.loads(resp_str)
    # except:
    #     return None
    print(resp_str)


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
        # degug
        # print(_order['id'])
        if _order['id'] == id:
            order = _order
    return order


def proceed_order(id: int):
    while True:
        order = get_order(id)
        if is_order_paid(order):
            print("greate job")
            create_ticket(order['email'], order['mobile'])
            break
        else:
            print('not so good') 
            time.sleep(10)



if __name__ == '__main__':
    set_order_status(334832, 20)
    



    # generate_qr(str(seed)).png('test.png', scale=5)