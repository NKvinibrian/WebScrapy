from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Models


class ControlMetaData(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Control(metaclass=ControlMetaData):

    def __init__(self):
        DATABASE_URL = 'postgresql://default:YET1NouGyxK5@ep-fragrant-mud-a4igk9fg-pooler.us-east-1.aws.neon.tech/verceldb'
        self.engine = create_engine(DATABASE_URL)

    def create_all_tables(self):
        base = Models.Base
        base.metadata.create_all(bind=self.engine)

    def get_session(self):
        session = sessionmaker(bind=self.engine)
        return session()
