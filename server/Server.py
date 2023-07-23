import json

import Pyro.core
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from repo.FileRepo import FileRepo
from service.FileService import FileService


class Server(Pyro.core.ObjBase):
    def __init__(self, service):
        Pyro.core.ObjBase.__init__(self)
        self.service = service

    def find_all_files(self):
        files = self.service.find_all_files()
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json

    def find_files_containing_substring(self, substring):
        files = self.service.find_files_containing_substring(substring)
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json

    def find_files_by_content_parts_text(self, content):
        files = self.service.find_files_by_content_parts_text(content)
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json

    def find_files_by_content_parts_binary(self, content):
        files = self.service.find_files_by_content_parts_binary(content)
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json

    def find_files_with_duplicate_hash(self):
        files = self.service.find_files_with_duplicate_hash()
        files_json = json.dumps(files, default=lambda x: x.to_dict())
        return files_json


def start():
    connection_string = 'mysql://root:root@localhost/fisiere'
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    conn = engine.connect()
    session = Session(bind=conn)

    file_repo = FileRepo(session)
    service = FileService(file_repo)

    Pyro.core.initServer()
    daemon = Pyro.core.Daemon()
    uri = daemon.connect(Server(service), "exec")
    print("Python Exec Pyro3 waiting with name \"exec\" at: " + str(uri))
    daemon.requestLoop()


if __name__ == "__main__":
    start()
