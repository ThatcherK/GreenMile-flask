from dotenv import load_dotenv
from flask.cli import FlaskGroup

from app import create_app, db
from app.api.models import Invited_user, Role, Status

load_dotenv()

app = create_app()
cli = FlaskGroup(create_app=create_app)


def create_roles():
    db.session.add(Role(role_name="admin"))
    db.session.add(Role(role_name="supplier"))
    db.session.add(Role(role_name="hub_manager"))
    db.session.add(Role(role_name="packager"))


def create_status():
    db.session.add(Status(name="ordered"))
    db.session.add(Status(name="packing"))
    db.session.add(Status(name="transit"))
    db.session.add(Status(name="delivered"))


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Invited_user(email="admin@mail.com", invite_code="admin", role_id=1))
    create_roles()
    create_status()
    db.session.commit()


if __name__ == "__main__":
    cli()
