from datetime import datetime

from sqlalchemy import select

from fast_zero.models import Todo, User


def test_create_user(session):
    new_user = User(
        email='test@test',
        name='JRF',
        password='secret',
        avatar='',
        role=1,
        updated_at=datetime.now(),
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.name == 'JRF'))

    assert user.name == 'JRF'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
