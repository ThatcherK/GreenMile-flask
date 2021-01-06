import pytest

from app import create_app, db
from app.api.models import Role, Status


def seed_test_db():
    db.session.add(Role(role_name="admin"))
    db.session.add(Role(role_name="supplier"))
    db.session.add(Role(role_name="hub_manager"))
    db.session.add(Role(role_name="packager"))
    db.session.add(Status(name="hub"))
    db.session.commit()


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("config.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_database():
    db.drop_all
    db.create_all()
    seed_test_db()
    yield db
    db.session.remove()
    db.drop_all()
