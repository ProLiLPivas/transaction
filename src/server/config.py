import os


class DBConfig:

    HOST = os.environ.get('DB_HOST', '127.0.0.1')
    PORT = os.environ.get('DB_PORT', '5432')
    NAME = os.environ.get('DB_NAME', 'test')
    USER = os.environ.get('DB_USER', 'postgres')
    PASSWORD = os.environ.get('DB_PASSWORD', 'qwerty')
    URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'

