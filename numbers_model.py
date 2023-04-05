from sqlalchemy.exc import IntegrityError

from models import Numbers, session
from service import fio_is_valid, number_is_valid


def set_number(from_user, data):
    fio = [data['last_name'], data['first_name'], data['patronymic']]
    if number_is_valid(data['number']) and fio_is_valid(fio):
        number_obj = Numbers(
            last_name=data['last_name'],
            first_name=data['first_name'],
            patronymic=data['patronymic'],
            number=data['number'],
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
    
    if not response:
        return False
    
    return '\n'.join([f'{i.id} {i.last_name} {i.first_name} {i.patronymic} { i.number}' for i in response])


def get_number(number_id):
    number = session.query(Numbers).get(number_id)
    if not number:
        return False
    
    return number


def edit_number(action, num_id, value=None):
    number = session.query(Numbers).get(num_id)
    if action == 'last_name':
        number.last_name = value
    elif action == 'first_name':
        number.first_name = value
    elif action == 'patronymic':
        number.patronymic = value
    elif action == 'number':
        number.number = value
    elif action == 'delete':
        session.delete(number)
        
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        
    return False
