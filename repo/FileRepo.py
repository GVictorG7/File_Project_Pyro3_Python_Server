from domain.FileEntity import FileEntity


class FileRepo:
    def __init__(self, session):
        self.session = session

    def find_all_files(self):
        return self.session.query(FileEntity).all()

    def find_all_files_sorted_by_hash(self):
        return self.session.query(FileEntity).order_by(FileEntity.hash).all()
