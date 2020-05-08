import sys
from app import create_app,db
from flask.cli import FlaskGroup
from dotenv import load_dotenv
from app.api.models import Invited_user,Role

load_dotenv()

app = create_app()
cli = FlaskGroup(create_app = create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(Invited_user( email='admin',invite_code='admin',role_id=0))
    db.session.add(Role(role_name='admin'))
    db.session.add(Role(role_name='supplier'))
    db.session.add(Role(role_name='hub_manager'))
    db.session.add(Role(role_name='packager'))
    db.session.commit()
if __name__ == "__main__":
    cli()