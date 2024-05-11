from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # engine = create_engine('sqlite:///:memory:')
    engine = create_engine(
        'mssql+pymssql://sa:2xeZGam9j9ez4YxEOFMryw@localhost:1433/x3v12db?charset=utf8'
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    user = User(
        name='Teste',
        email='teste@test.com',
        password='testtest',
        role=1,
        avatar='',
        updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
