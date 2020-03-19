import os

SECRET = os.getenv('JWT_SECRET', 'jwt-secret')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
