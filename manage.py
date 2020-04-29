import sys
from app import create_app,db
from flask.cli import FlaskGroup
from dotenv import load_dotenv

load_dotenv()

app = create_app()
cli = FlaskGroup(create_app = create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
if __name__ == "__main__":
    cli()