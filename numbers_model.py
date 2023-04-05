from sqlalchemy.exc import IntegrityError

from models import Numbers, session
from system import fio_is_valid, number_is_valid


def set_number(from_user, last_name, first_name, patronymic, number):
    fio = [last_name, first_name, patronymic]
    if number_is_valid(number) and fio_is_valid(fio):
        number_obj = Numbers(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            number=number,
            who_contributed_id=int(from_user.id),
            who_contributed_name=from_user.full_name,
        )
        session.add(number_obj)
        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()

    return False


def get_numbers(field, value):
    if field == 'last_name':
        response = session.query(Numbers).filter(Numbers.last_name == value).all()
    elif field == 'first_name':
        response = session.query(Numbers).filter(Numbers.first_name == value).all()
    elif field == 'patronymic':
        response = session.query(Numbers).filter(Numbers.patronymic == value).all()
    else:
        return False
    
    return '\n'.join([f'{i.id} {i.last_name} {i.first_name} {i.patronymic} { i.number}' for i in response])
