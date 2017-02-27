# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/2/14 20:20
"""
from random import Random

from MxOnline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord
from django.core.mail import send_mail


def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    random = Random()
    length = len(chars) -1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "哲商在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号： http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass

    elif send_type == "forget_pwd":
        email_title = "哲商在线网找回密码链接"
        email_body = "请点击下面的链接重设你的密码： http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
