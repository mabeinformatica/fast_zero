from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == user.email))

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already registered',
        )

    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        avatar=user.avatar,
        role=user.role,
        updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User).order_by(User.id).offset(skip).limit(limit)
    ).all()

    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db_user.avatar = user.avatar
    db_user.role = user.role
    db_user.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}')
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
