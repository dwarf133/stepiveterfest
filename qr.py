from fileinput import filename
from jinja2 import Template
import pyqrcode
import uuid
import png
from redmail import EmailSender
from smtplib import SMTP_SSL




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



def generate_qr(seed: str) -> str:
    image = pyqrcode.create(
        f'https://fest.stepiveter.ru/check?seed={str(seed)}'
        )
    image.png(f'tmp_img/{seed}.png', scale=5)
    return f'tmp_img/{seed}.png'


if __name__ == '__main__':
    create_ticket('map@stepiveter.ru', '89619332831')
    



    # generate_qr(str(seed)).png('test.png', scale=5)