import re


def number_is_valid(number):
    is_valid = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', number)
    
    return True if is_valid else False


def fio_is_valid(fio):
    fio = ' '.join(fio)
    is_valid = re.match(r'^[a-zA-Zа-яёА-ЯЁ]+\s[a-zA-Zа-яёА-ЯЁ]+\s[a-zA-Zа-яёА-ЯЁ]+$', fio)
    
    return True if is_valid else False
