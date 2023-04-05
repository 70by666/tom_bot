from sqlalchemy.exc import IntegrityError

from models import Numbers, session
from system import fio_is_valid, number_is_valid


def set_number(message):        
    data = message.text.split()[1:]
    if len(data) == 4:
        if number_is_valid(data[3]) and fio_is_valid(data[0:3]):
            number = Numbers(
                last_name=data[0],
                first_name=data[1],
                patronymic=data[2],
                number=data[3],
                who_contributed_id=int(message.from_user.id),
                who_contributed_name=message.from_user.full_name,
            )
            session.add(number)
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
    
    return '\n'.join([f'{i.last_name} {i.first_name} {i.patronymic} { i.number}' for i in response])
