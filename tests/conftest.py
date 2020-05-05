import pytest

from app import create_app,db

@pytest.fixture(scope='function')
def test_app():
    app = create_app()
    app.config.from_object('config.TestingConfig')
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

    