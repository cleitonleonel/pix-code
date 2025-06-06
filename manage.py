import getpass
import logging
import os
import sys

from alembic import command
from alembic.config import Config
from pix_app.db.base import SessionLocal, init_database
from pix_app.db.models import user_model

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

alembic_versions_path = os.path.join(os.path.dirname(__file__), "alembic/versions")

if not os.path.exists(alembic_versions_path):
    os.mkdir(alembic_versions_path)
    logger.info(f"Created directory: {alembic_versions_path}")


def create_user(is_admin=False):
    username = input("Enter username: ")
    # email = input("Enter email: ")

    while True:
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password == confirm_password:
            break
        else:
            logger.warning("Passwords do not match. Try again.")

    session = SessionLocal()

    user = user_model.User(
        username=username,
        # email=email,
        is_admin=is_admin,
    )
    user.set_password(password)

    session.add(user)
    session.commit()
    logger.info(f"{'Admin' if is_admin else 'User'} created successfully!")


def create_admin():
    return create_user(is_admin=True)


def make_migration(message="New migration"):
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)
    logger.info(f"Migration created with message: {message}")


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Database upgraded to the latest version.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python manage.py <command> [<args>]")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "create_admin":
        create_admin()
    elif arg == "create_user":
        create_user()
    elif arg == "makemigrations":
        description = sys.argv[2] if len(sys.argv) > 2 else "New migration"
        make_migration(description)
    elif arg == "migrate":
        run_migrations()
    elif arg == "create_db":
        init_database()
        logger.info("Database initialized successfully.")
    else:
        logger.error("Unknown command")
