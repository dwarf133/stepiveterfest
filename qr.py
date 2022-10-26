from fileinput import filename
from jinja2 import Template
import pyqrcode


name = 'kek'
with open('qr_templates/email.html') as file_:
    template = Template(file_.read())
    msg = template.render(name=name)
    print(msg)

text = "https://ya.ru"

image = pyqrcode.create(text)
print(image.terminal())