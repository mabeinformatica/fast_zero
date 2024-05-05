from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(email='test@test', name='JRF')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.name == 'JRF'))

    assert user.name == 'JRF'
