import re
from django.core.exceptions import ValidationError

def validate_username(username):
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be more than 3 and less than 50 characters"
    elif not username[0].isalpha():
        return False, "Username must start with a letter"
    elif not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, digits, and underscores"
    else:
        return True, "Username is valid"


def validate_email(email):

    ALLOWED_EMAIL_DOMAINS = {
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com",
        "icloud.com", "mail.com", "yandex.ru", "mail.ru", "rambler.ru",
        "bk.ru", "inbox.ru", "list.ru", "zoho.com", "protonmail.com",
        "tutanota.com", "gmx.com", "web.de", "yahoo.co.uk", "yahoo.co.in",
        "yahoo.fr", "yahoo.de", "qq.com", "naver.com", "daum.net", "hanmail.net",
        "rediffmail.com", "seznam.cz", "wp.pl", "o2.pl", "interia.pl",
        "t-online.de", "freenet.de", "gmx.net", "posteo.de"
    }

    if len(email) > 100:
        return False, "Email cannot be longer than 100 characters"
    elif not re.match(r"^[\w\.-]+@([\w\.-]+)$", email):
        return False, "Incorrect email format"
    else:
        domain = email.split("@")[1]
        if domain not in ALLOWED_EMAIL_DOMAINS:
            return False, f'The "{domain}" domain is not allowed'
        else:
            return True, "Email is valid"


def validate_password(password):
    if len(password) < 8 or len(password) > 128:
        return False, "Password must be more than 8 and less than 128 characters"
    elif \
        not re.search(r'[A-Z]', password) \
        or not re.search(r'[a-z]', password) \
        or not re.search(r'[\d]', password) \
        or not re.search(r'[!@#$%^&*()_\-+=\[{\]};:\'",<.>/?\\|`~]', password):
        return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit and one special character"
    return True, "Password is valid"