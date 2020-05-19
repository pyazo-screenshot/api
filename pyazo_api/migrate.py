from os import getenv

from alembic import command
from alembic.config import Config

if not getenv('ENV'):
	from dotenv import load_dotenv
	load_dotenv()

from pyazo_api.config import config  # noqa: E402

alembic_cfg = Config("pyazo_api/alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", config.db.SQLALCHEMY_DATABASE_URI)

command.upgrade(alembic_cfg, "head")
