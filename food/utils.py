from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from random import randint
import csv
import os

from django.conf import settings


def save_image_to_folder(image_file):
    fs = FileSystemStorage()
    filename = fs.save(image_file.name, image_file)
    return fs.url(filename)


def send_email(subject, recipient, context):
    html_message = render_to_string("mail/email.html", {"context": context})
    plain_message = strip_tags(html_message)
    result = send_mail(
        subject, plain_message, None, [recipient], html_message=html_message
    )
    if result == 1:
        print("Email was sent")
    else:
        print("Email was not sent")


def send_user_email(subject, recipient, context):
    html_message = render_to_string("mail/user.html", {"context": context})
    plain_message = strip_tags(html_message)
    result = send_mail(
        subject, plain_message, None, [recipient], html_message=html_message
    )
    if result == 1:
        print("Email was sent")
    else:
        print("Email was not sent")


def sanitize(inputstr):
    sanitized = inputstr
    badstrings = [
        ";",
        "$",
        "&&",
        "../",
        "<",
        ">",
        "%3C",
        "%3E",
        "'",
        "--",
        "1,2",
        "\x00",
        "`",
        "(",
        ")",
        "file://",
        "input://",
    ]
    for badstr in badstrings:
        if badstr in sanitized:
            sanitized = sanitized.replace(badstr, "")
    return sanitized


def query_parser(query):
    pass

def search_additifs(query):
    csv_filename = "./data/addd.csv"
    result = None
    with open(csv_filename, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if query in row["code"]:
                result = row
                break

    return result # return result or None


def random_products(products):
    product_list = []
    for i in range(6):
        index = randint(1, len(products) - 1)
        product_list.append(products[index])

    return product_list


def fake_additifs():
    fake_list = []
    tmp_list = []
    csv_filename = "./data/addd.csv"
    with open(csv_filename, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmp_list.append(row)
    for i in range(3):
        fake_list.append(tmp_list[randint(1, len(tmp_list))])
    return(fake_list)
