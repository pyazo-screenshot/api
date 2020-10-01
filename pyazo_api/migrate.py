import logging
from os import getenv

from alembic import command
from alembic.config import Config
from sqlalchemy.exc import OperationalError

if not getenv('ENV'):
    from dotenv import load_dotenv
    load_dotenv()

from pyazo_api.config import config  # noqa: E402

alembic_cfg = Config("pyazo_api/alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", config.db.SQLALCHEMY_DATABASE_URI)
alembic_cfg.set_main_option("script_location", "pyazo_api/alembic")


def run_migration():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    try:
        log.info('Running migrations')
        command.upgrade(alembic_cfg, "head")
    except OperationalError as e:
        log.error('Failed to run migrations')
        log.error(e)
        exit(1)

    log.info('Migrations ran successfully')


if __name__ == "__main__":
    run_migration()
