"""CLI commands for the haunted database! 👻"""
import os

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import text


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the haunted database! 👻"""
    from app import db

    # Chemin relatif depuis le dossier de l'app
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "SQL")

    click.echo("Creating tables...")
    db.create_all()

    click.echo("Executing schema.sql...")
    with open(os.path.join(sql_dir, "schema.sql")) as f:
        sql_commands = f.read().split(";")
        for command in sql_commands:
            if command.strip():
                db.session.execute(text(command))

    click.echo("Executing seed.sql...")
    with open(os.path.join(sql_dir, "seed.sql")) as f:
        sql_commands = f.read().split(";")
        for command in sql_commands:
            if command.strip():
                db.session.execute(text(command))

    db.session.commit()
    click.echo("Database initialized! 👻")
