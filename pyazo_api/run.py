import os

if not os.getenv('ENV'):
  from dotenv import load_dotenv
  load_dotenv()

from pyazo_api.application import create_app  # noqa: E402
app = create_app()
