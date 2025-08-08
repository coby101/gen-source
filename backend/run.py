import os
from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

from app import create_app, db
from app.models import FactType, SourceType  # Add more seed table models as needed
from app.seeds.source_types import seed_source_types
from app.seeds.fact_types import seed_fact_types

from app.seed import seed as perform_seed  # ✅ Import the reusable function

from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

app = create_app()

# Initialize database migrations
migrate = Migrate(app, db)

# Seed CLI command
@app.cli.command("seed")
@click.option('--reset', is_flag=True, help='Reset and reseed tables')
@with_appcontext
def seed(reset):
    """Seed essential lookup tables like SourceTypes and FactTypes."""
    if reset:
        click.echo("Resetting and reseeding source_types and fact_types...")
        db.session.query(SourceType).delete()
        db.session.query(FactType).delete()
        db.session.commit()
    else:
        click.echo("Seeding source_types and fact_types if missing...")

    perform_seed()  # ✅ Use the function from app/seed.py
    click.echo("Seeding complete.")


if __name__ == '__main__':
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(debug=debug, host='0.0.0.0', port=5000)
