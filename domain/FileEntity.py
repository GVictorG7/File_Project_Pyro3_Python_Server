from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://root:root@localhost/fisiere')


class FileEntity(Base):
    __tablename__ = 'fisiere'
    nume = Column('nume', VARCHAR(30))
    path = Column('path', VARCHAR(100), primary_key=True)
    hash = Column('hash', VARCHAR(129))

    def __init__(self, nume, path, hash):
        self.nume = nume
        self.path = path
        self.hash = hash

    def get_nume(self):
        return self.nume

    def get_path(self):
        return self.path

    def get_hash(self):
        return self.hash

    def to_dict(self):
        return {"nume": self.nume, "path": self.path, "hash": self.hash}


Base.metadata.create_all(engine)
